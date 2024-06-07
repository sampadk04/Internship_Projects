from singleFile import *
from data_transform import data_transform
from scipy import stats
from sklearn.ensemble import ExtraTreesClassifier

def make_predictions(video_path, fps):

    data = singleExtract(video_path=video_path, fps=fps)

    print('Coordinates Extracted..')

    data = data_transform(data, 3, 3)

    print('Data Transformed..')

    # Loading the model
    model = ExtraTreesClassifier(n_estimators=500)
    model.load_model('xgb_33.json')

    print('Model Loaded..')

    result = model.predict(data)

    print(len(result))

    correct_labels = {
        0:'aerobic',
        1:'balance_stability',
        2:'calisthenics',
        3:'coordination_agility',
        4:'flexibility',
        5:'idle',
        6:'weight_bearing',
        7:'weightlifting'
    }

    result = list(result)

    for index,x in enumerate(result):
        result[index] = correct_labels[x]

    data['target'] = result

    print('Predictions ready for RepNet')

    return data

