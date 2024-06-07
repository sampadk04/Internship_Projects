from pyparsing import col
from sklearn.metrics import top_k_accuracy_score
from data_extraction import extractData
from classify import make_predictions
from model import buildModel
import pandas as pd
from createVideo import video_output

# -------------------------------- READ FILES BELOW TO USE DATA WITH ANNOTATIONS --------------------------------

annotated = pd.read_csv('Data/annotated.csv')
coordinates = pd.read_csv('Data/coordinates.csv', index_col=0)
data = pd.read_csv('Data/blazepose_coordinates_main.csv', index_col=0)

# -------------------------------- CREATE DATA FILE WITH 3D COORDINATES --------------------------------
# NOTE: THIS STEP CAN TAKE A LONG TIME TO COMPLETE, RUN THIS SEPERATELY AND SAVE TO CSV TO BE USED IN THE NEXT STEP 

# dt = extractData(
#     path = '/Users/devanshsharma/Desktop/Code/Data/fitnessVideos',
#     annotated = annotated,
#     coordinates = coordinates
#     )

# data = dt.extract3DCoord()
# data.to_csv('3d_coords.csv')
# print(data.shape)

# -------------------------------- USING DATA EXTRACTED ABOVE, CREATE AND TRAIN MODEL --------------------------------

bm = buildModel(
    annotated=annotated,
    data=data,
    test_split=0.25,
    n=3,
    step=3,
    save_name='extraTrees_33.json'
)

bm.trainModel()

# -------------------------------- MAKE PREDICTIONS FOR ANY GIVEN VIDEO --------------------------------

data = make_predictions('/Users/devanshsharma/Desktop/Code/Data/fitnessVideos/kg_total_bodyblast1_11.mp4', 29)

# -------------------------------- REPNET WORK --------------------------------

# NOTE: NEXT STEPS INVOLVE REPNET. YOU WILL HAVE TO SAVE THE EXTRACTED COORDINATES WITH PREDICTIONS BELOW 

data.to_csv('data.csv')

# VISIT: https://colab.research.google.com/drive/14WWVUbVBsnRTVMQVwrRkw_A87AJRgmR6?usp=sharing AND FOLLOW STEPS MENTIONED

total_count = pd.read_csv('total_count.csv', index_col=False, names=['Count'])

video_output()