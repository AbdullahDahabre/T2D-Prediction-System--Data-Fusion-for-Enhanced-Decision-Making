from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/dashboard-latest")
def get_dashboard_data():
    conn = sqlite3.connect("diabetes_prediction.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.glucose,
            p.bmi,
            r.prediction,
            r.confidence
        FROM patient_data p
        JOIN prediction_result r ON p.patient_id = r.patient_id
        ORDER BY r.result_id DESC LIMIT 1;
    """)
    row = cursor.fetchone()
    conn.close()

    if row:
        glucose, bmi, prediction, confidence = row
        return {
            "bloodGlucose": glucose,
            "glucoseUnit": "mg/dL",
            "glucoseChange": "Latest value",
            "bmi": bmi,
            "bmiChange": "Latest BMI",
            "riskStatus": prediction,
            "riskPercent": round(confidence * 100, 2),
            "statusText": "Fetched from last record",
            "lastUpdated": "Just now"
        }
    else:
        return {
            "bloodGlucose": 0,
            "glucoseUnit": "mg/dL",
            "glucoseChange": "No data",
            "bmi": 0,
            "bmiChange": "No data",
            "riskStatus": "Unknown",
            "riskPercent": 0,
            "statusText": "No records yet",
            "lastUpdated": "-"
        }