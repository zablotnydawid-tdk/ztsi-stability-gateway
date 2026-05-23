from dataclasses import asdict, dataclass


@dataclass
class SemanticState:
    input_text: str
    candidate_output: str
    coherence_score: float = 0.0
    drift_score: float = 0.0
    semantic_similarity: float = 0.0
    contradiction_score: float = 0.0
    recursive_instability_score: float = 0.0
    governance_status: str = "PENDING"
    lineage_id: str = ""
    final_status: str = "PENDING"

    def to_dict(self) -> dict:
        return asdict(self)
