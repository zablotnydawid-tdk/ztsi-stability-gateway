import re


class SemanticNormalizer:
    def normalize(self, text: str) -> tuple[str, list[str]]:
        reasons: list[str] = []
        normalized = re.sub(r"\s+", " ", text).strip()
        normalized = re.sub(r"([.!?]){2,}", r"\1", normalized)

        if normalized != text:
            reasons.append("semantic_normalization")

        return normalized, reasons
