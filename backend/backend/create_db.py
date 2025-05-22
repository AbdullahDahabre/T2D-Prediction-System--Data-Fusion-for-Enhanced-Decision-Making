import sqlite3

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect("diabetes_prediction.db")
cursor = conn.cursor()

# Create patient_data table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patient_data (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    pulse_rate INTEGER,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    glucose REAL,
    cholesterol REAL,
    hdl REAL,
    bmi REAL,
    hypertensive INTEGER,
    family_diabetes INTEGER,
    family_hypertension INTEGER,
    cardiovascular_disease INTEGER,
    stroke INTEGER,
    gender INTEGER,
    chr_id INTEGER,
    chr_pos INTEGER,
    intergenic INTEGER,
    risk_allele_frequency REAL,
    p_value REAL,
    p_value_m_log REAL,
    effect_size REAL,
    ci_lower REAL,
    ci_upper REAL
);
""")

# Create prediction_result table
cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_result (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    prediction TEXT,
    confidence REAL,
    FOREIGN KEY (patient_id) REFERENCES patient_data(patient_id)
);
""")

# Save and close
conn.commit()
conn.close()

print("Database and tables created successfully.")