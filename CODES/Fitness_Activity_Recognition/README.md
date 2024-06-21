# Fitness Activity Recognition
This repository contains all the code developed for the **Fitness Activity Recognition** track as part of the fellowship cohort by LaunchPad AI of the period from Jan-Mar 2022, Apr-Jun 2022 and July-Sep 2022.

### BlazePose: A 3D Pose Estimation Model

![BlazePose](BlazePose.png)

MediaPipe Pose (BlazePose) is a ML solution for high-fidelity body pose tracking, inferring 33 3D landmarks, and background segmentation mask on the whole body from RGB video frames. Each of the landmarks(joints) contains the X, Y and Z coordinates, where Z is the depth. Using this, we converted all the videos into coordinates (99 total on X, Y, and Z axis) per frame and created a new CSV file with all the data extraction points. We created a new column in our CSV with unique name for every video. 

### Google RepNet

![RepNet](EmbeddedImage.gif)

RepNet is a model that takes as input a video that contains periodic action of a variety of classes (including those unseen during training) and returns the period of repetitions found therein. Our proposed application uses RepNet model for counting each class repetitions in videos.

### Demo Video

![Demo](demo_screenshot.png)

This is the screenshot from one of the demo videos we created. It contains the current activity, how long it lasted, and the repetition count from RepNet. Also, it displays the coordinates of the joints as well. You can find more demo videos on the [google drive link](https://drive.google.com/drive/folders/1l14EzbRZ4emgrHJdcT3wXN5v9YKRZG4J?usp=sharing).

### Feature Engineering:

#### 1. Momentum: 

The intuition is the idle states (talking, walking and sitting) tends to have less changes in the cordinates hence the momentum will be less compare to high dynamics workout/activities(running, jumping and push-ups).

![Momentum](Momentum.png)
#### Masking:
Masking was used at the end for some miss-classified prediction in between. We masked maximum 2 wrong prediction in between by taking mode of 5 frames (2 previous frame and 2 coming frame).

![Masking](masking.png)

### What are the different classes?
* aerobic - Any activity that you do for more than a few minutes at a time
  * ex) Swimming, Rowing, Cycling, Dancing, Hiking
* coordination_agility - Any activity that requires to move quickly and easily, helps prevent falls and injuries by improving your reflexes, coordination and focus
  * ex) Quick feet, Side steps, High knees, Lateral crossovers
* weight_bearing - Any activity in which you hold yourself up against gravity 
  * ex) Running, Cross-country skiing, Standing yoga poses, Body-weight squats, Standing bicep curls
* calisthenics - Any activity that are using own body weight as resistance
  * ex) Pull-ups, Planks, Glute bridges, Lunges, Handstands
* balance_stability - Fitness training that tests your ability to stand on one or two legs while moving other parts of your body
  * ex) Split squats, Tai chi, Single-leg deadlifts
* flexibility - Activities that enhances the ability of your muscle to stretch
  * ex) Yoga, Stretching
* weightlifting - Lifting weights
  * ex) Rows, Dumbbell lunges, Bench Press, Deadlift
* idle - Not on any activity status
  * ex) Standing, Talking

### Classifier

For the task of  multi-class classification of our preprocessed data ExtraTrees has been used. Earlier, the last cohort had used XGBoost which didn't gave good results with BlazePose/Mediapipe coordinates. But after testing several classifiers like SVM, catBoost, MultiLayer Perceptrons or Artificial Neural Networks we concluded with ExtraTrees as our classifier. <br/>
The reasons we choose ExtraTrees as our classifier are:

* ExtraTrees takes lesser time to train.
* We were able to get an accuracy of 97% with ExtraTrees.
* Highest F1 score that means lower mis-classification rate.

# Cohort: July-Sep 2022 (My Work)

## Project Overview

This project focuses on comparing fitness videos using Dynamic Time Warping (DTW) to assess the similarity between a trainee's performance and a trainer's demonstration. The goal is to develop a scoring system that quantifies how closely the trainee's movements match the expert's.

## What is DTW?

Dynamic Time Warping (DTW) is a technique used to measure the similarity between two sequences, which may vary in time or speed. It calculates the optimal match between two sequences by allowing for stretching and compressing of the time axis. This makes DTW particularly useful for comparing time series data of different lengths.

## Methodology

### How DTW Works

DTW compares the similarity by calculating the distance between two arrays or time series of different lengths. Instead of a one-to-one mapping, DTW employs a many-to-one or one-to-many strategy to minimize the total distance between the two series.

For example, if two sequences follow the same pattern but are of different lengths, DTW can align them by stretching or compressing certain parts of the sequences to achieve the best match.

### Application in Our Project

The project aims to compare two videos – one of a trainer and one of a trainee – to determine how similar the trainee's movements are to the trainer's. By treating the videos as collections of frames over time, they can be analyzed as time-series data, making DTW a natural choice for this comparison.

## Data

We used three different videos for preliminary comparisons:
1. **Trainer Video**: A video of the trainer performing bicep curls.
2. **Trainee Video with Correct Form**: A video of a trainee performing bicep curls with the correct form.
3. **Trainee Video with Incorrect Form**: A video of a trainee performing bicep curls with incorrect form.

These videos serve as a baseline to test the preliminary results of DTW.

## Implementation

The implementation involves the following steps:

1. **Data Collection**: Gather videos of the trainer and trainee performing the same exercise.
2. **Preprocessing**: Convert videos into a series of frames and extract relevant features.
3. **DTW Algorithm**: Apply the DTW algorithm to compare the time series data from the trainer and trainee videos.
4. **Scoring**: Calculate a score representing the similarity between the trainer's and trainee's performance.

## Conclusion

This project demonstrates the use of DTW for fitness activity recognition by comparing trainee performance to expert demonstrations. The approach can be extended to various exercises and used to provide real-time feedback in fitness applications.

