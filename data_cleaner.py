import numpy as np
import pandas as pd
import json
import multiprocessing

# WRITTEN IN PYTHON 3.6
# To launch in Python 2.7, you must specify the encoding method for the file. Even then, no garuntees ¯\_(ツ)_/¯
# 2017.08.23 Edward Rha
# This code is written for personal educational use.

def cutName(df):
    for i in range(df.shape[0]):
        if len(df.loc[i]['Author']) > 3:
            df.set_value(i, 'Author', df.loc[i]['Author'][-3:])
    return df

if __name__ == "__main__":
    ReplaceDict = {'국민일보':'GoodNews paper ⓒ , 무단전재 및 재배포금지',\
                '동아일보':'ⓒ 동아일보 & donga.com, 무단 전재 및 재배포 금지',\
                '문화일보':"[  |  |  ][Copyrightⓒmunhwa.com '대한민국 오후를 여는 유일석간 문화일보' 무단 전재 및 재배포 금지()]",\
                '세계일보':'ⓒ 세상을 보는 눈, 글로벌 미디어 세계일보',\
                '조선일보':'[]- Copyrights ⓒ 조선일보 & chosun.com, 무단 전재 및 재배포 금지 -',\
                '중앙일보':'▶SNS에서 만나는 중앙일보   ⓒ중앙일보 and JTBC Content Hub Co., Ltd. 무단 전재 및 재배포 금지',\
                '한겨례':'▶ 한겨레 절친이 되어 주세요!   [ⓒ한겨레신문 : 무단전재 및 재배포 금지]',\
                '경향신문':'▶ 경향신문 SNS   ▶ ©경향신문(), 무단전재 및 재배포 금지',\
                '서울신문':'▶  재미있는 세상[] ▶ [] []ⓒ 서울신문(), 무단전재 및 재배포금지',\
                '한국일보':'▶한국일보  ▶[ⓒ 한국일보(), 무단 전재 및 재배포 금지]'}

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

    df0 = cutName(df0)
    df8 = cutName(df8)
    df9 = cutName(df9)
    df0.head(1)
    df_month = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7, df8, df9], ignore_index=True)

    for i in range(df_month.shape[0]):
        source = df_month.loc[i]['Source']
        string = ReplaceDict[source]
        df_month.set_value(i, 'Contents', df_month.loc[i]['Contents'].replace(string, ''))

    df_month.to_json('data/Data_1_month.json')
