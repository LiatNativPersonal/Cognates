from RedditUser import RedditUser
from random import shuffle, sample
import pickle
import pandas as pd
import os

BEGIN_SENTENCE = "<s>"
END_SENTENCE = "</s>"
# INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Germanic\lemmas_pos_over_2000"
INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Germanic\Over2000"
# INPUT_DIR = r"/data/home/univ/lnativ1/RedditData/Romance/lemmas_pos_over_2000"
USERS_IN_BINS_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\Germanic\fold_8_germanic_vs_native_3_bins_dist_stat.csv"
# USERS_IN_BINS_FILE = r"/data/home/univ/lnativ1/scripts\new_bins_fold_2_romance_vs_natives_6_bins_stat.csv"

user_df = pd.read_csv(USERS_IN_BINS_FILE)
grades = sorted(user_df.bin.unique())
grade_to_user = {}
sample_size = 0
for grade in grades:
    # grade_df = user_df[user_df['bin'] ==grade]
    grade_df = user_df[(user_df['bin'] == grade) & (user_df['stdev_grades'] <= 1)]
    grade_to_user[grade] = list(grade_df['username'])
with open('ger_3_levels_raw_text_lexical_richness_DFH_lvl_corelation.csv','w',encoding='utf-8') as out:
    out.write('bin, #users, mattr, mtld\n')
    for grade in grades:
        user_text = []
        user = RedditUser("{}_level_users".format(grade),'Romance')
        print(grade)

        for f in grade_to_user[grade]:
            f = f.split("'")[1].split("'")[0]
            f += ".txt"

            # with open(os.path.join(INPUT_DIR, f), 'rb') as fh:
            with open(os.path.join(INPUT_DIR, f), 'r', encoding='utf-8') as fh:
                # print(f)
                # text = pickle.load(fh)
                text = fh.read()
                # text = [s.split(BEGIN_SENTENCE)[1] for s in text]
                # text = [s.split(END_SENTENCE)[0] for s in text]
                # user_text.append(fh.read())
                for sentence in text:
                    user_text.append(sentence)

                # print(user_text)
        shuffle(user_text)
        # if grade == 0:
        #     sample_size = len(user_text)
        sample_size = int(len(user_text)/3)
        user_text = sample(user_text, sample_size)
        user.text = " ".join(sent for sent in user_text)
        user.calculate_lexical_richness_measures()
        out.write("{}, {}, {}, {}\n".format(grade, len(grade_to_user[grade]), user.lexical_richness_measures['mattr'], user.lexical_richness_measures['mtld']))



    # print(len(user_text))
    # with open('debug.txt','w', encoding='utf-8') as debug:
    #     debug.write(user_text)
    #     break


