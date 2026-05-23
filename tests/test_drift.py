import unittest

from src.gateway.drift import (
    calculate_drift,
    detect_contradiction,
    detect_topic_deviation,
    detect_unstable_recursive_language,
)


class DriftTests(unittest.TestCase):
    def test_detects_contradiction(self) -> None:
        self.assertTrue(detect_contradiction("The gateway is stable and unstable."))

    def test_detects_topic_deviation(self) -> None:
        self.assertTrue(
            detect_topic_deviation(
                "Evaluate gateway governance and coherence.",
                "Here is a recipe for soup and weekend travel.",
            )
        )

    def test_detects_unstable_recursive_language(self) -> None:
        self.assertTrue(
            detect_unstable_recursive_language(
                "This output validates itself in a recursive infinite loop."
            )
        )

    def test_stable_output_has_low_drift(self) -> None:
        drift = calculate_drift(
            "Summarize gateway governance and coherence.",
            "Gateway governance uses coherence scoring to approve stable outputs.",
        )
        self.assertLessEqual(drift, 0.18)

    def test_unstable_output_has_high_drift(self) -> None:
        drift = calculate_drift(
            "Summarize gateway governance and coherence.",
            "This recursive output is stable and unstable and talks about gardening.",
        )
        self.assertGreater(drift, 0.18)


if __name__ == "__main__":
    unittest.main()
