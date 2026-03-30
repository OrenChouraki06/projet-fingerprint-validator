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

# definition of tabs for the fingerprint application
tabs = st.tabs(["Image Prediction", "About"])

# ---------------------------------------------------------------------------------------------
# Tab for the fingerprint image analysis
# ---------------------------------------------------------------------------------------------

with tabs[0]:
    st.header("Image Prediction")
   
    uploaded_file = st.file_uploader("Choose an image...", 
                                     type=["bmp", "jpg", "jpeg"],
                                     help="Click to upload an image file (BMP, JPEG format) for fingerprint class prediction.")

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
                        st.warning("The fingerprint image may not be actionable.")
                    else:
                        st.success(f"✅ The confidence level of the prediction is {confidence:.2f}%, which is above the threshold of {confidence_threshold*100:.2f}%.")
                        st.success("The fingerprint image is likely to be actionable.")

                    st.write("Prediction for all fingerprint classes:")
                    st.write(response.json())

                except Exception as e:
                    st.error(f"E⚠️ Unable to predict the fingerprint class from the uploaded image '{uploaded_file.name}': {e}")

# ---------------------------------------------------------------------------------------------
# Tab for application information and instructions
# ---------------------------------------------------------------------------------------------

with tabs[1]:
    st.header("About the FingerPrint Validator Application")

    st.write("""
        The FingerPrint Validator application is designed to analyze fingerprint images and predict their classes (e.g., thumb, index, middle, ring, little) using a machine learning model hosted on a FastAPI backend. 
        Users can upload fingerprint images in BMP or JPEG format and receive predictions along with confidence levels. 
        The application also allows users to set a confidence threshold to determine whether the fingerprint images are actionable.
    """)
    st.write("""
        **How to Use:**
        1. Upload a fingerprint image by clicking the "Choose an image..." button.
        2. Adjust the confidence threshold using the slider to set the minimum confidence level for actionable predictions.
        3. Click the "Predict FingerPrint Class" button to generate predictions for the uploaded image.
        4. Review the predicted classes and their confidence levels displayed below the prediction button.
    """)
    st.write("""
        **Note:** Ensure that the FastAPI backend is running and accessible at `http://localhost:8000` for the streamlitapplication to function correctly.
                    The FastAPI backend should have an endpoint `/predict_fingerprint` that accepts image files and returns predictions in JSON format.
                    The FastAPI backend is responsible for processing the uploaded images, running them through the machine learning model, and returning the predicted classes and confidence levels to the Streamlit frontend for display.
    """)
    st.write("""
        Technology Stack:
        - Streamlit: for creating the web application interface.
        - FastAPI: For hosting the machine learning model and handling API requests.
        - TensorFlow/Keras MobileNetV2: For the machine learning model used in fingerprint class prediction.
        - Transfer learning and fine tuning training techniques have been carried out on the machine learning model, which consists of:
             - MobileNetV2 architecture (pre-trained on ImageNet)
             - Hidden dense layers with 256 and 64 neurons respectively, with Leaky_ReLU activation function
             - Classification layer with softmax activation function for the 5 fingerprint classes.
        - Kaggle SOCOFing dataset: for training and evaluating the machine learning model.
    """)