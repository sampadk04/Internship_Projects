import os
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

# XG Boost Classifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.metrics import confusion_matrix, classification_report, f1_score, recall_score, precision_score

# config_{config.config_num}_frames{config.frames}_steps{config.steps}
import config


def model_xgb(X_train, y_train, X_test, y_test, configuration='no_config', cf_matrix=False):
    # Fitting the data
    # Create a classifier
    xgb = XGBClassifier(objective='multi:softmax', random_state=42)

    # Fit the classifier with the training data
    xgb.fit(X_train, y_train)

    # Use trained model to predict output of test dataset
    predictions = xgb.predict(X_test)
    preds_probs = xgb.predict_proba(X_test)

    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)

    f1 = f1_score(y_test, predictions, average='macro')
    precision = precision_score(y_test, predictions, average='micro', pos_label=1)
    recall = recall_score(y_test, predictions, average='micro', pos_label=1)

    print("ACCURACY PER INSTANCE:", accuracy)
    print("F1_score:", f1)
    print("Precision:", precision)
    print("Recall:", recall)

    (unique, count) = np.unique(y_train, return_counts=True)
    class_labels = unique

    # plotting confusion matrix
    if cf_matrix:
        plt.figure(figsize=(16, 6))
        sns.heatmap(pd.DataFrame(confusion_matrix(y_test, predictions)), annot=True, fmt="d",
                    xticklabels=class_labels, yticklabels=class_labels)

        plt.xlabel('Predictions', fontsize=18)
        plt.ylabel('Actuals', fontsize=18)
        plt.title(f'{configuration} Confusion Matrix {config.frames} {config.steps}', fontsize=18)
        print(classification_report(y_test, predictions))
        matrices_plots_dir = f'matrices_plots_dir/config_num{configuration}'
        isExist = os.path.exists(matrices_plots_dir)
        if not isExist:
            os.makedirs(matrices_plots_dir)
            print('directory_created!')
        plt.savefig(matrices_plots_dir + f"/{configuration}_confmatrix_{config.frames}_{config.steps}.jpg")
        plt.show()
        plt.close()

    return xgb, predictions, preds_probs, accuracy, f1, precision, recall
