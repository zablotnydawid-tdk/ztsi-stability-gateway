from pydantic import BaseModel, Field


class EvaluateRequest(BaseModel):
    input_text: str = Field(..., min_length=1)
    candidate_output: str = Field(..., min_length=1)


class EvaluateResponse(BaseModel):
    coherence_score: float
    drift_score: float
    semantic_similarity: float
    contradiction_score: float
    recursive_instability_score: float
    stabilization_applied: bool
    stabilization_reason: str
    stabilization_delta: float
    policy_severity: str
    policy_violations: int
    runtime_status: str
    runtime_locked: bool
    governance_status: str
    firewall_status: str
    lineage_id: str
    timestamp: str
    final_status: str
    memory_persisted: bool
    snapshot_created: bool
    rollback_available: bool


class HealthResponse(BaseModel):
    status: str


class GenerateRequest(BaseModel):
    input_text: str = Field(..., min_length=1)
    provider: str = "mock"


class GenerateResponse(BaseModel):
    input_text: str
    candidate_output: str
    coherence_score: float
    drift_score: float
    semantic_similarity: float
    contradiction_score: float
    recursive_instability_score: float
    stabilization_applied: bool
    stabilization_reason: str
    stabilization_delta: float
    policy_severity: str
    policy_violations: int
    runtime_status: str
    runtime_locked: bool
    governance_status: str
    firewall_status: str
    lineage_id: str
    timestamp: str
    final_status: str
    memory_persisted: bool
    snapshot_created: bool
    rollback_available: bool


class ErrorResponse(BaseModel):
    detail: str


class RollbackResponse(BaseModel):
    rollback_performed: bool
    restored_lineage_id: str
    restored_coherence: float
    rollback_reason: str


class AgentRegisterRequest(BaseModel):
    agent_id: str
    role: str = "runtime"
    permissions: list[str] = ["evaluate"]
    recursion_quota: int = 3
    drift_budget: float = 1.0
    memory_scope: str = "local"
    lineage_scope: str = "agent"
    output_rights: bool = True


class AgentEvaluateRequest(BaseModel):
    agent_id: str
    input_text: str
    candidate_output: str


class AgentEvaluateResponse(BaseModel):
    agent_id: str
    agent_status: str
    coherence_score: float
    drift_score: float
    policy_severity: str
    sandbox_violations: list
    governance_status: str
    firewall_status: str
    final_status: str


class ArbitrationCandidate(BaseModel):
    agent_id: str
    input_text: str
    candidate_output: str


class ArbitrationRequest(BaseModel):
    candidates: list[ArbitrationCandidate]


class ArbitrationResponse(BaseModel):
    winning_agent_id: str
    winning_lineage_id: str
    arbitration_reason: str
    candidate_count: int
    blocked_candidates: int
