import json
from pathlib import Path


REQUIRED_TELEMETRY_FIELDS = {
    "lineage_id",
    "coherence_score",
    "drift_score",
    "governance_status",
    "firewall_status",
    "final_status",
    "timestamp",
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_telemetry(limit: int = 200) -> dict:
    telemetry = read_jsonl(Path("runtime_logs") / "telemetry.jsonl")[-limit:]
    lineage_events = read_jsonl(Path("runtime_logs") / "lineage.jsonl")
    memory_events = read_jsonl(Path("runtime_logs") / "memory_events.jsonl")
    lineage_ids = {event.get("lineage_id") for event in lineage_events if event.get("lineage_id")}
    memory_ids = {event.get("lineage_id") for event in memory_events if event.get("lineage_id")}

    missing_fields = []
    orphan_lineages = []
    state_desync = []
    skipped_non_runtime_events = []
    for event in telemetry:
        if event.get("event_type") == "rollback" or event.get("governance_status") == "ROLLBACK":
            skipped_non_runtime_events.append(event.get("lineage_id", ""))
            continue
        missing = sorted(REQUIRED_TELEMETRY_FIELDS - set(event))
        if missing:
            missing_fields.append({"lineage_id": event.get("lineage_id", ""), "missing": missing})
        lineage_id = event.get("lineage_id")
        if lineage_id and lineage_id not in lineage_ids:
            orphan_lineages.append(lineage_id)
        if lineage_id and lineage_id not in memory_ids:
            state_desync.append(lineage_id)

    return {
        "telemetry_events_checked": len(telemetry),
        "missing_event_fields": missing_fields,
        "orphan_lineage_count": len(orphan_lineages),
        "orphan_lineages": orphan_lineages,
        "runtime_state_desync_count": len(state_desync),
        "runtime_state_desync": state_desync,
        "skipped_non_runtime_events": skipped_non_runtime_events,
        "passed": not missing_fields and not orphan_lineages and not state_desync,
    }


def main() -> None:
    print(json.dumps(validate_telemetry(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
