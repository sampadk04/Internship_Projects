import os
import cv2
import mediapipe as mp
import numpy as np
import time

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
FONT_COLOR = (255, 0, 0)
LINETYPE = 2

##### PARAMS #####
scale = 1 # to resize video
filepath = 'dataset/UCF101-small/raw/PushUps/v_PushUps_g25_c02.avi'
##################

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(filepath)

prev_frame_time = 0
fps = 0
frameCounter = 0

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False) as pose:
  
  while cap.isOpened():
    success, image = cap.read()
    
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      break

    # Calculate frame rate
    height, width, _ = image.shape
    curr_frame_time = time.time()
    fps += round(1 / (curr_frame_time - prev_frame_time))
    prev_frame_time = curr_frame_time
    frameCounter += 1

    if scale is not None:
        image = cv2.resize(
            image, (int(width * scale), int(height * scale))
        )

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    
    # Display frame rate
    cv2.putText(
        image,
        f"FPS: {str(fps//frameCounter)}",
        (image.shape[1] - 90, 30),
        FONT,
        FONT_SCALE,
        FONT_COLOR,
        LINETYPE,
    )
    
    cv2.imshow('Pose', image)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
