'''
   This file contains the implementation of the FastAPI application for the FingerPrint Validator.
    It defines the API endpoints for loading the fingerprint model, preprocessing the fingerprint
    image and predicting fingerprint images.
    The application loads a pre-trained MobileNetV2 model for fingerprint classification and 
    uses it to make predictions on uploaded images.
'''
# ---------------------------------------------------------------------------------------------
# import librairies
# ------------------------------------  ---------------------------------------------------------
import io
import numpy as np
from PIL import Image

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, applications, preprocessing

import constants

if constants.MobileNet_version == "MobileNet":
    from tensorflow.keras.applications import MobileNet
    from tensorflow.keras.applications.mobilenet import preprocess_input
elif constants.MobileNet_version == "MobileNetV2":
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
elif constants.MobileNet_version == "MobileNetV3Small":
    from tensorflow.keras.applications import MobileNetV3Small
    from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
elif constants.MobileNet_version == "MobileNetV3Large":
    from tensorflow.keras.applications import MobileNetV3Large
    from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
else:
    print("Unknown MobileNet version name")
    exit(0)

# ---------------------------------------------------------------------------------------------
# load the finger print model
# ---------------------------------------------------------------------------------------------
def load_fingerprint_model(model_path) -> tf.keras.Model:
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        print(f"⚠️ Unable to load Fingerprint model '{model_path}': {str(e)}.\n")
        raise e
    
    print(f"✅ Fingerprint model {model.name} has been loaded successfully.\n")
    return model

# ---------------------------------------------------------------------------------------------
# preprocess the fingerprint image bytes
# ---------------------------------------------------------------------------------------------
def preprocess_fingerprint_bytes(fingerprint_image_filename: str,
                                 fingerprint_image_bytes: bytes) -> np.ndarray:
    try:
        print(f"Preprocessing fingerprint image '{fingerprint_image_filename}'...\n")

        # convert bytes to PIL image
        img = Image.open(io.BytesIO(fingerprint_image_bytes))

        # resize the image to the expected input size of the model
        img = img.resize(constants.IMAGE_SIZE)

        # convert the image to grayscale and then back to RGB as the model expects 3 channels
        img = img.convert('L')  # Convert to grayscale
        img = img.convert('RGB')  # Convert back to RGB

        # convert the image to a numpy array and preprocess it for MobileNetV2
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = preprocess_input(img_array)  # Normalisation for MobileNetV2

    except Exception as e:
        print(f"⚠️ Unable to preprocess fingerprint image '{fingerprint_image_filename}': {str(e)}.\n")
        raise e

    print(f"✅ Fingerprint image '{fingerprint_image_filename}' has been preprocessed successfully.\n")
    return img_array

# ---------------------------------------------------------------------------------------------
# prediction function
# ---------------------------------------------------------------------------------------------
def predict_fingerprint_model(model: tf.keras.Model, 
                              fingerprint_image_filename: str,
                              fingerprint_image_bytes: bytes) -> dict:
    '''
    Predict the fingerprint class given an image with finetuned model
    Args:
        model: fingerprint trained model
        fingerprint_image_path: fingerprint image path
    '''
    try:
        print(f"Predicting fingerprint image '{fingerprint_image_filename}'...\n")

        # Preprocess the fingerprint image
        img_array = preprocess_fingerprint_bytes(fingerprint_image_filename, fingerprint_image_bytes)

        # Prediction
        predictions = model.predict(img_array, verbose=constants.PREDICTION_VERBOSE)

        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx]

        # Report top-2 predictions
        topk_idx = np.argsort(predictions[0])[-2:][::-1]

    except Exception as e:
        print(f"⚠️ Unable to predict fingerprint image '{fingerprint_image_filename}': {str(e)}.\n")
        raise e

    probabilities = {constants.class_names[i]: float(predictions[0][i]) for i in range(len(constants.class_names))}
    top2_probabilities = {constants.class_names[i]: float(predictions[0][i]) for i in topk_idx}
    response = {
        'fingerprint': constants.class_names[predicted_class_idx],
        'confidence': confidence,
        'probabilities': probabilities,
        'top2_probabilities': top2_probabilities
    }

    print(f"✅ Fingerprint image '{fingerprint_image_filename}' has been predicted successfully.\n")
    print(f"    Prediction response: {response}\n")

    return response