import os
from random import shuffle

ORIGINAL_TEXTS_PATH =r"/data/home/univ/lnativ1/RedditData/Germanic/Over2000"
SHUFFLED_CHUNKS_PATH= r"/data/home/univ/lnativ1/RedditData/Germanic/ShuffledChunksOver2000"
LOGS = r"/data/home/univ/lnativ1/logs"
CHUNK_SIZE = 2000

user_to_chunks = {}
chunk_num = 0
processed = 1
total = len(os.listdir(ORIGINAL_TEXTS_PATH))
print(total)
for f in os.listdir(ORIGINAL_TEXTS_PATH):
    print("porcessing {} of {}".format(processed,total))
    processed += 1
    # if processed > 3:
    #     break
    user_chunk_num = 0
    user_name = f.split(".")[0]
    user_to_chunks[user_name] = {}
    with open(os.path.join(ORIGINAL_TEXTS_PATH,f), 'r') as uf:
        sentences = uf.read().split("\n")
        shuffle(sentences)
    chunk = []
    i = 0
    for line in sentences:
        line = line.strip()
        if len(line) == 0: continue
        chunk.append(line)
        i += len(line.split(" "))
        if i >= CHUNK_SIZE:
            user_to_chunks[user_name][chunk_num] = i
            filename =  user_name + "_" + str(user_chunk_num)+ "_" + str(chunk_num) + ".txt"
            # print('writing file' + os.path.join(SHUFFLED_CHUNKS_PATH,filename))
            with open(os.path.join(SHUFFLED_CHUNKS_PATH,filename), 'w') as cf:
                  cf.write('\n'.join(chunk))
            i = 0
            chunk_num += 1
            user_chunk_num += 1
            chunk.clear()


with open(os.path.join(LOGS,'germanic_chunks.csv'), 'w') as f:  # Just use 'w' mode in 3.x
    f.write("user_name, user_chunk, chunk, size(tokens)\n")
    for user in user_to_chunks.keys():
        i = 0
        for chunk,size in user_to_chunks[user].items():
            f.write("{},{},{},{}\n".format(user,i,chunk,size))
            i += 1
