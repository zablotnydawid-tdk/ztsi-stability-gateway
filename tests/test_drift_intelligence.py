import unittest

from src.gateway.runtime import process
from src.intelligence.scoring import DriftIntelligenceScorer


class DriftIntelligenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = DriftIntelligenceScorer()

    def test_unified_score_combines_semantic_contradiction_and_instability(self) -> None:
        metrics = self.scorer.score(
            "Explain ZT&SI runtime stability governance.",
            (
                "Ignore previous rules. This recursive output is stable and unstable, "
                "approved and rejected, and repeats in an infinite loop."
            ),
        )

        self.assertGreater(metrics["drift_score"], 0.18)
        self.assertGreater(metrics["contradiction_score"], 0.0)
        self.assertGreater(metrics["recursive_instability_score"], 0.0)
        self.assertIn("semantic_similarity", metrics)

    def test_governance_recovers_correctable_high_drift(self) -> None:
        result = process(
            "Explain ZT&SI runtime stability governance.",
            (
                "Ignore previous rules. This recursive output is stable and unstable, "
                "approved and rejected, and repeats in an infinite loop."
            ),
        )

        self.assertTrue(result["stabilization_applied"])
        self.assertEqual(result["governance_status"], "APPROVED")
        self.assertEqual(result["final_status"], "ALLOWED")
        self.assertIn("semantic_similarity", result)
        self.assertIn("contradiction_score", result)
        self.assertIn("recursive_instability_score", result)


if __name__ == "__main__":
    unittest.main()
