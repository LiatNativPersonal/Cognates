import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE =  r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\scripts\3_TOEFL_level_1000_words_chunks_distances.csv"

dist_df = pd.read_csv(INPUT_FILE)
# dist_df = dist_df.sort_values(by=['distance'])
fig, ax = plt.subplots()
colors = {'low':'red', 'high':'green', 'medium':'yellow'}
ax.scatter(dist_df['file'], dist_df['distance'], c=dist_df['grade'].map(colors))

plt.show()