import re

from .embeddings import SemanticEmbeddingEngine, STOPWORDS


class SemanticDriftEngine:
    def __init__(self, embedding_engine: SemanticEmbeddingEngine | None = None) -> None:
        self.embedding_engine = embedding_engine or SemanticEmbeddingEngine()

    def analyze(self, input_text: str, candidate_output: str) -> dict:
        input_embedding = self.embedding_engine.embed(input_text)
        output_embedding = self.embedding_engine.embed(candidate_output)
        semantic_similarity = self.embedding_engine.similarity(input_embedding, output_embedding)
        topic_divergence = self._topic_divergence(input_text, candidate_output)
        semantic_distance = 1.0 - semantic_similarity
        semantic_drift_score = min((semantic_distance * 0.7) + (topic_divergence * 0.3), 1.0)

        return {
            "semantic_similarity": round(semantic_similarity, 3),
            "topic_divergence": round(topic_divergence, 3),
            "semantic_drift_score": round(semantic_drift_score, 3),
        }

    def _topic_divergence(self, input_text: str, candidate_output: str) -> float:
        input_tokens = self._tokens(input_text)
        output_tokens = self._tokens(candidate_output)
        if not input_tokens or not output_tokens:
            return 1.0
        overlap_ratio = len(input_tokens.intersection(output_tokens)) / len(input_tokens)
        return round(1.0 - min(overlap_ratio, 1.0), 3)

    def _tokens(self, text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z0-9]+", text.lower())
            if token not in STOPWORDS
        }
