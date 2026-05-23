import unittest

from src.gateway.coherence import calculate_coherence


class CoherenceTests(unittest.TestCase):
    def test_coherence_decreases_when_drift_rises(self) -> None:
        self.assertGreater(calculate_coherence(0.1), calculate_coherence(0.7))

    def test_coherence_is_bounded(self) -> None:
        self.assertEqual(calculate_coherence(-1.0), 1.0)
        self.assertEqual(calculate_coherence(2.0), 0.0)


if __name__ == "__main__":
    unittest.main()
