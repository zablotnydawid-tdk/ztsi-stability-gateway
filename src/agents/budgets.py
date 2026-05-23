import json
from pathlib import Path


BUDGETS_PATH = Path("runtime_memory") / "agent_budgets.json"


class AgentBudgetManager:
    def __init__(self, budgets_path: Path = BUDGETS_PATH) -> None:
        self.budgets_path = budgets_path

    def record_execution(
        self,
        agent: dict,
        drift_score: float,
        recursion_depth: int = 1,
        blocked: bool = False,
        stabilization_applied: bool = False,
    ) -> dict:
        budgets = self._load()
        current = budgets.setdefault(
            agent["agent_id"],
            {
                "current_drift_usage": 0.0,
                "recursion_depth": 0,
                "output_attempts": 0,
                "blocked_attempts": 0,
                "stabilization_attempts": 0,
            },
        )
        current["current_drift_usage"] = round(current["current_drift_usage"] + drift_score, 3)
        current["recursion_depth"] += recursion_depth
        current["output_attempts"] += 1
        current["blocked_attempts"] += 1 if blocked else 0
        current["stabilization_attempts"] += 1 if stabilization_applied else 0
        self._save(budgets)
        return current

    def get_budget(self, agent_id: str) -> dict:
        return self._load().get(
            agent_id,
            {
                "current_drift_usage": 0.0,
                "recursion_depth": 0,
                "output_attempts": 0,
                "blocked_attempts": 0,
                "stabilization_attempts": 0,
            },
        )

    def _load(self) -> dict:
        if not self.budgets_path.exists():
            return {}
        return json.loads(self.budgets_path.read_text(encoding="utf-8"))

    def _save(self, budgets: dict) -> None:
        self.budgets_path.parent.mkdir(parents=True, exist_ok=True)
        self.budgets_path.write_text(json.dumps(budgets, sort_keys=True, indent=2), encoding="utf-8")
