# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 11:10:22 2020

@author: liatn
"""


from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split, cross_validate, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
import pandas as pd
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
# import shutil
# from lexicalrichness import LexicalRichness
import os
import pickle
# from nltk.corpus import words
# import stanza
REDDIT_GERMANIC_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/NoBound/"

REDDIT_ROMANCE_DATASET = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\over2000"
REDDIT_NATIVE_DATASET = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Native\over2000"
REDDIT_GERMANIC_DATASET = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Germanic\over2000"


REDDIT_GERMANIC_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/shuffeldChunksOver2000/"
REDDIT_ROMANCE_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/complete_users_toy/"
REDDIT_NATIVE_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/complete_users_toy/"
REDDIT_ROMANCE_POS_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/complete_users_POS_TagToy/"
REDDIT_NATIVE_POS_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/complete_users_POS_TagToy/"

# REDDIT_NATIVE_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Native\lemmas_pos_over_2000"
# REDDIT_ROMANCE_LEMMAS_POS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\lemmas_pos_over_2000"
REDDIT_NATIVE_LEMMAS_POS = r"/data/home/univ/lnativ1/RedditData/Native/lemmas_pos_over_2000/"
REDDIT_ROMANCE_LEMMAS_POS = r"/data/home/univ/lnativ1/RedditData/Romance/lemmas_pos_over_2000/"
REDDIT_GERMANIC_LEMMAS_POS = r"/data/home/univ/lnativ1/RedditData/Germanic/lemmas_pos_over_2000/"


# FUNCTION_WORDS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\function-words.csv"
# POS_TRIGRAMS_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\POS_trigrams.txt"

FUNCTION_WORDS = r"/data/home/univ/lnativ1/RedditData/function-words.csv"
POS_TRIGRAMS_FILE = r"/data/home/univ/lnativ1/RedditData/POS_trigrams.txt"

TOEFL_INDEX = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\index.csv"
TOEFL_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text"
TOEFL_ESSEYS = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\tokenized"
TOEFL_STAT = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\stat.csv"
LOCNESS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\texts"

TOEFL_SHUFFELED_CHUNKS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\shuff_grade_aggr"
TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\shuff_grade_aggr\balanced"
LOCNESS_SHUFFELED_CHUNKS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\shuff"
CHUNK_SIZE = 2000
NUMBER_OF_BINS = 5
BEGIN_SENTENCE = "<s>"
END_SENTENCE = "</s>"
SEPERATOR = "_"
TRI = 3
TOP_POS_TRIGRAMS = 500
NATIVE = 1
NON_NATIVE = 0

COGNATES_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list.csv"
SYNSET_ORIGIN = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list_with_origin.csv'
class BinaryNLIClassifier:
    
    def __init__(self):
        self.classifier = LogisticRegression(penalty='l2', dual=True, solver='liblinear',warm_start=True, C=10.0 )

        #self.classifier = svm.SVC()
        self.function_words_file = FUNCTION_WORDS
        self.function_words_list =[]
        self.non_natives = []
        self.natives = []
        self.non_natives_user_to_distance_from_border_line = {}
        self.natives_user_to_distance_from_border_line = {}
        self.createFunctionWordList()
        self.create_pos_trigram_list()
        # self.createFeatureVectors()
        # self.splitDataAndClassify()



    def create_pos_trigram_list(self):

        with open(POS_TRIGRAMS_FILE, 'r', encoding='utf-8') as POS_tri:
            self.POS_trigrams_list = [tri.strip() for tri in POS_tri]
        # print(self.POS_trigrams_list)
    def createFunctionWordList(self):
        with open(self.function_words_file, 'r') as func_words:
           self.function_words_list = [word.strip() for word in func_words]
        # print(self.function_words_list)

    def Tokenize(text):
        return text.split(' ')

    def createFeatureVectorsLazy(self, INPUT_DIR, label, chunks_record):
        function_words_vectorizer = CountVectorizer(token_pattern=r"[a-z]*'[a-z]*|(?u)\b\w\w+\b|...|.|!|\?|\"|\'",
                                                    vocabulary=self.function_words_list)
        POS_vectorizer = CountVectorizer(ngram_range=(3,3), vocabulary=self.POS_trigrams_list, stop_words=None,
                                         tokenizer=BinaryNLIClassifier.Tokenize, lowercase=False)
        function_word_feature_vector = []
        POS_feature_vector = []
        for f in os.listdir(INPUT_DIR):
            print(f)
            with open(os.path.join(INPUT_DIR, f), 'rb') as fh:
                text = pickle.load(fh)
                shuffle(text)
                text = [s.split(BEGIN_SENTENCE)[1] for s in text]
                text = [s.split(END_SENTENCE)[0] for s in text]
                chunk = 0
                token_counter = 0
                lemmas = {}
                pos = {}
                lemmas[chunk] = []
                pos[chunk] = []
                pos_seq = ""
                lemmas_seq = ""
                for sentence in text:
                    if token_counter >= CHUNK_SIZE:
                        # print(token_counter)
                        lemmas[chunk].append(lemmas_seq)
                        pos[chunk].append(pos_seq)
                        chunks_record.append("{}_{}".format(f, chunk))
                        chunk += 1
                        pos[chunk] = []
                        lemmas[chunk] = []
                        token_counter = 0
                        pos_seq = ""
                        lemmas_seq = ""

                    sentence = sentence.strip()
                    token_counter += len(sentence.split(" "))
                    pos_seq += BEGIN_SENTENCE + " "
                    for token in sentence.split(" "):
                        lemma_pos = token.split(SEPERATOR)
                        lemmas_seq += lemma_pos[0] + " "
                        pos_seq += lemma_pos[1] + " "
                    lemmas_seq += ' '
                    pos_seq += END_SENTENCE + ' '

                #last chunk may be smaller than defined size, if so - ignore it
                # if token_counter < CHUNK_SIZE:
                #     pos.pop(chunk)
                #     lemmas.pop(chunk)

            for index in range(chunk):
                if len(lemmas[index]) == 0:
                    continue
                # print(index)
                function_word_feature_vector.append(function_words_vectorizer.fit_transform(lemmas[index]))
                POS_feature_vector.append(POS_vectorizer.fit_transform(pos[index]))
                # print(pos[index])
                # print(POS_feature_vector[index])
                # print(lemmas[index])
                # print(function_word_feature_vector[index])
                # print(len(function_word_feature_vector))


        result_func_words = vstack(function_word_feature_vector)
        result_POS_trigrams = vstack(POS_feature_vector)
        final_feature_vecotr_structure = hstack([result_func_words, result_POS_trigrams], format='csr')
        # final_feature_vecotr_structure = result_POS_trigrams
        tf_idf_transformer = TfidfTransformer()
        tf_idf_transformer.fit(final_feature_vecotr_structure)
        tf_idf_transformer.transform(final_feature_vecotr_structure)
        labels = [label] * final_feature_vecotr_structure.shape[0]
        return final_feature_vecotr_structure, labels


    def balanceClassWithSMOTE(self):
        oversample = SMOTE()
        self.X, self.Y = oversample.fit_resample(self.X, self.Y)
               
    def createFeatureVectors(self, native_source_dir, native_pos_dir, non_native_source_dir, non_native_pos_dir):
        contents = self.non_natives+self.natives

        function_word_dataset = [os.path.join(non_native_source_dir, f) for f in self.non_natives]
        function_word_dataset.extend([os.path.join(native_source_dir, f) for f in self.natives])
        pos_trigrams_dataset = [os.path.join(non_native_pos_dir, f) for f in self.non_natives]
        pos_trigrams_dataset.extend([os.path.join(native_pos_dir, f) for f in self.natives])
        print(len(function_word_dataset))
        print(len(pos_trigrams_dataset))
        # print(len(contents))
        function_word_vectorizer = TfidfVectorizer(input='filename',token_pattern=r"[a-z]*'[a-z]*|(?u)\b\w\w+\b|...|.|!|\?|\"|\'",vocabulary=self.function_words_list)
        pos_tri_vectorizer = TfidfVectorizer(input='filename', ngram_range=(3, 3))

        function_word_X = function_word_vectorizer.fit_transform(function_word_dataset)
        pos_tri_X = pos_tri_vectorizer.fit_transform(pos_trigrams_dataset)
        print(function_word_X.shape)
        print(pos_tri_X.shape)
        self.X = sp.hstack([function_word_X, pos_tri_X], format='csr')
        print("X:")
        print(self.X.shape)

        self.Y = [NON_NATIVE]*len(self.non_natives) + [NATIVE]*len(self.natives)
        self.balanceClassWithSMOTE()


        scoring = {'accuracy' : make_scorer(accuracy_score),
           'f1_score' : make_scorer(f1_score)}
        kfold = StratifiedKFold(n_splits=10)
        results = cross_validate(estimator=self.classifier,
                                          X=self.X,
                                          y=self.Y,
                                          cv=kfold,
                                          scoring=scoring,
                                           return_train_score=False)
        print("accuracy: {}".format(np.mean(results['test_accuracy'])))
        print("f1: {}".format(np.mean(results['test_f1_score'])))
        scores = cross_val_score(self.classifier, self.X, self.Y, cv=10)
        print(scores)
        # print(np.mean(scores))
        # print((self.X).shape)
        
        # # i = 0
        # # for i in range(len(self.non_natives)-1):
        # #      print(self.X.getrow(i))
        # #      i+=1
        
    def createFunctionWordFeatureVectors(self):
        contents = self.non_natives + self.natives
        function_word_vectorizer = TfidfVectorizer(input='filename',
                                                   token_pattern=r"[a-z]*'[a-z]*|(?u)\b\w\w+\b|...|.|!|\?|\"|\'",
                                                   vocabulary=self.function_words_list)
        self.X = function_word_vectorizer.fit_transform(contents)
        self.Y = [NON_NATIVE] * len(self.non_natives) + [NATIVE] * len(self.natives)



    def splitDataAndClassify(self, external_test):
         X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.1, random_state=0)
         clf = self.classifier.fit(X_train,y_train)
         print("accuracy: = {}".format(clf.score(X_test, y_test)))
         y_pred = self.classifier.predict(X_test)
         print("f1 = {}".format(f1_score(y_test,y_pred)))
          # i = 0
         chunks_to_dist = {}
         if len(external_test) > 0:
             # with open("low_vs_high_med_as_test.csv",'w', encoding='utf-8') as rf:
             with open("agr_high_vs_med_low_as_test.csv",'w', encoding='utf-8') as arf:    
                 # rf.write("chunk, class(0-low;1-high),distance,ttr, unique\n")
                 arf.write("aggregated_ranked_group,distance,ttr, unique\n")
                 for i in range(len(external_test)):
                     y = self.ext_y.getrow(i)                         
                     chunk = (external_test[i].split("shuff_grade_aggr/",1)[1]) 
                     chunks_to_dist[external_test[i]] = self.classifier.decision_function(y)[0]
                     # with open(external_test[i],'r', encoding='utf-8') as chunk_file:                             
                     #     content = chunk_file.read().lower().split(" ")              
                     #     ttr = len(content) / len(set(content))
                     #     unique_words = len(set(content))
                     #     rf.write("{},{},{},{},{}\n".format(chunk,(self.classifier.predict(y)[0]),self.classifier.decision_function(y)[0],ttr,unique_words))
                 chunks_to_dist_sorted =OrderedDict(sorted(chunks_to_dist.items(), key=lambda x: x[1]))
                 
                 text = ""
                 i = 0
                 distances = []
                 group = 1
                 counter = 1
                 percentile = len(chunks_to_dist_sorted)/10
                 for chunk,dist in chunks_to_dist_sorted.items():
                    
                    if i < percentile:
                        with open(chunk, 'r', encoding='utf-8') as cf:
                            text += cf.read().lower()
                            distances.append(dist)
                            i += 1
                            # print("{} : text length: {}".format(i,len(text.split(" "))))
                    if i >=percentile or counter == len(chunks_to_dist_sorted):
                        print(counter)
                        content = text.split(" ")
                        ttr = len(content) / len(set(content))
                        unique_words = len(set(content))
                        arf.write("{},{},{},{}\n".format(group,np.mean(distances),ttr,unique_words))
                        group += 1
                        text = ""
                        i = 0
                        distances = []
                    counter +=1
                    
                     
         
            
         i = 0
         print("writing dict")
         for i in range(len(self.non_natives)):
             self.non_natives_user_to_distance_from_border_line[self.non_natives[i]] = []
             fv = self.X.getrow(i)
             self.non_natives_user_to_distance_from_border_line[self.non_natives[i]].append(
                 [self.classifier.decision_function(fv)])
             self.non_natives_user_to_distance_from_border_line[self.non_natives[i]].append(
                 [self.classifier.predict(fv)])
             # print(self.classifier.predict_proba(fv))
         print(len(self.non_natives_user_to_distance_from_border_line.keys()))
         start = len(self.non_natives)
         i = 0
         for i in range(len(self.natives)):
             self.natives_user_to_distance_from_border_line[self.natives[i]] = []
             fv = self.X.getrow(i+start)
             self.natives_user_to_distance_from_border_line[self.natives[i]].append(
                 [self.classifier.decision_function(fv)])
             self.natives_user_to_distance_from_border_line[self.natives[i]].append(
                 [self.classifier.predict(fv)])
                  
             
         # with open('TOEFL_non_natives_distances.csv','w+',encoding='utf-8') as nndist:
         #      nndist.write("user,distance\n")
         #      for key,value in self.non_natives_user_to_distance_from_border_line.items():
         #          user = (key.split("BinClsf/",1)[1])
         #          nndist.write("{},{}\n".format(user,value))
                 
         # with open('TOEFL_natives_distances.csv','w+',encoding='utf-8') as nativedist:
         #      nativedist.write("user,distance\n")
         #      for key,value in self.natives_user_to_distance_from_border_line.items():
         #          # user = (key.split("Balanced/",1)[1]).split(".",1)[0]
         #          nativedist.write("{},{}\n".format(key,value))
                
             
              
         # print(scores)
         # print( np.mean(scores))
   
       
                
def calc_num_of_words_and_sentences(text, nlp):  

    word_count = 0
    sent_count = 0
    types = []
    for line in text:
        line = line.strip()
        if len(line) > 0:
            doc = nlp(line)
            sent_count += 1
            word_count += len(line.split(" ")) 
            for sentence in doc.sentences:
                for word in sentence.words:
                    if word.lemma not in types:
                        types.append(word.lemma)
    return word_count, sent_count, len(types)
                    
                
    
def create_TOEFL_scrumbled_chunks(chunk_size):
    lemmatizer = WordNetLemmatizer() 
    TOEFL_df = pd.read_csv(TOEFL_STAT)
    L1_to_level_data = {}
    level_to_text = {}
    L1s = TOEFL_df.Language.unique()
    grades = TOEFL_df["Score Level"].unique()
    print(grades)
    print(L1s)

    for l1 in L1s:
        L1_to_level_data[l1] = {}
        for grade in grades:
            L1_to_level_data[l1][grade] = []
    for grade in grades:
        level_to_text[grade] = []
    for index, row in TOEFL_df.iterrows():
        with open (TOEFL_ESSEYS + row['Filename'],'r',encoding='utf-8')as f:
            # print(f)
            for line in f:
                line = line.strip()
                if len(line) > 0:
                    lemmatized_line = []
                    for word in line.split(" "):
                        lemmatized_line.append(lemmatizer.lemmatize(word))
                    L1_to_level_data[row['Language']][row['Score Level']].append(" ".join(lemmatized_line))
                    level_to_text[row['Score Level']].append(" ".join(lemmatized_line))
                    # L1_to_level_data[row['Language']][row['Score Level']].append(line)
                    
    for grade,text in level_to_text.items():
       print("level: {}, text size = {}".format(grade,len(text)))
       shuffle(text)
       i = 0
       chunk_num = 0
       chunk = []
       for line in text:
            chunk.append(line)
            i += len(line.split(" "))
            if (i > CHUNK_SIZE):
                with open(TOEFL_SHUFFELED_CHUNKS_PATH + grade + "_" + str(chunk_num) + ".txt", 'w', encoding='utf-8') as cf:
                    for line in chunk:
                        cf.write(line + "\n")
                i = 0
                chunk_num += 1
                chunk.clear()

                
def create_LOCNESS_scrumbled_chunks(chunk_size):
    lemmatizer = WordNetLemmatizer() 
    natives = [f for f in os.listdir(LOCNESS_PATH) if f.endswith('.txt')]
    sentences = []
    for f in natives:
        with open(LOCNESS_PATH + f,'r',encoding='utf-8') as nf:
            for line in nf:
                line = line.strip()
                if len(line) > 0:
                    line_sent = sent_tokenize(line)
                    
                    for s in line_sent:
                        lemmatized_line = []
                        for word in word_tokenize(s):
                            lemmatized_line.append(lemmatizer.lemmatize(word))
                        sentences.append(" ".join(lemmatized_line))
    shuffle(sentences)
    i = 0
    chunk_num = 0
    chunk = []
    for line in sentences:
        chunk.append(line)
        i += len(line.split(" "))
        if (i > CHUNK_SIZE):
            with open(LOCNESS_SHUFFELED_CHUNKS_PATH + str(chunk_num) + ".txt", 'w', encoding='utf-8') as cf:
                for line in chunk:
                    cf.write(line + "\n")
            i = 0
            chunk_num += 1
            chunk.clear()
                
                
        
        
    
     
            

def load_TOEFL_LOCNESS():
    
    TOEFL_df = pd.read_csv(TOEFL_INDEX)
    
    natives = [f for f in os.listdir(LOCNESS_PATH) if f.endswith('.txt')]
    natives_num = len(natives)
    non_natives_df = pd.DataFrame()
    print(natives_num)  
    
    grades = TOEFL_df.Grade.unique()
    sample_size = int(natives_num/len(grades))
    grade_to_size = dict(zip(grades, [sample_size,sample_size+1,sample_size]))  
    print(grade_to_size)
    print(grades)
    
    print(sample_size)
    for grade,size in grade_to_size.items():
        x = (TOEFL_df.loc[((TOEFL_df['L1']=='GER') | (TOEFL_df['L1']=='SPA') | (TOEFL_df['L1']=='ITA')) & (TOEFL_df['Grade']==grade)]).sample(n=size)  
        print(len(x))
        non_natives_df = non_natives_df.append(x)
        print(len(non_natives_df))
        
        
    return natives,non_natives_df

def Main():
    # TOEFL_df = pd.read_csv(TOEFL_INDEX)
    # # print(TOEFL_df)
    # highs = (TOEFL_df.loc[(TOEFL_df['Score Level']=='high')])['Filename']
    # lens = {}
    # lens['high']=[]
    # lens['med']=[]
    # lens['low']=[]
    # for f in highs:
    #     f= os.path.join(TOEFL_ESSEYS,f)
    #     with open(f, 'r') as hf:
            
    #         (lens['high']).append(len(hf.read().split(' ')))
   
    # meds = (TOEFL_df.loc[(TOEFL_df['Score Level']=='medium')])['Filename']
    # for f in meds:
    #     f= os.path.join(TOEFL_ESSEYS,f)
    #     with open(f, 'r') as hf:
    #         lens['med'].append(len(hf.read().split(' ')))
            
    # lows = (TOEFL_df.loc[(TOEFL_df['Score Level']=='low')])['Filename']
    # for f in lows:
    #     f= os.path.join(TOEFL_ESSEYS,f)
    #     with open(f, 'r') as hf:
    #         lens['low'].append(len(hf.read().split(' ')))
    
    
    # with open('lens.csv','w',encoding='utf-8') as len_file:
    #     len_file.write("level, length\n")
    #     for lvl,lens in lens.items():            
    #         for l in lens:
    #             len_file.write("{},{}\n".format(lvl,l))
    
    # # print(highs)
    # return
   


   #### REDDIT POS_LEMMAS LAZY FV CONSTRUCTION

    binNLI_clf = BinaryNLIClassifier()

    X_non_native, y_non_native = binNLI_clf.createFeatureVectorsLazy(REDDIT_ROMANCE_LEMMAS_POS, NON_NATIVE, binNLI_clf.non_natives)
    X_nativ, y_native = binNLI_clf.createFeatureVectorsLazy(REDDIT_NATIVE_LEMMAS_POS, NATIVE, binNLI_clf.natives)
    print(X_nativ.shape)
    print(X_non_native.shape)
    binNLI_clf.X = vstack((X_nativ,X_non_native))
    binNLI_clf.Y = y_native + y_non_native

    # binNLI_clf.natives = [os.path.join(REDDIT_NATIVE_DATASET, f) for f in os.listdir(REDDIT_NATIVE_DATASET)]
    # binNLI_clf.non_natives = [os.path.join(REDDIT_ROMANCE_DATASET, f) for f in os.listdir(REDDIT_ROMANCE_DATASET)]
    # binNLI_clf.createFunctionWordFeatureVectors()

    binNLI_clf.balanceClassWithSMOTE()
    print(binNLI_clf.X.shape)

    external_test = []
    for i in range(3):
        binNLI_clf.splitDataAndClassify(external_test)
    # print(len(binNLI_clf.non_natives_user_to_distance_from_border_line))

        true_non_natives = {}
        false_natives = {}
        for key, val in binNLI_clf.non_natives_user_to_distance_from_border_line.items():
            if val[1][0] != NON_NATIVE:
                true_non_natives[key] = val[0][0][0]
            else:
                false_natives[key] = val[0][0][0]

        bins = NUMBER_OF_BINS - 1 - pd.qcut(np.array(list(true_non_natives.values())), NUMBER_OF_BINS, labels=False)

        data = {'User': list(true_non_natives.keys()) + list(false_natives.keys()),
                'Distance': list(true_non_natives.values()) + list(false_natives.values()),
                'grade': list(bins) + [NUMBER_OF_BINS] * len(false_natives.keys())}

        df = pd.DataFrame(data)
        print('writing csv')
        filename = "fold_{}_romance_vs_natives_6_bins.csv".format(i)
        df.to_csv(filename)

    return
    
    
    
    # #### Reddit
    # binNLI_clf = BinaryNLIClassifier()
    #
    # binNLI_clf.natives = [f for f in os.listdir(REDDIT_NATIVE_CHUNKS)]
    # # binNLI_clf.natives = binNLI_clf.natives[1:100]
    # #germanic_users = [os.path.join(REDDIT_GERMANIC_CHUNKS,f) for f in os.listdir(REDDIT_GERMANIC_CHUNKS)]
    # romance_users = [f for f in os.listdir(REDDIT_ROMANCE_CHUNKS)]
    # binNLI_clf.non_natives =  romance_users
    #
    # # binNLI_clf.non_natives = binNLI_clf.non_natives[0:300]
    # # binNLI_clf.natives = sample(binNLI_clf.natives,len(binNLI_clf.non_natives))
    # print(len(binNLI_clf.non_natives))
    # print(len(binNLI_clf.natives))
    #
    # external_test = []
    # binNLI_clf.createFeatureVectors(external_test, REDDIT_NATIVE_CHUNKS, REDDIT_NATIVE_POS_CHUNKS, REDDIT_ROMANCE_CHUNKS, REDDIT_ROMANCE_POS_CHUNKS)
    #
    # binNLI_clf.splitDataAndClassify(external_test)
    # return
    # true_non_natives = {}
    # false_natives = {}
    # for key,val in binNLI_clf.non_natives_user_to_distance_from_border_line.items():
    #     if val[0][0] < 0:
    #         true_non_natives[key] = val[0][0]
    #     else:
    #         false_natives[key] = val[0][0]
    #
    # bins = pd.qcut(np.array(list(true_non_natives.values())),NUMBER_OF_BINS,labels=False)
    #
    #
    # data = {'User': list(true_non_natives.keys()) + list(false_natives.keys()),
    #         'Distance': list(true_non_natives.values()) + list(false_natives.values()),
    #         'grade': list(bins) + [NUMBER_OF_BINS] * len(false_natives.keys())}
    #
    # df = pd.DataFrame(data)
    # print('writing csv')
    # df.to_csv("complete_users_6_bins_log_reg_toy.csv")
    # return
    #
    #
    # # df.to_csv("reddit{}bins.csv".format(NUMBER_OF_BINS))
    # # native_cog_counter = RedditCognatesCounter(SYNSET_ORIGIN)
    #
    # bin_text_files = []
    # cog_cntr = RedditCognatesCounter(SYNSET_ORIGIN)
    # with open('results.csv','w',encoding='utf-8') as res_file:
    #     res_file.write("user, ger_ratio, rom_ratio, rttr\n")
    #     for i in range(NUMBER_OF_BINS + 1):
    #         bin_df = df[df['grade']==i]
    #         bin_text_files = bin_df['User'].to_list()
    #         # bin_text_files = [f.replace("Balanced","Final") for f in bin_text_files]
    #         # print(bin_text_files)
    #
    #
    #         with open("ger_bin{}.txt".format(i), "w", encoding='utf-8') as binOutfile:
    #              for f in bin_text_files:
    #                  with open(f, "r", encoding='utf-8') as infile:
    #                      binOutfile.write(infile.read())
    #         print("calculating ttr")
    #         with open("ger_bin{}.txt".format(i), "r", encoding='utf-8') as user_file:
    #             text = user_file.read()
    #             lex = LexicalRichness(str(text))
    #         print('counting cognates')
    #         user = RedditUser("ger_bin{}".format(i), "germanic")
    #         user.text_file = "ger_bin{}.txt".format(i)
    #         cog_cntr.count_cognates_for_user(user)
    #         user_df = cog_cntr.users_cognate_counts_dict[user]
    #         syn_list = list(set(user_df['synset']))
    #         synset_to_ger_ratio = {}
    #         synset_to_rom_ratio = {}
    #         for synset in syn_list:
    #             total = ((user_df[user_df.synset == synset])['count']).sum()
    #             if total == 0:
    #                 synset_to_ger_ratio[synset] = 0
    #                 synset_to_rom_ratio[synset] = 0
    #             else:
    #                 ger_total = ((user_df[(user_df.synset== synset) & (user_df.Source == 'G')])['count']).sum()
    #                 rom_total =  ((user_df[(user_df.synset== synset) & (user_df.Source == 'R')])['count']).sum()
    #                 synset_to_ger_ratio[synset] =(ger_total/total)
    #                 synset_to_rom_ratio[synset] =(rom_total/total)
    # # Ger_count = []
    # # print(ratios)
    #
    #     # print(np.mean(list(synset_to_ger_ratio.values())))
    #     # print(np.mean(list(synset_to_rom_ratio.values())))
    #
    #         res_file.write("ger_bin{}.txt,".format(i))
    #         res_file.write(str(np.mean(list(synset_to_ger_ratio.values()))))
    #         res_file.write(", ")
    #         res_file.write(str(np.mean(list(synset_to_rom_ratio.values()))))
    #         res_file.write(", ")
    #         res_file.write(str(lex.mattr(window_size=25)))
    #         res_file.write("\n")
    #
    #
    #
    #
    # # print(bin_text_files)
    #
    #
    # # with open('reddit_non_native_distances.csv','w+',encoding='utf-8') as reddit_dist:
    # #         reddit_dist.write("user,distance,prob,ttr\n")
    # #         for key,value in binNLI_clf.non_natives_user_to_distance_from_border_line.items():
    #
    # #             ttr = 0.0
    # #             with open(key,'r',encoding='utf-8') as text_file:
    # #                 content = text_file.read().split(" ")
    # #                 ttr = len(set(content)) / len(content)
    #
    # #             #
    # #             reddit_dist.write("{},{},{},{}\n".format(key,value[0][0],value[1][0][0] ,ttr))
    #
    # return
    # create_TOEFL_scrumbled_chunks(CHUNK_SIZE)
    # create_LOCNESS_scrumbled_chunks(CHUNK_SIZE)
    # return
    ######## TOEFL
    non_natives_df = pd.read_csv(TOEFL_STAT)

    # print(len(non_natives_df))

    # for i in range(5):
    #     binNLI_clf = BinaryNLIClassifier()
    #     binNLI_clf.natives = [os.path.join(LOCNESS_PATH, f) for f in os.listdir(LOCNESS_SHUFFELED_CHUNKS_PATH)]
    #
    #     lows = sample([os.path.join(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH, f) for f in os.listdir(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH) if "low" in f],int(len(binNLI_clf.natives)/3))
    #     meds = sample([os.path.join(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH, f) for f in os.listdir(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH) if "medium" in f],int((len(binNLI_clf.natives)/3)) + 1)
    #     highs = sample([os.path.join(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH, f) for f in os.listdir(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH) if "high" in f],int(len(binNLI_clf.natives)/3))
    #     print("lows: {} , meds: {}, highs: {}".format(len(lows),len(meds),len(highs)))
    #
    #     binNLI_clf.non_natives = lows + meds + highs
    #     print("non_natives: {}, natives: {}".format(len(binNLI_clf.non_natives),len(binNLI_clf.natives)))
    #     external_test = []
    # #
    #     # first = [TOEFL_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_SHUFFELED_CHUNKS_PATH) if "high" in f]
    #     # second =  [TOEFL_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_SHUFFELED_CHUNKS_PATH) if "medium" in f]
    #     # second = sample(second,len(first))
    #     # binNLI_clf.non_natives = first
    #     # binNLI_clf.natives = second
    #     # external_test = [TOEFL_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_SHUFFELED_CHUNKS_PATH) if "low" in f]
    #     binNLI_clf.createFunctionWordFeatureVectors()
    #     binNLI_clf.splitDataAndClassify(external_test)
    #
    #     # with open('TOEFL_non_natives_distances.csv','w+',encoding='utf-8') as nndist:
    #     #          nndist.write("user,distance,grade\n")
    #     #          for key,value in binNLI_clf.non_natives_user_to_distance_from_border_line.items():
    #     #              user = (key.split("shuff_grade_aggr/",1)[1])
    #     #              print(user)
    #     #              user_grade = (non_natives_df.loc[non_natives_df['Filename']==user])['Score Level'].values[0]
    #     #              # print(user_grade)
    #     #              nndist.write("{},{},{}\n".format(user,value[0],user_grade))
    # #
    #     with open(str(i) + 'SVM_TOEFL_level_1000_words_chunks_distances.csv','w+',encoding='utf-8') as chunks_dist:
    #         chunks_dist.write("file,grade,distance,ttr\n")
    #         for key,value in binNLI_clf.non_natives_user_to_distance_from_border_line.items():
    #             chunk = (key.split("balanced",1)[1])[1:]
    #             ttr = 0.0
    #             with open(key,'r',encoding='utf-8') as text_file:
    #                 content = text_file.read().split(" ")
    #                 ttr = len(content) / len(set(content))
    #
    #             grade = chunk.split("_",1)[0]
    #             chunks_dist.write("{},{},{},{}\n".format(chunk,grade,value[0][0],ttr))
    #


if __name__ == '__main__':
    Main()