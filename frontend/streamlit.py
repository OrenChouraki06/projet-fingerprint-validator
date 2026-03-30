'''
    This file defines the Streamlit frontend for the fingerprint validator application. It provides a user 
    interface for uploading fingerprint images and predicting their classes using a FastAPI backend.
    The frontend is designed to be simple and user-friendly, allowing users to easily interact with the 
    application and view the results of model predictions.
'''
# ---------------------------------------------------------------------------------------------
# Import libraries
# ---------------------------------------------------------------------------------------------
import io
from PIL import Image

import streamlit as st
import requests

# ---------------------------------------------------------------------------------------------
# Constants for the Streamlit frontend
# ---------------------------------------------------------------------------------------------

# url of the FastAPI backend for the fingerprint validator application
FINGERPRINT_FASTAPI_URL = "http://localhost:8000"
FINGERPRINT_CONFIDENCE_THRESHOLD = 75.0

# ---------------------------------------------------------------------------------------------
# Streamlit application configuration
# ---------------------------------------------------------------------------------------------

st.set_page_config(page_title="FingerPrint Validator / Fault Detector", 
                   page_icon="🔍", layout="centered", initial_sidebar_state="auto")

st.title("FingerPrint Validator / Fault Detector")
st.write("Upload an image to analyze and generate its fingerprint prediction using FastAPI backend.")  

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="✅ Image has been successfully uploaded!", width="content")

if st.button("Predict FingerPrint", 
             type="primary", 
             help="Click to predict the fingerprint class of the uploaded image."):
    if uploaded_file is None:
        st.warning("⚠️ Please upload a fingerprint image to predict.")
    else:
        with st.spinner("Predicting fingerprint image..."):
            try:
                # Convert image to bytes
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='JPEG')
                img_bytes.seek(0)

                # files = {"image": ("image.jpeg", img_bytes, "image/jpeg")}
                files = {"file": (uploaded_file.name, img_bytes, uploaded_file.type)}   

                # Send request to FastAPI backend
                response = requests.post(f"{FINGERPRINT_FASTAPI_URL}/predict_fingerprint", files=files)

                confidence = response.json().get("confidence", 0)
                if confidence < FINGERPRINT_CONFIDENCE_THRESHOLD:
                    st.warning(f"⚠️ The confidence level of the prediction is {confidence:.2f}%, which is below the threshold of {FINGERPRINT_CONFIDENCE_THRESHOLD}%.")
                    st.warning("The prediction may not be reliable.")
                else:
                    st.success(f"✅ The confidence level of the prediction is {confidence:.2f}%, which is above the threshold of {FINGERPRINT_CONFIDENCE_THRESHOLD}%.")
                    st.success("The prediction is likely to be reliable.")

                st.write("Predictions response from FastAPI backend:")
                st.write(response.json())

            except Exception as e:
                st.error(f"E⚠️ Unable to predict the fingerprint image '{uploaded_file.name}': {e}")