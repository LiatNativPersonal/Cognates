# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 11:10:22 2020

@author: liatn
"""


from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split, cross_validate, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.utils import class_weight
import pandas as pd
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import OrderedDict
from collections import Counter
import string
from imblearn.over_sampling import SMOTE
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from RedditUser import RedditUser
from RedditCognatesCounter import RedditCognatesCounter
from scipy.sparse import coo_matrix, hstack
import scipy.sparse as sp
from sklearn import svm
import numpy as np
from random import sample, shuffle
from scipy.sparse import vstack
import shutil
from lexicalrichness import LexicalRichness
import os
from nltk.corpus import words
# import stanza
REDDIT_GERMANIC_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/NoBound/"
REDDIT_ROMANCE_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/NoBound/"
REDDIT_NATIVE_DATASET = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/NoBound/"
REDDIT_GERMANIC_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Germanic/shuffeldChunksOver2000/"
REDDIT_ROMANCE_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/complete_users_toy/"
REDDIT_NATIVE_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/complete_users_toy/"
REDDIT_ROMANCE_POS_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Romance/complete_users_POS_TagToy/"
REDDIT_NATIVE_POS_CHUNKS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/RedditData/Native/complete_users_POS_TagToy/"
FUNCTION_WORDS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/function-words.csv"
POS_TRIGRAMS_FILE = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/scripts/trigrams_toy_count.csv"
TOP_FREQUENT_POS_TRIGRAMS = 300

TOEFL_INDEX = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/ETS_Corpus_of_Non-Native_Written_English/data/text/index.csv"
TOEFL_PATH = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/ETS_Corpus_of_Non-Native_Written_English/data/text/"
TOEFL_ESSEYS = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/ETS_Corpus_of_Non-Native_Written_English/data/text/responses/tokenized/"
TOEFL_STAT = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/ETS_Corpus_of_Non-Native_Written_English/data/text/stat.csv"
LOCNESS_PATH = "c:/Users/liatn/Documents/Liat/Research//Repo/Cognates/LOCNESS/texts/"

TOEFL_SHUFFELED_CHUNKS_PATH = TOEFL_PATH + "shuff_grade_aggr/"
TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH = TOEFL_SHUFFELED_CHUNKS_PATH + "/balanced/"
LOCNESS_SHUFFELED_CHUNKS_PATH = "c:/Users/liatn/Documents/Liat/Research//Repo/Cognates/LOCNESS/shuff/"
CHUNK_SIZE = 500
NUMBER_OF_BINS = 5

COGNATES_LIST = "c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list.csv"
SYNSET_ORIGIN = 'c:/Users/liatn/Documents/Liat/Research/Repo/Cognates/combined_synset_list_with_origin.csv'
class BinaryNLIClassifier:
    
    def __init__(self):
        self.classifier = LogisticRegression(penalty='l2',dual=True, solver='liblinear', warm_start=True, C=10.0 )
        # self.classifier = svm.SVC()
        self.function_words_file = FUNCTION_WORDS
        self.function_words_list =[]
        self.non_natives = []
        self.natives = []
        self.non_natives_user_to_distance_from_border_line = {}
        self.natives_user_to_distance_from_border_line = {}
        self.createFunctionWordList()
        # self.create_pos_trigram_list()
        # self.createFeatureVectors()
        # self.splitDataAndClassify()
        

    def create_pos_trigram_list(self):
        pos_tri_df = pd.read_csv(POS_TRIGRAMS_FILE)
        most_frequent_pos = list(pos_tri_df.nlargest(TOP_FREQUENT_POS_TRIGRAMS, 'count')['pos_trigram'])
        self.pos_trigram_list = most_frequent_pos
        print(self.pos_trigram_list[1:10])
     
    def createFunctionWordList(self):
        with open(self.function_words_file, 'r') as func_words:
            for word in func_words: 
                self.function_words_list.append(word.strip())   
               
    def createFeatureVectors(self,external_test, native_source_dir, native_pos_dir, non_native_source_dir, non_native_pos_dir):
        contents = self.non_natives+self.natives

        function_word_dataset = [os.path.join(non_native_source_dir, f) for f in self.non_natives]
        function_word_dataset.extend([os.path.join(native_source_dir, f) for f in self.natives])
        pos_trigrams_dataset = [os.path.join(non_native_pos_dir, f) for f in self.non_natives]
        pos_trigrams_dataset.extend([os.path.join(native_pos_dir, f) for f in self.natives])
        print(len(function_word_dataset))
        print(len(pos_trigrams_dataset))
        # print(len(contents))
        function_word_vectorizer = TfidfVectorizer(input='filename',token_pattern=r"[a-z]*'[a-z]*|(?u)\b\w\w+\b|...|.|!|\?|\"|\'",vocabulary=self.function_words_list)
        pos_tri_vectorizer = TfidfVectorizer(input='filename', ngram_range=(3, 3) )
        # print(vectorizer.vocabulary)
        # if len(external_test) > 0:
        #     self.ext_y = vectorizer.fit_transform(external_test)

        function_word_X = function_word_vectorizer.fit_transform(function_word_dataset)
        pos_tri_X = pos_tri_vectorizer.fit_transform(pos_trigrams_dataset)
        print(function_word_X.shape)
        print(pos_tri_X.shape)
        self.X = sp.hstack([function_word_X, pos_tri_X], format='csr')
        # self.X = [function_word_X, pos_tri_X]
        # combined_features = FeatureUnion([('function_words', function_word_X), ('pos_tri', pos_tri_X)])
        # combined_features.transform(self.X)
        # self.X = pos_tri_X



        print("X:")
        print(self.X.shape)

        self.Y = [0]*len(self.non_natives) + [1]*len(self.natives)
        oversample = SMOTE()
        self.X, self.Y = oversample.fit_resample(self.X, self.Y)
       


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
        
    
    def splitDataAndClassify(self, external_test):
         X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.1, random_state=0)
         clf = self.classifier.fit(X_train,y_train)
         print(clf.score(X_test,y_test))
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
               fv = self.X.getrow(i)               
               self.non_natives_user_to_distance_from_border_line[self.non_natives[i]] = [self.classifier.decision_function(fv) ]
               # print(self.classifier.predict_proba(fv))
         print(len(self.non_natives_user_to_distance_from_border_line))
         start = len(self.non_natives)
         i = 0
         for i in range(len(self.natives)):             
               fv = self.X.getrow(i+start)
               self.natives_user_to_distance_from_border_line[self.natives[i]] = [self.classifier.decision_function(fv)]
                  
             
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
    doc = nlp(str(text))
    for line in text:
        line = line.strip()        
        # print(len(line))
        # print(line)
        # print(len(line.split(" ")))
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
    # nlp = stanza.Pipeline(lang='en', processors='tokenize,lemma')
    lemmatizer = WordNetLemmatizer() 
    TOEFL_df = pd.read_csv(TOEFL_STAT)
    L1_to_level_data = {}
    level_to_text = {}
    L1s = TOEFL_df.Language.unique()
    grades = TOEFL_df["Score Level"].unique()
    print(grades)
    print(L1s)
    
    # word_count = []
    # sent_count = []
    # types_count = []
    # i = 0
    # for file in TOEFL_df['Filename']:       
    #     with open(TOEFL_ESSEYS+file,'r',encoding='utf-8')as essay:
            # w_c,s_c,t_c = calc_num_of_words_and_sentences(essay,nlp)
            
            # print(  t_c)
            # word_count.append(w_c)
            # sent_count.append(s_c)
            # types_count.append(t_c)
            # i+=1
            # if i > 10 :
            #     break
    
    # print(len(word_count))
    # TOEFL_df['#token'] = word_count
    # TOEFL_df['#Sent'] = sent_count
    # TOEFL_df['#types'] = types_count
    # TOEFL_df.to_csv(TOEFL_PATH+'stat.csv')
    
    
    
    
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
                        
                    # print(" ".join(lemmatized_line))
                    L1_to_level_data[row['Language']][row['Score Level']].append(" ".join(lemmatized_line))
                    level_to_text[row['Score Level']].append(" ".join(lemmatized_line))
                    # L1_to_level_data[row['Language']][row['Score Level']].append(line)
                    
    for grade,text in level_to_text.items():
       print("level: {}, text size = {}".format(grade,len(text))) 
       # if grade != 'low':
       #     continue
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
            
            
    
    #aggrgate texts by bL1 and levl
    # for L1,level in L1_to_level_data.items():
    #     for lvl,text in level.items():
    #         print("{},{},{}".format(L1,lvl,len(text)))
    #         shuffle(text)
    #         with open(TOEFL_SHUFFELED_CHUNKS_PATH + L1+"_"+lvl+".txt",'w',encoding='utf-8') as of:
    #             for line in text:
    #                 of.write(line + "\n")
            
                
                
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
    # print(x.sample(n =20))
    # print(TOEFL_df.head(5))
    # print(TOEFL_df['L1'])




            
        
        





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
   
   
    
    
    
    # #### Reddit
    binNLI_clf = BinaryNLIClassifier()

    binNLI_clf.natives = [f for f in os.listdir(REDDIT_NATIVE_CHUNKS)]
    # binNLI_clf.natives = binNLI_clf.natives[1:100]
    #germanic_users = [os.path.join(REDDIT_GERMANIC_CHUNKS,f) for f in os.listdir(REDDIT_GERMANIC_CHUNKS)]
    romance_users = [f for f in os.listdir(REDDIT_ROMANCE_CHUNKS)]
    binNLI_clf.non_natives =  romance_users
    
    # binNLI_clf.non_natives = binNLI_clf.non_natives[0:300]
    # binNLI_clf.natives = sample(binNLI_clf.natives,len(binNLI_clf.non_natives))
    print(len(binNLI_clf.non_natives))
    print(len(binNLI_clf.natives))
    
    external_test = []
    binNLI_clf.createFeatureVectors(external_test, REDDIT_NATIVE_CHUNKS, REDDIT_NATIVE_POS_CHUNKS, REDDIT_ROMANCE_CHUNKS, REDDIT_ROMANCE_POS_CHUNKS)

    binNLI_clf.splitDataAndClassify(external_test)
    return
    true_non_natives = {}
    false_natives = {}
    for key,val in binNLI_clf.non_natives_user_to_distance_from_border_line.items():
        if val[0][0] < 0:
            true_non_natives[key] = val[0][0]
        else:
            false_natives[key] = val[0][0]
   
    bins = pd.qcut(np.array(list(true_non_natives.values())),NUMBER_OF_BINS,labels=False)
    

    data = {'User': list(true_non_natives.keys()) + list(false_natives.keys()),
            'Distance': list(true_non_natives.values()) + list(false_natives.values()),
            'grade': list(bins) + [NUMBER_OF_BINS] * len(false_natives.keys())}
    
    df = pd.DataFrame(data)
    print('writing csv')
    df.to_csv("complete_users_6_bins_log_reg_toy.csv")
    return
    
    
    # df.to_csv("reddit{}bins.csv".format(NUMBER_OF_BINS))
    # native_cog_counter = RedditCognatesCounter(SYNSET_ORIGIN)
    
    bin_text_files = []
    cog_cntr = RedditCognatesCounter(SYNSET_ORIGIN)
    with open('results.csv','w',encoding='utf-8') as res_file:
        res_file.write("user, ger_ratio, rom_ratio, rttr\n")
        for i in range(NUMBER_OF_BINS + 1):
            bin_df = df[df['grade']==i]
            bin_text_files = bin_df['User'].to_list()
            # bin_text_files = [f.replace("Balanced","Final") for f in bin_text_files]
            # print(bin_text_files)
            
            
            with open("ger_bin{}.txt".format(i), "w", encoding='utf-8') as binOutfile:
                 for f in bin_text_files:
                     with open(f, "r", encoding='utf-8') as infile:
                         binOutfile.write(infile.read())
            print("calculating ttr")
            with open("ger_bin{}.txt".format(i), "r", encoding='utf-8') as user_file:
                text = user_file.read()
                lex = LexicalRichness(str(text))
            print('counting cognates')   
            user = RedditUser("ger_bin{}".format(i), "germanic")
            user.text_file = "ger_bin{}.txt".format(i) 
            cog_cntr.count_cognates_for_user(user)
            user_df = cog_cntr.users_cognate_counts_dict[user]
            syn_list = list(set(user_df['synset']))
            synset_to_ger_ratio = {}
            synset_to_rom_ratio = {}
            for synset in syn_list:
                total = ((user_df[user_df.synset == synset])['count']).sum()
                if total == 0:
                    synset_to_ger_ratio[synset] = 0
                    synset_to_rom_ratio[synset] = 0
                else:
                    ger_total = ((user_df[(user_df.synset== synset) & (user_df.Source == 'G')])['count']).sum()
                    rom_total =  ((user_df[(user_df.synset== synset) & (user_df.Source == 'R')])['count']).sum()
                    synset_to_ger_ratio[synset] =(ger_total/total)
                    synset_to_rom_ratio[synset] =(rom_total/total)
    # Ger_count = []
    # print(ratios)
       
        # print(np.mean(list(synset_to_ger_ratio.values())))
        # print(np.mean(list(synset_to_rom_ratio.values())))
       
            res_file.write("ger_bin{}.txt,".format(i))
            res_file.write(str(np.mean(list(synset_to_ger_ratio.values()))))
            res_file.write(", ") 
            res_file.write(str(np.mean(list(synset_to_rom_ratio.values()))))
            res_file.write(", ") 
            res_file.write(str(lex.mattr(window_size=25)))
            res_file.write("\n")
        
        
        
    
    # print(bin_text_files)
    
    
    # with open('reddit_non_native_distances.csv','w+',encoding='utf-8') as reddit_dist: 
    #         reddit_dist.write("user,distance,prob,ttr\n")            
    #         for key,value in binNLI_clf.non_natives_user_to_distance_from_border_line.items():         
               
    #             ttr = 0.0
    #             with open(key,'r',encoding='utf-8') as text_file:
    #                 content = text_file.read().split(" ")                  
    #                 ttr = len(set(content)) / len(content)
                
    #             #  
    #             reddit_dist.write("{},{},{},{}\n".format(key,value[0][0],value[1][0][0] ,ttr))
    
    return 
    create_TOEFL_scrumbled_chunks(CHUNK_SIZE)
    create_LOCNESS_scrumbled_chunks(CHUNK_SIZE)
    return
    ######## TOEFL
    non_natives_df = pd.read_csv(TOEFL_STAT)
    
    # print(len(non_natives_df))
   
    for i in range(5):
        binNLI_clf = BinaryNLIClassifier()
        binNLI_clf.natives = [LOCNESS_PATH + f for f in os.listdir(LOCNESS_SHUFFELED_CHUNKS_PATH)]
       
        lows = sample([TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH) if "low" in f],int(len(binNLI_clf.natives)/3))
        meds = sample([TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH) if "medium" in f],int((len(binNLI_clf.natives)/3)) + 1)
        highs = sample([TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_BALANCED_SHUFFELED_CHUNKS_PATH) if "high" in f],int(len(binNLI_clf.natives)/3))
        print("lows: {} , meds: {}, highs: {}".format(len(lows),len(meds),len(highs)))
        
        binNLI_clf.non_natives = lows + meds + highs
        print("non_natives: {}, natives: {}".format(len(binNLI_clf.non_natives),len(binNLI_clf.natives)))
        external_test = []
        
        # first = [TOEFL_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_SHUFFELED_CHUNKS_PATH) if "high" in f]
        # second =  [TOEFL_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_SHUFFELED_CHUNKS_PATH) if "medium" in f]
        # second = sample(second,len(first))
        # binNLI_clf.non_natives = first
        # binNLI_clf.natives = second
        # external_test = [TOEFL_SHUFFELED_CHUNKS_PATH + f for f in os.listdir(TOEFL_SHUFFELED_CHUNKS_PATH) if "low" in f]
        binNLI_clf.createFeatureVectors(external_test)
        binNLI_clf.splitDataAndClassify(external_test) 
        
        # with open('TOEFL_non_natives_distances.csv','w+',encoding='utf-8') as nndist:
        #          nndist.write("user,distance,grade\n")
        #          for key,value in binNLI_clf.non_natives_user_to_distance_from_border_line.items():
        #              user = (key.split("shuff_grade_aggr/",1)[1])
        #              print(user)
        #              user_grade = (non_natives_df.loc[non_natives_df['Filename']==user])['Score Level'].values[0]
        #              # print(user_grade)
        #              nndist.write("{},{},{}\n".format(user,value[0],user_grade))
      
        with open(str(i) + '_TOEFL_level_1000_words_chunks_distances.csv','w+',encoding='utf-8') as chunks_dist: 
            chunks_dist.write("file,grade,distance,prob,ttr\n")            
            for key,value in binNLI_clf.non_natives_user_to_distance_from_border_line.items():            
                chunk = (key.split("balanced/",1)[1])
                ttr = 0.0
                with open(key,'r',encoding='utf-8') as text_file:
                    content = text_file.read().split(" ")                  
                    ttr = len(content) / len(set(content))
                
                grade = chunk.split("_",1)[0]
                chunks_dist.write("{},{},{},{},{}\n".format(chunk,grade,value[0][0],value[1][0][0],ttr))
        
    # for func_word in binNLI_clf.function_words_list:
    #     print(func_word)

if __name__ == '__main__':
    Main()