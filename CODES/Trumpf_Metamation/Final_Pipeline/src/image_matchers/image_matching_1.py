# import os, glob for file path operations
import os, glob

# import priority queue
import heapq

# import cv2 for image processing
import cv2

# import PIL for image processing
from PIL import Image

# import numpy for array operations
import numpy as np

# import imagehash for image hashing operations
import imagehash

# set variables/hyper-parameters

# path to the folder containing the CAD library
cad_library_folder_path = os.path.join('data','cad_library', 'transformed_library')

# extensions of the images in the CAD library
extensions = ['jpg', 'jpeg', 'png']

def match_image(img_path, top_k=5, cad_library_folder_path=cad_library_folder_path, extensions=extensions):
    '''
    Parameters:
        img_path: path to the image to be matched
        top_k: number of top matches to return
        cad_library_folder_path: path to the folder containing the CAD library
        extensions: extensions of the images in the CAD library
    
    Returns:
        top_k_matches_paths: list of paths to the top k matches
        best_match_path: path to the best match
    '''
    img = Image.open(img_path)

    print("")
    print("Matching the image at path: ", img_path)

    # extract hash of the image to be matched
    img_hash = imagehash.average_hash(img)

    # extract the paths to the images in the CAD library
    cad_image_paths = []
    for ext in extensions:
        cad_image_paths.extend(glob.glob(os.path.join(cad_library_folder_path, '*.'+ ext)))

    # initialize the best confidence to -infinity
    best_confidence = - np.inf
    # set index of the best match to None
    best_idx = None

    # we want to find top k matches 
    k = top_k
    # initalize a priority queue to store the top k matches
    top_k_matches = []

    for i in range(len(cad_image_paths)):
        # read the current cad image
        curr_img = cv2.imread(cad_image_paths[i])

        # resize the current cad image to (128, 128)
        template = cv2.resize(curr_img, (128,128), cv2.INTER_LINEAR)

        # convert Numpy array to PIL image
        template = Image.fromarray(template)

        # calculate the hash of the current cad image
        curr_hash = imagehash.average_hash(template)

        # calculate the hash difference between the image to be matched and the current cad image
        curr_confidence = -np.abs(img_hash - curr_hash)

        if len(top_k_matches) < k: # if the priority queue is not full
            heapq.heappush(top_k_matches, (curr_confidence, i))
        else: # if the priority queue is full
            # if the current confidence is greater than the kth largest confidence (kth largest confidence is at the root of the priority queue)
            if curr_confidence > top_k_matches[0][0]:
                # pop the ex-kth largest confidence
                heapq.heappop(top_k_matches)
                # push the current kth largest confidence
                heapq.heappush(top_k_matches, (curr_confidence, i))
            
            # check if the current confidence is greater than the best confidence
            if curr_confidence > best_confidence:
                # update the best confidence
                best_confidence = curr_confidence
                # update the index of the best matchx
                best_idx = i

    # print the confidence of the top k matches
    print("")
    print("Confidence of the top {} matches based on Image Hashing:".format(k))
    for i in range(len(top_k_matches)):
        print("Match {}: {}".format(i+1, top_k_matches[i][0]))
    
    # create a list to store the paths to the top k matches
    top_k_matches_paths = [cad_image_paths[top_k_matches[i][1]] for i in range(len(top_k_matches))]

    # best match cad file path
    best_match_path = cad_image_paths[best_idx]

    # print the confidence of the best match
    print("")
    print("Confidence of the best match: {}".format(best_confidence))

    return top_k_matches_paths, best_match_path