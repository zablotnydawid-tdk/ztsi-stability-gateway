def runtime_summary(summary: dict) -> str:
    return (
        f"Runtime executions: {summary['total_runtime_executions']}\n"
        f"Average coherence: {summary['average_coherence']}\n"
        f"Average drift: {summary['average_drift']}\n"
        f"Runtime health: {summary.get('runtime_health', 'UNKNOWN')}"
    )


def governance_summary(summary: dict) -> str:
    counts = summary.get("governance_counts", {})
    return "\n".join(f"{name}: {count}" for name, count in sorted(counts.items())) or "No governance data"


def stabilization_summary(summary: dict) -> str:
    return (
        f"Attempts: {summary['stabilization_attempts']}\n"
        f"Success rate: {summary['stabilization_success_rate']}"
    )
