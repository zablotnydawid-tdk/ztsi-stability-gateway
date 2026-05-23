import json
import tempfile
import unittest
from pathlib import Path

from src.gateway.lineage import create_lineage_id, log_state
from src.gateway.state import SemanticState


class LineageTests(unittest.TestCase):
    def test_lineage_id_is_unique_and_prefixed(self) -> None:
        first = create_lineage_id()
        second = create_lineage_id()
        self.assertTrue(first.startswith("ztsi-"))
        self.assertTrue(second.startswith("ztsi-"))
        self.assertNotEqual(first, second)

    def test_lineage_log_writes_jsonl_record(self) -> None:
        state = SemanticState(
            input_text="input",
            candidate_output="output",
            coherence_score=1.0,
            drift_score=0.0,
            governance_status="APPROVED",
            lineage_id=create_lineage_id(),
            final_status="ALLOWED",
        )

        with tempfile.TemporaryDirectory() as directory:
            log_path = Path(directory) / "lineage.jsonl"
            record = log_state(state, log_path)
            lines = log_path.read_text(encoding="utf-8").splitlines()

        self.assertEqual(len(lines), 1)
        parsed = json.loads(lines[0])
        self.assertEqual(parsed["lineage_id"], state.lineage_id)
        self.assertEqual(parsed["timestamp"], record["timestamp"])


if __name__ == "__main__":
    unittest.main()
