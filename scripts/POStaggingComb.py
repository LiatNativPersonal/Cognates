import os
import spacy
import csv
from random import sample

SAMPLE_SIZE = 10
BEGIN_SENTENCE = "<beg>"
END_SENTENCE = "<end>"
#ROMANCE_CHUNKS = r"c:\Users\liatn\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\complete_users_toy"
ROMANCE_CHUNKS = r"/data/home/univ/lnativ1/RedditData/Romance/Over2000"
NATIVE_CHUNKS = r"c:\Users\liatn\Documents\Liat\Research\Repo\Cognates\RedditData\Native\complete_users_toy"
# ROMANCE_POS_TAG_CHUNKS = r"c:\Users\liatn\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\complete_users_POS_TagToy"
ROMANCE_POS_TAG_CHUNKS = r"/data/home/univ/lnativ1/RedditData/Romance/txt_pos_over_2000"
NATIVE_POS_TAG_CHUNKS = r"c:\Users\liatn\Documents\Liat\Research\Repo\Cognates\RedditData\Native\complete_users_POS_TagToy"


def POS_tag_chunks(tagger, input_dir, output_dir):
    files = os.listdir(input_dir)
    # POS Tagging and writing tagged sentences to files
    i = 1
    dir_len = len(files)
    for file in files:
        print('processing file: {}, {} of {}'.format(file,i,dir_len))
        with open(os.path.join(input_dir, file), 'r', encoding='utf-8') as f:
            outfile = os.path.join(output_dir, file)
            if os.path.exists(outfile):
                continue
            with open(outfile, 'w', encoding='utf-8') as out:
                text = f.read().split("\n")
                for sent in text:
                    doc = tagger(sent)
                    out.write(BEGIN_SENTENCE)
                    for word in doc:
                        out.write(word.text + "_" + word.pos_ + " ")
                    out.write(END_SENTENCE + "\n")



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
    nlp = spacy.load("en_core_web_sm")
    # doc = nlp("he nailed it")
    # word_list = ['nail']
    # for word in word_list:
    #     doc = nlp(word)
    #     print(len(doc))
    # for token in doc:
    #     print(token.text, token.pos_)
    # pos_trigram_dict = {}
    POS_tag_chunks(nlp, ROMANCE_CHUNKS, ROMANCE_POS_TAG_CHUNKS)
    # print('done pos tagging romance users')
    # POS_tag_chunks(nlp, ROMANCE_CHUNKS, ROMANCE_POS_TAG_CHUNKS)
    # create_POS_trigram_dict(ROMANCE_POS_TAG_CHUNKS, pos_trigram_dict)
    # print(pos_trigram_dict['ADV ADP DET'])
    # create_POS_trigram_dict(NATIVE_POS_TAG_CHUNKS, pos_trigram_dict)
    # print(pos_trigram_dict['ADV ADP DET'])
    # write_pos_trigrams_to_file(pos_trigram_dict, 'trigrams_toy_count.csv')

if __name__ == '__main__':
    main()
