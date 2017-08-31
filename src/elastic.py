from elasticsearch import Elasticsearch, helpers
import json
import pandas as pd
import time
from konlpy.tag import Mecab

def Feed_to_ES(df, host='localhost', port=9200, index='ko_news_articles', input_type='news_article'):
    '''
    Input:  Pandas DataFrame
            ES host address
            ES port number
            index name
            input_type name
    Output: None

    Takes in the scraped data from DataFrame and indexes it to ElasticSearch
    '''

    es = Elasticsearch([{'host': host, 'port': port}])
    data = df.to_json(orient='records', date_format="iso")
    data = json.loads(data)
    data_feed = [{'_index':index, '_type': input_type, '_source':data[j]} for j in range(len(data))]

    helpers.bulk(es, data_feed)


def Get_relevant_articles(search_string, num_of_articles=100, date=time.strftime("%Y-%m-%d"), host='localhost', port=9200, index='ko_news_articles', index='ko_news_articles', input_type='news_article'):
    '''
        Input: Pandas   String,
                        max number of related articles to return,
                        max date parameter (default=now),
                        ES host address
                        ES port number
                        index name,
                        input_type name
        Output: list of dictionaries containing the article infos
    '''
    mecab = Mecab()
    search_string_lem = mecab.nouns(search_string)
    es= Elasticsearch([{'host': 'localhost', 'port': 9200}])


    es.search(index=index, )
    result = es.search(index='test', body={'query':\
                                {'fuzzy': {'articleContents':\
                                {'value':'박근혜', 'max_expansions':5}}}})

    es.search(index='test', body={'query':\
                                {'match': {'articleContents':\
                                {'query':'계란', "fuzziness":2, 'max_expansions':10}}}})


    first = es.search(index='ko_news_articles', body={'query':\
                                    {'match': \
                                        {'articleID':\
                                            {'query':'005_0001020056', "fuzziness":0, 'max_expansions':30}}}})
    first
    third = es.search(index='ko_news_articles', body={'query':\
                                    {'prefix': \
                                        {'articleContents':\
                                            {'value':'어느'}}}})
    third
    second = es.search(index='ko_news_articles', body={'query': \
                                    {'function_score': \
                                        {"functions":
                                            [{"gauss":\
                                                {"articleDate":\
                                                    {"origin":"2017-08-22",\
                                                    "scale":"10d",\
                                                    "offset":"5d",\
                                                    "decay": .5 }\
                                                }}],\
                                            'query':\
                                                {'match':\
                                                    {'articleContents':\
                                                        {'query':'트럼프 대통령', \
                                                        "fuzziness":1,\
                                                        'max_expansions':10\
                                                        }\
                                                    }\
                                                },\
                                            "score_mode":"multiply"\
                                        }\
                                    }\
                                })
    second
