from fastapi import APIRouter

from src.api.schemas import EvaluateRequest, EvaluateResponse, HealthResponse
from src.gateway.lineage import log_api_event
from src.gateway.runtime import process

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["runtime stability"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/evaluate", response_model=EvaluateResponse, tags=["runtime stability"])
def evaluate(request: EvaluateRequest) -> EvaluateResponse:
    result = process(
        input_text=request.input_text,
        candidate_output=request.candidate_output,
    )
    response = EvaluateResponse(
        coherence_score=result["coherence_score"],
        drift_score=result["drift_score"],
        governance_status=result["governance_status"],
        firewall_status=result["firewall_status"],
        lineage_id=result["lineage_id"],
        timestamp=result["timestamp"],
        final_status=result["final_status"],
    )
    log_api_event(
        {
            "route": "/evaluate",
            "lineage_id": response.lineage_id,
            "coherence_score": response.coherence_score,
            "drift_score": response.drift_score,
            "governance_status": response.governance_status,
            "firewall_status": response.firewall_status,
            "final_status": response.final_status,
        }
    )
    return response
