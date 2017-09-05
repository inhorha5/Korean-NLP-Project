import pandas as pd
from konlpy.tag import Mecab

# WRITTEN IN PYTHON 3.6
# 2017.08.28 Edward Rha
# This code is written for personal educational use.

def ko_lemmatize(inputString):
    """
        Input: string (Korean)
        Output: string (Korean)
    Takes in a sentence or a document and returns the lemmatized version of it.
    Returns only parts of speech that was tagged as Noun or Verb.
    Due to the challenges and limitations regarding parts-of-speech tagging in Korean, the output may not parse as expected.
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
    return ' '.join(Lem_temp)

def ko_lemmatize_nouns(inputString):
    """
        Input:  string (Korean)
        Output: list of strings (Korean)
    Returns only noun words.
    """
    mecab = Mecab()
    return mecab.nouns(inputString)

def Create_Lem_Column(df):
    """
        Input: Pandas DataFrame
        Output: Pandas DataFrame
    Takes in a Pandas DataFrame and creates an 'Lemmatized' column.
    """
    from multiprocessing import Pool, cpu_count
    df['Lemmatized'] = ""
    p = Pool(cpu_count())
    results = p.map(ko_lemmatize, df['articleContents'] + ' ' + df['articleTitle'])
    p.close()
    df['Lemmatized'] = results
    return df
if __name__=='__main__':
    __spec__ = None
