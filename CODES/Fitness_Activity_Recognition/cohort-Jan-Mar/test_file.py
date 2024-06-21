import numpy as np
import xgboost_model

config_num = str(1)
test_size = 0.25
train_test_data_dir = f'TrainTestData/config_{config_num}/test_size{str(test_size)}'
X_train = np.load(train_test_data_dir + f'/X_train_{str(test_size).replace(".", "_")}.npy')
X_test = np.load(train_test_data_dir + f'/X_test_{str(test_size).replace(".", "_")}.npy')
y_train = np.load(train_test_data_dir + f'/y_train_{str(test_size).replace(".", "_")}.npy')
y_test = np.load(train_test_data_dir + f'/y_test_{str(test_size).replace(".", "_")}.npy')

if __name__ == '__main__':
    # print(X_train.shape)
    model, predictions, preds_probs, accuracy, f1, precision, recall = xgboost_model.model_xgb(X_train, y_train, X_test,
                                                                                               y_test,
                                                                                               config=config_num,
                                                                                               cf_matrix=True)
