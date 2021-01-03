# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:50:51 2020

@author: liatn
"""
import os
from random import sample

ORIGINAL_DATA_SET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/Final/"
BALANCED_DATA_SET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/Balanced/"

min = 480
# for file in os.listdir(ORIGINAL_DATA_SET):
#     size = 0
#     with open(ORIGINAL_DATA_SET + file, 'r',encoding='utf-8') as f:
#           for line in f:
#               size += 1
#         # size=len([0 for _ in f])
        
#     if size<min:
#             min=size
# print(min)

for file in os.listdir(ORIGINAL_DATA_SET):
    with open(ORIGINAL_DATA_SET + file, 'r',encoding='utf-8') as f:
        all_content = []
        all_content.clear()
        for line in f:
            all_content.append(line)
        # print(len(all_content))
        sampaled_content = sample(all_content,min)
        nf = open(BALANCED_DATA_SET+file,'w',encoding='utf-8')
        for line in sampaled_content:
            nf.write(line)
    




