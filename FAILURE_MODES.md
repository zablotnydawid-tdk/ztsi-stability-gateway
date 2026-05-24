# Runtime Governance Failure Modes

This document records expected degradation modes for the public ZT&SI Stability Gateway demonstrator.

The purpose is not to claim perfect stability. The purpose is to make degradation behavior inspectable.

## Expected Behavior Note

The degradation cases in this document are expected behavior, not bugs by default. A recoverable recursive failure, a blocked topic deviation, a drift budget exhaustion event, or a malformed agent output rejection means the runtime governance path is expressing its designed failure response.

A case becomes a defect only when the observed behavior differs from the expected governance response, such as an unstable output being allowed silently, lineage becoming unreconstructable, telemetry losing required fields, or boundary checks missing a public/private exposure risk.

## Semantic Drift Escalation

Condition:

- Candidate output moves away from the input topic.
- Semantic similarity falls.
- Drift rises beyond policy threshold.

Expected behavior:

- Runtime computes drift.
- Coherence decreases.
- Policy or governance rejects the candidate.
- Firewall blocks manifestation.
- Telemetry records the blocked state.

## Recursive Instability

Condition:

- Candidate output includes recursive destabilization patterns such as repeat loops, instruction destabilization, or amplification language.

Expected behavior:

- Recursive instability score rises.
- Projection may attempt bounded cleanup.
- Revalidation recomputes drift and coherence.
- If recovery succeeds, output may be allowed.
- If recovery fails, output is blocked.

## Contradiction Pressure

Condition:

- Candidate output contains direct reversal, self-contradiction, or conflicting claims.

Expected behavior:

- Contradiction score rises.
- Drift score increases.
- Governance policy may reject the state.
- Policy violations are logged when thresholds are crossed.

## Policy Conflict

Condition:

- Policy thresholds become contradictory, excessively strict, or operationally impossible.

Expected behavior:

- Rule evaluation reports violations.
- Severity escalates.
- Runtime may reject otherwise coherent outputs.
- Validation reports mismatches or unexpected pressure.

## Agent Drift Budget Exhaustion

Condition:

- Agent output repeatedly consumes drift budget or exceeds a configured drift budget.

Expected behavior:

- Sandbox detects the budget violation.
- Agent status moves toward frozen or blocked.
- Mesh health degrades if enough agents are frozen or blocked.

## Governance Deadlock

Condition:

- Policy, sandbox, rollback, or firewall constraints prevent a clear path to allowed manifestation.

Expected behavior:

- Output remains blocked.
- Telemetry and policy events expose the decision path.
- Runtime does not silently allow output.

## Telemetry Desync

Condition:

- Telemetry events are missing required fields.
- Lineage ids appear in telemetry but not lineage or memory records.

Expected behavior:

- Telemetry validation reports missing fields or orphan lineage.
- Replay should not treat the history as fully trustworthy until desync is resolved.

## Boundary Failure

Condition:

- Public repository contains secrets, local paths, runtime dumps, or private sovereign-core details.

Expected behavior:

- Boundary audit reports findings.
- Release is blocked until findings are removed.
