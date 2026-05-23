import tempfile
import unittest
from pathlib import Path

from src.agents.budgets import AgentBudgetManager


class AgentBudgetTests(unittest.TestCase):
    def test_agent_budget_tracks_execution_usage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manager = AgentBudgetManager(Path(directory) / "budgets.json")
            agent = {"agent_id": "agent-a"}

            budget = manager.record_execution(
                agent,
                drift_score=0.25,
                recursion_depth=2,
                blocked=True,
                stabilization_applied=True,
            )

            self.assertEqual(budget["current_drift_usage"], 0.25)
            self.assertEqual(budget["recursion_depth"], 2)
            self.assertEqual(budget["output_attempts"], 1)
            self.assertEqual(budget["blocked_attempts"], 1)
            self.assertEqual(budget["stabilization_attempts"], 1)


if __name__ == "__main__":
    unittest.main()
