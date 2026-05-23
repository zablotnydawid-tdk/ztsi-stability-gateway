from datetime import datetime, timezone


def build_runtime_event(state: dict) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lineage_id": state["lineage_id"],
        "coherence_score": state.get("coherence_score", 0.0),
        "drift_score": state.get("drift_score", 0.0),
        "governance_status": state.get("governance_status", "PENDING"),
        "firewall_status": state.get("firewall_status", state.get("final_status", "PENDING")),
        "final_status": state.get("final_status", "PENDING"),
        "stabilization_applied": state.get("stabilization_applied", False),
        "stabilization_delta": state.get("stabilization_delta", 0.0),
        "projection_recovered": (
            state.get("stabilization_applied", False)
            and state.get("governance_status") == "APPROVED"
            and state.get("firewall_status") == "ALLOWED"
        ),
        "recursive_instability_score": state.get("recursive_instability_score", 0.0),
        "contradiction_score": state.get("contradiction_score", 0.0),
        "snapshot_created": state.get("snapshot_created", False),
        "lineage_path_length": len(state.get("lineage_path", [])),
        "rollback_available": state.get("rollback_available", False),
        "policy_severity": state.get("policy_severity", "INFO"),
        "policy_violations": state.get("policy_violations", 0),
        "runtime_locked": state.get("runtime_locked", False),
    }
