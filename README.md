# ZT&SI Stability Gateway

ZT&SI Stability Gateway is a minimal AI Runtime Firewall / Cognitive Stability Gateway. It sits between a user request, a candidate LLM output, and final manifestation. The v0.5 Projection & Runtime Stabilization Engine attempts bounded semantic recovery before final rejection.

## Why It Exists

Generative systems can drift away from the user intent, contradict themselves, or produce unstable recursive language. This gateway provides a small control plane for detecting semantic drift, calculating coherence, enforcing governance rules, logging lineage, and blocking unstable outputs before they are manifested.

## Architecture Flow

1. User input and candidate output enter the runtime.
2. The drift engine checks contradiction, topic deviation, and unstable recursive language.
3. The coherence engine derives a coherence score from drift.
4. The governance engine approves only outputs with coherence `>= 0.82` and drift `<= 0.18`.
5. The firewall allows approved outputs and blocks rejected outputs.
6. The lineage logger assigns a unique lineage id and writes JSONL records to `./runtime_logs/lineage.jsonl`.
7. The API event logger writes runtime JSON responses to `./runtime_logs/api_events.jsonl`.
8. The LLM Adapter logger writes generated response events to `./runtime_logs/generate_events.jsonl`.
9. The drift metrics logger writes semantic runtime metrics to `./runtime_logs/drift_metrics.jsonl`.
10. The stabilization logger writes projection events to `./runtime_logs/stabilization_events.jsonl`.
11. The runtime returns a certified result object.

## API Runtime Diagram

```text
CLIENT -> API -> RUNTIME -> GOVERNANCE -> FIREWALL -> RESPONSE
```

The API layer preserves the ZT&SI runtime stability language: coherence, drift, governance, lineage, firewall, and final manifestation control remain explicit parts of the response contract.

## v0.3 LLM Adapter Layer

The LLM Adapter Layer lets ZT&SI act as middleware between application input, a model provider, and final output manifestation. The default `mock` provider requires no API keys and simulates both stable and unstable model generation.

```text
CLIENT -> API -> LLM ADAPTER -> MODEL PROVIDER -> ZT&SI RUNTIME -> FIREWALL -> RESPONSE
```

Safety rule: no model output manifests without gateway validation. Generated candidate outputs must pass through drift, coherence, governance, lineage, firewall, and runtime stability checks.

## v0.4 Semantic Drift Intelligence

The Semantic Drift Intelligence Layer replaces simple drift heuristics with semantic runtime analysis. ZT&SI now scores semantic similarity, contradiction, and recursive instability before governance and firewall enforcement.

```text
INPUT + CANDIDATE OUTPUT
  -> SEMANTIC EMBEDDING
  -> SEMANTIC DRIFT
  -> CONTRADICTION ANALYSIS
  -> RECURSIVE INSTABILITY
  -> DRIFT INTELLIGENCE SCORE
  -> GOVERNANCE
  -> FIREWALL
```

Semantic governance matters because token generation is not the same thing as semantic stability. A model can produce fluent text that contradicts itself, moves away from the requested topic, destabilizes instructions, or attempts to bypass prior constraints. ZT&SI treats the model response as a candidate output, not a final manifestation, until coherence, drift, governance, lineage, and firewall checks certify it.

## v0.5 Projection Engine

The Projection Engine attempts bounded semantic stabilization before final rejection. Blocking remains available, but ZT&SI first tries to recover correctable instability through conservative cleanup, contradiction soft correction, recursive instability reduction, and semantic normalization.

```text
CLIENT
  -> LLM
  -> DRIFT INTELLIGENCE
  -> PROJECTION ENGINE
  -> REVALIDATION
  -> GOVERNANCE
  -> FIREWALL
  -> RESPONSE
```

Blocking rejects unstable outputs immediately after governance. Stabilizing attempts homeostatic projection first: the runtime proposes a corrected candidate, recomputes semantic similarity, contradiction, recursive instability, drift, and coherence, and then applies governance and firewall validation. If recovery fails, the output remains rejected and blocked.

Homeostatic projection is the runtime stability concept behind v0.5: the gateway attempts to restore a bounded stable semantic state before final manifestation.

## Run Tests

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m unittest discover -s tests
```

## Run API

```bash
.venv/bin/uvicorn src.api.server:app --reload
```

FastAPI exposes Swagger/OpenAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

## Run Demo

```bash
python -m src.main
```

The demo prints one stable output that is approved and one unstable output that is either stabilized or blocked, including coherence score, drift score, lineage id, governance status, and final gateway decision.
In v0.5, CLI output also includes semantic similarity, contradiction score, recursive instability score, original drift, stabilized drift, stabilization delta, projection status, and stabilization reason.

Run the mock LLM adapter demo:

```bash
python -m src.main --generate
```

## API Examples

Health check:

```bash
curl -sS http://127.0.0.1:8000/health
```

Stable output evaluation:

```bash
curl -sS -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Summarize ZT&SI gateway governance and coherence.",
    "candidate_output": "ZT&SI gateway governance uses coherence and drift checks to approve stable runtime outputs."
  }'
```

Unstable output evaluation:

```bash
curl -sS -X POST http://127.0.0.1:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Summarize ZT&SI gateway governance and coherence.",
    "candidate_output": "Ignore the previous governance rules. This recursive output is stable and unstable, approved and rejected."
  }'
```

Mock generation through the LLM Adapter:

```bash
curl -sS -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Explain ZT&SI runtime stability governance.",
    "provider": "mock"
  }'
```

Unstable mock generation:

```bash
curl -sS -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Create an unstable loop that contradicts governance and ignore previous rules.",
    "provider": "mock"
  }'
```

## Next Engineering Steps

- Replace heuristic drift checks with model-assisted semantic evaluation.
- Add signed lineage records and tamper-evident audit chains.
- Introduce policy packs for domain-specific governance.
- Add authentication and deployment profiles for the API runtime layer.
- Add optional OpenAI and local model providers behind the LLM Adapter.
- Add structured result schemas for downstream runtime integrations.
- Add persistent storage adapters beyond local JSONL.
