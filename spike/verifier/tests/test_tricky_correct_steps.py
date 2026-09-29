"""Correct steps that a naive checker might flag. The product rule: never 'invalid'.

Written by hand, independently of the synthetic generator.
"""

import pytest

from conftest import verdicts

SOLVE, SIMPLIFY, DIFF = "solve for x", "simplify", "differentiate"

TRICKY_CORRECT = [
    # expressions: domain subtleties, radicals, rewriting conventions
    (SIMPLIFY, [r"\frac{x^2 - 1}{x - 1}", "x + 1"]),
    (SIMPLIFY, [r"\sqrt{x^2}", "|x|"]),
    (SIMPLIFY, [r"(x^2)^{3}", "x^6"]),
    (SIMPLIFY, [r"\sqrt{8}", r"2\sqrt{2}"]),
    (SIMPLIFY, [r"\frac{1}{\sqrt{2}}", r"\frac{\sqrt{2}}{2}"]),
    (SIMPLIFY, [r"x^{\frac{1}{2}}", r"\sqrt{x}"]),
    (SIMPLIFY, [r"\frac{2}{4}", r"\frac{1}{2}"]),
    (SIMPLIFY, ["0.5x", r"\frac{x}{2}"]),
    (SIMPLIFY, ["2(x + 3) - (x - 1)", "x + 7"]),
    (SIMPLIFY, [r"\frac{x}{x}", "1"]),
    (SIMPLIFY, [r"\ln(e^{x})", "x"]),
    (SIMPLIFY, [r"e^{\ln x}", "x"]),
    (SIMPLIFY, [r"\frac{x^3 - 8}{x - 2}", "x^2 + 2x + 4"]),
    (SIMPLIFY, ["(a + b)^2", "a^2 + 2ab + b^2"]),
    (SIMPLIFY, [r"\sin^2 x + \cos^2 x", "1"]),
    (SIMPLIFY, [r"2\sin x \cos x", r"\sin(2x)"]),
    (SIMPLIFY, [r"\frac{6x^2 + 3x}{3x}", "2x + 1"]),
    (SIMPLIFY, ["x^{-2}", r"\frac{1}{x^2}"]),
    (SIMPLIFY, ["-(-x)", "x"]),
    (SIMPLIFY, ["(-x)^2", "x^2"]),
    (SIMPLIFY, [r"\sqrt{4x^2}", "2|x|"]),
    (SIMPLIFY, [r"\frac{a}{b} \div \frac{c}{d}", r"\frac{ad}{bc}"]),
    (SIMPLIFY, ["3x^0", "3"]),
    (SIMPLIFY, [r"\frac{x+1}{2} + \frac{x-1}{3}", r"\frac{5x + 1}{6}"]),
    # equations: rescaling, swapping, implication steps, decimals, special solution sets
    (SOLVE, ["x^2 = 2x", "x^2 - 2x = 0", "x(x - 2) = 0"]),
    (SOLVE, [r"\frac{x}{x-1} = \frac{1}{x-1} + 2", "x = 1 + 2(x - 1)", "x = 2x - 1"]),
    (SOLVE, ["3(x - 2) = 3", "x - 2 = 1", "x = 3"]),
    (SOLVE, [r"\frac{2x}{3} = 4", "2x = 12"]),
    (SOLVE, ["0.5x + 2 = 5", "x + 4 = 10"]),
    (SOLVE, ["x^2 + 4 = 0", "x^2 = -4"]),
    (SOLVE, ["(x - 3)^2 = 0", "x = 3"]),
    (SOLVE, ["x^3 = 8", "x = 2"]),
    (SOLVE, [r"\sqrt{x} = 3", "x = 9"]),
    (SOLVE, [r"\frac{1}{x} = 2", r"x = \frac{1}{2}"]),
    (SOLVE, ["|x| = 5", r"x = \pm 5"]),
    (SOLVE, ["2^{x+1} = 16", "x + 1 = 4"]),
    (SOLVE, ["x = 5", "5 = x"]),
    (SOLVE, ["x^2 - 6x + 9 = 0", "(x - 3)^2 = 0", "x = 3"]),
    (SOLVE, ["4x = 2", "x = 0.5"]),
    (SOLVE, ["-x = 3", "x = -3"]),
    (SOLVE, ["x^2 = 9", r"x = 3 \text{ or } x = -3"]),
    (SOLVE, [r"x^2 - 5x + 6 = 0", "x = 2, x = 3"]),
    # inequalities
    ("solve the inequality", ["-x > 3", "x < -3"]),
    ("solve the inequality", [r"2x \geq 6", r"x \geq 3"]),
    ("solve the inequality", ["3 > x", "x < 3"]),
    # derivatives
    (DIFF, [r"f(x) = \frac{1}{x}", r"f'(x) = -\frac{1}{x^2}"]),
    (DIFF, [r"f(x) = \sqrt{x}", r"f'(x) = \frac{1}{2\sqrt{x}}"]),
    (DIFF, [r"y = \ln x", r"y' = \frac{1}{x}"]),
    (DIFF, ["f(x) = 5", "f'(x) = 0"]),
    (DIFF, [r"f(x) = \tan x", r"f'(x) = \sec^2 x"]),
    (DIFF, [r"f(x) = x^2 e^{x}", r"f'(x) = e^{x}(x^2 + 2x)"]),
]


@pytest.mark.parametrize("task, lines", TRICKY_CORRECT)
def test_tricky_correct_step_is_never_flagged(task, lines):
    assert "invalid" not in verdicts(lines, task)


def test_most_tricky_steps_are_recognised_as_valid_not_just_skipped():
    results = [v for task, lines in TRICKY_CORRECT for v in verdicts(lines, task)]
    assert results.count("valid") / len(results) > 0.85
