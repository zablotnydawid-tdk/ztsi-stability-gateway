from .aggregation import TelemetryAggregator
from .events import build_runtime_event
from .health import RuntimeHealthMonitor
from .telemetry_store import TelemetryStore


class RuntimeTelemetryEngine:
    def __init__(
        self,
        store: TelemetryStore | None = None,
        aggregator: TelemetryAggregator | None = None,
    ) -> None:
        self.store = store or TelemetryStore()
        self.aggregator = aggregator or TelemetryAggregator(self.store)

    def emit_runtime_event(self, state: dict) -> dict:
        return self.store.append(build_runtime_event(state))

    def emit_rollback_event(self, rollback: dict) -> dict:
        event = {
            "timestamp": rollback.get("timestamp", ""),
            "event_type": "rollback",
            "lineage_id": rollback.get("restored_lineage_id") or rollback.get("requested_lineage_id", ""),
            "coherence_score": rollback.get("restored_coherence", 0.0),
            "drift_score": 0.0,
            "governance_status": "ROLLBACK",
            "firewall_status": "ROLLBACK",
            "final_status": "ROLLBACK",
            "stabilization_applied": False,
            "projection_recovered": False,
            "recursive_instability_score": 0.0,
            "contradiction_score": 0.0,
            "snapshot_created": False,
        }
        return self.store.append(event)

    def summary(self) -> dict:
        summary = self.aggregator.aggregate_runtime_summary()
        summary["runtime_health"] = RuntimeHealthMonitor(self.aggregator).health()["runtime_health"]
        return summary
