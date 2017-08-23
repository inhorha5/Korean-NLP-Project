from bs4 import BeautifulSoup
import glob, os
import numpy as np
import pandas as pd
import requests
import time
import csv

# Test if blocked
import requests
link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=032&aid=0002811525'
r = requests.get(link)
with open("Output.txt", "wa") as text_file:
    text_file.write(r.content)
2804500-2812318
df_temp = pd.read_json('data/Data_032_2804500~2812318.json')
df_temp['Author'][98]
".*[가-힣]+.*" # for cleaning up data later through Pandas
"""
source_id:
'005, '020', '021', '022', '023', '025', '028', '032', '081', '469'
source_id_list = ['005, '020', '021', '022', '023', '025', '028', '032', '081', '469']
u'국민일보', u'동아일보', u'문화일보', u'세계일보', u'조선일보', u'중앙일보', u'한겨례', u'경향신문', u'서울신문', u'한국일보'
year_end_target = [999999, 3080999, 2321499, 3193999, 3299499, 2737999, 2373031, 2804499, 2839999, 219944]
year_start_target = [929000, 3000000, 2281500, 3090000, 3259000, 2639651, 2330000, 2714500, 2740000, 160000]
delay_target = []
np.sum(np.array(year_end_target) - np.array(year_start_target))/10
1/((np.array(year_end_target) - np.array(year_start_target)) / 60 / 60 / 27.4)
prefix = ["0000", "000", "000", "000", "000", "000", "000", "000", "000", "0000"]
Aug 21st 8AM (PST):
1 국민일보 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=005&aid=0001019559
~0001011000 1 month DONE 1
~0000929000 1 year #NUMBER OF DIGIT IS DIFFERENT
2 동아일보 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=020&aid=0003088691
~0003081000 1 month DONE RESCRAPING 3
~0003000000 1 year
3 문화일보 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=021&aid=0002324813
~0002321500 1 month DONE
~0002281500 1 year
4 세계일보 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=022&aid=0003202400
~0003194000 1 month DONE
~0003090000 1 year
5 조선일보 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=023&aid=0003306675
~0003299500 1 month DONE
~0003259000 6 month
6 중앙일보 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=025&aid=0002747105
~0002738000 1 month DONE
~0002639651 0.9 year
7 한겨례 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=028&aid=0002376732
~0002373032 1 month DONE
~0002330000 1 year
8 경향신문 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=032&aid=0002812318
~0002804500 1 month IP 1
~0002714500 1 year
9 서울신문 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=081&aid=0002847019
~0002840000 1 month DONE
~0002740000 1 year
10 한국일보 http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=469&aid=0000227943
~0000219945 1 month IP 1
~0000160000 1 year
#

News source | Title | Date | Author | Contents | Article_id | Article_type (normal, entertainment, sports) | Emotion (dict) | comment count

"""


# News source | Title | Date | Author | Contents | Article_id | Article_type | Emotion (list of dict)
# http://entertain.naver.com/read?oid=469&aid=0000227942 #TV 연예
# http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=469&aid=0000227942

# http://sports.news.naver.com/kbaseball/news/read.nhn?oid=032&aid=0002811525 #스포츠

# http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=032&aid=0002810780 #일반

# http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=023&aid=0003219500 404
#pd.to_numeric(df['A_id'])

link = 'http://news.like.naver.com/v1/search/contents?&q=SPORTS%5Bne_032_0002811525%5D'
r = requests.get(link)
likesoup = BeautifulSoup(r.content, 'html.parser')
print likesoup.text

articles = []
for i in range(10):
    article_id = int(227942)-i
    link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=469&aid=0000' + str(article_id)
    r = requests.get(link)
    article_soup = BeautifulSoup(r.content, 'html.parser')
    articles.append(article_soup.contents)

sys.getsizeof(r.content)
Abc = np.array(unicode(articles).encode('utf-8'))
with open("Output5.txt", "r") as text_file:
    reader = csv.reader(text_file)
    for row in reader:
        output = (row)
np.array(output).shape
print output[0]
for i in range(10):
    article_id = int(2811185)-i
    link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=032&aid=000' + str(article_id)
    link = 'http://sports.news.naver.com/kbaseball/news/read.nhn?oid=032&aid=0002811525'
    link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=023&aid=0003219500'
    link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=469&aid=0000227942'
    link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=032&aid=0002811525'
    link = 'http://news.naver.com/main/read.nhn?mode=LPOD&mid=sec&oid=005&aid=0001013326'
    r = requests.get(link)
    article_soup = BeautifulSoup(r.content, 'html.parser')
    [s.extract() for s in article_soup('a')]
    [s.extract() for s in article_soup('script')]
    [b.replace_with("%s " % b.text) for b in article_soup('br')]

    Contents = article_soup.select('#articleBodyContents')[0].text.replace("\t", "").replace("\n",'')
    Contents
    article_contents = article_soup.select('.end_tit')[0].text.replace("\t", "").replace("\n",'')
    print article_contents
    print article_contents
    with open("Output4.txt", "w") as text_file:
        text_file.write(unicode(article_soup).encode('utf-8'))
    article_contents2 = article_soup.select('#news_end')
    article_contents2
    # tag = 0
    # image_list2 = []
    # for item in article_contents:
    #     tag = item.find('img')
    #     image_list2.append(tag['src'])
    articles.append(article_contents[0])
for i in articles:
    print i


################################################################################
# Python 3.6
for i in range(df.shape[0]):
    Author = ""
    Contents = df.loc[i]['Contents']
    if len(Contents)>150:
        Contents = '.' + Contents[len(Contents)-150:]
    Temp_list = re.findall(r'.*\.+.*?\s?\w*?\s?([가-힣]+)\s*\w*기자',Contents)
    try:
        Author = Temp_list[-1]
    except IndexError:
        Author = ""
    if i%1000 == 0:
        print(i)
    df.set_value(i, 'Author2', Author)

Temp_list = re.findall(r'.*\.+.*?\s*?\w*?\s*?\w*?([가-힣]+)\s*\w*기자',Contents)
