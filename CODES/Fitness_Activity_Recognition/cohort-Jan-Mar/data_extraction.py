import os
import sys
import warnings

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import transition_to_standing
import params

warnings.filterwarnings('ignore')

annotated_csv_path = "new_csv_files/video_annotated_processed.csv"

df = pd.read_csv(annotated_csv_path)
df = df.reset_index(drop=True)

# This is the section where the we create the parameters lists located in the params file. doubt, idel_standing,
# idle_sitting, idle_lyingdown, workout_standing, workout_transition, workout_lyingdown, workout_yoga_strectching
# remove_spe

req = df.iloc[:, 3:].values.tolist()
flatten = [items for lists in req for items in lists]
flatten = [x for x in flatten if str(x) != 'nan']
count_dict = {}
for action in flatten:
    if action in count_dict:
        count_dict[action] += 1
    else:
        count_dict[action] = 1

count = pd.DataFrame.from_dict(count_dict, orient='index')
count.reset_index(inplace=True)
count = count.rename(columns={'index': 'actions'})

count['idle/workingout'] = count['actions'].apply(lambda x: "idle" if x in params.idle else 'workingout')
count['six_class'] = count['actions'].apply(lambda x: transition_to_standing.change_actions(x))

# Seeing the current target labels
count.groupby(['six_class'])[0].sum()

# Seeing the idle/workout counts
count.groupby(['idle/workingout'])[0].sum()

data = pd.read_csv("csv_files/coordinates.csv", index_col=False)
data.drop("Unnamed: 0", axis=1, inplace=True)
col_names = data.columns.tolist()
index = col_names.index('actions')
new_cols = col_names[:index] + col_names[index + 1:] + [col_names[index]]
data = data[new_cols]
data.dropna(axis=0, inplace=True)

# This line gave an error in the notebook - data = data[~data['video_id'].isin(remove)]
# plt.figure(figsize=(16, 6))
# sns.heatmap(data.isnull())

plots_dir = f'plots_dir/'
isExist = os.path.exists(plots_dir)
if not isExist:
    os.makedirs(plots_dir)
    print(plots_dir + 'directory_created!')

# plt.savefig(plots_dir + "/null_counts.jpg")
# plt.close()

data['target'] = data['actions'].apply(lambda x: transition_to_standing.change_actions(x))
data.drop(['actions'], axis=1, inplace=True)

# remove_from_target = ['doubt', 'remove', 'idle_sitting', 'yoga/strectching']
# data = data[~data['target'].isin(remove_from_target)]

if __name__ == '__main__':
    annotated_csv_path = "new_csv_files/video_annotated_processed.csv"
    data.to_csv('new_csv_files/data_for_model.csv')
    # print(data.groupby(['target']).size())
    # print(data['target'].unique())
