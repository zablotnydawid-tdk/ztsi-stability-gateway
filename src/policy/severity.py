from enum import Enum


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    LOCKDOWN = "LOCKDOWN"


SEVERITY_ORDER = {
    Severity.INFO: 0,
    Severity.WARNING: 1,
    Severity.CRITICAL: 2,
    Severity.LOCKDOWN: 3,
}


def max_severity(severities: list[Severity]) -> Severity:
    if not severities:
        return Severity.INFO
    return max(severities, key=lambda severity: SEVERITY_ORDER[severity])
