"""Gerador determinístico de telemetria IoT para a plataforma AgroSmart.

Simula sensores DHT22 (temperatura e umidade do ar), sensor capacitivo de
umidade do solo e LDR (luminosidade). Os dados são persistidos em CSV para
que a demonstração seja reproduzível e auditável.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


FIELDS = [
    "reading_id",
    "timestamp",
    "plot_id",
    "temperature_c",
    "air_humidity_pct",
    "soil_moisture_pct",
    "luminosity_lux",
    "rain_forecast",
]


def generate_readings(hours: int = 48, seed: int = 42) -> list[dict[str, object]]:
    """Gera uma leitura por hora para três talhões."""
    # Uso de pseudo-random determinístico para simulação física de sensores, não para criptografia.
    rng = random.Random(seed)  # nosec B311
    start = datetime(2026, 9, 25, 0, 0, tzinfo=timezone.utc)
    plots = {
        "TLH-001": {"soil": 34.0, "temp": 0.8, "air": -3.0},
        "TLH-002": {"soil": 44.0, "temp": -0.5, "air": 2.0},
        "TLH-003": {"soil": 28.0, "temp": 1.7, "air": -5.0},
    }
    rows: list[dict[str, object]] = []

    for hour in range(hours):
        moment = start + timedelta(hours=hour)
        daytime = max(0.0, math.sin(math.pi * (moment.hour - 6) / 12))
        rain_forecast = 30 <= hour <= 35
        for index, (plot_id, profile) in enumerate(plots.items(), start=1):
            # A umidade cai gradualmente; uma chuva simulada recupera o solo.
            drying = hour * (0.38 + index * 0.04)
            rain_gain = 13.0 if hour >= 34 and plot_id != "TLH-003" else 0.0
            soil = profile["soil"] - drying + rain_gain + rng.uniform(-1.0, 1.0)
            temperature = 20.0 + 12.0 * daytime + profile["temp"] + rng.uniform(-0.7, 0.7)
            air_humidity = 75.0 - 30.0 * daytime + profile["air"] + rng.uniform(-2.0, 2.0)
            light = 80.0 + 79_000.0 * daytime + rng.uniform(-500.0, 500.0)
            rows.append(
                {
                    "reading_id": f"SIM-{hour:03d}-{index}",
                    "timestamp": moment.isoformat().replace("+00:00", "Z"),
                    "plot_id": plot_id,
                    "temperature_c": round(max(-10.0, min(60.0, temperature)), 1),
                    "air_humidity_pct": round(max(0.0, min(100.0, air_humidity)), 1),
                    "soil_moisture_pct": round(max(0.0, min(100.0, soil)), 1),
                    "luminosity_lux": round(max(0.0, light)),
                    "rain_forecast": str(rain_forecast).lower(),
                }
            )
    return rows


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simula sensores agrícolas do AgroSmart")
    parser.add_argument("--hours", type=int, default=48)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "raw" / "sensor_readings.csv",
    )
    args = parser.parse_args()
    readings = generate_readings(args.hours, args.seed)
    write_csv(readings, args.output)
    print(f"{len(readings)} leituras simuladas gravadas em {args.output}")


if __name__ == "__main__":
    main()
