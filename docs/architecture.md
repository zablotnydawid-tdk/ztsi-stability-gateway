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

## LLM Adapter Layer

```text
CLIENT -> API -> LLM ADAPTER -> MODEL PROVIDER -> ZT&SI RUNTIME -> FIREWALL -> RESPONSE
```

The v0.3 LLM Adapter receives application input at `/generate`, calls a provider such as `mock`, sends the generated candidate output through the existing ZT&SI runtime, logs generated events to `runtime_logs/generate_events.jsonl`, and returns the certified firewall response.

## Semantic Drift Intelligence Layer

```text
INPUT + CANDIDATE OUTPUT -> EMBEDDINGS -> SEMANTIC DRIFT -> CONTRADICTION -> RECURSIVE INSTABILITY -> GOVERNANCE -> FIREWALL
```

The v0.4 intelligence layer computes semantic similarity, contradiction score, recursive instability score, and final drift score. These metrics are logged to `runtime_logs/drift_metrics.jsonl` and returned by `/evaluate` and `/generate`.

## Projection & Runtime Stabilization

```text
CLIENT -> LLM -> DRIFT INTELLIGENCE -> PROJECTION ENGINE -> REVALIDATION -> GOVERNANCE -> FIREWALL -> RESPONSE
```

The v0.5 projection engine attempts bounded semantic recovery before final rejection. Correctable contradictions and recursive instability are normalized, re-scored, and sent through governance. Stabilization events are logged to `runtime_logs/stabilization_events.jsonl`.

## Recursive Memory & Lineage Graph

```text
CLIENT -> LLM -> DRIFT INTELLIGENCE -> PROJECTION -> GOVERNANCE -> FIREWALL -> MEMORY STORE -> LINEAGE GRAPH -> SNAPSHOT -> RESPONSE
```

The v0.6 memory engine persists cognition states to `runtime_memory/`, updates a directed semantic lineage graph, creates stable snapshots, and supports rollback to the nearest stable semantic ancestor.

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
- `src/llm/base.py` defines the provider interface.
- `src/llm/mock_provider.py` implements mock-first stable and unstable generation.
- `src/llm/providers.py` registers provider names.
- `src/llm/adapter.py` routes generated candidate outputs into ZT&SI runtime validation.
- `src/intelligence/embeddings.py` provides optional sentence-transformer embeddings with local fallback.
- `src/intelligence/semantic_drift.py` computes semantic continuity and topic divergence.
- `src/intelligence/contradiction.py` detects logical reversal and conflicting claims.
- `src/intelligence/recursive_instability.py` detects recursive destabilization language.
- `src/intelligence/scoring.py` combines intelligence signals into the unified drift score.
- `src/stabilization/projection.py` coordinates bounded semantic recovery.
- `src/stabilization/correction.py` performs contradiction soft correction.
- `src/stabilization/recovery.py` removes recursive instability and runaway recursion patterns.
- `src/stabilization/normalization.py` normalizes projected text.
- `src/stabilization/policies.py` defines projection modes.
- `src/memory/semantic_memory.py` persists runtime cognition states.
- `src/memory/lineage_graph.py` reconstructs ancestry and descendants.
- `src/memory/snapshots.py` creates stable checkpoints.
- `src/memory/rollback.py` restores nearest stable semantic ancestors.
- `src/memory/retrieval.py` provides recent, stable, unstable, and lineage-specific memory retrieval.
