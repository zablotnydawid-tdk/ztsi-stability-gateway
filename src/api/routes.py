from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    EvaluateRequest,
    EvaluateResponse,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    RollbackResponse,
)
from src.gateway.lineage import log_api_event
from src.gateway.runtime import process
from src.llm.adapter import LLMAdapter
from src.llm.providers import UnknownProviderError
from src.memory.lineage_graph import LineageGraph
from src.memory.retrieval import MemoryRetrievalEngine
from src.memory.rollback import RollbackEngine

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
        stabilization_applied=result["stabilization_applied"],
        stabilization_reason=result["stabilization_reason"],
        stabilization_delta=result["stabilization_delta"],
        governance_status=result["governance_status"],
        firewall_status=result["firewall_status"],
        lineage_id=result["lineage_id"],
        timestamp=result["timestamp"],
        final_status=result["final_status"],
        memory_persisted=result["memory_persisted"],
        snapshot_created=result["snapshot_created"],
        rollback_available=result["rollback_available"],
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
            "stabilization_applied": response.stabilization_applied,
            "stabilization_delta": response.stabilization_delta,
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
        stabilization_applied=result["stabilization_applied"],
        stabilization_reason=result["stabilization_reason"],
        stabilization_delta=result["stabilization_delta"],
        governance_status=result["governance_status"],
        firewall_status=result["firewall_status"],
        lineage_id=result["lineage_id"],
        timestamp=result["timestamp"],
        final_status=result["final_status"],
        memory_persisted=result["memory_persisted"],
        snapshot_created=result["snapshot_created"],
        rollback_available=result["rollback_available"],
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
            "stabilization_applied": response.stabilization_applied,
            "stabilization_delta": response.stabilization_delta,
            "governance_status": response.governance_status,
            "firewall_status": response.firewall_status,
            "final_status": response.final_status,
        }
    )
    return response


@router.get("/memory/recent", tags=["recursive memory"])
def memory_recent(limit: int = 10) -> list[dict]:
    return MemoryRetrievalEngine().retrieve_recent(limit=limit)


@router.get("/memory/stable", tags=["recursive memory"])
def memory_stable() -> list[dict]:
    return MemoryRetrievalEngine().retrieve_stable_states()


@router.get("/memory/unstable", tags=["recursive memory"])
def memory_unstable() -> list[dict]:
    return MemoryRetrievalEngine().retrieve_unstable_states()


@router.get("/memory/lineage/{lineage_id}", tags=["recursive memory"])
def memory_lineage(lineage_id: str) -> dict:
    state = MemoryRetrievalEngine().retrieve_by_lineage(lineage_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Lineage state not found.")
    graph = LineageGraph()
    return {
        "state": state,
        "ancestry": graph.get_ancestry(lineage_id),
        "path": graph.reconstruct_path(lineage_id),
        "descendants": graph.get_descendants(lineage_id),
    }


@router.post(
    "/rollback/{lineage_id}",
    response_model=RollbackResponse,
    tags=["recursive memory"],
)
def rollback(lineage_id: str) -> RollbackResponse:
    result = RollbackEngine().rollback(lineage_id)
    return RollbackResponse(**result)
