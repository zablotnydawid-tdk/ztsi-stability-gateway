from collections import Counter, defaultdict
from datetime import datetime

from .telemetry_store import TelemetryStore


class TelemetryAggregator:
    def __init__(self, store: TelemetryStore | None = None) -> None:
        self.store = store or TelemetryStore()

    def aggregate_recent(self, limit: int = 50) -> dict:
        return self._aggregate(self.store.read_events()[-limit:])

    def aggregate_daily(self) -> dict:
        daily: dict[str, list[dict]] = defaultdict(list)
        for event in self.store.read_events():
            day = event.get("timestamp", "")[:10] or "unknown"
            daily[day].append(event)
        return {day: self._aggregate(events) for day, events in daily.items()}

    def aggregate_runtime_summary(self) -> dict:
        return self._aggregate(self.store.read_events())

    def _aggregate(self, events: list[dict]) -> dict:
        total = len(events)
        approved = sum(1 for event in events if event.get("governance_status") == "APPROVED")
        blocked = sum(1 for event in events if event.get("firewall_status") == "BLOCKED")
        stabilization_attempts = sum(1 for event in events if event.get("stabilization_applied"))
        stabilization_successes = sum(1 for event in events if event.get("projection_recovered"))
        rollback_count = sum(1 for event in events if event.get("event_type") == "rollback")
        coherence_total = sum(float(event.get("coherence_score", 0.0)) for event in events)
        drift_total = sum(float(event.get("drift_score", 0.0)) for event in events)
        recursive_count = sum(1 for event in events if float(event.get("recursive_instability_score", 0.0)) > 0)
        contradiction_count = sum(1 for event in events if float(event.get("contradiction_score", 0.0)) > 0)
        snapshot_count = sum(1 for event in events if event.get("snapshot_created"))
        lineage_graph_size = len({event.get("lineage_id") for event in events if event.get("lineage_id")})
        governance_counts = Counter(event.get("governance_status", "UNKNOWN") for event in events)
        severity_counts = Counter(event.get("policy_severity", "INFO") for event in events)
        lockdown_events = sum(1 for event in events if event.get("runtime_locked"))
        stabilization_counts = Counter(
            "RECOVERED" if event.get("projection_recovered") else "ATTEMPTED"
            for event in events
            if event.get("stabilization_applied")
        )

        return {
            "total_runtime_executions": total,
            "approved_outputs": approved,
            "blocked_outputs": blocked,
            "stabilization_attempts": stabilization_attempts,
            "stabilization_success_rate": round(stabilization_successes / stabilization_attempts, 3)
            if stabilization_attempts
            else 0.0,
            "rollback_count": rollback_count,
            "average_coherence": round(coherence_total / total, 3) if total else 0.0,
            "average_drift": round(drift_total / total, 3) if total else 0.0,
            "recursive_instability_frequency": round(recursive_count / total, 3) if total else 0.0,
            "contradiction_frequency": round(contradiction_count / total, 3) if total else 0.0,
            "snapshot_count": snapshot_count,
            "lineage_graph_size": lineage_graph_size,
            "governance_counts": dict(governance_counts),
            "severity_distribution": dict(severity_counts),
            "lockdown_events": lockdown_events,
            "stabilization_counts": dict(stabilization_counts),
            "coherence_trend": [event.get("coherence_score", 0.0) for event in events],
            "drift_trend": [event.get("drift_score", 0.0) for event in events],
        }
