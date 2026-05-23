import math
import re
from collections import Counter
from collections.abc import Mapping


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "for",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "with",
}

CANONICAL_TERMS = {
    "approve": "governance",
    "approved": "governance",
    "block": "firewall",
    "blocked": "firewall",
    "candidate": "output",
    "checks": "validation",
    "coherent": "coherence",
    "gateway": "ztsi",
    "governance": "governance",
    "governed": "governance",
    "manifestation": "output",
    "manifest": "output",
    "response": "output",
    "runtime": "runtime",
    "semantic": "semantic",
    "stable": "stability",
    "stability": "stability",
    "validate": "validation",
    "validates": "validation",
    "validation": "validation",
    "ztsi": "ztsi",
}


class SemanticEmbeddingEngine:
    def __init__(self) -> None:
        self._sentence_model = None
        try:
            from sentence_transformers import SentenceTransformer

            self._sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            self._sentence_model = None

    def embed(self, text: str):
        if self._sentence_model is not None:
            return self._sentence_model.encode(text).tolist()
        return self._fallback_embed(text)

    def similarity(self, a, b) -> float:
        if isinstance(a, Mapping) and isinstance(b, Mapping):
            return round(self._mapping_cosine(a, b), 3)
        return round(self._vector_cosine(a, b), 3)

    def _fallback_embed(self, text: str) -> dict[str, float]:
        tokens = [self._normalize(token) for token in re.findall(r"[a-z0-9&]+", text.lower())]
        tokens = [token for token in tokens if token and token not in STOPWORDS]
        counts = Counter(tokens)
        for token in list(counts):
            canonical = CANONICAL_TERMS.get(token)
            if canonical and canonical != token:
                counts[canonical] += counts[token] * 0.65
        return dict(counts)

    def _normalize(self, token: str) -> str:
        token = token.replace("&", "")
        if token.endswith("ing") and len(token) > 5:
            return token[:-3]
        if token.endswith("ed") and len(token) > 4:
            return token[:-2]
        if token.endswith("s") and len(token) > 4:
            return token[:-1]
        return token

    def _mapping_cosine(self, a: Mapping[str, float], b: Mapping[str, float]) -> float:
        if not a or not b:
            return 0.0
        keys = set(a).union(b)
        dot = sum(float(a.get(key, 0.0)) * float(b.get(key, 0.0)) for key in keys)
        norm_a = math.sqrt(sum(float(value) ** 2 for value in a.values()))
        norm_b = math.sqrt(sum(float(value) ** 2 for value in b.values()))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return max(0.0, min(dot / (norm_a * norm_b), 1.0))

    def _vector_cosine(self, a, b) -> float:
        if not a or not b:
            return 0.0
        dot = sum(float(left) * float(right) for left, right in zip(a, b))
        norm_a = math.sqrt(sum(float(value) ** 2 for value in a))
        norm_b = math.sqrt(sum(float(value) ** 2 for value in b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return max(0.0, min(dot / (norm_a * norm_b), 1.0))
