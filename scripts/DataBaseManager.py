# -*- coding: utf-8 -*-
"""
Created on Tue May 28 07:59:37 2019

@author: liatn
"""

GERMANIC_USER_DB = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/germanic_users_db.csv"
ROMANCE_USERE_DB = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/romance_users_db.csv"
NATIVE_USERE_DB = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/native_users_db.csv"
IMAGES_LIB = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Images/"
ROMANCE_IMAGES_LIB = IMAGES_LIB + "RomanceUsers/"
GERMANIC_IMAGES_LIB = IMAGES_LIB + "GermanicUsers/"
USEFUL_MEASURES = {"MLS":"MLS","C/S":"C-S","DC/C":"DC-C","T/S":"T-S","CT/T":"CT-T"," TTR":"TTR"}
VALID_SYNSETS = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/valid_synsets.csv"
GER_DIFF = "_ger_diff"
ORIGIN = "origin"
COLOR = "color"
GER_COLOR = "Blue"
ROM_COLOR = "Red"



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns


class DataBaseManager:

    def __init__(self, germanic_user_file, romance_user_file, native_user_file, valid_synsets_file):
        self.read_db(germanic_user_file, romance_user_file, native_user_file)        
        self.create_synset_to_native_threshold_dict(valid_synsets_file)
        self.add_germanic_diff_col()

    def read_db(self,germanic_user_file, romance_user_file, native_user_file):
        self.germanic_db = pd.read_csv(germanic_user_file)
        self.romance_db = pd.read_csv(romance_user_file)
        self.native_db = pd.read_csv(native_user_file)
#        self.non_native_db = self.germanic_db.append(self.romance_db)
    
    def create_synset_to_native_threshold_dict(self, valid_synsets_file):
        self.valid_synsets_to_threshold = {}
        with open(valid_synsets_file, 'r', encoding='utf-8', errors = 'ignore') as synsets_file:
            for synset in synsets_file:  
                
                germanic_norm_count_col_name = synset.rstrip() + "_g"
                romance_norm_count_col_name = synset.rstrip() + "_r"
                germanic_sum = 0
                romance_sum = 0
                data = self.native_db.loc[:,[germanic_norm_count_col_name, romance_norm_count_col_name]]
                counts_no_zeros = []
                for index, row in data.iterrows():
                    ########## trying to figure out if romance words means higher English
                    germanic_sum += row[germanic_norm_count_col_name]
                    romance_sum += row[romance_norm_count_col_name]
                    ##########################################################
                    counts_no_zeros.append(row[germanic_norm_count_col_name])
#                    if row[germanic_norm_count_col_name] + row[romance_norm_count_col_name] > 0:
#                        counts_no_zeros.append(row[germanic_norm_count_col_name])
                    
                if (len(counts_no_zeros) > 0):    
                    self.valid_synsets_to_threshold[int(synset)] = np.mean(counts_no_zeros)
                else:
                    self.valid_synsets_to_threshold[int(synset)] = 0
#            print(self.valid_synsets_to_threshold)
    
    def add_germanic_diff_col(self):
        for synset, threshold in self.valid_synsets_to_threshold.items():
            col_name = str(synset) + "_g"
            self.germanic_db[str(synset) + GER_DIFF] = self.germanic_db[col_name] - threshold
            self.romance_db[str(synset) + GER_DIFF] = self.romance_db[col_name] - threshold
            
#        print(self.non_native_db.columns)
        
        
    def generate_scatter_plot(self,english_proficency_measure, synset_number, number_of_data_points):
        germanic_for_plot = (self.germanic_db.sort_values(by=[english_proficency_measure]).loc[:,['username', english_proficency_measure, synset_number+GER_DIFF, ORIGIN, COLOR]])
        romance_for_plot = (self.romance_db.sort_values(by=[english_proficency_measure]).loc[:,['username', english_proficency_measure, synset_number+GER_DIFF, ORIGIN, COLOR]])
        #Aggregating values for plot
        germanic_chunks = np.array_split(germanic_for_plot, number_of_data_points)
        germanic_agg_values = []
        for ger_chunk in germanic_chunks:
            germanic_agg_values.append([np.mean(ger_chunk[english_proficency_measure]),np.mean(ger_chunk[synset_number+GER_DIFF]),GER_COLOR])
        
        romance_chunks = np.array_split(romance_for_plot, number_of_data_points)
        romance_agg_values = []
        for rom_chunk in romance_chunks:
            romance_agg_values.append([np.mean(rom_chunk[english_proficency_measure]),np.mean(rom_chunk[synset_number+GER_DIFF]),ROM_COLOR])
        
        plot_df = pd.DataFrame(germanic_agg_values+ romance_agg_values, columns= [english_proficency_measure, synset_number+GER_DIFF, COLOR])
        colors = np.array(plot_df[COLOR])
        plot_df.plot.scatter(x=english_proficency_measure, y=synset_number+GER_DIFF, grid=True,  title="Synset" + synset_number + " -" + english_proficency_measure, c=colors)
        plt.savefig(IMAGES_LIB + synset_number + " -DC-C"  +".png")
        
        
    def draw_lollipop_plot(self, english_proficency_measure, position, row, lib, username ):
        x = np.array(list(self.valid_synsets_to_threshold.keys()))
        y = -np.sort(-np.array(row),axis=0)
        
