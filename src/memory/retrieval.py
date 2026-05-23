from .semantic_memory import SemanticMemoryStore


class MemoryRetrievalEngine:
    def __init__(self, store: SemanticMemoryStore | None = None) -> None:
        self.store = store or SemanticMemoryStore()

    def retrieve_recent(self, limit: int = 10) -> list[dict]:
        return list(reversed(self.store.all_states()))[:limit]

    def retrieve_by_lineage(self, lineage_id: str) -> dict | None:
        return self.store.get_state(lineage_id)

    def retrieve_stable_states(self) -> list[dict]:
        return [
            state
            for state in self.store.all_states()
            if state.get("governance_status") == "APPROVED"
            and state.get("firewall_status") == "ALLOWED"
        ]

    def retrieve_unstable_states(self) -> list[dict]:
        return [
            state
            for state in self.store.all_states()
            if state.get("governance_status") != "APPROVED"
            or state.get("firewall_status") != "ALLOWED"
        ]
