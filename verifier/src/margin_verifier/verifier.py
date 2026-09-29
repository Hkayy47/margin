"""Public entry point: check a handwritten solution step by step.

    check_solution(["2x + 3 = 7", "2x = 10", "x = 5"], task="solve for x")

returns one StepVerdict per transition (line i-1 -> line i). The product rule
is "never flag a correct step": INVALID is only returned when the maths says
so *and* the OCR text looks clean; everything doubtful becomes UNCERTAIN.
"""

from __future__ import annotations

import re

import sympy as sp

from margin_verifier.check_derivative import check_derivative_step
from margin_verifier.check_expression import check_expression_step
from margin_verifier.check_relation import check_relation_step
from margin_verifier.findings import Finding
from margin_verifier.malrules import hint_for
from margin_verifier.misreads import alternative_readings
from margin_verifier.parsing import ParsedLine, ParseError, parse_line
from margin_verifier.verdict import StepVerdict, Verdict

EXPRESSION_MODE = "expression"
EQUATION_MODE = "equation"  # equations and inequalities
DERIVATIVE_MODE = "derivative"

# Letters that OCR produces from digits: l/I->1, O/o->0, S->5, Z->2, B->8, g/q->9.
_CONFUSABLE_LETTERS = frozenset("lIOoSZBgq")
_UNCLASSIFIED_HINT = "Something in this step does not follow from the line before. Check it again."
_STRONG = 0.95  # confidence of a VALID finding that is equivalence, not just implication


def check_solution(
    lines: list[str],
    task: str | None = None,
    *,
    strict_ocr: bool = False,
    confirm_with_next_line: bool = False,
) -> list[StepVerdict]:
    """Verdicts for each transition line[i-1] -> line[i] (so len(lines) - 1 of them).

    strict_ocr: also abstain when a one-character OCR confusion (similar digit,
        dropped minus, dropped exponent) would make the step correct. Safer when the
        OCR gives no confidence scores, but it hides real sign errors and slips.
    confirm_with_next_line: use the line *after* a suspicious line as a witness
        (see _suppress_isolated_misreads). The app then has to wait for that line
        before speaking up."""
    mode = detect_mode(task, lines)
    parsed: list[ParsedLine | None] = []
    errors: list[str | None] = []
    for line in lines:
        try:
            parsed.append(parse_line(line, allow_heads=(mode == DERIVATIVE_MODE)))
            errors.append(None)
        except ParseError as error:
            parsed.append(None)
            errors.append(str(error))
    x = detect_variable(task, parsed)
    results = [_safely_check_step(parsed, errors, index, mode, x, strict_ocr) for index in range(1, len(lines))]
    if confirm_with_next_line:
        results = _suppress_isolated_misreads(results, parsed, mode, x)
    return results


def _suppress_isolated_misreads(
    results: list[StepVerdict], parsed: list[ParsedLine | None], mode: str, x: sp.Symbol
) -> list[StepVerdict]:
    """A correct student whose line k is misread gets two alarms in a row (into and out
    of line k), yet going straight from line k-1 to line k+1 is fine. A real mistake is
    followed by consistent work, so it causes one alarm. Two alarms that vanish when
    line k is skipped therefore point at the OCR, not the student."""
    adjusted = list(results)
    for into, out_of in zip(results, results[1:]):
        if into.verdict != Verdict.INVALID or out_of.verdict != Verdict.INVALID:
            continue
        line = into.step  # the line both alarms have in common
        if parsed[line - 1] is None or parsed[line + 1] is None:
            continue
        skipped = parsed[:line] + parsed[line + 1 :]
        try:
            skip_is_valid = _run_checker(skipped, line, mode, x).verdict == Verdict.VALID
        except Exception:  # noqa: BLE001 - same last-resort rule as _safely_check_step
            skip_is_valid = False
        if skip_is_valid:
            for verdict in (into, out_of):
                explanation = {**verdict.explanation, "reason": "isolated_misread", "suspect_line": line}
                explanation["suspected"] = {"error_type": verdict.error_type}
                adjusted[verdict.step - 1] = StepVerdict(verdict.step, Verdict.UNCERTAIN, None, 0.0, explanation)
    return adjusted


def detect_mode(task: str | None, lines: list[str]) -> str:
    text = (task or "").lower()
    if any(word in text for word in ("differentiat", "derivative", "d/dx")):
        return DERIVATIVE_MODE
    if any(word in text for word in ("solve", "inequalit", "equation")):
        return EQUATION_MODE
    if any(word in text for word in ("simplify", "expand", "factor", "evaluate", "combine", "compute")):
        return EXPRESSION_MODE
    joined = " ".join(lines)
    if re.search(r"\\frac\s*\{\s*d", joined) or re.search(r"[a-zA-Z]\s*'", joined):
        return DERIVATIVE_MODE
    first = lines[0] if lines else ""
    if re.search(r"=|<|>|\\leq?|\\geq?|\\neq?|\\lt|\\gt|≤|≥", first):
        return EQUATION_MODE
    return EXPRESSION_MODE


