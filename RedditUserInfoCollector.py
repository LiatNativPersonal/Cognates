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

NON_NATIVE_INPUT_DIR = "C:/Users/liatn/Documents/Liat/Research/Reddit/Reddit.Extended/Non-Native/"
NATIVE_INPUT_DIR = "C:/Users/liatn/Documents/Liat/Research/Reddit/Reddit.Extended/Native/"
NON_NATIVE_USERS_FOCUS_SET_DB = "C:/Users/liatn/Documents/Liat/Research/Cognates/MassiveUsersDB/NonNative/Chosen/"
NATIVE_USERS_FOCUS_SET_DB = "C:/Users/liatn/Documents/Liat/Research/Cognates/MassiveUsersDB/Native/Chosen/"
NATIVE_ENGLISH = ["US", "UK","Ireland","Australia", "NewZealand"]
COGNATES_LIST = "c:/Users/liatn/Documents/Liat/Research/Cognates/cognates_info/synsets.mult.final.100.dat"
COGNATE_TO_LANGUAGE_FAMILY = "c:/Users/liatn/Documents/Liat/Research/Cognates/cognates_info/cognate_to_family.csv"
GERMANIC_ORIGIN = ["Iceland","Sweden","Germany","Austria","Netherlands","Norway","Finland","Denmark"]
ROMANCE_ORIGIN = ["Romania","Portugal","Spain","Italy","France","Mexico","Argentina","Brazil","Venezuela","Sardinia","Andorra"]


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
        cognate_counter = RedditCognatesCounter(COGNATES_LIST)
        print("input_dir" + self.input_dir)
        for file in os.listdir(self.input_dir):    
            if not file.startswith("reddit.") or not file.endswith('.csv'):
                continue 
#            if "Albania" not in file:
#                continue;                             
            country_name_pefix= file.replace("reddit.","")
            language = RedditLanguage(country_name_pefix[0:country_name_pefix.find(".")])
            file_path = os.path.join(self.input_dir,file) 
            
            print("Processing {}".format(language.country_name))
#            if language.country_name != "Egypt":
#                continue
            
            wrong_lines = 0
            users = {}
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as country_file:                
                users.clear()  
                csvreader = csv.reader(country_file, delimiter=',')
                language.file = file_path
                for line in csvreader:                                         
                # user_name apears in the begining of every row inside []
                    if len(line) != 4:
                        wrong_lines += 1
                        continue
                    user_name = line[0]                   
                    
                    if len(self.users.keys()) == 0 or language not in self.users.keys() or user_name not in self.users[language].keys():  
                            user = RedditUser(user_name, language.country_name)    #                                print("NEW_USER: " + user_name)
                    else:
                            user = self.users[language][user_name]
                            
                    if language.country_name in NATIVE_ENGLISH:                            
                         language.native_engslish = True
                         
                    if language not in self.users.keys():
                        self.users[language]={}
                        
                    self.users[language][user_name] = user
                    text_line = line[3]                   
                    text_line = nltk.word_tokenize(text_line)
                    number_of_tokens = len(text_line)                           
                    self.users[language][user_name].number_of_sentences += 1
                    self.users[language][user_name].number_of_tokens += number_of_tokens  
                    cognate_counter.count_cognate_for_user_line(user, text_line)
        cognate_counter.write_cognates_vector_to_file("native_cognate_vectors.csv",10000,1000)
                    
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
                if len(user_row) != 4 :
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
                language.native_engslish = language.country_name in NATIVE_ENGLISH 
                user = RedditUser(user_name, country_name)
                user.totalCognateCount = number_of_cognates
#                user.number_of_tokens = number_of_tokens
#                user.number_of_sentences = number_of_sentences
                user_text_file_name = "sampled_" + user.user_name +"." +user.l1 + ".txt"
                if user_text_file_name in os.listdir(user_text_file_dir):
                    user.text_file = os.path.join(user_text_file_dir, user_text_file_name)
                if language not in self.users.keys():
                    self.users[language]={}
                self.users[language][user_name] = user
                
    def create_user_text_files(self, min_amount_of_tokens, min_amount_of_cognates, is_native_english):
        for language, users_dict in self.users.items():            
            print (language.country_name)
            if language.native_engslish != is_native_english:
                continue            
            users_focus_set = {}            
#            if language.country_name != "Israel":
#                continue
            
            
            for user_name, user in users_dict.items():                        
                if user.number_of_tokens < min_amount_of_tokens or user.totalCognateCount < min_amount_of_cognates :
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
                    user_file_path = ""
                    if language.native_engslish:
                        user_file_path += NATIVE_USERS_FOCUS_SET_DB
                    else:
                        user_file_path += NON_NATIVE_USERS_FOCUS_SET_DB
                    user_file_path += (user.user_name + "." + language.country_name + ".txt")
                    
                    user.dump__text_to_file(user_file_path)
            self.users[language] = users_focus_set
                            
            
       
    
    def dump_users_info_to_file(self, output_file, min_amount_of_tokens, min_amount_of_cognates):
      with open(output_file,"w", encoding="utf-8") as output:   
          output.write('Country, UserName, cognates#, sentences#, tokens#\n')
          for language, users in self.users.items():
              for user in self.users[language].values():
                  if user.number_of_tokens >= min_amount_of_tokens and user.totalCognateCount >= min_amount_of_cognates:
                      output.write(language.country_name + "," + user.user_name + "," + str(user.totalCognateCount) + "," + str(user.number_of_sentences) + "," + str(user.number_of_tokens) + '\n')
      return

    
    
    
    



    
def Main():    
    reddit_user_info_collector = RedditUserInfoCollector(NATIVE_INPUT_DIR)    
   # reddit_user_info_collector.load_users_info_from_file("native_out.csv", NATIVE_USERS_FOCUS_SET_DB)
    
#  
#    reddit_user_info_collector.collect_info()
#    reddit_user_info_collector.dump_users_info_to_file("natives_over_1000_cog.csv",10000,1000)
#    print(len(reddit_user_info_collector.users.values()))
#    reddit_user_info_collector.load_users_info_from_file("natives_over_1000_cog.csv", NATIVE_USERS_FOCUS_SET_DB)
#    reddit_user_info_collector.create_user_text_files(10000,1000,True)
    reddit_user_info_collector.load_users_info_from_file("16_4_non_native_users_short.csv", NON_NATIVE_USERS_FOCUS_SET_DB)
#    cognate_counter = RedditCognatesCounter(COGNATES_LIST)
    with open("01.05_8-4_eng_prof_measures.csv", "w+", encoding="utf-8") as measure_output:
        measure_output.write("username, cognates#, TTR, Mean word rank, Mean naming RT, AoA\n")
        print(reddit_user_info_collector.users.values())
        for language in reddit_user_info_collector.users.values():   
           for user in language.values():
#                if user.l1 not in GERMANIC_ORIGIN:
#                    continue
               
                print("procesing {} from {} \n".format(user.user_name, user.l1))
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
#                cognate_counter.count_cognates_for_user(user)
                measure_output.write("{}_{},,{},{},{},{}\n".format(user.user_name, user.l1, user.type_token_ratio, user.avg_word_rank, user.avg_naming_RT, user.avg_age_of_aquisition))            
#        cognate_counter.write_cognates_vector_to_file("native_cognate_vectors.csv",10000, 1000)


    return
    
if __name__ == '__main__':
    Main()
        
        
        