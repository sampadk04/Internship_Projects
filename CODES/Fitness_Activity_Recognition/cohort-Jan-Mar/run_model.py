import numpy as np
import xgboost_model
import yaml
import pickle
import os

with open("config.yaml") as f:
    config = yaml.safe_load(f)

train_test_data_dir = f'TrainTestData/config_{config.get("config_num")}_frames{config.get("frames")}_steps{config.get("steps")}/test_size{str(config.get("test_size"))}'
X_train = np.load(train_test_data_dir + f'/X_train_{str(config.get("test_size")).replace(".", "_")}.npy')
X_test = np.load(train_test_data_dir + f'/X_test_{str(config.get("test_size")).replace(".", "_")}.npy')
y_train = np.load(train_test_data_dir + f'/y_train_{str(config.get("test_size")).replace(".", "_")}.npy')
y_test = np.load(train_test_data_dir + f'/y_test_{str(config.get("test_size")).replace(".", "_")}.npy')

if __name__ == '__main__':
    print(f"Running Model for {config.get('config_num')} config, for {config.get('frames')} frame and {config.get('steps')}")
    xgb_model, predictions, preds_probs, accuracy, f1, precision, \
    recall = xgboost_model.model_xgb(X_train,
                                     y_train,
                                     X_test,
                                     y_test,
                                     configuration=config.get('config_num'),
                                     cf_matrix=True)

    trained_models_dir = f'trained_models_dir/config_num{config.get("config_num")}/'
    isExist = os.path.exists(trained_models_dir)
    if not isExist:
        os.makedirs(trained_models_dir)
        print('directory_created!')

    file_name = f"xbg_model{config.get('config_num')}_config_{config.get('frames')}_frames_{config.get('steps')}_steps"

    # save
    pickle.dump(xgb_model, open(trained_models_dir + file_name, "wb"))



