   # -*- coding: utf-8 -*-
"""
Created on Sun May 19 15:09:56 2019

@author: liatn
"""
import csv

INPUT_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/1.5.2019_native_over_300_sent_analyzed.csv"
OUTPUT_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/down_sample_19.5.2019_natives_over_300_sent_non_native_analyzed.csv"
with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as input_file:
    with open(OUTPUT_FILE, 'w+', encoding='utf-8') as down_sample:
     reader = csv.reader(input_file, delimiter=',')
     header = next(reader, None)
     for col_name in header:
         down_sample.write("{},".format(col_name))
     down_sample.write("\n")
     i = 1
     lines = 0
     for line in reader:
         if i % 2 == 0 and lines < 960:
             for attr in line:
                 down_sample.write("{},".format(attr))
             down_sample.write("\n")
             lines += 1
         i += 1
             