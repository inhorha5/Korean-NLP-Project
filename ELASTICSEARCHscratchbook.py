from elasticsearch import Elasticsearch
import json
import requests
import pandas as pd

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = requests.get('http://localhost:9200')
i = 1


df = pd.read_json('data/Sample.json')
df['A_id'] = df['A_id'].astype(str)
df.rename(columns={'A_id':'articleID', 'A_type':'Category', 'Source':'NewsOutlet', \
                    'Title':'articleTitle', 'Date':'articleDate', 'Contents':'articleContents', 'Author':'articleAuthor'}, inplace=True)
df.info()
df.to_json('test.json', orient='records', date_format="iso")



########################################################
df = pd.read_json('data/Data_1_month.json')
df.head(1)
with open('data/Data_1_month.json') as json_data:
    data = json.load(json_data)

with open('test.json') as json_data:
    data = json.load(json_data)
data
for i in range(len(data)):
    es.index(index='test2', doc_type='article', id=i, body=data[i])
    if i%2000 == 0:
        print(i)

from datetime import datetime


# es.get(index='test', doc_type='article', id=1)

result = es.search(index='test', body={'query':\
                            {'fuzzy': {'articleContents':\
                            {'value':'박근혜', 'max_expansions':5}}}})

es.search(index='test', body={'query':\
                            {'match': {'articleContents':\
                            {'query':'계란', "fuzziness":2, 'max_expansions':10}}}})


first = es.search(index='test2', body={'query':\
                                {'match': \
                                    {'articleContents':\
                                        {'query':'히말라', "fuzziness":0, 'max_expansions':30}}}})
first
third = es.search(index='test2', body={'query':\
                                {'prefix': \
                                    {'articleContents':\
                                        {'value':'어느'}}}})
third
second = es.search(index='test', body={'query': \
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
es.search(index='test', body={'query':})
first['hits']['hits']
second['hits']['hits']
es.delete(index='test', doc_type='article', id=1)
