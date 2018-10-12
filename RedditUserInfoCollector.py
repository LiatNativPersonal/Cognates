# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:21:03 2018

@author: TAL-LAPTOP
"""
import os
import re

NON_NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Reddit/"

class RedditUserInfoCollector:    
    
    def __init__(self, p_input_dir, p_output_file):
        self.input_dir = p_input_dir
        self.output_file = p_output_file
        
    def collect_info(self):
        print("input_dir" + self.input_dir)
        for root, dirs, files in os.walk(self.input_dir):
            for file in files:
                if not file.startswith("reddit."):
                    continue                      
                country_name= file.replace("reddit.","")
                country_name = country_name[0:country_name.find(".")]
                print("Processing {}".format(country_name))
    #            if country_name != "NewZealand" and country_name!="Canada":
    #                continue;
    #        user_to_number_of_tokens_dict = {}
    #        user_to_number_of_sentences_dict = {}            
#            with open(self.input_dir + file, 'r', encoding='utf-8', errors='ignore') as country_file:             
#                for line in country_file:
                    # user_name apears in the begining of every row inside []
    #                user_name = get_user_name_from_line(line)     
    #                # remove meta-data and extra characters
    #                line = remove_subreeddit_and_user_name_from_line(line)                
    #                line = clean_line(line)                    
    #                number_of_tokens = len(line.split())                   
    #                if user_name in user_to_number_of_tokens_dict.keys():
    #                    user_to_number_of_sentences_dict[user_name] += 1
    #                    user_to_number_of_tokens_dict[user_name] += number_of_tokens                   
    #                else:                        
    #                    user_to_number_of_sentences_dict[user_name] = 1
    #                    user_to_number_of_tokens_dict[user_name] = number_of_tokens
    #            print("Done processing {}, writing 100 longest contet users".format(country_name))
    #            counter = 0
    #            for user in sorted(user_to_number_of_tokens_dict, key=user_to_number_of_tokens_dict.get, reverse=True)[:number_of_top_users_per_country]:                        
    #                counter += 1
    #                output.write(country_name+ "," + str(counter) + ", "+ user + ', {}, {}\n'.format(user_to_number_of_sentences_dict[user], user_to_number_of_tokens_dict[user]))                    
    #                users_to_size_dict[user, country_name] = user_to_number_of_tokens_dict[user]

        
    def clean_line(line):
        strip_special_chars = re.compile("[^A-Za-z0-9 ',.]+")
        line = line.replace("<br />", " ")
        return re.sub(strip_special_chars, "", line)

    def get_user_name_from_line(line):
        return line[line.find('[')+1:line.find(']')]
    
    def remove_subreeddit_and_user_name_from_line(line):    
        l_line = line[line.find(']')+1:]
        l_line = l_line[l_line.find(']')+1:]
        return l_line
    
   
    
    def dump_to_file(self):
      with open(self.output_file,"a", encoding="utf-8") as output:   
          output.write('Country, position_in_country, UserName, sentences#, tokens#\n')
      return

    
    
    
    



    
def Main():
    reddit_user_info_collector = RedditUserInfoCollector(NON_NATIVE_INPUT_DIR, "out.txt")
    print(reddit_user_info_collector.input_dir)
    reddit_user_info_collector.collect_info()
    return
    
if __name__ == '__main__':
    Main()
        
        
        