import sqlite3

def save_patient_data_and_prediction(form_data: dict, prediction: str, confidence: float):
    conn = sqlite3.connect("diabetes_prediction.db")
    cursor = conn.cursor()

    # Normalize keys to lowercase for consistent access
    form = {k.lower(): v for k, v in form_data.items()}

    # Extract clinical and genetic features
    clinical_data = [
        form.get("age"), form.get("pulse_rate"), form.get("systolic_bp"), form.get("diastolic_bp"),
        form.get("glucose"), form.get("cholesterol"), form.get("hdl"), form.get("bmi"),
        form.get("family_diabetes"), form.get("hypertensive"), form.get("family_hypertension"),
        form.get("cardiovascular_disease"), form.get("stroke"), form.get("gender")
    ]

    genetic_data = [
        form.get("chr_id"), form.get("intergenic"), form.get("risk_allele_frequency"),
        form.get("pvalue_mlog"), form.get("effect_size"), form.get("ci_lower_bound"), form.get("ci_upper_bound")
    ]

    # Insert clinical + genetic data
    cursor.execute("""
        INSERT INTO patient_data (
            age, pulse_rate, systolic_bp, diastolic_bp, glucose, cholesterol, hdl, bmi,
            family_diabetes, hypertensive, family_hypertension, cardiovascular_disease,
            stroke, gender, chr_id, intergenic, risk_allele_frequency,
            p_value_mlog, effect_size, ci_lower, ci_upper
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, clinical_data + genetic_data)

    patient_id = cursor.lastrowid  # get the inserted patient ID

    # Insert prediction result
    cursor.execute("""
        INSERT INTO prediction_result (patient_id, prediction, confidence)
        VALUES (?, ?, ?)
    """, (patient_id, prediction, confidence))

    conn.commit()
    conn.close()