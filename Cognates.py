# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:16:43 2018

@author: TAL-LAPTOP
"""
import os
import re

NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.Native/"
NON_NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.nonNative/"
NATIVE_OUTPUT_FILE = "NativeCountryTop100UserAmountOfContent.csv"
NON_NATIVE_OUTPUT_FILE = "NonNativeCountryTop100UserAmountOfContent.csv"

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
def collectStatistics(input_dir, output_file):
    print("Collecting statistics, results will be written to {}".format(output_file))    
    with open(output_file,"a", encoding="utf-8") as output:   
        output.write('Country, position_in_country, UserName, sentences#, tokens#\n')
        for file in (os.listdir(input_dir)):            
            country_name= (file[len("reddit."):file.find(".txt")])
            print("Processing {}".format(country_name))
#            if country_name != "NewZealand" and country_name!="Canada":
#                continue;
            user_to_number_of_tokens_dict = {}
            user_to_number_of_sentences_dict = {}            
            with open(input_dir + file, 'r', encoding='utf-8', errors='ignore') as country_file:             
                for line in country_file:
                    # user_name apears in the begining of every row inside []
                    user_name = get_user_name_from_line(line)     
                    # remove meta-data and extra characters
                    line = remove_subreeddit_and_user_name_from_line(line)                
                    line = clean_line(line)                    
                    number_of_tokens = len(line.split())                   
                    if user_name in user_to_number_of_tokens_dict.keys():
                        user_to_number_of_sentences_dict[user_name] += 1
                        user_to_number_of_tokens_dict[user_name] += number_of_tokens                   
                    else:                        
                        user_to_number_of_sentences_dict[user_name] = 1
                        user_to_number_of_tokens_dict[user_name] = number_of_tokens
                print("Done processing {}, writing 100 longest contet users".format(country_name))
                counter = 0
                for user in sorted(user_to_number_of_sentences_dict, key=user_to_number_of_sentences_dict.get, reverse=True):                        
                    counter += 1
                    output.write(country_name+ ", " + str(counter) + ", "+ user + ', {}, {}\n'.format(user_to_number_of_sentences_dict[user], user_to_number_of_tokens_dict[user]))
                    if (counter >= 100):
                        break
    


if __name__ == '__main__':
    print("Entering function __main__")
    print("++++++++++++ Native +++++++++++++")
    open(NATIVE_OUTPUT_FILE, 'w+').close()
    collectStatistics(NATIVE_INPUT_DIR, NATIVE_OUTPUT_FILE)
    print("++++++++++++ Non-native +++++++++++++")
    open(NON_NATIVE_OUTPUT_FILE, 'w+').close()
    collectStatistics(NON_NATIVE_INPUT_DIR, NON_NATIVE_OUTPUT_FILE)
    print("Leaving function __main__")
