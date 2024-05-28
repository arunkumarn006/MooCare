#include <MAX30105.h>
#include <heartRate.h>
#include <spo2_algorithm.h>
#include <Wire.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "moocare";
const char* password = "12345678";

// Server endpoint
const char* serverName = "http://localhost:5000/api/data"; // Replace YOUR_SERVER_IP with the IP address of your server

// MAX30102
MAX30105 max30105;

// AD8232
const int ad8232Pin = 36;

// TinyGPS++
TinyGPSPlus gps;
HardwareSerial gpsSerial(1);

// WiFi client
WiFiClient client;
HTTPClient http;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Initialize MAX30102
  if (!max30105.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found. Please check wiring/power.");
    while (1);
  }
  max30105.setup();

  // Initialize AD8232
  pinMode(ad8232Pin, INPUT);

  // Initialize GPS
  gpsSerial.begin(9600, SERIAL_8N1, 16, 17);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Read data from MAX30102
  long irValue = max30105.getIR();
  long redValue = max30105.getRed();

  // Read data from AD8232
  int ecgValue = analogRead(ad8232Pin);

  // Read data from GPS
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  // Prepare data
  String jsonData = "{";
  jsonData += "\"ir\": " + String(irValue) + ",";
  jsonData += "\"red\": " + String(redValue) + ",";
  jsonData += "\"ecg\": " + String(ecgValue) + ",";
  if (gps.location.isValid()) {
    jsonData += "\"lat\": " + String(gps.location.lat(), 6) + ",";
    jsonData += "\"lon\": " + String(gps.location.lng(), 6);
  } else {
    jsonData += "\"lat\": null,";
    jsonData += "\"lon\": null";
  }
  jsonData += "}";

  

  // Send data to server
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/json");
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
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(1000);
}
