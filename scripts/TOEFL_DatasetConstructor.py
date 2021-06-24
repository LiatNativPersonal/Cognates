import pandas as pd
from random import sample, shuffle
from nltk.stem import WordNetLemmatizer
import shutil
import os
from scipy import stats
import CognateCountsAnalyzer

TOEFL_INDEX = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\index.csv"
TOEFL_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text"
TOEFL_ESSEYS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\tokenized"
TOEFL_STAT = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\stat.csv"
LOCNESS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\texts"
LOCNESS_INDEX = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\metadata.tsv"
LOCNESS_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\lemmas_pos"
TOEFL_SHUFFELED_CHUNKS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\romance_shuffeld_chunks"
LOCNESS_SHUFFELED_CHUNKS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\shuff"
LOCNESS_COGNATE_COUNT_DIR= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\CognateCount"
TOEFL_ROMANCE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance"
TOEFL_GERMANIC_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Germanic"
TOEFEL_GERMANIC_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Germanic\lemmas_pos"
TOEFEL_ROMANCE_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\lemmas_pos"
SYNSET_ORIGIN = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin.csv"
SYNSET_ORIGIN_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin_and_POS.csv"
TOEFL_ROMANCE_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\raw_text_no_pos"
TOEFL_GERMANIC_DIR_COG_COUNT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\raw_text_no_pos"
CHUNK_SIZE = 1000
TOEFL_GERMANIC_DIR_COG_COUNT_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Germanic\lemmas_pos"
TOEFL_ROMANCE_DIR_COG_COUNT_LEMMAS_POS_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\CognateCount\Romance\lemmas_pos"
dist_dir = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\TOEFL'

def isStatSigDiif():
    for f in os.listdir(dist_dir):
        dist_df = pd.read_csv(os.path.join(dist_dir, f))
        lows_dist = list(dist_df.loc[dist_df['grade'] == 'low', 'distance'])
        meds_dist = list(dist_df.loc[dist_df['grade'] == 'medium', 'distance'])
        highs_dist = list(dist_df.loc[dist_df['grade'] == 'high', 'distance'])
        print(stats.ranksums(lows_dist, highs_dist))
        print(stats.ranksums(lows_dist, meds_dist))
        print(stats.ranksums(meds_dist, highs_dist))


user_df = pd.read_csv(TOEFL_INDEX)
# romance_files = list(user_df.loc[(user_df['Language'] == 'SPA') | (user_df['Language'] == 'ITA') | (user_df['Language'] == 'FRA'), 'Filename'])
germanic_files = list(user_df.loc[(user_df['Language'] == 'DEU'), 'Filename'])
# for f in germanic_files:
#     shutil.copy(os.path.join(TOEFL_ESSEYS, f), TOEFL_GERMANIC_DIR)
locness_df = pd.read_csv(LOCNESS_INDEX, sep="\t")

# CognateCountsAnalyzer.createCountsDataFramePerUser(TOEFEL_ROMANCE_LEMMAS_POS_DIR,
#                                                    TOEFL_ROMANCE_DIR_COG_COUNT_LEMMAS_POS_DIR, 'Romance',
#                                                    SYNSET_ORIGIN_POS, piclkeld=True, POS=True)
CognateCountsAnalyzer.countTOEFLCognatesPerLevel(TOEFL_ROMANCE_DIR_COG_COUNT_LEMMAS_POS_DIR,
                                                 user_df.loc[(user_df['Language'] == 'FRA') ])#|
#                                                              (user_df['Language'] == 'ITA') |
#                                                              (user_df['Language'] == 'FRA')])
# CognateCountsAnalyzer.countCognatesPerLevel(LOCNESS_COGNATE_COUNT_DIR)


