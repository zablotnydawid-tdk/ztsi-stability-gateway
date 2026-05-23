# Runtime Observability & Telemetry Mesh

ZT&SI Stability Gateway v0.7 makes the runtime observable as a live cognitive stability system. Every runtime execution emits telemetry that can be aggregated into stability metrics, governance analytics, health state, and terminal dashboard summaries.

## Runtime Observability

The telemetry mesh records runtime events into `runtime_logs/telemetry.jsonl`. Each event captures coherence, drift, governance outcome, firewall status, stabilization state, recursive instability, contradiction, snapshot creation, lineage path size, and rollback-oriented context.

## Cognitive Telemetry

ZT&SI treats runtime behavior as cognitive telemetry rather than plain request logs. The system can answer:

- How many outputs were approved or blocked?
- How often projection recovery succeeds?
- Whether recursive instability is increasing?
- Whether contradiction pressure is rising?
- Whether rollback frequency signals degradation?

## Stability Metrics

`RuntimeTelemetryEngine` and `TelemetryAggregator` track:

- total runtime executions
- approved outputs
- blocked outputs
- stabilization attempts
- stabilization success rate
- rollback count
- average coherence
- average drift
- recursive instability frequency
- contradiction frequency
- snapshot count
- lineage graph size

## Governance Analytics

Governance analytics summarize approved, rejected, blocked, and recovered outputs. The API exposes these through `/telemetry/governance`, while the CLI dashboard renders governance outcome bars.

## Semantic Runtime Monitoring

`RuntimeHealthMonitor` classifies system health:

```text
STABLE   -> high coherence and low drift
DEGRADED -> rollback frequency rising or drift/coherence weakening
CRITICAL -> blocked outputs dominate or drift is high
```

## Dashboard Output

The dashboard is intentionally lightweight. It renders pure terminal summaries and ASCII charts for coherence trend, drift trend, governance outcomes, and stabilization outcomes. No frontend framework is required.
