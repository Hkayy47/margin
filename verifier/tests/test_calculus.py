import pytest
import sympy as sp

from margin_verifier.calculus import buggy_derivatives, differentiate

x = sp.Symbol("x")

FUNCTIONS = [
    3 * x**4 - 2 * x**2 + 5 * x - 7,
    (2 * x + 1) ** 3,
    x**2 * sp.sin(x),
    sp.sin(3 * x**2),
    sp.exp(x**2) * sp.cos(x),
    sp.log(x**2 + 1),
    sp.sqrt(x + 1),
    1 / (x - 2),
    2 ** (3 * x),
]


@pytest.mark.parametrize("function", FUNCTIONS)
def test_matches_sympy_without_bugs(function):
    assert sp.simplify(differentiate(function, x) - sp.diff(function, x)) == 0


def test_power_rule_bug():
    assert 3 * x**3 in buggy_derivatives(x**3, x, "power_no_decrement")


def test_chain_rule_bug():
    assert 3 * (2 * x + 1) ** 2 in buggy_derivatives((2 * x + 1) ** 3, x, "chain_omitted")


def test_product_rule_bug():
    assert 2 * x * sp.cos(x) in buggy_derivatives(x**2 * sp.sin(x), x, "product_as_product")


def test_bug_applied_to_a_single_term_is_also_offered():
    wrong = buggy_derivatives(x**3 + x**2, x, "power_no_decrement")
    assert 3 * x**3 + 2 * x in wrong  # only the first term kept its exponent
