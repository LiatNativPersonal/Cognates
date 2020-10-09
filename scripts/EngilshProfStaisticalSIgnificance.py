# -*- coding: utf-8 -*-
"""
Created on Tue Jan  1 13:44:51 2019

@author: TAL-LAPTOP
"""
from scipy import stats
import csv

NATIVE_ENG_PROF_RESULTS_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/native_users_lex_prof_measurs.csv"
#NON_NATIVE_ENG_PROF_RESULTS_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/19.5.2019_478_romance_non_native_analyzed.csv"
#NON_NATIVE_ENG_PROF_RESULTS_FILE = "C:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/Valid/19.5.2019_479_germanic_non_native_analyzed.csv"
GERMANIC_ENG_PROF_RESULTS_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/germanic_users_lex_prof_measurs.csv"
ROMANCE_ENG_PROF_RESULTS_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/Results/2020/romance_users_lex_prof_measurs.csv"

OUPUT_FILE =  "RomanceVsGermanicLexEngProfMeasureStatSig.csv"


def initialize_measuers_dict(measure_names):    
    native_measure_dict = {}
    non_native_measure_dict = {} 
    for name in measure_names:
        native_measure_dict[name] = []
        non_native_measure_dict[name] = []
    return [native_measure_dict,non_native_measure_dict]
    
def parse_files():
    native_measure_dict = {}
    non_native_measure_dict = {} 
    with open(GERMANIC_ENG_PROF_RESULTS_FILE, 'r') as native_eng_prof:
        with open(ROMANCE_ENG_PROF_RESULTS_FILE, 'r') as non_native_eng_prof:
            native_reader = csv.reader(native_eng_prof, delimiter=',')            
            measure_names = next(native_reader)             
            print(measure_names)
            [native_measure_dict,non_native_measure_dict] = initialize_measuers_dict(measure_names)
            
            for native_eng_prof_valus in native_reader:
                for i in range(len(measure_names)):
                    if i < 1 :
                        continue
                    native_measure_dict[measure_names[i]].append(float(native_eng_prof_valus[i]))
            non_native_reader = csv.reader(non_native_eng_prof, delimiter=',')
            next(non_native_reader,None)
            for non_native_eng_prof_valus in non_native_reader:
                for i in range(len(measure_names)):
                    if i < 1 or i > 4077:
                        continue
#                    print(i)
                    non_native_measure_dict[measure_names[i]].append(float(non_native_eng_prof_valus[i]))
    return [native_measure_dict,non_native_measure_dict]

def test_statistical_significance(native_measure_dict, non_native_measure_dict):
    with open(OUPUT_FILE, "w+", encoding="utf-8") as output_file:
        for measure in native_measure_dict.keys():
            output_file.write("{} :\n".format(measure))
        
            native_vector = native_measure_dict[measure]
            non_native_vector = non_native_measure_dict[measure]
    #        print(native_vector)
    #        native = stats.norm(size=168)
    #        non_native = stats.norm(size=168)
            print(len(non_native_vector))
            print(len(native_vector))
            [ttestMeasuerStatistics, ttestMeasurePvalue] =stats.ttest_ind(native_vector,non_native_vector)
            output_file.write(str(ttestMeasuerStatistics) + "\n")
            output_file.write(str(ttestMeasurePvalue)+ "\n" )
        


def Main():
    [native_measure_dict,non_native_measure_dict] = parse_files()
    test_statistical_significance(native_measure_dict,non_native_measure_dict)


if __name__ == '__main__':
    Main()