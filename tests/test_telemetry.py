import tempfile
import unittest
from pathlib import Path

from src.telemetry.aggregation import TelemetryAggregator
from src.telemetry.metrics import RuntimeTelemetryEngine
from src.telemetry.telemetry_store import TelemetryStore


class TelemetryTests(unittest.TestCase):
    def test_telemetry_events_emitted_and_aggregated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = TelemetryStore(Path(directory) / "telemetry.jsonl")
            engine = RuntimeTelemetryEngine(store)
            engine.emit_runtime_event(
                {
                    "lineage_id": "a",
                    "coherence_score": 0.9,
                    "drift_score": 0.1,
                    "governance_status": "APPROVED",
                    "firewall_status": "ALLOWED",
                    "final_status": "ALLOWED",
                    "stabilization_applied": False,
                    "recursive_instability_score": 0.0,
                    "contradiction_score": 0.0,
                    "snapshot_created": True,
                    "lineage_path": ["a"],
                }
            )
            engine.emit_runtime_event(
                {
                    "lineage_id": "b",
                    "coherence_score": 0.5,
                    "drift_score": 0.5,
                    "governance_status": "REJECTED",
                    "firewall_status": "BLOCKED",
                    "final_status": "BLOCKED",
                    "stabilization_applied": True,
                    "recursive_instability_score": 0.2,
                    "contradiction_score": 0.3,
                    "snapshot_created": False,
                    "lineage_path": ["a", "b"],
                }
            )

            summary = TelemetryAggregator(store).aggregate_runtime_summary()

            self.assertEqual(summary["total_runtime_executions"], 2)
            self.assertEqual(summary["approved_outputs"], 1)
            self.assertEqual(summary["blocked_outputs"], 1)
            self.assertEqual(summary["average_coherence"], 0.7)
            self.assertEqual(summary["average_drift"], 0.3)
            self.assertEqual(summary["recursive_instability_frequency"], 0.5)
            self.assertEqual(summary["contradiction_frequency"], 0.5)

    def test_rollback_metrics_tracked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = TelemetryStore(Path(directory) / "telemetry.jsonl")
            engine = RuntimeTelemetryEngine(store)
            engine.emit_rollback_event(
                {
                    "restored_lineage_id": "stable",
                    "restored_coherence": 0.91,
                    "requested_lineage_id": "unstable",
                }
            )

            summary = TelemetryAggregator(store).aggregate_runtime_summary()

            self.assertEqual(summary["rollback_count"], 1)


if __name__ == "__main__":
    unittest.main()
