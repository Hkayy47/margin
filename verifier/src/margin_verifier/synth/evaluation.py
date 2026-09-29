"""Run the verifier over generated solutions and compute the metrics for RESULTS.md."""

from __future__ import annotations

import random
import statistics
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from margin_verifier import check_solution
from margin_verifier.synth.generator import generate
from margin_verifier.synth.noise import ANTICIPATED, HELD_OUT, noisy_solution

STRICT = {"strict_ocr": True}
CONFIRM = {"confirm_with_next_line": True}
BOTH = {**STRICT, **CONFIRM}

# name -> (noise kinds, per-line noise rate, verifier options). Every condition with the
# same noise sees exactly the same noisy lines, so rows are directly comparable.
CONDITIONS = {
    "clean": ((), 0.0, {}),
    "ocr_noise": (ANTICIPATED, 0.35, {}),
    "held_out_noise": (HELD_OUT, 0.35, {}),
    "clean | strict": ((), 0.0, STRICT),
    "clean | confirm": ((), 0.0, CONFIRM),
    "ocr_noise | confirm": (ANTICIPATED, 0.35, CONFIRM),
    "held_out_noise | strict": (HELD_OUT, 0.35, STRICT),
    "held_out_noise | confirm": (HELD_OUT, 0.35, CONFIRM),
    "held_out_noise | strict+confirm": (HELD_OUT, 0.35, BOTH),
}
# How false alarms scale with the OCR misread rate (reported in their own table).
for _rate in (0.02, 0.05, 0.10):
    CONDITIONS[f"held_out@{_rate:.0%}"] = (HELD_OUT, _rate, {})
    CONDITIONS[f"held_out@{_rate:.0%} | confirm"] = (HELD_OUT, _rate, CONFIRM)


@dataclass
class Transition:
    solution: str
    family: str
    template: str
    condition: str
    step: int
    is_error: bool
    injected_rule: str | None
    verdict: str
    error_type: str | None
    matching_rules: list[str]
    reason: str
    noise: list[str]  # noise kinds on the two lines involved (empty = untouched)
    seconds: float
    lines: tuple[str, str] = ("", "")


@dataclass
class SolutionResult:
    uid: str
    family: str
    has_error: bool
    condition: str
    transitions: list[Transition] = field(default_factory=list)


def evaluate_index(index: int, seed: int = 7) -> list[SolutionResult]:
    """Generate solution `index` and check it under every condition (runs in a worker process)."""
    solution = generate(index, seed)
    if solution is None:
        return []
    results = []
    for condition, (kinds, rate, options) in CONDITIONS.items():
        rng = random.Random(f"{seed}-{index}-{'-'.join(kinds)}-{rate}")  # same noise for same kinds and rate
        lines, noise = noisy_solution(solution.lines, kinds, rate, rng)
        start = time.perf_counter()
        verdicts = check_solution(lines, solution.task, **options)
        seconds = (time.perf_counter() - start) / max(1, len(verdicts))
        result = SolutionResult(solution.uid, solution.family, solution.error_step is not None, condition)
        for verdict in verdicts:
            step = verdict.step
            is_error = step == solution.error_step
            result.transitions.append(
                Transition(
                    solution=solution.uid,
                    family=solution.family,
                    template=solution.template,
                    condition=condition,
                    step=step,
                    is_error=is_error,
                    injected_rule=solution.error_rule if is_error else None,
                    verdict=verdict.verdict.value,
                    error_type=verdict.error_type,
                    matching_rules=list(verdict.explanation.get("matching_rules", [])),
                    reason=str(verdict.explanation.get("reason")),
                    noise=[k for k in (noise[step - 1], noise[step]) if k],
                    seconds=seconds,
                    lines=(lines[step - 1], lines[step]),
                )
            )
        results.append(result)
    return results


def metrics(results: list[SolutionResult]) -> dict:
    """Headline numbers for one group of solution results."""
    transitions = [t for r in results for t in r.transitions]
    errors = [t for t in transitions if t.is_error]
    correct = [t for t in transitions if not t.is_error]
    flagged = [t for t in transitions if t.verdict == "invalid"]
    caught = [t for t in errors if t.verdict == "invalid"]
    clean_solutions = [r for r in results if not r.has_error]
    alarmed = [r for r in clean_solutions if any(t.verdict == "invalid" for t in r.transitions)]
    return {
        "solutions": len(results),
        "error_transitions": len(errors),
        "correct_transitions": len(correct),
        "recall": _ratio(len(caught), len(errors)),
        "precision": _ratio(len(caught), len(flagged)),
        "false_alarms": len(flagged) - len(caught),
        "false_alarm_rate_per_correct_transition": _ratio(len(flagged) - len(caught), len(correct)),
        "false_alarm_rate_per_correct_solution": _ratio(len(alarmed), len(clean_solutions)),
        "uncertain_rate_correct": _ratio(sum(t.verdict == "uncertain" for t in correct), len(correct)),
        "uncertain_rate_error": _ratio(sum(t.verdict == "uncertain" for t in errors), len(errors)),
        "missed_as_valid": sum(t.verdict == "valid" for t in errors),
        "diagnosis_accuracy": _ratio(sum(t.error_type == t.injected_rule for t in caught), len(caught)),
        "diagnosis_in_matches": _ratio(sum(t.injected_rule in t.matching_rules for t in caught), len(caught)),
        "seconds_mean": statistics.fmean(t.seconds for t in transitions) if transitions else None,
        "seconds_p95": _percentile([t.seconds for t in transitions], 95),
    }


def by(results: list[SolutionResult], key) -> dict[str, list[SolutionResult]]:
    groups: dict[str, list[SolutionResult]] = defaultdict(list)
    for result in results:
        groups[key(result)].append(result)
    return dict(sorted(groups.items()))


def per_rule(results: list[SolutionResult]) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    errors = [t for r in results for t in r.transitions if t.is_error]
    for rule in sorted({t.injected_rule for t in errors}):
        group = [t for t in errors if t.injected_rule == rule]
        caught = [t for t in group if t.verdict == "invalid"]
        confusions = Counter(t.error_type for t in caught if t.error_type != rule)
        rows[rule] = {
            "n": len(group),
            "recall": _ratio(len(caught), len(group)),
            "uncertain": _ratio(sum(t.verdict == "uncertain" for t in group), len(group)),
            "missed_as_valid": sum(t.verdict == "valid" for t in group),
            "diagnosis_accuracy": _ratio(sum(t.error_type == rule for t in caught), len(caught)),
            "confused_with": ", ".join(f"{k} ({v})" for k, v in confusions.most_common(3)),
        }
    return rows


def per_noise_kind(results: list[SolutionResult]) -> dict[str, dict]:
    """For correct transitions touched by each noise kind: how often valid / uncertain / invalid."""
    rows: dict[str, dict] = {}
    correct = [t for r in results for t in r.transitions if not t.is_error and t.noise]
    for kind in sorted({k for t in correct for k in t.noise}):
        group = [t for t in correct if kind in t.noise]
        rows[kind] = {
            "correct_transitions": len(group),
            "valid": _ratio(sum(t.verdict == "valid" for t in group), len(group)),
            "uncertain": _ratio(sum(t.verdict == "uncertain" for t in group), len(group)),
            "false_alarms": sum(t.verdict == "invalid" for t in group),
        }
    return rows


def _ratio(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _percentile(values: list[float], q: int) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * q / 100))]
