from src.intelligence.contradiction import ContradictionAnalyzer
from src.intelligence.recursive_instability import RecursiveInstabilityAnalyzer
from src.intelligence.scoring import DriftIntelligenceScorer
from src.intelligence.semantic_drift import SemanticDriftEngine


def detect_contradiction(candidate_output: str) -> bool:
    return ContradictionAnalyzer().analyze("", candidate_output) > 0.0


def detect_topic_deviation(input_text: str, candidate_output: str) -> bool:
    metrics = SemanticDriftEngine().analyze(input_text, candidate_output)
    return metrics["topic_divergence"] > 0.82


def detect_unstable_recursive_language(candidate_output: str) -> bool:
    return RecursiveInstabilityAnalyzer().analyze(candidate_output) > 0.0


def calculate_drift(input_text: str, candidate_output: str) -> float:
    return DriftIntelligenceScorer().score(input_text, candidate_output)["drift_score"]
