import pandas as pd
word_cols = ['word', 'PoS', 'count']
freq_word_list_df = pd.read_csv(r'c:\Users\User\Documents\Liat\Research\Repo\Cognates\encow16ax.wp.tsv', 'r', delimiter='\t', names = word_cols, header = None)
POS_dict = {"VERB":"V", "NOUN":"N", "ADJ":"JJ", "SCONJ":"IN", "ADV":"RB"}
synset_list = pd.read_csv(r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\manual_synset_list_with_origin_and_POS.csv")
print(freq_word_list_df.head())
print("**************")
freq_word_list_df['word'].str.lower()
print(freq_word_list_df.head())
# for row in synset_list.iterrows():
#     count = 0;
#     row_data = row[1]
#     word = row_data['word']
#     PoS = row_data['POS']
