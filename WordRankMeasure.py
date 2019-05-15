# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:28:42 2018

@author: TAL-LAPTOP
"""
#import math
#import numpy as np
from nltk.corpus import wordnet as wn

class WordRankMeasureCalculator:
    rank_dictionary = {}
    vocabname = "c:/Users/liatn/Documents/Liat/Research/Cognates/English proficiency measures/vocab.txt"
    word_count_file = "c:/Users/liatn/Documents/Liat/Research/Cognates/google_1grams/1gms/vocab_cs"
    def __init__(self):
        self.avg_rank = 0
        self.log_avg_rank = 0
        WordRankMeasureCalculator.create_rank_dict()
    
    @staticmethod    
    def create_rank_dict():
#        word_count_dictionry = {}
#        with open(WordRankMeasureCalculator.word_count_file, "r", encoding="utf-8") as word_count:            
#            for line in word_count:
#                (word, count) = line.split("\t")
#                word_count_dictionry[word] = int(count)
#        i = 1
#        for w in sorted(word_count_dictionry, key=word_count_dictionry.get, reverse=True):
#            WordRankMeasureCalculator.rank_dictionary[w]=i
#            i += 1
        with open(WordRankMeasureCalculator.vocabname, 'r', encoding = "utf-8", errors="ignore") as fin:
            i = 0
            for line in fin.readlines():
                if len(line.strip().split()) < 2: continue
                token = line.strip().split()[1]
                token_synsets = wn.synsets(token) # first token synset
                if len(token_synsets) == 0 or not token.isalpha(): continue
                if token in WordRankMeasureCalculator.rank_dictionary.keys(): continue
                WordRankMeasureCalculator.rank_dictionary[token.lower()] = i
                i += 1
            
    def calculate_rank_measure(self, text):
#       words = text.split()
#       relevant_words = [word for word in text if word in  WordRankMeasureCalculator.rank_dictionary.keys()]
#       ranks = [WordRankMeasureCalculator.rank_dictionary[x] for x in relevant_words]
#       log_ranks = [math.log(rank) for rank in ranks]
#       self.avg_rank = np.mean(ranks)
#       self.log_avg_rank = np.mean(log_ranks)
#       return [self.avg_rank, self.log_avg_rank]
        total_rank = 0
        total_log_ranks = 0
        total_tokens = 0        
        for token in text:
            if token in WordRankMeasureCalculator.rank_dictionary.keys():
                total_rank += WordRankMeasureCalculator.rank_dictionary[token]
#                total_log_ranks += math.log(float(WordRankMeasureCalculator.rank_dictionary[token]))
                total_tokens += 1
            # end if
        # end for
        return [float(total_rank) / total_tokens, float(total_log_ranks) / total_tokens]
 
#def Main():
#    
#      a = WordRankMeasureCalculator();
#      
#      for key, value in WordRankMeasureCalculator.rank_dictionary.items():
#          print("{} = {}".format(key,value))
#          if value > 15 :
#              break
#   
#if __name__ == '__main__':
#    Main()
    
        