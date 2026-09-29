"""Equation and inequality steps: compare the real solution sets of the two lines."""

from __future__ import annotations

import sympy as sp

from margin_verifier.findings import Finding, invalid, show, uncertain, valid
from margin_verifier.malrules import EXPRESSION, RELATION, RULES, SLIP, relation_candidates, slip_variants
from margin_verifier.parsing import ParsedLine
from margin_verifier.solutions import (
    Branch,
    evaluate_branches,
    is_solved_form,
    real_solutions,
    relate_sets,
    residuals_proportional,
    satisfies,
)


def check_relation_step(lines: list[ParsedLine | None], index: int, x: sp.Symbol) -> Finding:
    """lines[index - 1] -> lines[index]; unreadable lines are None (never the two checked here)."""
    prev, curr = lines[index - 1], lines[index]
    if not (_is_relation(prev) and _is_relation(curr)):
        return uncertain("unsupported_line_shape")
    before_branches, after_branches = evaluate_branches(prev.branches), evaluate_branches(curr.branches)
    inequality = any(op != "=" for _, op, _ in before_branches + after_branches)

    if not inequality and residuals_proportional(before_branches, after_branches, x):
        return valid("same_equation_rescaled", 0.99)
    before, after = real_solutions(before_branches, x), real_solutions(after_branches, x)
    if before is None or after is None:
        return uncertain("could_not_solve")
    change = relate_sets(before, after)
    details = {"solutions_before": show(before), "solutions_after": show(after)}

    def diagnose() -> list[str]:
        return diagnose_relation(surface_branches(prev), surface_branches(curr), x)

    if change.kind == "equal":
        return valid("same_solutions", 0.98, **details)
    if change.kind == "gained" and not inequality:
        # Squaring both sides or multiplying by an x-expression may add roots: that is
        # sound (they get checked later). Only a final list of values from a plain
        # polynomial equation must not contain values that do not solve it.
        if not (is_solved_form(after_branches, x) and _is_polynomial(before_branches, x)):
            return valid("implication_may_add_roots", 0.8, extra_candidates=_texts(change.gained), **details)
        return invalid("extra_solutions", 0.9, diagnose, extra=_texts(change.gained), **details)
    if change.kind == "lost" and not inequality and change.finite:
        # Dropping a root is fine if it was extraneous: it fails an earlier line.
        checks = [_fails_an_earlier_line(lines, index, v, x) for v in change.lost]
        if all(check is True for check in checks):
            return valid("extraneous_root_rejected", 0.9, rejected=_texts(change.lost), **details)
        if any(check is None for check in checks):
            return uncertain("cannot_check_dropped_root", lost=_texts(change.lost), **details)
    reason = {"lost": "lost_solutions", "gained": "extra_solutions", "different": "different_solutions"}
    return invalid(
        reason[change.kind], 0.9, diagnose, lost=_texts(change.lost), extra=_texts(change.gained), **details
    )


def surface_branches(line: ParsedLine) -> tuple[tuple[sp.Expr, str, sp.Expr], ...]:
    return tuple((r.sides[0], r.ops[0], r.sides[1]) for r in line.branches)


def diagnose_relation(before, after, x: sp.Symbol) -> list[str]:
    """Ids of mal-rules whose output matches the student's line."""
    target = evaluate_surface(after)
    previous = evaluate_surface(before)
    matches: list[str] = []
    for rule in RULES:
        if rule.kind in (RELATION, EXPRESSION):
            candidates = relation_candidates(rule, before, x)
            if any(_reproduces(evaluate_surface(c), target, x) for c in candidates):
                matches.append(rule.id)
        elif rule.kind == SLIP:
            if any(same_solutions(previous, evaluate_surface(v), x) for v in _slip_branches(after)):
                matches.append(rule.id)
    return list(dict.fromkeys(matches))


def _reproduces(candidate: tuple[Branch, ...], student: tuple[Branch, ...], x: sp.Symbol) -> bool:
    """Same equation up to a constant factor when both are single polynomial equations
    (so a wrong factoring (x-3)^2 = 0 is not blamed on 'dividing by x+3', which gives the
    same roots); otherwise the same solution set (e.g. the student also solved it)."""
    if _single_polynomial_equation(candidate, x) and _single_polynomial_equation(student, x):
        return residuals_proportional(candidate, student, x)
    return same_solutions(candidate, student, x)


def _single_polynomial_equation(branches: tuple[Branch, ...], x: sp.Symbol) -> bool:
    return len(branches) == 1 and branches[0][1] == "=" and _is_polynomial(branches, x)


def same_solutions(a: tuple[Branch, ...], b: tuple[Branch, ...], x: sp.Symbol) -> bool:
    if residuals_proportional(a, b, x):
        return True
    sa, sb = real_solutions(a, x), real_solutions(b, x)
    return sa is not None and sb is not None and relate_sets(sa, sb).kind == "equal"


def evaluate_surface(branches) -> tuple[Branch, ...]:
    return tuple((lhs.doit(), op, rhs.doit()) for lhs, op, rhs in branches)


def _slip_branches(branches):
    """The student's line with one number changed a little (see malrules.slip_variants)."""
    for index, (lhs, op, rhs) in enumerate(branches):
        for new_lhs in slip_variants(lhs):
            yield branches[:index] + ((new_lhs, op, rhs),) + branches[index + 1 :]
        for new_rhs in slip_variants(rhs):
            yield branches[:index] + ((lhs, op, new_rhs),) + branches[index + 1 :]


def _fails_an_earlier_line(lines: list[ParsedLine | None], index: int, value: sp.Expr, x: sp.Symbol) -> bool | None:
    """True if `value` does not solve some earlier line, i.e. it was an extraneous root
    introduced by squaring / clearing denominators. False if it solves all of them.
    None if we cannot tell because an earlier line is unreadable or looks misread."""
    unsure = False
    for line in lines[: index - 1]:
        if line is None or not _is_relation(line) or not _trustworthy(line, x):
            unsure = True
            continue
        result = satisfies(evaluate_branches(line.branches), x, value)
        if result is False:
            return True
        if result is None:
            unsure = True
    return None if unsure else False


def _trustworthy(line: ParsedLine, x: sp.Symbol) -> bool:
    """No OCR red flags and no letters other than the variable."""
    letters = {s for r in line.branches for side in r.sides for s in side.free_symbols}
    return not line.flags and letters <= {x}


def _is_relation(line: ParsedLine) -> bool:
    return all(len(r.sides) == 2 for r in line.branches)


def _is_polynomial(branches: tuple[Branch, ...], x: sp.Symbol) -> bool:
    return all((lhs - rhs).is_polynomial(x) for lhs, _, rhs in branches)


def _texts(values) -> list[str]:
    return [show(v) for v in values]
