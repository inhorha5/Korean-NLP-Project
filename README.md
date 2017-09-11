# Korean-NLP-Project

###### Last Edit: Sept 8, 2017

## Overview

<img align="right" src="/Ko_NLP.png" width="150">

A data science project about using NLP techniques on Korean news articles. Attempts to achieve a quick, unsupervised, automatic, and dynamic topic clustering on news articles retrieved from a keyword. The articles are retrieved from a local Elasticsearch database that is indexed with Korean news articles and can be updated in real-time.

Key technologies include: Elasticsearch, KoNLPy, Word2Vec, and HDBSCAN.

## Package requirements
 * **Python 3**
 * **Doc2Vec models:** [Download models.](https://drive.google.com/open?id=0BzwG1B4-gvAfbTh0ZTR4Nk9GcFU) Place the files inside `/models`
 * **Basic:** numpy, sklearn, pandas, beautifulsoup4, sklearn, matplotlib
 * **Elasticsearch:** `pip install elasticsearch`
 * **Gensim:** `conda install gensim`
 * **HDBSCAN:** `pip install hdbscan` _OR_ `conda install -c conda-forge hdbscan`
 * **KoNLPy:** [Instructions here](http://konlpy.org/en/v0.4.4/install/)
 * **with Mecab-ko:** [Mecab for Windows](https://groups.google.com/d/msg/eunjeon/Dzohqj4n3QI/WytnB4oZAgAJ) (requires some environment variable tweaking)
    * [Direct repo link just in case](https://github.com/Pusnow/mecab-ko-msvc)
    * [For Non-Window Python 3](https://bitbucket.org/eunjeon/mecab-ko-dic)
 * **Networkx:** `pip install networkx`
 * **PyTagCloud:** [Instructions](https://github.com/atizo/PyTagCloud)
    * Add Korean font to python3/site-packages/pytagcloud and edit .json file
 * **Googletrans:** [Instructions](https://pypi.python.org/pypi/googletrans) (optional)

## Basic process:
 1. Make sure Elasticsearch is running and the database is updated
 1. Input a keyword which will retrieve up to a 1000 relevant articles (accounts for time relevancy)
 1. A pre-trained Doc2Vec model is loaded and is used to infer the vectors of the 1000 articles.
 1. The vectors are labeled into clusters using HDBSCAN (density based clustering)
 1. Optional visualization of the clusters

## Model Flowchart
![Model diagram](/Diagram.png)

## Data source
 * The news articles are from the Naver's news hub: http://news.naver.com/main/officeList.nhn
 * The selected news outlets for this project are as follows:
    * Outlet Name: Source ID
    * 국민일보: 005
    * 동아일보: 020
    * 문화일보: 021
    * 세계일보: 022
    * 조선일보: 023
    * 중앙일보: 025
    * 한겨례: 028
    * 경향신문: 032
    * 서울신문: 081
    * 한국일보: 469
 * For the initial bootstraping for my database and model training, I scraped about a year worth of articles from these sources (from Aug 2016 to Aug 2017) except for 조선일보 (023) Where I only scraped 6 month worth of data.

## Future Works
 * Allow Elasticsearch address parameters to be inputted (Currently only localhost:9200)
 * Improve search algorithm
 * Untapped sentiment data for analysis
 * Add automatic and continuous Doc2Vec training
 * Implement the Phraser model (model exists but isn't implemented due to uncertainty of its performance)
 * Improve text processing
    * Improve author name extraction algorithm
    * Improve noise and template filtering algorithm (ex. delete all '동아일보', '포토' articles)

## Contact
If you have any questions regarding this project, feel free to email me.

Email: inhorha5+github@gmail.com
