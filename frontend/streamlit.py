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
FINGERPRINT_CONFIDENCE_DEFAULT_THRESHOLD = 0.75

# ---------------------------------------------------------------------------------------------
# Streamlit application configuration
# ---------------------------------------------------------------------------------------------

def slider_callback():
    st.session_state.confidence_threshold = st.session_state.slider_value

st.set_page_config(page_title="FingerPrint Validator", 
                   page_icon="🔍", layout="centered", initial_sidebar_state="auto")

st.title("FingerPrint Validator")
st.write("Upload an image to generate its fingerprint class prediction.")  

uploaded_file = st.file_uploader("Choose an image...", 
                                 type=["jpg", "jpeg"],
                                 help="Click to upload an image file (JPEG format) for fingerprint class prediction. Supported formats: .jpg, .jpeg.")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="✅ Image has been successfully uploaded!", width="content")

confidence_threshold = st.slider("Confidence Threshold (%)", 
                                 min_value=0.70, 
                                 max_value=1.0, 
                                 value=FINGERPRINT_CONFIDENCE_DEFAULT_THRESHOLD, 
                                 step=0.01,
                                 format="percent",
                                 help="Set the confidence threshold for fingerprint class prediction. Predictions with confidence below this threshold will be considered unreliable.")

if st.button("Predict FingerPrint Class", 
             type="primary", 
             help="Click to predict the fingerprint class (i.e. 'thumb', 'index', 'middle', 'ring', or 'little') of the uploaded image."):
    if uploaded_file is None:
        st.warning("⚠️ Please upload an image to predict its fingerprint class.")
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
                if confidence < confidence_threshold*100:
                    st.warning(f"⚠️ The confidence level of the prediction is {confidence:.2f}%, which is below the threshold of {confidence_threshold*100:.2f}%.")
                    st.warning("The prediction may not be reliable.")
                else:
                    st.success(f"✅ The confidence level of the prediction is {confidence:.2f}%, which is above the threshold of {confidence_threshold*100:.2f}%.")
                    st.success("The prediction is likely to be reliable.")

                st.write("Prediction for all classes:")
                st.write(response.json())

            except Exception as e:
                st.error(f"E⚠️ Unable to predict the fingerprint class from the uploaded image '{uploaded_file.name}': {e}")