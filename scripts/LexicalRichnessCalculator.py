# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:28:42 2018

@author: TAL-LAPTOP
"""
from lexicalrichness import LexicalRichness

class LexicalRichnessCalculator:

    def __init__(self):

        self.measures = {}
        self.lex = LexicalRichness("")
    

            
    def calculate_lexical_richness_measure(self, text, window_size = 200, threshold = 0.72):
        lex = LexicalRichness(text)
        self.measures['mattr'] = lex.mattr(window_size=window_size) #moving average
        self.measures['mtld'] = lex.mtld(threshold=threshold) #measure of lexical diversity
        return self.measures
