import pandas as pd
from random import sample, shuffle, choices
from scipy.stats import shapiro, normaltest
# from nltk.stem import WordNetLemmatizer
from collections import Counter
import shutil
import os
from scipy import stats
import CognateCountsAnalyzer
import spacy
import numpy as np
import pickle

ITER_NUM = 100

TOEFL_INDEX = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\index.csv"
TOEFL_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text"
TOEFL_ESSEYS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\tokenized"
TOEFL_STAT = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\stat.csv"
LOCNESS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\LOCNESS\texts"
LOCNESS_INDEX = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\LOCNESS\metadata.tsv"
LOCNESS_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\LOCNESS\lemmas_pos"
LOCNESS_COGNATE_COUNT_DIR= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\CognateCount"
TOEFL_ROMANCE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance"
TOEFL_GERMANIC_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Germanic"
TOEFL_GERMANIC_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Germanic\lemmas_pos"
TOEFL_ROMANCE_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\lemmas_pos"
TOEFL_ROMANCE_PERM_TEST_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\PermutationTest"
TOEFL_GERMANIC_PERM_TEST_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\PermutationTest"

SYNSET_ORIGIN = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin.csv"
SYNSET_ORIGIN_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin_and_POS.csv"
TOEFL_ROMANCE_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\raw_text_no_pos"
TOEFL_GERMANIC_DIR_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\raw_text_no_pos"

def corpus_stats(user_df, essay_dir, file_colum, output, file_ext = '', split_to_sentences = True):
    nlp = spacy.load('en_core_web_sm')
    words = []
    sentences = []
    types = []

    for row in user_df.iterrows():
        with open(os.path.join(essay_dir, str(row[1][file_colum]) + file_ext), 'r', encoding='utf-8') as file:
            text = file.read()
            doc = nlp(text)
            word_count = 0
            sent_count = 0
            curr_types = set()
            sent_lens = []
            for sent in doc.sents:
                if len(sent) > 0:
                    doc_clean = [w.lemma_ for w in sent if (not w.is_punct)]
                    sent_count += 1
                    word_count += len(doc_clean)
                    curr_types.update(doc_clean)
        sentences.append(sent_count)
        words.append(word_count)
        types.append(len(curr_types))
    user_df['word_count'] = words
    user_df['sent_count'] = sentences
    user_df['types_count'] = types
    user_df.to_csv(output)



def permutation_test(input_dir, output_dir, levels):
    all_text_cont = []
    lvl_to_sent_count = {}
    for lvl in levels:
        print(lvl)
        lvl_text_cont = []
        lvl_dir = os.path.join(input_dir, lvl)
        for f in os.listdir(lvl_dir):
            with open(os.path.join(lvl_dir, f), 'rb') as fh:
                # print("file = {}".format(f))
                s = pickle.load(fh)
                lvl_text_cont.append(s)
                all_text_cont.append(s)
        lvl_to_sent_count[lvl] = len([item for sublist in lvl_text_cont for item in sublist])
    all_text_cont = [item for sublist in all_text_cont for item in sublist]
    print(len(all_text_cont))
    print(lvl_to_sent_count)




    for i in range(ITER_NUM):
        shuffle(all_text_cont)
        path = os.path.join(output_dir, str(i))
        # os.mkdir(path)
        prev_count = 0
        for lvl in levels:
            new_lvl_txt = all_text_cont[prev_count:prev_count + lvl_to_sent_count[lvl]]
            prev_count += lvl_to_sent_count[lvl]
            print("new {} len = {}".format(lvl, len(new_lvl_txt)))
            with open(os.path.join(path,'{}_{}'.format(i,lvl)), 'wb') as out:
                pickle.dump( new_lvl_txt, out)



TOEFL_user_df = pd.read_csv(TOEFL_INDEX)
# LOCNESS_df = pd.read_csv(LOCNESS_INDEX, sep="\t")
# corpus_stats(LOCNESS_df, LOCNESS_PATH, 'ID', 'locness_extended_spacy.csv', file_ext=".txt", split_to_sentences=False)
# corpus_stats(TOEFL_user_df, TOEFL_ESSEYS, 'Filename', 'toefl_extended_spacy.csv')
TOEFL_df = pd.read_csv('toefl_extended_spacy.csv')
levels = ['low', 'medium', 'high', 'natives']
# levels = ['low', 'medium', 'high', 'natives', 'general']
# levels = ['low', 'medium', 'high']
input_perm_dir = os.path.join(TOEFL_ROMANCE_PERM_TEST_DIR, 'input')
output_perm_dir = os.path.join(TOEFL_ROMANCE_PERM_TEST_DIR, 'output')

# permutation_test(r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\lemmas_pos", input_perm_dir, levles)
# exit(0)

# for i in range(ITER_NUM):
#     print(i)
    # CognateCountsAnalyzer.createCountsDataFramePerUser(os.path.join(input_perm_dir, str(i)),
    #                                                    os.path.join(output_perm_dir, str(i)), 'Romance',
    #                                                    SYNSET_ORIGIN_POS, piclkeld=True, POS=True)
    # CognateCountsAnalyzer.countTOEFLCognatesPerLevel(os.path.join(output_perm_dir, str(i)), TOEFL_df)

# CognateCountsAnalyzer.countCognatesPerLevel(LOCNESS_COGNATE_COUNT_DIR)
# CognateCountsAnalyzer.countTOEFLCognatesPerLevel(ICLE_GERMANIC_COG_COUNT_DIR, ICLE_user_df, ['low','high'])


