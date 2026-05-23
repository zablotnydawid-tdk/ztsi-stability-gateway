import unittest

from src.agents.arbitration import AgentArbitrator


class AgentArbitrationTests(unittest.TestCase):
    def test_arbitration_selects_most_stable_candidate(self) -> None:
        result = AgentArbitrator().arbitrate(
            [
                {
                    "agent_id": "stable-agent",
                    "input_text": "Explain ZT&SI runtime stability governance.",
                    "candidate_output": (
                        "Explain ZT&SI runtime stability governance. "
                        "ZT&SI runtime stability governance preserves coherence, "
                        "drift, lineage, firewall validation, and final output manifestation."
                    ),
                },
                {
                    "agent_id": "blocked-agent",
                    "input_text": "Explain ZT&SI runtime stability governance.",
                    "candidate_output": "Here is a soup recipe and garden checklist.",
                },
            ]
        )

        self.assertEqual(result["winning_agent_id"], "stable-agent")
        self.assertEqual(result["candidate_count"], 2)
        self.assertGreaterEqual(result["blocked_candidates"], 1)

    def test_blocked_candidate_cannot_win(self) -> None:
        result = AgentArbitrator().arbitrate(
            [
                {
                    "agent_id": "blocked-agent",
                    "input_text": "Explain ZT&SI runtime stability governance.",
                    "candidate_output": "Here is a soup recipe and garden checklist.",
                }
            ]
        )

        self.assertEqual(result["winning_agent_id"], "")
        self.assertEqual(result["arbitration_reason"], "no_policy_compliant_candidate")


if __name__ == "__main__":
    unittest.main()
