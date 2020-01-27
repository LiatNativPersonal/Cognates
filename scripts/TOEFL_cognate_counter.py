# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 13:58:00 2019

@author: liatn
"""

GERMANIC_ESSAY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/GER/essays/"
GERMANIC_TRANSCRIPT_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/GER/speech_transcriptions/"
SPANISH_ESSAY_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/SPA/essays/"
SPANISH_TRANSCRIPT_LIB = "C:/Users/liatn/Documents/Liat/Research/TOEFL_MINI/SPA/speech_transcriptions/"
ROMANCE_LIB = ['c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/']
GERMANIC_LIB = ["C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/500to1000/Germanic/"]
CTRL_LIB=['C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/']
#ALT_COG_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Extended Alternative synset list.txt"
ALT_COG_LIST = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/valid_synsets_detailed.csv"
#SYNSET_ORIGIN = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/synset_list_with_origin"
SYNSET_ORIGIN = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/valid_cognates_origin "
ROMANCE_GERMANIC_VS_ROMANCE_COUNT_FILE = "over_1000_Romance_Users_Romance_Vs_Germanic.csv"
GERMANIC_GERMANIC_VS_ROMANCE_COUNT_FILE = "500-1000_ Germanic_Users_Romance_Vs_Germanic.csv"
NATIVE_GERMANIC_VS_ROMANCE_COUNT_FILE = "Control_Speakers_Romance_Vs_Germanic.csv"
REDDIT_GERMANIC_COUNTS_FILE = "500-1000_Germanic_Reddit_count.csv"
REDDIT_ROMANCE_COUNTS_FILE = "over_1000_Romance_Reddit_count.csv"
REDDIT_NATIVE_COUNTS_FILE = "Native_Reddit_count.csv"




import os
import csv
from RedditUser import RedditUser
from RedditCognatesCounter import RedditCognatesCounter


cognate_counter = RedditCognatesCounter(ALT_COG_LIST)
#i = 0
synset_origin_dict={}
with open(SYNSET_ORIGIN,'r') as origin_file:
    reader = csv.reader(origin_file, delimiter=',')            
    next(reader) #skipping header    
    for line in reader:       
       synset_origin_dict[line[1]] = line[2]


#print(synset_origin_dict)

user_to_ger_count = {}  
user_to_rom_count = {}    
users={}  
for lib in ROMANCE_LIB:

    for user_file in os.listdir(lib):
    #    i += 1
#        print('processing ' + lib + user_file  )
#        user = RedditUser(user_file, 'Spain')
        if user_file not in users.keys():
            users[user_file] = RedditUser(user_file, (user_file.split(".",1)[1]).split(".")[0])
        user = users[user_file]
            
        if user not in user_to_ger_count.keys():
            user_to_ger_count[user] = 0
        if user not in user_to_rom_count.keys():
            user_to_rom_count[user] = 0
        
        user.text_file = os.path.join(lib, user_file)
        cognate_counter.count_cognates_for_user(user)
        if user not in cognate_counter.users_cognate_counts_dict.keys():
            continue
        
    cognate_counter.write_cognates_vector_to_file(REDDIT_ROMANCE_COUNTS_FILE,0,0)

for user in users.values():    
    if user not in cognate_counter.users_cognate_counts_dict.keys():
        print(user.user_name)
    for synset,tokens in cognate_counter.users_cognate_counts_dict[user].items():
        for word,count in tokens.items():
           
            if count > 0:
                if word in synset_origin_dict.keys():
                    if synset_origin_dict[word] == 'G':
                        user_to_ger_count[user] += count
                    elif synset_origin_dict[word] == 'R':
                        user_to_rom_count[user] += count
                    else:
                        print(word)

#for user,count in user_to_ger_count.items():
#    print("Germanic count: {}:{}".format(user.user_name,count))
#
#for user,count in user_to_rom_count.items():
#    print("Romance count: {}:{}".format(user.user_name,count))
                            
#for user in users.values():
#    print("Germanic count: {}:{}".format(user.user_name,user_to_ger_count[user]))            
#    print("Romance count: {}:{}".format(user.user_name,user_to_rom_count[user]))
        
with open(ROMANCE_GERMANIC_VS_ROMANCE_COUNT_FILE,"w+",encoding='utf-8') as GerVsRomOut:
    GerVsRomOut.write("user,GermanicCount,RomanceCount\n")
    for user in users.values():
        
        GerVsRomOut.write("{},{},{}\n".format(user.user_name,user_to_ger_count[user],user_to_rom_count[user]))        
       
#        try:
#            user.sample_size = 10000
#            user.set_user_text_sample()                
#            user.calculate_word_rank_measure()
#            user.calculate_naming_RT_measure()
#            user.calculate_AOA_measure()                
#            user.set_user_text_sample
#            user.calculate_type_token_ratio()
#        except:
#            print("skipping {} from {} \n".format(user.user_name, user.l1))
##                cognate_counter.count_cognates_for_user(user)
#        GerVsRomOut.write(",{},{},{},{}\n".format( user.type_token_ratio, user.avg_word_rank, user.avg_naming_RT, user.avg_age_of_aquisition))            
        
#        debug.write(str(i) +" " + user.user_name + ": " + str(user.totalCognateCount) + "\n")
#    print(user.totalCognateCount)
    
#cognate_counter.write_cognates_vector_to_file(ROMANCE_COUNT_FILE,0,0)
    

