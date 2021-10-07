INPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Merlin\merlin-text-v1.1\meta_ltext\german"
OUTPUT_DIR = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Merlin\ClassificationDataset"
LVL_PREFIX = "Overall CEFR rating: "
TXT_PREFIX = "Learner text:"

import os

for file in os.listdir(INPUT_DIR):
    new_file_name = file
    text = []
    add_to_text = False
    lvl = ""
    with open(os.path.join(INPUT_DIR,file), 'r', encoding='utf-8') as input_f:
        for line in input_f.read().split("\n"):
            # print(line)
            if line.startswith(LVL_PREFIX):
                lvl = line.split(LVL_PREFIX)[1].strip()
                print(lvl)
            if add_to_text and len(line) > 0:
                text.append(line)
            if line.startswith(TXT_PREFIX):
                add_to_text = True

    lvl_dir = os.path.join(OUTPUT_DIR,lvl)
    with open(os.path.join(lvl_dir,file), 'w', encoding='utf-8') as out_f:
        for s in text:
            out_f.write(s + "\n")

