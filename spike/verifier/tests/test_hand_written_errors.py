"""Wrong steps written by hand (independent of the generator): all must be flagged.

`rule` is the mal-rule we expect the diagnosis to name, or None when no rule in
the library describes the mistake (then error_type must be "unclassified").
"""

import pytest

from margin_verifier import check_solution

SOLVE, SIMPLIFY, DIFF, INEQ = "solve for x", "simplify", "differentiate", "solve the inequality"

WRONG_STEPS = [
    (SOLVE, ["2x + 3 = 7", "2x = 10"], "sign_not_flipped_on_move"),
    (SOLVE, ["3(x + 2) = 12", "3x + 2 = 12"], "distribute_first_term_only"),
    (SOLVE, ["x^2 = 16", "x = 4"], "sqrt_missing_pm"),
    ("expand", ["(x + 2)^2", "x^2 + 4"], "square_of_sum"),
    (SIMPLIFY, [r"\frac{x + 3}{x}", "3"], "cancel_across_addition"),
    (SIMPLIFY, [r"\frac{1}{2} + \frac{1}{3}", r"\frac{2}{5}"], "add_fractions_add_denominators"),
    (SIMPLIFY, [r"x^3 \cdot x^4", "x^{12}"], "exponent_product_multiply"),
    (DIFF, ["f(x) = x^5", "f'(x) = 5x^5"], "power_rule_no_decrement"),
    (DIFF, [r"f(x) = \sin(2x)", r"f'(x) = \cos(2x)"], "chain_rule_omitted"),
    (DIFF, [r"f(x) = x e^{x}", r"f'(x) = e^{x}"], "product_rule_as_product"),
    (INEQ, ["-3x < 9", "x < -3"], "inequality_not_flipped"),
    (SOLVE, ["x^2 = 5x", "x = 5"], "divide_by_variable"),
    (SIMPLIFY, [r"\sqrt{9 + 16}", "3 + 4"], "sqrt_of_sum"),
    (SIMPLIFY, [r"\frac{4x + 8}{4}", "x + 8"], "divide_one_term_only"),
    (SOLVE, ["5x - 2 = 3x + 6", "2x = 4"], "sign_not_flipped_on_move"),
    (SIMPLIFY, ["-(x - 5)", "-x - 5"], "distribute_first_term_only"),
    (DIFF, [r"f(x) = (x^2 + 1)^3", r"f'(x) = 3(x^2 + 1)^2"], "chain_rule_omitted"),
    (SOLVE, ["4 - 2x = 10", "-2x = 14"], "sign_not_flipped_on_move"),
    (SIMPLIFY, [r"\sqrt{x + 4}", r"\sqrt{x} + 2"], "sqrt_of_sum"),
    (SOLVE, ["x - 7 = 3", "x = -4"], "sign_not_flipped_on_move"),
    (SIMPLIFY, ["2(x - 3) - (x + 1)", "x - 5"], "distribute_first_term_only"),  # -(x + 1) -> -x + 1
    (SOLVE, ["6x = 18", "x = 4"], "arithmetic_slip"),
    # mistakes outside the library: flagged, but "unclassified"
    (SOLVE, [r"\frac{x}{3} = 6", "x = 2"], None),
    (SOLVE, ["x^2 - 9 = 0", "(x - 3)^2 = 0"], None),
    (SOLVE, [r"\frac{3}{x} = 6", "x = 2"], None),
    (SOLVE, ["x^2 + 6x = 7", "(x + 3)^2 = 7"], None),
    (SIMPLIFY, [r"\frac{x^2 + x}{x}", "x^2"], "cancel_across_addition"),  # the added x 'cancelled'
    (SIMPLIFY, ["(2x)^3", "2x^3"], None),
    (SIMPLIFY, [r"2^3 \cdot 2^2", "2^6"], None),
    (DIFF, [r"f(x) = \ln x", r"f'(x) = \frac{1}{x^2}"], None),
]


@pytest.mark.parametrize("task, lines, rule", WRONG_STEPS)
def test_hand_written_error_is_flagged(task, lines, rule):
    (result,) = check_solution(lines, task)
    assert result.verdict.value == "invalid", result.explanation
    assert result.error_type == (rule or "unclassified"), result.explanation
