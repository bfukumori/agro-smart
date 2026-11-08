import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from monitor import collect_system_metrics  # noqa: E402
from pipeline import classify_risk, load_and_validate  # noqa: E402
from process_mining import analyze_process, generate_event_log  # noqa: E402
from simulate_sensors import generate_readings, write_csv  # noqa: E402


class AgroSmartPipelineTests(unittest.TestCase):
    def test_irrigation_is_triggered_for_dry_soil_without_rain(self):
        row = {
            "soil_moisture_pct": 18.0,
            "temperature_c": 28.0,
            "luminosity_lux": 30_000.0,
            "rain_forecast": False,
        }
        level, score, actions = classify_risk(row)
        self.assertEqual(level, "ATENCAO")
        self.assertEqual(score, 55)
        self.assertEqual(actions[0]["type"], "IRRIGACAO")

    def test_rain_forecast_postpones_irrigation(self):
        row = {
            "soil_moisture_pct": 18.0,
            "temperature_c": 28.0,
            "luminosity_lux": 30_000.0,
            "rain_forecast": True,
        }
        level, score, actions = classify_risk(row)
        self.assertEqual(level, "ATENCAO")
        self.assertEqual(score, 55)
        self.assertEqual(actions[0]["type"], "RECOMENDACAO")
        self.assertIn("Adiar irrigação", actions[0]["message"])

    def test_combined_heat_and_drought_is_critical(self):
        row = {
            "soil_moisture_pct": 15.0,
            "temperature_c": 35.0,
            "luminosity_lux": 80_000.0,
            "rain_forecast": False,
        }
        level, score, actions = classify_risk(row)
        self.assertEqual(level, "CRITICO")
        self.assertEqual(score, 95)
        self.assertEqual(len(actions), 3)

    def test_simulator_output_passes_validation(self):
        path = Path(__file__).parent / "_test_readings.csv"
        try:
            write_csv(generate_readings(hours=2), path)
            valid, rejected = load_and_validate(path)
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual(len(valid), 6)
        self.assertEqual(rejected, [])

    def test_process_mining_event_log_and_variants(self):
        rows = [
            {
                "reading_id": "TEST-001",
                "timestamp": "2026-09-25T12:00:00Z",
                "plot_id": "TLH-001",
                "temperature_c": 25.0,
                "air_humidity_pct": 60.0,
                "soil_moisture_pct": 15.0,
                "luminosity_lux": 40_000.0,
                "rain_forecast": False,
                "risk_level": "ATENCAO",
                "risk_score": 55,
            }
        ]
        event_log = generate_event_log(rows)
        self.assertGreaterEqual(len(event_log), 6)
        insights = analyze_process(event_log)
        self.assertEqual(insights["total_cases_analyzed"], 1)
        self.assertGreaterEqual(insights["distinct_variants"], 1)

    def test_health_monitoring_metrics(self):
        metrics = collect_system_metrics(total_readings=100, rejected=0, alerts_count=3, cycle_duration_ms=120.5)
        self.assertEqual(metrics["status"], "HEALTHY")
        self.assertEqual(metrics["kpis"]["data_quality_compliance_pct"], 100.0)
        self.assertGreater(metrics["kpis"]["throughput_readings_per_sec"], 0)


if __name__ == "__main__":
    unittest.main()
