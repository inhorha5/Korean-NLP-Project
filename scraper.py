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

# WRITTEN IN PYTHON 2.7
# 2017.08.22 Edward Rha
# This code is written only for my own educational use to gather Korean news articles from naver news.

# example target: http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=469&aid=0000227942
# target variables
source_id_list = ['005', '020', '021', '022', '023', '025', '028', '032', '081', '469']
source_id_names = [u'\uAD6D\uBBFC\uC77C\uBCF4', u'\uB3D9\uC544\uC77C\uBCF4', u'\uBB38\uD654\uC77C\uBCF4',\
                    u'\uC138\uACC4\uC77C\uBCF4', u'\uC870\uC120\uC77C\uBCF4', u'\uC911\uC559\uC77C\uBCF4',\
                    u'\uD55C\uACA8\uB840', u'\uACBD\uD5A5\uC2E0\uBB38', u'\uC11C\uC6B8\uC2E0\uBB38', u'\uD55C\uAD6D\uC77C\uBCF4']

source_target_prefix = ["0000", "000", "000", "000", "000", "000", "000", "000", "000", "0000"]
source_target_1year = [929000, 3000000, 2281500, 3090000, 3259000, 2639651, 2330000, 2714500, 2740000, 160000]
source_target_end_1year = [999999, 3080999, 2321499, 3193999, 3299499, 2737999, 2373031, 2804499, 2839999, 219944]
delay_list = [0.8, 0.65, 3.0, 0.45, 2.5, 0.5, 2.4, 0.55, 0.5,  1.1]

# 5 will finish first, theoretically
target = int(sys.argv[1])
source_id = source_id_list[target]
source_name = source_id_names[target] # Name of news source in Korean to save to database
print(source_name)
a_id_prefix = source_target_prefix[target]
start_id_int = source_target_1year[target]
end_id_int = source_target_end_1year[target]
Delay = delay_list[target]

# global
error = 'error_msg 404'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'}

def Delayer(input_time):
    Delay = input_time / np.exp(input_time * random())
    # print Delay
    time.sleep(Delay)

def Get_Author(Contents):
    gija = '\xea\xb8\xb0\xec\x9e\x90'
    Author = ""
    index = Contents.encode('utf-8').rfind(gija)
    if (index == -1) or ((index) < (len(Contents.encode('utf-8'))-200)):
        return Author
    else:
        regex = r'.*\.+.*?\s?\w*?\s?(' + '[\xea\xb0\x80-\xed\x9e\xa3]' + r'+)\s*\w*' + gija
        p = re.compile(unicode(regex,'utf-8'), re.UNICODE)
        if len(Contents) < 500:
            Contents = Contents[len(Contents)-100:]
        try:
            Author = p.match(Contents).group(1)
        except AttributeError:
            Author = ""
    return Author

# {u'angry', u'like', u'sad', u'want', u'warm', u'fan'}
def Get_Emotion(A_type, source_id, article_id):
    Emotion_link = 'http://news.like.naver.com/v1/search/contents?&q=' + A_type + '%5Bne_' + source_id + '_' + article_id + '%5D'
    Emotion_string = requests.get(Emotion_link, headers=headers)
    Emotion_string = json.loads(Emotion_string.content)['contents'][0]['reactions']
    Emotion_dict = dict()
    for item in Emotion_string:
        Emotion_dict[item['reactionType']] = item['count']
    return Emotion_dict

