# WRITTEN IN PYTHON 3.6
# 2017.09.08 InHo (Edward) Rha
# This code was written for personal educational use.


from elasticsearch import Elasticsearch, helpers
import json
import time
from konlpy.tag import Mecab


def Feed_to_ES(df, host='localhost', port=9200, index='ko_news_articles', input_type='news_article'):
    '''
        Input:  Pandas DataFrame (Required)
                ES host address
                ES port number
                index name
                input_type name
        Output: None
    ----------------------------------------------------------------------------
    Takes in the scraped data from DataFrame and indexes it to ElasticSearch
    '''

    es = Elasticsearch([{'host': host, 'port': port}])
    data = df.to_json(orient='records', date_format="iso")
    data = json.loads(data)
    data_feed = [{'_index':index, '_type': input_type, '_source':data[j]} for j in range(len(data))]

    helpers.bulk(es, data_feed)


def Get_relevant_articles(search_string, num_of_articles=1000, date=time.strftime("%Y-%m-%d"), host='localhost', port=9200, index='ko_news_articles'):
    '''
        Input:  String (Required)
                max number of related articles to return
                date origin point parameter (default=now)
                ES host address
                ES port number
                index name
        Output: list of dictionaries containing the article infos, index id, similarity score, etc.
    ----------------------------------------------------------------------------
    '''

    mecab = Mecab()
    search_string_lem = ' '.join(mecab.nouns(search_string))
    es = Elasticsearch([{'host': host, 'port': port}])

    Output = es.search(index=index, size=num_of_articles, body={'query': \
                                    {'function_score': \
                                        {'query':\
                                            {'dis_max':\
                                                {'queries': [\
                                                    {'match': {'articleContents': {'query':search_string, 'fuzziness': 'AUTO', 'max_expansions':5, "cutoff_frequency" : 0.001}}},\
                                                    {'match': {'Lemmatized': {'query':search_string_lem, 'fuzziness': 0, 'max_expansions':2, "cutoff_frequency" : 0.001}}}],\
                                                "tie_breaker":0.3\
                                                }\
                                            },\
                                        "functions":\
                                            [{"gauss":\
                                                {"articleDate":\
                                                    {"origin":date,\
                                                    "scale":"30d",\
                                                    "offset":"2d",\
                                                    "decay": .5 \
                                                    }\
                                                }\
                                            }],\
                                            "score_mode":"multiply"\
                                        }\
                                    }\
                                })

    return Output['hits']['hits']


def Get_recent_articles(date=time.strftime("%Y-%m-%d"), host='localhost', port=9200, num_of_articles=10000, index='ko_news_articles'):
    '''
        Returns the top 10000 most recent articles
    '''

    es = Elasticsearch([{'host': host, 'port': port}])
    Output = es.search(index=index, size=num_of_articles, body={'query': \
                                    {'function_score': \
                                        {"functions":\
                                            [{"gauss":\
                                                {"articleDate":\
                                                    {"origin":date,\
                                                    "scale":"30d",\
                                                    "decay": .5 \
                                                    }\
                                                }\
                                            }],\
                                            "score_mode":"multiply"\
                                        }\
                                    }\
                                })
    return Output['hits']['hits']


def Get_articles_to_update_emotions(host='localhost', port=9200, num_of_articles=10000, index='ko_news_articles'):
    '''
        Returns up to 10000 articles that should have their emotion data updated.
        (Articles that were scraped within 64 hours of posting. 48 hours + 16 hours timezone difference)
    '''

    es = Elasticsearch([{'host': host, 'port': port}])
    Output = es.search(index=index, size=num_of_articles, body={\
                                    "query" : {\
                                        "bool": {\
                                            "filter":[{
                                                "script" : {"script": "(doc['Emotion_date'].value - doc['articleDate'].value) <= 17280000"}\
                                            }]
                                        }\
                                    }\
                                })
    return [X['_source']['articleID'] for X in Output['hits']['hits']], [X['_source']['Category'] for X in Output['hits']['hits']], [X['_id'] for X in Output['hits']['hits']]


def Feed_updated_emotions(EMOTIONLIST, DOC_IDS, host='localhost', port=9200, index='ko_news_articles'):
    '''
        Input:  list of dictionaries containing emotion data
                list of unique document ids for elasticsearch indicies
        Output: None
    ----------------------------------------------------------------------------
    Updates the newly queried emotion-data to ES database.
    '''
    
    date=time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    es = Elasticsearch([{'host': host, 'port': port}])
    for i in range(len(EMOTIONLIST)):
        es.update(index=index,doc_type='news_article',id=DOC_IDS[i],
                    body={"doc": {"Emotion": EMOTIONLIST[i], "Emotion_date": date }})


if __name__=='__main__':
    __spec__ = None
