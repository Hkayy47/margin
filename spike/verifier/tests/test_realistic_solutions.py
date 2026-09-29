"""Hand-written student solutions, including correct steps that naive checks would flag."""

import pytest

from conftest import verdicts

SOLVE = "solve for x"

CORRECT_SOLUTIONS = {
    "lcd with numbers": (SOLVE, [r"\frac{x}{3} + \frac{x}{4} = 7", "4x + 3x = 84", "7x = 84", "x = 12"]),
    "cross-multiplying": (SOLVE, [r"\frac{3}{x} = \frac{6}{x+2}", "3(x+2) = 6x", "3x + 6 = 6x", "6 = 3x", "x = 2"]),
    "divide both sides by 2": (SOLVE, ["2x - 6 = 4x + 10", "x - 3 = 2x + 5", "-3 - 5 = 2x - x", "x = -8"]),
    "factoring": (SOLVE, ["x^2 + x - 12 = 0", "(x+4)(x-3) = 0", r"x = -4 \text{ or } x = 3"]),
    "completing the square": (SOLVE, ["x^2 - 4x - 5 = 0", "x^2 - 4x = 5", "x^2 - 4x + 4 = 9", "(x-2)^2 = 9",
                                      r"x - 2 = \pm 3", r"x = 5 \text{ or } x = -1"]),
    "x^2 = 9 -> x = pm 3": (SOLVE, ["x^2 = 9", r"x = \pm 3"]),
    "scaled square root": (SOLVE, ["2x^2 = 32", "x^2 = 16", r"x = \pm 4"]),
    "squaring with a check": (SOLVE, [r"\sqrt{2x+1} = x - 1", "2x + 1 = x^2 - 2x + 1", "0 = x^2 - 4x",
                                      "x(x-4) = 0", r"x = 0 \text{ or } x = 4", "x = 4"]),
    "variable lcd": (SOLVE, [r"\frac{2}{x} + \frac{1}{2} = 1", "4 + x = 2x", "x = 4"]),
    "negative distribution": (SOLVE, ["3 - (x - 5) = 2", "3 - x + 5 = 2", "8 - x = 2", "x = 6"]),
    "inequality divided by a negative": ("solve the inequality", [r"4 - 3x \leq 10", r"-3x \leq 6", r"x \geq -2"]),
    "rational simplification": ("simplify", [r"\frac{2x^2 - 8}{x^2 + 4x + 4}", r"\frac{2(x-2)(x+2)}{(x+2)^2}",
                                             r"\frac{2(x-2)}{x+2}"]),
    "exponent rules": ("simplify", [r"\frac{x^5 \cdot x^3}{x^2}", r"\frac{x^8}{x^2}", "x^6"]),
    "product rule": ("differentiate", [r"f(x) = x^3 e^{x}", r"f'(x) = 3x^2 e^{x} + x^3 e^{x}",
                                       r"f'(x) = x^2 e^{x}(3 + x)"]),
    "chain rule": ("differentiate", [r"y = (3x^2 + 1)^4", r"y' = 4(3x^2+1)^3 \cdot 6x", r"y' = 24x(3x^2+1)^3"]),
}


@pytest.mark.parametrize("name", CORRECT_SOLUTIONS)
def test_correct_solution_is_never_flagged(name):
    task, lines = CORRECT_SOLUTIONS[name]
    assert verdicts(lines, task) == ["valid"] * (len(lines) - 1)


def test_one_error_then_consistent_work():
    lines = ["5x - 3 = 2x + 9", "5x - 2x = 9 - 3", "3x = 6", "x = 2"]
    assert verdicts(lines, SOLVE) == ["invalid", "valid", "valid"]


def test_distribution_sign_error_then_consistent_work():
    lines = ["4 - 2(x - 3) = 8", "4 - 2x - 6 = 8", "-2x - 2 = 8", "-2x = 10", "x = -5"]
    assert verdicts(lines, SOLVE) == ["invalid", "valid", "valid", "valid"]


def test_forgotten_negative_root_at_the_end():
    lines = ["x^2 - 2x = 8", "x^2 - 2x - 8 = 0", "(x-4)(x+2) = 0", "x = 4"]
    assert verdicts(lines, SOLVE) == ["valid", "valid", "invalid"]


def test_prose_line_is_skipped_not_flagged():
    assert verdicts(["Let x be the number", "2x + 3 = 7"]) == ["uncertain"]


def test_check_solution_is_deterministic():
    from margin_verifier import check_solution

    lines = ["(x+3)^2 - 2x", "x^2 + 9 - 2x"]
    first = [v.to_dict() for v in check_solution(lines, "expand")]
    second = [v.to_dict() for v in check_solution(lines, "expand")]
    assert first == second
