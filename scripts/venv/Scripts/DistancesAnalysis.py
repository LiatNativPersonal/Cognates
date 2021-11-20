import pandas as pd
import os
import statistics as stat
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

DISTANCE_RESULT_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\TOEFL_LOCNESS\Log_reg_fold_4_TOEFL_vs_LOCNESS.csv"
# DISTANCE_RESULT_FILE =r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\NITE\Log_reg_fold_7_HEC.csv"
# DISTANCE_RESULT_FILE = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\Results\BinaryClassification\MERLIN_FALKO\LogReg_fold_3_MERLIN_Falko.csv"

TOEFL_HLC_level_to_number_dict = {'low':0, 'medium':1, 'high':2}
CERF_level_to_number_dict = {'A':0, 'B':1, 'C':2}


def analyze_distances(level_to_number):

    distances_df = pd.read_csv(DISTANCE_RESULT_FILE)
    distances_df = distances_df.sort_values(by='Distance',ascending=True)
    golden = [level_to_number[x] for x in distances_df['grade']]
    # print(golden[0:10])
    centroids = {}
    levels = level_to_number.keys()
    for lvl in levels:
        curr_centroid = round(stat.median(list(distances_df.loc[distances_df['grade']== lvl, 'Distance'])),3)
        centroids[lvl] = curr_centroid

    closest_centroids = []
    i = 1
    for row in distances_df.iterrows():
        curr_dist = row[1]['Distance']

        cent_dist = {lvl:abs(curr_dist-cent) for lvl,cent in centroids.items()}
        cent_dist = sorted(cent_dist, key=cent_dist.get)
        closest_centroids.append(level_to_number[cent_dist[0]])
    print("centroid analysis:")
    # print(closest_centroids[0:10])
    print("Total accurcy:")
    print(accuracy_score(golden,closest_centroids))
    print("precision:")
    print(precision_score(golden,closest_centroids,average=None))
    print(precision_score(golden, closest_centroids, average='weighted'))
    print(precision_score(golden, closest_centroids, average='micro'))
    print('recall:')
    print(recall_score(golden, closest_centroids, average=None))
    print(recall_score(golden, closest_centroids, average="weighted"))
    print(recall_score(golden, closest_centroids, average="micro"))
    print('f1:')
    print(f1_score(golden, closest_centroids, average=None))
    print(f1_score(golden, closest_centroids, average="weighted"))
    print(f1_score(golden, closest_centroids, average="micro"))




    pred_level_sorted = []
    for lvl,label in level_to_number.items():
        pred_level_sorted.extend([label] * len(distances_df[distances_df['grade']==lvl]))
    # print(pred_level_sorted[3400:3430])
    # print(len(pred_level_sorted))
    size = len(pred_level_sorted)
    low_ten = 0.1
    low_five = 0.05
    high_five = 0.95
    high_ten = 0.9
    low_five_golden = golden[0:int(low_five*size)]
    low_ten_golden =  golden[0:int(low_ten*size)]
    low_five_pred = pred_level_sorted[0:int(low_five*size)]
    low_ten_pred = pred_level_sorted[0:int(low_ten*size)]

    high_five_golden = golden[int(high_five * size):size]
    high_ten_golden = golden[int(high_ten * size):size]
    high_five_pred = pred_level_sorted[int(high_five * size):size]
    high_ten_pred = pred_level_sorted[int(high_ten * size):size]

    print("\n\n\nSort by distance analysis:")
    print("Total accuracy :")
    print(accuracy_score(golden, pred_level_sorted))
    print("Total f1 :")
    print(f1_score(golden, pred_level_sorted, average='weighted'))
    print(f1_score(golden, pred_level_sorted, average='micro'))
    print(f1_score(golden, pred_level_sorted, average=None))
    print(precision_score(golden, pred_level_sorted, average=None))
    print(recall_score(golden, pred_level_sorted, average=None))

    print('upper 10%')
    # print(accuracy_score(high_ten_golden, high_ten_pred))
    # print(precision_score(high_ten_golden, high_ten_pred, average=None))
    # print(recall_score(high_ten_golden, high_ten_pred, average=None))
    # print(f1_score(high_ten_golden, high_ten_pred, average=None))

    print(accuracy_score(high_ten_golden, [2] * len(high_ten_golden)))
    print(precision_score(high_ten_golden, [2] * len(high_ten_golden), average=None))
    print(recall_score(high_ten_golden, [2] * len(high_ten_golden), average=None))
    print(f1_score(high_ten_golden, [2] * len(high_ten_golden), average=None))

    print('upper 5%')
    # print(accuracy_score(high_five_golden, high_five_pred))
    # print(precision_score(high_five_golden, high_five_pred, average=None, zero_division=0))
    # print(recall_score(high_five_golden, high_five_pred, average=None))
    # print(f1_score(high_five_golden, high_five_pred, average=None))

    print(accuracy_score(high_five_golden, [2] * len(high_five_golden)))
    print(precision_score(high_five_golden, [2] * len(high_five_golden), average=None, zero_division=0))
    print(recall_score(high_five_golden, [2] * len(high_five_golden), average=None))
    print(f1_score(high_five_golden, [2] * len(high_five_golden), average=None))

    print('lower 10%')
    # print(accuracy_score(low_ten_golden, low_ten_pred))
    # print(precision_score(low_ten_golden, low_ten_pred, average=None, zero_division=0))
    # print(recall_score(low_ten_golden, low_ten_pred, average=None))
    # print(f1_score(low_ten_golden, low_ten_pred, average=None))
    print(accuracy_score(low_ten_golden, [0] * len(low_ten_golden)))
    print(precision_score(low_ten_golden, [0] * len(low_ten_golden), average=None, zero_division=0))
    print(recall_score(low_ten_golden, [0] * len(low_ten_golden), average=None))
    print(f1_score(low_ten_golden, [0] * len(low_ten_golden), average=None))

    print('lower 5%')
    # print(accuracy_score(low_five_golden, low_five_pred))
    # print(precision_score(low_five_golden, low_five_pred, average=None, zero_division=0))
    # print(recall_score(low_five_golden, low_five_pred, average=None))
    # print(f1_score(low_five_golden, low_five_pred, average=None))
    print(accuracy_score(low_five_golden, [0] * len(low_five_golden)))
    print(precision_score(low_five_golden, [0] * len(low_five_golden), average=None, zero_division=0))
    print(recall_score(low_five_golden, [0] * len(low_five_golden), average=None))
    print(f1_score(low_five_golden, [0] * len(low_five_golden), average=None))







def Main():
    analyze_distances(TOEFL_HLC_level_to_number_dict)
    # analyze_distances(CERF_level_to_number_dict)
if __name__ == '__main__':
    Main()

