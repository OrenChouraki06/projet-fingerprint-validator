'''
    This file contains the constants used in the FastAPI fingerprint validatorapplication. 
    It defines for instance the class labels for the fingerprint classification task. 
'''
# ---------------------------------------------------------------------------------------------
# Constants for the fingerprint classification
# ---------------------------------------------------------------------------------------------

# Class labels
class_names = ['thumb', 'index', 'middle', 'ring', 'little']
num_classes = len(class_names)

# Base model version
MobileNet_version = "MobileNetV2"

# Directory for the fingerprint model
FINGERPRINT_MODEL_DIR = "models"
FINGERPRINT_MODEL_FILENAME = MobileNet_version + "_FingerPrint_Model_" + str(num_classes) + "_classes_Fine_Tuning.keras"
FINGERPRINT_MODEL_PATH = FINGERPRINT_MODEL_DIR + "/" + FINGERPRINT_MODEL_FILENAME

# fingerprint image input size
IMAGE_SIZE = (96, 96)

# prediction verbosity level (0 = silent, 1 = progress bar, 2 = one line per epoch)
PREDICTION_VERBOSE = 0

# Debug log file
DEBUG_LOG_FILE = "debug.log"
DEBUG_TMP_DIR = "/tmp/"
DEBUG_LOG_PATH = DEBUG_TMP_DIR + DEBUG_LOG_FILE
