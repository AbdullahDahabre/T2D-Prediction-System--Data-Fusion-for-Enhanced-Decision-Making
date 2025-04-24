# app/crud.py
from sqlalchemy.orm import Session
from . import models

def get_all_predictions(db: Session):
    return db.query(models.Prediction).all()