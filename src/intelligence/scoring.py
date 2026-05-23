from .contradiction import ContradictionAnalyzer
from .recursive_instability import RecursiveInstabilityAnalyzer
from .semantic_drift import SemanticDriftEngine


class DriftIntelligenceScorer:
    def __init__(
        self,
        semantic_engine: SemanticDriftEngine | None = None,
        contradiction_analyzer: ContradictionAnalyzer | None = None,
        instability_analyzer: RecursiveInstabilityAnalyzer | None = None,
    ) -> None:
        self.semantic_engine = semantic_engine or SemanticDriftEngine()
        self.contradiction_analyzer = contradiction_analyzer or ContradictionAnalyzer()
        self.instability_analyzer = instability_analyzer or RecursiveInstabilityAnalyzer()

    def score(self, input_text: str, candidate_output: str) -> dict:
        semantic = self.semantic_engine.analyze(input_text, candidate_output)
        contradiction_score = self.contradiction_analyzer.analyze(input_text, candidate_output)
        recursive_instability_score = self.instability_analyzer.analyze(candidate_output)

        final_drift_score = (
            semantic["semantic_drift_score"] * 0.45
            + contradiction_score * 0.35
            + recursive_instability_score * 0.20
        )

        return {
            "semantic_similarity": semantic["semantic_similarity"],
            "semantic_drift_score": semantic["semantic_drift_score"],
            "topic_divergence": semantic["topic_divergence"],
            "contradiction_score": round(contradiction_score, 3),
            "recursive_instability_score": round(recursive_instability_score, 3),
            "drift_score": round(min(max(final_drift_score, 0.0), 1.0), 3),
        }
