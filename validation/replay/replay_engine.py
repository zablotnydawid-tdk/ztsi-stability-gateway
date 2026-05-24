import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.memory.lineage_graph import LineageGraph
from src.policy.engine import PolicyEngine, RuntimeLockdownManager


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def replay_runtime_events(limit: int = 50) -> dict:
    events = read_jsonl(Path("runtime_logs") / "telemetry.jsonl")[-limit:]
    lockdown_manager = RuntimeLockdownManager(Path("runtime_logs") / "validation_replay_lockdown_state.json")
    lockdown_manager.release()
    policy = PolicyEngine(lockdown_manager=lockdown_manager)
    comparisons = []
    skipped = []
    for event in events:
        if event.get("event_type") == "rollback" or event.get("governance_status") == "ROLLBACK":
            skipped.append(event.get("lineage_id", ""))
            continue
        replayed = policy.evaluate(event)
        comparisons.append(
            {
                "lineage_id": event.get("lineage_id", ""),
                "recorded_governance": event.get("governance_status", "UNKNOWN"),
                "replayed_governance": replayed["governance_decision"],
                "recorded_severity": event.get("policy_severity", "INFO"),
                "replayed_severity": replayed["severity"],
                "matches": event.get("governance_status") == replayed["governance_decision"],
            }
        )
    return {
        "events_replayed": len(events),
        "policy_matches": sum(1 for item in comparisons if item["matches"]),
        "policy_mismatches": sum(1 for item in comparisons if not item["matches"]),
        "skipped_non_evaluation_events": skipped,
        "comparisons": comparisons,
    }


def verify_lineage_reconstruction(limit: int = 50) -> dict:
    events = read_jsonl(Path("runtime_logs") / "telemetry.jsonl")[-limit:]
    graph = LineageGraph()
    checks = []
    for event in events:
        lineage_id = event.get("lineage_id")
        if not lineage_id:
            continue
        path = graph.reconstruct_path(lineage_id)
        checks.append(
            {
                "lineage_id": lineage_id,
                "path_length": len(path),
                "reconstructable": bool(path),
            }
        )
    return {
        "lineages_checked": len(checks),
        "reconstructable": sum(1 for item in checks if item["reconstructable"]),
        "orphaned": sum(1 for item in checks if not item["reconstructable"]),
        "checks": checks,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "replay": replay_runtime_events(),
                "lineage_reconstruction": verify_lineage_reconstruction(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
