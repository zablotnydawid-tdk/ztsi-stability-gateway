from pathlib import Path


DEFAULT_POLICY = {
    "name": "ZT&SI Default Runtime Governance Policy",
    "version": "0.8",
    "minimum_coherence": 0.82,
    "maximum_drift": 0.18,
    "maximum_contradiction": 0.50,
    "maximum_recursive_instability": 0.50,
    "allow_projection_recovery": True,
    "critical_block_threshold": 0.75,
    "rollback_frequency_warning": 0.15,
    "rollback_storm_threshold": 0.35,
    "repeated_failure_threshold": 5,
    "lockdown_recursive_instability": 0.95,
}


class PolicyLoader:
    def __init__(self, policy_path: Path = Path("policy") / "default_policy.yaml") -> None:
        self.policy_path = policy_path

    def load(self) -> dict:
        if not self.policy_path.exists():
            return dict(DEFAULT_POLICY)
        try:
            loaded = self._load_yaml_text(self.policy_path.read_text(encoding="utf-8"))
            return self._validate(loaded)
        except Exception:
            return dict(DEFAULT_POLICY)

    def _load_yaml_text(self, text: str) -> dict:
        try:
            import yaml

            parsed = yaml.safe_load(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        parsed: dict[str, object] = {}
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            parsed[key.strip()] = self._coerce_value(value.strip())
        return parsed

    def _coerce_value(self, value: str):
        lowered = value.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        try:
            return float(value)
        except ValueError:
            return value

    def _validate(self, policy: dict) -> dict:
        merged = dict(DEFAULT_POLICY)
        if not isinstance(policy, dict):
            return merged
        merged.update(policy)
        for key in (
            "minimum_coherence",
            "maximum_drift",
            "maximum_contradiction",
            "maximum_recursive_instability",
            "critical_block_threshold",
            "rollback_frequency_warning",
            "rollback_storm_threshold",
        ):
            float(merged[key])
        merged["allow_projection_recovery"] = bool(merged["allow_projection_recovery"])
        return merged
