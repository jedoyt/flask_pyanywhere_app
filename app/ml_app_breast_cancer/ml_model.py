# import sklearn and load the built-in breast cancer dataset
from sklearn.datasets import load_breast_cancer
# Import the KNN classifier
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# load the dataset
cancer = load_breast_cancer()

# Create dictionary of cancer dataset
def convert_dataset_to_dict(cancer=cancer):
    cancer_dict = {}
    for feature in cancer.feature_names:
        key = '_'.join(feature.split())
        cancer_dict[key] = []
    for row in cancer.data:
        for i, feature in enumerate(cancer_dict.keys()):
            cancer_dict[feature].append(row[i])
    return cancer_dict

def get_summary_stats(cancer_dict):
    stats_dict = {feature: dict() for feature in cancer_dict.keys()}
    for feature, list_val in cancer_dict.items():
        stats_dict[feature]['label'] =  feature.replace('_', ' ').title()
        stats_dict[feature]['min'] = np.round(np.min(list_val), decimals=4)
        stats_dict[feature]['mean'] = np.round(np.mean(list_val), decimals=4)
        stats_dict[feature]['median'] = np.round(np.median(list_val), decimals=4)
        stats_dict[feature]['max'] = np.round(np.max(list_val), decimals=4)
    return stats_dict

# Create the final KNN Classifier using the whole cancer dataset
def build_knn_model(n):
    knn_model = KNeighborsClassifier(n_neighbors=n)
    knn_model.fit(cancer['data'], cancer['target'])
    return knn_model

def knn_predict(model, X_arr):
    y = model.predict(X_arr)
    if y == 1:
        return "Benign"
    elif y == 0:
        return "Malignant"