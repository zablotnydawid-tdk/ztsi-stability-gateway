import json
from datetime import datetime, timezone
from pathlib import Path


RUNTIME_MEMORY_DIR = Path("runtime_memory")
STATES_DIR = RUNTIME_MEMORY_DIR / "states"


class SemanticMemoryStore:
    def __init__(self, memory_dir: Path = RUNTIME_MEMORY_DIR) -> None:
        self.memory_dir = memory_dir
        self.states_dir = memory_dir / "states"
        self.index_path = memory_dir / "states.jsonl"

    def store_state(self, state: dict, parent_state_id: str | None = None) -> dict:
        self.states_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "lineage_id": state["lineage_id"],
            "input_text": state.get("input_text", ""),
            "candidate_output": state.get("candidate_output", ""),
            "drift_score": state.get("drift_score", 0.0),
            "coherence_score": state.get("coherence_score", 0.0),
            "governance_status": state.get("governance_status", "PENDING"),
            "firewall_status": state.get("firewall_status", state.get("final_status", "PENDING")),
            "stabilization_applied": state.get("stabilization_applied", False),
            "timestamp": state.get("timestamp") or datetime.now(timezone.utc).isoformat(),
            "parent_state_id": parent_state_id,
            "final_status": state.get("final_status", "PENDING"),
        }
        record.update(
            {
                "semantic_similarity": state.get("semantic_similarity", 0.0),
                "contradiction_score": state.get("contradiction_score", 0.0),
                "recursive_instability_score": state.get("recursive_instability_score", 0.0),
                "stabilization_delta": state.get("stabilization_delta", 0.0),
                "stabilization_reason": state.get("stabilization_reason", ""),
            }
        )
        path = self._state_path(record["lineage_id"])
        path.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")
        with self.index_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        return record

    def get_state(self, lineage_id: str) -> dict | None:
        path = self._state_path(lineage_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def all_states(self) -> list[dict]:
        if not self.states_dir.exists():
            return []
        states = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in self.states_dir.glob("*.json")
        ]
        return sorted(states, key=lambda item: item.get("timestamp", ""))

    def _state_path(self, lineage_id: str) -> Path:
        return self.states_dir / f"{lineage_id}.json"
