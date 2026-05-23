from datetime import datetime, timezone
import json
from pathlib import Path

from .evaluator import RuleEvaluator
from .loader import PolicyLoader
from .registry import PolicyRegistry
from .severity import Severity, max_severity


POLICY_VIOLATIONS_LOG_PATH = Path("runtime_logs") / "policy_violations.jsonl"
LOCKDOWN_STATE_PATH = Path("runtime_logs") / "lockdown_state.json"


class RuntimeLockdownManager:
    def __init__(self, state_path: Path = LOCKDOWN_STATE_PATH) -> None:
        self.state_path = state_path

    def is_locked(self) -> bool:
        state = self._read_state()
        return bool(state.get("lockdown_active", False))

    def activate(self, reason: str) -> dict:
        state = {
            "lockdown_active": True,
            "runtime_status": "LOCKDOWN",
            "lockdown_reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, sort_keys=True, indent=2), encoding="utf-8")
        return state

    def release(self) -> dict:
        state = {
            "lockdown_active": False,
            "runtime_status": "NORMAL",
            "lockdown_reason": "manual_or_policy_recovery",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, sort_keys=True, indent=2), encoding="utf-8")
        return state

    def _read_state(self) -> dict:
        if not self.state_path.exists():
            return {"lockdown_active": False, "runtime_status": "NORMAL"}
        return json.loads(self.state_path.read_text(encoding="utf-8"))


class PolicyEngine:
    def __init__(
        self,
        policy: dict | None = None,
        loader: PolicyLoader | None = None,
        lockdown_manager: RuntimeLockdownManager | None = None,
    ) -> None:
        self.policy = policy or (loader or PolicyLoader()).load()
        self.lockdown_manager = lockdown_manager or RuntimeLockdownManager()

    def evaluate(self, state: dict, telemetry_summary: dict | None = None) -> dict:
        if self.lockdown_manager.is_locked():
            return {
                "policy_loaded": True,
                "severity": Severity.LOCKDOWN.value,
                "violations": [
                    {
                        "rule": "runtime_lockdown_active",
                        "scope": "RUNTIME",
                        "severity": Severity.LOCKDOWN.value,
                    }
                ],
                "governance_decision": "REJECTED",
                "runtime_status": "LOCKDOWN",
                "lockdown_active": True,
                "runtime_locked": True,
            }

        violations = RuleEvaluator(self.policy).evaluate(state, telemetry_summary)
        severity = max_severity([Severity(item["severity"]) for item in violations])
        lockdown_active = severity == Severity.LOCKDOWN
        if lockdown_active:
            self.lockdown_manager.activate("policy_lockdown_escalation")

        governance_decision = "REJECTED" if severity in {Severity.CRITICAL, Severity.LOCKDOWN} else "APPROVED"
        runtime_status = self._runtime_status(severity)
        result = {
            "policy_loaded": True,
            "severity": severity.value,
            "violations": violations,
            "governance_decision": governance_decision,
            "runtime_status": runtime_status,
            "lockdown_active": lockdown_active,
            "runtime_locked": lockdown_active,
        }
        self.log_violations(state, result)
        return result

    def status(self) -> dict:
        violations = self.recent_violations()
        registry = PolicyRegistry(self.policy)
        lockdown_active = self.lockdown_manager.is_locked()
        return {
            "runtime_status": "LOCKDOWN" if lockdown_active else ("WARNING" if violations else "NORMAL"),
            "policy_loaded": True,
            "active_rules": len(registry.active_rules()),
            "recent_violations": len(violations),
            "lockdown_active": lockdown_active,
        }

    def recent_violations(self, limit: int = 20) -> list[dict]:
        if not POLICY_VIOLATIONS_LOG_PATH.exists():
            return []
        lines = POLICY_VIOLATIONS_LOG_PATH.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines[-limit:] if line.strip()]

    def reload(self) -> dict:
        self.policy = PolicyLoader().load()
        return {"policy_loaded": True, "active_rules": len(PolicyRegistry(self.policy).active_rules())}

    def log_violations(self, state: dict, policy_result: dict) -> None:
        POLICY_VIOLATIONS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with POLICY_VIOLATIONS_LOG_PATH.open("a", encoding="utf-8") as handle:
            for violation in policy_result["violations"]:
                handle.write(
                    json.dumps(
                        {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "violated_rule": violation["rule"],
                            "severity": violation["severity"],
                            "runtime_state": {
                                "lineage_id": state.get("lineage_id", ""),
                                "coherence_score": state.get("coherence_score", 0.0),
                                "drift_score": state.get("drift_score", 0.0),
                                "governance_status": state.get("governance_status", "PENDING"),
                            },
                            "governance_decision": policy_result["governance_decision"],
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )

    def _runtime_status(self, severity: Severity) -> str:
        if severity == Severity.LOCKDOWN:
            return "LOCKDOWN"
        if severity == Severity.CRITICAL:
            return "CRITICAL"
        if severity == Severity.WARNING:
            return "WARNING"
        return "NORMAL"
