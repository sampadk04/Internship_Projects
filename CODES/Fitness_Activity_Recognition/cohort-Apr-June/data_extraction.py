import os
import pandas as pd
import cv2
import mediapipe as mp
import warnings
warnings.filterwarnings("ignore")

class extractData:
    
    def __init__(self, path, annotated, coordinates):
        self.path = path
        self.annotated = annotated
        self.coordinates = coordinates
    
    def getFiles(self):
        return os.listdir(self.path)
    
    def createDf(self):
        df = pd.DataFrame()
        df['video_id'] = 0
        df['frame_count'] = 0
        df['fps'] = 0
        for i in range(99):
            df[i] = 0
        return df

    def ret_Coord(self, video_id, frame, landmarks):
        result = []
        result.append(int(video_id)) # video_id
        result.append(frame) # frame_count
        # fps
        result.append(self.coordinates.iloc[self.coordinates.loc[self.coordinates['video_id'] == video_id].index[0]].fps)
        for lndmk in landmarks:
            result.append(float(str(lndmk).split('\n')[0].split(':')[1][1:]))
            result.append(float(str(lndmk).split('\n')[1].split(':')[1][1:]))
            result.append(float(str(lndmk).split('\n')[2].split(':')[1][1:]))
        return result
    
    def extract3DCoord(self):
        # mp_drawing = mp.solutions.drawing_utils
        # mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose
        data = self.createDf()
        files = self.getFiles()
        df = self.createDf()
        for video in files:
            video_path = self.path + str(video)
            try:
                videoid = int(self.annotated.loc[self.annotated['name'] == video[:-4]].video_id)
            except:
                continue
                
            if len(data.loc[data['video_id'] == videoid]) <= 0:
                print(videoid)
                cap = cv2.VideoCapture(video_path)
                count = 0

                # checking the frame in advance
            #     if int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != len(coordinates.loc[coordinates['video_id'] == videoid].actions):
            #         print(videoid)
            #         continue
                with mp_pose.Pose(
                    min_detection_confidence=0.3,
                    min_tracking_confidence=0.3) as pose:
                    while cap.isOpened():
                        success, image = cap.read()
                        if not success:
                            print("Ignoring empty camera frame.")
                            break      
                        count += 1
                        # To improve performance, optionally mark the image as not writeable to
                        # pass by reference.
                        image.flags.writeable = False
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        results = pose.process(image)
                        # this prints the x, y, z coordinates of the each joints for each frame within the visibility feature as well
                        # Draw the pose annotation on the image.
                        if not results.pose_landmarks:
                            continue
                        df.loc[len(df.index)] = self.ret_Coord(videoid,count,results.pose_landmarks.landmark)

                # making sure df and coordinates have same rows for distinct video_id        
                if len(df) > len(self.coordinates.loc[self.coordinates['video_id'] == videoid].actions):
                    diff = len(df)-len(self.coordinates.loc[self.coordinates['video_id'] == videoid].actions)
                    for x in range(1,diff+1):
                        df.drop(len(df)-x, inplace=True)
                    df['actions'] = list(self.coordinates.loc[self.coordinates['video_id'] == videoid].actions)
                    data = pd.concat([data, df], ignore_index = True)

                elif len(df) < len(self.coordinates.loc[self.coordinates['video_id'] == videoid].actions):
                    diff = len(self.coordinates.loc[self.coordinates['video_id'] == videoid].actions) - len(df)
                    df['actions'] = list(self.coordinates.loc[self.coordinates['video_id'] == videoid].actions)[:-diff]
                    data = pd.concat([data, df], ignore_index = True)

                else:
                    df['actions'] = list(self.coordinates.loc[self.coordinates['video_id'] == videoid].actions)
                    data = pd.concat([data, df], ignore_index = True)
                df = self.createDf()
                cap.release()
            else:
                continue
        return data