#        print(x)
#        print(len(y))
        lol = []
        for value in y:
            try:
                if value >=0 :
                    lol.append('orange')
                else:
                    lol.append('skyblue')
            except:
                continue
        lolli_color = np.array(lol)
        plt.vlines(x=x, ymin=0, ymax=y, color=lolli_color, alpha=0.4)
        plt.ylim(-1, 1)
        plt.scatter(x, y, color=lolli_color,  s=1, alpha=1)
        
        plt.savefig(lib + english_proficency_measure + "--"+str(position)+ "_" +username +"--" +".png")
        plt.cla()
        
    






def Main():
    db_mgr = DataBaseManager(GERMANIC_USER_DB, ROMANCE_USERE_DB, NATIVE_USERE_DB, VALID_SYNSETS)
    
    #for synset in db_mgr.valid_synsets_to_threshold.keys():
     #   db_mgr.generate_scatter_plot("DC/C", str(synset), 25)
#    print(len(db_mgr.non_native_db))
#    print(db_mgr.germanic_db)
    
    #LOLLIPOP GRAPH
#    for measure, print_measure in USEFUL_MEASURES.items():
#        print("Processing {}".format(print_measure))
#        data_for_analysis = (db_mgr.romance_db.sort_values(by=[measure]).loc[:,['username', 'country', measure]])
#        for synset in db_mgr.valid_synsets_to_threshold.keys():         
#            sysnset_num = str(synset)       
#            data_for_analysis[sysnset_num+GER_DIFF] = db_mgr.romance_db[sysnset_num+GER_DIFF]
#        position = 1
#        for index, row in data_for_analysis.iterrows():
#            db_mgr.draw_lollipop_plot(print_measure, position, pd.DataFrame(row[3::]),ROMANCE_IMAGES_LIB, row['username'])
#            position += 1
        
        
    user_vector = db_mgr.romance_db.loc[:,["username","MLS","C/S","DC/C","T/S","CT/T"," TTR"]]
    positive_distance = []
    negative_distance = []
    all_distance = []
    germanic_romance_ratio = []
    for index,row in db_mgr.romance_db.iterrows():
        pos_germanic_diff_sum = 0
        neg_germanic_diff_sum = 0
        all_germanic_diff_sum = 0
        for synset in db_mgr.valid_synsets_to_threshold.keys():
            col_name = str(synset) + GER_DIFF
            val = row[col_name]
            if val >= 0:
                pos_germanic_diff_sum += val
            else:
                neg_germanic_diff_sum += abs(val)
            all_germanic_diff_sum += abs(val)
        positive_distance.append(pos_germanic_diff_sum)
        negative_distance.append(neg_germanic_diff_sum)
        all_distance.append(all_germanic_diff_sum)
        germanic_romance_ratio.append(pos_germanic_diff_sum/neg_germanic_diff_sum)
    user_vector['POS_DIST_SUM'] = positive_distance
    user_vector['NEG_DIST_SUM'] = negative_distance
    user_vector['JOINED_DIST_SUM'] = all_distance
    user_vector['GERMANIC_ROMANCE_RATIO'] = germanic_romance_ratio
    for measure, print_measure in USEFUL_MEASURES.items():
        print("Processing {}".format(print_measure))     
        user_vector.plot.scatter(x=measure , y="GERMANIC_ROMANCE_RATIO", grid=True )
        plt.savefig(IMAGES_LIB + print_measure + "_Romance_users_overuse_ratio"+".png")
#    print(user_vector.head())
     

#    (data_for_analysis).to_csv(r'test.csv', index=None, header="True")
    

if __name__ == '__main__':
    Main()