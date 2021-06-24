
from sklearn.cluster import KMeans, MiniBatchKMeans
import os
import numpy as np
from BinaryNLIClassifier import BinaryNLIClassifier
from sklearn.metrics import f1_score, precision_score, recall_score,accuracy_score
from sklearn.preprocessing import StandardScaler, scale

TOEFL_SHUFFLED_CHUNKS_PATH = r"c:\Users\User\Documents\Liat\Research\Repo\Cognates\ETS_Corpus_of_Non-Native_Written_English\data\text\shuff_grade_aggr"
LOW = 2
MED = 0
HIGH = 1
N_CLUSTERS = 2


class LevelClustering:

    def __init__(self):
        self.bin_nli_clf = BinaryNLIClassifier()
        # self.clusterer = KMeans(n_clusters=N_CLUSTERS, random_state=0)
        self.clusterer = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=0, batch_size=20,max_iter=10)
        self.lows = []
        self.meds = []
        self.highs = []
        self.precision = 0.0
        self.recall = 0.0
        self.f1 = 0.0
        self.accuracy = 0.0

    def createFeatureVectors(self):
        self.lows = [os.path.join(TOEFL_SHUFFLED_CHUNKS_PATH, f)
                     for f in os.listdir(TOEFL_SHUFFLED_CHUNKS_PATH) if "low" in f]
        self.meds = [os.path.join(TOEFL_SHUFFLED_CHUNKS_PATH, f)
                     for f in os.listdir(TOEFL_SHUFFLED_CHUNKS_PATH) if "medium" in f]
        self.highs = [os.path.join(TOEFL_SHUFFLED_CHUNKS_PATH, f)
                      for f in os.listdir(TOEFL_SHUFFLED_CHUNKS_PATH) if "high" in f]
        print(len(self.meds))

        # labels = [LOW] * len(self.lows) + [MED] * len(self.meds) + [HIGH] * len(self.highs)
        labels = [HIGH] * len(self.highs) + [MED] * len(self.meds)
        self.bin_nli_clf.createFunctionWordFeatureVectors(self.highs + self.meds, labels)
        # self.bin_nli_clf.createFunctionWordFeatureVectors(self.lows + self.meds + self.highs, labels)
        self.bin_nli_clf.y = np.array(labels)
        self.bin_nli_clf.splitDataAndClassify()

    def cluster(self):
        scl = StandardScaler(with_mean=False)
        scl.fit(self.bin_nli_clf.X)

        self.clusterer.fit(self.bin_nli_clf.X)

        # print(self.clusterer.labels_)




    def evaluate(self):

        self.precision = precision_score(self.bin_nli_clf.y, self.clusterer.labels_, average='macro')
        self.recall = recall_score(self.bin_nli_clf.y, self.clusterer.labels_, average='macro')
        self.f1 = f1_score(self.bin_nli_clf.y, self.clusterer.labels_, average='macro')
        self.accuracy = accuracy_score(self.bin_nli_clf.y, self.clusterer.labels_)




lvl_cluster = LevelClustering()
lvl_cluster.createFeatureVectors()
lvl_cluster.cluster()
lvl_cluster.evaluate()
print(list(lvl_cluster.clusterer.labels_))
print(list(lvl_cluster.bin_nli_clf.y))
# print(len([x for x in lvl_cluster.clusterer.labels_ if x == 0]))
# print("precision: {}, recall: {}, f1: {}".format(lvl_cluster.precision, lvl_cluster.recall, lvl_cluster.f1))
print("accuracy: {}".format(lvl_cluster.accuracy))
