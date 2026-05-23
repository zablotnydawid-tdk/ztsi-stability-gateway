# Multi-Agent Governance Mesh

ZT&SI Stability Gateway v0.9 treats agents as sandboxed cognition processes. Each agent has permissions, drift budget, recursion quota, memory scope, lineage scope, output rights, and runtime status.

## Sandboxed Cognition Processes

An `AgentRuntime` is not a free execution path. It is a governed runtime subject with explicit boundaries:

- `agent_id`
- `role`
- `permissions`
- `recursion_quota`
- `drift_budget`
- `memory_scope`
- `lineage_scope`
- `output_rights`
- `status`

Statuses are `ACTIVE`, `FROZEN`, `QUARANTINED`, and `BLOCKED`.

## Agent Permissions

The sandbox checks whether an agent has the required permission for an action. A missing permission freezes the agent and logs a sandbox governance event.

## Drift Budgets

`AgentBudgetManager` tracks cumulative drift usage per agent. If an agent exceeds its configured drift budget, the sandbox freezes it and records a drift budget violation.

## Recursion Quotas

The sandbox enforces recursion quota limits. An agent exceeding its recursion quota is frozen before it can continue recursive execution.

## Lineage Scopes

Lineage scopes define how an agent is allowed to relate to memory and graph ancestry. v0.9 stores the field and enforces it as part of the sandbox model, leaving room for stricter cross-agent lineage policies.

## Governance Mesh

`GovernanceMesh` coordinates registered agents, evaluates agent execution through the existing ZT&SI runtime, syncs global policy, tracks agent stability, and computes mesh health.

Mesh health can be:

```text
STABLE
DEGRADED
CRITICAL
```

## Arbitration Logic

`AgentArbitrator` resolves competing outputs. The winning candidate must be policy-compliant and unblocked. Among viable candidates, arbitration prefers:

1. higher coherence
2. lower drift
3. policy-compliant output
4. stable lineage

Blocked outputs cannot win.

## Architecture

```text
CLIENT
  -> AGENT REGISTRY
  -> AGENT SANDBOX
  -> LLM / CANDIDATE OUTPUT
  -> DRIFT INTELLIGENCE
  -> PROJECTION
  -> POLICY ENGINE
  -> GOVERNANCE MESH
  -> ARBITRATION
  -> FIREWALL
  -> MEMORY
  -> TELEMETRY
  -> RESPONSE
```
