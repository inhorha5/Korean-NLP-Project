from bs4 import BeautifulSoup
from random import random, shuffle
import numpy as np
import pandas as pd
import requests
import time
import csv
import json
import re
import sys
from multiprocessing import Pool, cpu_count

# WRITTEN IN PYTHON 3.6
# 2017.08.28 Edward Rha
# This code is written for personal educational use.
# This code gathers Korean news articles from Naver news.
# This code will shuffle the scraping order and put random delays.

# Set max random delay between scraping
Delay = 0

# example Naver news url: http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=469&aid=0000227942

# fixed variables
source_id_list = ['005', '020', '021', '022', '023', '025', '028', '032', '081', '469']
source_id_names = ['국민일보', '동아일보', '문화일보', '세계일보', '조선일보', '중앙일보', '한겨례', '경향신문', '서울신문', '한국일보']
error = 'error_msg 404'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'}
Latest_update = ['','','','','','','','','','']


def Delayer(input_time):
    """
    Delayer
    """
    Delay = input_time / np.exp(input_time * random())
    # print Delay
    time.sleep(Delay)


def Get_Author(Contents):
    """
        Input: Article contents.
        Returns: Possible Author name, empty string if it doesn't detect.

    Given the article text, this function tries its best extract the author name which isn't always stated.
    Note: Prone to error. It works decently well when author name is properly stated at the end but not always reliable.
    """
    gija = '기자'
    Author = ""
    index = Contents.rfind(gija)
    if (index == -1) or ((index) < (len(Contents)*2/3)):
        return Author
    else:
        regex = r'.*\.+.*?\s*?\w*?\s*?(' + '[가-힣]' + r'+)\s*\w*' + gija
        p = re.compile(regex, re.UNICODE)
        if len(Contents) > 300:
            Contents = '.' + Contents[len(Contents)-300:]
        try:
            Author = p.match(Contents).group(1)
        except AttributeError:
            Author = ""
    return Author


def cutAuthor(df):
    """
        Input: Pandas DataFrame
        Output: Pandas DataFrame

    Cuts author's name to the last 3 characters. (Since Korean names almost never go over 3 characters)
    Only use for specific news outlets that benefits from this cut.
    """
    for i in range(df.shape[0]):
        if len(df.loc[i]['articleAuthor']) > 3:
            df.set_value(i, 'articleAuthor', df.loc[i]['articleAuthor'][-3:])
    return df


def Get_Emotion(A_type, source_id, article_id):
    """
        Input: Article type (NEWS, SPORTS, ENTERTAIN), source id (ex. '005'), article_id (ex. '0001013323')
        Output: dictionary containing the emotion data.

    Queries the site for the emotion data.
    ex: {'angry':5, 'like':1}
    emotion types: {u'angry', u'like', u'sad', u'want', u'warm', u'fan'}
    """
    Emotion_link = 'http://news.like.naver.com/v1/search/contents?&q=' + A_type + '%5Bne_' + source_id + '_' + article_id + '%5D'
    Emotion_string = requests.get(Emotion_link, headers=headers)
    Emotion_string = json.loads(Emotion_string.content)['contents'][0]['reactions']
    Emotion_dict = dict()
    for item in Emotion_string:
        Emotion_dict[item['reactionType']] = item['count']
    return Emotion_dict


def Get_LatestArticle_ids():
    """
        Output: list of strings

    Returns the ids for the most recent articles for each of the
    ex: ['0003130302', '00003023044', ...]
    """
    Output = []
    for source in source_id_list:
        link = "http://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=" + source
        r = requests.get(link, headers=headers)
        article_soup = BeautifulSoup(r.content, 'html.parser')
        article_id = article_soup.select('.type06_headline a[href]')[0]
        Output.append(article_id.attrs['href'][-10:])
    return Output


def Get_LastUpdatedArticle_ids():
    """
        Output: list of strings

    Returns the last updated article ids from 'logs/last_update.csv'
    """
    Output = []
    with open("../logs/last_update.csv", "r") as text_file:
        reader = csv.reader(text_file)
        for row in reader:
            Output.append(row)
    return Output[0]


def Update_LastUpdatedArticle_ids(ID_List):
    """
        Input: list of strings
    ex: ['0003130302', '0003023044', ...]
    Updates the last updated article ids to 'logs/last_update.csv'
    """
    with open("../logs/last_update.csv", "w") as text_file:
        writer = csv.writer(text_file,  lineterminator='\n')
        writer.writerow(ID_List)


