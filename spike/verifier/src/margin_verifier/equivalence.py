"""Are two expressions equal? Seeded random numeric testing, backed by SymPy.

Numeric testing is the workhorse: two different rational functions agree at a
random real point with probability ~0 (Schwartz-Zippel), so agreement at many
points is strong evidence of equality, and a disagreement at points where both
sides are defined is a concrete counterexample. SymPy's simplify is used as an
extra confirmation when the expression is small.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from functools import lru_cache

import mpmath
import sympy as sp
from sympy.core.function import AppliedUndef

EQUAL = "equal"
DIFFERENT = "different"
UNKNOWN = "unknown"

_SEED = 20260928
_POINTS = 12  # random points per comparison
_MIN_AGREEMENTS = 6  # points (where both sides are real and finite) needed to call "equal"
_MIN_DISAGREEMENTS = 2  # counterexamples needed to call "different"
_REL_TOL = 1e-9
_SIMPLIFY_MAX_OPS = 60  # skip sympy.simplify on bigger expressions (it can be slow)


@dataclass(frozen=True)
class Comparison:
    status: str  # EQUAL | DIFFERENT | UNKNOWN
    method: str  # how we know, e.g. "symbolic", "numeric", "positive_values_only"
    counterexample: dict[str, float] | None = None  # a point where the two differ


def evaluated(expr: sp.Expr) -> sp.Expr:
    """Evaluate an unevaluated parse tree (also performs any d/dx it contains)."""
    return expr.doit()


def compare_expressions(a: sp.Expr, b: sp.Expr) -> Comparison:
    """Decide whether a == b for all real values of their variables."""
    return _compare(evaluated(a), evaluated(b))


@lru_cache(maxsize=8192)
def _compare(a: sp.Expr, b: sp.Expr) -> Comparison:
    if a == b:
        return Comparison(EQUAL, "identical")
    if not (_numeric_friendly(a) and _numeric_friendly(b)):
        return Comparison(UNKNOWN, "unsupported_expression")
    symbols = tuple(sorted(a.free_symbols | b.free_symbols, key=lambda s: s.name))
    if not symbols:
        return _compare_numbers(a, b)
    tally = _numeric_tally(a, b, symbols, positive_only=False)
    if tally.disagreements >= _MIN_DISAGREEMENTS:
        if _has_branch_functions(a) or _has_branch_functions(b):
            # e.g. sqrt(x^2) vs x: wrong for x < 0 but routinely accepted in class.
            positive = _numeric_tally(a, b, symbols, positive_only=True)
            if positive.disagreements == 0 and positive.agreements >= _MIN_AGREEMENTS:
                return Comparison(UNKNOWN, "equal_only_for_positive_values")
        return Comparison(DIFFERENT, "numeric", tally.counterexample)
    if tally.disagreements == 0 and tally.agreements >= _MIN_AGREEMENTS:
        method = "symbolic+numeric" if _symbolically_zero(a - b) else "numeric"
        return Comparison(EQUAL, method)
    return Comparison(UNKNOWN, "not_enough_numeric_evidence")


def _compare_numbers(a: sp.Expr, b: sp.Expr) -> Comparison:
    """Two constants, e.g. sqrt(3^2 + 4^2) vs 7 (complex values allowed: sqrt(-400) != 20)."""
    try:
        va, vb = complex(sp.N(a, 30)), complex(sp.N(b, 30))
    except (TypeError, ValueError):
        return Comparison(UNKNOWN, "not_a_number")
    if not all(mpmath.isfinite(part) for part in (va.real, va.imag, vb.real, vb.imag)):
        return Comparison(UNKNOWN, "not_finite")
    if abs(va - vb) <= _REL_TOL * max(1, abs(va), abs(vb)):
        return Comparison(EQUAL, "numeric")
    return Comparison(DIFFERENT, "numeric", {"lhs_value": str(sp.N(a, 8)), "rhs_value": str(sp.N(b, 8))})


@dataclass(frozen=True)
class _Tally:
    agreements: int
    disagreements: int
    counterexample: dict[str, float] | None


def _numeric_tally(a: sp.Expr, b: sp.Expr, symbols: tuple[sp.Symbol, ...], positive_only: bool) -> _Tally:
    """Evaluate a and b at seeded random points; skip points where either is undefined."""
    f = _compiled(a, symbols)
    g = _compiled(b, symbols)
    agreements = disagreements = 0
    counterexample = None
    for point in _sample_points(len(symbols), positive_only):
        va, vb = _real_value(f, point), _real_value(g, point)
        if va is None or vb is None:
            continue  # outside the real domain of one side: not evidence either way
        scale = max(1, abs(va), abs(vb))
        if abs(va - vb) <= _REL_TOL * scale:
            agreements += 1
        else:
            disagreements += 1
            if counterexample is None:
                counterexample = {s.name: round(v, 6) for s, v in zip(symbols, point)}
                counterexample.update({"lhs_value": round(va, 6), "rhs_value": round(vb, 6)})
    return _Tally(agreements, disagreements, counterexample)


@lru_cache(maxsize=4)
def _sample_points(n_symbols: int, positive_only: bool) -> tuple[tuple[float, ...], ...]:
    """Deterministic 'random' points; avoid integers, where textbook singularities live."""
    rng = random.Random(_SEED + n_symbols * 10 + int(positive_only))
    low, high = (0.2, 4.0) if positive_only else (-4.0, 4.0)
    return tuple(tuple(rng.uniform(low, high) for _ in range(n_symbols)) for _ in range(_POINTS))


@lru_cache(maxsize=8192)
def _compiled(expr: sp.Expr, symbols: tuple[sp.Symbol, ...]):
    return sp.lambdify(symbols, expr, modules="mpmath")


def _real_value(func, point: tuple[float, ...]) -> float | None:
    """func(point) as a float, or None if undefined/non-real/infinite there."""
    with mpmath.workdps(30):
        try:
            value = mpmath.mpmathify(func(*[mpmath.mpf(v) for v in point]))
        except (ArithmeticError, ValueError, TypeError):
            return None
        real, imag = mpmath.re(value), mpmath.im(value)
        if not (mpmath.isfinite(real) and mpmath.isfinite(imag)):
            return None
        if abs(imag) > 1e-12 * (1 + abs(real)):
            return None  # e.g. sqrt of a negative number: not a real value
        return float(real)


def _numeric_friendly(expr: sp.Expr) -> bool:
    """We can only evaluate plain expressions (no f(x), no unevaluated d/dx, no oo)."""
    if expr.has(AppliedUndef, sp.Derivative, sp.Integral, sp.zoo, sp.oo, -sp.oo, sp.nan):
        return False
    return not isinstance(expr, (sp.logic.boolalg.Boolean, sp.Set))


def _has_branch_functions(expr: sp.Expr) -> bool:
    """Functions whose real-domain rules depend on sign: sqrt, |x|, log, fractional powers."""
    if expr.has(sp.Abs, sp.log):
        return True
    return any(p.exp.is_Rational and not p.exp.is_Integer for p in expr.atoms(sp.Pow))


def _symbolically_zero(difference: sp.Expr) -> bool:
    if sp.count_ops(difference) > _SIMPLIFY_MAX_OPS:
        return False
    try:
        return sp.simplify(difference) == 0
    except Exception:  # simplify can fail on odd inputs; numeric evidence still stands
        return False
