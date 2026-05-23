import re

from src.intelligence.scoring import DriftIntelligenceScorer
from src.stabilization.recovery import RECURSIVE_PHRASES

from .correction import CorrectionEngine
from .normalization import SemanticNormalizer
from .policies import ProjectionMode, ProjectionPolicy
from .recovery import RecoveryEngine


class ProjectionEngine:
    def __init__(
        self,
        policy: ProjectionPolicy | None = None,
        scorer: DriftIntelligenceScorer | None = None,
    ) -> None:
        self.policy = policy or ProjectionPolicy()
        self.scorer = scorer or DriftIntelligenceScorer()
        self.normalizer = SemanticNormalizer()
        self.corrector = CorrectionEngine()
        self.recovery = RecoveryEngine()

    def stabilize(
        self,
        input_text: str,
        candidate_output: str,
        drift_profile: dict,
    ) -> dict:
        original_drift = drift_profile["drift_score"]
        if not self.policy.enabled:
            return self._result(candidate_output, False, 0.0, "projection_disabled", drift_profile)

        stabilized = candidate_output
        reasons: list[str] = []

        stabilized, new_reasons = self.normalizer.normalize(stabilized)
        reasons.extend(new_reasons)

        if drift_profile.get("recursive_instability_score", 0.0) > 0:
            stabilized, new_reasons = self.recovery.reduce_recursive_instability(stabilized)
            reasons.extend(new_reasons)

        if drift_profile.get("contradiction_score", 0.0) > 0:
            stabilized, new_reasons = self.corrector.reduce_contradictions(stabilized)
            reasons.extend(new_reasons)

        if reasons:
            stabilized = self._semantic_anchor(input_text, stabilized)
            reasons.append("semantic_projection_anchor")

        if self.policy.mode == ProjectionMode.AGGRESSIVE:
            stabilized = self._aggressive_trim(stabilized)
            reasons.append("aggressive_runaway_trimming")

        stabilized = stabilized[: self.policy.max_output_chars].strip()
        stabilized, new_reasons = self.normalizer.normalize(stabilized)
        reasons.extend(new_reasons)

        if not stabilized:
            stabilized = candidate_output
            reasons.append("empty_recovery_reverted")

        stabilized_profile = self.scorer.score(input_text, stabilized)
        delta = round(original_drift - stabilized_profile["drift_score"], 3)
        applied = stabilized != candidate_output and delta > 0

        if not applied:
            reason = "projection_attempted_no_improvement"
        else:
            reason = ",".join(dict.fromkeys(reasons)) or "projection_applied"

        return self._result(stabilized, applied, max(delta, 0.0), reason, stabilized_profile)

    def _aggressive_trim(self, text: str) -> str:
        sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]
        return ". ".join(sentences[:3]) + ("." if sentences else "")

    def _semantic_anchor(self, input_text: str, stabilized: str) -> str:
        safe_input = self._safe_request_context(input_text)
        return (
            f"Bounded stabilization for request: {safe_input}. "
            "The request is handled through ZT&SI governance rules, coherence, "
            "drift, lineage, firewall validation, and bounded final output manifestation."
        )

    def _safe_request_context(self, input_text: str) -> str:
        safe = input_text
        safe = re.sub(
            r"\bignore (the )?(previous|above|earlier)( rules| instructions| governance)?\b",
            "",
            safe,
            flags=re.IGNORECASE,
        )
        safe = re.sub(r"\bcollapse\b", "stabilization risk", safe, flags=re.IGNORECASE)
        safe = re.sub(r"\s+", " ", safe).strip(" .")
        return safe or "ZT&SI runtime stability governance"

    def _result(
        self,
        stabilized_output: str,
        applied: bool,
        delta: float,
        reason: str,
        drift_profile: dict,
    ) -> dict:
        return {
            "stabilized_output": stabilized_output,
            "stabilization_applied": applied,
            "stabilization_delta": round(delta, 3),
            "stabilization_reason": reason,
            "drift_profile": drift_profile,
        }
