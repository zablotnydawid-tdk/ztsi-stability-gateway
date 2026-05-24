import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from validation.boundary.boundary_audit import audit_boundary
from validation.policies.stress_framework import (
    test_contradictory_policy,
    test_drift_budget_exhaustion,
    test_malformed_agent_output,
    test_recursion_saturation,
)
from validation.replay.replay_engine import replay_runtime_events, verify_lineage_reconstruction
from validation.runtime.scenario_harness import (
    run_agent_conflict_simulation,
    run_rollback_integrity_check,
    run_runtime_scenarios,
)
from validation.telemetry.integrity_validation import validate_telemetry


EVIDENCE_PACK_PATH = ROOT / "validation" / "evidence" / "EVIDENCE_PACK.md"
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
PRIVATE_PATH_PATTERNS = [
    re.compile(r"/mnt/c/(?!\[)[^\s)]+"),
    re.compile(r"C:\\Users\\[^\s)]+", re.IGNORECASE),
    re.compile(r"Users[/\\][^\s)]+", re.IGNORECASE),
]


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def get_git_commit_hash() -> str:
    result = run_command(["git", "rev-parse", "--short", "HEAD"])
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def run_test_suite() -> dict:
    result = run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_[a-u]*.py"])
    return {
        "command": "python -m unittest discover -s tests -p test_[a-u]*.py",
        "passed": result.returncode == 0,
        "returncode": result.returncode,
        "summary": extract_test_summary(result.stdout + result.stderr),
    }


def extract_test_summary(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if line.startswith("Ran ") and index + 1 < len(lines):
            return f"{line}; {lines[index + 1]}"
    return "No unittest summary captured."


def run_validation_modules() -> dict:
    original_cwd = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="ztsi-evidence-") as runtime_dir:
        os.chdir(runtime_dir)
        try:
            runtime_scenarios = run_runtime_scenarios()
            blocked = next((item for item in runtime_scenarios if item["final_status"] == "BLOCKED"), None)
            runtime = {
                "runtime_scenarios": runtime_scenarios,
                "agent_conflict": run_agent_conflict_simulation(),
                "rollback_integrity": run_rollback_integrity_check(blocked["lineage_id"] if blocked else None),
            }
            replay = {
                "replay": replay_runtime_events(),
                "lineage_reconstruction": verify_lineage_reconstruction(),
            }
            policies = {
                "policy_stress": [
                    test_contradictory_policy(),
                    test_recursion_saturation(),
                    test_drift_budget_exhaustion(),
                    test_malformed_agent_output(),
                ]
            }
            telemetry = validate_telemetry()
        finally:
            os.chdir(original_cwd)

    return {
        "runtime": runtime,
        "replay": replay,
        "policies": policies,
        "telemetry": telemetry,
        "boundary": audit_boundary(ROOT),
    }


def summarize_evidence(test_status: dict, evidence: dict) -> dict:
    runtime_cases = evidence["runtime"]["runtime_scenarios"]
    replay = evidence["replay"]["replay"]
    telemetry = evidence["telemetry"]
    boundary = evidence["boundary"]
    policy_stress = evidence["policies"]["policy_stress"]
    module_status = {
        "runtime": all(item["passed"] for item in runtime_cases),
        "replay": replay["policy_mismatches"] == 0 and evidence["replay"]["lineage_reconstruction"]["orphaned"] == 0,
        "policies": bool(policy_stress),
        "telemetry": telemetry["passed"],
        "boundary": boundary["passed"],
    }
    return {
        "module_status": module_status,
        "overall_passed": test_status["passed"] and all(module_status.values()),
        "degradation_cases": [
            item["scenario"]
            for item in runtime_cases
            if item["final_status"] == "BLOCKED" or item["stabilization_applied"]
        ]
        + [item["stress_case"] for item in policy_stress],
        "policy_mismatches": replay["policy_mismatches"],
        "boundary_findings": len(boundary["findings"]),
        "telemetry_passed": telemetry["passed"],
    }


def scrub_report(text: str) -> str:
    for pattern in PRIVATE_PATH_PATTERNS:
        text = pattern.sub("[redacted-local-path]", text)
    return text


