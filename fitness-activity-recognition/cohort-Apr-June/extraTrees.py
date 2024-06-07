from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.metrics import confusion_matrix, classification_report, f1_score, recall_score, precision_score
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def model_extraTrees(X_train, y_train, X_test, y_test, cf_matrix = False):
    
    # Create a classifier
    clf_extra = ExtraTreesClassifier(n_estimators=500)

    # Fit the classifier with the training data
    clf_extra.fit(X_train, y_train)

    # Use trained model to predict output of test dataset
    predictions  = clf_extra.predict(X_test) 
    preds_probs = clf_extra.predict_proba(X_test)
    
    
    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)
    
    f1 = f1_score(y_test, predictions, average='macro')
    precision = precision_score(y_test, predictions,average = 'micro', pos_label=1)
    recall = recall_score(y_test, predictions,average = 'micro', pos_label=1)
   
    print("ACCURACY PER INSTANCE:" ,accuracy)
    print("F1_score:" ,f1)
    print("Precision:", precision)
    print("Recall:",recall)
    
    (unique,count) = np.unique(y_train, return_counts=True)
    
    class_labels = unique


    # plotting confusion matrix
    
    if cf_matrix == True:

        plt.figure(figsize = (16,6))
        sns.heatmap(pd.DataFrame(confusion_matrix(y_test , predictions)),annot=True, fmt="d",
                    xticklabels = class_labels, yticklabels = class_labels)

        plt.xlabel('Predictions', fontsize=18)
        plt.ylabel('Actuals', fontsize=18)
        plt.title('Confusion Matrix', fontsize=18)
        print(classification_report(y_test, predictions))
        plt.show()

    return (clf_extra, predictions, preds_probs, accuracy, f1, precision, recall )