# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 10:41:27 2019

@author: liatn
"""

NON_NATIVE_ORIGIN = 'c:/Users/liatn/Documents/Liat/Research/Cognates/MassiveUsersDB/NonNative/'
NATIVE_ORIGIN = 'c:/Users/liatn/Documents/Liat/Research/Cognates/MassiveUsersDB/Native/'
GERMANIC_USERS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Summer2020/down_sampled_germanic_extended_list_over_500_cog_200_synsets.csv"
ROMANCE_USERS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Summer2020/romance_extended_list_over_500_cog_200_synsets.csv"
NATIVE_USERS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Summer2020/down_sampled_native_extended_list_over_500_cog_200_synsets.csv"
GERMANIC_SOURCE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData//Germanic/ExtendedSynsetList/"
ROMANCE_SOURCE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData//Romance/ExtendedSynsetList/"
NATIVE_SOURCE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData//Native/ExtendedSynsetList/"
NATIVE_TARGET =  'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/Final'
GERMANIC_TARGET =  'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/Final/'
ROMANCE_TARGET =  'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/Final'
debug = "debug.csv"
SOURCE_FILES = 'c:/Users/liatn/Documents/Liat/Research/Reddit/'
ORIGINAL_GERMANIC_ROMANCE_ONLY_COG_LIST = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/valid_synsets_detailed.csv'
NEW_COG_LIST = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/synset_list'
COMBINED_SYNSET_LIST = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list'



import os
import shutil 
import csv
i = 0
with open(NATIVE_USERS) as users_file:
    reader = csv.reader(users_file, delimiter=',')
    header = next(reader, None)
    for line in reader:
        i+= 1
        username = line[1]
       
        country = line[0]
        file =  username + "." + country+".txt"
        if file not in os.listdir(NATIVE_TARGET):
            print(i)
            print(file)
            continue
        # shutil.copy(NATIVE_SOURCE+file,NATIVE_TARGET)
    print(i)

##########combining synsets lists################
# orig_synset_to_words = {}
# word_to_synsets = {}
# with open(NEW_COG_LIST, 'r') as new_list:
#     with open(ORIGINAL_GERMANIC_ROMANCE_ONLY_COG_LIST, 'r') as original_list:
        
#         i=1
#         for line in original_list:
           
#             orig_synset_to_words[i] = []
#             for word in line.split():
#                 if word not in word_to_synsets.keys():
#                     word_to_synsets[word] = []
#                 orig_synset_to_words[i].append(word)
#                 word_to_synsets[word].append(i)
#             i+= 1

# with open("log.txt",'w+') as log:
#         for word in word_to_synsets.keys():
#             if len(word_to_synsets[word]) > 1:
#                 log.write("{} appear in {} synsets:\n".format(word,len(word_to_synsets[word])))
#                 for synset in word_to_synsets[word]:
#                     log.write("{}: {}\n".format(synset,orig_synset_to_words[synset]))
        
       
     

 
#with open(debug, 'w+') as debug:
#    rejects = {}
#    with open(ROMANCE_USERS, 'r') as usersFile:
#        for user in usersFile:
#            user = user.strip()
#            try:
#                shutil.copy(ROMANCE_ORIGIN+user,ROMANCE_TARGET)
#            except:
#                country = (user.split(".",1)[1]).split(".")[0]
#                if country not in rejects.keys():
#                    rejects[country] = []
#                rejects[country].append(user.split(".")[0])
#                continue
#    for country, users in rejects.items():
#        print(country)
      
#        print (country)
#user_to_text_file = {}
#user_to_text = {}
#for source in os.listdir(SOURCE_FILES):
#    print(source)
#    
#    for country in rejects.keys(): 
##        if country != 'Brazil':
##            continue            
#        if country in source:
#            print(country)   
#            for user in rejects[country]:
#                print(user)
#                user_to_text_file[user] = NATIVE_TARGET+user+""+country+".txt"
#            with open(SOURCE_FILES+source, 'r', encoding='utf-8', errors='ignore') as country_file:                
#                csvreader = csv.reader(country_file, delimiter=',')                
#                for line in csvreader:                                         
##                # user_name apears in the begining of every row inside []
#                    if len(line) != 4:                        
#                        continue
#                    user_name = line[0] 
#                    if user_name not in rejects[country]:
#                        continue                    
#                    if user_name not in user_to_text.keys():
#                        user_to_text[user_name] = []                  
#                    user_to_text[user_name].append(str(line[3])+"\n")
#for user,file in user_to_text_file.items():
#    print("writing file {}".format(file))
#    with open(file,'w+',encoding='utf-8') as user_file:
#        print('writing {} lines'.format(len(user_to_text[user])))
#        for line in user_to_text[user]:
#            user_file.write(str(line))
#  
#romance_users={}                 
#with open('romance_users_over_500.csv','r') as romance_file:
#    csvreader = csv.reader(romance_file, delimiter=',') 
#    next(csvreader, None)
#    for line in csvreader:
#        romance_users[line[1]] = line[2]


    
     
            

#            
