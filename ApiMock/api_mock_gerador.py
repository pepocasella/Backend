from datetime import datetime, timedelta
import random
import json

# Função para gerar um único data point
def gerar_data_point(data, estacao_id="ESP8266_01"):
    return {
        "timestamp": data.isoformat(),
        "estacao_id": estacao_id,
        "sensores": {
            "LM35": {
                "id": "LM35_01",
                "tipo": "temperatura",
                "unidade": "°C",
                "valor": round(random.uniform(20.0, 30.0), 1)
            },
            "DHT11": {
                "id": "DHT11_01",
                "tipo": "temperatura_umidade",
                "temperatura": {
                    "unidade": "°C",
                    "valor": round(random.uniform(20.0, 30.0), 1)
                },
                "umidade": {
                    "unidade": "%",
                    "valor": round(random.uniform(40.0, 70.0), 1)
                }
            },
            "BMP280": {
                "id": "BMP280_01",
                "tipo": "pressao_temperatura",
                "temperatura": {
                    "unidade": "°C",
                    "valor": round(random.uniform(20.0, 30.0), 1)
                },
                "pressao": {
                    "unidade": "hPa",
                    "valor": round(random.uniform(1000.0, 1020.0), 2)
                }
            }
        }
    }

# Gerar os 50 data points entre 2025-01-01 e 2025-01-10, 5 por dia
data_inicial = datetime(2025, 1, 1, 0, 0)
data_points = []

for dia in range(10):
    for ponto in range(5):
        timestamp = data_inicial + timedelta(days=dia, hours=ponto * 4)  # intervalo de 4h entre pontos
        data_points.append(gerar_data_point(timestamp))

# Exibir os primeiros 2 como amostra e gerar o JSON completo
amostra = data_points[:2]
json_resultado = json.dumps(data_points, indent=2)

amostra, json_resultado[:1000]  # Mostrar os dois primeiros pontos e o início do JSON final para visualização parcial
