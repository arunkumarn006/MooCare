#include <Wire.h>
#include <MAX30105.h>
#include <heartRate.h>
#include <spo2_algorithm.h>
#include <WiFi.h>
#include <HTTPClient.h>

MAX30105 particleSensor;

const byte RATE_SIZE = 4; // Increase this for more precision, but slower updates
byte rates[RATE_SIZE]; // Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; // Time at which the last beat occurred
float beatsPerMinute;
int beatAvg;

int32_t bufferLength; // Buffer length for heart rate and SpO2 calculation
uint32_t irBuffer[100]; // IR LED sensor data
uint32_t redBuffer[100]; // Red LED sensor data
int32_t spo2; // SPO2 value
int8_t validSPO2; // SPO2 validity
int32_t heartRate; // Heart rate value
int8_t validHeartRate; // Heart rate validity

// Replace with your network credentials
const char* ssid = "moo";
const char* password = "12345678";

const char* serverName = "https://moocare.onrender.com/data";
const int httpPort = 5001;

void setup() {
  Serial.begin(115200);
  delay(100);

  // Initialize WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Initialize MAX30102
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 was not found. Please check wiring/power.");
    while (1);
  }
  particleSensor.setup(); // Configure sensor with default settings

  Serial.println("Place your finger on the sensor to start reading...");
}

void loop() {
  // Read data from MAX30102
  bufferLength = 100; // Sample 100 data points
  
  // Read 100 samples from the sensor
  for (byte i = 0; i < bufferLength; i++) {
    while (!particleSensor.available()) {
      particleSensor.check(); // Check the sensor for new data
    }
    redBuffer[i] = particleSensor.getRed();
    irBuffer[i] = particleSensor.getIR();
    particleSensor.nextSample(); // Move to the next sample
  }

  // Calculate heart rate and SpO2
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

  // Determine cow status
  String cowStatus = "Unknown";
  if (validHeartRate && validSPO2) {
    if (heartRate < 40 || heartRate > 100 || spo2 < 90) {
      cowStatus = "Critical";
    } else {
      cowStatus = "Normal";
    }
  }

  // Print data to Serial Monitor
  Serial.print("HR: "); Serial.print(heartRate);
  Serial.print(", SpO2: "); Serial.print(spo2);
  Serial.print(", Status: "); Serial.println(cowStatus);

  // Send data to server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Prepare JSON payload
    String jsonPayload = "{";
    jsonPayload += "\"heartRate\": " + String(heartRate) + ",";
    jsonPayload += "\"spo2\": " + String(spo2) + ",";
    jsonPayload += "\"status\": \"" + cowStatus + "\"";
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);

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

  delay(5000); // Send data every 5 seconds
}
