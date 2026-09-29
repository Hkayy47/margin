import sympy as sp

from margin_verifier.equivalence import DIFFERENT, EQUAL, UNKNOWN, compare_expressions

x, y = sp.symbols("x y")


def test_identical_after_evaluation():
    assert compare_expressions(sp.Mul(3, x + 2, evaluate=False), 3 * x + 6).status == EQUAL


def test_rational_simplification_with_a_hole_is_equal():
    # (x^2 - 9)/(x + 3) = x - 3 except at x = -3, which random points never hit
    assert compare_expressions((x**2 - 9) / (x + 3), x - 3).status == EQUAL


def test_different_expressions_give_a_counterexample():
    result = compare_expressions((x + 3) ** 2, x**2 + 9)
    assert result.status == DIFFERENT
    assert set(result.counterexample) >= {"x", "lhs_value", "rhs_value"}


def test_two_variables():
    assert compare_expressions((x + y) ** 2, x**2 + 2 * x * y + y**2).status == EQUAL
    assert compare_expressions((x + y) ** 2, x**2 + y**2).status == DIFFERENT


def test_sqrt_of_square_is_not_flagged():
    # sqrt(x^2) = |x|, but "= x" is routinely accepted in class: abstain, never flag.
    assert compare_expressions(sp.sqrt(x**2), x).status == UNKNOWN


def test_log_rules_only_valid_for_positive_values_are_not_flagged():
    assert compare_expressions(sp.log(x**2), 2 * sp.log(x)).status != DIFFERENT


def test_constants():
    assert compare_expressions(sp.sqrt(3**2 + 4**2), sp.Integer(5)).status == EQUAL
    assert compare_expressions(sp.sqrt(3**2 + 4**2), sp.Integer(7)).status == DIFFERENT
    assert compare_expressions(sp.sqrt(-400), sp.Integer(20)).status == DIFFERENT


def test_undefined_functions_are_unknown():
    f = sp.Function("f")
    assert compare_expressions(f(x), x**2).status == UNKNOWN


def test_deterministic():
    first = compare_expressions((x + 1) ** 3, x**3 + 1)
    second = compare_expressions((x + 1) ** 3, x**3 + 1)
    assert first == second
