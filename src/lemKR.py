import pandas as pd
from konlpy.tag import Mecab
from multiprocessing import Pool, cpu_count

# WRITTEN IN PYTHON 3.6
# 2017.08.28 Edward Rha
# This code is written for personal educational use.

def ko_lemmatize(inputString):
    """
        Input: string (Korean)
        Output: string (Korean)
    Takes in a sentence or a document and returns the lemmatized version of it. Returns only nouns.
    """
    mecab = Mecab()
    Lemmatized_String = ' '.join(mecab.nouns(inputString))
    return Lemmatized_String

def Create_Lem_Column(df):
    """
        Input: Pandas DataFrame
        Output: Pandas DataFrame
    Takes in a Pandas DataFrame and creates an 'Lemmatized' column.
    """
    df['Lemmatized'] = ""
    p = Pool(cpu_count())
    results = p.map(ko_lemmatize, df['articleContents'] + ' ' + df['articleTitle'])
    df['Lemmatized'] = results
    return df
