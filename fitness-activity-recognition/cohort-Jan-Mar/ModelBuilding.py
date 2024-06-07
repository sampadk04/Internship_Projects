# Annotating the video with output lable
import cv2
import numpy as np
import pandas as pd
from scipy import stats
import tensorflow as tf
import tensorflow_hub as hub

model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']


# To processes the video and retrun the coordinates per frame
def video_processing(name):
    points = []
    cap = cv2.VideoCapture(name)
    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        # Resize image
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 384, 640)
        input_img = tf.cast(img, dtype=tf.int32)

        # Detection section
        results = movenet(input_img)
        keypoints_with_scores = results['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))

        points.append(keypoints_with_scores[0][:, :2].flatten())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("video processed")

    cap.release()
    return points


def video_output(points, name, n, step, model):
    # Predicting
    test_df = pd.DataFrame(points)
    test_df = data_transform(test_df, n, step, test=True)
    result = model.predict(test_df)
    shape = result.shape[0]
    pred_list = []

    cap = cv2.VideoCapture(name)

    fps = int(cap.get(cv2.CAP_PROP_FPS))

    for i in range(0, shape, fps):
        # print(i)
        pred_list.append(stats.mode(result[i: i + fps])[0][0])

    for i in range(1, len(pred_list) - 1):
        if pred_list[i] != pred_list[i - 1] and pred_list[i] != pred_list[i + 1]:
            new = [pred_list[i - 1]] + [pred_list[i + 1]]
            pred_list[i] = stats.mode(new)[0][0]

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    video_out = name[:-4] + "_" + str(n) + "_frame_output.mp4"

    out = cv2.VideoWriter(video_out, cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), fps, (frame_width, frame_height))
    frame_count = 1
    time_stamp = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success or time_stamp == len(pred_list):
            break
        # Display Text
        cv2.putText(frame, str(pred_list[time_stamp]),
                    (10, 100),
                    cv2.FONT_HERSHEY_PLAIN, 8, (0, 0, 255), 5, cv2.LINE_AA)

        out.write(frame)
        frame_count += 1
        if frame_count % fps == 0:
            time_stamp += 1
    print("Video Rendered")
    cap.release()
    out.release()


# Function to return the diffrence in coordinate of xth frame and x+nth frame
def data_transform(data, n, step, test=False):
    if test == False:
        segments = []
        labels = []
        video_id = []
        for id in data['video_id'].unique():
            sub_set = data[data["video_id"] == id]
            for i in range(0, sub_set.shape[0] - n, step):
                values = sub_set.iloc[i: i + n, 3:37].mean()

                label = stats.mode(sub_set['target'][i: i + n])[0][0]

                video_id.append(id)
                segments.append([values])
                labels.append(label)

        reshaped_segments = np.asarray(segments, dtype=np.float32).reshape(-n, 34)
        video_id = np.asarray(video_id)
        return reshaped_segments, labels, video_id

    else:
        segments = []
        for i in range(0, data.shape[0] - n, step):
            values = data[i: i + n].mean()
            segments.append([values])
        reshaped_segments = np.asarray(segments, dtype=np.float32).reshape(-n, 34)
        return reshaped_segments
