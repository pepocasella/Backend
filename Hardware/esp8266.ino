#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>
#include <time.h>

// ======== CONFIG Wi-Fi =========
const char* ssid = "Casella";
const char* password = "casellaadmin";

// ======== CONFIG API ===========
const char* serverName = "http://SEU_ENDPOINT_DJANGO_NINJA/api/sensores/";

// ======== CONFIG SENSORES ======
#define DHTPIN 4  // GPIO4 = D2 no NodeMCU
#define DHTTYPE DHT11
#define LM35PIN A0

DHT dht(DHTPIN, DHTTYPE);

// ========== Função Timestamp ==========
String getISOTime() {
  time_t now = time(nullptr);
  struct tm* t = localtime(&now);
  char buf[30];
  strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%S-03:00", t);  // fixo -03:00
  return String(buf);
}

void setup() {
  Serial.begin(115200);
  delay(100);

  // Iniciar sensor
  dht.begin();

  // Conectar Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  Serial.println(WiFi.localIP());

  // Configurar NTP para hora
  configTime(-3 * 3600, 0, "pool.ntp.org", "time.nist.gov");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float tempDHT = dht.readTemperature();
    float umidade = dht.readHumidity();

    int rawLM35 = analogRead(LM35PIN);
    float voltsLM35 = (rawLM35 / 1023.0) * 3.3;
    float tempLM35 = voltsLM35 * 100;

    String timestamp = getISOTime();

    // Montar JSON
    String json = "{";
    json += "\"timestamp\":\"" + timestamp + "\",";
    json += "\"estacao_id\":\"ESP8266_01\",";
    json += "\"sensores\":{";

    json += "\"LM35\":{";
    json += "\"id\":\"LM35_01\",";
    json += "\"tipo\":\"temperatura\",";
    json += "\"unidade\":\"°C\",";
    json += "\"valor\":" + String(tempLM35, 2);
    json += "},";

    json += "\"DHT11\":{";
    json += "\"id\":\"DHT11_01\",";
    json += "\"tipo\":\"temperatura_umidade\",";
    json += "\"temperatura\":{";
    json += "\"unidade\":\"°C\",";
    json += "\"valor\":" + String(tempDHT, 2);
    json += "},";
    json += "\"umidade\":{";
    json += "\"unidade\":\"%\",";
    json += "\"valor\":" + String(umidade, 2);
    json += "}";
    json += "}";

    json += "}}";

    // Print JSON
    Serial.println("======= JSON ENVIADO =======");
    Serial.println(json);

    // Enviar para API
    HTTPClient http;
    // http.begin(serverName);
    // http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(json);
    Serial.print("HTTP Status: ");
    Serial.println(httpCode);

    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Resposta:");
      Serial.println(response);
    }

    http.end();
  } else {
    Serial.println("Wi-Fi desconectado. Reconectando...");
    WiFi.begin(ssid, password);
  }

  delay(1000);
}
