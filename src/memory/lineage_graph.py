from .graph import DirectedSemanticGraph


class LineageGraph:
    def __init__(self, graph: DirectedSemanticGraph | None = None) -> None:
        self.graph = graph or DirectedSemanticGraph()

    def add_state(self, state: dict) -> None:
        self.graph.add_node(
            state["lineage_id"],
            {
                "coherence_score": state.get("coherence_score", 0.0),
                "drift_score": state.get("drift_score", 0.0),
                "governance_status": state.get("governance_status", "PENDING"),
                "timestamp": state.get("timestamp", ""),
            },
        )

    def connect_parent(self, lineage_id: str, parent_state_id: str | None) -> None:
        if parent_state_id:
            self.graph.connect(parent_state_id, lineage_id)

    def reconstruct_path(self, lineage_id: str) -> list[str]:
        path = []
        current = lineage_id
        while current:
            path.append(current)
            current = self.graph.parent(current)
        return list(reversed(path))

    def get_ancestry(self, lineage_id: str) -> list[str]:
        path = self.reconstruct_path(lineage_id)
        return path[:-1]

    def get_descendants(self, lineage_id: str) -> list[str]:
        descendants: list[str] = []
        stack = list(self.graph.children(lineage_id))
        while stack:
            current = stack.pop()
            descendants.append(current)
            stack.extend(self.graph.children(current))
        return descendants
