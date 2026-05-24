# Release Candidate Checklist

## Test Status

Run:

```bash
python -m unittest discover -s tests
```

Expected result:

```text
All tests pass.
```

## Validation Status

Run:

```bash
python validation/evidence/generate_evidence_pack.py
```

Expected result:

```text
runtime: pass
replay: pass
policies: pass
telemetry: pass
boundary: pass
```

## Evidence Pack Status

Evidence output:

```text
validation/evidence/EVIDENCE_PACK.md
```

The Evidence Pack is a local, repeatable snapshot of runtime governance degradation behavior. It is not a certificate, not an external audit, and not a production security guarantee.

## Boundary Audit Status

Required checks:

- no secrets
- no private local paths
- no sovereign-core leakage
- no tracked runtime logs
- no tracked runtime memory
- no runtime artifacts committed outside controlled evidence output

## Known Limitations

- The public runtime uses lightweight heuristics and mock generation.
- The Evidence Pack is local and depends on the current repository state.
- Replay validates recorded governance outcomes against public policy behavior; it does not prove semantic correctness.
- This repository is a public proof-of-work, not production security software.
- Advanced sovereign-core mechanisms are intentionally outside this repository.

## Non-Claims

- This release candidate is not an external audit.
- This release candidate is not a safety certification.
- This release candidate is not a production firewall guarantee.
- This release candidate does not expose private sovereign-core IP.
- This release candidate does not claim AGI behavior.

## Release Decision

Release candidate is acceptable when:

- full test suite passes
- Evidence Pack is generated successfully
- boundary audit has zero findings
- telemetry integrity passes
- policy mismatch count is understood and documented
- no runtime artifacts or secrets are tracked

Decision:

```text
READY FOR v1.0 RC SNAPSHOT when all required checks pass locally.
```
