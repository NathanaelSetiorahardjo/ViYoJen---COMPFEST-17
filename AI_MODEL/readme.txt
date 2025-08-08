FOR VIEL AND JEN

1. Environment & Dataset
Virtual Environment
– Created and activated microsleep-env (Python 3.13).
– Installed key libraries: pandas, numpy, scikit-learn, joblib, tensorflow (for later TFLite).

Synthetic Dataset
– Generated Indonesia-specific motorcycle microsleep data (2,394 balanced samples).
– Features:

Copy code
avg_pitch, avg_roll,
nod_duration,
nod_count_last_min,
gyro_peak,
speed_kmh
– Label rules based on head-tilt, nod duration/count, and riding speed.

2. Model Training & Evaluation
Training Script
– train_microsleep_model.py loads CSV, scales features, splits train/test (80/20), and trains a RandomForestClassifier.

Baseline Model
– Achieved 100% precision/recall/F1 on the synthetic test split (balanced classes).

Artifacts Saved

rf_microsleep_model.joblib (trained model)

scaler_microsleep.save (fitted StandardScaler)

3. Testing & Inference
Test Script
– test_microsleep_model.py demonstrates how to load the model & scaler, create a pandas.DataFrame sample with matching feature names, scale it, and predict.

Validation Samples
– Provided examples for both “microsleep” and “normal” test cases, ensuring the model labels them correctly.

4. Next-Step Artifacts
Colab Training Notebook
– train_and_export_tflite_colab.py: ready-to-run script to train a Keras model on our dataset and export a .tflite for the Flutter app.

Inference Demo
– inference_demo_rf.py: Python snippet showcasing real-time RF predictions on new data.