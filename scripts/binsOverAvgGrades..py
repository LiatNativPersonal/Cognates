import pandas as pd
import numpy as np
import os
from RedditUser import RedditUser
from RedditCognatesCounter import RedditCognatesCounter

user_stat_file = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\complete_users_6_bins_log_reg_toy_stat.csv"
output_file= r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\avg_grade_bins.csv"
text_file_dir = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\over2000"
NUMBER_OF_BINS = 6
SYNSET_ORIGIN = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\combined_synset_list_with_origin.csv"

# df = pd.read_csv(user_stat_file)
# bins = pd.qcut(np.array(df['avg_grade']), NUMBER_OF_BINS,labels=False)
# user_to_text_file = {}
# i = 1
# for user in df['username']:
#     username = user[1:len(user)-1]
#     print(username)
#     # print(str(i) +" " + user[1:len(user)-1])
#
#     user_to_text_file[username] = [f for f in os.listdir(text_file_dir) if f.startswith(username + ".")][0]
#     i += 1
#
# print (user_to_text_file)
# data = {'User': user_to_text_file.keys(), 'Text_file':user_to_text_file.values(), 'avg_grade': df['avg_grade'], 'bin': list(bins)}

# bins_df = pd.DataFrame(data)
bins_df = pd.read_csv(output_file)
cog_cntr = RedditCognatesCounter(SYNSET_ORIGIN)
for i in range(NUMBER_OF_BINS):
    bin_users = bins_df[bins_df['bin'] == i]
    bin_reddit_user_list = [(RedditUser(row.User, 'Romance', os.path.join(text_file_dir,row.Text_file))) for index, row in bin_users.iterrows()]
    for reddit_user in bin_reddit_user_list:
        cog_cntr.count_cognates_for_user(reddit_user)
        user_df = cog_cntr.users_cognate_counts_dict[reddit_user]
        # print(user_df)
        # break
    cog_cntr.write_cognates_vector_to_file("{}_bin_cognate_count.csv".format(i),0,0)
    break