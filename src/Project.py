import scraper
import lemKR
import elastic
import pandas as pd
from elasticsearch import Elasticsearch, helpers

# WRITTEN IN PYTHON 3.6
# 2017.08.28 Edward Rha
# This code is written for personal educational use.

def Update_and_index_to_ES():
    """
    Gets new articles that haven't been previously scraped.
    Also indexes to ElasticSearch.
    """
    # Scrape Latest Articles
    scraper.Update_LatestArticle_ids()
    df = scraper.Update()
    df = lemKR.Create_Lem_Column(df)
    df.to_json('../data/Most_recent_scrape.json', orient='records', date_format="iso")

    # Input data to Elastic Search index
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    elastic.Feed_to_ES(df)

    # Update article ids
    scraper.Update_LastUpdatedArticle_ids(scraper.Get_LatestArticle_ids())

if __name__=="__main__":
    """
    NOTICE: If running this for the first time, you must manually set your starting articles at ../logs/last_update.csv
    August 28, 2017 starting locations:
    0001021525,0003090626,0002325585,0003204490,0003308799,0002749295,0002377613,0002814085,0002849023,0000230093
    """

    # df_temp = pd.read_json('data/Data_1_year_with_lem.json', orient='records', dtype={"articleID":'object'})
