# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 18:44:45 2018

@author: TAL-LAPTOP
"""
import nltk
from nltk.stem import WordNetLemmatizer 
#from nltk.stem.porter import PorterStemmer
import pandas as pd
from collections import Counter

class RedditCognatesCounter:
                
    def __init__(self, cognates_list_file):
        self.total_syn_set_count = 0
        self.users_cognate_counts_dict = {}
        self.cog_to_syn_set = {}
        self.cognates_df = pd.read_csv(cognates_list_file)
        self.word_list = self.cognates_df['word'] + "_" + self.cognates_df['POS']
        self.user_word_to_count = {}
        

    # this is a nested dictionary of dictionaris maps a user to an additional dictionary that maps 
    # synset to a dictionary that maps cognate to its number of occurences
    def init_user_cognate_count_dict(self):
        user_cog_df = self.cognates_df[['synset','word','Source']].copy()
        user_cog_df['count'] = 0
        return user_cog_df
    
    def get_total_cognate_count_for_user(self, user, user_text):
        lemmatizer = WordNetLemmatizer()
        for line in user_text:  
             for token in line:               
                basic_token = lemmatizer.lemmatize(token)   
                if token in self.cog_to_syn_set.keys() or basic_token in self.cog_to_syn_set.keys():                        
                    user.totalCognateCount += 1
            
    def count_cognate_for_user_line(self,user, tok_line):
        lemmatizer = WordNetLemmatizer()        
        for token in tok_line:
            basic_token = lemmatizer.lemmatize(token) 
            if token in self.word_list:
                self.update_user_cognate_counts(token, user)
                # for synset in list((user_df.loc[user_df['word'] == token])['synset']):
                #     if (user_df.loc[user_df['synset']==synset])['count'].sum() == 0:
                # # for  synset in self.cog_to_syn_set[token]:      
                # #      if self.users_cognate_counts_dict[user][synset][token] == 0:
                #          user.totalSynsetUsed += 1
                #      # self.users_cognate_counts_dict[user][synset][token] += 1
                #     user_df.loc[user_df['word']== token,'count'] += 1
            elif basic_token in self.word_list:
                self.update_user_cognate_counts(basic_token, user)
                # for synset in list((user_df.loc[user_df['word'] == basic_token])['synset']):
                #     if (user_df.loc[user_df['synset']==synset])['count'].sum() == 0:
                #        user.totalSynsetUsed += 1
                #     user_df.loc[user_df['word']== basic_token,'count'] += 1
                   
                # for synset in self.cog_to_syn_set[basic_token]: 
                #     if self.users_cognate_counts_dict[user][synset][basic_token] == 0:
                #          user.totalSynsetUsed += 1
                    # self.users_cognate_counts_dict[user][synset][basic_token] += 1
            # else:
            #     continue
            
            
    def update_user_cognate_counts(self, cognate,user):
        if user not in self.user_word_to_count.keys():
            self.user_word_to_count[user] = {}
        if cognate not in self.user_word_to_count.keys():
            self.user_word_to_count[user][cognate] = 0
        self.user_word_to_count[user][cognate] += 1
        
        
    def count_cognates_for_user(self, user):
        # self.user_word_to_count[user] = Counter(dict((w, 0) for w in self.word_list))
        lemmatizer = WordNetLemmatizer()  
        if user not in self.users_cognate_counts_dict.keys():
            self.users_cognate_counts_dict[user] = self.init_user_cognate_count_dict()
            # user_df = self.users_cognate_counts_dict[user]
        with open(user.text_file, "r", encoding="utf-8") as input_file:
            tok_rows = [nltk.word_tokenize(row) for row in input_file.read().split("\n")]
            tok_words = [word.lower() for row in tok_rows for word in row]           
            lemmatized_words = [(lemmatizer.lemmatize(word)).lower() for word in tok_words]     
            diff = list((Counter(tok_words) - Counter(lemmatized_words)).elements())
            full = lemmatized_words + diff
            cnt = Counter(full)
            self.user_word_to_count[user] = {key:cnt[key] for key in cnt if key in self.word_list}
            extra = {x:0 for x in self.word_list if x not in self.user_word_to_count[user].keys()}
            self.user_word_to_count[user].update(extra)
            for word in self.word_list:
                user_df = self.users_cognate_counts_dict[user]
                # print(word)
                # print(self.user_word_to_count[user][word])
                count = self.user_word_to_count[user][word]
                user_df.loc[(user_df.word == word),'count'] = count
                # if count > 0:
                #     print(word)
                #     print(user_df[user_df['word'] == word])






    
                
    
    
    def write_cognates_vector_to_file(self, output_file_path, min_amount_of_tokens, min_amount_of_cognates ):
        with open(output_file_path, "w", encoding="utf-8") as output:
            # with open("norm_" + output_file_path, "w", encoding="utf-8") as norm_output:
            users = ""
            for user in self.user_word_to_count.keys():
                if user.totalCognateCount < min_amount_of_cognates or user.number_of_tokens < min_amount_of_tokens:
                    print('not enough')
                    continue
                users += "," + user.user_name + "." + user.l1
            output.write("synset, word, source{}\n".format(users))
            
                # norm_output.write(users)
            for row in self.cognates_df.iterrows():
                data = row[1]
                output.write("{},{},{}".format(data['synset'], data['word'],data['Source']))
                for user in self.users_cognate_counts_dict.keys():
                    count = 0
                    if data['word'] in self.user_word_to_count[user].keys():
                        count = self.user_word_to_count[user][data['word']]
                    output.write(",{}".format(count))
                output.write("\n")
                # for cognate in cognates:  
                    #         output.write(str(synset) + ", " + cognate)
                    #         norm_output.write(str(synset) + ", " + cognate)
                    #         for user in self.users_cognate_counts_dict.keys():                                
                    #             cog_norm_count = ""
                    #             syn_set_sum = sum(self.users_cognate_counts_dict[user][synset].values())                                                     
                    #             count = self.users_cognate_counts_dict[user][synset][cognate]
                    #             if syn_set_sum == 0:                                                                                     
                    #                 cog_norm_count = ", " + str(count)                                                  
                    #             else:
                    #                 cog_norm_count = ", " + str(count/syn_set_sum)
                                
                    #             output.write( ", " + str(count))
                    #             norm_output.write(cog_norm_count)
                    #         output.write( "\n")
                    #         norm_output.write("\n")
       
#    def init_from_file(self, ,cognates_list_file, user_info_file):
                            