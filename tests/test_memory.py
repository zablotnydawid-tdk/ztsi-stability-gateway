import tempfile
import unittest
from pathlib import Path

from src.memory.retrieval import MemoryRetrievalEngine
from src.memory.semantic_memory import SemanticMemoryStore


class MemoryTests(unittest.TestCase):
    def test_stable_state_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SemanticMemoryStore(Path(directory))
            state = {
                "lineage_id": "state-1",
                "input_text": "input",
                "candidate_output": "output",
                "drift_score": 0.1,
                "coherence_score": 0.9,
                "governance_status": "APPROVED",
                "firewall_status": "ALLOWED",
                "final_status": "ALLOWED",
                "stabilization_applied": False,
                "timestamp": "2026-05-23T00:00:00+00:00",
            }

            record = store.store_state(state)
            loaded = store.get_state("state-1")

            self.assertEqual(record["lineage_id"], "state-1")
            self.assertEqual(loaded["governance_status"], "APPROVED")
            self.assertEqual(len(store.all_states()), 1)

    def test_retrieval_stable_and_unstable_states(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = SemanticMemoryStore(Path(directory))
            store.store_state(
                {
                    "lineage_id": "stable",
                    "governance_status": "APPROVED",
                    "firewall_status": "ALLOWED",
                    "coherence_score": 0.9,
                    "drift_score": 0.1,
                    "stabilization_applied": False,
                    "timestamp": "2026-05-23T00:00:00+00:00",
                }
            )
            store.store_state(
                {
                    "lineage_id": "unstable",
                    "governance_status": "REJECTED",
                    "firewall_status": "BLOCKED",
                    "coherence_score": 0.4,
                    "drift_score": 0.6,
                    "stabilization_applied": False,
                    "timestamp": "2026-05-23T00:00:01+00:00",
                }
            )
            retrieval = MemoryRetrievalEngine(store)

            self.assertEqual(retrieval.retrieve_stable_states()[0]["lineage_id"], "stable")
            self.assertEqual(retrieval.retrieve_unstable_states()[0]["lineage_id"], "unstable")
            self.assertEqual(retrieval.retrieve_recent(1)[0]["lineage_id"], "unstable")


if __name__ == "__main__":
    unittest.main()
