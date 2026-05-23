import unittest

from fastapi.testclient import TestClient

from src.api.server import app


class GovernanceStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_governance_status_response_shape(self) -> None:
        response = self.client.get("/governance/status")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn(body["runtime_status"], {"NORMAL", "WARNING", "CRITICAL", "LOCKDOWN"})
        self.assertTrue(body["policy_loaded"])
        self.assertGreaterEqual(body["active_rules"], 1)
        self.assertIn("recent_violations", body)
        self.assertIn("lockdown_active", body)

    def test_policy_endpoint_returns_active_rules(self) -> None:
        response = self.client.get("/policy")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("policy", body)
        self.assertIn("active_rules", body)
        self.assertGreaterEqual(len(body["active_rules"]), 1)


if __name__ == "__main__":
    unittest.main()
