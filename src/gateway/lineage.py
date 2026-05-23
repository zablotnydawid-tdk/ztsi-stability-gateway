import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .state import SemanticState


DEFAULT_LOG_PATH = Path("runtime_logs") / "lineage.jsonl"
API_EVENTS_LOG_PATH = Path("runtime_logs") / "api_events.jsonl"
GENERATE_EVENTS_LOG_PATH = Path("runtime_logs") / "generate_events.jsonl"
DRIFT_METRICS_LOG_PATH = Path("runtime_logs") / "drift_metrics.jsonl"
STABILIZATION_EVENTS_LOG_PATH = Path("runtime_logs") / "stabilization_events.jsonl"


def create_lineage_id() -> str:
    return f"ztsi-{uuid.uuid4().hex}"


def log_state(state: SemanticState, log_path: Path = DEFAULT_LOG_PATH) -> dict:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **state.to_dict(),
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def log_api_event(event: dict, log_path: Path = API_EVENTS_LOG_PATH) -> dict:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def log_generate_event(
    event: dict,
    log_path: Path = GENERATE_EVENTS_LOG_PATH,
) -> dict:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def log_drift_metrics(
    metrics: dict,
    log_path: Path = DRIFT_METRICS_LOG_PATH,
) -> dict:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **metrics,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def log_stabilization_event(
    event: dict,
    log_path: Path = STABILIZATION_EVENTS_LOG_PATH,
) -> dict:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record
