# This file isn't meant to be run again.
from elasticsearch import Elasticsearch, helpers
import json
import requests
import pandas as pd
import datetime
import gc


if __name__=="__main__":
    data_path = '../data/Data_1_year_with_lem_pt.5.json'
    df = pd.read_json(data_path, orient='records', dtype={"articleID":'object', "articleDate":"datetime64[ns]"})
    d = datetime.datetime.strptime('20170823', '%Y%m%d')
    df['Emotion_date'] = d.strftime('%Y-%m-%dT%H:%M:%S')
    df['Emotion_date'] = df['Emotion_date'].astype('datetime64[ns]')
    data = df.to_json(orient='records', date_format="iso")
    data = json.loads(data)
    del df
    data_feed = []
    data_feed = [{'_index':'ko_news_articles', '_type': 'news_article', '_source':data[j]} for j in range(len(data))]

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    r = requests.get('http://localhost:9200')
    # helpers.parallel_bulk(es, data_feed, thread_count=4)
    helpers.bulk(es, data_feed)
