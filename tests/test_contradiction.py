import unittest

from src.intelligence.contradiction import ContradictionAnalyzer


class ContradictionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = ContradictionAnalyzer()

    def test_detects_self_contradiction(self) -> None:
        score = self.analyzer.analyze(
            "Evaluate stable gateway output.",
            "The output is stable and unstable, approved and rejected.",
        )

        self.assertGreaterEqual(score, 0.6)

    def test_stable_claim_has_low_contradiction(self) -> None:
        score = self.analyzer.analyze(
            "Approve coherent gateway output.",
            "The gateway approves coherent output after governance validation.",
        )

        self.assertEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
