# import os for file path operations
import os

# import shutil to copy files
import shutil

# import subprocess to run shell commands
import subprocess

# import warnings to ignore warnings
import warnings

# function to clear and create a directory
from src.utils import create_or_clear_dir

# we will be using DexiNed Edge Detector:
'''
DexiNed Edge Detector: https://github.com/xavysp/DexiNed
'''

# set variables/hyper-parameters

# folder paths where the edge detector will save the edge detected images
destination_folders = {
    'avg':os.path.join('models', 'edge_detector', 'DexiNed', 'result', 'BIPED2CLASSIC', 'avg'),
    'fused':os.path.join('models', 'edge_detector', 'DexiNed', 'result', 'BIPED2CLASSIC', 'fused')
}

# folder paths where the edge detected images by the edge detector will be copied from the destination folders
smp_edge_detected_folders = {
    'avg':os.path.join('data', 'smp_edge_detected', 'avg'),
    'fused':os.path.join('data', 'smp_edge_detected', 'fused')
}

# folder path where the edge detector is located
edge_detector_folder_path = os.path.join('models', 'edge_detector', 'DexiNed')

# name of the virtual environment
# virtual_env_name = '.venv'

def edge_detect(bgrem_img_path, save_folder_paths=smp_edge_detected_folders, edge_detector_folder_path=edge_detector_folder_path):
    '''
    Parameters:
        bgrem_img_path: path to the background removed image
        save_folder_paths: folder paths where the edge detected images by the edge detector will be saved
        edge_detector_folder_path: folder path where the edge detector is located

    Returns:
        None

    Note:
        Make sure to activate the virtual environment (containing the relevant libraries) before running this function
    '''
    # set source_folder_path: folder to copy the background removed image for the edge detector to process as inputs
    source_folder_path = os.path.join(edge_detector_folder_path, 'data')

    # folder paths where the edge detector will save the edge detected images
    destination_folder_paths = {
        'avg':os.path.join(edge_detector_folder_path, 'result', 'BIPED2CLASSIC', 'avg'),
        'fused':os.path.join(edge_detector_folder_path, 'result', 'BIPED2CLASSIC', 'fused')
    }
    
    print("")
    print("Create/Clear directories...")
    # first clear all the contents of in the following folders
    create_or_clear_dir(source_folder_path)
    create_or_clear_dir(destination_folder_paths['avg'])
    create_or_clear_dir(destination_folder_paths['fused'])
    create_or_clear_dir(save_folder_paths['avg'])
    create_or_clear_dir(save_folder_paths['fused'])

    # copy the image to source folder
    img_name = bgrem_img_path.split('/')[-1]
    img_copy_path = os.path.join(source_folder_path, img_name)

    # copy the image to the source_folder
    shutil.copy(bgrem_img_path, img_copy_path)

    # run the edge detector in the folder containing edge detector
    subprocess.run(['python', 'main.py', '--choose_test_data=-1'], cwd=edge_detector_folder_path)
    
    print("")
    print("Copying Edge Detected Images...")
    # copy the images from output destination directories to the save_folder
    for filename in os.listdir(destination_folder_paths['avg']):
        src_path = os.path.join(destination_folder_paths['avg'], filename)
        dst_path = os.path.join(save_folder_paths['avg'], filename)
        # copy from source to destination
        shutil.copy(src_path, dst_path)
    
    for filename in os.listdir(destination_folder_paths['fused']):
        src_path = os.path.join(destination_folder_paths['fused'], filename)
        dst_path = os.path.join(save_folder_paths['fused'], filename)
        # copy from source to destination
        shutil.copy(src_path, dst_path)

    print("")
    print('Edge Detection Complete!')


if __name__=='__main__':
    # supress the warnings
    warnings.filterwarnings("ignore")

    # path to the background removed test image
    bgrem_img_path = os.path.join('data', 'smp_bgrem', 'test.jpg')

    # run the edge detector on the background removed test image
    edge_detect(bgrem_img_path=bgrem_img_path)