import pyconll
import os
import pickle

NATIVE_INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\NICE_tagged\native"
NATIVE_OUTPUT_DIR = r":\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\ClassificationDataset\lemmas_pos\native"
NON_NATIVE_INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\NICE_tagged\nonnative"
NON_NATIVE_OUTPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\ClassificationDataset\lemmas_pos\non_native"
BEGIN_SENTENCE = "<s>"
END_SENTENCE = "</s>"

levels = ['low', 'medium', 'high']
BASE_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Data\Hebrew\NITE\ClassificationDataset\texts"

sent_count = 0
token_count = 0
total_essays = len(os.listdir(NATIVE_INPUT_DIR))
for file in os.listdir(NATIVE_INPUT_DIR):
    trees = pyconll.load_from_file(os.path.join(NATIVE_INPUT_DIR, file))
    sent_count += len(trees)
    for sent in trees:
        token_count += len(sent)

print(" {} average sentence number: {}".format('native', sent_count/total_essays))
print("{} average token number: {}".format('native', token_count/total_essays))

print(" {} total sentence number: {}".format('native', sent_count ))
print("{} total token number: {}".format('native', token_count ))




# sent_count = 0
# token_count = 0
# for lvl in levels:
#     lvl_dir = os.path.join(BASE_DIR,lvl)
#     total_essays = len(os.listdir(lvl_dir))
#     for file in os.listdir(lvl_dir):
#         trees = pyconll.load_from_file(os.path.join(lvl_dir, file))
#         sent_count += len(trees)
#         for sent in trees:
#             token_count += len(sent)
#
#     print(" {} average sentence number: {}".format(lvl, sent_count/total_essays))
#     print("{} average token number: {}".format(lvl, token_count/total_essays))
#
#     print(" {} total sentence number: {}".format(lvl, sent_count ))
#     print("{} total token number: {}".format(lvl, token_count ))

# for file in os.listdir(NON_NATIVE_INPUT_DIR):
#     outfile = os.path.join(NON_NATIVE_OUTPUT_DIR,file.split('.')[0])
#     print(outfile)
#     trees = pyconll.load_from_file(os.path.join(NON_NATIVE_INPUT_DIR,file))
#     tagged_text = []
#     for sent in trees:
#         tagged_sentence = BEGIN_SENTENCE
#         for token in sent:
#             tagged_sentence += "{}_{} ".format(token.lemma,token.upos)
#         tagged_sentence += END_SENTENCE
#         tagged_text.append(tagged_sentence)
#     with open(outfile, 'wb') as out:
#         pickle.dump(tagged_text, out)
#
#
