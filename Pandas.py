# -*- coding: utf-8 -*-
"""
Created on Mon May  6 20:26:53 2019

@author: liatn
"""

import numpy as np
import pandas as pd

filename = "C:/Users/liatn/Documents/Liat/Research/Cognates/synset3NNforPandas.csv"
df = pd.read_csv(filename)
#print(df.head())
#print(df.tail(3))
#print(df.dtypes)
print(df.columns)
#print(df.index)
#print(df.describe())
#print(df.sort_values('TTR'))
print(len(df))
Germanic_users_df = df[df.origin.isin(["G"])]
Romance_users_df = df[df.origin.isin(["R"])]
print(len(Germanic_users_df))
print(len(Romance_users_df))
Germanic_by_TTR = (Germanic_users_df.sort_values(by=['TTR']).loc[:,['user', 'TTR', 'Germanic Diff', 'origin']])
Romance_by_TTR = (Romance_users_df.sort_values(by=['TTR']).loc[:,['user', 'TTR', 'Germanic Diff', 'origin']])
#print(len(Germanic_by_TTR))
#print(Germanic_by_TTR)
#Germanic_users_df.reindex([2])
#print(Germanic_users_df.loc[:,['user', 'TTR', 'Germanic Diff', 'origin']])
ger_chunks = np.array_split(Germanic_by_TTR, 20)
Ger_values = []
for chunk in ger_chunks:
    Ger_values.append([np.mean(chunk["TTR"]),np.mean(chunk["Germanic Diff"]),"Blue"])
rom_chunks = np.array_split(Romance_by_TTR,20)
Rom_values = []
for chunk in rom_chunks:
    Rom_values.append([np.mean(chunk["TTR"]),np.mean(chunk["Germanic Diff"]),"Red"])
mean_df = pd.DataFrame(Ger_values+Rom_values, columns = ["TTR", "Ger_Diff", "Origin"])
colors = np.array(mean_df['Origin'])
print(mean_df)
g1 = mean_df.plot.scatter(x='TTR', y='Ger_Diff', c=colors)    
