# API

The current MVP exposes a Python runtime function.

```python
from src.gateway.runtime import process

result = process(
    input_text="Summarize gateway governance.",
    candidate_output="Gateway governance validates drift and coherence.",
)
```

## Result Object

```python
{
    "input_text": str,
    "candidate_output": str,
    "coherence_score": float,
    "drift_score": float,
    "governance_status": "APPROVED" | "REJECTED",
    "lineage_id": str,
    "final_status": "ALLOWED" | "BLOCKED",
}
```

## Governance Rule

Outputs are approved only when:

```text
coherence_score >= 0.82
drift_score <= 0.18
```

All other outputs are rejected and blocked by the firewall.