def Update_new_articles_to_data(source_index_number):
    """
        Input: Source number
        Output: Pandas DataFrame

    Scrapes new articles for the chosen source number and creates a DataFrame
    """
    starting_position = Get_LastUpdatedArticle_ids()[source_index_number]
    end_position = Get_LatestArticle_ids()[source_index_number]
    Latest_update[source_index_number] = end_position
    aid_list = list(range(int(starting_position), int(end_position)))
    shuffle(aid_list)
    progress_tracker = 0
    errorlist = []
    exceptionlist = []
    df = pd.DataFrame(columns=['NewsOutlet', 'articleTitle', 'articleDate', 'articleAuthor', 'articleContents', 'articleID', 'Category', 'Emotion', 'Emotion_date'])
    df['Emotion_date'] = df['Emotion_date'].astype('datetime64[ns]')
    df['articleDate'] = df['articleDate'].astype('datetime64[ns]')

    for i in aid_list:
        i = str(i)
        while len(i) < 10:
            i = '0' + i

        # information to retrieve
        title = ''
        Date = ''
        Author = ''
        Contents = ''
        A_type = ''
        Emotion = {}

        # Call article source
        article_id = i
        link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=' + source_id_list[source_index_number] + '&aid=' + article_id
        r = requests.get(link, headers=headers)

        # Check which charset. For future use.
        decode_type = "utf-8"
        if r.text.lower().find('charset="utf-8"') == -1:
            decode_type = "cp949"

        # Removed Articles
        if r.text.find(error) != -1:
            # errorlist.append(i)
            continue
        # Articles with ENTERTAIN template
        elif r.text.find('data-sid="ENTERTAIN"') != -1:
            A_type = 'ENTERTAIN'
            article_soup = BeautifulSoup(r.content, 'html.parser')
            title = article_soup.select('.end_tit')[0].text.replace("\t", "").replace("\n",'')
            Date = article_soup.select('.article_info em')[0].text
            for i, char in enumerate(Date):
                if char.isdigit():
                    Date = Date[i:]
                    break;
            Date = Date.replace(".", "-")
            if Date.find('오전')!=-1:
                Date = Date.replace('오전 ','')
            elif Date.find('오후')!=-1:
                Date = Date.replace('오후 ', '') + ' PM'
                Date = pd.to_datetime(Date).strftime('%Y-%m-%d %H:%M:%S')
            [s.extract() for s in article_soup('script')]
            [s.extract() for s in article_soup('a')]
            [b.replace_with("%s " % b.text) for b in article_soup('br')]
            Contents = article_soup.select('#articeBody')[0].text.replace("\t", "").replace("\n",' ')
            Contents = ' '.join(Contents.split())
            Author = Get_Author(Contents)
            Emotion = Get_Emotion(A_type, source_id_list[source_index_number], article_id)
        # Articles with SPORTS template
        elif r.text.find('data-sid="SPORTS"') != -1:
            A_type = 'SPORTS'
            article_soup = BeautifulSoup(r.content, 'html.parser')
            title = article_soup.select('title')[0].text.replace("\t", "").replace("\n",'')
            Date = article_soup.select('.info span')[0].text
            for i, char in enumerate(Date):
                if char.isdigit():
                    Date = Date[i:]
                    break;
            Date = Date.replace(".", "-")
            if Date.find('오전')!=-1:
                Date = Date.replace('오전 ','')
            elif Date.find('오후')!=-1:
                Date = Date.replace('오후 ', '') + ' PM'
                Date = pd.to_datetime(Date).strftime('%Y-%m-%d %H:%M:%S')
            [s.extract() for s in article_soup('script')]
            [s.extract() for s in article_soup('a')]
            [b.replace_with("%s " % b.text) for b in article_soup('br')]
            Contents = article_soup.select('#newsEndContents')[0].text.replace("\t", "").replace("\n",' ')
            Contents = ' '.join(Contents.split())
            Emotion = Get_Emotion(A_type, source_id_list[source_index_number], article_id)
            Author = Get_Author(Contents)
        # Default Article template
        elif r.text.find('data-sid="NEWS"') != -1:
            A_type = 'NEWS'
            article_soup = BeautifulSoup(r.content, 'html.parser')
            title = article_soup.select('#articleTitle')[0].text.replace("\t", "").replace("\n",'')
            Date = article_soup.select('.article_header .t11')[0].text
            for i, char in enumerate(Date):
                if char.isdigit():
                    Date = Date[i:]
                    break;
            Date = Date[:16] + ':00'
            [s.extract() for s in article_soup('script')]
            [s.extract() for s in article_soup('a')]
            [b.replace_with("%s " % b.text) for b in article_soup('br')]
            Contents = article_soup.select('#articleBodyContents')[0].text.replace("\t", "").replace("\n",' ')
            Contents = ' '.join(Contents.split())
            Emotion = Get_Emotion(A_type, source_id_list[source_index_number], article_id)
            Author = Get_Author(Contents)
        else:
            # exceptionlist.append(i)
            continue

        article_id = source_id_list[source_index_number] + '_' + article_id
        df.loc[df.shape[0]] = [source_id_names[source_index_number], title, Date, Author, Contents, article_id, A_type, Emotion, pd.to_datetime('today')]
        progress_tracker+=1
        Delayer(Delay)
    df['articleDate'] = pd.to_datetime(df['articleDate'])
    df['Emotion_date'] = pd.to_datetime(df['Emotion_date'])
    return df


def Update():
    """
        Output: Pandas DataFrame

    Returns the new articles since last update.
    """
    df_list = []
    p = Pool(4)
    df_list = p.map(Update_new_articles_to_data, list(range(len(source_id_list))))
    Update_LastUpdatedArticle_ids(Latest_update)

    # for i in range(len(source_id_list)):
    #     df_list.append(Update_new_articles_to_data(i))
    df_list[0] = cutAuthor(df_list[0])
    df_list[8] = cutAuthor(df_list[8])
    df_list[9] = cutAuthor(df_list[9])
    df_all = pd.concat(df_list, ignore_index=True)
    ReplaceDict = {'국민일보':'GoodNews paper ⓒ',\
                '동아일보':'ⓒ 동아일보',\
                '문화일보':"[ | | ] [Copyrightⓒmunhwa.com",\
                '세계일보':'ⓒ 세상을 보는 눈',\
                '조선일보':'[] - Copyrights ⓒ',\
                '중앙일보':'▶SNS에서 만나는 중앙일보',\
                '한겨례':'▶ 한겨레',\
                '경향신문':'▶ 경향신문',\
                '서울신문':'▶ 재미있는',\
                '한국일보':'▶한국일보'}
    for i in range(df_all.shape[0]):
        source = df_all.loc[i]['NewsOutlet']
        string = ReplaceDict[source]
        location = df_all.loc[i]['articleContents'].find(string)
        df_all.set_value(i, 'articleContents', df_all.loc[i]['articleContents'][:location])
    return df_all
