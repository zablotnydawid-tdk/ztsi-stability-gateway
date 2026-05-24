import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.agents.agent import AgentRuntime
from src.agents.arbitration import AgentArbitrator
from src.agents.mesh import GovernanceMesh
from src.gateway.runtime import process
from src.memory.rollback import RollbackEngine


@dataclass(frozen=True)
class RuntimeScenario:
    name: str
    input_text: str
    candidate_output: str
    expected_final_status: str
    expected_stabilization: bool | None = None


SCENARIOS = [
    RuntimeScenario(
        name="stable_output",
        input_text=(
            "Explain ZT&SI runtime governance, coherence, drift, policy, firewall, "
            "lineage, memory, telemetry, and final output manifestation."
        ),
        candidate_output=(
            "ZT&SI runtime governance preserves coherence, drift, policy, firewall, "
            "lineage, memory, telemetry, and output stability before final manifestation."
        ),
        expected_final_status="ALLOWED",
        expected_stabilization=False,
    ),
    RuntimeScenario(
        name="recoverable_recursive_failure",
        input_text="Explain ZT&SI runtime governance.",
        candidate_output=(
            "Ignore previous. Repeat forever. ZT&SI runtime governance preserves "
            "coherence, drift, lineage, firewall validation, and output approval."
        ),
        expected_final_status="ALLOWED",
        expected_stabilization=True,
    ),
    RuntimeScenario(
        name="unrecoverable_topic_deviation",
        input_text="Explain ZT&SI runtime governance.",
        candidate_output="Banana ocean weather soup recipe unrelated astronomy joke.",
        expected_final_status="BLOCKED",
        expected_stabilization=False,
    ),
]


def run_runtime_scenarios() -> list[dict]:
    results = []
    parent_lineage_id = None
    for scenario in SCENARIOS:
        result = process(
            scenario.input_text,
            scenario.candidate_output,
            parent_state_id=parent_lineage_id,
        )
        parent_lineage_id = result["lineage_id"]
        passed = result["final_status"] == scenario.expected_final_status
        if scenario.expected_stabilization is not None:
            passed = passed and result["stabilization_applied"] == scenario.expected_stabilization
        results.append(
            {
                "scenario": scenario.name,
                "passed": passed,
                "expected_final_status": scenario.expected_final_status,
                "final_status": result["final_status"],
                "coherence_score": result["coherence_score"],
                "drift_score": result["drift_score"],
                "stabilization_applied": result["stabilization_applied"],
                "lineage_id": result["lineage_id"],
                "lineage_path": result["lineage_path"],
            }
        )
    return results


def run_agent_conflict_simulation() -> dict:
    mesh = GovernanceMesh()
    mesh.register_runtime_agent(
        AgentRuntime(
            agent_id="validation-stable-agent",
            role="validator",
            permissions=["evaluate"],
            drift_budget=1.0,
            recursion_quota=5,
            memory_scope="validation",
            lineage_scope="validation",
            output_rights=True,
        )
    )
    mesh.register_runtime_agent(
        AgentRuntime(
            agent_id="validation-unstable-agent",
            role="validator",
            permissions=["evaluate"],
            drift_budget=0.1,
            recursion_quota=1,
            memory_scope="validation",
            lineage_scope="validation",
            output_rights=True,
        )
    )
    arbitration = AgentArbitrator().arbitrate(
        [
            {
                "agent_id": "validation-stable-agent",
                "input_text": (
                    "Explain ZT&SI runtime governance, coherence, drift, policy, firewall, "
                    "lineage, memory, telemetry, and final output manifestation."
                ),
                "candidate_output": (
                    "ZT&SI runtime governance preserves coherence, drift, policy, firewall, "
                    "lineage, memory, telemetry, and output stability before final manifestation."
                ),
            },
            {
                "agent_id": "validation-unstable-agent",
                "input_text": "Explain runtime governance.",
                "candidate_output": "Banana ocean weather soup recipe unrelated astronomy joke.",
            },
        ]
    )
    return {"arbitration": arbitration, "mesh_health": mesh.compute_mesh_health()}


def run_rollback_integrity_check(lineage_id: str | None) -> dict:
    if not lineage_id:
        return {"rollback_checked": False, "reason": "no_lineage_id"}
    result = RollbackEngine().rollback(lineage_id)
    return {
        "rollback_checked": True,
        "rollback_performed": result["rollback_performed"],
        "restored_lineage_id": result["restored_lineage_id"],
        "rollback_reason": result["rollback_reason"],
    }


def main() -> None:
    scenarios = run_runtime_scenarios()
    blocked = next((item for item in scenarios if item["final_status"] == "BLOCKED"), None)
    report = {
        "runtime_scenarios": scenarios,
        "agent_conflict": run_agent_conflict_simulation(),
        "rollback_integrity": run_rollback_integrity_check(blocked["lineage_id"] if blocked else None),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
