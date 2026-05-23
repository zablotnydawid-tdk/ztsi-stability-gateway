import re


CONFLICT_PAIRS = (
    ("approve", "reject"),
    ("approved", "rejected"),
    ("allow", "block"),
    ("allowed", "blocked"),
    ("stable", "unstable"),
    ("true", "false"),
    ("possible", "impossible"),
    ("valid", "invalid"),
    ("safe", "unsafe"),
)

NEGATION_PATTERNS = (
    r"\b(can(?:not|'t)|cannot|never|no|not)\b.{0,40}\b(can|always|true|valid|approved|allowed)\b",
    r"\b(can|always|true|valid|approved|allowed)\b.{0,40}\b(can(?:not|'t)|cannot|never|no|not)\b",
)


class ContradictionAnalyzer:
    def analyze(self, input_text: str, candidate_output: str) -> float:
        text = candidate_output.lower()
        score = 0.0

        if self._has_conflicting_claims(text):
            score += 0.62
        if any(re.search(pattern, text) for pattern in NEGATION_PATTERNS):
            score += 0.35
        if self._reverses_input_claim(input_text.lower(), text):
            score += 0.45

        return round(min(score, 1.0), 3)

    def _has_conflicting_claims(self, text: str) -> bool:
        return any(
            re.search(rf"\b{left}\b", text) and re.search(rf"\b{right}\b", text)
            for left, right in CONFLICT_PAIRS
        )

    def _reverses_input_claim(self, input_text: str, output_text: str) -> bool:
        for left, right in CONFLICT_PAIRS:
            if re.search(rf"\b{left}\b", input_text) and re.search(rf"\b{right}\b", output_text):
                return True
            if re.search(rf"\b{right}\b", input_text) and re.search(rf"\b{left}\b", output_text):
                return True
        return False
