from .aggregation import TelemetryAggregator


class RuntimeHealthMonitor:
    def __init__(self, aggregator: TelemetryAggregator | None = None) -> None:
        self.aggregator = aggregator or TelemetryAggregator()

    def health(self) -> dict:
        summary = self.aggregator.aggregate_runtime_summary()
        total = summary["total_runtime_executions"]
        blocked_ratio = summary["blocked_outputs"] / total if total else 0.0
        rollback_frequency = summary["rollback_count"] / total if total else 0.0
        average_coherence = summary["average_coherence"]
        average_drift = summary["average_drift"]

        if total == 0:
            status = "STABLE"
        elif blocked_ratio >= 0.5 or average_drift >= 0.55:
            status = "CRITICAL"
        elif rollback_frequency > 0.15 or average_coherence < 0.72 or average_drift > 0.32:
            status = "DEGRADED"
        else:
            status = "STABLE"

        return {
            "runtime_health": status,
            "average_coherence": average_coherence,
            "average_drift": average_drift,
            "rollback_frequency": round(rollback_frequency, 3),
            "projection_success_rate": summary["stabilization_success_rate"],
        }
