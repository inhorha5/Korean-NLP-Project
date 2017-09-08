# WRITTEN IN PYTHON 3.6
# 2017.09.08 InHo (Edward) Rha
# This code was written for personal educational use.


import scraper, lemKR, elastic, summarizer
import time, csv, re
import pandas as pd
import numpy as np
from hdbscan import HDBSCAN
from sklearn.metrics.pairwise import pairwise_distances
from collections import Counter
from multiprocessing import Pool


def Update_and_index_to_ES():
    '''
    Gets new articles that haven't been previously scraped and indexes them to ElasticSearch.
    '''

    # Scrape Latest Articles
    scraper.Update_LatestArticle_ids()
    df = scraper.Update()
    df = lemKR.Create_Lem_Column(df)
    df.to_json('../data/Most_recent_scrape.json', orient='records', date_format="iso")

    # Input data to Elastic Search index
    elastic.Feed_to_ES(df)

    # Update article ids
    scraper.Update_LastUpdatedArticle_ids(scraper.Get_LatestArticle_ids())


def Update_emotion_data():
    '''
    Updates the sentiment data from articles.
    (Only the ones with the scraping timestamp that is within 64 hours of the published timestamp)
    '''

    articleIDs, articleType, esIDs = elastic.Get_articles_to_update_emotions(num_of_articles=10000)
    Emotion_List = []

    p = Pool(10)
    Emotion_List = p.map(scraper.Get_Emotion(articleType[i], articleIDs[i][:3], articleIDs[i][4:]), list(range(len(articleIDs))))
    p.close()

    elastic.Feed_updated_emotions(Emotion_List, esIDs)
    if len(articleIDs) >= 10000:
        Update_emotion_data()


def Query_data(search_string, num_of_articles=1000, date=time.strftime("%Y-%m-%d"), host='localhost', port=9200, index='ko_news_articles'):
    '''
        Input:  String,
                number of related articles to return,
                origin date point (default=now),
                ES host address
                ES port number
                index name
        Output: Tuple (list of search results, list of 'relevance' scores)
    '''

    search_results = elastic.Get_relevant_articles(search_string, num_of_articles=num_of_articles, date=date, host=host, port=port, index=index)
    contents = np.array([search_results[x]['_source'] for x in range(len(search_results))])
    scores = np.array([search_results[x]['_score'] for x in range(len(search_results))])
    return contents, scores


# def Translate(input_text):
#     '''
#         Input: List of strings
#         Output: List of strings
#     ----------------------------------------------------------------------------
#     Translates list of strings through Google Translate
#     requires 'pip install googletrans'
#     '''
#
#     from googletrans import Translator
#     translator = Translator()
#     translated = translator.translate(input_text, src='ko', dest='en')
#     return [translation.text for translation in translated]


def Get_cluster_labels(input_data, Doc2Vec_model):
    '''
        Input: List of Results from search query, pre-loaded Doc2Vec_model (to prevent re-loading each time)
        Output: List of cluster labels
    ----------------------------------------------------------------------------
    '''

    Lem_words = [result_list[x]['Lemmatized'].split() for x in range(len(result_list))]
    vectors = [Doc2Vec_model.infer_vector(document) for document in Lem_words]

    distance = pairwise_distances(vectors, metric='cosine')
    clusterer = HDBSCAN( metric='precomputed', cluster_selection_method='leaf')
    db = clusterer.fit(distance.astype('float64'))
    return db.labels_, db.probabilities_


def Make_word_cloud(input_data, cluster_labels):
    '''
        Input:  List of Results from search query, list of cluster labels
        Output: None
    ----------------------------------------------------------------------------
    Creates and saves a wordcloud for each cluster at '../image_outputs'
    '''

    import pytagcloud
    labels = np.unique(cluster_labels)
    for label in labels:
        content_list = []
        for item in input_data[cluster_labels==label]:
            content_list.append(item['Lemmatized'])
        split_to_words = ' '.join(content_list).split()
        counter = Counter(split_to_words)
        tags = counter.most_common(40)
        taglist = pytagcloud.make_tags(tags, maxsize=80)
        pytagcloud.create_tag_image(taglist, '../image_outputs/wordcloud_'+str(label)+'.png', size=(700, 500), fontname='Korean', rectangular=False, layout=2)


