import pandas as pd
import numpy as np
from scipy import stats
def data_transform(data, n, step):
    

    segments = []
    labels = []
    video_id = []
    for id in data['video_id'].unique():
        sub_set = data[data["video_id"] == id]
        for i in range(0, sub_set.shape[0] - n, step):

            values = ((sub_set.iloc[i+n, 3:102] - sub_set.iloc[i, 3:102]) / sub_set.iloc[i+n, 3:102])

            # label = stats.mode(sub_set['target'][i: i+n])[0][0]

            #video_id.append(id)
            segments.append([values.append(sub_set.iloc[i+n, 3:102])])
            # labels.append(label)
    
            

    reshaped_segments = np.asarray(segments, dtype = np.float32).reshape(-n,198)
    #video_id = np.asarray(video_id)
    df = pd.DataFrame(reshaped_segments)
    #df.insert(0, "video_id", video_id)
    # df['target'] = labels  
    
    return(df)