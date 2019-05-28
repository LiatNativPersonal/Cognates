# -*- coding: utf-8 -*-
"""
Created on Tue May 28 07:59:37 2019

@author: liatn
"""

GERMANIC_USER_DB = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/germanic_users_db.csv"
ROMANCE_USERE_DB = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/romance_users_db.csv"
NATIVE_USERE_DB = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/native_users_db.csv"
USEFUL_MEASURES = ["MLS","C/S","DC/C","T/S","CT/T","TTR"]

import numpy as np
import pandas as pd

class DataBaseManager:

    def __init__(self, germanic_user_file, romance_user_file, native_user_file):
        self.read_db(germanic_user_file, romance_user_file, native_user_file)

    def read_db(self,germanic_user_file, romance_user_file, native_user_file):
        self.germanic_db = pd.read_csv(germanic_user_file)
        self.romance_db = pd.read_csv(romance_user_file)
        self.native_db = pd.read_csv(native_user_file)
    
    
    






def Main():
    db_mgr = DataBaseManager(GERMANIC_USER_DB, ROMANCE_USERE_DB, NATIVE_USERE_DB)

if __name__ == '__main__':
    Main()