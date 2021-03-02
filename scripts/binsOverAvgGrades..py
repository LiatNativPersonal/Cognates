import pandas as pd
import numpy as np
import os

user_stat_file = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\complete_users_6_bins_log_reg_toy_stat.csv"
output_file= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\avg_grade_bins.csv"
text_file_dir = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\over2000"
NUMBER_OF_BINS = 6

df = pd.read_csv(user_stat_file)
bins = pd.qcut(np.array(df['avg_grade']), NUMBER_OF_BINS,labels=False)
user_to_text_file = {}
i = 1
for user in df['username']:
    username = user[1:len(user)-1]
    print(username)
    # print(str(i) +" " + user[1:len(user)-1])

    user_to_text_file[username] = [f for f in os.listdir(text_file_dir) if f.startswith(username)]
    i += 1

print (user_to_text_file)
data = {'User': user_to_text_file.keys(), 'Text_file':user_to_text_file.values(), 'grade': list(bins)}

pd.DataFrame(data).to_csv(output_file)