# import os for file path operations
import os

# import cv2 for image processing
import cv2

# import remove from rembg for background removal
from rembg import remove
# if rembg not present use: pip install rembg

# set variables/hyper-parameters

# folder to save the background removed smp images
smp_bgrem_folder_path = os.path.join('data','smp_bgrem')

def bgrem(img_path, save_folder_path=smp_bgrem_folder_path):
    '''
    Parameters:
        img_path: path to the image to be pre-processed
        save_folder_path: folder to save the background removed smp images
    
    Returns:
        bgrem_img: the background removed image; a numpy array of shape (h, w)
        img_save_path: path to the saved background removed smp image
    '''
    img_name = img_path.split('/')[-1]
    img_save_path = os.path.join(save_folder_path, img_name)
    
    print("")
    print("Reading non-background removed SMP image...")
    # read the image
    img = cv2.imread(img_path)
    # extract dimensions of the image
    h,w,_ = img.shape
    
    print("")
    print("Removing background...")
    # remove the background
    bgrem_img = remove(img)

    # reshape the image to have height and width as a multiple of 16 (required by Edge Detector)
    h += (16 - h%16) % 16
    w += (16 - w%16) % 16
    # resizing the image
    bgrem_img = cv2.resize(bgrem_img, (w,h))

    
    print("")
    print("Saving background removed SMP image...")
    # save the bgrem image
    cv2.imwrite(img_save_path, bgrem_img)

    return bgrem_img, img_save_path


if __name__=='__main__':
    # set the path to the test image to be background removed
    img_path = os.path.join('data', 'smp_input', 'test.jpg')

    # call the bgrem function onto the test image
    bgrem_img = bgrem(img_path=img_path)