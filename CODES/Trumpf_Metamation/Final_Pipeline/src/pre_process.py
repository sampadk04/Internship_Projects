# import os for file path operations
import os

# import cv2 for image processing
import cv2

# import numpy for array operations
import numpy as np

# import Image from PIL for image processing
from PIL import Image

import torch
# importing Dataset, DataLoader
from torch.utils.data import Dataset, DataLoader, TensorDataset
# create datasets using `ImageFolder`
from torchvision.datasets import ImageFolder
# import compose and other transformations
from torchvision.transforms import Compose, RandomResizedCrop, RandomHorizontalFlip, ToTensor, Resize, Normalize

# set variables/hyper-parameters

# set the mean and standard deviation of the images in the dataset
mean = np.array([0.5, 0.5, 0.5])
std = np.array([0.25, 0.25, 0.25])

# define the transform on the image before feeding into the classifier
data_transform = Compose([
    Resize(256), # resize the image to 256x256
    RandomResizedCrop(224), # randomly crop the image to 224x224
    RandomHorizontalFlip(), # randomly flip the image horizontally
    ToTensor(), # convert the image to a tensor
    Normalize(mean, std) # normalize the image
])

def classifier_preprocess(img_path, data_transform=data_transform):
    '''
    Parameters:
        img_path: path to the image to be pre-processed
        data_transform: the transform to be applied on the image
    
    Returns:
        img: the pre-processed image; a tensor of shape (1, 3, 224, 224)
    '''
    print("")
    print("Reading Image...")
    img = Image.open(img_path)
    
    # transform the image
    print("")
    print("Transforming Image...")
    img = data_transform(img)
    
    # add batch dimension
    img = img.unsqueeze(0)

    return img

# set variables/hyper-parameters

# pixel padding to be added to minimum contrast to obtain threshold
padding=175
# folder to save the transformed cad images
cad_files_transformed_folder_path = os.path.join('data','cad_library', 'transformed_library')

def cad_files_preprocess(img_path, padding=padding, save_folder_path=cad_files_transformed_folder_path):
    '''
    Parameters:
        img_path: path to the image to be pre-processed
        padding: pixel padding to be added to minimum contrast to obtain threshold
        save_folder_path: folder to save the transformed cad images
    
    Returns:
        img: the pre-processed image; a numpy array of shape (h, w)
    '''
    img_name = img_path.split('/')[-1]
    img_save_path = os.path.join(save_folder_path, img_name)
    
    # read as a grayscale image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # extract the dimensions
    h,w = img.shape

    # flip the contrast
    img = cv2.bitwise_not(img)

    # extract minimum contrast
    min_contrast = np.min(img)

    # set threshold to minimum contrast + padding (175)
    threshold = min_contrast + padding

    for i in range(h):
        for j in range(w):
            if img[i][j] > threshold:
                img[i][j] = 255
            else:
                img[i][j] = 0

    # save the image
    cv2.imwrite(img_save_path, img)
    
    # return the image
    return img