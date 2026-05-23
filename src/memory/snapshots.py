import json
from pathlib import Path

from .semantic_memory import RUNTIME_MEMORY_DIR


class SnapshotManager:
    def __init__(self, snapshot_dir: Path = RUNTIME_MEMORY_DIR / "snapshots") -> None:
        self.snapshot_dir = snapshot_dir

    def should_snapshot(self, state: dict) -> bool:
        return (
            state.get("governance_status") == "APPROVED"
            and state.get("firewall_status") == "ALLOWED"
            and state.get("coherence_score", 0.0) >= 0.82
        )

    def create_snapshot(self, state: dict) -> dict | None:
        if not self.should_snapshot(state):
            return None
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        snapshot = {
            "lineage_id": state["lineage_id"],
            "coherence_score": state["coherence_score"],
            "drift_score": state["drift_score"],
            "governance_status": state["governance_status"],
            "firewall_status": state["firewall_status"],
            "timestamp": state["timestamp"],
            "state": state,
        }
        self._snapshot_path(state["lineage_id"]).write_text(
            json.dumps(snapshot, sort_keys=True, indent=2),
            encoding="utf-8",
        )
        return snapshot

    def get_snapshot(self, lineage_id: str) -> dict | None:
        path = self._snapshot_path(lineage_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def snapshot_count(self) -> int:
        if not self.snapshot_dir.exists():
            return 0
        return len(list(self.snapshot_dir.glob("*.json")))

    def _snapshot_path(self, lineage_id: str) -> Path:
        return self.snapshot_dir / f"{lineage_id}.json"
