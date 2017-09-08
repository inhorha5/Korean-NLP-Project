# This code is only for manual bootstraping use only.

# This file is meant to create an gensim phrases and Phraser (term detector ex: new york -> new_york) and then save the model.
# This model will be extremely conservative about phrase detection to reduce false positives as much as possible.
# phrases model can be loaded and then updated with newly scrapped data.
# Phraser model needs to be re-created from the new phrases model if you want to update the model.

from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from konlpy.tag import Mecab
import gensim


file1 = '../data/Data_1_year_with_lem_pt.1.json'
file2 = '../data/Data_1_year_with_lem_pt.2.json'
file3 = '../data/Data_1_year_with_lem_pt.3.json'
file4 = '../data/Data_1_year_with_lem_pt.4.json'
file5 = '../data/Data_1_year_with_lem_pt.5.json'
file6 = '../data/Update_pack.json'
file_path_list = [file1,file2,file3,file4,file5,file6]

mecab = Mecab()
total_list = []
for path in file_path_list:
    df = pd.read_json(path)
    list_articleContents = df['articleContents'].str.replace('["#%\'()*+,/:;<=>@\[\]^_`{|}~’”“′‘\\\]', ' ').str.split(pat='[.!?『』]')
    flat_list = [item for sublist in list_articleContents for item in sublist]
    for i in range(len(flat_list)):
        lem = mecab.pos(flat_list[i])
        last_word_tag = ''
        for pair in lem:
            if pair[1] == "NNP":
                if last_word_tag == 'NNP':
                    total_list.append(last_word+'_'+pair[0])
                    total_list.append(pair[0])
                else:
                    total_list.append(pair[0])
                last_word_tag = 'NNP'
                last_word = pair[0]
            else:
                last_word_tag = ''
            last_word = pair[0]
    print("One Done")
temp = np.array([total_list])
phrases = gensim.models.phrases.Phrases(temp.T)
phrases.save('../models/phrases')
bigram = gensim.models.phrases.Phraser(phrases)
bigram.save('../models/phraser')
