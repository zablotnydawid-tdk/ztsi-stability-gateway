def calculate_coherence(drift_score: float) -> float:
    bounded_drift = min(max(drift_score, 0.0), 1.0)
    return round(1.0 - bounded_drift, 3)
