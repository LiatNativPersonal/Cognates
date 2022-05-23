import pandas as pd
import numpy as np
import os
import glob
import re
from RedditUser import RedditUser
from RedditCognatesCounter import RedditCognatesCounter
import csv
import pickle
import csv
SYNSET_ORIGIN = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin_and_POS.csv"
GERMANIC_INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Germanic\lemmas_pos_over_2000"
ROMANCE_INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\lemmas_pos_over_2000"
NATIVE_INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Native\lemmas_pos_over_2000"
GERMANIC_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Germanic\CognateCounts"
ROMANCE_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\CognateCounts"
USERS_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\Germanic\fold_8_germanic_vs_native_6_bins_dist_stat.csv"
NUMBER_OF_LEVELS = 6
# NATIVES_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Native\CognateCounts"
NATIVES_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\CognateCount"
SYNSET_NUM = 235
TOEFL_SYNSET_NUM = 235
MIN_OCCUR = 1000


def createCountsDataFramePerUser(SOURCE_DIR, COG_DIR, L1, synset_origin, piclkeld = True, POS = True):
    cog_cntr = RedditCognatesCounter(synset_origin)
    for f in os.listdir(SOURCE_DIR):
        redditUser = RedditUser(f, L1, os.path.join(SOURCE_DIR, f))
        output_path = os.path.join(COG_DIR, "{}.csv".format(redditUser.user_name))
        # if not os.path.exists(output_path):
        print("processing {}".format(redditUser.user_name))
        cog_cntr.count_cognates_for_user(redditUser, piclkeld)
        user_df = cog_cntr.users_cognate_counts_dict[redditUser]
        user_df.to_csv(output_path)




def countTOEFLCognatesPerLevel(COG_COUNT_DIR, non_native_df, levels = ['low', 'medium', 'high']):
    user_df = non_native_df
    synset_to_level_to_total_count = {}

    for level in levels:
        synset_to_level_to_total_count[level] = {}

        for syn in range(1, TOEFL_SYNSET_NUM + 1):
            synset_to_level_to_total_count[level][syn] = {}
            synset_to_level_to_total_count[level][syn]['G'] = 0
            synset_to_level_to_total_count[level][syn]['R'] = 0
    with open(os.path.join(COG_COUNT_DIR, "{}_Romance_cognate_counts_lemmas_pos.csv".format(os.path.basename(COG_COUNT_DIR))), 'w',encoding='utf-8') as counts_out:
        header = "level"
        for syn in range(1, TOEFL_SYNSET_NUM + 1):
            header += ",{}_ratio".format(syn)

        counts_out.write(header + "\n")
        for level in levels:
            level_users = user_df.loc[user_df['Score Level'] == level, 'Filename']
            files = list([os.path.join(COG_COUNT_DIR, x) for x in level_users])
            print(files)
            level_counts_df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
            for syn in range(1, TOEFL_SYNSET_NUM + 1):
                synset_to_level_to_total_count[level][syn]['G'] = level_counts_df.loc[
                    (level_counts_df['Source'] == 'G') & (level_counts_df['synset'] == syn), 'count'].sum()
                synset_to_level_to_total_count[level][syn]['R'] = level_counts_df.loc[
                    (level_counts_df['Source'] == 'R') & (level_counts_df['synset'] == syn), 'count'].sum()
        for level in levels:
            ger_counts_line = "level_{}_ger_count".format(level)
            for syn in range(1, TOEFL_SYNSET_NUM + 1):
                ger_counts_line += ",{}".format(synset_to_level_to_total_count[level][syn]['G'])

            counts_out.write(ger_counts_line + "\n")

        for level in levels:
            rom_counts_line = "level_{}_rom_count".format(level)
            for syn in range(1, TOEFL_SYNSET_NUM + 1):
                rom_counts_line += ",{}".format(synset_to_level_to_total_count[level][syn]['R'])
            counts_out.write(rom_counts_line + "\n")

