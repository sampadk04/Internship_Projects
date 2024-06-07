from numpy import save
from classes import*
from extraTrees import model_extraTrees
from sklearn.model_selection import train_test_split
from data_transform import data_transform
from sklearn.preprocessing import LabelEncoder

class buildModel:

    def __init__(self, annotated, data, test_split, n, step, save_name):
        self.annotated = annotated
        self.data = data
        self.test_split = test_split
        self.n = n
        self.step = step
        self.save_name = save_name

    def changeActions(self, x):
        if x in aerobic:
            return 'aerobic'
        elif x in coordination_agility:
            return 'coordination_agility'
        elif x in weight_bearing:
            return 'weight_bearing'
        elif x in calisthenics:
            return 'calisthenics'
        elif x in weightlifting:
            return 'weightlifting'
        elif x in balance_stability:
            return 'balance_stability'
        elif x in flexibility:
            return 'flexibility'
        elif x in remove:
            return 'remove'
        elif x in doubt:
            return "doubt"
        else:
            return 'idle'

    def trainModel(self):


        self.data['target']= self.data['actions'].apply(lambda x: self.changeActions(x))
        self.data.drop(['actions'] , axis = 1,inplace = True)


        data_transformed = data_transform(self.data, self.n, self.step)
        remove_from_target = ['doubt', 'remove']
        data_transformed = data_transformed[~data_transformed['target'].isin(remove_from_target)]
        print(data_transformed.groupby("target").size())

        X = data_transformed.iloc[:,:-1]
        y = data_transformed['target']

        # changing the target value to numeric value to fit the data
        le = LabelEncoder()
        le.fit(y)
        y = le.transform(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=self.test_split, shuffle  = True)

        model, predictions , preds_probs, accuracy, f1, precision, recall = model_extraTrees(X_train, y_train, X_test, y_test, cf_matrix =True)

        model.save_model(self.save_name)


