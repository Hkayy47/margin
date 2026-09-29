"""Expression rewriting: simplify / expand / factor / fractions / exponent rules."""

import pytest

from conftest import only, verdicts


@pytest.mark.parametrize(
    "before, after",
    [
        ("(x+3)^2 - 2x", "x^2 + 4x + 9"),  # expand
        ("x^2 - 7x + 12", "(x-3)(x-4)"),  # factor
        (r"\frac{x^2-9}{x^2+5x+6}", r"\frac{x-3}{x+2}"),  # cancel a common factor
        (r"\frac{1}{x} + \frac{2}{x+1}", r"\frac{3x+1}{x(x+1)}"),  # combine fractions
        (r"x^2 \cdot x^3", "x^5"),  # exponent rule
        (r"\frac{x^7}{x^3}", "x^4"),
        (r"\frac{6x + 9}{3}", "2x + 3"),
        (r"\sqrt{3^2 + 4^2}", "5"),
        (r"2 \cdot 3 + 4", "10"),
    ],
)
def test_correct_rewrites_are_valid(before, after):
    assert verdicts([before, after], "simplify") == ["valid"]


@pytest.mark.parametrize(
    "before, after",
    [
        ("(x+3)^2 - 2x", "x^2 + 9 - 2x"),
        (r"\frac{x^2-9}{x^2+5x+6}", r"\frac{-9}{5x+6}"),
        (r"x^2 \cdot x^3", "x^6"),
        ("2(x-4) + 3(x+1)", "5x - 4"),
    ],
)
def test_wrong_rewrites_are_invalid(before, after):
    assert verdicts([before, after], "simplify") == ["invalid"]


def test_invalid_verdict_explains_itself():
    result = only(["(x+3)^2", "x^2 + 9"], "expand")
    assert result.explanation["mode"] == "expression"
    assert result.explanation["term_diff"]["missing"] == ["6*x"]
    assert "counterexample" in result.explanation
    assert result.hint and "6" not in result.hint  # a nudge, not the answer


def test_equals_chain_on_one_line_is_checked_link_by_link():
    assert verdicts(["(x+1)(x+2)", "= x^2 + 2x + x + 2 = x^2 + 3x + 2"], "expand") == ["valid"]
    assert verdicts(["(x+1)(x+2)", "= x^2 + 2x + x + 2 = x^2 + 3x + 3"], "expand") == ["invalid"]


def test_sqrt_of_a_square_abstains_rather_than_flags():
    assert verdicts([r"\sqrt{(x+1)^2}", "x + 1"], "simplify") == ["uncertain"]
