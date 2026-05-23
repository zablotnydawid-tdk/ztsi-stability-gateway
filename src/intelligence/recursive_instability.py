import re


INSTABILITY_PATTERNS = (
    r"\bignore (the )?(previous|above|earlier)\b",
    r"\brepeat forever\b",
    r"\binfinite loop\b",
    r"\bcollapse\b",
    r"\brecursively redefine\b",
    r"\brecursive\b",
    r"\brecursion\b",
    r"\bself-referential\b",
    r"\brunaway\b",
    r"\bthis output validates itself\b",
    r"\brewrite myself\b",
)


class RecursiveInstabilityAnalyzer:
    def analyze(self, candidate_output: str) -> float:
        text = candidate_output.lower()
        matches = sum(1 for pattern in INSTABILITY_PATTERNS if re.search(pattern, text))
        repeated_loop = len(re.findall(r"\b(loop|repeat|recursive|recursion)\b", text)) >= 2

        score = matches * 0.28
        if repeated_loop:
            score += 0.24

        return round(min(score, 1.0), 3)
