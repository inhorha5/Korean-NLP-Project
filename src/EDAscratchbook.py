import numpy as np
import pandas as pd
import json
import re
import konlpy
from konlpy.tag import Kkma
from konlpy.utils import pprint
import konlpy.tag as tag
import nltk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

mecab = konlpy.tag.Mecab()
df = pd.read_json('data/Data_1_month.json')

import json, requests
from pandas.io.json import json_normalize

r = requests.get('http://rank.search.naver.com/rank.js')
json_normalize(json.loads(r.text), ['data', 'data'])
json.loads(r.text)['ts']

# test = df.loc[12649]['Contents']

df['Lemmatized'] = ""
for i in range(df.shape[0]):
    Content = df.loc[i]['articleContents']
    df.set_value(i, 'Lemmatized', ' '.join(mecab.nouns(Content)))
    if i%2000 == 0:
        print(i)
temp = df['Lemmatized'].as_matrix()[60000:]

temp = np.append(temp, '트럼프')

tfidf = TfidfVectorizer(max_features = 1000, lowercase=False)

temp2 = tfidf.fit_transform(temp)
Similarity = (temp2*temp2.T).A
Similarity[10591].argsort()[::-1][:10]

df['Contents'].as_matrix()[64162]
df['Contents'].as_matrix()[60000]

df['EventCount'] = df['Contents'].str.len()
df['EventCount'].max()
test
temp = tag.Kkma()
temp.pos(test)
tokens = temp.nouns(test)
tokens
ko = nltk.Text(tokens, name="실험용")

ko.common_contexts('전')
print(len(ko.tokens))
print(len(set(ko.tokens)))
ko.vocab()

kkma = Kkma()
df
Content = df.loc[1070]['Contents']
Content
kkma.nouns(Content)






from collections import Counter
like = []
angry = []
warm = []
sad = []
fan = []
more = []
for i in range(df.shape[0]):
    Emotion_data = Counter(df.loc[i]['Emotion'])
    like.append(Emotion_data['like'])
    angry.append(Emotion_data['angry'])
    warm.append(Emotion_data['warm'])
    sad.append(Emotion_data['sad'])
    fan.append(Emotion_data['fan'])
    more.append(Emotion_data['want'])
np.array(angry).argsort()[::-1][3:]

##########################
