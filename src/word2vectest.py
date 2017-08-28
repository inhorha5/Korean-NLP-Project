from gensim.models import Word2Vec
import numpy as np
import pandas as pd
import konlpy
from konlpy.tag import Mecab
from multiprocessing import Pool, cpu_count
import time
import gensim

def ko_lemmatize(inputString):
    mecab = Mecab()
    Lemmatized_String = ' '.join(mecab.pos(inputString)[0])
        # if i%10000 == 0 :
        #     print(i)
    return Lemmatized_String



df = pd.read_json('data/Data_1_month.json')

mecab = Mecab()
Lem_list = []
for i in range(df.shape[0]):
    sentences = df.loc[i]['articleContents'].split('.')
    Lem_sent_list = []
    for sentence in sentences:
        Lem_temp = mecab.morphs(sentence)
        Lem_sent_list.append(Lem_temp)
    Lem_list.append(Lem_sent_list)

    # Lem_list.append(Lem_temp)
flat_list = [item for sublist in Lem_list for item in sublist]
# len(flat_list)
flat_list[1]

s = time.clock()
embedding_model2 = Word2Vec(flat_list, size=100, window = 5, min_count=50, workers=8, iter=5, sg=1)
t = time.clock()
print(t-s)

s = time.clock()
embedding_model = Word2Vec(flat_list, size=100, window = 5, min_count=5, workers=8, iter=10, sg=0)
t = time.clock()
print(t-s)


print(embedding_model2.most_similar(positive=['카카오','뱅크'], negative=[], topn=5))
