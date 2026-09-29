"""Generate labelled solutions: fully correct ones, and ones with exactly one mal-rule error.

Labels come from the construction plus *independent* ground-truth checks
(SymPy simplify/solveset on the generator's own trees), never from the verifier.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import sympy as sp

from margin_verifier.malrules import (
    DERIVATIVE,
    EXPRESSION,
    RELATION,
    RULES,
    SLIP,
    derivative_candidates,
    relation_candidates,
    slip_variants,
)
from margin_verifier.parsing import ParseError, parse_line
from margin_verifier.synth.lines import X, Line, ev, ordered
from margin_verifier.synth.templates import TEMPLATES, Template

_MAX_LINES = 9


@dataclass
class Solution:
    uid: str
    family: str
    template: str
    task: str
    lines: list[str]
    error_step: int | None = None  # line index of the injected error (transition error_step-1 -> error_step)
    error_rule: str | None = None
    notes: dict = field(default_factory=dict)


def solve(history: list[Line], solver) -> list[Line]:
    """Apply the first transform that fires, until none does (or the page is full)."""
    lines = list(history)
    seen = {line.render() for line in lines}
    while len(lines) < _MAX_LINES:
        for transform in solver:
            try:
                candidate = transform(lines[-1], lines)
            except ValueError:  # the renderer met something like sqrt(-7)
                candidate = None
            if candidate is None or not _renderable(candidate):
                continue  # e.g. a wrong line led to sqrt(-7): the student would stop here
            if candidate.render() not in seen:  # no loops
                lines.append(candidate)
                seen.add(candidate.render())
                break
        else:
            break
    return lines


def generate(index: int, seed: int = 7) -> Solution | None:
    """Solution number `index` of the dataset: even = correct, odd = one error.

    Deterministic: the same (index, seed) always gives the same solution."""
    rng = random.Random(seed * 1_000_003 + index)
    template = TEMPLATES[(index // 2) % len(TEMPLATES)]
    for _attempt in range(20):
        lines = solve([template.start(rng)], template.solver)
        if len(lines) < 2 or not _all_steps_correct(lines):
            continue
        if index % 2 == 0:
            solution = _package(index, template, lines)
        else:
            injected = _inject_somewhere(template, lines, rng)
            if injected is None:
                continue
            wrong_lines, step, rule_id = injected
            solution = _package(index, template, wrong_lines, step, rule_id)
        if solution is not None:
            return solution
    return None


def _inject_somewhere(template: Template, lines: list[Line], rng: random.Random):
    options = [(step, rule_id) for step in range(1, len(lines)) for rule_id in template.rules]
    rng.shuffle(options)
    for step, rule_id in options:
        wrong = inject(rule_id, lines[step - 1], lines[step], rng)
        if wrong is None:
            continue
        continued = solve(lines[:step] + [wrong], template.solver)
        return continued, step, rule_id
    return None


def _package(index: int, template: Template, lines: list[Line], step: int | None = None,
             rule_id: str | None = None) -> Solution | None:
    rendered = [line.render() for line in lines]
    if not all(_renders_faithfully(line, text) for line, text in zip(lines, rendered)):
        return None  # renderer/parser disagreement: drop rather than risk a wrong label
    return Solution(f"{template.name}-{index}", template.family, template.name, template.task,
                    rendered, step, rule_id)


# ------------------------------------------------------------------------------------ injection


def inject(rule_id: str, prev: Line, correct_next: Line, rng: random.Random) -> Line | None:
    """A wrong next line produced by mal-rule `rule_id`, or None if it does not apply here."""
    candidates: list[Line] = []
    for rule in RULES:
        if rule.id == rule_id:
            candidates.extend(_candidate_lines(rule, prev, correct_next))
    rng.shuffle(candidates)
    for candidate in candidates:
        # Half the time write it with the arithmetic done, like a student combining as they go.
        preferred = _tidy(candidate) if rng.random() < 0.5 else candidate
        for option in (preferred, candidate):
            if _renderable(option) and _is_wrong(prev, option, correct_next):
                return option
    return None


def _renderable(line: Line) -> bool:
    try:
        line.render()
    except ValueError:
        return False
    return True


def _candidate_lines(rule, prev: Line, correct_next: Line) -> list[Line]:
    if rule.kind == SLIP:
        return _slipped(correct_next)
    if prev.kind == "relation" and rule.kind in (RELATION, EXPRESSION):
        return [Line("relation", branches=b) for b in relation_candidates(rule, prev.branches, X)]
    if prev.kind in ("expr", "derivative") and rule.kind == EXPRESSION and correct_next.kind == prev.kind:
        return [Line(prev.kind, expr=c, continuation=correct_next.continuation) for c in rule.candidates(prev.expr)]
    if prev.kind in ("function", "operator") and rule.kind == DERIVATIVE:
        derivatives = derivative_candidates(rule, prev.expr, X)
        return [Line("derivative", expr=ordered(d), continuation=correct_next.continuation) for d in derivatives]
    return []


def _slipped(line: Line) -> list[Line]:
    """One number of the correct next line changed a little."""
    if line.kind != "relation":
        return [Line(line.kind, expr=v, continuation=line.continuation) for v in slip_variants(line.expr)]
    out = []
    for i, (lhs, op, rhs) in enumerate(line.branches):
        for new_lhs in slip_variants(lhs):
            out.append(Line("relation", branches=line.branches[:i] + ((new_lhs, op, rhs),) + line.branches[i + 1 :]))
        for new_rhs in slip_variants(rhs):
            out.append(Line("relation", branches=line.branches[:i] + ((lhs, op, new_rhs),) + line.branches[i + 1 :]))
    return out


def _tidy(line: Line) -> Line:
    """The same line with the arithmetic done (students often combine as they go)."""
    if line.kind == "relation":
        return Line("relation", branches=tuple((ordered(ev(l)), op, ordered(ev(r))) for l, op, r in line.branches))
    return Line(line.kind, expr=ordered(ev(line.expr)), continuation=line.continuation)


# --------------------------------------------------------------------------- ground-truth checks


def _is_wrong(prev: Line, candidate: Line, correct_next: Line) -> bool:
    """True only if we can *prove* the candidate is not a correct next line."""
    if candidate.kind == "relation":
        before, after, right = _solutions(prev), _solutions(candidate), _solutions(correct_next)
        if before is None or after is None or right is None:
            return False
        return after != before and after != right
    if candidate.kind == "derivative" and prev.kind in ("function", "operator"):
        return _differs(sp.diff(ev(prev.expr), X), ev(candidate.expr))
    return _differs(ev(prev.expr), ev(candidate.expr))


def _differs(a: sp.Expr, b: sp.Expr) -> bool:
    difference = sp.simplify(a - b)
    if difference == 0:
        return False
    return difference.equals(0) is False


def _solutions(line: Line) -> sp.Set | None:
    total = sp.S.EmptySet
    for lhs, op, rhs in line.branches:
        relation = {"=": sp.Eq, "<": sp.Lt, "<=": sp.Le, ">": sp.Gt, ">=": sp.Ge}[op](ev(lhs), ev(rhs))
        try:
            solutions = sp.solveset(relation, X, domain=sp.S.Reals)
        except Exception:
            return None
        if isinstance(solutions, sp.ConditionSet):
            return None
        total = sp.Union(total, solutions)
    return total


def _all_steps_correct(lines: list[Line]) -> bool:
    """Sanity check of the generator itself: every step of a correct solution is sound."""
    for prev, curr in zip(lines, lines[1:]):
        if curr.kind == "relation":
            before, after = _solutions(prev), _solutions(curr)
            if before is None or after is None:
                return False
            if before != after and not (sp.Complement(before, after) == sp.S.EmptySet or _rejects_extraneous(lines, prev, curr)):
                return False  # allowed: equal sets, implication (squaring), rejecting extraneous roots
        elif curr.kind == "derivative" and prev.kind in ("function", "operator"):
            if _differs(sp.diff(ev(prev.expr), X), ev(curr.expr)):
                return False
        elif _differs(ev(prev.expr), ev(curr.expr)):
            return False
    return True


def _rejects_extraneous(lines: list[Line], prev: Line, curr: Line) -> bool:
    original = _solutions(lines[0])
    after = _solutions(curr)
    return original is not None and after == original


def _renders_faithfully(line: Line, text: str) -> bool:
    """Parse the rendered LaTeX back and check it means the same thing."""
    try:
        parsed = parse_line(text, allow_heads=line.kind in ("function", "derivative"))
    except ParseError:
        return False
    if line.kind == "relation":
        if len(parsed.branches) != len(line.branches):
            return False
        for (lhs, op, rhs), relation in zip(line.branches, parsed.branches):
            if relation.ops != (op,):
                return False
            if _differs(ev(lhs) - ev(rhs), ev(relation.sides[0]) - ev(relation.sides[1])):
                return False
        return True
    side = parsed.branches[0].sides[-1]
    if line.kind == "operator":
        return not _differs(sp.diff(ev(line.expr), X), ev(side))
    return not _differs(ev(line.expr), ev(side))
