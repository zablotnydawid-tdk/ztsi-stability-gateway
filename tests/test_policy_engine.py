import tempfile
import unittest
from pathlib import Path

from src.policy.engine import PolicyEngine, RuntimeLockdownManager
from src.policy.loader import PolicyLoader


class PolicyEngineTests(unittest.TestCase):
    def test_policy_loading_works(self) -> None:
        policy = PolicyLoader().load()

        self.assertEqual(policy["minimum_coherence"], 0.82)
        self.assertEqual(policy["maximum_drift"], 0.18)
        self.assertTrue(policy["allow_projection_recovery"])

    def test_invalid_policy_falls_back_safely(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_policy.yaml"
            path.write_text("minimum_coherence: not-a-number\n", encoding="utf-8")

            policy = PolicyLoader(path).load()

            self.assertEqual(policy["minimum_coherence"], 0.82)
            self.assertEqual(policy["maximum_drift"], 0.18)

    def test_policy_engine_blocks_critical_violation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            engine = PolicyEngine(
                lockdown_manager=RuntimeLockdownManager(Path(directory) / "lockdown.json")
            )
            result = engine.evaluate(
                {
                    "lineage_id": "bad",
                    "coherence_score": 0.4,
                    "drift_score": 0.5,
                    "contradiction_score": 0.0,
                    "recursive_instability_score": 0.0,
                    "stabilization_applied": False,
                },
                telemetry_summary={},
            )

            self.assertEqual(result["severity"], "CRITICAL")
            self.assertEqual(result["governance_decision"], "REJECTED")
            self.assertTrue(result["violations"])


if __name__ == "__main__":
    unittest.main()
