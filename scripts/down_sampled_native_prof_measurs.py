# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 14:35:32 2020

@author: liatn
"""
import csv
import os

# DOWN_SAMPLE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/scripts/natives_distances.csv"
DOWN_SAMPLE = "c:/Users/liatn/Downloads/natives.csv"
ALL = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Summer2020/native_users_synsets_germanic_ratio.csv"
OUTPUT = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/scripts/NativesProficiency_accurcy93.csv"
NATIVE_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/Final/"

files = os.listdir(NATIVE_DATASET)


users = {}
with open('native_txt_files.txt','w',encoding='utf-8') as listdir:
    with open(DOWN_SAMPLE, 'r', encoding='utf-8') as downsample:
        reader = csv.reader(downsample, delimiter=',')
        header = next(reader, None)
        for line in reader:
            print(line[0])
            user = line[0]
            users[line[0]] = line[1]
            for file in files:
                if file.startswith(user+"."):
                    listdir.write(file + "\n")
                    break
              
# with open(ALL, 'r', encoding='utf-8') as all:
#     reader = csv.reader(all, delimiter=',')
#     header = next(reader, None)
#     with open(OUTPUT,'w+',encoding='utf-8') as output:
#         output.write("user,TTR,AVG_WORD_RANK,AVG_AOA,AVG_NAMING_RT,Distance\n")
#         for line in reader:
#             if line[0] in users.keys():
#                 output.write("{},{},{},{},{},{}\n".format(line[0],line[480],line[481],line[482],line[483],users[line[0]]))
    
