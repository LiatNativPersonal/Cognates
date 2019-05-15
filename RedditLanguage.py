# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 09:37:11 2018

@author: TAL-LAPTOP
"""

class RedditLanguage:

    def __init__(self, p_language):
        self.country_name = p_language
        self.native_engslish = False
        self.file = ""
    
    def __eq__(self, other):
      return self.country_name == other.country_name
  
    def __str__(self):
        return str(self.country_name)
    
    def __hash__(self):
        return hash(self.country_name)