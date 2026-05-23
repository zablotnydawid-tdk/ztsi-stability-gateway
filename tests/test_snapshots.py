import tempfile
import unittest
from pathlib import Path

from src.memory.snapshots import SnapshotManager


class SnapshotTests(unittest.TestCase):
    def test_stable_state_creates_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manager = SnapshotManager(Path(directory))
            snapshot = manager.create_snapshot(
                {
                    "lineage_id": "stable",
                    "coherence_score": 0.9,
                    "drift_score": 0.1,
                    "governance_status": "APPROVED",
                    "firewall_status": "ALLOWED",
                    "timestamp": "2026-05-23T00:00:00+00:00",
                }
            )

            self.assertIsNotNone(snapshot)
            self.assertEqual(manager.snapshot_count(), 1)

    def test_unstable_states_not_snapshotted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manager = SnapshotManager(Path(directory))
            snapshot = manager.create_snapshot(
                {
                    "lineage_id": "unstable",
                    "coherence_score": 0.5,
                    "drift_score": 0.5,
                    "governance_status": "REJECTED",
                    "firewall_status": "BLOCKED",
                    "timestamp": "2026-05-23T00:00:00+00:00",
                }
            )

            self.assertIsNone(snapshot)
            self.assertEqual(manager.snapshot_count(), 0)


if __name__ == "__main__":
    unittest.main()
