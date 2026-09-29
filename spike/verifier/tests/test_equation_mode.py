"""Equation and inequality steps: compare real solution sets."""

import pytest

from conftest import only, verdicts

SOLVE = "solve for x"


@pytest.mark.parametrize(
    "before, after",
    [
        ("2x + 3 = 7", "2x = 4"),
        ("2x + 4 = 10", "x + 2 = 5"),  # divide every term by 2
        (r"\frac{x}{2} + \frac{x}{3} = 5", "3x + 2x = 30"),  # multiply through by the LCD
        (r"\frac{x+1}{2} = \frac{x-3}{4}", "2(x+1) = x - 3"),  # cross-multiplying
        ("x^2 - 5x + 6 = 0", "(x-2)(x-3) = 0"),
        ("(x-2)(x-3) = 0", r"x = 2 \text{ or } x = 3"),
        ("x^2 = 9", r"x = \pm 3"),
        ("x^2 = 9", "x = 3, x = -3"),
        ("(x+1)^2 = 16", r"x + 1 = \pm 4"),
        (r"x + 1 = \pm 4", r"x = -1 \pm 4"),
        ("5 = 2x + 1", "2x + 1 = 5"),
        ("x^2 + 6x + 5 = 0", "x^2 + 6x + 9 = 4"),  # completing the square
    ],
)
def test_equivalent_equations_are_valid(before, after):
    assert verdicts([before, after], SOLVE) == ["valid"]


def test_changed_solution_is_invalid():
    result = only(["2x + 3 = 7", "2x = 10"], SOLVE)
    assert result.verdict.value == "invalid"
    assert result.explanation["lost"] == ["2"] and result.explanation["extra"] == ["5"]


def test_lost_solution_when_dividing_by_x():
    result = only(["x^2 = 4x", "x = 4"], SOLVE)
    assert result.verdict.value == "invalid"
    assert result.explanation["reason"] == "lost_solutions"
    assert result.explanation["lost"] == ["0"]


def test_lost_solution_when_forgetting_plus_minus():
    result = only(["x^2 = 9", "x = 3"], SOLVE)
    assert (result.verdict.value, result.error_type) == ("invalid", "sqrt_missing_pm")


def test_squaring_both_sides_is_a_sound_step_that_may_add_roots():
    result = only([r"\sqrt{x+3} = x - 3", "x + 3 = (x-3)^2"], SOLVE)
    assert result.verdict.value == "valid"
    assert result.explanation["reason"] == "implication_may_add_roots"
    assert result.explanation["extra_candidates"] == ["1"]


def test_rejecting_the_extraneous_root_after_squaring_is_valid():
    lines = [r"\sqrt{x+3} = x - 3", "x + 3 = x^2 - 6x + 9", "(x-1)(x-6) = 0", r"x = 1 \text{ or } x = 6", "x = 6"]
    assert verdicts(lines, SOLVE) == ["valid"] * 4


def test_dropping_a_genuine_root_is_invalid():
    assert verdicts(["(x-1)(x-6) = 0", r"x = 1 \text{ or } x = 6", "x = 6"], SOLVE) == ["valid", "invalid"]


def test_adding_a_wrong_value_to_a_final_answer_is_invalid():
    assert verdicts(["(x-2)(x-3) = 0", r"x = 2 \text{ or } x = 3 \text{ or } x = 5"], SOLVE) == ["invalid"]


def test_clearing_a_variable_denominator_may_add_a_root_but_is_sound():
    lines = [r"\frac{x^2-4}{x-2} = 0", "x^2 - 4 = 0", r"x = \pm 2", "x = -2"]
    assert verdicts(lines, SOLVE) == ["valid", "valid", "valid"]


def test_inequalities():
    assert verdicts(["-2x + 3 > 7", "-2x > 4", "x < -2"], "solve the inequality") == ["valid", "valid"]
    result = only(["-2x > 4", "x > -2"], "solve the inequality")
    assert (result.verdict.value, result.error_type) == ("invalid", "inequality_not_flipped")
    assert result.explanation["mode"] == "inequality"


def test_equations_with_other_letters_are_out_of_scope():
    assert verdicts(["ax + b = 0", "x = -b/a"], SOLVE) == ["uncertain"]


def test_solver_gives_up_after_its_time_budget(monkeypatch):
    import time

    import sympy as sp

    from margin_verifier import solutions

    def slow_solveset(*args, **kwargs):
        time.sleep(1)
        return sp.S.EmptySet

    monkeypatch.setattr(solutions, "_SOLVE_SECONDS", 0.05)
    monkeypatch.setattr(solutions.sp, "solveset", slow_solveset)
    x = sp.Symbol("x")
    assert solutions._solveset_within_budget(sp.Eq(sp.sqrt(x), 3), x) is None
