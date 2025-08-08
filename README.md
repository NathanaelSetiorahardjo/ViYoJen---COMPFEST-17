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

TO BE EXPLAINED FURTHER LATER

Labels: 0 (normal), 1 (microsleep)
