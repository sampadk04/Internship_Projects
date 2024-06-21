import os
import pandas as pd
import cv2
import mediapipe as mp
import warnings
warnings.filterwarnings("ignore")

def createDf():
        df = pd.DataFrame()
        df['video_id'] = 0
        df['frame_count'] = 0
        df['fps'] = 0
        for i in range(99):
            df[i] = 0
        return df

def single_ret_Coord(video_id,fps, frame, landmarks):
    result = []
    result.append(video_id)
    result.append(frame) # frame_count
    # fps
    result.append(fps)
    for lndmk in landmarks:
        result.append(float(str(lndmk).split('\n')[0].split(':')[1][1:]))
        result.append(float(str(lndmk).split('\n')[1].split(':')[1][1:]))
        result.append(float(str(lndmk).split('\n')[2].split(':')[1][1:]))
    return result

def singleExtract(video_path, fps):
    mp_pose = mp.solutions.pose
    df = createDf()
    cap = cv2.VideoCapture(video_path)
    count = 0
    with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:
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
            df.loc[len(df.index)] = single_ret_Coord(1,fps,count,results.pose_landmarks.landmark)
    return df