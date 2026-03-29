# README file for projet-fingerprint-validator 

# dataset/SOCO_Fing : contain original images 
# dataset/SOCOFing_Custom/train | validation : sanitized (96,96,3) images split by class name

# deliverables : prezs and docs for certification

# notebooks 
#  end2end_fingerprint_classification.ipynb : end 2 end notebook for comprehensive model training
#  this includes : train / validation / test datasets exploration, split and prep for training
#                  fingrprint model creation : MobileNetV2 + hidden dense layers + classification
#                  transfer learning and fine tuning
#                  model evaluation

# models : directory for saved trained models

# app : fastAPI based application for web deployment
#       to run : fastapi dev app/main.py

# frontend : Streamlit interface
#       to run : uv run streamlit run frontend/streamlit.py --server.port=5801 --server.address="0.0.0.0"