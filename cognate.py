# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 13:23:41 2018

@author: TAL-LAPTOP
"""

class Cognate:
    cognate_to_language_family_dict = {}
    def __init__(self, content):
        self.content = content
        self.language_family = ""
    
    @staticmethod
    def init_cognate_to_language_family_dict(cognate_to_family_file):
        with open(cognate_to_family_file, "r", encoding="utf-8") as input_file:
            for line in input_file:
                (word, family) = line.split(",")
                Cognate.cognate_to_language_family_dict[word] = family
    
    def setLanguageFamily(self):
        self.language_family = Cognate.cognate_to_language_family_dict[self.content]
        
    