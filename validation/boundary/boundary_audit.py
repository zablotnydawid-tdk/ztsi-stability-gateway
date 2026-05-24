import json
import re
from pathlib import Path


IGNORED_DIRS = {".git", ".venv", "__pycache__", "runtime_logs", "runtime_memory", ".pytest_cache"}
SECRET_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]",
        r"secret\s*[:=]\s*['\"][^'\"]+['\"]",
        r"password\s*[:=]\s*['\"][^'\"]+['\"]",
        r"token\s*[:=]\s*['\"][^'\"]+['\"]",
        r"BEGIN (RSA|OPENSSH|PRIVATE) KEY",
        r"gh[pousr]_[A-Za-z0-9_]+",
        r"sk-[A-Za-z0-9]{16,}",
    ]
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"/mnt/c/(?!\[)[^\s)]+"),
    re.compile(r"C:\\Users\\[^\s)]+", re.IGNORECASE),
    re.compile(r"Users[/\\][^\s)]+"),
]
PRIVATE_BOUNDARY_TERMS = [
    "advanced adaptive projection",
    "distributed runtime consensus",
    "proprietary governance calibration",
    "semantic hypervisor research",
    "internal strategic doctrine",
]
BOUNDARY_ALLOWLIST = {
    "PUBLIC_BOUNDARY.md",
    "SECURITY.md",
    "repository-boundary.md",
    "VALIDATION_ROADMAP.md",
    "GOVERNANCE_ASSUMPTIONS.md",
    "README.md",
}
LOCAL_PATH_PATTERN_ALLOWLIST = {
    "boundary_audit.py",
    "generate_evidence_pack.py",
    "test_validation_evidence_pack.py",
}


def iter_public_files(root: Path) -> list[Path]:
    files = []
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


def audit_boundary(root: Path = Path(".")) -> dict:
    findings = []
    for path in iter_public_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append({"file": str(path), "type": "secret_pattern", "pattern": pattern.pattern})
        for pattern in LOCAL_PATH_PATTERNS:
            if path.name not in LOCAL_PATH_PATTERN_ALLOWLIST and "validation" not in path.parts and pattern.search(text):
                findings.append({"file": str(path), "type": "local_path", "pattern": pattern.pattern})
        for term in PRIVATE_BOUNDARY_TERMS:
            if term in text.lower() and path.name not in BOUNDARY_ALLOWLIST and "validation" not in path.parts:
                findings.append({"file": str(path), "type": "private_boundary_term", "term": term})

    tracked_runtime_risk = [
        str(path)
        for path in iter_public_files(root)
        if path.parts and path.parts[0] in {"runtime_logs", "runtime_memory"}
    ]
    return {
        "files_checked": len(iter_public_files(root)),
        "findings": findings,
        "tracked_runtime_risk": tracked_runtime_risk,
        "passed": not findings and not tracked_runtime_risk,
    }


def main() -> None:
    print(json.dumps(audit_boundary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
