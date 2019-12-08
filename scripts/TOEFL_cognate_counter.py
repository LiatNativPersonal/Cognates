# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 13:58:00 2019

@author: liatn
"""

GERMANIC_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/GER/"
SPANISH_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/SPA/"
VALID_COGNATES = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/valid_synsets_detailed.csv"
ALT_COG_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Alternative synset list.txt"
GERMANIC_COUNT_FILE =  "ALT_TOEFL_Germanic_cognate_count.csv"
ROMANCE_COUNT_FILE =  "ALT_TOEFL_ROMANCE_cognate_count.csv"

import os
from RedditUser import RedditUser
from RedditCognatesCounter import RedditCognatesCounter


cognate_counter = RedditCognatesCounter(ALT_COG_LIST)
for user_file in os.listdir(GERMANIC_ESSEY_LIB):
    print('processing ' + user_file  )
    user = RedditUser(user_file, 'Germany')
    user.text_file = os.path.join(GERMANIC_ESSEY_LIB, user_file)
    cognate_counter.count_cognates_for_user(user)
    print(user.totalCognateCount)
    
cognate_counter.write_cognates_vector_to_file(GERMANIC_COUNT_FILE,0,0)
    

