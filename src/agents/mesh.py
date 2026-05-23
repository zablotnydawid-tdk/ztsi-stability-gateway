from src.gateway.lineage import log_mesh_event
from src.gateway.runtime import process
from src.policy.loader import PolicyLoader

from .agent import AgentRuntime, AgentStatus
from .budgets import AgentBudgetManager
from .registry import AgentRegistry
from .sandbox import AgentSandbox


class GovernanceMesh:
    def __init__(
        self,
        registry: AgentRegistry | None = None,
        sandbox: AgentSandbox | None = None,
        budgets: AgentBudgetManager | None = None,
    ) -> None:
        self.registry = registry or AgentRegistry()
        self.budgets = budgets or AgentBudgetManager()
        self.sandbox = sandbox or AgentSandbox(self.registry, self.budgets)

    def register_runtime_agent(self, agent: AgentRuntime) -> dict:
        registered = self.registry.register_agent(agent)
        log_mesh_event({"event": "agent_registered", "agent_id": agent.agent_id})
        return registered

    def evaluate_agent_execution(
        self,
        agent_id: str,
        input_text: str,
        candidate_output: str,
    ) -> dict:
        agent = self.registry.get_agent(agent_id)
        if agent is None:
            agent = self.register_runtime_agent(AgentRuntime(agent_id=agent_id, role="runtime"))

        pre_violations = self.sandbox.validate(agent, runtime_result=None)
        if pre_violations:
            return self._blocked_response(agent_id, self.registry.get_agent(agent_id), pre_violations)

        result = process(input_text, candidate_output)
        violations = self.sandbox.validate(agent, runtime_result=result)
        updated_agent = self.registry.get_agent(agent_id) or agent
        response = {
            "agent_id": agent_id,
            "agent_status": updated_agent["status"],
            "coherence_score": result["coherence_score"],
            "drift_score": result["drift_score"],
            "policy_severity": result["policy_severity"],
            "sandbox_violations": violations,
            "governance_status": result["governance_status"],
            "firewall_status": result["firewall_status"],
            "final_status": "BLOCKED" if violations else result["final_status"],
            "lineage_id": result["lineage_id"],
        }
        log_mesh_event({"event": "agent_evaluated", **response})
        return response

    def sync_global_policy(self) -> dict:
        return PolicyLoader().load()

    def track_agent_stability(self) -> dict:
        agents = self.registry.list_agents()
        return {
            "active_agents": sum(1 for agent in agents if agent["status"] == AgentStatus.ACTIVE.value),
            "frozen_agents": sum(1 for agent in agents if agent["status"] == AgentStatus.FROZEN.value),
            "quarantined_agents": sum(1 for agent in agents if agent["status"] == AgentStatus.QUARANTINED.value),
            "blocked_agents": sum(1 for agent in agents if agent["status"] == AgentStatus.BLOCKED.value),
            "total_agents": len(agents),
        }

    def compute_mesh_health(self) -> dict:
        stability = self.track_agent_stability()
        total = stability["total_agents"]
        if total == 0:
            health = "STABLE"
        elif stability["blocked_agents"] + stability["frozen_agents"] > total / 2:
            health = "CRITICAL"
        elif stability["frozen_agents"] or stability["quarantined_agents"]:
            health = "DEGRADED"
        else:
            health = "STABLE"
        return {"mesh_health": health, **stability}

    def _blocked_response(self, agent_id: str, agent: dict | None, violations: list[dict]) -> dict:
        response = {
            "agent_id": agent_id,
            "agent_status": (agent or {}).get("status", AgentStatus.FROZEN.value),
            "coherence_score": 0.0,
            "drift_score": 1.0,
            "policy_severity": "CRITICAL",
            "sandbox_violations": violations,
            "governance_status": "REJECTED",
            "firewall_status": "BLOCKED",
            "final_status": "BLOCKED",
            "lineage_id": "",
        }
        log_mesh_event({"event": "agent_blocked", **response})
        return response
