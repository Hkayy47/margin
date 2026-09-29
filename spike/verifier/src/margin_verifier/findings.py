"""Internal result of checking one step, before OCR guarding and packaging."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import sympy as sp

from margin_verifier.verdict import Verdict


@dataclass(frozen=True)
class Finding:
    verdict: Verdict
    reason: str  # short machine-readable code, e.g. "counterexample", "lost_solutions"
    confidence: float
    details: dict[str, Any] = field(default_factory=dict)
    # Only for INVALID: returns the ids of mal-rules that reproduce the student's line.
    diagnose: Callable[[], list[str]] | None = None


def valid(reason: str, confidence: float, **details: Any) -> Finding:
    return Finding(Verdict.VALID, reason, confidence, details)


def uncertain(reason: str, **details: Any) -> Finding:
    return Finding(Verdict.UNCERTAIN, reason, 0.0, details)


def invalid(reason: str, confidence: float, diagnose: Callable[[], list[str]], **details: Any) -> Finding:
    return Finding(Verdict.INVALID, reason, confidence, details, diagnose)


def show(expr: sp.Basic) -> str:
    """Compact text for explanations (plain SymPy syntax, easy to log and parse)."""
    return sp.sstr(expr)


def term_diff(expected: sp.Expr, got: sp.Expr) -> dict[str, list[str]] | None:
    """Which expanded terms are missing / unexpected (polynomials only).

    e.g. expected (x+3)^2, got x^2 + 9  ->  missing ['6*x']."""
    symbols = sorted(expected.free_symbols | got.free_symbols, key=lambda s: s.name)
    if not symbols or not (expected.is_polynomial(*symbols) and got.is_polynomial(*symbols)):
        return None
    want = set(sp.Add.make_args(sp.expand(expected)))
    have = set(sp.Add.make_args(sp.expand(got)))
    return {
        "missing": sorted(show(t) for t in want - have),
        "unexpected": sorted(show(t) for t in have - want),
    }
