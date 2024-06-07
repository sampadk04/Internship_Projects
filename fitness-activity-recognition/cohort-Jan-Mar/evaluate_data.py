import os
import pandas as pd

"""
df = pd.read_csv('csv_files/video_annotated.csv')
remove = df[df['name'].str.contains('.avi', regex=False)].video_id.unique().tolist()
df = df[~df['video_id'].isin(remove)]
df = df.reset_index(drop=True)
"""

DataFromFile = pd.read_csv('csv_files/data_for_model.csv')

remove_from_target1 = ['doubt', 'remove']
data_config1 = DataFromFile[~DataFromFile['target'].isin(remove_from_target1)]

remove_from_target2 = ['doubt', 'remove', 'yoga/strectching', 'idle_lyingdown', 'idle_sitting']
data_config2 = DataFromFile[~DataFromFile['target'].isin(remove_from_target2)]

if __name__ == "__main__":
    print(data_config1.groupby(['target']).size())
    print("-------------------------------------")
    print("-------------------------------------")
    print("-------------------------------------")
    print(data_config2.groupby(['target']).size())
