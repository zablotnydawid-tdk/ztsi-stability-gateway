import json
from pathlib import Path


TELEMETRY_LOG_PATH = Path("runtime_logs") / "telemetry.jsonl"


class TelemetryStore:
    def __init__(self, log_path: Path = TELEMETRY_LOG_PATH) -> None:
        self.log_path = log_path

    def append(self, event: dict) -> dict:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        return event

    def read_events(self) -> list[dict]:
        if not self.log_path.exists():
            return []
        return [
            json.loads(line)
            for line in self.log_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
