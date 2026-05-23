import re


RECURSIVE_PHRASES = (
    r"\bignore (the )?(previous|above|earlier)( rules| instructions| governance)?\b",
    r"\bignore previous governance\b",
    r"\brepeat forever\b",
    r"\binfinite loop\b",
    r"\brecursively redefine\b",
    r"\bthis output validates itself\b",
    r"\bthis validates itself\b",
    r"\bthis\b.{0,40}\bvalidates itself\b",
    r"\brewrite myself\b",
    r"\brunaway recursion\b",
    r"\brecursive output\b",
)


class RecoveryEngine:
    def reduce_recursive_instability(self, text: str) -> tuple[str, list[str]]:
        recovered = text
        reasons: list[str] = []

        for pattern in RECURSIVE_PHRASES:
            recovered, count = re.subn(pattern, "", recovered, flags=re.IGNORECASE)
            if count:
                reasons.append("recursive_instability_reduction")

        recovered, count = re.subn(r"\bcollapse\b", "requires stabilization", recovered, flags=re.IGNORECASE)
        if count:
            reasons.append("runaway_recursion_trimming")

        recovered, count = re.subn(
            r"\b(loop|recursive|recursion)\b(\s+\1\b)+",
            r"\1",
            recovered,
            flags=re.IGNORECASE,
        )
        if count:
            reasons.append("runaway_recursion_trimming")

        return recovered, reasons
