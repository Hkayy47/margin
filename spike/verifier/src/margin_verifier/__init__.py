"""Margin step verifier: checks each line of a handwritten solution against the previous one."""

from margin_verifier.verdict import StepVerdict, Verdict
from margin_verifier.verifier import check_solution

__all__ = ["StepVerdict", "Verdict", "check_solution"]
