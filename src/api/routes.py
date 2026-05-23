from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    EvaluateRequest,
    EvaluateResponse,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
)
from src.gateway.lineage import log_api_event
from src.gateway.runtime import process
from src.llm.adapter import LLMAdapter
from src.llm.providers import UnknownProviderError

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
        semantic_similarity=result["semantic_similarity"],
        contradiction_score=result["contradiction_score"],
        recursive_instability_score=result["recursive_instability_score"],
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
            "semantic_similarity": response.semantic_similarity,
            "contradiction_score": response.contradiction_score,
            "recursive_instability_score": response.recursive_instability_score,
            "governance_status": response.governance_status,
            "firewall_status": response.firewall_status,
            "final_status": response.final_status,
        }
    )
    return response


@router.post(
    "/generate",
    response_model=GenerateResponse,
    tags=["llm adapter"],
)
def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        adapter = LLMAdapter.from_provider_name(request.provider)
    except UnknownProviderError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    result = adapter.generate(
        input_text=request.input_text,
        provider_name=request.provider,
    )
    response = GenerateResponse(
        input_text=result["input_text"],
        candidate_output=result["candidate_output"],
        coherence_score=result["coherence_score"],
        drift_score=result["drift_score"],
        semantic_similarity=result["semantic_similarity"],
        contradiction_score=result["contradiction_score"],
        recursive_instability_score=result["recursive_instability_score"],
        governance_status=result["governance_status"],
        firewall_status=result["firewall_status"],
        lineage_id=result["lineage_id"],
        timestamp=result["timestamp"],
        final_status=result["final_status"],
    )
    log_api_event(
        {
            "route": "/generate",
            "provider": request.provider,
            "lineage_id": response.lineage_id,
            "coherence_score": response.coherence_score,
            "drift_score": response.drift_score,
            "semantic_similarity": response.semantic_similarity,
            "contradiction_score": response.contradiction_score,
            "recursive_instability_score": response.recursive_instability_score,
            "governance_status": response.governance_status,
            "firewall_status": response.firewall_status,
            "final_status": response.final_status,
        }
    )
    return response
