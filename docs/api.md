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
    "policy_severity": str,
    "policy_violations": int,
    "runtime_status": str,
    "runtime_locked": bool,
    "governance_status": "APPROVED" | "REJECTED",
    "firewall_status": "ALLOWED" | "BLOCKED",
    "lineage_id": str,
    "timestamp": str,
    "final_status": "ALLOWED" | "BLOCKED",
    "memory_persisted": bool,
    "snapshot_created": bool,
    "rollback_available": bool,
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
  "policy_severity": "INFO",
  "policy_violations": 0,
  "runtime_status": "NORMAL",
  "runtime_locked": false,
  "governance_status": "APPROVED",
  "firewall_status": "ALLOWED",
  "lineage_id": "ztsi-example",
  "timestamp": "2026-05-23T00:00:00+00:00",
  "final_status": "ALLOWED",
  "memory_persisted": true,
  "snapshot_created": true,
  "rollback_available": true
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
  "policy_severity": "INFO",
  "policy_violations": 0,
  "runtime_status": "NORMAL",
  "runtime_locked": false,
  "governance_status": "APPROVED",
  "firewall_status": "ALLOWED",
  "lineage_id": "ztsi-example",
  "timestamp": "2026-05-23T00:00:00+00:00",
  "final_status": "ALLOWED",
  "memory_persisted": true,
  "snapshot_created": true,
  "rollback_available": true
}
```

Unknown providers return HTTP `400` with a clear error message. The default provider is `mock`.

### GET /memory/recent

Returns recent persisted cognition states.

### GET /memory/stable

Returns approved and allowed memory states.

### GET /memory/unstable

Returns rejected or blocked memory states.

### GET /memory/lineage/{lineage_id}

Returns a persisted state with ancestry, path, and descendants.

### POST /rollback/{lineage_id}

Response:

```json
{
  "rollback_performed": true,
  "restored_lineage_id": "ztsi-example",
  "restored_coherence": 0.9,
  "rollback_reason": "nearest_stable_snapshot_restored"
}
```

### GET /policy

Returns the active policy and rule registry.

### POST /policy/reload

Reloads policy configuration from `policy/default_policy.yaml`.

### GET /governance/status

```json
{
  "runtime_status": "NORMAL",
  "policy_loaded": true,
  "active_rules": 8,
  "recent_violations": 0,
  "lockdown_active": false
}
```

### GET /governance/violations

Returns recent policy violation log entries.

## Governance Rule

Outputs are approved only when:

```text
coherence_score >= 0.82
drift_score <= 0.18
```

All other outputs are rejected and blocked by the firewall.
