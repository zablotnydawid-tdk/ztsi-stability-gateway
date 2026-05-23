import tempfile
import unittest
from pathlib import Path

from src.agents.agent import AgentRuntime
from src.agents.budgets import AgentBudgetManager
from src.agents.registry import AgentRegistry
from src.agents.sandbox import AgentSandbox


class AgentSandboxTests(unittest.TestCase):
    def test_agent_sandbox_blocks_permission_violation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = AgentRegistry(Path(directory) / "agents.json")
            budgets = AgentBudgetManager(Path(directory) / "budgets.json")
            sandbox = AgentSandbox(registry, budgets)
            agent = registry.register_agent(
                AgentRuntime(agent_id="agent-a", role="observer", permissions=[])
            )

            violations = sandbox.validate(agent, permission="evaluate")

            self.assertEqual(violations[0]["rule"], "permission_scope_violation")
            self.assertEqual(registry.get_agent("agent-a")["status"], "FROZEN")

    def test_drift_budget_violation_freezes_agent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = AgentRegistry(Path(directory) / "agents.json")
            budgets = AgentBudgetManager(Path(directory) / "budgets.json")
            sandbox = AgentSandbox(registry, budgets)
            agent = registry.register_agent(
                AgentRuntime(agent_id="agent-a", role="writer", drift_budget=0.1)
            )

            violations = sandbox.validate(agent, runtime_result={"drift_score": 0.2})

            self.assertIn("drift_budget_violation", {violation["rule"] for violation in violations})
            self.assertEqual(registry.get_agent("agent-a")["status"], "FROZEN")


if __name__ == "__main__":
    unittest.main()
