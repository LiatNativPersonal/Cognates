# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 15:06:54 2020

@author: liatn
"""
import os, shutil
import sys
from random import shuffle
import csv
import pandas as pd
import re
import numpy as np
from  statistics import stdev, variance 
CHUNK_SIZE = 2000
from lexicalrichness import LexicalRichness


REDDIT_GERMANIC_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/over500/"
GERMANIC_2000_chunks = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/shuffeldChunksOver2000/"
REDDIT_ROMANCE_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/over500/"
ROMANCE_2000_chunks = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/shuffeldChunksOver2000/"
REDDIT_NATIVE_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/over500/"
NATIV_2000_chunks = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/shuffeldChunksOver2000/"

 

# from cleantext import clean
# for file in os.listdir(REDDIT_ROMANCE_DATASET):
#     text = []
#     with open(os.path.join(REDDIT_ROMANCE_DATASET, file),'r',encoding='utf-8') as f:
#         text = f.read()
#         print(file)
#         text = clean(text,    
#                      fix_unicode=True,               # fix various unicode errors
#                      to_ascii=True,                  # transliterate to closest ASCII representation
#                      lower=True,                     # lowercase text
#                      no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
#                      no_urls=True,                  # replace all URLs with a special token
#                      no_emails=True,                # replace all email addresses with a special token
#                      no_phone_numbers=True,         # replace all phone numbers with a special token
#                      no_numbers=True,               # replace all numbers with a special token
#                      no_digits=True,                # replace all digits with a special token
#                      no_currency_symbols=True,      # replace all currency symbols with a special token
#                      no_punct=True ,                 # remove punctuations
#                      replace_with_punct="",          # instead of removing punctuations you may replace them
#                      replace_with_url="",
#                      replace_with_email="",
#                      replace_with_phone_number="",
#                      replace_with_number="",
#                      replace_with_digit="",
#                      replace_with_currency_symbol="",
#                      lang="en" )                      # set to 'de' for German special handling
#     with open(os.path.join(REDDIT_ROMANCE_DATASET, file),'w',encoding='utf-8') as f:             
#         f.write(text)
    # break        



# user_to_chunks = {}
# chunk_num = 0
# for f in os.listdir(REDDIT_NATIVE_DATASET):
#     user_chunk_num = 0
#     user_name = f.split(".")[0]
#     user_to_chunks[user_name] = {}
#     with open(os.path.join(REDDIT_NATIVE_DATASET,f), 'r', encoding = 'utf-8') as uf:
#         sentences = uf.read().split("\n")
#         shuffle(sentences)
#     chunk = []
#     i = 0        
#     for line in sentences:
#         line = line.strip()
#         if len(line) == 0: continue
#         chunk.append(line)
#         i += len(line.split(" "))
#         if i >= CHUNK_SIZE:
#             user_to_chunks[user_name][chunk_num] = i
#             with open(NATIV_2000_chunks + user_name + "_" + str(user_chunk_num)+ "_" + str(chunk_num) + ".txt", 'w', encoding='utf-8') as cf:
#                   cf.write('\n'.join(chunk))
#             i = 0
#             chunk_num += 1
#             user_chunk_num += 1
#             chunk.clear()
    # break
    # if i > 0:
    #     user_to_chunks[user_name][chunk_num] = i
    #     with open(NATIV_500_chunks + user_name + "_" + str(chunk_num) + ".txt", 'w', encoding='utf-8') as cf:
    #         for line in chunk:
    #             cf.write(line + "\n")
    #     i = 0
        # chunk_num += 1
        # chunk.clear()
        
   
# with open('romance_chunks.csv', 'w', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
#     f.write("user_name, user_chunk, chunk, size(tokens)\n")
#     for user in user_to_chunks.keys():
#         i = 0
#         for chunk,size in user_to_chunks[user].items():
#             f.write("{},{},{},{}\n".format(user,i,chunk,size))
#             i+=1
           
# native_df = pd.read_csv("romance _chunks.csv")
# print(len(native_df))
# # print(native_df.head())
# short = native_df[native_df[' size(tokens)']<500]
# print(len(short))

######## chunk grades stat #############

romance_chunks_df = pd.read_csv('complete_users_6_bins_log_reg_toy.csv')


###calculating chunk ttr
# files = list(romance_chunks_df['User'])

# print(len(files))
# ttrs = {}
# for file in files:
#     ttrs[file] = 0.0
#     with open(os.path.join(ROMANCE_2000_chunks,file),'r',encoding='utf-8') as chunk:
#         text = chunk.read()
#         lex = LexicalRichness(text)
#         ttrs[file] = lex.ttr
# for user,ttr in ttrs.items():
#     # p int(ttr)
#     romance_chunks_df.loc[romance_chunks_df['User'] == user, 'ttr'] = ttr

# romance_chunks_df.to_csv('10bins_over_2000_with_ttr.csv')
# sys.exit(0)


# print(romance_chunks_df.head())
# a = list(romance_chunks_df['User'])
user_names = [re.split('_[0-9]+_[0-9]+.txt', s)[0] for s in romance_chunks_df['User']]
# print(user_names[1:5])        
romance_chunks_df['user_name'] = user_names
# print(romance_chunks_df.head())
with open('complete_users_6_bins_log_reg_toy_stat.csv', 'w', encoding='utf-8', newline='') as stat:
    # fieldnames = ['username', 'chunks_num', 'avg_grade','stdev_grades','var_grades','avg_ttr','stdev_ttrs','var_ttrs']
    fieldnames = ['username', 'chunks_num', 'avg_grade', 'stdev_grades', 'var_grades']
    writer = csv.DictWriter(stat, fieldnames=fieldnames)
    writer.writeheader()
    # user_to_stat = {}
    i = 1
    for user_name in set(user_names):
        # user_to_stat[user_name] = []
       
        grades = list((romance_chunks_df[romance_chunks_df['user_name'] == user_name])['grade'])
        # ttrs = list((romance_chunks_df[romance_chunks_df['user_name'] == user_name])['ttr'])
        chunks_num = len(grades)
        var_grades = 0.0
        std_dev_grades = 0.0
        # var_ttrs = 0.0
        # std_dev_ttrs = 0.0
        if chunks_num >= 2 :           
            var_grades = variance(grades)
            std_dev_grades = stdev(grades)
            # var_ttrs = variance(ttrs)
            # std_dev_ttrs = stdev(ttrs)
            
           
        # writer.writerow({'username':"'" + user_name+"'",'chunks_num':chunks_num, 'avg_grade':np.mean(grades), 'stdev_grades': std_dev_grades, 'var_grades':var_grades, 'avg_ttr':np.mean(ttrs),'stdev_ttrs': std_dev_ttrs, 'var_ttrs':var_ttrs})
        writer.writerow({'username': "'" + user_name + "'", 'chunks_num': chunks_num, 'avg_grade': np.mean(grades),
                         'stdev_grades': std_dev_grades, 'var_grades': var_grades})
        # i += 1
        # if i > 100:
        #     break
        # user_to_stat[user_name] = [len(grades), np.mean(grades), stdev(grades), variance(grades)]
        # print(user_to_stat[user_name])
        # break
