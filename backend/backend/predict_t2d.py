from fastapi import APIRouter, HTTPException
import xgboost as xgb
import numpy as np
import os
from pydantic import BaseModel

router = APIRouter()

# Load model once at startup
model_path = "models/xgb_t2d_model.json"
xgb_model = xgb.Booster()
xgb_model.load_model(model_path)

# Define expected input
class ClinicalGeneticInput(BaseModel):
    age: float
    pulse_rate: float
    systolic_bp: float
    diastolic_bp: float
    glucose: float
    cholesterol: float
    hdl: float
    bmi: float
    family_diabetes: int
    hypertensive: int
    family_hypertension: int
    cardiovascular_disease: int
    stroke: int
    gender: int

    CHR_ID: int
    INTERGENIC: int
    RISK_ALLELE_FREQUENCY: float
    PVALUE_MLOG: float
    EFFECT_SIZE: float
    CI_LOWER_BOUND: float
    CI_UPPER_BOUND: float

@router.post("/predict-t2d")
def predict_t2d(data: ClinicalGeneticInput):
    try:
        input_dict = data.dict()
        features = np.array([list(input_dict.values())], dtype=np.float32)
        dmatrix = xgb.DMatrix(features, feature_names=list(input_dict.keys()))

        prediction = xgb_model.predict(dmatrix)[0]
        result = "High risk of T2D" if prediction >= 0.5 else "Low risk of T2D"
        return {"prediction": result, "score": round(float(prediction), 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))