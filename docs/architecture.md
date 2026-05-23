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

## Modules

- `state.py` defines `SemanticState`.
- `drift.py` detects contradiction, topic deviation, and unstable recursive language.
- `coherence.py` calculates coherence from drift.
- `governance.py` applies approval thresholds.
- `firewall.py` converts governance decisions into allowed or blocked final status.
- `lineage.py` creates lineage ids and writes JSONL audit records.
- `runtime.py` orchestrates the full gateway flow.
