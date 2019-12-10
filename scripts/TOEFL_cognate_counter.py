# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 13:58:00 2019

@author: liatn
"""

GERMANIC_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/GER/essays/"
GERMANIC_TRANSCRIPT_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/GER/speech_transcriptions/"
SPANISH_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/SPA/essays/"
SPANISH_TRANSCRIPT_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/SPA/speech_transcriptions/"
#ALT_COG_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Extended Alternative synset list.txt"
ALT_COG_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/synset_list"
GERMANIC_COUNT_FILE =  "Speech_Extended_ALT_TOEFL_Germanic_cognate_count.csv"
ROMANCE_COUNT_FILE =  "Speech_Extended_ALT_TOEFL_ROMANCE_cognate_count.csv"

import os
from RedditUser import RedditUser
from RedditCognatesCounter import RedditCognatesCounter


cognate_counter = RedditCognatesCounter(ALT_COG_LIST)
#i = 0
#with open('debug.txt','w') as debug:
for user_file in os.listdir(GERMANIC_TRANSCRIPT_LIB):
#    i += 1
#    print('processing ' + user_file  )
    user = RedditUser(user_file, 'Spain')
    user.text_file = os.path.join(GERMANIC_TRANSCRIPT_LIB, user_file)
    cognate_counter.count_cognates_for_user(user)
        
#        debug.write(str(i) +" " + user.user_name + ": " + str(user.totalCognateCount) + "\n")
#    print(user.totalCognateCount)
    
cognate_counter.write_cognates_vector_to_file(GERMANIC_COUNT_FILE,0,0)
    

