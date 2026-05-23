from .coherence import calculate_coherence
from .firewall import apply_firewall
from .governance import evaluate_governance
from .lineage import create_lineage_id, log_drift_metrics, log_state
from .state import SemanticState
from src.intelligence.scoring import DriftIntelligenceScorer


def process(input_text: str, candidate_output: str) -> dict:
    state = SemanticState(
        input_text=input_text,
        candidate_output=candidate_output,
        lineage_id=create_lineage_id(),
    )
    drift_metrics = DriftIntelligenceScorer().score(input_text, candidate_output)
    state.drift_score = drift_metrics["drift_score"]
    state.semantic_similarity = drift_metrics["semantic_similarity"]
    state.contradiction_score = drift_metrics["contradiction_score"]
    state.recursive_instability_score = drift_metrics["recursive_instability_score"]
    state.coherence_score = calculate_coherence(state.drift_score)
    state.governance_status = evaluate_governance(
        state.coherence_score,
        state.drift_score,
    )
    state.final_status = apply_firewall(state.governance_status)
    log_drift_metrics(
        {
            "lineage_id": state.lineage_id,
            "semantic_similarity": state.semantic_similarity,
            "contradiction_score": state.contradiction_score,
            "recursive_instability_score": state.recursive_instability_score,
            "drift_score": state.drift_score,
            "governance_status": state.governance_status,
        }
    )
    lineage_record = log_state(state)
    result = state.to_dict()
    result["firewall_status"] = state.final_status
    result["timestamp"] = lineage_record["timestamp"]
    return result
