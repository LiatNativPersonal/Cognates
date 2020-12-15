# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:21:03 2018

@author: TAL-LAPTOP
"""
import os
#import re
from RedditUser import RedditUser
from RedditLanguage import RedditLanguage
from RedditCognatesCounter import RedditCognatesCounter
from dateutil.parser import parse
from pathlib import Path
import csv
import nltk
from LanguageOrigin import LanguageOrigin
from statistics import mean

GERMANIC_INPUT_DIR = "C:/Users/liatn/Documents/Liat/Research/Reddit/Germanic/"
ROMANCE_INPUT_DIR="C:/Users/liatn/Documents/Liat/Research/Reddit/Romance/"
NATIVE_INPUT_DIR = "C:/Users/liatn/Documents/Liat/Research/Reddit/Native/"

GERMANIC_USERS_FOCUS_SET_DB = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/NoBound/"
ROMANCE_USERS_FOCUS_SET_DB = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/NoBound/"
NATIVE_USERS_FOCUS_SET_DB = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/NoBound/"
COGNATES_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list.csv"
SYNSET_ORIGIN = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list_with_origin.csv'
NATIVE_ENGLISH = ["US", "UK","Ireland","Australia", "NewZealand"]
COGNATE_TO_LANGUAGE_FAMILY = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/cognates_origin.csv"
GERMANIC_ORIGIN = ["Iceland","Sweden","Germany","Austria","Netherlands","Norway","Denmark"]
ROMANCE_ORIGIN = ["Romania","Portugal","Spain","Italy","France","Mexico","Argentina","Brazil","Venezuela","Sardinia","Andorra"]

NATIVE_FINAL_USER_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Summer2020/down_sampled_native_extended_list_over_500_cog_200_synsets.csv"
GERMANIC_FINAL_USER_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Summer2020/down_sampled_germanic_extended_list_over_500_cog_200_synsets.csv"
ROMANCE_FINAL_USER_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Summer2020/romance_extended_list_over_500_cog_200_synsets.csv"
#GERMANIC_INPUT_DIR = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/"
#ROMANCE_INPUT_DIR = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/"
#NATIVE_INPUT_DIR = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/"

REDDIT_NATIVE_COUNTS_FILE = "native_users_synsets_germanic_count.csv"
REDDIT_GERMANIC_COUNTS_FILE = "germanic_users_synsets_germanic_count.csv"
REDDIT_ROMANCE_COUNTS_FILE = "romance_users_synsets_germanic_count.csv"
NATIVE_GERMANIC_RATIO_FILE = "native_users_synsets_germanic_ratio.csv"
GERMANIC_GERMANIC_RATIO_FILE = "germanic_users_synsets_germanic_ratio.csv"
ROMANCE_GERMANIC_RATIO_FILE = "romance_users_synsets_germanic_ratio.csv"
NATIVE_GERMANIC_VS_ROMANCE_COUNT_FILE = "Native_Users_Romance_Vs_Germanic.csv"   

class RedditUserInfoCollector:    
    
    def is_date(string):
        try: 
            parse(string) 
            return True
        except ValueError:
            return False
    
    def __init__(self, p_input_dir):
        self.input_dir = p_input_dir
        self.users = {}

    def collect_info(self):
        existing_users=[]
        for user_file in os.listdir(NATIVE_INPUT_DIR):
            existing_users.append(user_file.split(".")[0])
     
        cognate_counter = RedditCognatesCounter(SYNSET_ORIGIN)
        print("input_dir" + self.input_dir)
        for file in os.listdir(self.input_dir):    
            if not file.startswith("reddit.") or not file.endswith('.csv'):
                continue 
#            if "Albania" not in file:
#                continue;                             
            country_name_pefix= file.replace("reddit.","")
            country = country_name_pefix[0:country_name_pefix.find(".")]
            language = RedditLanguage(country)
            file_path = os.path.join(self.input_dir,file) 
            
            print("Processing {}".format(language.country_name))
#            if language.country_name != "Egypt":
#                continue
            
            wrong_lines = 0
            users = {}
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as country_file:                
                users.clear()  
                if language.country_name == 'Austria':
                    continue
                csvreader = csv.reader(country_file, delimiter=',')
                language.file = file_path
                for line in csvreader:                                         
                # user_name apears in the begining of every row inside []
                    if len(line) != 4:
                        wrong_lines += 1
                        continue
                    user_name = line[0]                   
                    if user_name in existing_users:
                        continue
                    if len(self.users.keys()) == 0 or language not in self.users.keys() or user_name not in self.users[language].keys():  
                            user = RedditUser(user_name, language.country_name)    #                                print("NEW_USER: " + user_name)
                    else:
                            user = self.users[language][user_name]
                            
                    language.set_origin()
                         
                    if language not in self.users.keys():
                        self.users[language]={}
                        
                    self.users[language][user_name] = user
                    text_line = line[3]                   
                    text_line = nltk.word_tokenize(text_line)
                    number_of_tokens = len(text_line)                           
                    self.users[language][user_name].number_of_sentences += 1
                    self.users[language][user_name].number_of_tokens += number_of_tokens  
                    cognate_counter.count_cognate_for_user_line(user, text_line)
#        cognate_counter.write_cognates_vector_to_file("native_cognate_vectors.csv",10000,500)
                    
#                    if (user not in users.keys()):
#                        users[user] = []                
#                    users[user].append(text_line)                
#            RedditUserInfoCollector.count_total_cognates(users)
                
#    def count_total_cognates(users):
#        cognates_counter = RedditCognatesCounter(COGNATES_LIST)
#        with open("non_native_total_cognate_count.csv", "a+") as total_cognates:
#            for user, text in users.items():
#                cognates_counter.get_total_cognate_count_for_user(user, text)
#                if user.totalCognateCount > 100 and user.number_of_tokens >= 10000:                
#                    print("processing {} , total cognate count: {} , # of tokens: {} , # of sentences: {}\n".format(user.user_name, user.totalCognateCount, user.number_of_tokens, user.number_of_sentences))
#                    total_cognates.write("{} ,{} ,{} ,{}\n".format(user.user_name,  user.totalCognateCount, user.number_of_tokens, user.number_of_sentences))
        
        
    def load_users_info_from_file(self, users_file, user_text_file_dir):        
        with open(users_file, 'r', encoding='utf-8', errors="ignore") as user_info_file:
            reader = csv.reader(user_info_file, delimiter=',')
            #ignore header            
            next(reader, None)
            for user_row in reader:                
#                if len(user_row) != 5 :
                if len(user_row) != 6 :
                    continue                
                country_name = user_row[0]
                user_name = user_row[1]
                number_of_cognates = int(user_row[3])
#                number_of_sentences = int(user_row[3])
#                number_of_tokens = int(user_row[4])                
                file_name = "reddit." + country_name + ".clean.en.sent.csv"
                country_file = os.path.join(self.input_dir,file_name) 
                language = RedditLanguage(country_name)
                language.file = country_file
                language.set_origin()
                user = RedditUser(user_name, country_name)
                user.totalCognateCount = number_of_cognates
#                user.number_of_tokens = number_of_tokens
#                user.number_of_sentences = number_of_sentences
                user_text_file_name = user.user_name +"." +user.l1 + ".txt"
                if user_text_file_name in os.listdir(user_text_file_dir):
                    user.text_file = os.path.join(user_text_file_dir, user_text_file_name)
                    # print(user.text_file)
                if language not in self.users.keys():
                    self.users[language]={}
                self.users[language][user_name] = user
                
    def create_user_text_files(self, min_amount_of_tokens, min_amount_of_cognates, min_amount_of_synsets, origin, destination):
        for language, users_dict in self.users.items():            
            print (language.country_name)
            language.set_origin()
            if language.origin != origin:
                continue            
            users_focus_set = {}            
#            if language.country_name != "Israel":
#                continue
            
            
            for user_name, user in users_dict.items():                        
                if user.number_of_tokens < min_amount_of_tokens or user.totalCognateCount < min_amount_of_cognates or user.totalSynsetUsed < min_amount_of_synsets:
                    continue;
                print(user.user_name + " " + str(user.number_of_tokens))
                users_focus_set[user_name] = user
#            print("********focus users*********")          
            
            with open(language.file, 'r', encoding='utf-8', errors='ignore') as l1_file:
                print("reading file: " + language.file)
                reader = csv.reader(l1_file, delimiter=',')
                for line in reader:
                    if len(line) != 4:                            
                        continue
#                    print(line)
                    user_name = line[0]      
                
                    if user_name in users_focus_set.keys():
#                        print("found : " + users_focus_set[user_name].user_name)
                        users_focus_set[user_name].text.append(str(line[3]) + "\n")
                            
            for user in users_focus_set.values():
                print (user.user_name)
                with open('log.txt', "a") as log:
                    log.write("writing user file " +  user.user_name + "\n")                    
                    user.dump__text_to_file(destination + user.user_name + "." + language.country_name + ".txt")
            self.users[language] = users_focus_set
                            
            
       
    
    def dump_users_info_to_file(self, output_file, min_amount_of_tokens, min_amount_of_cognates, min_amount_of_synsets):
      with open(output_file,"w", encoding="utf-8") as output:   
          output.write('Country, UserName, cognates#,synsets#, sentences#, tokens#\n')
          for language, users in self.users.items(): 
              for user in self.users[language].values():
                  if user.number_of_tokens >= min_amount_of_tokens and user.totalCognateCount >= min_amount_of_cognates and user.totalSynsetUsed >= min_amount_of_synsets:
                      output.write(language.country_name + "," + user.user_name + "," + str(user.totalCognateCount) + "," + str(user.totalSynsetUsed) + "," + str(user.number_of_sentences) + "," + str(user.number_of_tokens) + '\n')
      return

    
    
    
    



    
def Main():    
    
    # reddit_user_info_collector = RedditUserInfoCollector(GERMANIC_INPUT_DIR)
    
    ##Creating text files for all users no limits on cognates count or number of synsests in use
#     for country in os.listdir(GERMANIC_INPUT_DIR):
#         print(country)
#         country_users = {}
#         with open(os.path.join(GERMANIC_INPUT_DIR,country),'r',encoding='utf-8') as country_file:
#             country_name = country[7:country.find(".clean")]
            
#             print("reading file: " + country_name)
#             # break
#             reader = csv.reader(country_file, delimiter=',')
#             for line in reader:
#                 if len(line) != 4:                            
#                     continue
# #                    print(line)
#                 user_name = line[0]      
                
#                 if user_name not in country_users.keys():
#                     country_users[user_name] = []
#                 country_users[user_name].append(str(line[3]) + "\n")
#             for user in country_users.keys():
#                 with open("{}{}.{}.txt".format(GERMANIC_USERS_FOCUS_SET_DB,user,country_name),'w',encoding='utf-8') as user_file:
#                     user_file.write("".join(country_users[user]))
                    
                        
                #     user.dump__text_to_file(destination + user.user_name + "." + language.country_name + ".txt")
                # self.users[language] = users_focus_set
        
    
    # reddit_user_info_collector.collect_info() 
    # reddit_user_info_collector.dump_users_info_to_file("romance_no_bound_list.csv",0,0,0)
    # reddit_user_info_collector.create_user_text_files(0,0,0,LanguageOrigin.GERMANIC, GERMANIC_USERS_FOCUS_SET_DB)
    # reddit_user_info_collector.load_users_info_from_file(ROMANCE_FINAL_USER_DATASET, ROMANCE_USERS_FOCUS_SET_DB)
    
    # i=1
    
#    reddit_user_info_collector.collect_info()
#    reddit_user_info_collector.dump_users_info_to_file("natives_over_1000_cog.csv",10000,1000)
#    print(len(reddit_user_info_collector.users.values()))
#    reddit_user_info_collector.load_users_info_from_file("natives_over_1000_cog.csv", NATIVE_USERS_FOCUS_SET_DB)
#    reddit_user_info_collector.create_user_text_files(10000,1000,True)
#    reddit_user_info_collector.load_users_info_from_file("16_4_non_native_users_short.csv", NON_NATIVE_USERS_FOCUS_SET_DB)
     cognate_counter = RedditCognatesCounter(SYNSET_ORIGIN)
     length = len(os.listdir(NATIVE_USERS_FOCUS_SET_DB))
     i = 1
     for f in os.listdir(NATIVE_USERS_FOCUS_SET_DB):
         print("processing {}: {} out of {} users".format(f,i,length  ))
         user_file = os.path.join(NATIVE_USERS_FOCUS_SET_DB,f)
         user_name = f.split('.')[0]
         country = f[f.find('.')+1:f.find(".txt")]
         # print(f)
         # print(user_name)
         # print(country)
         
         user = RedditUser(user_name, country)
         user.text_file = user_file
         cognate_counter.count_cognates_for_user(user)
         i += 1
     cognate_counter.write_cognates_vector_to_file("native)sers_counts.csv",0,0)
   
     
#    with open("01.05_8-4_eng_prof_measures.csv", "w+", encoding="utf-8") as measure_output:
#        measure_output.write("username, cognates#, TTR, Mean word rank, Mean naming RT, AoA\n")
# #        print(reddit_user_info_collector.users.values())
#     synset_origin_dict={}
#     with open(SYNSET_ORIGIN,'r') as origin_file:
#         reader = csv.reader(origin_file, delimiter=',')            
#         next(reader) #skipping header    
#         for line in reader:       
#            synset_origin_dict[line[1]] = line[2]
           
#     for language in reddit_user_info_collector.users.values():   
#        for user in language.values():
# ##                if user.l1 not in GERMANIC_ORIGIN:
# ##                    continue
#                 # if i>10:
#                      # break
#                 print("procesing {} from {} \n".format(user.user_name, user.l1))
# #                try:
# #                    user.sample_size = 10000
# #                    user.set_user_text_sample()                
# #                    user.calculate_word_rank_measure()
# #                    user.calculate_naming_RT_measure()
# #                    user.calculate_AOA_measure()                
# #                    user.set_user_text_sample
# #                    user.calculate_type_token_ratio()
# #                except:
# #                    print("skipping {} from {} \n".format(user.user_name, user.l1))
#                 cognate_counter.count_cognates_for_user(user)
#                 # i+=1
# #                measure_output.write("{}_{},,{},{},{},{}\n".format(user.user_name, user.l1, user.type_token_ratio, user.avg_word_rank, user.avg_naming_RT, user.avg_age_of_aquisition))      

    
#     cognate_counter.write_cognates_vector_to_file("andorra_vectors.csv",1, 1)
    # i=1
    # user_ger_ratio = {}
    # user_ger_count = {}
    # user_to_ger_count = {}  
    # user_to_rom_count = {} 
    # for language in reddit_user_info_collector.users.values():   
    #    for user in language.values():
    #        # if i>10:
    #        #     break
    #        if user not in cognate_counter.users_cognate_counts_dict.keys():
    #             print(user.user_name)
    #        if user not in user_to_ger_count.keys():
    #             user_to_ger_count[user] = 0
    #        if user not in user_to_rom_count.keys():
    #             user_to_rom_count[user] = 0
    #        for synset,tokens in cognate_counter.users_cognate_counts_dict[user].items():
    #             ger_counter = 0
    #             rom_counter = 0
    #             for word,count in tokens.items():
                    
    #                 if count > 0:
    #                     if word in synset_origin_dict.keys():
    #                         if synset_origin_dict[word] == 'G':
    #                             user_to_ger_count[user] += count
    #                             ger_counter += count
    #                         elif synset_origin_dict[word] == 'R':
    #                             user_to_rom_count[user] += count
    #                             rom_counter += count
    #             if user not in user_ger_ratio.keys():
    #                 user_ger_ratio[user] = {}
    #             if user not in user_ger_count:
    #                 user_ger_count[user]={}
    #             user_ger_count[user][synset] = ger_counter
    #             if rom_counter + ger_counter >0:            
    #                 user_ger_ratio[user][synset] = ger_counter/(ger_counter+rom_counter)       
    #             else:
    #                 user_ger_ratio[user][synset] = -1
    #        # i+=1
    
       
    
    # with open(REDDIT_GERMANIC_COUNTS_FILE, "w+") as CountOut:
    #     with open(GERMANIC_GERMANIC_RATIO_FILE,"w+",encoding='utf-8') as GerRatioOut: 
    #         GerRatioOut.write(",")
    #         CountOut.write(",")
    #         for synset in range(1,cognate_counter.total_syn_set_count+1):
    #             GerRatioOut.write("{},".format(synset))  
    #             CountOut.write("{},".format(synset))
    #         GerRatioOut.write("TTR,WORD_RANK,NAMING_RT,AOA")
    #         GerRatioOut.write("\n")
    #         CountOut.write("\n")
    #         for user in user_ger_ratio.keys():        
    #             GerRatioOut.write("{},".format(user.user_name))
    #             CountOut.write("{},".format(user.user_name))
    #             for synset in range(1,cognate_counter.total_syn_set_count+1):
    #                 GerRatioOut.write("{},".format(user_ger_ratio[user][synset]))
    #                 CountOut.write("{},".format(user_ger_count[user][synset]))
    #             try:
    #                 user.sample_size = 10000
    #                 user.set_user_text_sample()                
    #                 user.calculate_word_rank_measure()
    #                 user.calculate_naming_RT_measure()
    #                 user.calculate_AOA_measure()                
    #                 user.set_user_text_sample
    #                 user.calculate_type_token_ratio()
    #             except:
    #                 print("skipping {} from {} \n".format(user.user_name, user.l1))
    #     #                cognate_counter.count_cognates_for_user(user)
    #             GerRatioOut.write("{},{},{},{}\n".format( user.type_token_ratio, user.avg_word_rank, user.avg_naming_RT, user.avg_age_of_aquisition))        
    #             CountOut.write("\n")
            


    # return
    
if __name__ == '__main__':
    Main()
        
        
        