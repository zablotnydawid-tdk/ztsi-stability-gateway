from src.gateway.lineage import log_generate_event
from src.gateway.runtime import process
from src.llm.base import BaseLLMProvider
from src.llm.providers import get_provider


class LLMAdapter:
    def __init__(self, provider: BaseLLMProvider | None = None) -> None:
        self.provider = provider or get_provider("mock")

    @classmethod
    def from_provider_name(cls, provider_name: str = "mock") -> "LLMAdapter":
        return cls(provider=get_provider(provider_name))

    def generate(self, input_text: str, provider_name: str = "mock") -> dict:
        candidate_output = self.provider.generate(input_text)
        result = process(
            input_text=input_text,
            candidate_output=candidate_output,
        )
        log_generate_event(
            {
                "provider": provider_name,
                "input_text": input_text,
                "candidate_output": candidate_output,
                "lineage_id": result["lineage_id"],
                "coherence_score": result["coherence_score"],
                "drift_score": result["drift_score"],
                "semantic_similarity": result["semantic_similarity"],
                "contradiction_score": result["contradiction_score"],
                "recursive_instability_score": result["recursive_instability_score"],
                "stabilization_applied": result["stabilization_applied"],
                "stabilization_reason": result["stabilization_reason"],
                "stabilization_delta": result["stabilization_delta"],
                "policy_severity": result["policy_severity"],
                "policy_violations": result["policy_violations"],
                "runtime_status": result["runtime_status"],
                "runtime_locked": result["runtime_locked"],
                "memory_persisted": result["memory_persisted"],
                "snapshot_created": result["snapshot_created"],
                "rollback_available": result["rollback_available"],
                "governance_status": result["governance_status"],
                "firewall_status": result["firewall_status"],
                "final_status": result["final_status"],
            }
        )
        return result
