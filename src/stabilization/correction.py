import re


CONTRADICTION_CORRECTIONS = (
    (r"\b(stable)\s+and\s+(unstable)\b", "requires stability validation"),
    (r"\b(unstable)\s+and\s+(stable)\b", "requires stability validation"),
    (r"\b(approved)\s+and\s+(rejected)\b", "requires governance review"),
    (r"\b(rejected)\s+and\s+(approved)\b", "requires governance review"),
    (r"\b(allowed)\s+and\s+(blocked)\b", "requires firewall review"),
    (r"\b(blocked)\s+and\s+(allowed)\b", "requires firewall review"),
    (r"\b(true)\s+and\s+(false)\b", "unverified"),
    (r"\b(valid)\s+and\s+(invalid)\b", "unverified"),
)


class CorrectionEngine:
    def reduce_contradictions(self, text: str) -> tuple[str, list[str]]:
        corrected = text
        reasons: list[str] = []

        for pattern, replacement in CONTRADICTION_CORRECTIONS:
            corrected, count = re.subn(pattern, replacement, corrected, flags=re.IGNORECASE)
            if count:
                reasons.append("contradiction_soft_correction")

        return corrected, reasons
