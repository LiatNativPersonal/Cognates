import pandas as pd
from random import sample, shuffle, choices
from scipy.stats import shapiro, normaltest
# from nltk.stem import WordNetLemmatizer
import shutil
import os
from scipy import stats
# import CognateCountsAnalyzer
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

# ICLE_GERMANIC_LEMMAS_POS_DIR = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\lemmas_pos\Germanic'
# ICLE_ROMANCE_LEMMAS_POS_DIR = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\lemmas_pos\Romance'
SYNSET_ORIGIN = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin.csv"
SYNSET_ORIGIN_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin_and_POS.csv"
TOEFL_ROMANCE_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\raw_text_no_pos"
TOEFL_GERMANIC_DIR_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\raw_text_no_pos"
# ICLE_ROMANCE_COG_COUNT_DIR = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\CognateCount\Romance'
# ICLE_GERMANIC_COG_COUNT_DIR = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\CognateCount\Germanic'

# ICLE_ROMANCE_TOP_AND_BOTTOM_10_PERCENT = r'C:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\Log_reg_fold_3_Romance_ICLE_vs_LOCNESS_top_and_bottom_10_pr.csv'
# ICLE_GERMANIC_TOP_AND_BOTTOM_10_PERCENT = r'C:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\Log_reg_fold_3_Germanic_ICLE_vs_LOCNESS_top_and_bottom_10_pr.csv'
#
# CHUNK_SIZE = 1000
# TOEFL_GERMANIC_DIR_COG_COUNT_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\lemmas_pos"
# TOEFL_ROMANCE_DIR_COG_COUNT_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\lemmas_pos"
# dist_dir = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\TOEFL'
#
# def isStatSigDiif():
#     for f in os.listdir(dist_dir):
#         dist_df = pd.read_csv(os.path.join(dist_dir, f))
#         lows_dist = list(dist_df.loc[dist_df['grade'] == 'low', 'distance'])
#         meds_dist = list(dist_df.loc[dist_df['grade'] == 'medium', 'distance'])
#         highs_dist = list(dist_df.loc[dist_df['grade'] == 'high', 'distance'])
#         print(stats.ranksums(lows_dist, highs_dist))
#         print(stats.ranksums(lows_dist, meds_dist))
#         print(stats.ranksums(meds_dist, highs_dist))
#
#
#
def corpus_stats(user_df, essay_dir, file_colum, output, file_ext = '', split_to_sentences = True):
    nlp = spacy.load('en_core_web_sm')
    words = []
    sentences = []
    types = []
    # avg_sent_len = []

    for row in user_df.iterrows():
        with open(os.path.join(essay_dir, str(row[1][file_colum]) + file_ext), 'r', encoding='utf-8') as file:
            text = file.read()
            doc = nlp(text)
            # if not split_to_sentences:
            #     text = text.replace('.', '\n')
            word_count = 0
            sent_count = 0
            curr_types = set()
            sent_lens = []
            for sent in doc.sents:
            # for line in text.split('\n'):
            #     line = line.strip()
                if len(sent) > 0:
            #         doc = nlp(line)
                    doc_clean = [w.lemma_ for w in sent if (not w.is_punct)]
                    sent_count += 1
                    word_count += len(doc_clean)
                    # sent_lens.append(len(doc_clean))
                    curr_types.update(doc_clean)
        sentences.append(sent_count)
        words.append(word_count)
        types.append(len(curr_types))
        # avg_sent_len.append(numpy.mean(sent_lens))
    # print(len(sentences))
         # print("{}: sent: {}, words: {}, types: {}".format(file, sent_count, word_count, len(types)))
    user_df['word_count'] = words
    user_df['sent_count'] = sentences
    user_df['types_count'] = types
    # user_df['avg_sent_len'] = avg_sent_len
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
levels = ['low', 'medium', 'high']
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
ORIGIN = 'rom'
GER_ANALYSIS_DIR= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\Analysis"
ROM_ANALYSIS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\Analysis"
# with open(os.path.join(GER_ANALYSIS_DIR,'ger_perm_test_info'), 'rb') as fh:
#     perm_test_info = pickle.load(fh)
# print(len(perm_test_info))

# true_df = pd.read_csv(r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\lemmas_pos\TOEFL_Romance_cognate_counts_lemmas_pos.csv")
# real_info = CognateCountsAnalyzer.get_info(true_df, levels)
# with open('ger_real_info', 'wb') as out:
#     pickle.dump(real_info, out)

with open(os.path.join(ROM_ANALYSIS_DIR,'{}_real_info'.format(ORIGIN)), 'rb') as fh:
    real_info = pickle.load(fh)
valids = {}
# print(real_info[1])

for synset, level in real_info.items():
    # for info in level.values():
    #     print(info)
    not_nones = [level[x]['{}_ratio'.format(ORIGIN)] for x in level.keys() if level[x]['{}_ratio'.format(ORIGIN)] is not None]
    if len(not_nones) > 1:
        valids[synset] = not_nones

    # print(not_nones)
