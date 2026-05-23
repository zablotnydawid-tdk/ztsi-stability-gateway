from src.dashboard.charts import bar, sparkline
from src.dashboard.summaries import governance_summary, runtime_summary, stabilization_summary
from src.telemetry.metrics import RuntimeTelemetryEngine


class RuntimeDashboard:
    def __init__(self, telemetry: RuntimeTelemetryEngine | None = None) -> None:
        self.telemetry = telemetry or RuntimeTelemetryEngine()

    def generate(self) -> dict:
        summary = self.telemetry.summary()
        return {
            "runtime_summary": runtime_summary(summary),
            "governance_summary": governance_summary(summary),
            "drift_summary": self._drift_summary(summary),
            "stabilization_summary": stabilization_summary(summary),
            "rollback_summary": f"Rollback count: {summary['rollback_count']}",
            "charts": self.render_charts(summary),
        }

    def render_charts(self, summary: dict | None = None) -> str:
        summary = summary or self.telemetry.summary()
        total = summary["total_runtime_executions"]
        approved = summary["approved_outputs"]
        blocked = summary["blocked_outputs"]
        stabilization_attempts = summary["stabilization_attempts"]
        recovered = int(round(stabilization_attempts * summary["stabilization_success_rate"]))
        return "\n".join(
            [
                f"Coherence trend: {sparkline(summary.get('coherence_trend', []))}",
                f"Drift trend:     {sparkline(summary.get('drift_trend', []))}",
                bar("Approved", approved, total),
                bar("Blocked", blocked, total),
                bar("Recovered", recovered, stabilization_attempts),
            ]
        )

    def _drift_summary(self, summary: dict) -> str:
        return (
            f"Average drift: {summary['average_drift']}\n"
            f"Recursive instability frequency: {summary['recursive_instability_frequency']}\n"
            f"Contradiction frequency: {summary['contradiction_frequency']}"
        )
