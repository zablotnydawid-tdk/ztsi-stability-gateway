from dataclasses import dataclass
from enum import Enum


class ProjectionMode(str, Enum):
    DISABLED = "DISABLED"
    CONSERVATIVE = "CONSERVATIVE"
    AGGRESSIVE = "AGGRESSIVE"


@dataclass(frozen=True)
class ProjectionPolicy:
    mode: ProjectionMode = ProjectionMode.CONSERVATIVE
    max_output_chars: int = 1200
    max_corrections: int = 6

    @property
    def enabled(self) -> bool:
        return self.mode != ProjectionMode.DISABLED
