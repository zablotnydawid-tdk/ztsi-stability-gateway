import re
import unittest
from pathlib import Path

from validation.evidence.generate_evidence_pack import EVIDENCE_PACK_PATH, generate_evidence_pack


class ValidationEvidencePackTests(unittest.TestCase):
    def test_generator_creates_required_report_sections_without_private_exposure(self) -> None:
        result = generate_evidence_pack(run_tests=False)
        self.assertEqual(result["path"], "validation/evidence/EVIDENCE_PACK.md")
        self.assertTrue(EVIDENCE_PACK_PATH.exists())

        report = EVIDENCE_PACK_PATH.read_text(encoding="utf-8")
        required_sections = [
            "# Governance Validation Evidence Pack",
            "## Timestamp",
            "## Git Commit Hash",
            "## Test Status",
            "## Validation Modules Executed",
            "## Pass/Fail Summary",
            "## Detected Degradation Cases",
            "## Policy Mismatches",
            "## Boundary Findings",
            "## Telemetry Integrity Status",
            "## Final Governance Readiness Statement",
        ]
        for section in required_sections:
            self.assertIn(section, report)

        forbidden_patterns = [
            r"api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]",
            r"secret\s*[:=]\s*['\"][^'\"]+['\"]",
            r"password\s*[:=]\s*['\"][^'\"]+['\"]",
            r"token\s*[:=]\s*['\"][^'\"]+['\"]",
            r"BEGIN (RSA|OPENSSH|PRIVATE) KEY",
            r"gh[pousr]_[A-Za-z0-9_]+",
            r"sk-[A-Za-z0-9]{16,}",
            r"/mnt/c/(?!\[)[^\s)]+",
            r"C:\\Users\\[^\s)]+",
            r"Users[/\\][^\s)]+",
        ]
        for pattern in forbidden_patterns:
            self.assertIsNone(re.search(pattern, report, flags=re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
