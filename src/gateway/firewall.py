from .governance import APPROVED, REJECTED

ALLOWED = "ALLOWED"
BLOCKED = "BLOCKED"


def apply_firewall(governance_status: str) -> str:
    if governance_status == APPROVED:
        return ALLOWED
    if governance_status == REJECTED:
        return BLOCKED
    return BLOCKED
