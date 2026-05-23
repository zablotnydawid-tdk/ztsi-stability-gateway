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
