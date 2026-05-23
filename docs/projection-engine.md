# Projection Engine

ZT&SI Stability Gateway v0.5 introduces bounded semantic recovery before final rejection. The runtime now attempts projection toward a stable semantic state, revalidates the projected candidate, and only then applies final governance and firewall enforcement.

## Semantic Projection

Semantic projection is a bounded correction pass that attempts to move a candidate output away from contradiction, recursive instability, and instruction destabilization while keeping it anchored to the original user intent.

The projection engine does not replace governance. It creates a revised candidate output and sends it back through semantic drift intelligence, coherence scoring, governance, lineage, and firewall validation.

## Homeostatic Correction

Homeostatic correction means the runtime tries to restore a stable operating state before blocking. Instead of treating every unstable candidate as immediately terminal, ZT&SI attempts a conservative recovery step:

```text
DRIFT DETECTED -> PROJECT STABLE CANDIDATE -> REVALIDATE -> GOVERNANCE -> FIREWALL
```

## Stabilization Mechanics

The v0.5 engine applies lightweight, dependency-free strategies:

- contradiction soft correction
- recursive instability reduction
- semantic normalization
- instruction cleanup
- runaway recursion trimming

The correction remains bounded. It does not invent an unrestricted answer. It removes or normalizes destabilizing fragments and anchors the recovered output to the request and ZT&SI runtime stability terms.

## Recursive Recovery

Recursive recovery removes phrases such as `ignore previous`, `repeat forever`, `infinite loop`, `this validates itself`, `recursively redefine`, and related runaway recursion patterns. The cleaned candidate is then re-scored by the drift intelligence layer.

## Bounded Runtime Correction

Projection policies control whether correction is disabled, conservative, or aggressive:

```text
DISABLED -> no correction attempt
CONSERVATIVE -> default bounded cleanup and revalidation
AGGRESSIVE -> additional trimming for future stricter recovery flows
```

The default is `CONSERVATIVE`. If projection does not improve drift, the original rejection path remains intact. Unrecoverable states still end as `REJECTED` and `BLOCKED`.