def Make_emotion_graph(input_data, cluster_labels):
    '''
        Input:  List of Results from search query, list of cluster labels
        Output: None
    ----------------------------------------------------------------------------
    Creates and saves a bar graph of the emotion data for each cluster at '../image_outputs'
    '''

    import matplotlib.pyplot as plt
    Emotions = np.array([input_data[x]['Emotion'] for x in range(len(input_data))])
    labels = np.unique(cluster_labels)
    for label in labels:
        Emotion_sum = Counter()
        indexes = [i for i, x in enumerate(cluster_labels==label) if x]
        for index in indexes:
            Emotion_sum += Counter(Emotions[index])
        fig, ax = plt.subplots()
        ax.set_ylabel('Count')
        ax.set_title('Emotion count for cluster #' + str(label))
        # colors = ['#6DC107', 'r', '#2D84E1', '#FF33E0', 'g', '#D9E12D']
        for i, emotion in enumerate(['like', 'angry', 'sad', 'warm', 'want', 'fan']):
            plt.bar(i, Emotion_sum[emotion], align='center')
        ax.set_xticklabels([0, 'like', 'angry', 'sad', 'warm', 'want', 'fan'])
        plt.savefig('../image_outputs/emotions_'+str(label)+'.png')
        plt.close('all')


def Delete_image_output_folder():
    '''
    Deletes all the files inside '../image_outputs'
    '''

    import os, shutil
    folder = '../image_outputs'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


if __name__=="__main__":
    ############## UPDATE DATABASE
    ### For real time updating, create a separate file with these functions and loop them on a interval.
    ### Must edit the functions if the ElasticSearch location isn't 'localhost:9200'
    # Update_emotion_data()
    # Update_and_index_to_ES()

    ############## PRELOAD DOC2VEC MODEL
    from gensim.models import Doc2Vec
    Doc2Vec_model = Doc2Vec.load('../models/ko_Doc2vec_model1')

    ############## SEARCH AND MAP THE RESULTS INTO VECTORSPACE. THEN CLUSTER
    result_list, scores = Query_data('삼성', num_of_articles=1000)
    cluster_labels, label_probabilities = Get_cluster_labels(result_list, Doc2Vec_model)

    ############## MAKE WORDCLOUD AND EMOTION BAR GRAPH
    Delete_image_output_folder()
    Make_word_cloud(result_list, cluster_labels)
    Make_emotion_graph(result_list, cluster_labels)

    ############## OUTPUT UP TO 20 ARTICLE TITLES PER CLUSTER TO '../text_outputs/Output_titles.txt'
    Titles = np.array([result_list[x]['articleTitle'] for x in range(len(result_list))])
    with open("../text_outputs/Output_titles.txt", "w") as text_file:
        writer = csv.writer(text_file,  lineterminator='\n\n', delimiter='\n')
        for label in np.unique(cluster_labels):
            writer.writerow(Titles[cluster_labels==label][:20])

    ############## OUTPUT 3 MOST IMPORTANT SENTENCES PER CLUSTER TO '../text_outputs/Output_sentences.txt'
    ############## WARNING. THIS IS A TIME-CONSUMING PROCESS. NOISE CLUSTER (-1) IS EXCLUDED FROM THE PROCESS
    # from summarizer import TextRank
    # summaries = []
    # s = time.clock()
    # for label in range(0,np.max(cluster_labels)):
    #     contents = '. '.join([result_list[cluster_labels==label][x]['articleContents'] for x in range(len(result_list[cluster_labels==label]))])
    #     textrank = TextRank(contents)
    #     summaries.append(textrank.summarize())
    # with open("../text_outputs/Output_sentences.txt", "w") as text_file:
    #     for item in summaries:
    #         text_file.write(item+'\r\n\r\n')
    # t = time.clock()
    # print(t-s)
