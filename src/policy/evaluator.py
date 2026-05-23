from .scopes import PolicyScope
from .severity import Severity


class RuleEvaluator:
    def __init__(self, policy: dict) -> None:
        self.policy = policy

    def evaluate(self, state: dict, telemetry_summary: dict | None = None) -> list[dict]:
        telemetry_summary = telemetry_summary or {}
        violations: list[dict] = []
        violations.extend(self.evaluate_coherence(state))
        violations.extend(self.evaluate_drift(state))
        violations.extend(self.evaluate_contradiction(state))
        violations.extend(self.evaluate_instability(state))
        violations.extend(self.evaluate_stabilization_success(state))
        violations.extend(self.evaluate_rollback_frequency(telemetry_summary))
        return violations

    def evaluate_coherence(self, state: dict) -> list[dict]:
        if state.get("coherence_score", 0.0) < float(self.policy["minimum_coherence"]):
            return [self._violation("minimum_coherence", PolicyScope.COHERENCE, Severity.CRITICAL, state)]
        return []

    def evaluate_drift(self, state: dict) -> list[dict]:
        drift = state.get("drift_score", 0.0)
        if drift >= float(self.policy["critical_block_threshold"]):
            return [self._violation("critical_drift_escalation", PolicyScope.DRIFT, Severity.LOCKDOWN, state)]
        if drift > float(self.policy["maximum_drift"]):
            return [self._violation("maximum_drift", PolicyScope.DRIFT, Severity.CRITICAL, state)]
        return []

    def evaluate_contradiction(self, state: dict) -> list[dict]:
        if state.get("contradiction_score", 0.0) > float(self.policy["maximum_contradiction"]):
            return [self._violation("maximum_contradiction", PolicyScope.CONTRADICTION, Severity.CRITICAL, state)]
        return []

    def evaluate_instability(self, state: dict) -> list[dict]:
        instability = state.get("recursive_instability_score", 0.0)
        if instability >= float(self.policy["lockdown_recursive_instability"]):
            return [self._violation("recursive_instability_lockdown", PolicyScope.RECURSION, Severity.LOCKDOWN, state)]
        if instability > float(self.policy["maximum_recursive_instability"]):
            return [self._violation("maximum_recursive_instability", PolicyScope.RECURSION, Severity.CRITICAL, state)]
        return []

    def evaluate_stabilization_success(self, state: dict) -> list[dict]:
        if state.get("stabilization_applied") and state.get("drift_score", 0.0) <= float(self.policy["maximum_drift"]):
            return [self._violation("projection_recovery_applied", PolicyScope.STABILIZATION, Severity.INFO, state)]
        if state.get("stabilization_applied") and not self.policy["allow_projection_recovery"]:
            return [self._violation("projection_recovery_disallowed", PolicyScope.STABILIZATION, Severity.CRITICAL, state)]
        return []

    def evaluate_rollback_frequency(self, telemetry_summary: dict) -> list[dict]:
        total = telemetry_summary.get("total_runtime_executions", 0)
        if not total:
            return []
        rollback_frequency = telemetry_summary.get("rollback_count", 0) / total
        if rollback_frequency >= float(self.policy["rollback_storm_threshold"]):
            return [
                {
                    "rule": "rollback_storm_detection",
                    "scope": PolicyScope.ROLLBACK.value,
                    "severity": Severity.LOCKDOWN.value,
                    "observed": round(rollback_frequency, 3),
                    "threshold": self.policy["rollback_storm_threshold"],
                }
            ]
        if rollback_frequency >= float(self.policy["rollback_frequency_warning"]):
            return [
                {
                    "rule": "rollback_frequency_warning",
                    "scope": PolicyScope.ROLLBACK.value,
                    "severity": Severity.WARNING.value,
                    "observed": round(rollback_frequency, 3),
                    "threshold": self.policy["rollback_frequency_warning"],
                }
            ]
        return []

    def _violation(self, rule: str, scope: PolicyScope, severity: Severity, state: dict) -> dict:
        return {
            "rule": rule,
            "scope": scope.value,
            "severity": severity.value,
            "lineage_id": state.get("lineage_id", ""),
            "coherence_score": state.get("coherence_score", 0.0),
            "drift_score": state.get("drift_score", 0.0),
            "contradiction_score": state.get("contradiction_score", 0.0),
            "recursive_instability_score": state.get("recursive_instability_score", 0.0),
        }
