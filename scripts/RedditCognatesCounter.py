# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 18:44:45 2018

@author: TAL-LAPTOP
"""
import nltk
from nltk.stem import WordNetLemmatizer 
#from nltk.stem.porter import PorterStemmer

class RedditCognatesCounter:
    

    def read_cognages_list(self, cognates_list_file):
        cog_list = {}
        with open(cognates_list_file, "r", encoding="utf-8") as cognates_file:
            syn_set_count = 0
            for line in cognates_file:
                syn_set_count += 1
                cog_syn_set_list=[]
                for cognate in line.split():
                    cognate = cognate.strip()
                    cog_syn_set_list.append(cognate)
                    if cognate not in self.cog_to_syn_set.keys():
                        self.cog_to_syn_set[cognate] = []                        
                    self.cog_to_syn_set[cognate].append(syn_set_count)
                cog_list[syn_set_count] = cog_syn_set_list
            self.total_syn_set_count = syn_set_count
        return cog_list
                
    def __init__(self, cognates_list_file):
        self.total_syn_set_count = 0
        self.users_cognate_counts_dict = {}
        self.cog_to_syn_set = {}        
        self.cognates_list = self.read_cognages_list(cognates_list_file)
        

    # this is a nested dictionary of dictionaris maps a user to an additional dictionary that maps 
    # synset to a dictionary that maps cognate to its number of occurences
    def init_user_cognate_count_dict(self):
        cog_count_dict = {}
        for key,synset in self.cognates_list.items():
            syn_set_dict={}
            cog_count_dict[key] = syn_set_dict
            for cognate in synset:
                syn_set_dict[cognate] = 0
        return cog_count_dict
    
    def get_total_cognate_count_for_user(self, user, user_text):
        lemmatizer = WordNetLemmatizer()
        for line in user_text:  
             for token in line:               
                basic_token = lemmatizer.lemmatize(token)   
                if token in self.cog_to_syn_set.keys() or basic_token in self.cog_to_syn_set.keys():                        
                    user.totalCognateCount += 1
            
    def count_cognate_for_user_line(self,user, tok_line): 
        
        if user not in self.users_cognate_counts_dict.keys():
            self.users_cognate_counts_dict[user] = self.init_user_cognate_count_dict()
        lemmatizer = WordNetLemmatizer()        
        for token in tok_line:
            basic_token = lemmatizer.lemmatize(token) 
            if token in self.cog_to_syn_set.keys():
                for synset in self.cog_to_syn_set[token]:      
                     if self.users_cognate_counts_dict[user][synset][token] == 0:
                         user.totalSynsetUsed += 1
                     self.users_cognate_counts_dict[user][synset][token] += 1
            elif basic_token in self.cog_to_syn_set.keys():
                for synset in self.cog_to_syn_set[basic_token]: 
                    if self.users_cognate_counts_dict[user][synset][basic_token] == 0:
                         user.totalSynsetUsed += 1
                    self.users_cognate_counts_dict[user][synset][basic_token] += 1
            else:
                continue
            user.totalCognateCount += 1
            
            
        
    def count_cognates_for_user(self, user):   
        with open(user.text_file, "r", encoding="utf-8") as input_file:   
            for line in input_file:               
                line = nltk.word_tokenize(line)
                self.count_cognate_for_user_line(user, line)
#                tok_line = nltk.word_tokenize(line)
#                for token in tok_line:
#                    basic_token = lemmatizer.lemmatize(token)   
#                    if token in self.cog_to_syn_set.keys():
#                        for synset in self.cog_to_syn_set[token]:                                             
#                            cognate_count_dict[synset][token] += 1
#                    elif basic_token in self.cog_to_syn_set.keys():
#                        for synset in self.cog_to_syn_set[basic_token]:
#                            cognate_count_dict[synset][basic_token] += 1
#            self.users_cognate_counts_dict[user] =  cognate_count_dict       
#            print("betray_count = " + str(betray_count))
#            print("basic_betray_count = " + str(basic_betray_count))

    def write_cognates_vector_to_file(self, output_file_path, min_amount_of_tokens, min_amount_of_cognates ):
        with open(output_file_path, "w", encoding="utf-8") as output:
            with open("norm_" + output_file_path, "w", encoding="utf-8") as norm_output:
                users = " ,"
                for user in self.users_cognate_counts_dict.keys():
                    if user.totalCognateCount < min_amount_of_cognates or user.number_of_tokens < min_amount_of_tokens:
                        continue
                    users += " ," + user.user_name + "." + user.l1
                    
                users += "\n"
                output.write(users)
                norm_output.write(users)               
                for synset, cognates in self.cognates_list.items():    
                    for cognate in cognates:  
                            output.write(str(synset) + ", " + cognate)
                            norm_output.write(str(synset) + ", " + cognate)
                            for user in self.users_cognate_counts_dict.keys():                                
                                cog_norm_count = ""
                                syn_set_sum = sum(self.users_cognate_counts_dict[user][synset].values())                                                     
                                count = self.users_cognate_counts_dict[user][synset][cognate]
                                if syn_set_sum == 0:                                                                                     
                                    cog_norm_count = ", " + str(count)                                                  
                                else:
                                    cog_norm_count = ", " + str(count/syn_set_sum)
                                
                                output.write( ", " + str(count))
                                norm_output.write(cog_norm_count)
                            output.write( "\n")
                            norm_output.write("\n")
       
#    def init_from_file(self, ,cognates_list_file, user_info_file):
                            