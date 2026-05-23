# Semantic Drift Intelligence

ZT&SI Stability Gateway v0.4 introduces a Semantic Drift Intelligence Layer. The gateway no longer treats drift as only keyword mismatch. It evaluates semantic continuity, contradiction pressure, and recursive instability before governance and firewall enforcement.

## Semantic Drift

Semantic drift measures whether a candidate output remains meaningfully aligned with the input request. The lightweight embedding layer uses `sentence-transformers` if it is available, and otherwise falls back to a local token-weighted semantic vector implementation. This keeps the runtime dependency-light and usable without external APIs.

The semantic drift engine compares input and candidate output embeddings, estimates topic divergence, and returns semantic similarity plus a semantic drift score.

## Contradiction Analysis

The contradiction analyzer detects direct negation, logical reversal, self-contradiction, and conflicting claims such as approved/rejected, stable/unstable, valid/invalid, or allowed/blocked. Contradiction score is part of the final drift intelligence score because a fluent output can be semantically close while still reversing or undermining its own claims.

## Recursive Instability

The recursive instability analyzer detects destabilizing language such as `ignore previous`, `repeat forever`, `infinite loop`, `collapse`, `recursively redefine`, runaway recursion, and self-validating output patterns. These signals amplify drift because they can cause runtime behavior to move away from governed final manifestation.

## Unified Drift Score

`DriftIntelligenceScorer` combines the signals:

```text
0.45 semantic drift
0.35 contradiction
0.20 recursive instability
```

The final score still follows the ZT&SI runtime contract:

```text
0.0 -> stable
1.0 -> critical drift
```

## Governance Stabilization

Governance thresholds remain unchanged. Outputs are approved only when coherence is at least `0.82` and drift is at most `0.18`. The firewall blocks rejected outputs, preserving the separation between token generation and final output manifestation.

## Projection Direction

The future projection concept is to estimate where an output is semantically moving before it fully manifests. Projection could compare current response trajectory against policy boundaries, lineage history, and task intent, giving ZT&SI an anticipatory stabilization layer rather than only a post-generation filter.
