# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:43:15 2019

@author: liatn
"""
LABEL_FILE = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/labels.csv"
ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL2017/nli-shared-task-2017/data/speech_transcriptions/train/tokenized/"
GERMANIC_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/GER/speech_transcriptions/"
SPANISH_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/SPA/speech_transcriptions/"
CONTROL_ESSEY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/CTRL/essays/"
CONTROL_SPEECH_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/CTRL/speech_transcriptions/"
CTRL_LABELS = ['CHI','JPN','HIN','KOR','TEL','TUR','ARA']
import pandas as pd
import os
import shutil 
from random import sample

labels = pd.read_csv(LABEL_FILE)

##print(labels)
#esseys = {}
#for file in os.listdir(ESSEY_LIB):
#    esseys[int(file.split(".txt")[0])] = file
#
#for label in CTRL_LABELS:   
#    file_list = []
#    print('processing {}:\n'.format(label))
#    for index,row in labels.iterrows():
#        if(row['L1'] == label):
#            file = esseys[int(row['test_taker_id'])]
#            file_list.append(ESSEY_LIB+file)
#    samlpe_file_list = sample(file_list,143)  
#    for file in samlpe_file_list:     
#    #        with open(ESSEY_LIB+file, 'r') as ff:
#    #            print("xxx")
#        try:
#            shutil.copy(file,CONTROL_ESSEY_LIB)
#        except:
#            continue

#with open("c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Extended Alternative synset list.txt", 'r') as synset_list:
#    with open("c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/revised_list.dat", 'w+', encoding='utf-8') as revised_list:
#        for line in synset_list:
#            for word in line.split():
#                revised_list.write(word.strip() + " ")
#            revised_list.write("\n")

for file in os.listdir(CONTROL_ESSEY_LIB):
    print(file)
    try:
        shutil.copy(CONTROL_ESSEY_LIB+file,CONTROL_SPEECH_LIB)
    except:
        continue