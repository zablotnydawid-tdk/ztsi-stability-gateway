import tempfile
import unittest
from pathlib import Path

from src.memory.graph import DirectedSemanticGraph
from src.memory.lineage_graph import LineageGraph
from src.memory.rollback import RollbackEngine
from src.memory.semantic_memory import SemanticMemoryStore
from src.memory.snapshots import SnapshotManager


class RollbackTests(unittest.TestCase):
    def test_rollback_restores_stable_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            store = SemanticMemoryStore(base)
            graph = LineageGraph(DirectedSemanticGraph(base / "lineage_graph.json"))
            snapshots = SnapshotManager(base / "snapshots")

            stable = store.store_state(
                {
                    "lineage_id": "stable",
                    "coherence_score": 0.9,
                    "drift_score": 0.1,
                    "governance_status": "APPROVED",
                    "firewall_status": "ALLOWED",
                    "final_status": "ALLOWED",
                    "stabilization_applied": False,
                    "timestamp": "2026-05-23T00:00:00+00:00",
                }
            )
            unstable = store.store_state(
                {
                    "lineage_id": "unstable",
                    "coherence_score": 0.4,
                    "drift_score": 0.6,
                    "governance_status": "REJECTED",
                    "firewall_status": "BLOCKED",
                    "final_status": "BLOCKED",
                    "stabilization_applied": False,
                    "timestamp": "2026-05-23T00:00:01+00:00",
                },
                parent_state_id="stable",
            )
            graph.add_state(stable)
            graph.add_state(unstable)
            graph.connect_parent("unstable", "stable")
            snapshots.create_snapshot(stable)

            result = RollbackEngine(store, graph, snapshots).rollback("unstable")

            self.assertTrue(result["rollback_performed"])
            self.assertEqual(result["restored_lineage_id"], "stable")
            self.assertEqual(result["restored_coherence"], 0.9)


if __name__ == "__main__":
    unittest.main()
