import pandas as pd
import spacy
import os

ICLE_META_DATA = r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\ICLE.csv'

metadata_df = pd.read_csv(ICLE_META_DATA)
# print(metadata_df.head())
filenames = list(metadata_df['File name'])
nlp = spacy.load('en_core_web_sm')
tokens = []
sentences = []
PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\texts"
# i = 0
for filename in filenames:
    # if i >= 1:
    #     break
    with open(os.path.join(PATH, filename + '.txt'), 'r', encoding='utf-8') as infile:
        print(filename)
        contents = infile.read()
        doc = nlp(contents)
        tokens.append(len(doc))
        sentences.append(len(list(doc.sents)))
        # i += 1
        # print(list(doc.sents))
metadata_df['sentences'] = sentences
metadata_df['tokens'] = tokens
metadata_df.to_csv(r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\ICLE_ext.csv')
