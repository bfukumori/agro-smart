"""Executa a cadeia completa de simulação, processamento, mineração e monitoramento."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulate_sensors import generate_readings, write_csv  # noqa: E402
from pipeline import RAW_PATH, run as run_pipeline  # noqa: E402
from process_mining import run_process_mining  # noqa: E402
from monitor import run_monitoring_cycle  # noqa: E402


def main() -> None:
    print("=" * 60)
    print("           INICIALIZANDO PLATAFORMA AGROSMART              ")
    print("=" * 60)

    # 1. Simulação inicial
    write_csv(generate_readings(hours=48, seed=42), RAW_PATH)
    print(f"[1/4] Simulação IoT concluída: {RAW_PATH}")

    # 2. Pipeline de Processamento e Regras
    summary = run_pipeline()
    print(f"[2/4] Pipeline concluído: {summary['total_readings']} registros, {summary['open_alerts']} alertas.")

    # 3. Mineração de Processos
    insights = run_process_mining()
    print(
        f"[3/4] Mineração de Processos: {insights['distinct_variants']} variantes, "
        f"{insights['total_events']} eventos mapeados."
    )

    # 4. Monitoramento e Integridade
    run_monitoring_cycle(cycles=1, delay_sec=0.1)
    print("[4/4] Monitoramento e Healthcheck operacionais.")

    print("=" * 60)
    print("PLATAFORMA AGROSMART TOTALMENTE OPERACIONAL E ATUALIZADA!")
    print("=" * 60)


if __name__ == "__main__":
    main()
