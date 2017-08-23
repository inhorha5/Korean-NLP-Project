import numpy as np
import pandas as pd
import json
import re
import konlpy
from konlpy.tag import Kkma
from konlpy.utils import pprint


kkma = Kkma()
df
Content = df.loc[1070]['Contents']
Content
kkma.nouns(Content)


def cutName(df):
    for i in range(df.shape[0]):
        if len(df.loc[i]['Author']) > 3:
            df.set_value(i, 'Author', df.loc[i]['Author'][-3:])
    return df

if __name__ == "__main__":
    df0 = pd.read_json('data/Data_005_1011000~1019559.json') # CUT
    df1 = pd.read_json('data/Data_020_3081000~3088691.json')
    df2 = pd.read_json('data/Data_021_2321500~2324813.json')
    df3 = pd.read_json('data/Data_022_3194000~3202400.json')
    df4 = pd.read_json('data/Data_023_3299500~3306675.json')
    df5 = pd.read_json('data/Data_025_2738000~2747105.json')
    df6 = pd.read_json('data/Data_028_2373032~2376732.json')
    df7 = pd.read_json('data/Data_032_2804500~2812318.json')
    df8 = pd.read_json('data/Data_081_2840000~2847019.json') # CUT
    df9 = pd.read_json('data/Data_469_219945~227943.json') # CUT

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

df.loc[3498]
