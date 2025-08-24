#include <WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>

// ====== WiFi Credentials ======
const char* ssid = "HPNYA YONG";
const char* password = "Yong ganteng";

// ====== WebSocket Server ======
const char* ws_host = "172.20.10.8";
const int ws_port = 8765;
const char* ws_path = "/";

WebSocketsClient webSocket;
Adafruit_MPU6050 mpu;

unsigned long lastReconnectAttempt = 0;

// ====== Buzzer Pin ======
#define BUZZER_PIN 12   

// ====== WebSocket Event Handler ======
void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch (type) {
    case WStype_DISCONNECTED:
      Serial.println("❌ Disconnected from server");
      break;
    case WStype_CONNECTED:
      Serial.println("✅ Connected to server!");
      break;
    case WStype_TEXT: {
      String msg = String((char*)payload);
      Serial.printf("Prediction from server: %s\n", payload);

      // Control buzzer based on server message
      if (msg.indexOf("MICROSLEEP") >= 0) {
        digitalWrite(BUZZER_PIN, HIGH);  // turn buzzer ON
        Serial.println("🔔 Buzzer ON (Microsleep detected)");
      }
      else if (msg.indexOf("AWAKE") >= 0) {
        digitalWrite(BUZZER_PIN, LOW);   // turn buzzer OFF
        Serial.println("🔕 Buzzer OFF (Awake)");
      }
      break;
    }
  }
}

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void connectWebSocket() {
  Serial.println("🔄 Connecting WebSocket...");
  webSocket.begin(ws_host, ws_port, ws_path);
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000); // auto-reconnect every 5s
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Setup buzzer pin
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW); // buzzer OFF initially

  connectWiFi();
  connectWebSocket();

  // Setup MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip!");
    while (1) { delay(10); }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("Setup complete!");
}

void loop() {
  // Keep WiFi alive
  if (WiFi.status() != WL_CONNECTED) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt > 5000) {
      lastReconnectAttempt = now;
      Serial.println("⚠️ WiFi lost, reconnecting...");
      connectWiFi();
    }
    return; // skip sending if no WiFi
  }

  // Keep WebSocket alive
  webSocket.loop();

  if (!webSocket.isConnected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt > 5000) {
      lastReconnectAttempt = now;
      Serial.println("⚠️ WebSocket lost, reconnecting...");
      connectWebSocket();
    }
    return; // skip sending if socket not connected
  }

  // Read sensor
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Build JSON
  StaticJsonDocument<200> doc;
  doc["ax"] = a.acceleration.x;
  doc["ay"] = a.acceleration.y;
  doc["az"] = a.acceleration.z;
  doc["gx"] = g.gyro.x;
  doc["gy"] = g.gyro.y;
  doc["gz"] = g.gyro.z;
  doc["t"]  = temp.temperature;

  char buffer[200];
  size_t n = serializeJson(doc, buffer);

  // Send JSON to server
  webSocket.sendTXT(buffer, n);

  // Print sensor values locally
  Serial.printf("Sent: ax=%.2f ay=%.2f az=%.2f gx=%.2f gy=%.2f gz=%.2f t=%.2f\n",
                a.acceleration.x, a.acceleration.y, a.acceleration.z,
                g.gyro.x, g.gyro.y, g.gyro.z, temp.temperature);

  delay(200); // ~5 Hz
}
