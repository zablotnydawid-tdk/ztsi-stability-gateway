from pydantic import BaseModel, Field


class EvaluateRequest(BaseModel):
    input_text: str = Field(..., min_length=1)
    candidate_output: str = Field(..., min_length=1)


class EvaluateResponse(BaseModel):
    coherence_score: float
    drift_score: float
    governance_status: str
    firewall_status: str
    lineage_id: str
    timestamp: str
    final_status: str


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
    governance_status: str
    firewall_status: str
    lineage_id: str
    timestamp: str
    final_status: str


class ErrorResponse(BaseModel):
    detail: str
