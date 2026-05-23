from dataclasses import asdict, dataclass, field
from enum import Enum


class AgentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    QUARANTINED = "QUARANTINED"
    BLOCKED = "BLOCKED"


@dataclass
class AgentRuntime:
    agent_id: str
    role: str
    permissions: list[str] = field(default_factory=lambda: ["evaluate"])
    recursion_quota: int = 3
    drift_budget: float = 1.0
    memory_scope: str = "local"
    lineage_scope: str = "agent"
    output_rights: bool = True
    status: str = AgentStatus.ACTIVE.value

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AgentRuntime":
        return cls(**data)