# print(len(valids.keys()))

real_sig_value =0
syn_to_total_counts = {}
for syn, ratios in valids.items():
    if ratios[0] < ratios[1]:
        real_sig_value += 1
    if len(ratios) == 3 and ratios[1] < ratios[2]:
        real_sig_value += 1
    syn_to_total_counts[syn] = []
    syn_info = real_info[syn]
    syn_to_total_counts[syn].append(sum([syn_info[x]['rom_count'] for x in level.keys()]))
    syn_to_total_counts[syn].append(sum([syn_info[x]['ger_count'] for x in level.keys()]))
print("real_sig_value = {}".format(real_sig_value))
# print(syn_to_total_counts)
random_ratios = {}
sig_values = []
for x in range(800):

    sig_value = 0
    for syn,count in syn_to_total_counts.items():
        number_of_samples = len(valids[syn])
        # print(number_of_samples)
        rom_start = 0
        ger_start = 0
        rom_end = count[0]
        ger_end = count[1]
        # print("rom_end = {}".format(rom_end))
        # print("ger_end = {}".format(ger_end))

        random_ratios[syn] = []

        for i in range(number_of_samples -1):
            # print("i = {}".format(i))
            rom = 0
            ger = 0
            if rom_end > 0:
                rom = choices(range(rom_start, rom_end), k=1)[0]
            if ger_end > 0:
                ger = choices(range(ger_start, ger_end), k=1)[0]
            # print("rom = {}".format(rom))
            # print("ger = {}".format(ger))
            if ger+rom > 0:
                random_ratios[syn].append(rom/(ger+rom))
            else:
                random_ratios[syn].append(None)
            rom_end -= rom
            ger_end -= ger

        if rom_end + ger_end > 0:
            random_ratios[syn].append(rom_end / (ger_end + rom_end))
        else:
            random_ratios[syn].append(None)
        if random_ratios[syn][0] is not None and random_ratios[syn][1] is not None \
                and random_ratios[syn][0] < random_ratios[syn][1]:
            sig_value += 1
        if len(random_ratios) == 3 and random_ratios[syn][1] is not None and random_ratios[syn][2] is not None \
                and random_ratios[syn][1] < random_ratios[syn][2]:
            sig_value += 1
    sig_values.append(sig_value)
print(sig_values)
print(random_ratios)
print(len(random_ratios.keys()))
stat, p = normaltest(sig_values)
print(p)
print(np.mean(sig_values))
print(np.std(sig_values))
# with open("ger_debug.csv", 'w', encoding='utf-8') as out:
#     for val in sig_values:
#         out.write("{},".format(val))


    # print(nones)
    # break

exit(0)
# exit(0)
# print(perm_test_info[0])
# print(perm_test_info[1])
# exit(0)

# print(real_info)
thresholds = [1, 3, 5]
valid_synsets = {}

ratios_data = {}
# ratios_data['real'] = {}

for th in thresholds:
    ratios_data[th] = {}
    print("threshold = {}".format(th))
    valid_synsets[th] = []
    for synset in real_info.keys():
        counts = []
        ger_total = 0
        rom_total = 0
        for lvl, info in real_info[synset].items():
            counts.append(info['total'])
            ger_total += info['ger_count']
            rom_total += info['rom_count']
        if all(i >= th for i in counts) :
            # and ger_total > 0 and rom_total > 0:
            valid_synsets[th].append(synset)


for th in thresholds:
    ratios_data[th]['real'] = {}
    for lvl in levels:
        ratios = []
        for valid_s in valid_synsets[th]:
            ratios.append(real_info[valid_s][lvl]['ger_ratio'])
        ratios_data[th]['real'][lvl] = np.mean(ratios)
    for i in range(ITER_NUM):
        ratios_data[th][i] = {}
        for lvl in levels:
            ratios = []
            for valid_s in valid_synsets[th]:
                ratio = perm_test_info[i][valid_s][lvl]['ger_ratio']
                if ratio != None:
                    ratios.append(ratio)
            ratios_data[th][i][lvl] = np.mean(ratios)
#     for th in thresholds:
#         ratios[]



ANALYSIS_DIR= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\PermutationTest\Analysis"
print(ratios_data)
data = {}
data['Level'] = levels
for th in thresholds:
    filename = os.path.join(GER_ANALYSIS_DIR, '{}_germanic_ratios.csv'.format(th))

    for i in range(ITER_NUM):
        values = []
        for lvl in levels:
            values.append(ratios_data[th][i][lvl])
        data[i] = values
    values = []
    for lvl in levels:
        values.append(ratios_data[th]['real'][lvl])
    data['real'] = values
    df = pd.DataFrame(data)
    df.to_csv(filename)
    # counts = [x['total'] for lvl in info.keys() for x in info[lvl]]
    # print(counts)
