# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:32:52 2018

@author: TAL-LAPTOP
"""



class RedditUser:

    
    
    def __init__(self, p_name, p_l1):
        self.user_name = p_name
        self.l1 = p_l1
        self.number_of_tokens = 0
        self.number_of_sentences = 0
        self.text = []
    
    @classmethod
    def set_amount_of_test(self, p_num_of_tokens, p_num_of_sentences):
        self.number_of_tokens = p_num_of_tokens
        self.number_of_sentences = p_num_of_sentences
    
    