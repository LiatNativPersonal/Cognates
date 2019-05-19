# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:26:34 2019

@author: TAL-LAPTOP
"""
import os
import random

NON_NATIVE_USERS_FOCUS_SET_DB = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/NonNative/"
NATIVE_USERS_FOCUS_SET_DB = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/Native/"
NON_NATIVE_SAMPLED_FILES = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/NonNative/1000_Sentences/"
NATIVE_SAMPLED_FILES = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/Native/1000_Sentenc_es/"
NATIVE_VALID_USRES = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/native_users_mathced.csv"
NON_NATIVE_VALID_USRES = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/non_native_user_to_valid_cognate_count.csv"
SETNTECES_SAMPLE_SIZE = 1000

valid_users = []
with open(NON_NATIVE_VALID_USRES, "r", encoding="utf-8") as valid_users_file:
    for line in valid_users_file:
        [user, cognate] = line.split(",")
        valid_users.append(user+".txt")
print(len(valid_users))


for file in valid_users:
    sentences = []
    file_path = os.path.join(NON_NATIVE_USERS_FOCUS_SET_DB, file)
    if not os.path.isfile(file_path):
        continue
#    print(file_path)
    
    print("sampling file {} \n".format(file_path))
    with open(file_path, "r", encoding="utf-8") as user_file:
        for line in user_file:
            if "http" in line or len(line.split(" ")) < 15 :
                continue
            sentences.append(line)
        sentences = random.sample(sentences, SETNTECES_SAMPLE_SIZE)
        sampled_file =  os.path.join(NON_NATIVE_SAMPLED_FILES, "sampled_"+file)
        with open(sampled_file, "w+",encoding="utf-8") as sampled_user_file:
            for line in sentences:
                sampled_user_file.write(line)
    
    
        
        


