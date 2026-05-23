from .coherence import calculate_coherence
from .firewall import apply_firewall
from .governance import evaluate_governance
from .lineage import (
    create_lineage_id,
    log_drift_metrics,
    log_memory_event,
    log_stabilization_event,
    log_state,
)
from .state import SemanticState
from src.intelligence.scoring import DriftIntelligenceScorer
from src.memory.lineage_graph import LineageGraph
from src.memory.semantic_memory import SemanticMemoryStore
from src.memory.snapshots import SnapshotManager
from src.stabilization.projection import ProjectionEngine
from src.telemetry.metrics import RuntimeTelemetryEngine


def process(
    input_text: str,
    candidate_output: str,
    parent_state_id: str | None = None,
) -> dict:
    scorer = DriftIntelligenceScorer()
    state = SemanticState(
        input_text=input_text,
        candidate_output=candidate_output,
        lineage_id=create_lineage_id(),
    )
    drift_metrics = scorer.score(input_text, candidate_output)
    original_drift = drift_metrics["drift_score"]
    original_coherence = calculate_coherence(original_drift)
    initial_governance = evaluate_governance(original_coherence, original_drift)

    if initial_governance == "REJECTED":
        projection = ProjectionEngine(scorer=scorer).stabilize(
            input_text,
            candidate_output,
            drift_metrics,
        )
        state.stabilization_applied = projection["stabilization_applied"]
        state.stabilization_reason = projection["stabilization_reason"]
        state.stabilization_delta = projection["stabilization_delta"]
        if state.stabilization_applied:
            state.candidate_output = projection["stabilized_output"]
            drift_metrics = projection["drift_profile"]
    else:
        state.stabilization_reason = "not_required"

    state.drift_score = drift_metrics["drift_score"]
    state.original_drift_score = original_drift
    state.stabilized_drift_score = state.drift_score
    state.semantic_similarity = drift_metrics["semantic_similarity"]
    state.contradiction_score = drift_metrics["contradiction_score"]
    state.recursive_instability_score = drift_metrics["recursive_instability_score"]
    state.coherence_score = calculate_coherence(state.drift_score)
    state.governance_status = evaluate_governance(
        state.coherence_score,
        state.drift_score,
    )
    state.final_status = apply_firewall(state.governance_status)
    if initial_governance == "REJECTED":
        coherence_improvement = round(state.coherence_score - original_coherence, 3)
        log_stabilization_event(
            {
                "lineage_id": state.lineage_id,
                "original_drift": original_drift,
                "stabilized_drift": state.drift_score,
                "stabilization_delta": state.stabilization_delta,
                "correction_strategy": state.stabilization_reason,
                "governance_status": state.governance_status,
                "projection_attempts": 1,
                "stabilization_success_rate": 1.0 if state.stabilization_applied else 0.0,
                "projection_recovery_rate": (
                    1.0 if state.stabilization_applied and state.governance_status == "APPROVED" else 0.0
                ),
                "post_projection_coherence_improvement": coherence_improvement,
            }
        )
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

    memory_store = SemanticMemoryStore()
    lineage_graph = LineageGraph()
    snapshot_manager = SnapshotManager()
    memory_record = memory_store.store_state(result, parent_state_id=parent_state_id)
    lineage_graph.add_state(memory_record)
    lineage_graph.connect_parent(state.lineage_id, parent_state_id)
    snapshot = snapshot_manager.create_snapshot(memory_record)
    ancestry = lineage_graph.get_ancestry(state.lineage_id)
    result["memory_persisted"] = True
    result["parent_state_id"] = parent_state_id
    result["lineage_ancestry"] = ancestry
    result["lineage_path"] = lineage_graph.reconstruct_path(state.lineage_id)
    result["snapshot_created"] = snapshot is not None
    result["rollback_available"] = snapshot is not None or bool(ancestry)
    log_memory_event(
        {
            "lineage_id": state.lineage_id,
            "parent_state_id": parent_state_id,
            "lineage_growth": len(result["lineage_path"]),
            "stable_snapshot_count": snapshot_manager.snapshot_count(),
            "unstable_state_frequency": 1 if state.governance_status != "APPROVED" else 0,
            "memory_persisted": True,
            "snapshot_created": result["snapshot_created"],
        }
    )
    RuntimeTelemetryEngine().emit_runtime_event(result)
    return result
