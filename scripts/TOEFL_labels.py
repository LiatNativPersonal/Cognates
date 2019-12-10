# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:43:15 2019

@author: liatn
"""
LABEL_FILE = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/labels.csv"
ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL2017/nli-shared-task-2017/data/speech_transcriptions/train/tokenized/"
GERMANIC_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/GER/speech_transcriptions/"
SPANISH_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/SPA/speech_transcriptions/"
import pandas as pd
import os
import shutil 

labels = pd.read_csv(LABEL_FILE)

##print(labels)
#esseys = {}
#for file in os.listdir(ESSEY_LIB):
#    esseys[int(file.split(".txt")[0])] = file
#    
#for index,row in labels.iterrows():
#    if(row['L1'] == 'GER'):
#        file = esseys[int(row['test_taker_id'])]
#        with open(ESSEY_LIB+file, 'r') as ff:
#            print("xxx")
#        shutil.copy(ESSEY_LIB+file,GERMANIC_ESSEY_LIB)

with open("c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Extended Alternative synset list.txt", 'r') as synset_list:
    with open("c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/revised_list.dat", 'w+', encoding='utf-8') as revised_list:
        for line in synset_list:
            for word in line.split():
                revised_list.write(word.strip() + " ")
            revised_list.write("\n")