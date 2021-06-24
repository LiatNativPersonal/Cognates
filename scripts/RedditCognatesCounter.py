# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 18:44:45 2018

@author: TAL-LAPTOP
"""
import pandas as pd
from collections import Counter
import pickle

class RedditCognatesCounter:
                
    def __init__(self, cognates_list_file, sent_beg = "<s>", sent_end = " </s>", _POS = True):
        self.total_syn_set_count = 0
        self.users_cognate_counts_dict = {}
        self.cog_to_syn_set = {}
        self.cognates_df = pd.read_csv(cognates_list_file)
        self.POS = _POS
        if self.POS:
            self.word_list = list(self.cognates_df['word'] + "_" + self.cognates_df['POS'])
        else:
            self.word_list = list(self.cognates_df['word'])
        self.user_word_to_count = {}
        self.begin_sentence_marker = sent_beg
        self.end_sentence_marker = sent_end

        

    # this is a nested dictionary of dictionaris maps a user to an additional dictionary that maps 
    # synset to a dictionary that maps cognate to its number of occurences
    def init_user_cognate_count_dict(self):
        if self.POS:
            user_cog_df = self.cognates_df[['synset','word','Source','POS']].copy()
        else:
            user_cog_df = self.cognates_df[['synset', 'word', 'Source']].copy()
        user_cog_df['count'] = 0
        return user_cog_df
    
    # def get_total_cognate_count_for_user(self, user, user_text):
    #     # lemmatizer = WordNetLemmatizer()
    #     for line in user_text:
    #          for token in line:
    #             basic_token = lemmatizer.lemmatize(token)
    #             if token in self.cog_to_syn_set.keys() or basic_token in self.cog_to_syn_set.keys():
    #                 user.totalCognateCount += 1
            
    # def count_cognate_for_user_line(self,user, tok_line):
    #     lemmatizer = WordNetLemmatizer()
    #     for token in tok_line:
    #         basic_token = lemmatizer.lemmatize(token)
    #         if token in self.word_list:
    #             self.update_user_cognate_counts(token, user)
    #         elif basic_token in self.word_list:
    #             self.update_user_cognate_counts(basic_token, user)
            
            
    def update_user_cognate_counts(self, cognate,user):
        if user not in self.user_word_to_count.keys():
            self.user_word_to_count[user] = {}
        if cognate not in self.user_word_to_count.keys():
            self.user_word_to_count[user][cognate] = 0
        self.user_word_to_count[user][cognate] += 1
        
        
    def count_cognates_for_user(self, user, pickled = False):

        # lemmatizer = WordNetLemmatizer()
        if user not in self.users_cognate_counts_dict.keys():
            self.users_cognate_counts_dict[user] = self.init_user_cognate_count_dict()
        if pickled:
            fh = open(user.text_file, 'rb')
        else:
            fh = open(user.text_file, 'r', encoding='utf-8')
        raw_text = []
        if pickled:
            raw_text = pickle.load(fh)
            # print(raw_text[0:10])
        else:
            raw_text = fh.read().split("\n")
        text = [x.replace(self.begin_sentence_marker,'').replace(self.end_sentence_marker,'') for x in raw_text]
        words = [word for row in text for word in row.split(" ")]
        cnt = Counter(words)

        self.user_word_to_count[user] = {key:cnt[key] for key in cnt if key in self.word_list}
        extra = {x:0 for x in self.word_list if x not in self.user_word_to_count[user].keys()}
        self.user_word_to_count[user].update(extra)
        for word in self.word_list:
            if self.POS:
                lemma, pos = word.split("_")

            user_df = self.users_cognate_counts_dict[user]
            count = self.user_word_to_count[user][word]
            if self.POS:
                user_df.loc[(user_df['word'] == lemma) & (user_df['POS'] == pos), 'count'] = count
            else:
                user_df.loc[(user_df['word'] == word), 'count'] = count
        fh.close()
    
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
                            