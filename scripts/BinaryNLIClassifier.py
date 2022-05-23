# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 11:10:22 2020

@author: liatn
"""

from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split, cross_validate, StratifiedKFold, \
    KFold, StratifiedShuffleSplit, ShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
import pandas as pd
from scipy import stats
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import StandardScaler

from nltk.tokenize import sent_tokenize, word_tokenize
from collections import OrderedDict
from collections import Counter

from imblearn.over_sampling import SMOTE
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
# from RedditUser import RedditUser
# from RedditCognatesCounter import RedditCognatesCounter
from scipy.sparse import coo_matrix, hstack
import scipy.sparse as sp
from sklearn import svm
import numpy as np
from random import sample, shuffle
from scipy.sparse import vstack
import shutil
# from lexicalrichness import LexicalRichness
import os
import pickle
import LogisticRegressionUsingGD


FUNCTION_WORDS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\function-words.csv"
# FUNCTION_WORDS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\German_function_word.txt"
# FUNCTION_WORDS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\5_prefixes_heb.txt"

# POS_TRIGRAMS_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\TOEFEL_LOCNESS_POS_trigrams.txt"
POS_TRIGRAMS_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Merlin_Falko_POS_trigrams.txt"
# POS_TRIGRAMS_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\HEC_POS_trigrams.txt"

TOEFL_INDEX = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\index.csv"
TOEFL_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text"
TOEFL_ESSEYS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\tokenized"
TOEFL_STAT = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\stat.csv"
LOCNESS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\LOCNESS\texts"

LOCNESS_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\LOCNESS\lemmas_pos"
TOEFL_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\lemmas_pos"
TOEFL_ROMANCE_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\lemmas_pos"
TOEFL_FRA_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\FRA"
TOEFL_ITA_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\ITA"
TOEFL_GERMANIC_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\Germanic\lemmas_pos"

MERLIN_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\German\Merlin\ClassificationDataset\lemmas_pos"
FALKO_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\German\Falko\ClassificationDataset\lemmas_pos"

HEC_NATIVE_LEMMAS_POS = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\ClassificationDataset\lemmas_pos\native'
HEC_NON_NATIVE_LEMMAS_POS = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\ClassificationDataset\lemmas_pos\non_native'
HEC_NON_NATIVE_META_DATA = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\data\HEC\Non_Native_Metadata.csv'


TOEFL_DEBUG = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\English\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\debug'

CHUNK_SIZE = 1000
NUMBER_OF_BINS = 5

BEGIN_SENTENCE = "<s>"
END_SENTENCE = "</s>"
SEPERATOR = "_"
TRI = 3
TOP_POS_TRIGRAMS = 500
NATIVE = 1
NON_NATIVE = 0
SPLITS = 10
TEST_SIZE = 1/SPLITS


class BinaryNLIClassifier:

    def __init__(self):
        self.classifier = LogisticRegression(penalty='l2', dual=True, solver='liblinear', warm_start=True, C=10.0)
        # self.classifier = svm.SVC()
        # self.classifier = svm.LinearSVC()
        self.function_words_file = FUNCTION_WORDS
        self.function_words_list = []
        self.non_natives = []
        self.natives = []
        self.non_natives_user_to_distance_from_border_line = {}
        self.natives_user_to_distance_from_border_line = {}
        self.createFunctionWordList()
        self.create_pos_trigram_list()
        # self.createFeatureVectors()
        # self.splitDataAndClassify()

    def create_pos_trigram_list(self):
        pos_tri = {}
        with open(POS_TRIGRAMS_FILE, 'r', encoding='utf-8') as POS_tri:
            for tri in POS_tri:
                tri_freq = tri.split(",")
                pos_tri[tri_freq[0]] = tri_freq[1]
        self.POS_trigrams_list = list(pos_tri.keys())
        # print(len(self.POS_trigrams_list))

    def createFunctionWordList(self):
        with open(self.function_words_file, 'r', encoding='utf-8') as func_words:
            self.function_words_list = set([word.strip() for word in func_words])
        # print(len(self.function_words_list))

    def Tokenize(text):
        return text.split(' ')

    def createFeatureVectorsLazy(self, input_dir, label, chunks_record, flat_list=False, chunks=True):
        function_words_vectorizer = CountVectorizer(token_pattern=r"[a-z]*'[a-z]*|(?u)\b\w\w+\b|...|.|!|\?|\"|\'",
                                                    vocabulary=self.function_words_list)
        POS_vectorizer = CountVectorizer(ngram_range=(3, 3), vocabulary=self.POS_trigrams_list, stop_words=None,
                                         tokenizer=BinaryNLIClassifier.Tokenize, lowercase=False)
        function_word_feature_vector = []
        POS_feature_vector = []
        text = []

        for f in os.listdir(input_dir):
            with open(os.path.join(input_dir, f), 'rb') as fh:
                text.append(pickle.load(fh))
                if flat_list:
                    text = [item for sublist in text for item in sublist]
        text = [item for sublist in text for item in sublist]
        shuffle(text)
        text = [s.split(BEGIN_SENTENCE)[1] for s in text]
        chunk = 0
        token_counter = 0
        lemmas = {}
        pos = {}
        lemmas[chunk] = []
        pos[chunk] = []
        pos_seq = ""
        lemmas_seq = ""
        for sentence in text:
            sentence = sentence.strip()
            if len(sentence) > 0 and chunks and token_counter >= CHUNK_SIZE:
                lemmas[chunk].append(lemmas_seq)
                pos[chunk].append(pos_seq)
                chunks_record.append("{}_{}".format(os.path.basename(os.path.normpath(input_dir)), chunk))
                chunk += 1
                pos[chunk] = []
                lemmas[chunk] = []
                token_counter = 0
                pos_seq = ""
                lemmas_seq = ""

            token_counter += len(sentence.split(" "))
            # print(token_counter)
            pos_seq += BEGIN_SENTENCE + " "
            for token in sentence.split(" "):
                try:
                    lemma_pos = token.split(SEPERATOR)
                    lemmas_seq += lemma_pos[0] + " "
                    pos_seq += lemma_pos[1] + " "
                    lemmas_seq += ' '

                except:
                    continue
            pos_seq += END_SENTENCE + ' '

        if not chunks:
            lemmas[chunk].append(lemmas_seq)
            pos[chunk].append(pos_seq)
            chunks_record.append("{}_{}".format(f, chunk))
            chunk += 1

        for index in range(chunk):
            if len(lemmas[index]) == 0:
                continue
            # print(index)
            function_word_feature_vector.append(function_words_vectorizer.fit_transform(lemmas[index]))
            POS_feature_vector.append(POS_vectorizer.fit_transform(pos[index]))
            with open(os.path.join(TOEFL_DEBUG, "{}_{}".format(f, index)), 'w', encoding='utf-8') as chunk_out:
                for sent in lemmas[index]:
                    # sent = (sent.split(END_SENTENCE)[0]).strip()

                    chunk_out.write(sent + "\n")
            # print(pos[index])
            # print(POS_feature_vector[index])
            # print(lemmas[index])
            # print(function_word_feature_vector[index])
            # print(len(function_word_feature_vector))

        # break
        print("chunk = {}".format(chunk))
        result_func_words = vstack(function_word_feature_vector)
        result_POS_trigrams = vstack(POS_feature_vector)
        final_feature_vecotr_structure = hstack([result_func_words, result_POS_trigrams], format='csr')
        # final_feature_vecotr_structure = result_POS_trigrams
        # final_feature_vecotr_structure = result_func_words
        tf_idf_transformer = TfidfTransformer()
        tf_idf_transformer.fit(final_feature_vecotr_structure)
        tf_idf_transformer.transform(final_feature_vecotr_structure)
        labels = [label] * final_feature_vecotr_structure.shape[0]
        return final_feature_vecotr_structure, labels

    def balanceClassWithSMOTE(self):
        oversample = SMOTE()
        self.X, self.y = oversample.fit_resample(self.X, self.y)

    def createFeatureVectors(self, native_source_dir, native_pos_dir, non_native_source_dir, non_native_pos_dir):
        contents = self.non_natives + self.natives

        function_word_dataset = [os.path.join(non_native_source_dir, f) for f in self.non_natives]
        function_word_dataset.extend([os.path.join(native_source_dir, f) for f in self.natives])
        pos_trigrams_dataset = [os.path.join(non_native_pos_dir, f) for f in self.non_natives]
        pos_trigrams_dataset.extend([os.path.join(native_pos_dir, f) for f in self.natives])
        print(len(function_word_dataset))
        print(len(pos_trigrams_dataset))
        # print(len(contents))
        function_word_vectorizer = TfidfVectorizer(input='filename',
                                                   token_pattern=r"[a-z]*'[a-z]*|(?u)\b\w\w+\b|...|.|!|\?|\"|\'",
                                                   vocabulary=self.function_words_list)
        pos_tri_vectorizer = TfidfVectorizer(input='filename', ngram_range=(3, 3))

        function_word_X = function_word_vectorizer.fit_transform(function_word_dataset)
        pos_tri_X = pos_tri_vectorizer.fit_transform(pos_trigrams_dataset)
        print(function_word_X.shape)
        print(pos_tri_X.shape)
        self.X = sp.hstack([function_word_X, pos_tri_X], format='csr')
        print("X:")
        print(self.X.shape)

        self.y = [NON_NATIVE] * len(self.non_natives) + [NATIVE] * len(self.natives)
        self.balanceClassWithSMOTE()

    def createFunctionWordFeatureVectors(self, contents, labels):
        function_word_vectorizer = TfidfVectorizer(input='filename',
                                                   token_pattern=r"[a-z]*'[a-z]*|(?u)\b\w\w+\b|...|.|!|\?|\"|\'",
                                                   vocabulary=self.function_words_list)
        self.X = function_word_vectorizer.fit_transform(contents)
        self.y = labels

    def splitDataAndClassify(self, external_test=[]):
        fold = 0
        sss = StratifiedShuffleSplit(n_splits=SPLITS, test_size=TEST_SIZE, random_state=0)
        for train_index, test_index in sss.split(self.X, self.y):
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.y[train_index], self.y[test_index]
            clf = self.classifier.fit(X_train, y_train)
            print("accuracy: = {}".format(clf.score(X_test, y_test)))
            y_pred = self.classifier.predict(X_test)
            print("f1 = {}".format(f1_score(y_test, y_pred, average='micro')))

            i = 0
            self.non_natives_user_to_distance_from_border_line[fold] = {}

            print("writing dict")
            for i in range(len(self.non_natives)):
                self.non_natives_user_to_distance_from_border_line[fold][self.non_natives[i]] = []
                fv = self.X.getrow(i)
                self.non_natives_user_to_distance_from_border_line[fold][self.non_natives[i]].append(
                    [self.classifier.decision_function(fv)])
                self.non_natives_user_to_distance_from_border_line[fold][self.non_natives[i]].append(
                    [self.classifier.predict(fv)])
                # print(self.classifier.predict_proba(fv))
            # print(len(self.non_natives_user_to_distance_from_border_line[fold].keys()))
            start = len(self.non_natives)
            i = 0
            self.natives_user_to_distance_from_border_line[fold] = {}
            for i in range(len(self.natives)):
                self.natives_user_to_distance_from_border_line[fold][self.natives[i]] = []
                fv = self.X.getrow(i + start)
                self.natives_user_to_distance_from_border_line[fold][self.natives[i]].append(
                    [self.classifier.decision_function(fv)])
                self.natives_user_to_distance_from_border_line[fold][self.natives[i]].append(
                    [self.classifier.predict(fv)])
            fold += 1



def Main():
    non_native_df = pd.read_csv(TOEFL_STAT)
    # print(len(non_natives_df))
    # non_native_df = pd.read_csv(HEC_NON_NATIVE_META_DATA)
    # levels = list(non_native_df['level'].unique())
    # levels = ['high', 'low']
    # levels = [str(x).split(".0")[0] for x in levels]
    levels = list(non_native_df['Score Level'].unique())
    # levels = ["A", "B", "C"]
    binNLI_clf = BinaryNLIClassifier()

    X_non_native = []
    y_non_native = []
    #
    for lvl in levels:
        print("level = {}".format(lvl))
        # lvl_dir = os.path.join(TOEFL_FRA_LEMMAS_POS, os.path.join(lvl))
        # lvl_dir = os.path.join(HEC_NON_NATIVE_LEMMAS_POS, lvl)
        # lvl_dir = os.path.join(HEC_NON_NATIVE_LEMMAS_POS, os.path.join(lvl))
        lvl_dir = os.path.join(TOEFL_LEMMAS_POS, os.path.join(lvl))
        print(lvl_dir)
        X_non_native_curr_lvl, y_non_native_curr_lvl = binNLI_clf.createFeatureVectorsLazy(lvl_dir, NON_NATIVE,
                                                                                           binNLI_clf.non_natives,
                                                                                           flat_list=False, chunks=True)
        X_non_native.append(X_non_native_curr_lvl)
        print(X_non_native_curr_lvl.shape)
        y_non_native.append(y_non_native_curr_lvl)


    # print(non_natives['high'])
    y_non_native = [item for sublist in y_non_native for item in sublist]
    X_non_native_fv = vstack(X_non_native)

    # non_natives_dir = ICLE_GERMANIC_LEMMAS_POS
    # X_non_native, y_non_native = binNLI_clf.createFeatureVectorsLazy(non_natives_dir, NON_NATIVE,
    #                                                                  binNLI_clf.non_natives, flat_list=False,
    #                                                                  chunks=False)
    natives_dir = os.path.join(LOCNESS_LEMMAS_POS, 'unified')
    # natives_dir = HEC_NATIVE_LEMMAS_POS
    # natives_dir = HEC_NATIVE_LEMMAS_POS
    X_nativ, y_native = binNLI_clf.createFeatureVectorsLazy(natives_dir, NATIVE, binNLI_clf.natives, flat_list=True,
                                                            chunks=True)

    print(len(y_native))
    print(len(y_non_native))
    binNLI_clf.X = vstack((X_non_native_fv, X_nativ))
    # binNLI_clf.X = vstack((X_non_native, X_nativ))
    binNLI_clf.y = np.array(y_non_native + y_native)
    print(binNLI_clf.X.shape)
    print(binNLI_clf.y.shape)
    binNLI_clf.balanceClassWithSMOTE()
    print(binNLI_clf.X.shape)
    print(binNLI_clf.y.shape)

    external_test = []
    binNLI_clf.splitDataAndClassify(external_test)

    for fold in range(SPLITS):
        non_natives = {}
        for key, val in binNLI_clf.non_natives_user_to_distance_from_border_line[fold].items():
            non_natives[key] = val[0][0][0]
        data = {'User': list(non_natives.keys()),
                'Distance': list(non_natives.values()),
                'grade': [x.split('_')[0] for x in non_natives.keys()]}
        #
        # df = pd.DataFrame(data)
        print('writing csv')





if __name__ == '__main__':
    Main()
