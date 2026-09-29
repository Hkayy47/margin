"""Derivative steps: differentiate, then rewrite."""

import pytest

from conftest import only, verdicts

DIFF = "differentiate with respect to x"


@pytest.mark.parametrize(
    "lines",
    [
        ["f(x) = x^3 + 2x", "f'(x) = 3x^2 + 2"],
        ["f(x) = (2x+1)^3", r"f'(x) = 3(2x+1)^2 \cdot 2", "f'(x) = 6(2x+1)^2"],
        [r"f(x) = x^2 \sin x", r"f'(x) = 2x \sin x + x^2 \cos x", r"f'(x) = x(2\sin x + x\cos x)"],
        [r"y = e^{3x}", r"y' = 3e^{3x}"],
        [r"y = \ln(x^2 + 1)", r"\frac{dy}{dx} = \frac{2x}{x^2+1}"],
        [r"\frac{d}{dx}(x^3 \sin x)", r"= 3x^2 \sin x + x^3 \cos x"],
        [r"\frac{d}{dx}\left(\cos(3x^2)\right) = -6x\sin(3x^2)", r"= -6x \sin(3x^2)"],
        ["f(x) = x^4", "f'(x) = 4x^3", "f''(x) = 12x^2"],
    ],
)
def test_correct_derivatives(lines):
    assert verdicts(lines, DIFF) == ["valid"] * (len(lines) - 1)


def test_task_is_optional_when_notation_says_it():
    assert verdicts(["f(x) = x^2", "f'(x) = 2x"]) == ["valid"]


def test_wrong_derivative_is_invalid():
    result = only(["f(x) = x^3", "f'(x) = 3x^3"], DIFF)
    assert (result.verdict.value, result.error_type) == ("invalid", "power_rule_no_decrement")
    assert result.explanation["reason"] == "wrong_derivative"


def test_rewrite_after_differentiating_is_compared_with_the_previous_line():
    lines = ["f(x) = (x+1)^2", "f'(x) = 2(x+1)", "f'(x) = 2x + 1"]
    assert verdicts(lines, DIFF) == ["valid", "invalid"]


def test_error_is_not_repeated_on_the_following_line():
    # the student carries on consistently from a wrong line: only that line is flagged
    lines = ["f(x) = (2x+1)^3", "f'(x) = 3(2x+1)^2", "f'(x) = 12x^2 + 12x + 3"]
    assert verdicts(lines, DIFF) == ["invalid", "valid"]


def test_bare_lines_accept_either_reading():
    # without f'(x) notation we cannot know whether line 2 is a rewrite or the derivative
    assert verdicts(["(x+1)^2", "x^2 + 2x + 1"], DIFF) == ["valid"]
    assert verdicts(["(x+1)^2", "2(x+1)"], DIFF) == ["valid"]
