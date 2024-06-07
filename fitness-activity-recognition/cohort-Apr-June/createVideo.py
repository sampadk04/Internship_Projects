from data_transform import data_transform
import cv2
from scipy import stats
from singleFile import singleExtract
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def mark_false(image, pose):
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    return results

def video_output(n, step, model, outPath, video_path, total_count):
    # Predicting
    test_df = singleExtract(video_path=video_path, fps=fps)
    test_df = data_transform(test_df,n,step)
    result = model.predict(test_df)
    shape = result.shape[0]
    pred_list=[]
    
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_path)
    time = clip.duration
    
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
    pred_list = []

    shape = len(result)
    frame_to_stack = int(round(shape/time))
    
    for i in range(0, shape, frame_to_stack):
        pred_list.append(stats.mode(result[i: i+frame_to_stack])[0][0])
    
    pred_masked = pred_list[:]
    
    # Masking used at the end for some miss-classified prediction in between
    
    for i in range(1,len(pred_list)-1):
        if ((pred_masked[i] != pred_masked[i-1]) and (pred_masked[i] != pred_masked[i+1]) and (pred_masked[i-1] == pred_masked[i+1])):
            pred_masked[i] = pred_masked[i-1]

        if ((pred_masked[i] != pred_masked[i-1]) and (pred_masked[i] != pred_masked[i+1]) and (pred_masked[i-1] != pred_masked[i+1])):
            pred_masked[i] = pred_masked[i-1]


    cap = cv2.VideoCapture(video_path)
    fps= int(cap.get(cv2.CAP_PROP_FPS))
    
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter(outPath,cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width,frame_height))
    frame_count = 1
    time_stamp = 0
    for index,x in enumerate(pred_masked):
        pred_masked[index] = correct_labels[x]

    time_spent = {}
    cnt = 0
    with mp_pose.Pose(
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success or time_stamp == len(pred_masked):
                break
            #print(time_spent)
            #Display Text for the labels and time spending for each labels
            cv2.putText(frame, str(pred_masked[time_stamp]),
                                (0, 250),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2, cv2.LINE_AA)

            try:
                cv2.putText(frame, str(time_spent[pred_masked[time_stamp]])+' Seconds',
                                    (0, 300),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2, cv2.LINE_AA)
            except:
                pass
            # we get the count for each frame from total_count    
            cv2.putText(frame, 'Count: ' + str(total_count.iloc[cnt]['Count']),
                            (0, 350),
                            cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2, cv2.LINE_AA)
            cnt += 1

            frame_count+=1
            if frame_count % fps == 0:
                if pred_masked[time_stamp] not in time_spent:
                    time_spent[pred_masked[time_stamp]] = 1
                else:
                    time_spent[pred_masked[time_stamp]] += 1
                time_stamp+=1
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Draws pose estimation joints and connections  
            results = mark_false(frame, pose)
            frame.flags.writeable = True
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            #cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            out.write(image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
                
        print("Video Rendered")
        cap.release()
        out.release()