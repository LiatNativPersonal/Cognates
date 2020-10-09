   # -*- coding: utf-8 -*-
"""
Created on Sun May 19 15:09:56 2019

@author: liatn
"""
import csv

INPUT_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/scripts/native_extended_list_over_500_cog_200_synsets.csv"
OUTPUT_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/scripts/down_sampled_native_extended_list_over_500_cog_200_synsets.csv"
with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as input_file:
    with open(OUTPUT_FILE, 'w+', encoding='utf-8') as down_sample:
     reader = csv.reader(input_file, delimiter=',')
     header = next(reader, None)
     for col_name in header:
         down_sample.write("{},".format(col_name))
     down_sample.write("\n")
     i = 1
     lines = 0
     cognate_number_to_number_of_users = {}
     for line in reader:
         cognate_num = line[2]
         if cognate_num not in cognate_number_to_number_of_users.keys():
             cognate_number_to_number_of_users[cognate_num] = 0
         cognate_number_to_number_of_users[cognate_num] +=1
         if lines%4 == 0:
             lines +=1
             continue
         if cognate_number_to_number_of_users[cognate_num] <= 2 :
             for attr in line:
                 down_sample.write("{},".format(attr))
             down_sample.write("\n")
             lines += 1
         i += 1
             