'''
    Nom du projet : FingerPrint Validdator / Fault Detector
    Description : This project is a web application that allows users to upload images of 
                fingerprints and receive predictions about the validity of the fingerprint. 
                The application uses a pre-trained MobileNetV2 model to analyze the uploaded 
                images and provide insights into the quality of the fingerprint.
                The application is built using FastAPI, which provides a robust and 
                efficient way to handle requests and responses. The application includes 
                a health check endpoint to ensure that the API is running smoothly. Overall, 
                this project aims to provide a reliable tool for validating fingerprints and 
                detecting faults in a user-friendly Streamlit interface.
    Author : Laurent Chouraki
'''
# ---------------------------------------------------------------------------------------------
# import librairies
# ---------------------------------------------------------------------------------------------
import sys
import numpy as np

from fastapi import FastAPI, File, UploadFile, HTTPException

import constants
from schema import FingerprintPrediction
from model import load_fingerprint_model, predict_fingerprint_model

# ---------------------------------------------------------------------------------------------
#  simple logging mechanism for debug
# ---------------------------------------------------------------------------------------------

try:
    debug_log_path = open(constants.DEBUG_LOG_PATH, "w")
    debug_log_path.write(f"✅ Debug log file {debug_log_path.name} has been created.\n")
except Exception as e:
    print(f"⚠️ Unable to create debug log file: {str(e)}.\n")
    exit(100)

# redirect stdout and stderr to the debug log file
sys.stdout = debug_log_path
sys.stderr = debug_log_path
print("✅ Standard output and error have been redirected to the debug log file.\n")

# ---------------------------------------------------------------------------------------------
# instance creation of FastAPI application
# ---------------------------------------------------------------------------------------------
try:
    app = FastAPI()
    print(f"✅ FastAPI application instance has been created.\n")
except Exception as e:
    print(f"⚠️ Unable to create FastAPI application instance: {str(e)}.\n")
    raise HTTPException(status_code=200, 
                        detail=f"⚠️ Unable to create FastAPI application instance: {str(e)}")  

# ---------------------------------------------------------------------------------------------
# load the fingerprint model
# ---------------------------------------------------------------------------------------------
try:
    fingerprint_model = load_fingerprint_model(constants.FINGERPRINT_MODEL_PATH)
except Exception as e:
    print(f"⚠️ Unable to load fingerprint model '{constants.FINGERPRINT_MODEL_PATH}': {str(e)}.\n")
    raise HTTPException(status_code=300, 
                        detail=f"⚠️ Unable to load fingerprint model '{constants.FINGERPRINT_MODEL_PATH}': {str(e)}")

# ---------------------------------------------------------------------------------------------
# FastAPI routes creation
# ---------------------------------------------------------------------------------------------

# top-level application route
@app.get("/")
def root():
    return {"status": "running", 
            "message": "Welcome to the FingerPrint Validator FastAPI!"}

# health check route
@app.get("/health")
def health_check():
    return {"status": "healthy", 
            "message": "The FastAPI is up and running!"}

# prediction and route
@app.post("/predict_fingerprint", response_model=FingerprintPrediction)
async def predict_fingerprint(file: UploadFile = File(...)):
    fingerprint_image_bytes = await file.read()

    try:
        prediction = predict_fingerprint_model(fingerprint_model, 
                                               file.filename,
                                               fingerprint_image_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, 
                            detail=f"⚠️ Unable to predict fingerprint: {str(e)}")
    
    print(f"✅ FastAPI application returned prediction: {prediction}.\n")
    return prediction
