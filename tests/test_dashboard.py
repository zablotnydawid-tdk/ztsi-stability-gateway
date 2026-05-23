import tempfile
import unittest
from pathlib import Path

from src.dashboard.runtime_dashboard import RuntimeDashboard
from src.telemetry.metrics import RuntimeTelemetryEngine
from src.telemetry.telemetry_store import TelemetryStore


class DashboardTests(unittest.TestCase):
    def test_dashboard_renders_runtime_summaries_and_charts(self) -> None:
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

            dashboard = RuntimeDashboard(engine).generate()

            self.assertIn("Runtime executions: 1", dashboard["runtime_summary"])
            self.assertIn("APPROVED: 1", dashboard["governance_summary"])
            self.assertIn("Coherence trend:", dashboard["charts"])
            self.assertIn("Drift trend:", dashboard["charts"])


if __name__ == "__main__":
    unittest.main()
