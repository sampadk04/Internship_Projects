# Making video name to video_id dictionary
import os
import sys
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import time
import pandas as pd

videos_dir = "G:\\My Drive\\Fellowship AI\\Mirror Training App Activity Recognition\\dataset\\annotated videos- " \
             "Main\\videos"

model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']


def get_single_video_statistics(single_file_path):
    """
    This function gets basic statistics of a single video.
    :param single_file_path: Path of single video file
    :return: basic statistics in the form of a dictionary
    """
    cap = cv2.VideoCapture(single_file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    minutes = int(duration / 60)
    seconds = duration % 60
    cap.release()

    single_vid_stats_dictionary = {'fps = ': str(fps), 'number of frames = ': str(frame_count),
                                   'duration (S) = ': str(duration),
                                   'duration (M:S) = ': str(minutes) + ':' + str(seconds)}

    return single_vid_stats_dictionary


def get_directory_videos_statistics(video_directory):
    """
    This function iterates through a directory of videos
    :param video_directory: path where all videos are located
    :return: dictionary of time statistics for given path
    """
    total_time_secs = 0
    for index, video_name in enumerate(os.listdir(video_directory)):
        cap = cv2.VideoCapture(video_directory + "\\" + video_name)
        fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        try:
            duration = frame_count / fps
            minutes = int(duration / 60)
            seconds = duration % 60
            cap.release()
            total_time_secs += seconds
        except ZeroDivisionError:
            pass

    total_time = time.gmtime(total_time_secs)
    directory_stats_dictionary = {'Total duration (S) = ': str(total_time_secs),
                                  'Total duration (H:M:S)': f'{time.strftime("%H:%M:%S", total_time)}'}

    return directory_stats_dictionary


def create_video_id_dict(video_data_path):
    """
    This function creates a dictionary of unique video id's for a given path
    :param video_data_path: path from where videos are located
    :return: video id dictionary
    """
    video_id = {}
    count = 1
    for video in os.listdir(video_data_path):
        if video not in video_id:
            video_id[video] = count
            count += 1
        else:
            print(f"Video with file name {video} already exists")
    return video_id


def process_annotated_excel(excel_file, created_id_dictionary):
    """
    This function processes an excel file that was manually annotated and adds video ids for each video
    :param excel_file: manually annotated excel file containing the name of the file and manually annoated poses
    at specific time stamps
    :param created_id_dictionary:
    :return:
    """
    df = pd.read_excel(excel_file, engine='openpyxl')
    # Adding video_id and time columns
    video_id_list = []
    for x in df['name']:
        try:
            if '.avi' in x:
                video_id_list.append(created_id_dictionary[x])
            else:
                video_id_list.append(created_id_dictionary[x + '.mp4'])
        except KeyError:
            print("Video Annotation Missing for id ", x + '.mp4')
            video_id_list.append(0)

    # Inserting video id
    df.insert(1, "video_id", video_id_list)

    # Find the length of video by counting the annotations
    df.insert(2, "Length", list(df.notnull().sum(axis=1) - 2))

    # Dropping columns (video) details that cann't be used
    df.drop(df[df['video_id'] == 0].index, inplace=True)
    df = df.reset_index(drop=True)
    df.head()

    # Saving them as video_annotated csv for future use
    df.to_csv("new_csv_files/video_annotated_processed.csv", index=False)
    video_annotated_processed_df = df
    return video_annotated_processed_df


def videos_pose_estimation_coordinates(annotated_df, all_vids_path):
    """
    This function iterates through the names of a dictionary of annotated videos, finds the corresponding video in
    a given directory and creates movenet keypoints. All 2d points for all videos are saved to a csv file.
    :param annotated_df: Dataframe of all manually annotated videos
    :param all_vids_path: path containing all videos
    :return: N/A
    """
    data = pd.DataFrame()

    for i in range(0, annotated_df.shape[0]):
        if '.avi' in annotated_df['name'][i]:
            path = all_vids_path + '\\' + annotated_df['name'][i]
        else:
            path = all_vids_path + '\\' + annotated_df['name'][i] + '.mp4'

        vid_id = int(annotated_df['video_id'][i])
        length = int(annotated_df['Length'][i])
        actions = list(annotated_df.iloc[i][3: length + 3])

        cap = cv2.VideoCapture(path)

        if not cap.isOpened():
            print("Error opening video stream or file")

        fps = int(cap.get(cv2.CAP_PROP_FPS))

        vid_id_list = []
        points = []
        fps_list = []
        frame_list = []
        action_list = []
        max_frames = fps * length

        frame_count = 1
        seconds = 0
        while cap.isOpened():
            success, frame = cap.read()

            if not success or frame_count > max_frames:
                break

            # Resize image
            img = frame.copy()
            img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 384, 640)
            input_img = tf.cast(img, dtype=tf.int32)

            # Detection section
            results = movenet(input_img)
            keypoints_with_scores = results['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))

            points.append(keypoints_with_scores[0][:, :2].flatten())

            vid_id_list.append(vid_id)
            fps_list.append(fps)
            frame_list.append(frame_count)
            action_list.append(actions[seconds])

            if frame_count % fps == 0:
                seconds += 1

            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()

        sub = pd.DataFrame(points)
        sub.insert(0, 'fps', fps_list)
        sub.insert(0, 'frame_count', frame_list)
        sub.insert(0, 'video_id', vid_id_list)
        sub['actions'] = action_list

        data = data.append(sub, ignore_index=True)
        print(f"Annotated {i + 1} videos out of {annotated_df.shape[0]}")

    data.to_csv("new_csv_files/coordinates.csv", index=False)


if __name__ == "__main__":
    video_annotated_excel = 'csv_files/videos_annotated.xlsx'
    id_dictionary = create_video_id_dict(videos_dir)
    # processed_df = process_annotated_excel(video_annotated_excel, id_dictionary)
    processed_df = pd.read_csv('csv_files/video_annotated_processed.csv')
    videos_pose_estimation_coordinates(processed_df, videos_dir)
