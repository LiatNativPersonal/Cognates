import os
import pickle
from collections import Counter
from nltk import ngrams

CHUNK_SIZE = 2000
BEGIN_SENTENCE = "<s>"
END_SENTENCE = "</s>"
SEPERATOR = "_"
TRI = 3
TOP_POS_TRIGRAMS = 500

NATIVE_DIR = r"/data/home/univ/lnativ1/RedditData/Native/lemmas_pos_over_2000/"
NON_NATIVE_DIR = r"/data/home/univ/lnativ1/RedditData/Romance/lemmas_pos_over_2000/"
# NATIVE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Native\lemmas_pos_over_2000"
# NON_NATIVE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\lemmas_pos_over_2000"
POS_TRIGRAMS = r"/data/home/univ/lnativ1/RedditData/POS_trigrams.txt"
# POS_TRIGRAMS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\POS_trigrams.txt"
function_words_list = []

POS_trigrams_vocab = Counter()
INPUT_DIRS = [NATIVE_DIR, NON_NATIVE_DIR]
for input_dir in INPUT_DIRS:
    for f in os.listdir(input_dir):
        print(f)
        with open(os.path.join(input_dir,f),'rb') as fh:
            text = pickle.load(fh)
            text = [s.split(BEGIN_SENTENCE)[1] for s in text]
            text = [s.split(END_SENTENCE)[0] for s in text]
            for sentence in text:
                sentence = sentence.strip()
                pos_seq = BEGIN_SENTENCE + " " + " ".join([token.split(SEPERATOR)[1] for token in sentence.split()]) + " " + END_SENTENCE
                POS_trigrams_vocab.update(ngrams(pos_seq.split(" "), TRI))
most_common_trigrams = POS_trigrams_vocab.most_common(TOP_POS_TRIGRAMS)
most_common_trigrams = [" ".join(x[0]) for x in most_common_trigrams]
with open(POS_TRIGRAMS, 'w', encoding='utf-8') as POS_tri_file:
    for pos_tri in most_common_trigrams:
        POS_tri_file.write(pos_tri + '\n')
