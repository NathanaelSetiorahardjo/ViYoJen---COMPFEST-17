# ViYoJen---COMPFEST-17
Aviel, Yong and Jennifer

INTRODUCING [SUPER COOL ANTI MICRO-SLEEP HELMET]
AI-powered microsleep detection system embedded into a motorcycle helmet. By combining motion sensors (MPU6050), an ESP32 board, BLE communication, and a mobile app with on-device ML inference, it aims to prevent drowsy riding incidents with real-time alerts via buzzer and vibration motor.

🚀 Features
Real-time head movement tracking via MPU6050

AI-based drowsiness/microsleep detection using mobile device inference

BLE communication from ESP32 to Android app

Buzzer & vibration motor alerts during microsleep events

Data logging and visualization

Powered by Li-Po battery with TP4056 charging module

📦 Hardware Components
Component	Description
ESP32 Dev Board	Main MCU with BLE
MPU6050	3-axis gyroscope + accelerometer
Piezo Buzzer	Alert actuator
Vibration Motor	Haptic feedback actuator
TP4056 Module	Li-Po battery charging + output
Li-Po Battery (3.7V)	Power supply
Slide Switch	Power toggle

See /hardware folder for circuit diagram and wiring.

📲 Mobile App
Built with: Flutter
AI Model: TensorFlow Lite (.tflite)

Features:
Receives sensor data via BLE

Runs on-device AI model

Sends alert signal back to ESP32 via BLE

Stores session data locally (SQLite) or online (Firebase - optional)

🧠 AI Model
Input: time-windowed features from MPU6050 (pitch, roll, accel, gyro)

Output: Binary classification (0 = normal, 1 = microsleep)

Trained using: scikit-learn / TensorFlow

Inference runs on mobile app

For training scripts and datasets, see /ai_model.

📂 Repository Structure
bash
Copy
Edit
SmartGuard/
├── hardware/         # Circuit diagram, wiring schematic
├── firmware/         # ESP32 code (Arduino/C++)
├── app/              # Flutter app source code
├── ai_model/         # Model training notebook, data, TFLite model
├── docs/             # Proposal and documentation
└── README.md
🛠️ Getting Started
1. Flash ESP32
arduino
Copy
Edit
cd firmware/
Upload code using Arduino IDE or PlatformIO
2. Run Mobile App
Install dependencies in /app/

Load .tflite model into app assets

Build and run on Android device

3. Pair BLE and Test
Power on SmartGuard

Open app and connect to BLE

Ride, simulate head nods, test alerts!

📈 Dataset
Real-world and synthetic datasets available in /ai_model/dataset.csv

Collected across 3 states: alert, drowsy, aggressive

Labels: 0 (normal), 1 (microsleep)
