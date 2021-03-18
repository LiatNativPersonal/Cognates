import pandas as pd
import numpy as np
import os
import re
from RedditUser import RedditUser
from RedditCognatesCounter import RedditCognatesCounter

user_stat_file = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\complete_users_6_bins_log_reg_toy_stat.csv"
output_file = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\avg_grade_bins.csv"
text_file_dir = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Romance\over2000"
NUMBER_OF_BINS = 6
SYNSET_ORIGIN = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\combined_synset_list_with_origin_and_POS.csv"


df = pd.read_csv(user_stat_file)
bins = pd.qcut(np.array(df['avg_grade']), NUMBER_OF_BINS,labels=False)
user_to_text_file = {}
i = 1
for user in df['username']:
    username = user[1:len(user)-1]
    # print(username)
    # print(str(i) +" " + user[1:len(user)-1])

    user_to_text_file[username] = [f for f in os.listdir(text_file_dir) if f.startswith(username + ".")][0]
    i += 1

# print (user_to_text_file)
data = {'User': user_to_text_file.keys(), 'Text_file':user_to_text_file.values(), 'avg_grade': df['avg_grade'], 'bin': list(bins)}
#
bins_df = pd.DataFrame(data)
bins_df = pd.read_csv(output_file)
cog_cntr = RedditCognatesCounter(SYNSET_ORIGIN)
number_of_synsets = max(cog_cntr.cognates_df['synset'])
user_data_fields = {'user': [], 'bin': []}
bin_data_fields = {'bin':[]}
synsets_counts = {}
for i in range(1, number_of_synsets + 1):
    user_data_fields['{}_ratio'.format(i)] = []
    bin_data_fields['{}_ratio'.format(i)] = []
    # print(user_data_fields.keys())
    synsets_counts[i] = {}
    synsets_counts[i]['G'] = 0
    synsets_counts[i]['R'] = 0

all_users_df = pd.DataFrame()
for i in range(NUMBER_OF_BINS):
    print('processing bin {}'.format(i))
    bin_users = bins_df[bins_df['bin'] == i]
    bin_reddit_user_list = [(RedditUser(row.User, 'Romance', os.path.join(text_file_dir, row.Text_file))) for index, row
                            in bin_users.iterrows()]
    for reddit_user in bin_reddit_user_list:
        print('processing user {}'.format(reddit_user.user_name))
        cog_cntr.count_cognates_for_user(reddit_user)
        user_counts_df = cog_cntr.users_cognate_counts_dict[reddit_user]
        # user_data_fields['user'].append(reddit_user.user_name)
        # user_data_fields['bin'].append(i)

        for syn in range(1, number_of_synsets + 1):
            synset_info = user_counts_df[user_counts_df['synset'] == syn]
            ger_count = sum(synset_info[synset_info['Source'] == 'G']['count'])
            rom_count = sum(synset_info[synset_info['Source'] == 'R']['count'])
            # synset_ger_count = ger_count
            # synset_rom_count = rom_count
            # total = synset_rom_count + synset_ger_count

            synsets_counts[syn]['R'] += rom_count
            synsets_counts[syn]['G'] += ger_count
            #
            # current_field = "{}_ratio".format(syn)
            # ratio = 0.0
            # if total > 0:
            #     ratio = synset_rom_count / total
            # else:
            #     ratio = '-'
            # user_data_fields[current_field].append(ratio)
    bin_data_fields['bin'].append(i)
    for syn in range(1, number_of_synsets + 1):
        current_field = "{}_ratio".format(syn)
        ratio = 0.0
        total = synsets_counts[syn]['G'] + synsets_counts[syn]['R']
        if total > 0:
            ratio = synsets_counts[syn]['R'] / total
        else:
            ratio = '-'
        bin_data_fields[current_field].append(ratio)
    for syn in range(1, number_of_synsets + 1):
        synsets_counts[syn]['G'] = 0
        synsets_counts[syn]['R'] = 0

# bin_users_df = pd.DataFrame(user_data_fields)
agg_bin_users_df = pd.DataFrame(bin_data_fields)
# bin_users_df.to_csv('bin_users_ratios.csv')
agg_bin_users_df.to_csv('agg_bin_users_ratios.csv')
    # print(bin_users_df)

    # cog_cntr.write_cognates_vector_to_file("{}_bin_cognate_count.csv".format(i),0,0)


# ### NATIVES
# natives_chunks_dir = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Native\complete_users_toy"
# natives_full_text_dir = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\RedditData\Native\over2000"
#
# user_data_fields = {'user': []}
# cog_cntr = RedditCognatesCounter(SYNSET_ORIGIN)
# number_of_synsets = max(cog_cntr.cognates_df['synset'])
# for i in range(1, number_of_synsets + 1):
#     user_data_fields['{}_ratio'.format(i)] = []
# print(user_data_fields.keys())
#
# usernames = set([re.split('_[0-9]+_[0-9]+.txt', s)[0] for s in os.listdir(natives_chunks_dir)])
#
# for username in usernames:
#     user_data_fields['user'].append(username)
#
#     text_file = [f for f in os.listdir(text_file_dir) if f.startswith(username + ".")][0]
#     reddit_user = RedditUser(username, 'native', os.path.join(natives_full_text_dir, text_file))
#     cog_cntr.count_cognates_for_user(reddit_user)
#     user_counts_df = cog_cntr.users_cognate_counts_dict[reddit_user]
#     for syn in range(1, number_of_synsets + 1):
#         synset_info = user_counts_df[user_counts_df['synset'] == syn]
#         # print(synset_info)
#         synset_ger_count = sum(synset_info[synset_info['Source'] == 'G']['count'])
#         synset_rom_count = sum(synset_info[synset_info['Source'] == 'R']['count'])
#         total = synset_rom_count + synset_ger_count
#         # if synset_rom_count > 0:
#         #     print(synset_ger_count)
#         #     print(total)
#         current_field = "{}_ratio".format(syn)
#         ratio = 0.0
#         if total > 0:
#             ratio = synset_rom_count / total
#         else:
#             ratio = '-'
#         user_data_fields[current_field].append(ratio)


#