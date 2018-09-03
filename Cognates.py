# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:16:43 2018

@author: TAL-LAPTOP
"""
import os
import re

NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.Native/"
NON_NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.nonNative/"
STAT_NATIVE_OUTPUT_FILE = "NativeCountryTop100UserAmountOfContent.csv"
STAT_NON_NATIVE_OUTPUT_FILE = "NonNativeCountryTop100UserAmountOfContent.csv"
NATIVE_LARGE_CONTENT_USER_DB = "NativeLargeContentUserDB.txt"
NON_NATIVE_LARGE_CONTENT_USER_DB = "NonNativeLargeContentUserDB.txt"
COGNATES_FOCUS_SET = "c:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/synsets.mult.final.100.dat"

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
def collect_statistics_(input_dir, output_file, number_of_top_users_per_country):
    print("Collecting statistics, results will be written to {}".format(output_file))   
    users_to_size_dict={}
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
                for user in sorted(user_to_number_of_sentences_dict, key=user_to_number_of_sentences_dict.get, reverse=True)[:number_of_top_users_per_country]:                        
                    counter += 1
                    output.write(country_name+ "," + str(counter) + ", "+ user + ', {}, {}\n'.format(user_to_number_of_sentences_dict[user], user_to_number_of_tokens_dict[user]))                    
                    users_to_size_dict[user, country_name] = user_to_number_of_tokens_dict[user]
    return users_to_size_dict


def create_large_content_user_dataset(tokens_lower_bound, users_to_num_tokens_file, input_dir):          
    with open(users_to_num_tokens_file, 'r') as users_to_num_tokens:
        i = 0
        for line in users_to_num_tokens:
            if i == 0:
                i += 1
                continue
            (country, rank, user, num_sentences, num_tokens) = line.split(",")  
            user = user.strip()            
            if int(num_tokens) >= tokens_lower_bound:
                with open('MassiveUsersDB/reddit.' + user + "." + country +".txt", "w+") as user_output_file:
                    with open (input_dir + "reddit." + country + ".txt.tok.clean", "r", encoding="utf-8") as user_country_file:
                        for user_line in user_country_file:
                            
                            if get_user_name_from_line(user_line) == user:
                                user_line = remove_subreeddit_and_user_name_from_line(user_line)
                                user_line = clean_line(user_line)
                                user_output_file.write(user_line + '\n')      
def create_cognates_dict():
    cognates_dict = {}
    with open(COGNATES_FOCUS_SET, "r", encoding="utf-8") as cognates_file:
        for line in cognates_file:
            for cognate in line.split():
                cognates_dict[cognate] = 0                
    print("cognates count {}".format(cognates_dict.keys()))
    return cognates_dict

def count_cognates(massive_users_dir):
    cognates_count_dict = create_cognates_dict()



def Main():    
    print("Entering function __main__")
    #print("++++++++++++ Native +++++++++++++")
#    open(STAT_NATIVE_OUTPUT_FILE, 'w+').close()
#    native_users_to_tokens_num_dict = collect_statistics_(NATIVE_INPUT_DIR, STAT_NATIVE_OUTPUT_FILE, 100)
#    print("++++++++++++ Non-native +++++++++++++")
#    open(STAT_NON_NATIVE_OUTPUT_FILE, 'w+').close()
#    nonnative_users_to_tokens_num_dict =collect_statistics_(NON_NATIVE_INPUT_DIR, STAT_NON_NATIVE_OUTPUT_FILE,100)
    
    #create_large_content_user_dataset(1000000, STAT_NON_NATIVE_OUTPUT_FILE, NON_NATIVE_INPUT_DIR)
    count_cognates("MassiveUsersDB")
    print("Leaving function __main__")

    

if __name__ == '__main__':
    Main()