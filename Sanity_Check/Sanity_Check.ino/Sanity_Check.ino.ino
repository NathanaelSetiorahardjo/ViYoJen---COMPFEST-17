#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

const int buzzerPin = 19;
const float tiltThreshold = 6.0; // m/s² for X/Y tilt detection

void setup() {
  Serial.begin(115200);

  pinMode(buzzerPin, OUTPUT);

  // Initialize I2C and MPU
  Wire.begin(21, 22);
  if (!mpu.begin()) {
    Serial.println("MPU6050 not found! Check wiring.");
    while (1);
  }

  Serial.println("MPU6050 Initialized. Printing full data...");
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // --- Print ALL data ---
  Serial.print("Accel (m/s^2) X: "); Serial.print(a.acceleration.x);
  Serial.print(" Y: "); Serial.print(a.acceleration.y);
  Serial.print(" Z: "); Serial.println(a.acceleration.z);

  Serial.print("Gyro (deg/s) X: "); Serial.print(g.gyro.x);
  Serial.print(" Y: "); Serial.print(g.gyro.y);
  Serial.print(" Z: "); Serial.println(g.gyro.z);

  Serial.print("Temperature (°C): "); Serial.println(temp.temperature);

  Serial.println("-------------------------");

  // --- Tilt detection (basic) ---
  if (abs(a.acceleration.x) > tiltThreshold || abs(a.acceleration.y) > tiltThreshold) {
    Serial.println("Tilt detected! Buzzer ON");
    digitalWrite(buzzerPin, HIGH);
  } else {
    digitalWrite(buzzerPin, LOW);
  }

  delay(500);
}
