"""Derivative steps.

Supported line shapes:
    f(x) = E            the function (order 0; also y = E)
    f'(x) = R           claims R is the derivative (also y' = R, dy/dx = R, f''(x) = R)
    \\frac{d}{dx}(E)     "differentiate E" (optionally followed by = R)
    = R  /  R           continues the previous line (same order)

A step is either a *differentiation* (compare with d/dx of the previous function)
or a *rewrite* (compare with the previous value). When the notation does not say
which one it is, both readings are tried and the step is accepted if either works.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from margin_verifier.check_expression import check_rewrite
from margin_verifier.equivalence import DIFFERENT, EQUAL, compare_expressions, evaluated
from margin_verifier.findings import Finding, invalid, show, term_diff, uncertain, valid
from margin_verifier.malrules import DERIVATIVE, RULES, SLIP, slip_variants
from margin_verifier.parsing import ParsedLine
from margin_verifier.verdict import Verdict


@dataclass(frozen=True)
class DerivativeLine:
    order: int | None  # derivative order stated by the notation; None if not stated
    value: sp.Expr | None  # the expression the line ends with (None for a bare d/dx(E))
    operand: sp.Expr | None  # E for lines written d/dx(E) ...
    rewrites: tuple[sp.Expr, ...]  # sides after the first value: 'f'(x) = A = B'


def read_derivative_line(line: ParsedLine) -> DerivativeLine | None:
    if line.is_list or any(op != "=" for op in line.branches[0].ops):
        return None
    sides = line.branches[0].sides
    if line.head is not None:
        return DerivativeLine(line.head.order, sides[0], None, sides[1:])
    first = sides[0]
    if isinstance(first, sp.Derivative):
        value = sides[1] if len(sides) > 1 else None
        return DerivativeLine(first.derivative_count, value, first.expr, sides[2:])
    return DerivativeLine(None, first, None, sides[1:])


def check_derivative_step(lines: list[ParsedLine | None], index: int, x: sp.Symbol) -> Finding:
    readings = [read_derivative_line(line) if line is not None else None for line in lines]
    prev, curr = readings[index - 1], readings[index]
    if prev is None or curr is None:
        return uncertain("unsupported_line_shape")
    finding = _main_step(prev, curr, _effective_order(readings, index - 1), x)
    if finding.verdict != Verdict.VALID:
        return finding
    chain = ((curr.value,) if curr.value is not None else ()) + curr.rewrites
    for before, after in zip(chain, chain[1:]):  # 'f'(x) = A = B' also claims A = B
        finding = check_rewrite(before, after)
        if finding.verdict != Verdict.VALID:
            return finding
    return finding


def _main_step(prev: DerivativeLine, curr: DerivativeLine, prev_order: int | None, x: sp.Symbol) -> Finding:
    if curr.operand is not None:  # 'd/dx(E) = R': the line says what it differentiates
        if curr.value is None:
            return uncertain("restates_the_problem")
        return check_differentiation(curr.operand, curr.value, x)
    if prev.operand is not None and prev.value is None:  # previous line was a bare d/dx(E)
        return check_differentiation(prev.operand, curr.value, x)
    if curr.order is not None and prev_order is not None:
        if curr.order == prev_order + 1:
            return check_differentiation(prev.value, curr.value, x)
        if curr.order == prev_order:
            return check_rewrite(prev.value, curr.value)
        return uncertain("unsupported_derivative_order")
    if curr.order is None and prev_order is not None and prev_order > 0:
        return check_rewrite(prev.value, curr.value)
    # Notation does not say: is this line the derivative, or a rewrite of the function?
    as_derivative = check_differentiation(prev.value, curr.value, x)
    as_rewrite = check_rewrite(prev.value, curr.value)
    for finding in (as_derivative, as_rewrite):
        if finding.verdict == Verdict.VALID:
            return finding
    if as_derivative.verdict == Verdict.INVALID and as_rewrite.verdict == Verdict.INVALID:
        return as_derivative
    return uncertain("ambiguous_step")


def check_differentiation(function: sp.Expr, claimed: sp.Expr, x: sp.Symbol) -> Finding:
    expected = sp.diff(evaluated(function), x)
    result = compare_expressions(expected, claimed)
    if result.status == EQUAL:
        return valid("correct_derivative", 0.95 if result.method == "numeric" else 0.99, method=result.method)
    if result.status != DIFFERENT:
        return uncertain(result.method)
    got = evaluated(claimed)
    return invalid(
        "wrong_derivative",
        0.9,
        lambda: diagnose_differentiation(function, claimed, expected, x),
        expected=show(expected),
        got=show(got),
        counterexample=result.counterexample,
        term_diff=term_diff(expected, got),
    )


def diagnose_differentiation(function: sp.Expr, claimed: sp.Expr, expected: sp.Expr, x: sp.Symbol) -> list[str]:
    matches: list[str] = []
    for rule in RULES:
        if rule.kind == DERIVATIVE:
            if any(_equal(candidate, claimed) for candidate in rule.candidates(function, x)):
                matches.append(rule.id)
        elif rule.kind == SLIP:
            if any(_equal(expected, variant) for variant in slip_variants(claimed)):
                matches.append(rule.id)
    return matches


def _effective_order(readings: list[DerivativeLine | None], index: int) -> int | None:
    """Derivative order of line `index` (0 = the function itself); None if unknown."""
    reading = readings[index]
    if reading is None:
        return None
    if reading.order is not None:
        return reading.order
    if index == 0:
        return 0  # a bare first line is the function to differentiate
    if index == 1 and readings[0] is not None and readings[0].order is None:
        return None  # two bare lines: line 1 may be the function or its derivative
    return _effective_order(readings, index - 1)  # '= ...' continues the previous line


def _equal(a: sp.Expr, b: sp.Expr) -> bool:
    return compare_expressions(a, b).status == EQUAL
