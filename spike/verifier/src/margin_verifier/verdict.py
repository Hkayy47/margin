"""Public result types returned by `check_solution`."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    VALID = "valid"
    INVALID = "invalid"  # only when we are confident: the app speaks up
    UNCERTAIN = "uncertain"  # we could not decide: the app stays silent


@dataclass(frozen=True)
class StepVerdict:
    """Verdict for the transition from line `step - 1` to line `step`."""

    step: int
    verdict: Verdict
    error_type: str | None  # mal-rule id or "unclassified" when invalid, else None
    confidence: float  # heuristic evidence strength in [0, 1]; NOT a calibrated probability
    explanation: dict[str, Any] = field(default_factory=dict)  # machine-readable details
    hint: str | None = None  # a nudge for the student, never the answer (invalid only)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["verdict"] = self.verdict.value
        return data
