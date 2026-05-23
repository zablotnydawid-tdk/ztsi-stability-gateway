# Recursive Memory & Lineage Graph Engine

ZT&SI Stability Gateway v0.6 preserves recoverable semantic cognition trajectories across execution time. Every runtime pass can now become part of persistent semantic memory, lineage ancestry, and rollback-capable cognition history.

## Recursive Semantic Memory

`SemanticMemoryStore` persists runtime cognition states into `runtime_memory/` using lightweight JSON files. Stored states include lineage id, input, candidate output, drift, coherence, governance, firewall, stabilization status, timestamp, and optional parent state id.

This lets ZT&SI reason over execution history instead of treating every runtime request as isolated.

## Lineage Graph Topology

`LineageGraph` represents runtime states as a directed semantic graph. Parent-child edges preserve recursive ancestry between states:

```text
stable checkpoint -> projected recovery -> follow-up state
```

The graph supports ancestry, descendant lookup, and deterministic path reconstruction.

## Rollback-Capable Cognition

`RollbackEngine` reconstructs the lineage path for a requested state and searches backward for the nearest stable snapshot. If one exists, rollback returns the restored lineage id and coherence score. If none exists, rollback reports that no stable snapshot is available.

Rollback does not bypass governance. It restores only approved, allowed, high-coherence snapshots.

## Snapshot Architecture

`SnapshotManager` creates checkpoints only when:

```text
governance_status == APPROVED
firewall_status == ALLOWED
coherence_score >= 0.82
```

Snapshots are stored in `runtime_memory/snapshots/`.

## Semantic Ancestry

Semantic ancestry is the ordered chain of parent states that led to a runtime state. This lets ZT&SI inspect whether a response came from a stable path, a recovered projection, or an unstable branch.

## Deterministic Trajectory Reconstruction

Because states and graph edges are persisted locally, ZT&SI can reconstruct trajectory paths deterministically:

```text
lineage_id -> parent -> parent -> stable root
```

This supports recursive runtime debugging, rollback, and future policy evaluation over cognition history.
