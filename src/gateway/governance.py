APPROVED = "APPROVED"
REJECTED = "REJECTED"


def evaluate_governance(coherence_score: float, drift_score: float) -> str:
    if coherence_score >= 0.82 and drift_score <= 0.18:
        return APPROVED
    return REJECTED
