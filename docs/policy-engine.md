# Policy Engine & Governance Ruleset

ZT&SI Stability Gateway v0.8 introduces dynamic runtime governance. Hardcoded thresholds are replaced by a configurable policy engine that evaluates coherence, drift, contradiction, recursive instability, projection recovery, and rollback pressure.

## Runtime Governance Doctrine

ZT&SI treats every output as a governed candidate until a policy decision allows manifestation. Policy evaluation happens after semantic drift intelligence and projection revalidation, and before final firewall manifestation.

The default policy is stored at:

```text
policy/default_policy.yaml
```

## Dynamic Rule Evaluation

`PolicyLoader` loads the policy file and falls back to safe defaults if the file is missing or invalid. `RuleEvaluator` evaluates runtime states against active rules:

- minimum coherence
- maximum drift
- maximum contradiction
- maximum recursive instability
- projection recovery allowance
- rollback frequency warning
- rollback storm detection

## Severity Escalation

Governance severity levels:

```text
INFO     -> allow and record
WARNING  -> allow but log
CRITICAL -> block output
LOCKDOWN -> freeze manifestation
```

The policy engine returns severity, violations, runtime status, and governance decision for every runtime execution.

## Lockdown Protocols

`RuntimeLockdownManager` activates lockdown when policy detects critical recursive instability, critical drift escalation, rollback storm conditions, or other sovereign runtime enforcement triggers.

When lockdown is active, manifestation is disabled and runtime responses are blocked until lockdown is released or policy recovery is applied.

## Sovereign Runtime Enforcement

The policy layer sits between projection and firewall:

```text
DRIFT INTELLIGENCE -> PROJECTION ENGINE -> POLICY ENGINE -> GOVERNANCE -> FIREWALL
```

This makes governance dynamically configurable while preserving ZT&SI terminology, lineage, telemetry, memory, stabilization, and firewall enforcement.
