"""Pipeline Raw -> Silver -> Gold e motor de decisões do AgroSmart."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "sensor_readings.csv"
SILVER_PATH = ROOT / "data" / "processed" / "telemetry_processed.csv"
ALERTS_PATH = ROOT / "data" / "output" / "alerts.json"
SUMMARY_PATH = ROOT / "data" / "output" / "dashboard_summary.json"
WEB_DATA_PATH = ROOT / "dashboard" / "data.js"

NUMERIC_FIELDS = {
    "temperature_c": (-10.0, 60.0),
    "air_humidity_pct": (0.0, 100.0),
    "soil_moisture_pct": (0.0, 100.0),
    "luminosity_lux": (0.0, 150_000.0),
}


def parse_boolean(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes", "sim"}


def load_and_validate(path: Path) -> tuple[list[dict], list[dict]]:
    """Converte tipos e separa registros inválidos sem interromper o lote."""
    valid: list[dict] = []
    rejected: list[dict] = []
    with path.open(encoding="utf-8", newline="") as stream:
        for line_number, raw in enumerate(csv.DictReader(stream), start=2):
            try:
                row = dict(raw)
                datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
                for field, (minimum, maximum) in NUMERIC_FIELDS.items():
                    value = float(row[field])
                    if not minimum <= value <= maximum:
                        raise ValueError(f"{field} fora do intervalo")
                    row[field] = value
                if not row["plot_id"].startswith("TLH-"):
                    raise ValueError("plot_id inválido")
                row["rain_forecast"] = parse_boolean(row["rain_forecast"])
                row["quality_status"] = "APROVADO"
                valid.append(row)
            except (KeyError, TypeError, ValueError) as exc:
                rejected.append({"line": line_number, "reason": str(exc), "record": raw})
    valid.sort(key=lambda item: (item["timestamp"], item["plot_id"]))
    return valid, rejected


def classify_risk(row: dict) -> tuple[str, int, list[dict]]:
    """Aplica regras transparentes e retorna risco, score e decisões."""
    soil = row["soil_moisture_pct"]
    temperature = row["temperature_c"]
    light = row["luminosity_lux"]
    rain = row["rain_forecast"]
    score = 0
    actions: list[dict] = []

    if soil < 20:
        score += 55
        if rain:
            actions.append({"type": "RECOMENDACAO", "message": "Adiar irrigação e reavaliar após a chuva prevista."})
        else:
            actions.append({"type": "IRRIGACAO", "message": "Ativar irrigação por 30 minutos e medir novamente."})
    elif soil < 30:
        score += 30
        actions.append({"type": "ALERTA", "message": "Umidade do solo em atenção; acompanhar nas próximas 2 horas."})

    if temperature > 32:
        score += 25
        actions.append({
            "type": "ALERTA",
            "message": "Temperatura elevada; evitar aplicação de defensivos neste horário."
        })

    if light > 75_000 and temperature > 30:
        score += 15
        actions.append({
            "type": "RECOMENDACAO",
            "message": "Risco de estresse térmico; priorizar irrigação no início da noite."
        })

    score = min(score, 100)
    level = "CRITICO" if score >= 60 else "ATENCAO" if score >= 30 else "NORMAL"
    if not actions:
        actions.append({"type": "MONITORAMENTO", "message": "Condições dentro dos limites; manter monitoramento."})
    return level, score, actions


def process(rows: list[dict]) -> tuple[list[dict], list[dict], dict]:
    processed: list[dict] = []
    alerts: list[dict] = []
    by_plot: dict[str, list[dict]] = defaultdict(list)

    for row in rows:
        level, score, actions = classify_risk(row)
        enriched = {**row, "risk_level": level, "risk_score": score}
        processed.append(enriched)
        by_plot[row["plot_id"]].append(enriched)
        if level != "NORMAL":
            for action in actions:
                alerts.append(
                    {
                        "alert_id": f"ALT-{len(alerts) + 1:04d}",
                        "timestamp": row["timestamp"],
                        "plot_id": row["plot_id"],
                        "severity": level,
                        "risk_score": score,
                        "action_type": action["type"],
                        "recommendation": action["message"],
                    }
                )

    latest = {plot: values[-1] for plot, values in by_plot.items()}
    statuses = Counter(item["risk_level"] for item in latest.values())
    # Carregar insights de mineração e integridade se disponíveis
    pm_insights = None
    pm_path = ROOT / "data" / "output" / "process_mining_insights.json"
    if pm_path.exists():
        try:
            pm_insights = json.loads(pm_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pm_insights = None

    health_info = None
    health_path = ROOT / "data" / "output" / "health_status.json"
    if health_path.exists():
        try:
            health_info = json.loads(health_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            health_info = None

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": "Simulação IoT AgroSmart",
        "total_readings": len(processed),
        "active_plots": len(by_plot),
        "rejected_readings": 0,
        "open_alerts": sum(1 for item in latest.values() if item["risk_level"] != "NORMAL"),
        "critical_plots": statuses["CRITICO"],
        "latest": list(latest.values()),
        "series": processed,
        "alerts": alerts[-12:][::-1],
        "rules": [
            {"condition": "Umidade do solo < 20% e sem chuva", "decision": "Ativar irrigação por 30 min"},
            {"condition": "Umidade do solo entre 20% e 30%", "decision": "Gerar alerta de atenção"},
            {"condition": "Temperatura > 32 °C", "decision": "Evitar defensivos no horário"},
            {"condition": "Luz > 75.000 lux e temperatura > 30 °C", "decision": "Alertar estresse térmico"},
        ],
        "process_mining": pm_insights,
        "health": health_info,
    }
    return processed, alerts, summary


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("Nenhum registro válido para gravar")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(data: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def run() -> dict:
    valid, rejected = load_and_validate(RAW_PATH)
    processed, alerts, summary = process(valid)
    summary["rejected_readings"] = len(rejected)
    write_csv(processed, SILVER_PATH)
    write_json(alerts, ALERTS_PATH)
    write_json(summary, SUMMARY_PATH)
    WEB_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    WEB_DATA_PATH.write_text(
        "window.AGROSMART_DATA = " + json.dumps(summary, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    if rejected:
        write_json(rejected, ROOT / "data" / "output" / "rejected_readings.json")
    print(
        f"Pipeline concluído: {len(processed)} leituras, {len(alerts)} decisões, "
        f"{len(rejected)} rejeições."
    )
    return summary


if __name__ == "__main__":
    run()
