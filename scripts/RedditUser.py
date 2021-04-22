# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:32:52 2018

@author: TAL-LAPTOP
"""


import nltk
from pathlib import Path
import random
from WordRankMeasure import WordRankMeasureCalculator
from NamingRTMeasure import NamingRTMeasureCalculator
from AgeOfAquisitionMeasure import AgeOfAquisitionMeasureCalculator
from LexicalRichnessCalculator import LexicalRichnessCalculator

class RedditUser:

    word_rank_measure_calculator = WordRankMeasureCalculator()
    naming_RT_measure_calculator = NamingRTMeasureCalculator()
    aoa_measure_calculator = AgeOfAquisitionMeasureCalculator()
    lexical_richness_calculator = LexicalRichnessCalculator()
    def __init__(self, p_name, p_l1, text_file=""):
        self.user_name = p_name
        self.l1 = p_l1
        self.number_of_tokens = 0
        self.number_of_sentences = 0
        self.text = []
        self.text_file = text_file
        self.type_token_ratio = 0.0
        self.avg_word_rank = 0.0
        self.avg_log_word_rank = 0.0
        self.avg_naming_RT = 0.0
        self.avg_age_of_aquisition = 0.0
        self.lexical_richness_measures = {}
        self.sample_size = 0
        self.totalCognateCount = 0
        self.totalSynsetUsed = 0

    
    def set_amount_of_text(self, p_num_of_tokens, p_num_of_sentences):
        self.number_of_tokens = p_num_of_tokens
        self.number_of_sentences = p_num_of_sentences
        
    def dump__text_to_file(self, file_path):
        self.text_file = file_path
        print (self.text_file)
        with open(file_path, 'w+', encoding='utf-8') as user_output_file:
            for line in self.text:
                user_output_file.write(line)
                
    def set_user_text_sample(self):        
        words = []
        print("from file: {}".format(self.text_file))
        if len(self.text) > 0:
            words = nltk.word_tokenize(self.text) 
            print("in memory")
        elif Path(self.text_file).is_file():
            
            with open(self.text_file, "r", encoding= "utf-8") as text:
                words = nltk.word_tokenize(text.read())
        if len(words) == 0 :
            print("no words")
            self.type_token_ratio = 0.0
            return
        
                        
        # Lowercase all words (default_stopwords are lowercase too)
        words = [word.lower() for word in words]
        if len(words) <= self.sample_size:
            self.text = words
        else:
            self.text = random.sample(words,self.sample_size)
                
    def calculate_type_token_ratio(self): 
#        self.set_user_text_sample()
        content_tokens = [token for token in self.text if token in RedditUser.word_rank_measure_calculator.rank_dictionary.keys()]
        self.type_token_ratio = len(set(content_tokens)) / len(content_tokens)

    def calculate_lexical_richness_measures(self):
        self.lexical_richness_measures = self.lexical_richness_calculator.calculate_lexical_richness_measure(text)

        
    def calculate_word_rank_measure(self):
#        self.set_user_text_sample()
        [self.avg_word_rank, self. avg_log_word_rank] = RedditUser.word_rank_measure_calculator.calculate_rank_measure(self.text)
        
    def calculate_naming_RT_measure(self):
#        self.set_user_text_sample()
        self.avg_naming_RT = RedditUser.naming_RT_measure_calculator.calculate_naming_RT_measure(self.text)
        
    def calculate_AOA_measure(self):
        self.avg_age_of_aquisition = RedditUser.aoa_measure_calculator.calculate_age_of_aquisition_measure(self.text)
        
        
    
#    def __eq__(self, other):
#      return (self.user_name == other.user_name and self.l1 == other.l1)
#  
#    def __str__(self):
#        return str(self.user_name)
#    
#    def __hash__(self):
#        return hash(self.user_name)
                
    
    