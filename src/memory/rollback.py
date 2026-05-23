from src.gateway.lineage import log_rollback_event
from src.telemetry.metrics import RuntimeTelemetryEngine

from .lineage_graph import LineageGraph
from .semantic_memory import SemanticMemoryStore
from .snapshots import SnapshotManager


class RollbackEngine:
    def __init__(
        self,
        store: SemanticMemoryStore | None = None,
        graph: LineageGraph | None = None,
        snapshots: SnapshotManager | None = None,
    ) -> None:
        self.store = store or SemanticMemoryStore()
        self.graph = graph or LineageGraph()
        self.snapshots = snapshots or SnapshotManager()

    def rollback(self, lineage_id: str) -> dict:
        path = self.graph.reconstruct_path(lineage_id)
        if lineage_id not in path:
            path = [lineage_id]

        for candidate_id in reversed(path):
            snapshot = self.snapshots.get_snapshot(candidate_id)
            if snapshot:
                response = {
                    "rollback_performed": True,
                    "restored_lineage_id": candidate_id,
                    "restored_coherence": snapshot["coherence_score"],
                    "rollback_reason": "nearest_stable_snapshot_restored",
                }
                log_rollback_event(
                    {
                        **response,
                        "requested_lineage_id": lineage_id,
                        "rollback_count": 1,
                    }
                )
                RuntimeTelemetryEngine().emit_rollback_event(
                    {
                        **response,
                        "requested_lineage_id": lineage_id,
                    }
                )
                return response

        response = {
            "rollback_performed": False,
            "restored_lineage_id": "",
            "restored_coherence": 0.0,
            "rollback_reason": "no_stable_snapshot_available",
        }
        log_rollback_event(
            {
                **response,
                "requested_lineage_id": lineage_id,
                "rollback_count": 0,
            }
        )
        RuntimeTelemetryEngine().emit_rollback_event(
            {
                **response,
                "requested_lineage_id": lineage_id,
            }
        )
        return response
