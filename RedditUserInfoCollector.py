# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:21:03 2018

@author: TAL-LAPTOP
"""
import os
import re
from RedditUser import RedditUser

NON_NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Documents/Liat/Research/Reddit/"

class RedditUserInfoCollector:    
    
    def __init__(self, p_input_dir, p_output_file):
        self.input_dir = p_input_dir
        self.output_file = p_output_file
        self.users = {}
        
    def get_user_name_from_line(self, line):
        if line.startswith('['):
            return line[line.find('[')+1:line.find(']')]
        return line[0:line.find(',')]
    
    def remove_subreeddit_and_user_name_from_line(self,line):
        if line.startswith('['):
            l_line = line[line.find(']')+1:]
            l_line = l_line[l_line.find(']')+1:]
        else:    
            l_line = line[line.find(''):]
            l_line = l_line[l_line.find(''):]
        return l_line
    
    def clean_line(self,line):
        strip_special_chars = re.compile("[^A-Za-z0-9 ',.]+")
        line = line.replace("<br />", " ")
        return re.sub(strip_special_chars, "", line)
        
    def collect_info(self):
        print("input_dir" + self.input_dir)
        for root, dirs, files in os.walk(self.input_dir):            
            for file in files:
                if not file.startswith("reddit."):
                    continue                      
                country_name= file.replace("reddit.","")
                country_name = country_name[0:country_name.find(".")]
                
                file_path = os.path.join(root,file)
                print(file_path)
                print("Processing {}".format(country_name))
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as country_file:             
                    for line in country_file:                        
                    # user_name apears in the begining of every row inside []
                        user_name = self.get_user_name_from_line(line)
                        user = RedditUser(user_name, country_name)
                        if country_name not in self.users.keys():
                            self.users[country_name]={}
                        self.users[country_name][user_name] = user
    #                # remove meta-data and extra characters
                    line = self.remove_subreeddit_and_user_name_from_line(line)                
                    line = self.clean_line(line)                    
                    number_of_tokens = len(line.split())   
                    self.users[country_name][user_name].number_of_sentences += 1
                    self.users[country_name][user_name].number_of_tokens += number_of_tokens
        print(len(self.users))
    
        
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
        
        
        