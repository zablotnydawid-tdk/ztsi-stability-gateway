from .loader import PolicyLoader
from .rules import PolicyRule
from .scopes import PolicyScope
from .severity import Severity


class PolicyRegistry:
    def __init__(self, policy: dict | None = None) -> None:
        self.policy = policy or PolicyLoader().load()

    def active_rules(self) -> list[PolicyRule]:
        return [
            PolicyRule("minimum_coherence", PolicyScope.COHERENCE, Severity.CRITICAL, self.policy["minimum_coherence"], "Minimum allowed coherence."),
            PolicyRule("maximum_drift", PolicyScope.DRIFT, Severity.CRITICAL, self.policy["maximum_drift"], "Maximum allowed drift."),
            PolicyRule("maximum_contradiction", PolicyScope.CONTRADICTION, Severity.CRITICAL, self.policy["maximum_contradiction"], "Maximum contradiction score."),
            PolicyRule("maximum_recursive_instability", PolicyScope.RECURSION, Severity.CRITICAL, self.policy["maximum_recursive_instability"], "Maximum recursive instability."),
            PolicyRule("allow_projection_recovery", PolicyScope.STABILIZATION, Severity.INFO, self.policy["allow_projection_recovery"], "Projection recovery allowance."),
            PolicyRule("critical_block_threshold", PolicyScope.DRIFT, Severity.LOCKDOWN, self.policy["critical_block_threshold"], "Critical drift escalation."),
            PolicyRule("rollback_frequency_warning", PolicyScope.ROLLBACK, Severity.WARNING, self.policy["rollback_frequency_warning"], "Rollback warning frequency."),
            PolicyRule("rollback_storm_threshold", PolicyScope.ROLLBACK, Severity.LOCKDOWN, self.policy["rollback_storm_threshold"], "Rollback storm lockdown."),
        ]
