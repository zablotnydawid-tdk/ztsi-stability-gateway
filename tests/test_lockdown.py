import tempfile
import unittest
from pathlib import Path

from src.policy.engine import PolicyEngine, RuntimeLockdownManager


class LockdownTests(unittest.TestCase):
    def test_lockdown_activates_correctly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manager = RuntimeLockdownManager(Path(directory) / "lockdown.json")
            engine = PolicyEngine(lockdown_manager=manager)

            result = engine.evaluate(
                {
                    "lineage_id": "lockdown",
                    "coherence_score": 0.0,
                    "drift_score": 0.9,
                    "contradiction_score": 0.0,
                    "recursive_instability_score": 1.0,
                    "stabilization_applied": False,
                },
                telemetry_summary={},
            )

            self.assertEqual(result["severity"], "LOCKDOWN")
            self.assertTrue(result["lockdown_active"])
            self.assertTrue(manager.is_locked())

    def test_runtime_recovers_from_lockdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manager = RuntimeLockdownManager(Path(directory) / "lockdown.json")
            manager.activate("test")
            self.assertTrue(manager.is_locked())

            manager.release()

            self.assertFalse(manager.is_locked())


if __name__ == "__main__":
    unittest.main()
