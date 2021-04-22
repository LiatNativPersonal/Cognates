# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:28:42 2018

@author: TAL-LAPTOP
"""
from lexicalrichness import LexicalRichness

class LexicalRichnessCalculator:

    def __init__(self, text, window_size = 200, ttr_thrshold = 0.72):

        self.mattr = 0 # Moving average type-token ratio
        self.mtld = 0 # Measure of Textual Lexical Diversity
        self.text = text
        self.window_size = window_size
        self.ttr_thrshold = ttr_thrshold
        self.lex = LexicalRichness(text)
    

            
    def calculate_maatr(self):
        self.mattr =  self.lex.mattr(window_size=self.window_size)
        return self.mattr

    def calculate_mtld(self):
        self.mtld = self.lex.mtld(self.ttr_thrshold)
        return self.mtld
