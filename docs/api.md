# API

The runtime exposes both a Python function and a FastAPI REST API.

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
    "semantic_similarity": float,
    "contradiction_score": float,
    "recursive_instability_score": float,
    "stabilization_applied": bool,
    "stabilization_reason": str,
    "stabilization_delta": float,
    "governance_status": "APPROVED" | "REJECTED",
    "firewall_status": "ALLOWED" | "BLOCKED",
    "lineage_id": str,
    "timestamp": str,
    "final_status": "ALLOWED" | "BLOCKED",
}
```

## REST Runtime

Start the API server:

```bash
uvicorn src.api.server:app --reload
```

Swagger/OpenAPI is available at `/docs`, backed by the OpenAPI description:

```text
ZT&SI Stability Gateway — Cognitive Runtime Firewall
```

### GET /health

```json
{
  "status": "ok"
}
```

### POST /evaluate

Request:

```json
{
  "input_text": "Summarize ZT&SI gateway governance and coherence.",
  "candidate_output": "ZT&SI gateway governance uses coherence and drift checks."
}
```

Response:

```json
{
  "coherence_score": 1.0,
  "drift_score": 0.0,
  "semantic_similarity": 1.0,
  "contradiction_score": 0.0,
  "recursive_instability_score": 0.0,
  "stabilization_applied": false,
  "stabilization_reason": "not_required",
  "stabilization_delta": 0.0,
  "governance_status": "APPROVED",
  "firewall_status": "ALLOWED",
  "lineage_id": "ztsi-example",
  "timestamp": "2026-05-23T00:00:00+00:00",
  "final_status": "ALLOWED"
}
```

### POST /generate

Request:

```json
{
  "input_text": "Explain ZT&SI runtime stability governance.",
  "provider": "mock"
}
```

Response:

```json
{
  "input_text": "Explain ZT&SI runtime stability governance.",
  "candidate_output": "ZT&SI Stability Gateway response: ...",
  "coherence_score": 1.0,
  "drift_score": 0.0,
  "semantic_similarity": 1.0,
  "contradiction_score": 0.0,
  "recursive_instability_score": 0.0,
  "stabilization_applied": false,
  "stabilization_reason": "not_required",
  "stabilization_delta": 0.0,
  "governance_status": "APPROVED",
  "firewall_status": "ALLOWED",
  "lineage_id": "ztsi-example",
  "timestamp": "2026-05-23T00:00:00+00:00",
  "final_status": "ALLOWED"
}
```

Unknown providers return HTTP `400` with a clear error message. The default provider is `mock`.

## Governance Rule

Outputs are approved only when:

```text
coherence_score >= 0.82
drift_score <= 0.18
```

All other outputs are rejected and blocked by the firewall.
