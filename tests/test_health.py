import tempfile
import unittest
from pathlib import Path

from src.telemetry.health import RuntimeHealthMonitor
from src.telemetry.metrics import RuntimeTelemetryEngine
from src.telemetry.telemetry_store import TelemetryStore


class HealthTests(unittest.TestCase):
    def test_runtime_health_stable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = TelemetryStore(Path(directory) / "telemetry.jsonl")
            engine = RuntimeTelemetryEngine(store)
            engine.emit_runtime_event(
                {
                    "lineage_id": "stable",
                    "coherence_score": 0.9,
                    "drift_score": 0.1,
                    "governance_status": "APPROVED",
                    "firewall_status": "ALLOWED",
                    "final_status": "ALLOWED",
                    "stabilization_applied": False,
                    "recursive_instability_score": 0.0,
                    "contradiction_score": 0.0,
                    "snapshot_created": True,
                }
            )

            health = RuntimeHealthMonitor(engine.aggregator).health()

            self.assertEqual(health["runtime_health"], "STABLE")
            self.assertEqual(health["average_coherence"], 0.9)

    def test_runtime_health_critical_when_blocked_dominates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = TelemetryStore(Path(directory) / "telemetry.jsonl")
            engine = RuntimeTelemetryEngine(store)
            for index in range(3):
                engine.emit_runtime_event(
                    {
                        "lineage_id": f"blocked-{index}",
                        "coherence_score": 0.4,
                        "drift_score": 0.6,
                        "governance_status": "REJECTED",
                        "firewall_status": "BLOCKED",
                        "final_status": "BLOCKED",
                        "stabilization_applied": False,
                        "recursive_instability_score": 0.0,
                        "contradiction_score": 0.0,
                        "snapshot_created": False,
                    }
                )

            health = RuntimeHealthMonitor(engine.aggregator).health()

            self.assertEqual(health["runtime_health"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
