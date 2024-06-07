# import os, glob for file path operations
import os, glob

# for reading config files
import yaml

# import argparse for command line arguments parsing and help
import argparse

# import cv2 for image processing
import cv2

# to classify image into smp or non-smp
from src.smp_classifier import smp_classifier

# to remove background from smp images
from src.background_remover import bgrem 

# to detect edges in the background removed smp images
from src.edge_detector import edge_detect

from src.pre_process import cad_files_preprocess

# suppress warnings
import warnings
warnings.filterwarnings("ignore")


##########################################################################################################################


# extract the parameters from the config file
config_file_path = os.path.join('config', 'main.yaml')

with open(config_file_path, 'r') as fh:
    config = yaml.load(fh, Loader=yaml.FullLoader)

# import image matcher based on the index in the config file
if config['image_matcher_index'] == 0:
    from src.image_matchers.image_matching_0 import match_image
elif config['image_matcher_index'] == 1:
    from src.image_matchers.image_matching_1 import match_image


##########################################################################################################################


if __name__ == '__main__':

    # argument parsers
    parser = argparse.ArgumentParser(description='Final Pipeline')

    # add arguments

    ## smp classifier arguments
    parser.add_argument('--img_path', type=str, default=config['img_path'], help='path to the image to be processed')

    parser.add_argument('--smp_classifier_path', type=str, default=config['smp_classifier_path'], help='path to the smp classifier model (.pth file)')

    parser.add_argument('--device', type=str, default=config['device']['mps'], help='device to use for inference (cpu, mps or cuda)')

    parser.add_argument('--class_names', type=list, default=config['class_names'], help='names of the classes (0: non_smp, 1: smp)')

    ## background remover arguments
    parser.add_argument('--bgrem_save_folder_path', type=str, default=config['bgrem_save_folder_path'], help='path to the folder to save the background removed smp images')

    ## edge detector arguments
    parser.add_argument('--edge_detector_save_folder_path', type=str, default=config['edge_detector_save_folder_path'], help='path to the folder to save the edge detected smp images (post background removal)')

    parser.add_argument('--edge_detector_folder_path', type=str, default=config['edge_detector_folder_path'], help='path to the folder containing the edge detector')

    ## preprocessing cad files in the library
    parser.add_argument('--extensions', type=list, default=config['extensions'], help='list of extensions of the cad files in the library')

    parser.add_argument('--raw_cad_lib_folder_path', type=str, default=config['cad_lib_folder_path']['raw'], help='path to the folder containing the raw cad files in the library')

    parser.add_argument('--transformed_cad_lib_folder_path', type=str, default=config['cad_lib_folder_path']['transformed'], help='path to the folder containing the transformed cad files in the library')

    parser.add_argument('--threshold_padding', type=int, default=config['threshold_padding'], help='pixel padding to be added to minimum contrast to obtain threshold for preprocessing cad files in the library')

    ## image matching arguments
    parser.add_argument('--k', type=int, default=config['top_k'], help='number of top matches to be returned')

    parser.add_argument('--edge_detector_strategy', type=str, default='fused', help='edge detector strategy to be used for matching (`avg` or `fused`)')

    parser.add_argument('--show_best_match', type=bool, default=True, help='whether to show the best match or not')

    parser.add_argument('--show_top_k_matches', type=bool, default=True, help='whether to show the top k matches or not')

    # parse the arguments
    args = parser.parse_args()
    print(args)

    print("")
    print('Checking if the paths are valid...')

    # check if the image path is valid
    if not os.path.exists(args.img_path):
        raise ValueError('Invalid Image Path!')
    
    # check if the smp classifier path is valid
    if not os.path.exists(args.smp_classifier_path):
        raise ValueError('Invalid SMP Classifier Path!')
    
    # check if the background remover save folder path is valid
    if not os.path.exists(args.bgrem_save_folder_path):
        raise ValueError('Invalid Background Remover Save Folder Path!')
    
    # check if the edge detector save folder path is valid
    if not os.path.exists(args.edge_detector_save_folder_path['avg']):
        raise ValueError('Invalid Edge Detector Save Folder Path!')
    if not os.path.exists(args.edge_detector_save_folder_path['fused']):
        raise ValueError('Invalid Edge Detector Save Folder Path!')
    
    # check if the edge detector folder path is valid
    if not os.path.exists(args.edge_detector_folder_path):
        raise ValueError('Invalid Edge Detector Folder Path!')
    
    # check if the raw cad library folder path is valid
    if not os.path.exists(args.raw_cad_lib_folder_path):
        raise ValueError('Invalid Raw Cad Library Folder Path!')
    
    # check if the transformed cad library folder path is valid
    if not os.path.exists(args.transformed_cad_lib_folder_path):
        raise ValueError('Invalid Transformed Cad Library Folder Path!')
    
    # check if the device is valid
    if args.device not in ['cpu', 'mps', 'cuda']:
        raise ValueError('Invalid Device!')
    
    
    # 1. classify the image into smp or non-smp
    img_class = smp_classifier(
        img_path=args.img_path,
        classifier_save_path=args.smp_classifier_path,
        class_names=args.class_names,
        device=args.device
    )

    # 2. if the image is not an smp image, exit
    if img_class == args.class_names[0]:
        print('The image is a non-smp image. Exiting...')
        exit()
    
    # 3. if the image is an smp image:

    # 3.1. remove the background from the smp image
    _, bgrem_img_path = bgrem(
        img_path=args.img_path,
        save_folder_path=args.bgrem_save_folder_path
    )

    # 3.2. detect the edges in the background removed smp image
    edge_detect(
        bgrem_img_path=bgrem_img_path,
        save_folder_paths=args.edge_detector_save_folder_path,
        edge_detector_folder_path=args.edge_detector_folder_path
    )

    print("")
    print("Now Matching the Edge Detected Image with the CAD Files in the Library...")

    # 4. preprocess the cad files in the library

    # 4.1 extract the paths of the raw cad files in the library
    raw_cad_image_paths = []
    for ext in args.extensions:
        raw_cad_image_paths.extend(glob.glob(os.path.join(args.raw_cad_lib_folder_path, '*.'+ ext)))
    
    # 4.2 preprocess the raw cad files in the library one by one
    for raw_cad_image_path in raw_cad_image_paths:
        _ = cad_files_preprocess(
            img_path=raw_cad_image_path,
            padding=args.threshold_padding,
            save_folder_path=args.transformed_cad_lib_folder_path
        )
    
    # 5. match the edge detected smp image with the cad files in the transformed library

    # 5.1 extract the path of the edge detected smp image with the given 'edge_detector_strategy'
    if args.edge_detector_strategy == 'avg':
        # extract the path of the image in edge_detector_save_folder_path['avg'] directory
        
        # get a list of all the files in the directory
        file_list = os.listdir(args.edge_detector_save_folder_path['avg'])

        # filter the files based on extensions = ['jpg', 'jpeg', 'png']
        file_list = [file for file in file_list if file.lower().endswith(tuple(args.extensions))]

        # get the path of the image
        edge_detected_img_path = os.path.join(args.edge_detector_save_folder_path['avg'], file_list[0])

    elif args.edge_detector_strategy == 'fused':
        # extract the path of the image in edge_detector_save_folder_path['fused'] directory
        
        # get a list of all the files in the directory
        file_list = os.listdir(args.edge_detector_save_folder_path['fused'])

        # filter the files based on extensions = ['jpg', 'jpeg', 'png']
        file_list = [file for file in file_list if file.lower().endswith(tuple(args.extensions))]

        # get the path of the image
        edge_detected_img_path = os.path.join(args.edge_detector_save_folder_path['fused'], file_list[0])

    # 5.2 extract top k matches and the best match path from the transformed cad library
    top_k_matches_paths, best_match_path = match_image(
        img_path=edge_detected_img_path,
        top_k=args.k,
        cad_library_folder_path=args.transformed_cad_lib_folder_path,
        extensions=args.extensions,
    )

    print("")
    print('Image Matching Complete!')
    
    # 6. show the top k matches and the best match
    if args.show_top_k_matches:
        print("")
        print("Displaying the Top K Matches...")

        if args.show_best_match:
            print("")
            print("Displaying the Best Match...")

            # show the best match image
            best_img = cv2.imread(best_match_path)
            cv2.imshow('Best Match', best_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # show the top k matches images except the best match image
            for i in range(len(top_k_matches_paths)):
                img_path = top_k_matches_paths[i]
                if img_path != best_match_path:
                    img = cv2.imread(img_path)
                    cv2.imshow('Match '+str(i+1), img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
        
        else:
            # show the top k matches images
            for i in range(len(top_k_matches_paths)):
                img_path = top_k_matches_paths[i]
                img = cv2.imread(top_k_matches_paths[i])
                cv2.imshow('Match '+str(i+1), img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
    
    else:

        if args.show_best_match:
            print("")
            print("Displaying the Best Match...")

            # show the best match image
            best_img = cv2.imread(best_match_path)
            cv2.imshow('Best Match', best_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    print("")
    print('Exiting...')