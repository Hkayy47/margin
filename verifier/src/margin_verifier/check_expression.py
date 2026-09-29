"""Expression steps (simplify / expand / factor / combine fractions / exponent rules)."""

from __future__ import annotations

import sympy as sp

from margin_verifier.equivalence import DIFFERENT, EQUAL, compare_expressions, evaluated
from margin_verifier.findings import Finding, invalid, show, term_diff, uncertain, valid
from margin_verifier.malrules import EXPRESSION, RULES, SLIP, slip_variants
from margin_verifier.parsing import ParsedLine
from margin_verifier.verdict import Verdict


def check_expression_step(prev: ParsedLine, curr: ParsedLine) -> Finding:
    """prev's (last) expression must equal every expression written on curr."""
    if not (_is_equality_chain(prev) and _is_equality_chain(curr)):
        return uncertain("unsupported_line_shape")
    sides = (prev.branches[0].sides[-1],) + curr.branches[0].sides
    finding = uncertain("nothing_to_compare")
    for before, after in zip(sides, sides[1:]):
        finding = check_rewrite(before, after)
        if finding.verdict != Verdict.VALID:
            return finding
    return finding


def check_rewrite(before: sp.Expr, after: sp.Expr) -> Finding:
    """One rewriting step before -> after, with mal-rule diagnosis when wrong."""
    result = compare_expressions(before, after)
    if result.status == EQUAL:
        confidence = 0.95 if result.method == "numeric" else 0.99
        return valid("equivalent", confidence, method=result.method)
    if result.status != DIFFERENT:
        return uncertain(result.method)
    expected, got = evaluated(before), evaluated(after)
    return invalid(
        "not_equivalent",
        0.9,
        lambda: diagnose_rewrite(before, after),
        expected=show(expected),
        got=show(got),
        counterexample=result.counterexample,
        term_diff=term_diff(expected, got),
    )


def diagnose_rewrite(before: sp.Expr, after: sp.Expr) -> list[str]:
    """Ids of mal-rules that turn `before` into something equal to `after`."""
    matches: list[str] = []
    for rule in RULES:
        if rule.kind == EXPRESSION:
            if any(_equal(candidate, after) for candidate in rule.candidates(before)):
                matches.append(rule.id)
        elif rule.kind == SLIP:
            if any(_equal(before, variant) for variant in slip_variants(after)):
                matches.append(rule.id)
    return matches


def _equal(a: sp.Expr, b: sp.Expr) -> bool:
    return compare_expressions(a, b).status == EQUAL


def _is_equality_chain(line: ParsedLine) -> bool:
    return len(line.branches) == 1 and all(op == "=" for op in line.branches[0].ops)
