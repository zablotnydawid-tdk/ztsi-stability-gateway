import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from src.agents.agent import AgentRuntime, AgentStatus
from src.agents.registry import AgentRegistry
from src.agents.mesh import GovernanceMesh
from src.api.server import app


class MeshHealthTests(unittest.TestCase):
    def test_mesh_health_degrades_with_frozen_agents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            registry = AgentRegistry(Path(directory) / "agents.json")
            mesh = GovernanceMesh(registry=registry)
            registry.register_agent(AgentRuntime(agent_id="active", role="writer"))
            registry.register_agent(AgentRuntime(agent_id="frozen", role="critic"))
            registry.update_status("frozen", AgentStatus.FROZEN.value)

            health = mesh.compute_mesh_health()

            self.assertEqual(health["mesh_health"], "DEGRADED")
            self.assertEqual(health["frozen_agents"], 1)

    def test_api_agent_evaluate_works(self) -> None:
        client = TestClient(app)
        client.post(
            "/agents/register",
            json={
                "agent_id": "api-agent",
                "role": "writer",
                "permissions": ["evaluate"],
                "recursion_quota": 3,
                "drift_budget": 10.0,
                "memory_scope": "local",
                "lineage_scope": "agent",
                "output_rights": True,
            },
        )

        response = client.post(
            "/agents/api-agent/evaluate",
            json={
                "agent_id": "api-agent",
                "input_text": "Explain ZT&SI runtime stability governance.",
                "candidate_output": (
                    "ZT&SI runtime stability governance preserves coherence, "
                    "drift, lineage, firewall validation, and final output manifestation."
                ),
            },
        )

        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["agent_id"], "api-agent")
        self.assertIn(body["agent_status"], {"ACTIVE", "FROZEN"})
        self.assertIn("sandbox_violations", body)


if __name__ == "__main__":
    unittest.main()
