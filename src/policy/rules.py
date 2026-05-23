from dataclasses import dataclass

from .scopes import PolicyScope
from .severity import Severity


@dataclass(frozen=True)
class PolicyRule:
    name: str
    scope: PolicyScope
    severity: Severity
    threshold: float | bool
    description: str