# perm_test_info = CognateCountsAnalyzer.collectPermutaionTestInfo(output_perm_dir, ITER_NUM,  levels, 'Romance')

# with open('rom_perm_test_info', 'wb') as out:
#     pickle.dump(perm_test_info, out)
ORIGIN = 'ger'
#For Tendency permutation test
GER_ANALYSIS_DIR= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\Analysis"
ROM_ANALYSIS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\Analysis"

#For texts perumtation test
TEXTS_PREM_TEST_ROM_ANALYSIS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\PermutationTest\Analysis"
TEXTS_PREM_TEST_GER_ANALYSIS_DIR= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\PermutationTest\Analysis"
# with open(os.path.join(TEXTS_PREM_TEST_ROM_ANALYSIS_DIR,'{}_perm_test_info'.format(ORIGIN)), 'rb') as fh:
#     perm_test_info = pickle.load(fh)
# print(len(perm_test_info))

# true_df = pd.read_csv(r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\Analysis\TOEFL_Germanic_cognate_counts_lemmas_pos.csv")
# real_info = CognateCountsAnalyzer.get_info(true_df, levels)
# exit(0)
# with open(os.path.join(ROM_ANALYSIS_DIR,'{}_real_info_with_natives'.format(ORIGIN)), 'wb') as out:
#     pickle.dump(real_info, out)
with open(os.path.join(GER_ANALYSIS_DIR, '{}_real_info_with_natives'.format(ORIGIN)), 'rb') as fh:
    real_info = pickle.load(fh)

def RatioPermTest():

    valids = {}
    # print(real_info[1])

    for synset, level in real_info.items():
        # for info in level.values():
        #     print(info)

        not_nones = [level[x]['{}_ratio'.format(ORIGIN)] for x in level.keys() if level[x]['{}_ratio'.format(ORIGIN)] is not None]
        if len(not_nones) > 1:
            valids[synset] = not_nones
    print(len(valids))
    exit(0)
    # print(not_nones)
# print(len(valids.keys()))
# Ratio Permutation test.

    real_sig_value =0
    syn_to_total_counts = {}

    for syn, ratios in valids.items():
        for i in range(1, len(ratios)):
            if ratios[i-1] > ratios[i]:
                real_sig_value += 1
        # print(real_sig_value)
        # if ratios[0] < ratios[1]:
        #     real_sig_value += 1
        # if len(ratios) == 3 and ratios[1] < ratios[2]:
        #     real_sig_value += 1
        syn_to_total_counts[syn] = {}
        syn_info = real_info[syn]
        syn_to_total_counts[syn]['total_rom'] = sum([syn_info[x]['rom_count'] for x in level.keys()])
        syn_to_total_counts[syn]['total_ger'] = sum([syn_info[x]['ger_count'] for x in level.keys()])
        syn_to_total_counts[syn]['total_low'] = sum([syn_info['low']['ger_count']]) + sum([syn_info['low']['rom_count']])
        syn_to_total_counts[syn]['total_medium'] = sum([syn_info['medium']['ger_count']]) + sum([syn_info['medium']['rom_count']])
        syn_to_total_counts[syn]['total_high'] = sum([syn_info['high']['ger_count']]) + sum([syn_info['high']['rom_count']])
        syn_to_total_counts[syn]['total_natives'] = sum([syn_info['natives']['ger_count']]) + sum(
            [syn_info['natives']['rom_count']])
        # syn_to_total_counts[syn]['total_general'] = sum([syn_info['general']['ger_count']]) + sum(
        #     [syn_info['general']['rom_count']])
    print("real_sig_value = {}".format(real_sig_value))
    # print(syn_to_total_counts)
    random_ratios = {}
    sig_values = []

    for x in range(10000):
        sig_value = 0

        for syn,totals in syn_to_total_counts.items():
            random_ratios[syn] = []
            number_of_samples = len(valids[syn])
            perm = ['G'] * totals['total_ger'] + ['R'] * totals['total_rom']
            shuffle(perm)
            # print(perm)
            start = 0
            for lvl in level.keys():
                if totals['total_{}'.format(lvl)] > 0:
                    sample = perm[start:start + totals['total_{}'.format(lvl)]]
                    start += totals['total_{}'.format(lvl)]
                    c = Counter(sample)
                    random_ratios[syn].append(c['R'] / (c['R'] + c['G']))
                    # print(rom_ratio)
                    # random_ratios[syn].append(c['R'](c['R'] + c['G']))
            # print(random_ratios)
            for i in range(1, len(random_ratios[syn])):
                if random_ratios[syn][i - 1] > random_ratios[syn][i]:
                    sig_value += 1
            # if random_ratios[syn][0] < random_ratios[syn][1]:
            #     sig_value += 1
            # if len(random_ratios) ==  and random_ratios[syn][1] < random_ratios[syn][2]:
            #     sig_value += 1
        sig_values.append(sig_value)
        # print(sig_value)
    print(sig_values)
    import matplotlib.pyplot as plt
    plt.hist(sig_values)
    plt.savefig('rom_with_locness_perm.png')
    # print(random_ratios)
    print(len(random_ratios.keys()))
    stat, p = normaltest(sig_values)
    print(p)
    print(np.mean(sig_values))
    print(max(sig_values))
    print(min(sig_values))
    with open("{}_debug.csv".format(ORIGIN), 'w', encoding='utf-8') as out:
        for val in sig_values:
            out.write("{},".format(val))




thresholds = [3]
valid_synsets = {}

ratios_data = {}

RatioPermTest()