def countCognatesPerLevel(COG_COUNT_DIR):
    user_df = pd.read_csv(USERS_FILE)
    levels_num = NUMBER_OF_LEVELS
    natives_counts = glob.glob(os.path.join(NATIVES_COG_COUNT_DIR, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

    natives_counts_df = pd.concat([pd.read_csv(f) for f in natives_counts], ignore_index=True)
    synset_to_native_info = {}
    for syn in range(1, SYNSET_NUM+1):
        synset_to_native_info[syn] = {}


        synset_to_native_info[syn]['G'] = natives_counts_df.loc[
            (natives_counts_df['Source'] == 'G') & (natives_counts_df['synset'] == syn), 'count'].sum()
        synset_to_native_info[syn]['R'] = natives_counts_df.loc[
            (natives_counts_df['Source'] == 'R') & (natives_counts_df['synset'] == syn), 'count'].sum()
        all = synset_to_native_info[syn]['G'] +  synset_to_native_info[syn]['R']
        if all > 0:
            synset_to_native_info[syn]['ratio'] =  synset_to_native_info[syn]['R']/all
        else:
            synset_to_native_info[syn]['ratio'] = '-'
    with open(os.path.join(NATIVES_COG_COUNT_DIR,"native_synset_to_ratio.csv"), 'w') as natives_counts_out:
        header = ""
        for syn in range(1, SYNSET_NUM + 1):
            header += ",{}_ratio".format(syn)
        natives_counts_out.write(header+"\n")
        native_ger_counts_line = "natives_ger_count"
        for syn in range(1, SYNSET_NUM + 1):
            native_ger_counts_line += ",{}".format(synset_to_native_info[syn]['G'])
        natives_counts_out.write(native_ger_counts_line + "\n")

        native_rom_counts_line = "natives_rom_count"
        for syn in range(1, SYNSET_NUM + 1):
            native_rom_counts_line += ",{}".format(synset_to_native_info[syn]['R'])
        natives_counts_out.write(native_rom_counts_line + "\n")

    return


    synset_to_level_to_total_count = {}
    for level in range(levels_num):
        synset_to_level_to_total_count[level] = {}
        for syn in range(1, SYNSET_NUM + 1):
            synset_to_level_to_total_count[level][syn] = {}
            synset_to_level_to_total_count[level][syn]['G'] = 0
            synset_to_level_to_total_count[level][syn]['R'] = 0

    with open(os.path.join(COG_COUNT_DIR, "6_levels_cognates_ratios_per_bin_with_counts.csv"), 'w', encoding='utf-8') as ratios_out:
        header = "level"
        for syn in range(1,SYNSET_NUM+1):
            header += ",{}_ratio".format(syn)

        ratios_out.write(header +"\n")
        synset_to_non_native_ratio = {}
        for level in range(levels_num):
            level_users = user_df.loc[(user_df['bin'] == level) & (user_df['stdev_grades'] <= 1), 'username']
            level_users = [x[1:-1] for x in level_users]
            files =list([os.path.join(COG_COUNT_DIR, x + ".csv") for x in level_users])
            print("levle {}: {} files".format(level, len(files)))
            level_counts_df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
            print(len(level_counts_df))


            synset_to_non_native_ratio[level] = {}
            line = "level_{}".format(level)

            for syn in range(1, SYNSET_NUM+1):

                # print(synset_to_level_to_total_count[level][syn])

                synset_to_level_to_total_count[level][syn]['G'] = level_counts_df.loc[(level_counts_df['Source'] == 'G') & (level_counts_df['synset'] == syn), 'count'].sum()
                synset_to_level_to_total_count[level][syn]['R'] = level_counts_df.loc[(level_counts_df['Source'] == 'R') & (level_counts_df['synset'] == syn), 'count'].sum()

                total = synset_to_level_to_total_count[level][syn]['G'] + synset_to_level_to_total_count[level][syn]['R']
                if total > 0 and synset_to_native_info[syn]['ratio'] != '-':
                    line += ",{}".format((synset_to_level_to_total_count[level][syn]['R'] / total) - synset_to_native_info[syn]['ratio'])
                else:
                    line += ",-"

            ratios_out.write(line + "\n")
        ratios_out.write("\n\n\n")




        for level in range(levels_num):
            ger_counts_line = "level_{}_ger_count".format(level)
            for syn in range(1, SYNSET_NUM + 1):
                ger_counts_line += ",{}".format(synset_to_level_to_total_count[level][syn]['G'])

            ratios_out.write(ger_counts_line + "\n")





        for level in range(levels_num):
            rom_counts_line = "level_{}_rom_count".format(level)
            for syn in range(1, SYNSET_NUM + 1):
                rom_counts_line += ",{}".format(synset_to_level_to_total_count[level][syn]['R'])
            ratios_out.write(rom_counts_line + "\n")

        ratios_out.write("\n\n\n")

        native_ger_counts_line = "natives_ger_count"
        for syn in range(1, SYNSET_NUM + 1):
            native_ger_counts_line += ",{}".format(synset_to_native_info[syn]['G'])
        ratios_out.write(native_ger_counts_line + "\n")

        native_rom_counts_line = "natives_rom_count"
        for syn in range(1, SYNSET_NUM + 1):
            native_rom_counts_line += ",{}".format(synset_to_native_info[syn]['R'])
        ratios_out.write(native_rom_counts_line + "\n")




def calcGeneralFrequency(freq_list, output):
    cols = ['word', 'pos', 'freq']
    freq_df = pd.read_csv(freq_list, 'r', delimiter= '\t', names = cols, header = None)
    POS_dict = {"VERB": "V", "NOUN": "N", "ADJ": "JJ", "SCONJ": "IN", "ADV": "RB"}
    fieldnames =['synset', 'word', 'pos', 'source', 'freq']
    # i = 0
    with open(output,'w', encoding='utf-8') as freq_out:
        writer = csv.DictWriter(freq_out, fieldnames=fieldnames)
        writer.writeheader()
        synset_df = pd.read_csv(SYNSET_ORIGIN)
        for row in synset_df.iterrows():
            word = row[1]['word']
            pos = POS_dict[row[1]['POS']]
            occ = freq_df[freq_df['word'] == word]
            # print(occ)
            freq_sum = 0
            for word_pos in occ.iterrows():
                if str(word_pos[1]['pos']).startswith(pos):
                    freq_sum += int(word_pos[1]['freq'])
            writer.writerow({'synset':row[1]['synset'], 'word':word, 'pos':row[1]['POS'], 'source': row[1]['Source'], 'freq':freq_sum})

def calcGeneralCountsPerSynsetOrigin(freq_list, output):
    general_freq_df = pd.read_csv(freq_list)
    synset_to_origin_to_count = {}
    for syn in range(1, SYNSET_NUM+1):
        synset_to_origin_to_count[syn] = {}
        synset_to_origin_to_count[syn]['G'] = general_freq_df.loc[
            (general_freq_df['Source'] == 'G') & (general_freq_df['synset'] == syn), 'freq'].sum()
        synset_to_origin_to_count[syn]['R'] = general_freq_df.loc[
            (general_freq_df['Source'] == 'R') & (general_freq_df['synset'] == syn), 'freq'].sum()
    with open(output, 'w', encoding='utf-8') as ratios_out:
        header = ""
        for syn in range(1, SYNSET_NUM + 1):
            header += ",{}_ratio".format(syn)
        ratios_out.write(header + "\n")
        general_ger_counts_line = "general_ger_count"
        for syn in range(1, SYNSET_NUM + 1):
            general_ger_counts_line += ",{}".format(synset_to_origin_to_count[syn]['G'])
        ratios_out.write(general_ger_counts_line + "\n")

        general_rom_counts_line = "general_rom_count"
        for syn in range(1, SYNSET_NUM + 1):
            general_rom_counts_line += ",{}".format(synset_to_origin_to_count[syn]['R'])
        ratios_out.write(general_rom_counts_line + "\n")



def get_info(df_info, levels):
    info_dict = {}
    for j in range(1, SYNSET_NUM + 1):
        info_dict[j] = {}
        for lvl in levels:

            info_dict[j][lvl] = {}
            info_dict[j][lvl]['ger_count'] = int(df_info.loc[df_info['level'] ==
                                                                     'level_{}_ger_count'.format(lvl),
                                                                     "{}_ratio".format(j)])
            info_dict[j][lvl]['rom_count'] = int(df_info.loc[df_info['level'] ==
                                                                     'level_{}_rom_count'.format(lvl),
                                                                     "{}_ratio".format(j)])
            info_dict[j][lvl]['total'] = info_dict[j][lvl]['ger_count'] + info_dict[j][lvl]['rom_count']
            if info_dict[j][lvl]['total'] > 0:
                info_dict[j][lvl]['ger_ratio'] = info_dict[j][lvl]['ger_count'] / info_dict[j][lvl]['total']
                info_dict[j][lvl]['rom_ratio'] = info_dict[j][lvl]['rom_count'] / info_dict[j][lvl]['total']
            else:
                info_dict[j][lvl]['ger_ratio'] = None
                info_dict[j][lvl]['rom_ratio'] = None
    return info_dict

# calcGeneralFrequency(r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\encow16ax.wp.tsv', 'freq_out_origin.csv')

# calcGeneralCountsPerSynsetOrigin(r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\freq_list_origin.csv',"general_counts.csv")










