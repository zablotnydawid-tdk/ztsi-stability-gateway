APPROVED = "APPROVED"
REJECTED = "REJECTED"

from src.policy.loader import PolicyLoader


def evaluate_governance(coherence_score: float, drift_score: float) -> str:
    policy = PolicyLoader().load()
    if coherence_score >= float(policy["minimum_coherence"]) and drift_score <= float(policy["maximum_drift"]):
        return APPROVED
    return REJECTED
