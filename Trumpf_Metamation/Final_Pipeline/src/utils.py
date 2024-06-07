# import os for file path operations
import os
# import shutil to copy files
import shutil

# list of utility functions

def create_or_clear_dir(dir_path):
    '''
    Parameters:
        dir_path: path to the directory to be created or cleared
    
    Returns:
        None
    '''
    # if folder exists, delete the folder
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    # make the directory again
    os.makedirs(dir_path)