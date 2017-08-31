# This code is only for manual bootstraping use only.

# This file is meant to create a Doc2vec model from the Korean news articles.
if __name__ == "__main__":
    from gensim.models import Doc2Vec
    import gensim
    import pandas as pd
from multiprocessing import cpu_count, Pool
from konlpy.tag import Mecab

def ko2vec_ko_lemmatize(inputString):
    """
        Input: string
        Output: list of split words
    Takes in a document and returns the lemmatized+split version of it.
    """
    mecab = Mecab()
    tag_set = {'N', 'V'}
    temp = mecab.pos(inputString)
    Lem_temp = []
    for pair in temp:
        if pair[1][0] in tag_set:
            Lem_temp.append(pair[0])
        elif pair[1] == 'SL':
            Lem_temp.append(pair[0])
    del temp
    del inputString
    return Lem_temp

class LabeledLineSentence(object):
    def __init__(self, articles, labels):
        bigram = gensim.models.phrases.Phraser.load('../models/phraser')
        self.articles = list(bigram[articles])
        self.labels = labels

    def __iter__(self):
        for i in range(len(self.articles)):
            yield gensim.models.doc2vec.TaggedDocument(words=self.articles[i], tags=[self.labels[i]])
    def __len__(self):
        return len(self.labels)


if __name__ == "__main__":
    data_path = '../data/Data_1_year.json'

    df1 = pd.read_json('1.json', orient='records', dtype={"articleID":'object', "articleDate":"datetime64[ns]"})
    df2 = pd.read_json('2.json', orient='records', dtype={"articleID":'object', "articleDate":"datetime64[ns]"})
    df = pd.concat([df1,df2],ignore_index=True)

    list_label = list(df['articleID'])
    # list_articleContents = df['articleContents'].str.replace('["#%\'()*+,/:;<=>@\[\]^_`{|}~’”“′‘\\\.!?『』 ]+', ' ')
    #
    # p = Pool(int(cpu_count()/2))
    # results = p.map(ko2vec_ko_lemmatize, list_articleContents)
    list_articleContents = list(df['articleContents'])


    tag_stream = LabeledLineSentence(list_articleContents, list_label)

    print('started')
    model = Doc2Vec(tag_stream, alpha=0.05, min_alpha=0.025, window=15, size=50, iter=15, min_count=5, workers=cpu_count())
    model.save('../models/ko_Doc2vec_model1')
    # model.docvecs.save()
    print('one done')

    model2 = Doc2Vec(tag_stream, alpha=0.1, min_alpha=0.025, window=10, size=50, iter=15, min_count=5, workers=cpu_count())
    model2.save('../models/ko_Doc2vec_model2')
    print('two done')

    model3 = Doc2Vec(tag_stream, alpha=0.05, min_alpha=0.025, window=15, size=50, iter=40, min_count=5, workers=cpu_count())
    model.save('../models/ko_Doc2vec_model3')

    model_test = Doc2Vec.load('deep_copy')
    Doc2Vec.
    model.docvecs.most_similar(['005_1017333'])
    model_test.most_similar(['005_1017333'])
    model_test = model_test.docvecs.load('doc_vec_save3')
    model_test.mo

    a

    #
    # tag_stream = LabeledLineSentence([['이것은', '하나의', '실험입니다']],['문서1번'])
    # model = Doc2Vec(tag_stream,  alpha=0.05, min_alpha=0.025, window=15, size=50, iter=15, min_count=0, workers=cpu_count())
    # model.corpus_count
    # tag_stream = LabeledLineSentence([['다른', '두번째', '실험임']],['문서3번'])
    # model.build_vocab(tag_stream, update=True)
    # model.train(tag_stream, total_examples=model.docvecs.count, epochs=model.iter)

    #
    # print(df.loc[7301]['articleTitle'])
    # vector = model.infer_vector(tag_stream[7301])
    # for item in model.docvecs.most_similar([vector]):
    #     print(item[1],item[0], df[df['articleID']==item[0]]['articleTitle'])
    #
    # vector = model2.infer_vector(results[51343])
    # for item in model2.docvecs.most_similar([vector]):
    #     print(item[1],item[0], df[df['articleID']==item[0]]['articleTitle'])
    #
    # vector = model.infer_vector(results[23503])
    # print(model.docvecs.most_similar([vector]))
    # print(model2.docvecs.most_similar([vector]))
    #
    # model2.train(tag_stream, epochs=10, total_examples=model2.corpus_count)

    # FOR NEW ARTICLES
    # model = Doc2Vec.load('file')
    # model.build_vocab(new_article_tagged, update=True)
    # model.train(new_article_tagged, total_examples=model.docvecs.count, epochs=model.iter)







    #
    # ko2vec_model = None
    # first = 1
    # for name in file_list:
    #     df = pd.read_json(name)
    #     if first==1:
    #         first = 0
    #         ko2vec_model = Word2Vec(df['temp'], size=300, window = 5, min_count=5, workers=cpu_count(), iter=12, sg=0)
    #     else:
    #         ko2vec_model.build_vocab(df['temp'], update=True)
    #         ko2vec_model.train(df['temp'], total_examples=ko2vec_model.corpus_count, epochs=ko2vec_model.iter)
    #
    #
    #     print('One Training Done')
    #
    # ko2vec_model.save('../models/ko2vec_model2')
    # ko2vec_model3 = deepcopy(ko2vec_model)
    # ko2vec_model3.save('../models/ko2vec_model3')
