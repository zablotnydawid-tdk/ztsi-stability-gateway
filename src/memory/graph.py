import json
from pathlib import Path

from .semantic_memory import RUNTIME_MEMORY_DIR


class DirectedSemanticGraph:
    def __init__(self, graph_path: Path = RUNTIME_MEMORY_DIR / "lineage_graph.json") -> None:
        self.graph_path = graph_path
        self.nodes: dict[str, dict] = {}
        self.edges: dict[str, list[str]] = {}
        self.parents: dict[str, str | None] = {}
        self._load()

    def add_node(self, lineage_id: str, metadata: dict | None = None) -> None:
        self.nodes[lineage_id] = metadata or {}
        self.edges.setdefault(lineage_id, [])
        self.parents.setdefault(lineage_id, None)
        self._save()

    def connect(self, parent_id: str, child_id: str) -> None:
        self.edges.setdefault(parent_id, [])
        if child_id not in self.edges[parent_id]:
            self.edges[parent_id].append(child_id)
        self.parents[child_id] = parent_id
        self.edges.setdefault(child_id, [])
        self._save()

    def children(self, lineage_id: str) -> list[str]:
        return list(self.edges.get(lineage_id, []))

    def parent(self, lineage_id: str) -> str | None:
        return self.parents.get(lineage_id)

    def _load(self) -> None:
        if not self.graph_path.exists():
            return
        data = json.loads(self.graph_path.read_text(encoding="utf-8"))
        self.nodes = data.get("nodes", {})
        self.edges = data.get("edges", {})
        self.parents = data.get("parents", {})

    def _save(self) -> None:
        self.graph_path.parent.mkdir(parents=True, exist_ok=True)
        self.graph_path.write_text(
            json.dumps(
                {
                    "nodes": self.nodes,
                    "edges": self.edges,
                    "parents": self.parents,
                },
                sort_keys=True,
                indent=2,
            ),
            encoding="utf-8",
        )
