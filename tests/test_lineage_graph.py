import tempfile
import unittest
from pathlib import Path

from src.memory.graph import DirectedSemanticGraph
from src.memory.lineage_graph import LineageGraph


class LineageGraphTests(unittest.TestCase):
    def test_lineage_ancestry_reconstruction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            graph = LineageGraph(DirectedSemanticGraph(Path(directory) / "graph.json"))
            graph.add_state({"lineage_id": "root", "coherence_score": 0.9})
            graph.add_state({"lineage_id": "child", "coherence_score": 0.88})
            graph.add_state({"lineage_id": "grandchild", "coherence_score": 0.86})
            graph.connect_parent("child", "root")
            graph.connect_parent("grandchild", "child")

            self.assertEqual(graph.reconstruct_path("grandchild"), ["root", "child", "grandchild"])
            self.assertEqual(graph.get_ancestry("grandchild"), ["root", "child"])
            self.assertEqual(graph.get_descendants("root"), ["child", "grandchild"])


if __name__ == "__main__":
    unittest.main()
