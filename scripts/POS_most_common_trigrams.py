import os
import pickle
from collections import Counter, OrderedDict
from nltk import ngrams

CHUNK_SIZE = 2000
BEGIN_SENTENCE = "<s>"
END_SENTENCE = "</s>"
SEPERATOR = "_"
TRI = 3
TOP_POS_TRIGRAMS = 500

# NATIVE_DIR = r"/data/home/univ/lnativ1/RedditData/Native/lemmas_pos_over_2000/"
# ROMANCE_DIR = r"/data/home/univ/lnativ1/RedditData/Romance/lemmas_pos_over_2000/"
# GEMANIC_DIR = r"/data/home/univ/lnativ1/RedditData/Germanic/lemmas_pos_over_2000/"
# NATIVE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\lemmas_pos\essays"
NATIVE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\main-HebrewEssays-data-HEC\lemmas_pos\native"
# NON_NATIVE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\lemmas_pos\all"
# NON_NATIVE_DIR = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\lemmas_pos\All'
NON_NATIVE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\main-HebrewEssays-data-HEC\lemmas_pos\non_native\all"
# POS_TRIGRAMS = r"/data/home/univ/lnativ1/RedditData/GER_POS_trigrams.txt"
POS_TRIGRAMS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\HEC_POS_trigrams.txt"
function_words_list = []

POS_trigrams_vocab = Counter()
INPUT_DIRS = [NATIVE_DIR, NON_NATIVE_DIR]
for input_dir in INPUT_DIRS:
    for f in os.listdir(input_dir):
        print(f)
        with open(os.path.join(input_dir,f),'rb') as fh:
            text = pickle.load(fh)
            # text = [item for sublist in text for item in sublist]

            text = [s.split(BEGIN_SENTENCE)[1] for s in text]
            text = [s.split(END_SENTENCE)[0] for s in text]
            for sentence in text:
                sentence = sentence.strip()
                try:
                    pos_seq = BEGIN_SENTENCE + " " + " ".join([token.split(SEPERATOR)[1] for token in sentence.split()]) + " " + END_SENTENCE
                    POS_trigrams_vocab.update(ngrams(pos_seq.split(" "), TRI))
                except:
                    continue

# most_common_trigrams = POS_trigrams_vocab.most_common(TOP_POS_TRIGRAMS)
# most_common_trigrams = [" ".join(x[0]) for x in most_common_trigrams]
POS_tri_sorted_by_value = OrderedDict(sorted(POS_trigrams_vocab.items(), key=lambda x: x[1], reverse=True))
with open(POS_TRIGRAMS, 'w', encoding='utf-8') as POS_tri_file:
    for pos_tri, count in POS_tri_sorted_by_value.items():
        POS_tri_file.write(" ".join(pos_tri) + ', {}\n'.format(count))
