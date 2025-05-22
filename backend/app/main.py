from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import joblib
import numpy as np
from fastapi.responses import JSONResponse
from . import models, database, schemas, crud, auth

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
model = joblib.load("app/model.pkl")

# Dependency: DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "T2D Prediction Backend is running 🎯"}

# Register new user (admin or doctor only)
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        role=user.role,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login with JWT token return
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# POST /predict - requires doctor or admin token
@app.post("/predict", response_model=schemas.PredictionOut)
def make_prediction(
    data: schemas.PredictionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_or_doctor)
):
    features = np.array([[data.glucose, data.bmi, data.age]])
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    result = "yes" if prediction == 1 else "no"
    confidence = float(np.max(proba))

    db_data = models.Prediction(
        patient_name=data.patient_name,
        glucose=data.glucose,
        bmi=data.bmi,
        age=data.age,
        result=result,
        confidence=confidence,
        patient_id=data.patient_id,
        created_by_id=current_user.id
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# GET /history - requires doctor or admin token
@app.get("/history", response_model=list[schemas.PredictionOut])
def read_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_or_doctor)
):
    return db.query(models.Prediction).filter(
        models.Prediction.created_by_id == current_user.id
    ).all()

# POST /vitals - Samsung Watch sends data
@app.post("/vitals", response_model=schemas.VitalsOut)
def receive_vitals(
    data: schemas.VitalsCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_or_doctor)
):
    # Optional: check if current user owns the patient
    patient = db.query(models.Patient).filter_by(id=data.patient_id, doctor_id=current_user.id).first()
    if not patient:
        raise HTTPException(status_code=403, detail="Not authorized for this patient")

    new_vitals = models.Vitals(
        patient_id=data.patient_id,
        heart_rate=data.heart_rate,
        temperature=data.temperature,
        steps=data.steps,
        timestamp=data.timestamp
    )
    db.add(new_vitals)
    db.commit()
    db.refresh(new_vitals)
    return new_vitals

@app.get("/dashboard-data/{patient_id}")
def get_patient_dashboard_data(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_or_doctor)
):
    # Check if the doctor owns the patient
    patient = db.query(models.Patient).filter_by(id=patient_id, doctor_id=current_user.id).first()
    if not patient:
        raise HTTPException(status_code=403, detail="Not your patient")

    predictions = db.query(models.Prediction).filter_by(patient_id=patient_id).all()
    vitals = db.query(models.Vitals).filter_by(patient_id=patient_id).all()

    return JSONResponse({
        "predictions": [
            {
                "result": p.result,
                "confidence": p.confidence,
                "age": p.age,
                "bmi": p.bmi,
                "glucose": p.glucose
            } for p in predictions
        ],
        "vitals": [
            {
                "timestamp": v.timestamp,
                "heart_rate": v.heart_rate,
                "temperature": v.temperature,
                "steps": v.steps
            } for v in vitals
        ]
    })

import requests

# Endpoint for ChatGLM API
chatglm_url = "http://127.0.0.1:8001/generate-report"

@app.post("/generate-report")
async def generate_report(
    patient_id: int,
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_or_doctor)
):
    # Fetch patient and prediction data
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id, models.Patient.doctor_id == current_user.id).first()
    prediction = db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()

    if not patient or not prediction:
        raise HTTPException(status_code=404, detail="Patient or prediction not found")

    # Prepare data for the request
    payload = {
        "patient_name": patient.name,
        "glucose": prediction.glucose,
        "bmi": prediction.bmi,
        "age": patient.age,
        "history": "Patient history data..."  # You can add more relevant info
    }

    # Send request to ChatGLM API
    response = requests.post(chatglm_url, json=payload)
    
    if response.status_code == 200:
        report = response.json()["report"]
        return {"report": report}
    else:
        raise HTTPException(status_code=500, detail="Error generating report with ChatGLM")