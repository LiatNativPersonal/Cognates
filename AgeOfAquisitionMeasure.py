# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:28:42 2018

@author: TAL-LAPTOP
"""
import numpy as np
import openpyxl as px


class AgeOfAquisitionMeasureCalculator:
    AOA_dict = {}
    AOA_file = "c:/Users/liatn/Documents/Liat/Research/Cognates/English proficiency measures/AoA_ratings_Kuperman_et_al_BRM.xlsx"
    
    def __init__(self):
        self.avg_AOA = 0.0
        AgeOfAquisitionMeasureCalculator.create_AOA_dict()
    
    @staticmethod    
    def create_AOA_dict():
        TOTAL_WORDS = 31125        
        wb = px.load_workbook(AgeOfAquisitionMeasureCalculator.AOA_file) 
        # load the excel file
        ws = wb['AoA-data']
        count = 0
        for row in ws.iter_rows():
            if count == TOTAL_WORDS: break
            word = row[0].value.strip().lower()
            if row[4].value == "NA" or row[4].value == "Rating.Mean":
                count += 1
                continue
            AgeOfAquisitionMeasureCalculator.AOA_dict[word] = float(row[4].value) # word and its rating.mean
            count += 1
                
    def calculate_age_of_aquisition_measure(self, text):
       relevant_words = [word for word in text if word in  AgeOfAquisitionMeasureCalculator.AOA_dict.keys()]
       AOAs = [AgeOfAquisitionMeasureCalculator.AOA_dict[x] for x in relevant_words]       
       self.avg_AOA = np.mean(AOAs) 
       return self.avg_AOA
       
            
            
    
        