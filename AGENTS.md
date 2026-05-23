# Agent Instructions

Future coding agents working on ZT&SI Stability Gateway must preserve the ZT&SI terminology and product framing.

Do not remove governance logic. Do not bypass firewall validation. Every output must pass through drift, coherence, governance, lineage, and firewall handling before final manifestation.

Keep modules small, explicit, and testable. Preserve the separation between semantic state, drift scoring, coherence scoring, governance decisions, firewall enforcement, lineage logging, and runtime orchestration.

When adding new capabilities, update tests and documentation together. Any external LLM integration must remain behind the gateway validation flow.