if __name__ == '__main__':
    aid_list = range(start_id_int, end_id_int+1)
    shuffle(aid_list)
    progress_tracker = 0
    errorcount = 0
    errorlist = []
    exceptioncount = 0
    exceptionlist = []
    df = pd.DataFrame(columns=['Source', 'Title', 'Date', 'Author', 'Contents', 'A_id', 'A_type', 'Emotion'])

    # WRITING PATHS
    middle = source_id + '_' + str(start_id_int) + '~' + str(end_id_int)
    json_path = 'data/Data_' + middle + '.json'
    error_path = 'logs/error_log_' + middle + '.csv'
    exception_path = 'logs/exception_log_' + middle + '.csv'

    # Save the shuffled article id list for debugging
    list_path = 'data/Data_list_' + middle + '.csv'
    with open(list_path, "wa") as text_file:
        writer = csv.writer(text_file)
        writer.writerow(aid_list)

    for i in aid_list:
        # information to retrieve
        title = ''
        Date = ''
        Author = ''
        Contents = ''
        A_type = ''
        Emotion = {}

        # Call article source
        article_id = a_id_prefix + str(i)
        link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=' + source_id + '&aid=' + article_id
        r = requests.get(link, headers=headers)

        # Check which charset
        decode_type = "utf-8"
        if r.content.lower().find('charset="utf-8"') == -1:
            decode_type = "cp949"

        # Removed Articles
        if r.content.find(error) != -1:
            errorcount+=1
            errorlist.append(i)
            # print '404 error ', progress_tracker, i
            continue
        # Articles with ENTERTAIN template
        elif r.content.find('data-sid="ENTERTAIN"') != -1:
            A_type = 'ENTERTAIN'
            article_soup = BeautifulSoup(r.content, 'html.parser')
            title = article_soup.select('.end_tit')[0].text.replace("\t", "").replace("\n",'')
            Date = article_soup.select('.article_info em')[0].text
            for i, char in enumerate(Date):
                if char.isdigit():
                    Date = Date[i:]
                    break;
            Date = Date.replace(".", "-")
            if Date.encode('utf-8').find('\xec\x98\xa4\xec\xa0\x84')!=-1:
                Date = Date.replace(u'\uc624\uc804 ','')
            elif Date.encode('utf-8').find('\xec\x98\xa4\xed\x9b\x84')!=-1:
                Date = Date.replace(u'\uc624\ud6c4 ', '') + ' PM'
                Date = pd.to_datetime(Date).strftime('%Y-%m-%d %H:%M:%S')
            [s.extract() for s in article_soup('a')]
            Contents = article_soup.select('#articeBody')[0].text.replace("\t", "").replace("\n",'')
            Author = Get_Author(Contents)
            Emotion = Get_Emotion(A_type, source_id, article_id)
        # Articles with SPORTS template
        elif r.content.find('data-sid="SPORTS"') != -1:
            A_type = 'SPORTS'
            article_soup = BeautifulSoup(r.content, 'html.parser')
            title = article_soup.select('title')[0].text.replace("\t", "").replace("\n",'')
            Date = article_soup.select('.info span')[0].text
            for i, char in enumerate(Date):
                if char.isdigit():
                    Date = Date[i:]
                    break;
            Date = Date.replace(".", "-")
            if Date.encode('utf-8').find('\xec\x98\xa4\xec\xa0\x84')!=-1:
                Date = Date.replace(u'\uc624\uc804 ','')
            elif Date.encode('utf-8').find('\xec\x98\xa4\xed\x9b\x84')!=-1:
                Date = Date.replace(u'\uc624\ud6c4 ', '') + ' PM'
                Date = pd.to_datetime(Date).strftime('%Y-%m-%d %H:%M:%S')
            [s.extract() for s in article_soup('a')]
            Contents = article_soup.select('#newsEndContents')[0].text.replace("\t", "").replace("\n",'')
            Emotion = Get_Emotion(A_type, source_id, article_id)
            Author = Get_Author(Contents)
        # Default Article template
        elif r.content.find('data-sid="NEWS"') != -1:
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
            Contents = article_soup.select('#articleBodyContents')[0].text.replace("\t", "").replace("\n",'')
            Emotion = Get_Emotion(A_type, source_id, article_id)
            Author = Get_Author(Contents)
        else:
            exceptioncount+=1
            exceptionlist.append(i)
            # print 'Exception error ', progress_tracker, i
            continue

        df.loc[df.shape[0]] = [source_name, title, Date, Author, Contents, article_id, A_type, Emotion]
        df
        progress_tracker+=1
        # print(progress_tracker)
        Delayer(Delay)
    df['Date'] = pd.to_datetime(df['Date'])


    # Write the collected data to json
    df.to_json(json_path)
    # Write 404 list to csv
    if len(errorlist) != 0:
        with open(error_path, "wa") as text_file:
            writer = csv.writer(text_file)
            writer.writerow(errorlist)

    # Write exceptions to csv
    if len(exceptionlist) != 0:
        with open(exception_path, "wa") as text_file:
            writer = csv.writer(text_file)
            writer.writerow(exceptionlist)
            article_id
    print('DONE')
