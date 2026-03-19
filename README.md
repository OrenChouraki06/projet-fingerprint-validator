# README file for projet-fingerprint-validator 

# dataset/SOCO_Fing : contain original images 
# dataset/SOCOFing_Training : sanitized (96,96,3) images split by class named subdirectories
# dataset/SOCOFing_Test : sanitized (96,96,3) images split by class named subdirectories

# deliverables : prezs and docs for certification

# notebooks 
#  construct_datasets.ipynb : transform the original dataset, convert images to iput shape of pre-trained model and save images in class names subdirectories
#                             build SOCOFing_Training as set of original Real and Altered-Easy images
#                             build SOCOFing_Test as set of original Real images
#  transfer_learning_mobilenet.ipynb : transfer leaning from pre-trained model mobilenetbased 

# models : directory for saved trained models
