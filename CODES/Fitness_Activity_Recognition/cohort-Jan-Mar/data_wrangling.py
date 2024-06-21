import os
import sys
import warnings

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import transition_to_standing

warnings.filterwarnings('ignore')


def convert_categories_to_base_classes(input_df):
    req = input_df.iloc[:, 3:].values.tolist()
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

    count['base_classes'] = count['actions'].apply(lambda x: transition_to_standing.change_actions(x))

    # Seeing the current target labels
    count.groupby(['base_classes'])[0].sum()


def create_final_data(path_to_coordinates):
    data = pd.read_csv(path_to_coordinates, index_col=0)
    # print(data.columns)
    # sys.exit()
    data.dropna(axis=0, inplace=True)

    data['target'] = data['actions'].apply(lambda x: transition_to_standing.change_actions(x))
    data.drop(['actions'], axis=1, inplace=True)

    return data


def create_null_counts_plot(all_data):
    plt.figure(figsize=(16, 6))
    sns.heatmap(all_data.isnull())

    plots_dir = f'plots_dir/'
    isExist = os.path.exists(plots_dir)
    if not isExist:
        os.makedirs(plots_dir)
        print(plots_dir + 'directory_created!')

    plt.savefig(plots_dir + "/null_counts.jpg")
    plt.close()


if __name__ == '__main__':
    coordinates_file = 'new_csv_files/coordinates.csv'
    final_data = create_final_data(coordinates_file)
    final_data.to_csv('new_csv_files/data_for_model.csv')

