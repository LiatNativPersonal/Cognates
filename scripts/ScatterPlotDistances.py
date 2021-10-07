import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


INPUT_FILE =  r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\TOEFL_LOCNESS\Log_reg_fold_4_TOEFL_vs_LOCNESS.csv"
# INPUT_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\Log_reg_fold_9_MERLIN_essays_vs_FALCO.csv"
# INPUT_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\MERLIN_FALKO\LogReg_fold_3_MERLIN_Falko.csv"
# INPUT_FILE =  r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\LogReg_fold_2_TOEFL_Low_High.csv"
# INPUT_FILE =  r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\NITE\Log_reg_fold_9_HEC.csv"
# INPUT_FILE =  r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\LogReg_fold_0_HEC.csv"
fold = 4

dist_df = pd.read_csv(INPUT_FILE)
# high_dists = dist_df[dist_df['grade'] == 'C']
high_dists = dist_df[dist_df['grade'] == 'high']
# high_dists = high_dists.sort_values('Distance')
# med_dists = dist_df[dist_df['grade'] == 'B']
med_dists = dist_df[dist_df['grade'] == 'medium']
# med_dists = med_dists.sort_values('Distance')
# low_dists = dist_df[dist_df['grade'] == 'A']
low_dists = dist_df[dist_df['grade'] == 'low']
# low_dists = low_dists.sort_values('Distance')
# print(len(high_dists))

dist_df = dist_df.assign(color='green')
dist_df.loc[dist_df['grade'] == 'medium', 'color'] = 'yellow'
dist_df.loc[dist_df['grade'] == 'low', 'color'] = 'red'
print(dist_df)


high_chunks = np.array_split(high_dists['Distance'], len(high_dists))
med_chunks = np.array_split(med_dists['Distance'], len(med_dists))
low_chunks = np.array_split(low_dists['Distance'], len(low_dists))

print(stats.kruskal(list(high_dists['Distance']), list(low_dists['Distance'])))
print(stats.kruskal(list(high_dists['Distance']), list(med_dists['Distance'])))
print(stats.kruskal(list(med_dists['Distance']), list(low_dists['Distance'])))
print(stats.kruskal(list(high_dists['Distance']), list(med_dists['Distance']), list(low_dists['Distance'])))


# print(list(high_chunks))
print(stats.mannwhitneyu(list(high_dists['Distance']), list(low_dists['Distance'])))
print(stats.mannwhitneyu(list(high_dists['Distance']), list(med_dists['Distance'])))
print(stats.mannwhitneyu(list(med_dists['Distance']), list(low_dists['Distance'])))



high_agg_values = []
med_agg_values = []
low_agg_values = []
i = 0

high_chunks = np.array_split(high_chunks, int(len(high_chunks)/20))
med_chunks = np.array_split(med_chunks, int(len(med_chunks)/20))
low_chunks = np.array_split(low_chunks, int(len(low_chunks)/20))



for high in range(len(high_chunks)):

    high_agg_values.append([i,np.mean(high_chunks[high]),'green', 2])
    i+=1
for med in range(len(med_chunks)):
    med_agg_values.append([i,np.mean(med_chunks[med]),'yellow', 1])
    i+=1
for low in range(len(low_chunks)):
    low_agg_values.append([i,np.mean(low_chunks[low]),'red', 0])
    i+=1

plot_df = pd.DataFrame(high_agg_values+ med_agg_values + low_agg_values, columns= ['id','distance', 'color', 'level'])
#
# print(plot_df)
colors = np.array(plot_df['color'])
plot_df.plot.scatter(x='id', y='distance', grid=True,  title="TOEFL distance per level", c=colors)
# colors = np.array(dist_df['color'])
# dist_df.plot.scatter(x='User', y='Distance', grid=True,  title="TOEFL distance per level", c=colors)
# plt.savefig('Linear_SVM_NITE_hebrew.png')
plt.savefig('Log_Reg_TOEFL_{}.png'.format(fold))

slope, intercept, r_value, p_value, std_err = stats.linregress(plot_df['distance'],plot_df['level'])
    # return
# r_square = r2_score(plot_df['distance'],plot_df['level'])
print(r_value**2)

# print((high_chunks))
# fig, ax = plt.subplots()
# colors = {'low':'red', 'high':'green', 'medium':'yellow'}
# ax.scatter(dist_df['User'], dist_df['Distance'], c=dist_df['grade'].map(colors))
# #
# plt.show()