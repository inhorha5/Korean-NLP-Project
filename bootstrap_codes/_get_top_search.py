# This code is only for manual bootstraping use only.

#This file is meant to crawl through www.1min.kr for the daily top 20 trending search terms from naver.com

import pandas as pd
import requests
import csv
import datetime
from bs4 import BeautifulSoup

days_to_search_back = 365
start_date = '20170809'
# As of Aug 28, this was the most recent record from this site. It seems this site doesn't update anymore or it's on temporary hiatus.
# Later, write a program to scrape directly from the source: http://datalab.naver.com/keyword/realtimeList.naver

if __name__=="__main__":
    s = start_date
    top_search_list = []
    for i in range(days_to_search_back):
        link = 'http://www.1min.kr/main/daily.php?date=' + s
        r = requests.get(link)
        likesoup = BeautifulSoup(r.content, 'html.parser')
        search_terms = likesoup.select('#naver a.rtk_link')
        daily_list = [s]
        for item in search_terms[:20]:
        daily_list.append(item.text)
        top_search_list.append(daily_list)

        d = datetime.datetime.strptime(s, '%Y%m%d') + datetime.timedelta(days=-1)
        s = d.strftime('%Y%m%d')

    with open("../data/top_search_trend_record.csv", "w") as text_file:
        writer = csv.writer(text_file,  lineterminator='\n')
        writer.writerows(top_search_list)
