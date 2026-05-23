# Architecture

The runtime pipeline is intentionally small:

```text
input_text + candidate_output
        |
        v
SemanticState
        |
        v
Drift Engine -> Coherence Engine -> Governance Engine -> Firewall
        |
        v
Lineage Logger
        |
        v
Certified Result Object
```

## API Runtime Layer

```text
CLIENT -> API -> RUNTIME -> GOVERNANCE -> FIREWALL -> RESPONSE
```

The FastAPI layer receives runtime stability evaluation requests at `/evaluate`, forwards them into the existing ZT&SI runtime, returns a certified response object, and logs API response events to `runtime_logs/api_events.jsonl`.

## Modules

- `state.py` defines `SemanticState`.
- `drift.py` detects contradiction, topic deviation, and unstable recursive language.
- `coherence.py` calculates coherence from drift.
- `governance.py` applies approval thresholds.
- `firewall.py` converts governance decisions into allowed or blocked final status.
- `lineage.py` creates lineage ids and writes JSONL audit records.
- `runtime.py` orchestrates the full gateway flow.
- `src/api/schemas.py` defines Pydantic request and response models.
- `src/api/routes.py` defines `/health` and `/evaluate`.
- `src/api/server.py` creates the FastAPI application, OpenAPI description, and timing middleware.
