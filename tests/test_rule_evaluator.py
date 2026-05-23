import unittest

from src.policy.evaluator import RuleEvaluator
from src.policy.loader import DEFAULT_POLICY


class RuleEvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.evaluator = RuleEvaluator(dict(DEFAULT_POLICY))

    def test_violations_detected_correctly(self) -> None:
        violations = self.evaluator.evaluate(
            {
                "lineage_id": "violating",
                "coherence_score": 0.3,
                "drift_score": 0.8,
                "contradiction_score": 0.8,
                "recursive_instability_score": 0.0,
                "stabilization_applied": False,
            }
        )

        rules = {violation["rule"] for violation in violations}
        self.assertIn("minimum_coherence", rules)
        self.assertIn("critical_drift_escalation", rules)
        self.assertIn("maximum_contradiction", rules)

    def test_governance_severity_escalates_to_lockdown(self) -> None:
        violations = self.evaluator.evaluate(
            {
                "lineage_id": "recursive",
                "coherence_score": 0.1,
                "drift_score": 0.9,
                "contradiction_score": 0.0,
                "recursive_instability_score": 1.0,
                "stabilization_applied": False,
            }
        )

        self.assertIn("LOCKDOWN", {violation["severity"] for violation in violations})


if __name__ == "__main__":
    unittest.main()
