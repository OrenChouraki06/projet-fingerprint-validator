'''
    This file defines the schema for the FastAPI response. It uses Pydantic's BaseModel to 
    create a structured response model for fingerprint image predictions. The FingerprintPrediction 
    class includes several fields: 
        fingerprint: string representing the predicted class
        confidence: float representing the confidence level of the prediction 
        probabilities: dictionary containing the probabilities for each class
'''
# ---------------------------------------------------------------------------------------------
# import librairies
# ---------------------------------------------------------------------------------------------
from pydantic import BaseModel

# ---------------------------------------------------------------------------------------------
# Model Schema definition
# ---------------------------------------------------------------------------------------------
class FingerprintPrediction(BaseModel):
    fingerprint: str
    confidence: float
    probabilities: dict