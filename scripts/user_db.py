# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:29:49 2019

@author: liatn
"""
import numpy as np
import pandas as pd
import csv

NATIVE_USERS_ENG_PROF_INPUT_FILE =  "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/19.5.2019_960_natives_analyzed.csv"
NATIVE_USERS_NORMALIZED_COGNATE_COUNTS_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/20.5.219_native_2way_normalized_cognate_vectors.csv"
GERMANIC_NON_NATIVE_USERS_ENG_PROF_INPUT_FILE=  "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/19.5.2019_479_germanic_non_native_analyzed.csv"
ROMANCE_NON_NATIVE_USERS_ENG_PROF_INPUT_FILE=  "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/19.5.2019_478_romance_non_native_analyzed.csv"
NON_NATIVE_USERS_NORMALIZED_COGNATE_COUNTS_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/20.5.2019_non_native_2way_normalized_cognate_vectors.csv"

native_users = []
germanic_NN_users=[]
romance_NN_users = []

native_users_cog_db = {}
germanic_NN_users_cog_db = {}
romance_NN_users_cog_db = {}

native_users_eng_prof_db = {}
germanic_NN_users_eng_prof_db = {}
romance_NN_users_eng_prof_db = {}

 ######## NATIVE ##########
with open(NATIVE_USERS_ENG_PROF_INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as native_users_file:   
     reader = csv.reader(native_users_file, delimiter=',')
     header = next(reader, None)
     for line in reader:
         native_users.append(line[1] + "." + line[2])
#     print (native_users)


####### NON NATIVE ##########
## Germanic ##
with open(GERMANIC_NON_NATIVE_USERS_ENG_PROF_INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as germanic_non_native_users_file:   
     reader = csv.reader(germanic_non_native_users_file, delimiter=',')
     header = next(reader, None)
     for line in reader:
         germanic_NN_users.append(line[1] + "." + line[2])
## Romance ##
with open(ROMANCE_NON_NATIVE_USERS_ENG_PROF_INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as romance_non_native_users_file:   
     reader = csv.reader(romance_non_native_users_file, delimiter=',')
     header = next(reader, None)
     for line in reader:
         romance_NN_users.append(line[1] + "." + line[2])
         
         
 ######## NATIVE ##########         
with open(NATIVE_USERS_NORMALIZED_COGNATE_COUNTS_FILE, 'r', errors = 'ignore') as native_cognates_file:
     cog_reader = csv.reader(native_cognates_file, delimiter = ',')
     
     user_to_col_number = {}
     col_num = 0
     for username in next(cog_reader, None):            
         if len(username) > 2 and username in native_users:
             native_users_cog_db[username] = {}
             user_to_col_number[username] = [col_num, col_num+1]
#                 print(col_num)
         col_num += 1
#         print(len(native_users_db))
     for line in cog_reader:
         for user_name, user in native_users_cog_db.items():
             synset = line[0]
             user[synset] = []
#                 print(columns_to_collect)
             for col in user_to_col_number[user_name]:
                 user[synset].append(line[col])
                 
 ######## NON NATIVE ##########        
## Germanic ## 
with open(NON_NATIVE_USERS_NORMALIZED_COGNATE_COUNTS_FILE, 'r', errors = 'ignore') as non_native_cognates_file:
     cog_reader = csv.reader(non_native_cognates_file, delimiter = ',')
     
     user_to_col_number = {}
     col_num = 0
     for username in next(cog_reader, None):            
         if len(username) > 2 and username in germanic_NN_users:
             germanic_NN_users_cog_db[username] = {}
             user_to_col_number[username] = [col_num, col_num+1]
#                 print(col_num)
         col_num += 1
#         print(len(native_users_db))
     for line in cog_reader:
         for user_name, user in germanic_NN_users_cog_db.items():
             synset = line[0]
             user[synset] = []
#                 print(columns_to_collect)
             for col in user_to_col_number[user_name]:
                 user[synset].append(line[col])
## Romance ## 
with open(NON_NATIVE_USERS_NORMALIZED_COGNATE_COUNTS_FILE, 'r', errors = 'ignore') as non_native_cognates_file:
     cog_reader = csv.reader(non_native_cognates_file, delimiter = ',')
     
     user_to_col_number = {}
     col_num = 0
     for username in next(cog_reader, None):            
         if len(username) > 2 and username in romance_NN_users:
             romance_NN_users_cog_db[username] = {}
             user_to_col_number[username] = [col_num, col_num+1]
#                 print(col_num)
         col_num += 1
#         print(len(native_users_db))
     for line in cog_reader:
         for user_name, user in romance_NN_users_cog_db.items():
             synset = line[0]
             user[synset] = []
#                 print(columns_to_collect)
             for col in user_to_col_number[user_name]:
                 user[synset].append(line[col])
                 
#             break
 ######## NATIVE ##########   
with open(NATIVE_USERS_ENG_PROF_INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as native_users_file:       
     with open("native_users_db.csv", "w+", encoding='utf-8', errors='ignore') as native_users_info_output:
        reader = csv.reader(native_users_file, delimiter=',')
        header = next(reader, None)
        for col in header:
            native_users_info_output.write("{},".format(col))        
        for synset in native_users_cog_db["Independent.US"].keys():
            native_users_info_output.write("{},{},".format(synset + "_g", synset + "_r"))
        native_users_info_output.write("\n")
        for line in reader:
            username = line[1] + "." + line[2]
            for field in line:
                native_users_info_output.write("{},".format(field))
            for synset,values in native_users_cog_db[username].items():
                for count in values:
                    native_users_info_output.write("{},".format(count))
            native_users_info_output.write("\n")


 ######## NON NATIVE ##########   
## Germanic ##  
with open(GERMANIC_NON_NATIVE_USERS_ENG_PROF_INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as germanic_non_native_users_file:       
     with open("germanic_users_db.csv", "w+", encoding='utf-8', errors='ignore') as germanic_users_info_output:
        reader = csv.reader(germanic_non_native_users_file, delimiter=',')
        header = next(reader, None)
        for col in header:
            germanic_users_info_output.write("{},".format(col))        
        for synset in germanic_NN_users_cog_db["2baldguys.Sweden"].keys():
            germanic_users_info_output.write("{},{},".format(synset + "_g", synset + "_r"))
        germanic_users_info_output.write("\n")
        for line in reader:
            username = line[1] + "." + line[2]
            for field in line:
                germanic_users_info_output.write("{},".format(field))
            for synset,values in germanic_NN_users_cog_db[username].items():
                for count in values:
                    germanic_users_info_output.write("{},".format(count))
            germanic_users_info_output.write("\n")

## Romance ##  
with open(ROMANCE_NON_NATIVE_USERS_ENG_PROF_INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as romnace_non_native_users_file:       
     with open("romance_users_db.csv", "w+", encoding='utf-8', errors='ignore') as romance_users_info_output:
        reader = csv.reader(romnace_non_native_users_file, delimiter=',')
        header = next(reader, None)
        for col in header:
            romance_users_info_output.write("{},".format(col))        
        for synset in romance_NN_users_cog_db["AJaume_2.Spain"].keys():
            romance_users_info_output.write("{},{},".format(synset + "_g", synset + "_r"))
        romance_users_info_output.write("\n")
        for line in reader:
            username = line[1] + "." + line[2]
            for field in line:
                romance_users_info_output.write("{},".format(field))
            for synset,values in romance_NN_users_cog_db[username].items():
                for count in values:
                    romance_users_info_output.write("{},".format(count))
            romance_users_info_output.write("\n")