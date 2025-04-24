from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    role = Column(String)  # "doctor" or "admin"
    hashed_password = Column(String)

    patients = relationship("Patient", back_populates="doctor")
    predictions = relationship("Prediction", back_populates="created_by")

# Patient table
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gender = Column(String)
    dob = Column(String)
    doctor_id = Column(Integer, ForeignKey("users.id"))

    doctor = relationship("User", back_populates="patients")
    predictions = relationship("Prediction", back_populates="patient")
    vitals = relationship("Vitals", back_populates="patient")

# Prediction table
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    glucose = Column(Float)
    bmi = Column(Float)
    age = Column(Integer)
    result = Column(String)
    confidence = Column(Float)
    
    patient_id = Column(Integer, ForeignKey("patients.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))

    patient = relationship("Patient", back_populates="predictions")
    created_by = relationship("User", back_populates="predictions")

#
class Vitals(Base):
    __tablename__ = "vitals"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    heart_rate = Column(Integer)
    temperature = Column(Float)
    steps = Column(Integer)
    timestamp = Column(String)

    patient = relationship("Patient", back_populates="vitals")
