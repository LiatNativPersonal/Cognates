import os
import spacy
import csv
import pickle
from random import sample


SAMPLE_SIZE = 10
BEGIN_SENTENCE = "<s>"
END_SENTENCE = "</s>"
#ROMANCE_CHUNKS = r"c:\Users\liatn\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\complete_users_toy"
ROMANCE_CHUNKS = r"/data/home/univ/lnativ1/RedditData/Romance/Over2000"
NATIVE_CHUNKS =  r"/data/home/univ/lnativ1/RedditData/Native/Over2000"
GERMANIC_CHUNKS = r"/data/home/univ/lnativ1/RedditData/Germanic/Over2000"
GERMANIC_TOEFL = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Germanic\text"
ROMANCE_TOEFL = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\text"
TOEFL_ALL = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\tokenized"
# ROMANCE_POS_TAG_CHUNKS = r"c:\Users\liatn\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\complete_users_POS_TagToy"
ROMANCE_POS_TAG_CHUNKS = r"/data/home/univ/lnativ1/RedditData/Romance/lemmas_pos_over_2000/"
NATIVE_POS_TAG_LEMMAS =  r"/data/home/univ/lnativ1/RedditData/Native/lemmas_pos_over_2000/"
GERMANIC_POS_TAG_LEMMAS =  r"/data/home/univ/lnativ1/RedditData/Germanic/lemmas_pos_over_2000/"
GERMANIC_TOEFL_POS_TAG_LEMMA = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Germanic\lemmas_pos"
ROMANCE_TOEFL_POS_TAG_LEMMA = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\Romance\lemmas_pos"
TOEFL_ALL_POS_TAG_LEMMA = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\responses\lemmas_pos"
LOCNESS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\texts"
LOCNESS_POS_TAG_LEMMA = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\LOCNESS\lemmas_pos"
ICLE_ALL = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\texts"
ICLE_GERMANIC = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\texts\Germanic"
ICLE_ALL_ROMANCE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\texts\Romance"
ICLE_ALL_POS_TAG_LEMMA = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\lemmas_pos"
ICLE_ALL_POS_TAG_LEMMA_GERMANIC = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\lemmas_pos\Germanic"
ICLE_ALL_POS_TAG_LEMMA_ROMANCE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ICLE\lemmas_pos\Romance"


def POS_tag_chunks(nlp, input_dir, combined_output_dir):
    files = os.listdir(input_dir)

    # Tokenize, lemmetaize, POS Tagging and pickling pro cessed text
    i = 0
    dir_len = len(files)
    for file in files:
        if not ".txt" in file:
            continue
        i += 1
        with open(os.path.join(input_dir, file), 'r', encoding='utf-8') as f:
            outfile = os.path.join(combined_output_dir, file.split(".txt")[0])
            print('processing file: {}, {} of {}'.format(file.split(".txt")[0], i, dir_len))
            if os.path.exists(outfile):
                continue
            text = f.read().split("\n")
            tagged_text = []
            for sent in text:
                doc = nlp(sent)
                tagged_sentence = BEGIN_SENTENCE
                for word in doc:
                    tagged_sentence += word.lemma_ + "_" + word.pos_ + " "
                tagged_sentence += END_SENTENCE
                tagged_text.append(tagged_sentence)
            with open(outfile, 'wb') as out:
                pickle.dump(tagged_text, out)





def create_POS_trigram_dict(input_dir, pos_trigram_dict):

    files = [os.path.join(input_dir, file) for file in os.listdir(input_dir)]
    for f in files:
        with open(f, 'r', encoding='utf-8') as tagged_f:
            for line in tagged_f:
                pos_tag_list = line.strip().split(" ")
                pos_trigrams = ([" ".join(x) for x in [pos_tag_list[i:i + 3] for i in range(0, len(pos_tag_list), 1)] if len(x) == 3])
                for j in range(len(pos_trigrams)):
                    pos_tri = str(pos_trigrams[j])
                    if pos_tri not in pos_trigram_dict.keys():
                        pos_trigram_dict.setdefault(pos_tri, 0)
                    pos_trigram_dict[pos_tri] += 1
    return pos_trigram_dict

def write_pos_trigrams_to_file(pos_trigram_dict, output_file):
    with open(output_file, 'w', encoding='utf-8', newline='') as pos_trigram_dict_file:
        fieldnames = ['pos_trigram', 'count']
        writer = csv.DictWriter(pos_trigram_dict_file, fieldnames=fieldnames)
        writer.writeheader()
        for key,value in pos_trigram_dict.items():
            writer.writerow({'pos_trigram':key, 'count':value})



def main():
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    # doc = nlp("he nailed it")
    # word_list = ['nail']
    # for word in word_list:
    #     doc = nlp(word)
    #     print(len(doc))
    # for token in doc:
    #     print(token.text, token.pos_)
    # pos_trigram_dict = {}
    POS_tag_chunks(nlp, ICLE_ALL, ICLE_ALL_POS_TAG_LEMMA)
    # print('done pos tagging romance users')
    # POS_tag_chunks(nlp, ROMANCE_CHUNKS, ROMANCE_POS_TAG_CHUNKS)
    # create_POS_trigram_dict(ROMANCE_POS_TAG_CHUNKS, pos_trigram_dict)
    # print(pos_trigram_dict['ADV ADP DET'])
    # create_POS_trigram_dict(NATIVE_POS_TAG_CHUNKS, pos_trigram_dict)
    # print(pos_trigram_dict['ADV ADP DET'])
    # write_pos_trigrams_to_file(pos_trigram_dict, 'trigrams_toy_count.csv')

if __name__ == '__main__':
    main()
