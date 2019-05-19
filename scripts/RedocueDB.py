# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 15:11:50 2019

@author: TAL-LAPTOP
"""
import os
import shutil

VALID_USERS = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/non_native_user_to_valid_cognate_count.csv"
SOURCE_DIR = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/NonNative/4000_Sentences/"
DEST_DIR = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/NonNative/Chosen/"

#screend_users=[]
files = os.listdir(SOURCE_DIR)
with open(VALID_USERS, "r", encoding = "utf-8") as valid_users:
    for line in valid_users:
        [user, synsets] = line.split(",")
#        print(user)
        
        filename = "sampled_" + user + ".txt"
        
#        print(len(files))
#        print(files)
#        print(substr)
        if any(filename == file for file in files):
#            print(filename)
            filePath = os.path.join(SOURCE_DIR, filename)
#            print(filePath)
            shutil.copy(filePath, DEST_DIR)
        else:
            print(filename)
            print()
#
           
        