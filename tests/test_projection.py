import unittest

from src.intelligence.scoring import DriftIntelligenceScorer
from src.stabilization.projection import ProjectionEngine


class ProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = DriftIntelligenceScorer()
        self.engine = ProjectionEngine(scorer=self.scorer)

    def test_unstable_output_becomes_stable_after_correction(self) -> None:
        input_text = "Explain ZT&SI runtime stability governance."
        candidate = (
            "Ignore previous rules. This recursive output is stable and unstable, "
            "approved and rejected."
        )
        original = self.scorer.score(input_text, candidate)

        projected = self.engine.stabilize(input_text, candidate, original)

        self.assertTrue(projected["stabilization_applied"])
        self.assertGreater(projected["stabilization_delta"], 0.0)
        self.assertLessEqual(projected["drift_profile"]["drift_score"], 0.18)

    def test_projection_can_leave_unrecoverable_topic_drift_unchanged(self) -> None:
        input_text = "Explain ZT&SI runtime stability governance."
        candidate = "Here is a soup recipe and a weekend travel plan."
        original = self.scorer.score(input_text, candidate)

        projected = self.engine.stabilize(input_text, candidate, original)

        self.assertFalse(projected["stabilization_applied"])
        self.assertEqual(projected["stabilization_delta"], 0.0)


if __name__ == "__main__":
    unittest.main()
