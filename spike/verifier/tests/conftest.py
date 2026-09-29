"""Shared helpers for the test-suite."""

from __future__ import annotations

from margin_verifier import check_solution


def verdicts(lines: list[str], task: str | None = None, **kwargs) -> list[str]:
    """Just the verdict strings, e.g. ['valid', 'invalid']."""
    return [v.verdict.value for v in check_solution(lines, task, **kwargs)]


def only(lines: list[str], task: str | None = None, **kwargs):
    """The single StepVerdict of a two-line solution."""
    (result,) = check_solution(lines, task, **kwargs)
    return result
