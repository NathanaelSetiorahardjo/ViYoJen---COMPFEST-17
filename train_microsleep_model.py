
# train_microsleep_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib

# Load synthetic dataset
df = pd.read_csv("synthetic_microsleep_dataset.csv")

# Features and labels
X = df.drop("label", axis=1)
y = df["label"]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(clf, "rf_microsleep_model.joblib")
joblib.dump(scaler, "scaler_microsleep.save")

print("Model and scaler saved.")

# Evaluate model
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(clf, "rf_microsleep_model.joblib")
joblib.dump(scaler, "scaler_microsleep.save")
