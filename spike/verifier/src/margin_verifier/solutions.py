"""Real solution sets of (in)equations, and how two solution sets relate.

A step between two equations is judged by what it does to the set of real
solutions: same set = valid; lost solutions (divided by x, forgot +/-) or a
different set = error; extra solutions after squaring = sound but needs a check.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from margin_verifier.equivalence import evaluated

Branch = tuple[sp.Expr, str, sp.Expr]  # (lhs, op, rhs), evaluated

_OPS = {"=": sp.Eq, "<": sp.Lt, "<=": sp.Le, ">": sp.Gt, ">=": sp.Ge, "!=": sp.Ne}
_MAX_OPS = 80  # bigger equations are out of scope for v1 (solveset can get slow)
_MAX_DEGREE = 6  # polynomial degree we are willing to solve
_SOLVE_SECONDS = 2.0  # time budget for one solveset call
_TOL = 1e-9


@dataclass(frozen=True)
class SetRelation:
    kind: str  # "equal" | "lost" | "gained" | "different"
    lost: tuple[sp.Basic, ...] = ()  # solutions of the previous line missing now
    gained: tuple[sp.Basic, ...] = ()  # solutions that are new in this line
    finite: bool = True  # False when lost/gained hold intervals rather than single values


def evaluate_branches(branches) -> tuple[Branch, ...]:
    """(lhs, op, rhs) triples from parsed relations with exactly two sides."""
    return tuple((evaluated(r.sides[0]), r.ops[0], evaluated(r.sides[1])) for r in branches)


def real_solutions(branches: tuple[Branch, ...], variable: sp.Symbol) -> sp.Set | None:
    """Union of the real solution sets of 'or'-joined branches; None if unknown."""
    total: sp.Set = sp.S.EmptySet
    for branch in branches:
        solutions = _branch_solutions(branch, variable)
        if solutions is None:
            return None
        total = sp.Union(total, solutions)
    return total


@lru_cache(maxsize=4096)
def _branch_solutions(branch: Branch, variable: sp.Symbol) -> sp.Set | None:
    lhs, op, rhs = branch
    residual = lhs - rhs
    if residual.free_symbols - {variable}:
        return None  # parameters / other letters: out of scope for v1
    if sp.count_ops(residual) > _MAX_OPS:
        return None
    if op == "=":
        roots = _rational_equation_roots(residual, variable)
        if roots is not None:
            return roots
    relation = _OPS[op](lhs, rhs)
    if relation is sp.true:
        return sp.S.Reals
    if relation is sp.false:
        return sp.S.EmptySet
    result = _solveset_within_budget(relation, variable)
    return result if result is not None and _is_explicit(result) else None


def _solveset_within_budget(relation: sp.Basic, variable: sp.Symbol) -> sp.Set | None:
    """solveset, or None if it fails or runs past the time budget.

    Some radical equations keep solveset busy for minutes. We cannot kill a thread in
    Python, so a timed-out solve keeps running in a daemon thread and its result is
    ignored (SymPy's global flags are thread-local, so it cannot disturb us)."""
    outcome: list[sp.Set | None] = []

    def solve() -> None:
        try:
            outcome.append(sp.solveset(relation, variable, domain=sp.S.Reals))
        except Exception:  # solveset raises assorted errors on inputs it cannot handle
            outcome.append(None)

    worker = threading.Thread(target=solve, daemon=True)
    worker.start()
    worker.join(_SOLVE_SECONDS)
    return outcome[0] if outcome else None


def _rational_equation_roots(residual: sp.Expr, x: sp.Symbol) -> sp.Set | None:
    """Real solutions of P(x)/Q(x) = 0 via polynomial root isolation (fast and exact:
    cubics come back as CRootOf instead of slow Cardano radicals). None if not rational."""
    if residual.has(sp.I):
        return None  # not real-valued maths (often a misread 'I' for '1')
    numerator, denominator = sp.fraction(sp.together(residual))
    try:
        top, bottom = sp.Poly(numerator, x), sp.Poly(denominator, x)
        if top.degree() > _MAX_DEGREE or bottom.degree() > _MAX_DEGREE:
            return None
        poles = bottom.real_roots() if bottom.degree() > 0 else []
        roots = [] if top.is_zero else top.real_roots()
    except (sp.PolynomialError, NotImplementedError):
        return None  # radicals, trig, irrational coefficients...: let solveset handle it
    if top.is_zero:
        return sp.S.Reals if not poles else sp.Complement(sp.S.Reals, sp.FiniteSet(*poles))
    return sp.FiniteSet(*[r for r in dict.fromkeys(roots) if not _contains(poles, r)])


def _is_explicit(result: sp.Set) -> bool:
    """Only trust answers made of plain numbers and intervals (no ConditionSet...)."""
    if isinstance(result, sp.FiniteSet):
        return all(value.is_number and value.is_real for value in result)
    if isinstance(result, (sp.Interval, sp.sets.sets.EmptySet)) or result == sp.S.Reals:
        return True
    if isinstance(result, (sp.Union, sp.Complement)):
        return all(_is_explicit(part) for part in result.args)
    return False


def relate_sets(previous: sp.Set, current: sp.Set) -> SetRelation:
    """How the current line's solution set compares to the previous line's."""
    if _finite_or_empty(previous) and _finite_or_empty(current):
        return _relate_finite(_values(previous), _values(current))
    lost = sp.Complement(previous, current)
    gained = sp.Complement(current, previous)
    lost_part = () if _is_empty(lost) else (lost,)
    gained_part = () if _is_empty(gained) else (gained,)
    if not lost_part and not gained_part:
        return SetRelation("equal")
    if not gained_part:
        return SetRelation("lost", lost=lost_part, finite=False)
    if not lost_part:
        return SetRelation("gained", gained=gained_part, finite=False)
    return SetRelation("different", lost=lost_part, gained=gained_part, finite=False)


def _relate_finite(previous: list[sp.Expr], current: list[sp.Expr]) -> SetRelation:
    lost = tuple(v for v in previous if not _contains(current, v))
    gained = tuple(v for v in current if not _contains(previous, v))
    if not lost and not gained:
        return SetRelation("equal")
    if lost and gained:
        return SetRelation("different", lost=lost, gained=gained)
    return SetRelation("lost", lost=lost) if lost else SetRelation("gained", gained=gained)


def _contains(values: list[sp.Expr], target: sp.Expr) -> bool:
    """Numeric membership test (solveset may write the same root in two forms)."""
    t = _as_number(target)
    return any(abs(_as_number(v) - t) <= _TOL * max(1, abs(t)) for v in values)


def _as_number(value: sp.Expr) -> complex:
    return complex(sp.N(value, 30))


def _values(solutions: sp.Set) -> list[sp.Expr]:
    return [] if _is_empty(solutions) else list(solutions)


def _is_empty(solutions: sp.Set) -> bool:
    return solutions == sp.S.EmptySet


def _finite_or_empty(solutions: sp.Set) -> bool:
    return isinstance(solutions, sp.FiniteSet) or _is_empty(solutions)


def satisfies(branches: tuple[Branch, ...], variable: sp.Symbol, value: sp.Expr) -> bool | None:
    """Does `value` satisfy at least one branch? None if we cannot tell."""
    solutions = real_solutions(branches, variable)
    if solutions is None:
        return None
    if isinstance(solutions, sp.FiniteSet) or _is_empty(solutions):
        return _contains(_values(solutions), value)
    try:
        return bool(solutions.contains(value))
    except TypeError:
        return None


def is_solved_form(branches: tuple[Branch, ...], variable: sp.Symbol) -> bool:
    """'x = 3' or 'x = 2 or x = -2': variable alone on the left, a number on the right."""
    return all(
        op == "=" and lhs == variable and not rhs.free_symbols for lhs, op, rhs in branches
    )


def residuals_proportional(previous: tuple[Branch, ...], current: tuple[Branch, ...], variable: sp.Symbol) -> bool:
    """Fast path: single polynomial equations whose (lhs - rhs) differ by a nonzero constant
    factor have the same roots (covers moving terms, expanding, dividing by 2...)."""
    if len(previous) != 1 or len(current) != 1:
        return False
    (l1, op1, r1), (l2, op2, r2) = previous[0], current[0]
    if op1 != "=" or op2 != "=":
        return False
    p, q = l1 - r1, l2 - r2
    if not (p.is_polynomial(variable) and q.is_polynomial(variable)):
        return False
    if (p.free_symbols | q.free_symbols) - {variable}:
        return False
    if sp.expand(p) == 0 or sp.expand(q) == 0:
        return False
    ratio = sp.cancel(q / p)
    return ratio.is_number and ratio != 0
