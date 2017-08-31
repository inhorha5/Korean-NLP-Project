# This code is only for manual bootstraping use only.

# This file is meant to create a word2vec model from the pre-processed sentence streams from the articles.

from gensim.models import Word2Vec
import gensim
import numpy as np
import pandas as pd
from multiprocessing import cpu_count
from copy import deepcopy

if __name__ == "__main__":
    bigram = gensim.models.phrases.Phraser.load('../models/phraser')

    file1 = 'only_lem_1.json'
    file2 = 'only_lem_2.json'
    file3 = 'only_lem_3.json'
    file4 = 'only_lem_4.json'
    file5 = 'only_lem_5.json'
    file6 = 'only_lem_6.json'
    file_list = [file1,file2,file3,file4,file5,file6]

    df1 = pd.read_json(file1)
    df2 = pd.read_json(file2)
    df3 = pd.read_json(file3)
    df4 = pd.read_json(file4)
    df5 = pd.read_json(file5)
    df6 = pd.read_json(file6)

    df = pd.concat([df1,df2,df3,df4,df5,df6], ignore_index=True)

    ko2vec_model1 = Word2Vec(df['temp'], size=300, window = 5, min_count=5, workers=cpu_count(), iter=12, sg=0)
    ko2vec_model1.save('../models/ko2vec_model1')
    ko2vec_model1_1 = deepcopy(ko2vec_model1)
    ko2vec_model1_1.save('../models/ko2vec_model1_1')

    ko2vec_model2 = Word2Vec(df['temp'], size=300, window = 7, min_count=5, workers=cpu_count(), iter=12, sg=0)
    ko2vec_model2.save('../models/ko2vec_model2')
    ko2vec_model2_2 = deepcopy(ko2vec_model2)
    ko2vec_model2_2.save('../models/ko2vec_model2_2')

    ko2vec_model3 = Word2Vec(bigram[df['temp']], size=300, window = 5, min_count=5, workers=cpu_count(), iter=12, sg=0)
    ko2vec_model3.save('../models/ko2vec_model3')
    ko2vec_model3_3 = deepcopy(ko2vec_model3)
    ko2vec_model3_3.save('../models/ko2vec_model3_3')

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
