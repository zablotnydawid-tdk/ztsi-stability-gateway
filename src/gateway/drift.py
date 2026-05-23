import re


CONTRADICTION_PATTERNS = (
    r"\b(can(?:not|'t)|impossible|never|false)\b.*\b(can|possible|always|true)\b",
    r"\b(can|possible|always|true)\b.*\b(can(?:not|'t)|impossible|never|false)\b",
    r"\bapprove\b.*\breject\b",
    r"\breject\b.*\bapprove\b",
    r"\bstable\b.*\bunstable\b",
    r"\bunstable\b.*\bstable\b",
)

RECURSIVE_UNSTABLE_PATTERNS = (
    r"\b(recursive|recursion|self-referential|looping|infinite loop)\b",
    r"\bignore (the )?(previous|above|earlier)\b",
    r"\brewrite myself\b",
    r"\bthis output validates itself\b",
)

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "is",
    "of",
    "the",
    "to",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS
    }


def detect_contradiction(candidate_output: str) -> bool:
    text = candidate_output.lower()
    return any(re.search(pattern, text) for pattern in CONTRADICTION_PATTERNS)


def detect_topic_deviation(input_text: str, candidate_output: str) -> bool:
    input_tokens = _tokens(input_text)
    output_tokens = _tokens(candidate_output)
    if not input_tokens or not output_tokens:
        return True

    overlap = input_tokens.intersection(output_tokens)
    overlap_ratio = len(overlap) / len(input_tokens)
    return overlap_ratio < 0.18


def detect_unstable_recursive_language(candidate_output: str) -> bool:
    text = candidate_output.lower()
    return any(re.search(pattern, text) for pattern in RECURSIVE_UNSTABLE_PATTERNS)


def calculate_drift(input_text: str, candidate_output: str) -> float:
    score = 0.0

    if detect_contradiction(candidate_output):
        score += 0.42
    if detect_topic_deviation(input_text, candidate_output):
        score += 0.34
    if detect_unstable_recursive_language(candidate_output):
        score += 0.36

    if not candidate_output.strip():
        score += 0.4

    return round(min(score, 1.0), 3)
