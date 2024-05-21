#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include "MAX30105.h"
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

// WiFi credentials
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// Server URL
const char* serverName = "https://moocare.onrender.com/"; // Replace with your server IP

// MAX30102
MAX30105 particleSensor;

// AD8232
const int AD8232_PIN = 36;

// NEO-M8N GPS
TinyGPSPlus gps;
SoftwareSerial gpsSerial(17, 16); // RX, TX

// Seeed Studio 24GHz mmWave Sensor
SoftwareSerial mmWaveSerial(1, 3); // RX, TX

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  Wire.begin();
  
  // Initialize MAX30102
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30105 not found. Check wiring/power.");
    while (1);
  }
  particleSensor.setup();
  
  // Initialize AD8232
  pinMode(AD8232_PIN, INPUT);
  
  // Initialize GPS
  gpsSerial.begin(9600);
  
  // Initialize mmWave Sensor
  mmWaveSerial.begin(115200);
}

void loop() {
  long irValue = particleSensor.getIR();
  long redValue = particleSensor.getRed();
  int ecgValue = analogRead(AD8232_PIN);
  String gpsData = "";
  if (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
    if (gps.location.isUpdated()) {
      gpsData = String(gps.location.lat(), 6) + "," + String(gps.location.lng(), 6);
    }
  }
  String mmWaveData = "";
  if (mmWaveSerial.available() > 0) {
    mmWaveData = mmWaveSerial.readStringUntil('\n');
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");
    
    String jsonData = "{\"ir\":" + String(irValue) + 
                      ", \"red\":" + String(redValue) + 
                      ", \"ecg\":" + String(ecgValue) + 
                      ", \"gps\":\"" + gpsData + 
                      "\", \"mmwave\":\"" + mmWaveData + "\"}";

    int httpResponseCode = http.POST(jsonData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
  delay(1000);
}
