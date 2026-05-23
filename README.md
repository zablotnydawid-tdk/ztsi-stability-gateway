# ZT&SI Stability Gateway

ZT&SI Stability Gateway is a minimal AI Runtime Firewall / Cognitive Stability Gateway. It sits between a user request, a candidate LLM output, and final manifestation. The MVP does not call an external model yet; it simulates validation for supplied input and output text.

## Why It Exists

Generative systems can drift away from the user intent, contradict themselves, or produce unstable recursive language. This gateway provides a small control plane for detecting semantic drift, calculating coherence, enforcing governance rules, logging lineage, and blocking unstable outputs before they are manifested.

## Architecture Flow

1. User input and candidate output enter the runtime.
2. The drift engine checks contradiction, topic deviation, and unstable recursive language.
3. The coherence engine derives a coherence score from drift.
4. The governance engine approves only outputs with coherence `>= 0.82` and drift `<= 0.18`.
5. The firewall allows approved outputs and blocks rejected outputs.
6. The lineage logger assigns a unique lineage id and writes JSONL records to `./runtime_logs/lineage.jsonl`.
7. The runtime returns a certified result object.

## Run Tests

```bash
python -m unittest discover -s tests
```

## Run Demo

```bash
python -m src.main
```

The demo prints one stable output that is approved and one unstable output that is blocked, including coherence score, drift score, lineage id, governance status, and final gateway decision.

## Next Engineering Steps

- Replace heuristic drift checks with model-assisted semantic evaluation.
- Add signed lineage records and tamper-evident audit chains.
- Introduce policy packs for domain-specific governance.
- Add HTTP API endpoints for gateway validation.
- Add structured result schemas for downstream runtime integrations.
- Add persistent storage adapters beyond local JSONL.
