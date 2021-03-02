# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 15:06:54 2020

@author: liatn
"""
import os, shutil
from random import sample
sample_size = 1500

REDDIT_GERMANIC_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/over500/"
GERMANIC_LESS_THAN_2000 = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/LessThan2000Tokens/"
REDDIT_ROMANCE_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/over500/"
ROMANCE_LESS_THAN_2000 = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/LessThan2000Tokens/"
REDDIT_NATIVE_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/over500/"
NATIVE_LESS_THAN_2000 = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/LessThan2000Tokens/"
#
# small=[]
# for f in os.listdir(REDDIT_GERMANIC_DATASET):
#     text_len = 0
#     with open(os.path.join(REDDIT_GERMANIC_DATASET,f),'r', encoding='utf-8') as text:
#         # print(f)
#         text_len = len(text.read().split(" "))
#     if  text_len < 2000:
#         small.append(f)
#         shutil.move(os.path.join(REDDIT_GERMANIC_DATASET,f),os.path.join(GERMANIC_LESS_THAN_2000,f))
#         # print(f)
#
# print(len(small))
# print(small)


toy =  "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/complete_users_toy/"
chunks = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/shuffeldChunksOver2000"

romance_users = sample([x.split(".")[0] for x in os.listdir(REDDIT_NATIVE_DATASET)], sample_size)
print(romance_users)

for user in romance_users:
    # print(user)
    for chunk in os.listdir(chunks):
        # print(chunk)
        if chunk.startswith(user):
            shutil.copy(os.path.join(chunks,chunk),os.path.join(toy,chunk))
# ft = sample(os.listdir(chunks),sample_size)
# for f in ft:
#     shutil.copy(os.path.join(chunks,f),os.path.join(toy,f))
# print(len(ft))