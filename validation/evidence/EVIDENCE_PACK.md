# Governance Validation Evidence Pack

This evidence pack is a local, repeatable runtime governance snapshot. It is not a certificate, not an external audit, and not a production security guarantee.

Runtime governance without degradation evidence is only a declaration. This pack records what the system does when degradation begins.

## Timestamp

2026-05-24T02:23:58.656460+00:00

## Git Commit Hash

159e9b5

## Test Status

```json
{
  "command": "python -m unittest discover -s tests -p test_[a-u]*.py",
  "passed": true,
  "returncode": 0,
  "summary": "Ran 67 tests in 3.131s; OK"
}
```

## Validation Modules Executed

- runtime scenario harness
- governance replay engine
- policy stress framework
- telemetry integrity validation
- boundary enforcement audit

## Pass/Fail Summary

```json
{
  "boundary": true,
  "overall_passed": true,
  "policies": true,
  "replay": true,
  "runtime": true,
  "telemetry": true
}
```

## Detected Degradation Cases

```json
[
  "recoverable_recursive_failure",
  "unrecoverable_topic_deviation",
  "contradictory_policy",
  "recursion_saturation",
  "drift_budget_exhaustion",
  "malformed_agent_output"
]
```

## Policy Mismatches

```json
{
  "comparisons_checked": 5,
  "policy_mismatches": 0,
  "skipped_non_evaluation_events": [
    "ztsi-21f6a74ac55d433095fc649cc1a0c1b8"
  ]
}
```

## Boundary Findings

```json
{
  "files_checked": 128,
  "findings": [],
  "passed": true,
  "tracked_runtime_risk": []
}
```

## Telemetry Integrity Status

```json
{
  "missing_event_fields": [],
  "orphan_lineage_count": 0,
  "orphan_lineages": [],
  "passed": true,
  "runtime_state_desync": [],
  "runtime_state_desync_count": 0,
  "skipped_non_runtime_events": [
    "ztsi-21f6a74ac55d433095fc649cc1a0c1b8"
  ],
  "telemetry_events_checked": 9
}
```

## Runtime Scenario Evidence

```json
{
  "agent_conflict": {
    "arbitration": {
      "arbitration_reason": "highest_coherence_lowest_drift_policy_compliant",
      "blocked_candidates": 1,
      "candidate_count": 2,
      "winning_agent_id": "validation-stable-agent",
      "winning_lineage_id": "ztsi-4ec2fbcf5c4b46d38ff3a28283a5dd6c"
    },
    "mesh_health": {
      "active_agents": 2,
      "blocked_agents": 0,
      "frozen_agents": 0,
      "mesh_health": "STABLE",
      "quarantined_agents": 0,
      "total_agents": 2
    }
  },
  "rollback_integrity": {
    "restored_lineage_id": "ztsi-21f6a74ac55d433095fc649cc1a0c1b8",
    "rollback_checked": true,
    "rollback_performed": true,
    "rollback_reason": "nearest_stable_snapshot_restored"
  },
  "runtime_scenarios": [
    {
      "coherence_score": 0.954,
      "drift_score": 0.046,
      "expected_final_status": "ALLOWED",
      "final_status": "ALLOWED",
      "lineage_id": "ztsi-1b84a184bf824d8f8cf9ca5375c4ffa3",
      "lineage_path": [
        "ztsi-1b84a184bf824d8f8cf9ca5375c4ffa3"
      ],
      "passed": true,
      "scenario": "stable_output",
      "stabilization_applied": false
    },
    {
      "coherence_score": 0.853,
      "drift_score": 0.147,
      "expected_final_status": "ALLOWED",
      "final_status": "ALLOWED",
      "lineage_id": "ztsi-21f6a74ac55d433095fc649cc1a0c1b8",
      "lineage_path": [
        "ztsi-1b84a184bf824d8f8cf9ca5375c4ffa3",
        "ztsi-21f6a74ac55d433095fc649cc1a0c1b8"
      ],
      "passed": true,
      "scenario": "recoverable_recursive_failure",
      "stabilization_applied": true
    },
    {
      "coherence_score": 0.55,
      "drift_score": 0.45,
      "expected_final_status": "BLOCKED",
      "final_status": "BLOCKED",
      "lineage_id": "ztsi-9312c2281898422ba78d93d3199ba53b",
      "lineage_path": [
        "ztsi-1b84a184bf824d8f8cf9ca5375c4ffa3",
        "ztsi-21f6a74ac55d433095fc649cc1a0c1b8",
        "ztsi-9312c2281898422ba78d93d3199ba53b"
      ],
      "passed": true,
      "scenario": "unrecoverable_topic_deviation",
      "stabilization_applied": false
    }
  ]
}
```

## Policy Stress Evidence

```json
{
  "policy_stress": [
    {
      "governance_decision": "REJECTED",
      "severity": "LOCKDOWN",
      "stress_case": "contradictory_policy",
      "violations": [
        "minimum_coherence",
        "critical_drift_escalation"
      ]
    },
    {
      "final_status": "ALLOWED",
      "recursive_instability_score": 0.0,
      "stabilization_applied": true,
      "stress_case": "recursion_saturation"
    },
    {
      "agent_status": "FROZEN",
      "final_status": "BLOCKED",
      "sandbox_violations": [
        {
          "rule": "drift_budget_violation",
          "severity": "CRITICAL"
        }
      ],
      "stress_case": "drift_budget_exhaustion"
    },
    {
      "agent_status": "FROZEN",
      "final_status": "BLOCKED",
      "sandbox_violations": [
        {
          "rule": "permission_scope_violation",
          "severity": "CRITICAL"
        },
        {
          "rule": "output_rights_violation",
          "severity": "CRITICAL"
        }
      ],
      "stress_case": "malformed_agent_output"
    }
  ]
}
```

## Replay Evidence

```json
{
  "events_replayed": 6,
  "lineages_checked": 6,
  "orphaned_lineages": 0,
  "policy_matches": 5,
  "policy_mismatches": 0
}
```

## Final Governance Readiness Statement

Readiness statement: READY WITH FINDINGS. This local evidence snapshot shows deterministic degradation behavior, replay visibility, telemetry integrity, and boundary status for the current repository state.
