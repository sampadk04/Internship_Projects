import os
import sys
import yaml

# import config
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from ModelBuilding import data_transform

DataFromFile = pd.read_csv('new_csv_files/data_for_model.csv')
with open("config.yaml") as f:
    config = yaml.safe_load(f)

remove_from_target = config.get('remove_from_target_list')
ConfiguredData = DataFromFile[~DataFromFile['target'].isin(config.get(remove_from_target[int(config.get('config_num'))]))]
data_transformed = data_transform(ConfiguredData, config.get('frames'), config.get('steps'))
X = data_transformed[0]
y = data_transformed[1]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=config.get('test_size'), shuffle=True)
train_test_data_dir = f'TrainTestData/config_{config.get("config_num")}_frames{config.get("frames")}_steps{config.get("steps")}/test_size{str(config.get("test_size"))}'

isExist = os.path.exists(train_test_data_dir)
if not isExist:
    os.makedirs(train_test_data_dir)
    print('directory_created!')

np.save(train_test_data_dir + f'/X_train_{str(config.get("test_size")).replace(".", "_")}', X_train)
np.save(train_test_data_dir + f'/X_test_{str(config.get("test_size")).replace(".", "_")}', X_test)
np.save(train_test_data_dir + f'/y_train_{str(config.get("test_size")).replace(".", "_")}', y_train)
np.save(train_test_data_dir + f'/y_test_{str(config.get("test_size")).replace(".", "_")}', y_test)

if __name__ == '__main__':
    (unique, counts) = np.unique(y_train, return_counts=True)
    # print(np.asarray((unique, counts / len(y_train))).T)