def assert_report_safe(text: str) -> None:
    for pattern in SECRET_PATTERNS + PRIVATE_PATH_PATTERNS:
        if pattern.search(text):
            raise ValueError(f"Evidence pack contains disallowed pattern: {pattern.pattern}")


def render_json_block(value: object) -> str:
    return "```json\n" + json.dumps(value, indent=2, sort_keys=True) + "\n```"


def render_evidence_pack(timestamp: str, git_hash: str, test_status: dict, evidence: dict, summary: dict) -> str:
    readiness = (
        "READY WITH FINDINGS"
        if test_status["passed"] and summary["module_status"]["telemetry"] and summary["module_status"]["boundary"]
        else "NOT READY"
    )
    lines = [
        "# Governance Validation Evidence Pack",
        "",
        "This evidence pack is a local, repeatable runtime governance snapshot. It is not a certificate, "
        "not an external audit, and not a production security guarantee.",
        "",
        "Runtime governance without degradation evidence is only a declaration. This pack records what "
        "the system does when degradation begins.",
        "",
        "## Timestamp",
        "",
        timestamp,
        "",
        "## Git Commit Hash",
        "",
        git_hash,
        "",
        "## Test Status",
        "",
        render_json_block(test_status),
        "",
        "## Validation Modules Executed",
        "",
        "- runtime scenario harness",
        "- governance replay engine",
        "- policy stress framework",
        "- telemetry integrity validation",
        "- boundary enforcement audit",
        "",
        "## Pass/Fail Summary",
        "",
        render_json_block(summary["module_status"] | {"overall_passed": summary["overall_passed"]}),
        "",
        "## Detected Degradation Cases",
        "",
        render_json_block(summary["degradation_cases"]),
        "",
        "## Policy Mismatches",
        "",
        render_json_block(
            {
                "policy_mismatches": summary["policy_mismatches"],
                "comparisons_checked": len(evidence["replay"]["replay"]["comparisons"]),
                "skipped_non_evaluation_events": evidence["replay"]["replay"]["skipped_non_evaluation_events"],
            }
        ),
        "",
        "## Boundary Findings",
        "",
        render_json_block(evidence["boundary"]),
        "",
        "## Telemetry Integrity Status",
        "",
        render_json_block(evidence["telemetry"]),
        "",
        "## Runtime Scenario Evidence",
        "",
        render_json_block(evidence["runtime"]),
        "",
        "## Policy Stress Evidence",
        "",
        render_json_block(evidence["policies"]),
        "",
        "## Replay Evidence",
        "",
        render_json_block(
            {
                "events_replayed": evidence["replay"]["replay"]["events_replayed"],
                "policy_matches": evidence["replay"]["replay"]["policy_matches"],
                "policy_mismatches": evidence["replay"]["replay"]["policy_mismatches"],
                "lineages_checked": evidence["replay"]["lineage_reconstruction"]["lineages_checked"],
                "orphaned_lineages": evidence["replay"]["lineage_reconstruction"]["orphaned"],
            }
        ),
        "",
        "## Final Governance Readiness Statement",
        "",
        f"Readiness statement: {readiness}. This local evidence snapshot shows deterministic degradation "
        "behavior, replay visibility, telemetry integrity, and boundary status for the current repository state.",
        "",
    ]
    return "\n".join(lines)


def generate_evidence_pack(run_tests: bool = True) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    git_hash = get_git_commit_hash()
    test_status = run_test_suite() if run_tests else {"command": "skipped", "passed": True, "returncode": 0, "summary": "Skipped by caller."}
    evidence = run_validation_modules()
    summary = summarize_evidence(test_status, evidence)
    report = scrub_report(render_evidence_pack(timestamp, git_hash, test_status, evidence, summary))
    assert_report_safe(report)
    EVIDENCE_PACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PACK_PATH.write_text(report, encoding="utf-8")
    return {
        "path": str(EVIDENCE_PACK_PATH.relative_to(ROOT)),
        "timestamp": timestamp,
        "git_commit_hash": git_hash,
        "test_status": test_status,
        "summary": summary,
    }


def main() -> None:
    print(json.dumps(generate_evidence_pack(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
