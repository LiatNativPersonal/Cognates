# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:16:43 2018

@author: TAL-LAPTOP
"""
import os
import re

NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.Native/"
NON_NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.nonNative/"

def collectUserStatistics():
    
    return

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

def collectStatistics():
    countries_to_users_dict = {}
    for file in (os.listdir(NATIVE_INPUT_DIR)):
        
        country_name= (file[len("reddit."):file.find(".txt")])
        if country_name != "NewZealand" :
            continue;
        countries_to_users_dict[country_name] = {}
        with open(NATIVE_INPUT_DIR + file, 'r', encoding='utf-8', errors='ignore') as country_file:
            for line in country_file:
                user_name = get_user_name_from_line(line)
                line = remove_subreeddit_and_user_name_from_line(line)                
                line = clean_line(line)
                if user_name in countries_to_users_dict[country_name].keys():
                    countries_to_users_dict[country_name][user_name] += len(line.split())
                    if user_name == 'zedok12':
                        print (str(line.split()) + ' ' + str(len(line.split())) +  '\n' )
                else:
                    countries_to_users_dict[country_name][user_name] = len(line.split())
#                    if user_name == 'zedok12':
#                        print (str(line.split()) + '\n')
#        country = file.substring(len("reddit."), file.find()
        print(countries_to_users_dict)
    return


if __name__ == '__main__':
    print("Entering function __main__")
    collectStatistics()
    print("Leaving function __main__")
