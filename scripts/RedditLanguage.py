# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 09:37:11 2018

@author: TAL-LAPTOP
"""
from LanguageOrigin import LanguageOrigin

NATIVE_ENGLISH = ["US", "UK","Ireland","Australia", "NewZealand"]
GERMANIC_ORIGIN = ["Iceland","Sweden","Germany","Austria","Netherlands","Norway","Finland","Denmark"]
ROMANCE_ORIGIN = ["Romania","Portugal","Spain","Italy","France","Mexico","Argentina","Brazil","Venezuela","Sardinia","Andorra"]



class RedditLanguage:
   

    def __init__(self, p_language):
        self.country_name = p_language
        self.origin = LanguageOrigin.UNDEF
        self.file = ""
    
    def __eq__(self, other):
      return self.country_name == other.country_name
  
    def __str__(self):
        return str(self.country_name)
    
    def __hash__(self):
        return hash(self.country_name)
    
    def set_origin(self):
        if self.country_name in NATIVE_ENGLISH:
            self.origin = LanguageOrigin.NATIVE
        elif self.country_name in GERMANIC_ORIGIN:
            self.origin = LanguageOrigin.GERMANIC
        elif self.country_name in ROMANCE_ORIGIN:
            self.origin = LanguageOrigin.ROMANCE
        else:
            self.origin = LanguageOrigin.UNDEF