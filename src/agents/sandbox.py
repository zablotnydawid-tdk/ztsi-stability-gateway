from src.gateway.lineage import log_agent_event

from .agent import AgentStatus
from .budgets import AgentBudgetManager
from .permissions import has_permission
from .registry import AgentRegistry


class AgentSandbox:
    def __init__(
        self,
        registry: AgentRegistry | None = None,
        budgets: AgentBudgetManager | None = None,
    ) -> None:
        self.registry = registry or AgentRegistry()
        self.budgets = budgets or AgentBudgetManager()

    def validate(
        self,
        agent: dict,
        runtime_result: dict | None = None,
        permission: str = "evaluate",
        recursion_depth: int = 1,
    ) -> list[dict]:
        violations: list[dict] = []
        if agent.get("status") != AgentStatus.ACTIVE.value:
            violations.append({"rule": "agent_not_active", "severity": "CRITICAL"})
        if not has_permission(agent, permission):
            violations.append({"rule": "permission_scope_violation", "severity": "CRITICAL"})
        if not agent.get("output_rights", False):
            violations.append({"rule": "output_rights_violation", "severity": "CRITICAL"})
        if recursion_depth > int(agent.get("recursion_quota", 0)):
            violations.append({"rule": "recursion_quota_violation", "severity": "CRITICAL"})

        if runtime_result is not None:
            budget = self.budgets.record_execution(
                agent,
                runtime_result.get("drift_score", 0.0),
                recursion_depth=recursion_depth,
                blocked=runtime_result.get("final_status") == "BLOCKED",
                stabilization_applied=runtime_result.get("stabilization_applied", False),
            )
            if budget["current_drift_usage"] > float(agent.get("drift_budget", 0.0)):
                violations.append({"rule": "drift_budget_violation", "severity": "CRITICAL"})

        if violations:
            self.registry.update_status(agent["agent_id"], AgentStatus.FROZEN.value)
            log_agent_event(
                {
                    "agent_id": agent["agent_id"],
                    "event": "sandbox_violation",
                    "violations": violations,
                    "agent_status": AgentStatus.FROZEN.value,
                }
            )
        return violations
