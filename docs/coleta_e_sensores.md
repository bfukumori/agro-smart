# Coleta de dados do ambiente

## Sensores utilizados

- **DHT22:** mede a temperatura em graus Celsius e a umidade relativa do ar em porcentagem.
- **Sensor capacitivo de umidade do solo:** produz leitura analógica convertida para uma escala de 0% a 100%.
- **LDR:** representa a luminosidade ambiente em lux por meio de uma leitura analógica.
- **ESP32:** microcontrolador que lê os sensores e envia um registro JSON pelo monitor serial.

Os arquivos `simulator/diagram.json` e `simulator/agrosmart_esp32.ino` podem ser abertos no Wokwi, ferramenta equivalente ao TinkerCad. Para garantir que a entrega funcione sem internet, `src/simulate_sensors.py` reproduz as mesmas grandezas para três talhões ao longo de 48 horas.

## Exemplo de leitura

```json
{
  "reading_id": "SIM-023-1",
  "timestamp": "2026-09-25T23:00:00Z",
  "plot_id": "TLH-001",
  "temperature_c": 21.2,
  "air_humidity_pct": 71.4,
  "soil_moisture_pct": 23.6,
  "luminosity_lux": 140,
  "rain_forecast": false
}
```

## Eventos simulados

O cenário reduz gradualmente a umidade do solo, cria picos diurnos de temperatura e luminosidade e introduz previsão de chuva entre as horas 30 e 35. Depois da hora 34, a umidade dos talhões 1 e 2 aumenta para representar precipitação. O talhão 3 permanece seco para produzir um caso crítico e demonstrar a recomendação automática.
