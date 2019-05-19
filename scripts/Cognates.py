# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:16:43 2018

@author: TAL-LAPTOP
"""
import os
import re
from nltk.stem.porter import PorterStemmer

NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.Native/"
NON_NATIVE_INPUT_DIR = "C:/Users/TAL-LAPTOP/Desktop/NLP Lab/rawData/reddit.nonNative/"
STAT_NATIVE_OUTPUT_FILE = "NativeCountryUserAmountOfContent.csv"
STAT_NON_NATIVE_OUTPUT_FILE = "NonNativeCountryTop100UserAmountOfContent.csv"
NON_NATIVE_LARGE_CONTENT_USER_DB = "c:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/NonNative/"
NATIVE_LARGE_CONTENT_USER_DB = "c:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/MassiveUsersDB/Native/"
COGNATES_FOCUS_SET = "c:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/synsets.mult.final.100.dat"
NON_NATIVE_COGNATES_COUNT_PER_USER = "c:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/non-native_cognates_count_per_user.csv"
NATIVE_COGNATES_COUNT_PER_USER = "c:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/native_cognates_count_per_user.csv"


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
                for user in sorted(user_to_number_of_tokens_dict, key=user_to_number_of_tokens_dict.get, reverse=True)[:number_of_top_users_per_country]:                        
                    counter += 1
                    output.write(country_name+ "," + str(counter) + ", "+ user + ', {}, {}\n'.format(user_to_number_of_sentences_dict[user], user_to_number_of_tokens_dict[user]))                    
                    users_to_size_dict[user, country_name] = user_to_number_of_tokens_dict[user]
    return users_to_size_dict


def create_large_content_user_dataset(tokens_lower_bound, users_to_num_tokens_file, input_dir, user_db):          
    with open(users_to_num_tokens_file, 'r') as users_to_num_tokens:
        i = 0
        for line in users_to_num_tokens:
            if i == 0:
                i += 1
                continue
            (country, rank, user, num_sentences, num_tokens) = line.split(",")  
            user = user.strip()            
            if int(num_tokens) >= tokens_lower_bound:
                with open(user_db + "reddit." + user + "." + country +".txt", "w+") as user_output_file:
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
    return cognates_dict

def print_dict(dict):
    for key,value in dict.items():
        print(str(key) + ": " + str(value))

def count_cognates(massive_users_dir, output_file):
    users_cognates_count = {}
    cognates_count_dict = create_cognates_dict()
    porter_stemmer = PorterStemmer()    
    for user_file in os.listdir(massive_users_dir):
        user_country = user_file.replace("reddit.", "")
        user_country = user_country.replace(".txt", "")
        with open(massive_users_dir+user_file, "r", encoding="utf-8") as user_text:
            print("processing file {}".format(user_file))
            #clear dictioanry
            cognates_count_dict = cognates_count_dict.fromkeys(cognates_count_dict,0)
            for line in user_text:
                for word in line.split():
                    basic_word = porter_stemmer.stem(word)
                    if basic_word in cognates_count_dict.keys():
                        cognates_count_dict[basic_word] += 1
            
            users_cognates_count[user_country] = cognates_count_dict            
    #print_dict(users_cognates_count)
    print_output(users_cognates_count, output_file)        
    return
            
def print_output(users_to_cognates_dict, output_file):
    heading = True
    with open(output_file, "w+") as cognates_count_out:
        cognates_count_out.write(" ,")
        for user,cognate_count in users_to_cognates_dict.items():
            if heading:
                for cognate in cognate_count.keys():
                    cognates_count_out.write(cognate + ",")                    
                cognates_count_out.write("\n")
                heading = False
            cognates_count_out.write(user )
            for count in cognate_count.values():
                cognates_count_out.write("," + str(count))
            cognates_count_out.write("\n")
                
            

def Main():    
    print("Entering function __main__")
    print("++++++++++++ Native +++++++++++++")
#    open(STAT_NATIVE_OUTPUT_FILE, 'w+').close()
#    native_users_to_tokens_num_dict = collect_statistics_(NATIVE_INPUT_DIR, STAT_NATIVE_OUTPUT_FILE, 10000)
#    print("++++++++++++ Non-native +++++++++++++")
#    open(STAT_NON_NATIVE_OUTPUT_FILE, 'w+').close()
#    nonnative_users_to_tokens_num_dict =collect_statistics_(NON_NATIVE_INPUT_DIR, STAT_NON_NATIVE_OUTPUT_FILE,100)
    
    #create_large_content_user_dataset(1000000, STAT_NON_NATIVE_OUTPUT_FILE, NON_NATIVE_INPUT_DIR, NON_NATIVE_LARGE_CONTENT_USER_DB)
#    create_large_content_user_dataset(1000000, STAT_NATIVE_OUTPUT_FILE, NATIVE_INPUT_DIR, NATIVE_LARGE_CONTENT_USER_DB)
    count_cognates(NATIVE_LARGE_CONTENT_USER_DB, NATIVE_COGNATES_COUNT_PER_USER)
    print("Leaving function __main__")

    

if __name__ == '__main__':
    Main()