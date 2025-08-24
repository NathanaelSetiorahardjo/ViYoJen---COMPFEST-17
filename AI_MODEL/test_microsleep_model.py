import pandas as pd
import joblib

# Load trained model and scaler
model = joblib.load("rf_microsleep_model.joblib")
scaler = joblib.load("scaler_microsleep.save")

# Create a test sample using the exact same column names as in training
sample = pd.DataFrame([{
    "avg_pitch":          2.0,    # small natural head bob
    "avg_roll":           0.5,
    "nod_duration":       0.3,    # blink‐like
    "nod_count_last_min": 0,      # no repeated nods
    "gyro_peak":         20.0,    # slow movement
    "speed_kmh":         25.0     # slow urban speed
}])

# Scale the sample using the same scaler
scaled_sample = scaler.transform(sample)

# Predict
pred = model.predict(scaled_sample)
proba = model.predict_proba(scaled_sample)

# Show prediction
print("Predicted Label:", pred[0])
print("Confidence (Not Sleep / Micro Sleep):", proba[0])
