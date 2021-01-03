# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:00:00 2020

@author: liatn
"""

REDDIT_GERMANIC_COUNTS_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/germanic_users_synsets_germanic_count.csv"
REDDIT_ROMANCE_COUNTS_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/romance_users_synsets_germanic_count.csv"
REDDIT_NATIVE_COUNTS_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/native_users_synsets_germanic_count.csv"
GERMANIC_GERMANIC_RATIO_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/germanic_users_synsets_germanic_ratio.csv"
ROMANCE_GERMANIC_RATIO_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/romance_users_synsets_germanic_ratio.csv"
NATIVE_GERMANIC_RATIO_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/native_users_synsets_germanic_ratio.csv"
GERMANIC_GERMANIC_RATIO_DIST_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/germanic_users_synsets_germanic_ratio_dist_from_native.csv"
ROMANCE_GERMANIC_RATIO_DIST_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/romance_users_synsets_germanic_ratio_dist_from_native.csv"
GERMANIC_GERMANIC_COUNT_DIST_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/germanic_users_synsets_germanic_count_distance_from_native.csv"
ROMANCE_GERMANIC_COUNT_DIST_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/romance_users_synsets_germanic_count_distance_from_native.csv"
OUPUT_FILE = "GermanicVsRomanceGermanicCountDistancePerSynsetStatAnalysis.csv"
import csv
from scipy import stats



def createSynsetToValue(file_name):
    synset_to_value_dict = {}    
    with open(file_name,'r') as UsersFile:        
        reader = csv.reader(UsersFile, delimiter=',')  
        header = next(reader)
        for synset in header:
            try:
                synset_to_value_dict[int(synset)] = []
            except:
                continue
        for line in reader:
            for value in range(1,len(line)-1):
                synset_to_value_dict[value].append(float(line[value]))
    return synset_to_value_dict
        


def test_statistical_significance(dict1, dict2):
    with open(OUPUT_FILE, "w", encoding="utf-8") as output_file:      
        output_file.write("synset,stat,p value\n")
        for synset in dict1.keys():           
            [ttestMeasuerStatistics, ttestMeasurePvalue] =stats.ttest_ind(dict1[synset],dict2[synset])
            output_file.write("{}, ".format(synset))
            output_file.write(str(ttestMeasuerStatistics) + ",")
            output_file.write(str(ttestMeasurePvalue)+ "\n" )
            
            
def Main():  
    germanic_users_synset_to_value = createSynsetToValue(REDDIT_GERMANIC_COUNTS_FILE)
    romance_users_synset_to_value = createSynsetToValue(REDDIT_ROMANCE_COUNTS_FILE)
    native_users_synset_to_value = createSynsetToValue(REDDIT_NATIVE_COUNTS_FILE)
    test_statistical_significance(germanic_users_synset_to_value,romance_users_synset_to_value)
    
    
if __name__ == '__main__':
    Main()
            
