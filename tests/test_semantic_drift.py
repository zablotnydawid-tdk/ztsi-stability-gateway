import unittest

from src.intelligence.semantic_drift import SemanticDriftEngine


class SemanticDriftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = SemanticDriftEngine()

    def test_stable_semantic_continuity_has_high_similarity(self) -> None:
        metrics = self.engine.analyze(
            "Explain ZT&SI runtime stability governance.",
            (
                "ZT&SI runtime stability governance preserves coherence, "
                "measures drift, and validates output manifestation."
            ),
        )

        self.assertGreaterEqual(metrics["semantic_similarity"], 0.45)
        self.assertLess(metrics["semantic_drift_score"], 0.55)

    def test_topic_deviation_has_high_semantic_drift(self) -> None:
        metrics = self.engine.analyze(
            "Explain ZT&SI runtime stability governance.",
            "Here is a recipe for soup, weekend travel, and garden planning.",
        )

        self.assertLess(metrics["semantic_similarity"], 0.25)
        self.assertGreater(metrics["semantic_drift_score"], 0.75)


if __name__ == "__main__":
    unittest.main()
