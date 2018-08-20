# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:16:43 2018

@author: TAL-LAPTOP
"""
import os
import re

NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.Native/"
NON_NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.nonNative/"
OUTPUT_FILE = "UserAmountOfContent.csv"

def printStatistics(stat_dict):    
    for country,users_dict in stat_dict.items():
        with open(country+OUTPUT_FILE,"w+", encoding="utf-8") as output:            
            for user,counts in users_dict.items():            
                output.write("'" + user + "', " + str(counts[0]) + " ," + str(counts[1]) + "\n")           
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

#Construct a dictionary that maps each country to its users, 
#and for each user holds the amount of tokens and sentences
def collectStatistics():
    countries_to_users_dict = {}
    for file in (os.listdir(NATIVE_INPUT_DIR)):
        
        country_name= (file[len("reddit."):file.find(".txt")])
        if country_name != "NewZealand" :
            continue;
        countries_to_users_dict[country_name] = {}
        with open(NATIVE_INPUT_DIR + file, 'r', encoding='utf-8', errors='ignore') as country_file:
            for line in country_file:
                # user_name apears in the begining of every row inside []
                user_name = get_user_name_from_line(line)     
                # remove meta-data and extra characters
                line = remove_subreeddit_and_user_name_from_line(line)                
                line = clean_line(line)
                
                number_of_tokens = len(line.split())
                if user_name in countries_to_users_dict[country_name].keys():
                    countries_to_users_dict[country_name][user_name][0] += 1
                    countries_to_users_dict[country_name][user_name][1] += number_of_tokens                   
                else:
                    count_user_text = [1, number_of_tokens]
                    countries_to_users_dict[country_name][user_name] = count_user_text
    return countries_to_users_dict


if __name__ == '__main__':
    print("Entering function __main__")
    stat_dict = collectStatistics()
    printStatistics(stat_dict)
    print("Leaving function __main__")
