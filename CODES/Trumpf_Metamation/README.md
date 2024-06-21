# Trumpf Metamation Project 2022-2023: Sheet Metal Part Identification using Machine Learning

## Project Overview

This project aims to develop a pipeline for classifying sheet metal parts and returning the corresponding CAD file using machine learning techniques. The primary objectives are to improve accuracy, save time, and reduce costs in the manufacturing process by automating the classification and handling of sheet metal parts.

## Team Members

- **Priyadharsshni**
- **Sampad Kumar Kar**
- **Shankar Ram Vasudevan**

## Project Guide

- **Sanjiv Doraiswamy**, Trumpf Metamation

## Organization

- **Trumpf Metamation**
- SIPCOT IT Park, Siruseri, Chennai

## Internship Period

- 2022-23

## Contents

1. [Objective](#1-objective)
2. [Introduction](#2-introduction)
   - [Image Processing](#21-image-processing)
   - [Fundamentals of Machine Learning](#22-fundamentals-of-machine-learning)
   - [Computer Vision](#23-computer-vision)
3. [Work Done](#3-work-done)
   - [Preparation and Background Research](#31-preparation-and-background-research)
   - [Data Collection](#32-data-collection)
   - [Model Building](#33-model-building)
4. [Results](#4-results)
5. [Future Work](#5-future-work)
6. [Acknowledgements](#6-acknowledgements)

## 1. Objective

The main objective of this project is to create a pipeline that can accurately classify a given image as a sheet metal part or not, and output the corresponding CAD file if it is. The problem can be broken down into three steps:
1. Collect relevant labeled data (images) and apply pre-processing techniques.
2. Choose the appropriate model architecture and optimize it for accuracy.
3. Deploy the model and make it accessible to customers.

## 2. Introduction

### 2.1 Image Processing

Image processing involves manipulating and analyzing digital images using mathematical algorithms. Techniques used include image enhancement, contrast correction, and perspective warping.

### 2.2 Fundamentals of Machine Learning

- **Classical ML**: Techniques like linear regression, logistic regression, SVMs, and decision trees.
- **Deep Learning**: Neural networks, especially Convolutional Neural Networks (CNNs), which are useful for image recognition and classification.

### 2.3 Computer Vision

Computer vision enables computers to process visual data, capturing complex patterns using image processing, classical ML, and deep learning.

## 3. Work Done

### 3.1 Preparation and Background Research

Courses completed:
- Image Processing (Prof. Kavita Sutar, CMI)
- Python for Data Science and Machine Learning Bootcamp (Udemy)
- Intro to Deep Learning with PyTorch (Udacity)

### 3.2 Data Collection

Images of sheet metal parts were collected using the Bing image search API and manually sorted. Data augmentation techniques were applied to produce a dataset for model training.

### 3.3 Model Building

#### Phase I: Classification of Images as SMP/Non-SMP

A ResNet18 model pre-trained on ImageNet was used for classification, achieving a test accuracy of 96.5%.

#### Phase II: Matching SMP with Corresponding CAD Files

Various edge detection and matching algorithms were tested. The U2-net model was used for background removal.

## 4. Results

- **Phase I**: ResNet18 achieved a test accuracy of 96.5%.
- **Phase II**: U2-net successfully removed backgrounds from complex images, and DexiNed was used for edge detection.

## 5. Future Work

Future plans include deploying a web application for identifying sheet metal parts in images, storing the corresponding CAD files, and making the app accessible via a web URL.

## 6. Acknowledgements

We express our sincere appreciation to everyone who contributed to this project, including Sanjiv Doraiswamy, Wolf Wadehn, Nancy Kuriakose, and the staff at Trumpf Metamation.