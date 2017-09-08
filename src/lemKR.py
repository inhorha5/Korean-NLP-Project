# WRITTEN IN PYTHON 3.6
# 2017.09.08 InHo (Edward) Rha
# This code was written for personal educational use.


import pandas as pd
from konlpy.tag import Mecab


def ko_lemmatize(inputString):
    '''
        Input: string
        Output: string
    ----------------------------------------------------------------------------
    Takes in a sentence or a document string and returns the lemmatized version of it.
    Returns only parts of speech that was tagged as Noun or Verb.
    !!! Due to the challenges and limitations regarding parts-of-speech tagging in Korean, the output may not parse as expected.
    '''

    mecab = Mecab()
    tag_set = {'N', 'V'}
    temp = mecab.pos(inputString)
    Lem_temp = []
    for pair in temp:
        if pair[1][0] in tag_set:
            Lem_temp.append(pair[0])
        elif pair[1] == 'SL':
            Lem_temp.append(pair[0])
    return ' '.join(Lem_temp)


def ko_lemmatize_nouns(inputString):
    '''
        Input:  string (Korean)
        Output: list of strings (Korean)
    ----------------------------------------------------------------------------
    Returns list of nouns from the input.
    '''
    mecab = Mecab()
    return mecab.nouns(inputString)


def Create_Lem_Column(df):
    '''
        Input: Pandas DataFrame
        Output: Pandas DataFrame
    ----------------------------------------------------------------------------
    Takes in a Pandas DataFrame and creates an 'Lemmatized' column.
    '''
    from multiprocessing import Pool, cpu_count
    df['Lemmatized'] = ""
    p = Pool(cpu_count())
    results = p.map(ko_lemmatize, df['articleContents'] + ' ' + df['articleTitle'])
    p.close()
    df['Lemmatized'] = results
    return df


if __name__=='__main__':
    __spec__ = None
