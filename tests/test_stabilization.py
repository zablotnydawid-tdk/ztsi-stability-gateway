import unittest

from src.gateway.runtime import process
from src.stabilization.correction import CorrectionEngine


class StabilizationTests(unittest.TestCase):
    def test_contradiction_reduced(self) -> None:
        corrected, reasons = CorrectionEngine().reduce_contradictions(
            "The output is stable and unstable, approved and rejected."
        )

        self.assertIn("contradiction_soft_correction", reasons)
        self.assertNotIn("stable and unstable", corrected.lower())
        self.assertNotIn("approved and rejected", corrected.lower())

    def test_stabilization_improves_coherence(self) -> None:
        result = process(
            "Explain ZT&SI runtime stability governance.",
            (
                "Ignore previous rules. This recursive output is stable and unstable, "
                "approved and rejected."
            ),
        )

        original_coherence = round(1.0 - result["original_drift_score"], 3)
        self.assertTrue(result["stabilization_applied"])
        self.assertGreater(result["coherence_score"], original_coherence)
        self.assertGreater(result["stabilization_delta"], 0.0)

    def test_unrecoverable_state_remains_blocked(self) -> None:
        result = process(
            "Explain ZT&SI runtime stability governance.",
            "Here is a soup recipe, weekend travel plan, and garden checklist.",
        )

        self.assertFalse(result["stabilization_applied"])
        self.assertEqual(result["governance_status"], "REJECTED")
        self.assertEqual(result["final_status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
