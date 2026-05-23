import tempfile
import unittest
from pathlib import Path

from src.agents.agent import AgentRuntime, AgentStatus
from src.agents.registry import AgentRegistry


class AgentRegistryTests(unittest.TestCase):
    def test_agent_registration_works(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = AgentRegistry(Path(directory) / "agents.json")
            agent = registry.register_agent(AgentRuntime(agent_id="agent-a", role="critic"))

            self.assertEqual(agent["agent_id"], "agent-a")
            self.assertEqual(registry.get_agent("agent-a")["role"], "critic")
            self.assertEqual(len(registry.list_agents()), 1)

            registry.update_status("agent-a", AgentStatus.FROZEN.value)
            self.assertEqual(registry.get_agent("agent-a")["status"], "FROZEN")
            self.assertTrue(registry.remove_agent("agent-a"))


if __name__ == "__main__":
    unittest.main()
