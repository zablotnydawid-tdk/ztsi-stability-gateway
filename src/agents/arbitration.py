from src.gateway.lineage import log_arbitration_event
from src.gateway.runtime import process


class AgentArbitrator:
    def arbitrate(self, candidates: list[dict]) -> dict:
        evaluated = []
        for candidate in candidates:
            result = process(candidate["input_text"], candidate["candidate_output"])
            evaluated.append({"agent_id": candidate["agent_id"], "result": result})

        viable = [
            item
            for item in evaluated
            if item["result"]["final_status"] != "BLOCKED"
            and item["result"]["governance_status"] == "APPROVED"
        ]
        blocked_count = len(evaluated) - len(viable)
        if not viable:
            response = {
                "winning_agent_id": "",
                "winning_lineage_id": "",
                "arbitration_reason": "no_policy_compliant_candidate",
                "candidate_count": len(candidates),
                "blocked_candidates": blocked_count,
            }
            log_arbitration_event(response)
            return response

        winner = sorted(
            viable,
            key=lambda item: (
                item["result"]["coherence_score"],
                -item["result"]["drift_score"],
                item["result"]["snapshot_created"],
            ),
            reverse=True,
        )[0]
        response = {
            "winning_agent_id": winner["agent_id"],
            "winning_lineage_id": winner["result"]["lineage_id"],
            "arbitration_reason": "highest_coherence_lowest_drift_policy_compliant",
            "candidate_count": len(candidates),
            "blocked_candidates": blocked_count,
        }
        log_arbitration_event(response)
        return response
