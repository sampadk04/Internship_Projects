# import os for file path operations
import os

# import pytorch
import torch

# import the pre-processing function
from src.pre_process import classifier_preprocess

# set device to GPU
device = torch.device("mps" if torch.backends.mps.is_available else "cpu") # for apple metal
# device = torch.device("cuda" if torch.cuda.is_available else "cpu") # for nvidea cuda

# set variables/hyper-parameters
class_names = ['non_smp', 'smp']
smp_clf_save_path = os.path.join('models', 'smp_classifier', 'model1_mps.pth')

# use the model to classify
def smp_classifier(img_path, classifier_save_path=smp_clf_save_path, class_names=class_names, device=device):
    '''
    Parameters:
        img_path: path to the image to be classified
        classifier_save_path: path to the pre-trained classifier model (.pth file)
        class_names: the names of the classes (non_smp: 0, smp: 1)
    
    Returns:
        img_class: the predicted class of the image (non_smp: 0, smp: 1)
    '''
    # preprocess the image
    img = classifier_preprocess(img_path)

    # load the pre-trained model
    classifier = torch.load(classifier_save_path)

    print("")
    print("Feeding Image to the SMP Classifier...")
    with torch.no_grad():
        # set the model to evaluation mode
        classifier.eval()
        # feed the image to the model
        out = classifier(img.to(device))
        # get the predicted class
        _, pred = torch.max(out.data, dim=1)
        # get the predicted class name
        img_class = class_names[pred.item()]

    print("")
    print("Predicted Class:", img_class)
    
    return img_class


if __name__=='__main__':
    # test the classifier, change the path to the image you want to classify
    img_path = os.path.join('data', 'smp_input', 'test.jpg')

    # get the predicted class of the test image
    img_class = smp_classifier(img_path)