def detect_variable(task: str | None, parsed: list[ParsedLine | None]) -> sp.Symbol:
    match = re.search(r"(?:\bfor|respect to|in terms of)\s+\$?([a-zA-Z])\b", task or "")
    if match:
        return sp.Symbol(match.group(1))
    for line in parsed:
        if line is None:
            continue
        if line.head is not None and line.head.variable:
            return sp.Symbol(line.head.variable)
        letters = sorted(_letters(line) - _CONFUSABLE_LETTERS)  # an 'S' may be a misread 5
        if "x" in letters or not letters:
            return sp.Symbol("x")
        return sp.Symbol(letters[0])
    return sp.Symbol("x")


def _safely_check_step(
    parsed: list[ParsedLine | None], errors: list[str | None], index: int, mode: str, x: sp.Symbol, strict_ocr: bool
) -> StepVerdict:
    """Any internal failure (odd OCR text can trip SymPy) means silence, never a crash."""
    try:
        return _check_step(parsed, errors, index, mode, x, strict_ocr)
    except Exception as error:  # noqa: BLE001 - deliberate last-resort guard
        explanation = {"mode": mode, "reason": "internal_error", "error": type(error).__name__}
        return StepVerdict(index, Verdict.UNCERTAIN, None, 0.0, explanation)


def _check_step(
    parsed: list[ParsedLine | None], errors: list[str | None], index: int, mode: str, x: sp.Symbol, strict_ocr: bool
) -> StepVerdict:
    prev, curr = parsed[index - 1], parsed[index]
    if prev is None or curr is None:
        unreadable = index - 1 if prev is None else index
        explanation = {"mode": mode, "reason": "unreadable_line", "line": unreadable, "error": errors[unreadable]}
        return StepVerdict(index, Verdict.UNCERTAIN, None, 0.0, explanation)

    finding = _run_checker(parsed, index, mode, x)
    explanation = {"mode": _mode_label(mode, prev, curr), "reason": finding.reason, **finding.details}
    flags = _ocr_flags(prev, x) + _ocr_flags(curr, x) + _new_letters(prev, curr, x)
    if flags:
        explanation["ocr_flags"] = list(dict.fromkeys(flags))
    if finding.verdict != Verdict.INVALID:
        return StepVerdict(index, finding.verdict, None, finding.confidence, explanation)

    matches = finding.diagnose() if finding.diagnose else []
    error_type = matches[0] if matches else "unclassified"
    if matches:
        explanation["matching_rules"] = matches
    misread = _misread_that_fixes_step(parsed, index, mode, x, strict_ocr)
    if misread:
        explanation["misread_that_fixes_step"] = misread
    if flags or misread:
        # The text may be a misreading of a correct line: stay silent rather than risk it.
        explanation["suspected"] = {"reason": finding.reason, "error_type": error_type}
        explanation["reason"] = "possible_misread"
        return StepVerdict(index, Verdict.UNCERTAIN, None, 0.0, explanation)
    confidence = 0.97 if matches else finding.confidence
    hint = hint_for(error_type) or _UNCLASSIFIED_HINT
    return StepVerdict(index, Verdict.INVALID, error_type, confidence, explanation, hint)


def _run_checker(parsed: list[ParsedLine | None], index: int, mode: str, x: sp.Symbol) -> Finding:
    if mode == DERIVATIVE_MODE:
        return check_derivative_step(parsed, index, x)
    if mode == EQUATION_MODE:
        return check_relation_step(parsed, index, x)
    return check_expression_step(parsed[index - 1], parsed[index])


def _misread_that_fixes_step(
    parsed: list[ParsedLine | None], index: int, mode: str, x: sp.Symbol, strict_ocr: bool
) -> str | None:
    """Name of a plausible OCR misread (in either line) under which the step is correct."""
    for which in (index - 1, index):
        for repair, text in alternative_readings(parsed[which].raw, strict=strict_ocr):
            try:
                reading = parse_line(text, allow_heads=(mode == DERIVATIVE_MODE))
            except ParseError:
                continue
            trial = list(parsed)
            trial[which] = reading
            finding = _run_checker(trial, index, mode, x)
            # Only a clearly correct step counts (not e.g. "sound, but may add roots").
            if finding.verdict == Verdict.VALID and finding.confidence >= _STRONG:
                return f"{repair} in line {which}"
    return None


def _mode_label(mode: str, prev: ParsedLine, curr: ParsedLine) -> str:
    ops = {op for line in (prev, curr) for relation in line.branches for op in relation.ops}
    if mode == EQUATION_MODE and ops - {"="}:
        return "inequality"
    return mode


def _letters(line: ParsedLine) -> set[str]:
    return {s.name for relation in line.branches for side in relation.sides for s in side.free_symbols}


def _ocr_flags(line: ParsedLine, x: sp.Symbol) -> list[str]:
    """Signs that the OCR text may not be what the student wrote."""
    flags = list(line.flags)
    for letter in sorted(_letters(line)):
        if letter in _CONFUSABLE_LETTERS and letter != x.name:
            flags.append(f"confusable_letter:{letter}")  # 'l' may be '1', 'S' may be '5', ...
    if any(side.has(sp.I) for relation in line.branches for side in relation.sides):
        flags.append("imaginary_unit")  # the parser reads a capital I as sqrt(-1): likely a misread 1
    return flags


def _new_letters(prev: ParsedLine, curr: ParsedLine, x: sp.Symbol) -> list[str]:
    """A correct step rarely introduces a letter that was not there before."""
    return [f"new_letter:{name}" for name in sorted(_letters(curr) - _letters(prev) - {x.name})]
