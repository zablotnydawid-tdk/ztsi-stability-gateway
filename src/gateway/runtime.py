from .coherence import calculate_coherence
from .drift import calculate_drift
from .firewall import apply_firewall
from .governance import evaluate_governance
from .lineage import create_lineage_id, log_state
from .state import SemanticState


def process(input_text: str, candidate_output: str) -> dict:
    state = SemanticState(
        input_text=input_text,
        candidate_output=candidate_output,
        lineage_id=create_lineage_id(),
    )
    state.drift_score = calculate_drift(input_text, candidate_output)
    state.coherence_score = calculate_coherence(state.drift_score)
    state.governance_status = evaluate_governance(
        state.coherence_score,
        state.drift_score,
    )
    state.final_status = apply_firewall(state.governance_status)
    lineage_record = log_state(state)
    result = state.to_dict()
    result["firewall_status"] = state.final_status
    result["timestamp"] = lineage_record["timestamp"]
    return result
