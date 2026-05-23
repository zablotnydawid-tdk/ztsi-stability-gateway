import json
from pathlib import Path

from .agent import AgentRuntime, AgentStatus


AGENTS_PATH = Path("runtime_memory") / "agents.json"


class AgentRegistry:
    def __init__(self, agents_path: Path = AGENTS_PATH) -> None:
        self.agents_path = agents_path

    def register_agent(self, agent: AgentRuntime) -> dict:
        agents = self._load()
        agents[agent.agent_id] = agent.to_dict()
        self._save(agents)
        return agents[agent.agent_id]

    def get_agent(self, agent_id: str) -> dict | None:
        return self._load().get(agent_id)

    def list_agents(self) -> list[dict]:
        return list(self._load().values())

    def update_status(self, agent_id: str, status: str) -> dict | None:
        agents = self._load()
        if agent_id not in agents:
            return None
        agents[agent_id]["status"] = status
        self._save(agents)
        return agents[agent_id]

    def remove_agent(self, agent_id: str) -> bool:
        agents = self._load()
        removed = agents.pop(agent_id, None) is not None
        self._save(agents)
        return removed

    def _load(self) -> dict[str, dict]:
        if not self.agents_path.exists():
            return {}
        return json.loads(self.agents_path.read_text(encoding="utf-8"))

    def _save(self, agents: dict[str, dict]) -> None:
        self.agents_path.parent.mkdir(parents=True, exist_ok=True)
        self.agents_path.write_text(json.dumps(agents, sort_keys=True, indent=2), encoding="utf-8")
