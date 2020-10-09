# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 13:58:00 2019

@author: liatn
"""
from statistics import mean

ROMANCE_LIB = ['c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/']
GERMANIC_LIB = ["C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/"]
NATIVE_LIB=['C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/']
#ALT_COG_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Extended Alternative synset list.txt"
ALT_COG_LIST = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list.csv'
#SYNSET_ORIGIN = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/synset_list_with_origin"
SYNSET_ORIGIN = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list_with_origin.csv'
ROMANCE_GERMANIC_VS_ROMANCE_COUNT_FILE = "over_1000_Romance_Users_Romance_Vs_Germanic.csv"
NATIVE_GERMANIC_VS_ROMANCE_COUNT_FILE = "over_1000_Native_Users_Romance_Vs_Germanic.csv"
GERMANIC_GERMANIC_VS_ROMANCE_COUNT_FILE = "500-1000_ Germanic_Users_Romance_Vs_Germanic.csv"
NATIVE_GERMANIC_VS_ROMANCE_COUNT_FILE = "Control_Speakers_Romance_Vs_Germanic.csv"
REDDIT_GERMANIC_COUNTS_FILE = "germanic_users_synsets_germanic_count.csv"
REDDIT_ROMANCE_COUNTS_FILE = "romance_users_synsets_germanic_count.csv"
REDDIT_NATIVE_COUNTS_FILE = "native_users_synsets_germanic_count.csv"
GERMANIC_GERMANIC_RATIO_FILE = "germanic_users_synsets_germanic_ratio.csv"
ROMANCE_GERMANIC_RATIO_FILE = "romance_users_synsets_germanic_ratio.csv"
NATIVE_GERMANIC_RATIO_FILE = "native_users_synsets_germanic_ratio.csv"
GERMANIC_LEX_PROF_MEASURE = "germanic_users_lex_prof_measurs.csv"
ROMANCE_LEX_PROF_MEASURE = "romance_users_lex_prof_measurs.csv"
NATIVE_LEX_PROF_MEASURE = "native_users_lex_prof_measurs.csv"



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
with open(NATIVE_LEX_PROF_MEASURE,'w+') as prof_measures_out:
    for lib in NATIVE_LIB:
#        i = 0
        for user_file in os.listdir(lib):
#            i += 1
#            print('processing ' + lib + user_file  )
    #        user = RedditUser(user_file, 'Spain')
            if user_file not in users.keys():
                    users[user_file] = RedditUser(user_file, (user_file.split(".",1)[1]).split(".")[0])
            user = users[user_file]
#            if i>10:
#                break
                    
        #        if user not in user_to_ger_count.keys():
        #            user_to_ger_count[user] = 0
        #        if user not in user_to_rom_count.keys():
        #            user_to_rom_count[user] = 0
                
            user.text_file = os.path.join(lib, user_file)
            prof_measures_out.write("{},".format(user.user_name))
                
            try:
                user.sample_size = 10000
                user.set_user_text_sample()                
                user.calculate_word_rank_measure()
                user.calculate_naming_RT_measure()
                user.calculate_AOA_measure()                
                user.set_user_text_sample
                user.calculate_type_token_ratio()
            except:
                print("skipping {} from {} \n".format(user.user_name, user.l1))
    
            prof_measures_out.write(",{},{},{},{}\n".format( user.type_token_ratio, user.avg_word_rank, user.avg_naming_RT, user.avg_age_of_aquisition))     

##        i += 1
##        if i > 10:
##            break
#        
#print("total snysets = {}".format(cognate_counter.total_syn_set_count))              
##    cognate_counter.write_cognates_vector_to_file(REDDIT_NATIVE_COUNTS_FILE,0,0)
#user_ger_ratio = {}
#user_ger_count={}
#
#for user in users.values():    
#    if user not in cognate_counter.users_cognate_counts_dict.keys():
#        print(user.user_name)
#    for synset,tokens in cognate_counter.users_cognate_counts_dict[user].items():
#        ger_counter = 0
#        rom_counter = 0
#        for word,count in tokens.items():
#            
#            if count > 0:
#                if word in synset_origin_dict.keys():
#                    if synset_origin_dict[word] == 'G':
#                        user_to_ger_count[user] += count
#                        ger_counter += count
#                    elif synset_origin_dict[word] == 'R':
#                        user_to_rom_count[user] += count
#                        rom_counter += count
#        if user not in user_ger_ratio.keys():
#            user_ger_ratio[user] = {}
#        if user not in user_ger_count:
#            user_ger_count[user]={}
#        user_ger_count[user][synset] = ger_counter
#        if rom_counter + ger_counter >0:            
#            user_ger_ratio[user][synset] = ger_counter/(ger_counter+rom_counter)       
#        else:
#            user_ger_ratio[user][synset] = -1
#        
#                        
                   
#for user,count in user_to_ger_count.items():
#    print("Germanic count: {}:{}".format(user.user_name,count))
#
#for user,count in user_to_rom_count.items():
#    print("Romance count: {}:{}".format(user.user_name,count))
                            
#for user in users.values():
#    print("Germanic count: {}:{}".format(user.user_name,user_to_ger_count[user]))            
#    print("Romance count: {}:{}".format(user.user_name,user_to_rom_count[user]))
        
#with open(NATIVE_GERMANIC_VS_ROMANCE_COUNT_FILE,"w+",encoding='utf-8') as GerVsRomOut:
#    GerVsRomOut.write("user,GermanicCount,RomanceCount\n")
#    for user in users.values():
#with open(REDDIT_NATIVE_COUNTS_FILE, "w+") as CountOut:
#    with open(NATIVE_GERMANIC_RATIO_FILE,"w+",encoding='utf-8') as GerRatioOut: 
#        GerRatioOut.write(",")
#        CountOut.write(",")
#        for synset in range(1,cognate_counter.total_syn_set_count+1):
#            GerRatioOut.write("{},".format(synset))  
#            CountOut.write("{},".format(synset))
#        GerRatioOut.write("\n")
#        CountOut.write("\n")
#        for user in user_ger_ratio.keys():        
#             GerRatioOut.write("{},".format(user.user_name))
#             CountOut.write("{},".format(user.user_name))
#             for synset in range(1,cognate_counter.total_syn_set_count+1):
#                GerRatioOut.write("{},".format(user_ger_ratio[user][synset]))
#                CountOut.write("{},".format(user_ger_count[user][synset]))
#             GerRatioOut.write("\n")
#             CountOut.write("\n")
        
#    GerRatioOut.write(",Germanic_Ratio_Mean\n")      
#    ger_ratio_mean ={}
#    for user,synset in user_ger_ratio.items():
#        ger_ratio_mean[user] = mean(user_ger_ratio[user].values())
#    for user in ger_ratio_mean.keys():
#        GerRatioOut.write("{},{}\n".format(user.user_name,ger_ratio_mean[user]))
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
    



