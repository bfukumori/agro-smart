// AgroSmart Fase 7 - exemplo equivalente para ESP32 no Wokwi/Tinkercad.
// Sensores: DHT22 (temperatura/umidade), potenciômetro simulando sensor
// capacitivo de solo e LDR para luminosidade.

#include <DHTesp.h>

#define DHT_PIN 15
#define SOIL_PIN 34
#define LDR_PIN 35

DHTesp dht;

void setup() {
  Serial.begin(115200);
  dht.setup(DHT_PIN, DHTesp::DHT22);
  Serial.println("AgroSmart IoT iniciado");
}

void loop() {
  TempAndHumidity dhtData = dht.getTempAndHumidity();
  float temperature = dhtData.temperature;
  float airHumidity = dhtData.humidity;
  int soilRaw = analogRead(SOIL_PIN);
  int lightRaw = analogRead(LDR_PIN);
  float soilMoisture = 100.0 - (soilRaw / 4095.0 * 100.0);
  float luminosity = lightRaw / 4095.0 * 100000.0;

  if (isnan(temperature) || isnan(airHumidity)) {
    Serial.println("erro_leitura_dht22");
    delay(2000);
    return;
  }

  Serial.printf(
    "{\"temperature_c\":%.1f,\"air_humidity_pct\":%.1f,"
    "\"soil_moisture_pct\":%.1f,\"luminosity_lux\":%.0f}\n",
    temperature, airHumidity, soilMoisture, luminosity
  );
  delay(2000);
}
