# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:28:42 2018

@author: TAL-LAPTOP
"""
import numpy as np
import csv

class NamingRTMeasureCalculator:
    naming_RT_dictionary = {}
    naming_RT_file = r"c:\Users\User\Documents\Liat\Research\Cognates\English proficiency measures\Naming_RT.csv"
    
    def __init__(self):
        self.avg_naming_RT = 0.0
        NamingRTMeasureCalculator.create_naming_RT_dict()
    
    @staticmethod    
    def create_naming_RT_dict():
        with open(NamingRTMeasureCalculator.naming_RT_file, "r", encoding="utf-8") as naming_RT:
            csvreader = csv.reader(naming_RT, delimiter=',')  
            next(csvreader, None)
            for line in csvreader:
                if len(line) != 6:
                    continue
                word = line[0]
                try:
                    mean_RT = float(line[1])
                except:
                    mean_RT = 0.0
                NamingRTMeasureCalculator.naming_RT_dictionary[word] = mean_RT        
            
    def calculate_naming_RT_measure(self, text):
#       words = text.split()
       relevant_words = [word for word in text if word in  NamingRTMeasureCalculator.naming_RT_dictionary.keys()]
       naming_RTs = [NamingRTMeasureCalculator.naming_RT_dictionary[x] for x in relevant_words if NamingRTMeasureCalculator.naming_RT_dictionary[x] > 0.0]
       self.avg_naming_RT = np.mean(naming_RTs) 
       return self.avg_naming_RT
       
            
            
    
        