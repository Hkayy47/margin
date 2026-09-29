"""Problem templates: a random starting line, a solver, and the mistakes that fit it.

Parameters are drawn so that answers are small integers (like textbook problems).
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

import sympy as sp

from margin_verifier.synth import transforms as t
from margin_verifier.synth.lines import X, Line, ordered, relation_line
from margin_verifier.tree import add, fraction, mul


@dataclass(frozen=True)
class Template:
    name: str
    family: str
    task: str
    start: Callable[[random.Random], Line]
    solver: tuple[t.Transform, ...]  # correct steps, in priority order
    rules: tuple[str, ...]  # mal-rules that make sense to inject here


def _nonzero(rng: random.Random, low: int, high: int) -> int:
    return rng.choice([k for k in range(low, high + 1) if k != 0])


LINEAR = (t.expand_brackets, t.clear_fractions, t.combine_like_terms, t.swap_sides, t.move_terms,
          t.divide_by_coefficient)
LINEAR_DIVIDE_FIRST = (t.expand_brackets, t.clear_fractions, t.combine_like_terms, t.divide_through,
                       t.swap_sides, t.move_terms, t.divide_by_coefficient)
QUADRATIC = (t.isolate_pm, t.solve_linear_branches, t.square_root_both_sides, t.split_zero_product,
             t.isolate_square, t.move_everything_left, t.factor_polynomial, t.quadratic_formula)
COMPLETE_SQUARE = (t.isolate_pm, t.solve_linear_branches, t.square_root_both_sides, t.write_as_square,
                   t.complete_the_square, t.move_constant_right)
RADICAL = (t.reject_extraneous, t.solve_linear_branches, t.split_zero_product, t.square_both_sides,
           t.expand_brackets, t.move_everything_left, t.factor_polynomial, t.quadratic_formula)
RATIONAL = (t.split_numeric_fraction, t.combine_fractions, t.expand_numerator, t.factor_fraction,
            t.cancel_fraction, t.combine_terms)
POLYNOMIAL = (t.expand_each_term, t.combine_terms)
POWERS = (t.add_exponents, t.evaluate_squares, t.combine_terms)


# ------------------------------------------------------------------------------ linear equations


def linear_bracket(rng: random.Random) -> Line:
    a, c = rng.randint(2, 6), rng.randint(1, 5)
    while c == a:
        c = rng.randint(1, 5)
    b, root = _nonzero(rng, -6, 6), rng.randint(-9, 9)
    d = a * (root + b) - c * root
    return relation_line(mul(sp.Integer(a), add(X, sp.Integer(b))), ordered(c * X + d))


def linear_two_sided(rng: random.Random) -> Line:
    a, c = rng.randint(2, 9), rng.randint(1, 8)
    while c == a:
        c = rng.randint(1, 8)
    b, root = _nonzero(rng, -12, 12), rng.randint(-9, 9)
    d = a * root + b - c * root
    return relation_line(ordered(a * X + b), ordered(c * X + d))


def linear_divide_first(rng: random.Random) -> Line:
    g, a = rng.randint(2, 5), rng.randint(1, 4)
    b, root = _nonzero(rng, -6, 6), rng.randint(-8, 8)
    return relation_line(ordered(g * a * X + g * b), sp.Integer(g * (a * root + b)))


def linear_fractions(rng: random.Random) -> Line:
    p, q = rng.sample([2, 3, 4, 5, 6], 2)
    root = sp.ilcm(p, q) * _nonzero(rng, -3, 3)
    total = sp.Rational(root, p) + sp.Rational(root, q)
    return relation_line(add(fraction(X, sp.Integer(p)), fraction(X, sp.Integer(q))), total)


def linear_cross_multiply(rng: random.Random) -> Line:
    p, q = rng.sample([2, 3, 4, 5], 2)
    b, root = _nonzero(rng, -5, 5), rng.randint(-8, 8)
    # (x + b)/p = (x + d)/q with d chosen so that x = root works
    d = sp.Rational(q * (root + b), p) - root
    if not d.is_Integer:
        return linear_cross_multiply(rng)
    return relation_line(fraction(add(X, sp.Integer(b)), sp.Integer(p)), fraction(ordered(X + d), sp.Integer(q)))


# ------------------------------------------------------------------------------------ quadratics


def quadratic_factor(rng: random.Random) -> Line:
    r1, r2 = rng.sample([k for k in range(-9, 10) if k != 0], 2)
    polynomial = sp.expand((X - r1) * (X - r2))
    if rng.random() < 0.5:
        return relation_line(ordered(polynomial), sp.Integer(0))
    constant = polynomial.coeff(X, 0)
    return relation_line(ordered(polynomial - constant), -constant)  # x^2 - 5x = -6


def quadratic_square_root(rng: random.Random) -> Line:
    k = rng.randint(1, 9)
    shape = rng.choice(["plain", "scaled", "shifted"])
    if shape == "plain":
        return relation_line(X**2, sp.Integer(k * k))
    if shape == "scaled":
        a = rng.randint(2, 4)
        return relation_line(ordered(a * X**2 - a * k * k), sp.Integer(0))
    p = _nonzero(rng, -6, 6)
    return relation_line(sp.Pow(ordered(X + p), 2, evaluate=False), sp.Integer(k * k))


def quadratic_common_factor(rng: random.Random) -> Line:
    a = _nonzero(rng, -9, 9)
    if rng.random() < 0.5:
        return relation_line(X**2, ordered(a * X))
    b = rng.randint(2, 4)
    return relation_line(ordered(b * X**2), ordered(a * b * X))


def complete_square(rng: random.Random) -> Line:
    p, q = _nonzero(rng, -6, 6), rng.randint(1, 5)
    c = p * p - q * q
    if c == 0:
        return complete_square(rng)
    return relation_line(ordered(X**2 + 2 * p * X + c), sp.Integer(0))


def radical_squaring(rng: random.Random) -> Line:
    """sqrt(x + a) = x - b with one real root and one extraneous root."""
    b = rng.randint(1, 6)
    good = rng.randint(b + 1, b + 6)
    bad = 2 * b + 1 - good  # the other root of the squared equation
    a = b * b - good * bad
    if bad >= b or bad + a < 0:
        return radical_squaring(rng)
    return relation_line(sp.Pow(ordered(X + a), sp.Rational(1, 2), evaluate=False), ordered(X - b))


# ------------------------------------------------------------------------------------ rational


def rational_cancel(rng: random.Random) -> Line:
    p, q, r = rng.sample([k for k in range(-6, 7) if k != 0], 3)
    top, bottom = sp.expand((X + p) * (X + q)), sp.expand((X + q) * (X + r))
    return Line("expr", expr=fraction(ordered(top), ordered(bottom)))


def rational_add(rng: random.Random) -> Line:
    a, b, c = rng.randint(1, 5), rng.randint(1, 5), _nonzero(rng, -5, 5)
    return Line("expr", expr=add(fraction(sp.Integer(a), X), fraction(sp.Integer(b), ordered(X + c))))


def rational_numeric_denominator(rng: random.Random) -> Line:
    d = rng.randint(2, 5)
    a, b, k = rng.randint(1, 4), _nonzero(rng, -5, 5), _nonzero(rng, -4, 4)
    return Line("expr", expr=add(fraction(ordered(a * d * X + b * d), sp.Integer(d)), ordered(k * X)))


# ---------------------------------------------------------------------------------- polynomials


def poly_square_expand(rng: random.Random) -> Line:
    a, b = _nonzero(rng, -7, 7), _nonzero(rng, -6, 6)
    return Line("expr", expr=add(sp.Pow(ordered(X + a), 2, evaluate=False), ordered(b * X)))


def poly_distribute(rng: random.Random) -> Line:
    a, c = rng.randint(2, 6), rng.randint(2, 6)
    b, d = _nonzero(rng, -7, 7), _nonzero(rng, -7, 7)
    sign = rng.choice([1, -1])
    second = mul(sp.Integer(sign * c), ordered(X + d))
    return Line("expr", expr=add(mul(sp.Integer(a), ordered(X + b)), second))


def poly_foil(rng: random.Random) -> Line:
    a, b = _nonzero(rng, -7, 7), _nonzero(rng, -7, 7)
    return Line("expr", expr=mul(ordered(X + a), ordered(X + b)))


def poly_factor(rng: random.Random) -> Line:
    a, b = rng.sample([k for k in range(-8, 9) if k != 0], 2)
    return Line("expr", expr=ordered(sp.expand((X + a) * (X + b))))


def exponent_product(rng: random.Random) -> Line:
    m, n = rng.randint(2, 6), rng.randint(2, 6)
    c1, c2 = rng.randint(1, 5), rng.randint(1, 5)
    factors = [sp.Integer(c1), sp.Pow(X, m, evaluate=False), sp.Integer(c2), sp.Pow(X, n, evaluate=False)]
    return Line("expr", expr=mul(*[f for f in factors if f != 1]))  # 5x^{3} \cdot 2x^{6}


def pythagorean(rng: random.Random) -> Line:
    a, b, _ = rng.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20)])
    inside = add(sp.Pow(sp.Integer(a), 2, evaluate=False), sp.Pow(sp.Integer(b), 2, evaluate=False))
    return Line("expr", expr=sp.Pow(inside, sp.Rational(1, 2), evaluate=False))


# ---------------------------------------------------------------------------------- derivatives


def derivative_power(rng: random.Random) -> Line:
    n, m = rng.sample([2, 3, 4, 5, 6], 2)
    a, b, c = _nonzero(rng, -6, 6), _nonzero(rng, -6, 6), _nonzero(rng, -9, 9)
    return Line("function", expr=ordered(a * X**n + b * X**m + c * X))


def derivative_chain_linear(rng: random.Random) -> Line:
    a, b, n = rng.randint(2, 4), _nonzero(rng, -5, 5), rng.randint(2, 3)
    return Line("function", expr=sp.Pow(ordered(a * X + b), n, evaluate=False))


def derivative_product(rng: random.Random) -> Line:
    n = rng.randint(2, 4)
    other = rng.choice([sp.sin(X), sp.cos(X), sp.exp(X)])
    return Line("function", expr=mul(sp.Pow(X, n, evaluate=False), other))


def derivative_chain_function(rng: random.Random) -> Line:
    a, n = rng.randint(2, 5), rng.randint(2, 3)
    outer = rng.choice([sp.sin, sp.cos, sp.exp])
    return Line("operator", expr=outer(mul(sp.Integer(a), sp.Pow(X, n, evaluate=False)), evaluate=False))


# ---------------------------------------------------------------------------------- inequalities


def inequality_linear(rng: random.Random) -> Line:
    a = rng.choice([-5, -4, -3, -2, -1, 2, 3, 4, -2, -3])  # mostly negative: the flip matters
    b, bound = _nonzero(rng, -9, 9), rng.randint(-6, 6)
    op = rng.choice(["<", ">", "<=", ">="])
    return relation_line(ordered(a * X + b), sp.Integer(a * bound + b), op)


def inequality_bracket(rng: random.Random) -> Line:
    a, b = rng.choice([-4, -3, -2, 2, 3]), _nonzero(rng, -5, 5)
    c = rng.choice([k for k in range(-3, 6) if k not in (0, a)])
    bound = rng.randint(-6, 6)
    d = a * (bound + b) - c * bound
    op = rng.choice(["<", ">", "<=", ">="])
    return relation_line(mul(sp.Integer(a), add(X, sp.Integer(b))), ordered(c * X + d), op)


SOLVE, SIMPLIFY, EXPAND, FACTOR, DIFF = "Solve for x", "Simplify", "Expand and simplify", "Factor", "Differentiate with respect to x"

TEMPLATES: tuple[Template, ...] = (
    Template("linear_bracket", "linear_equation", SOLVE, linear_bracket, LINEAR,
             ("distribute_first_term_only", "sign_not_flipped_on_move", "divide_one_term_only", "arithmetic_slip")),
    Template("linear_two_sided", "linear_equation", SOLVE, linear_two_sided, LINEAR,
             ("sign_not_flipped_on_move", "divide_one_term_only", "arithmetic_slip")),
    Template("linear_divide_first", "linear_equation", SOLVE, linear_divide_first, LINEAR_DIVIDE_FIRST,
             ("divide_one_term_only", "sign_not_flipped_on_move", "arithmetic_slip")),
    Template("linear_fractions", "linear_equation", SOLVE, linear_fractions, LINEAR,
             ("add_fractions_add_denominators", "arithmetic_slip")),
    Template("linear_cross_multiply", "linear_equation", SOLVE, linear_cross_multiply, LINEAR,
             ("sign_not_flipped_on_move", "arithmetic_slip")),
    Template("quadratic_factor", "quadratic_equation", SOLVE, quadratic_factor, QUADRATIC,
             ("sign_not_flipped_on_move", "arithmetic_slip")),
    Template("quadratic_square_root", "quadratic_equation", SOLVE, quadratic_square_root, QUADRATIC,
             ("sqrt_missing_pm", "square_of_sum", "arithmetic_slip")),
    Template("quadratic_common_factor", "quadratic_equation", SOLVE, quadratic_common_factor, QUADRATIC,
             ("divide_by_variable", "arithmetic_slip")),
    Template("complete_square", "quadratic_equation", SOLVE, complete_square, COMPLETE_SQUARE,
             ("sign_not_flipped_on_move", "sqrt_missing_pm", "arithmetic_slip")),
    Template("radical_squaring", "quadratic_equation", SOLVE, radical_squaring, RADICAL,
             ("square_of_sum", "arithmetic_slip")),
    Template("rational_cancel", "rational_expression", SIMPLIFY, rational_cancel, RATIONAL,
             ("cancel_across_addition", "arithmetic_slip")),
    Template("rational_add", "rational_expression", SIMPLIFY, rational_add, RATIONAL,
             ("add_fractions_add_denominators", "distribute_first_term_only", "arithmetic_slip")),
    Template("rational_numeric_denominator", "rational_expression", SIMPLIFY, rational_numeric_denominator, RATIONAL,
             ("divide_one_term_only", "arithmetic_slip")),
    Template("poly_square_expand", "polynomial", EXPAND, poly_square_expand, POLYNOMIAL,
             ("square_of_sum", "arithmetic_slip")),
    Template("poly_distribute", "polynomial", EXPAND, poly_distribute, POLYNOMIAL,
             ("distribute_first_term_only", "arithmetic_slip")),
    Template("poly_foil", "polynomial", EXPAND, poly_foil, POLYNOMIAL, ("arithmetic_slip",)),
    Template("poly_factor", "polynomial", FACTOR, poly_factor, (t.factor_expression,), ("arithmetic_slip",)),
    Template("exponent_product", "powers_roots", SIMPLIFY, exponent_product, POWERS,
             ("exponent_product_multiply", "arithmetic_slip")),
    Template("pythagorean", "powers_roots", SIMPLIFY, pythagorean, POWERS, ("sqrt_of_sum", "arithmetic_slip")),
    Template("derivative_power", "derivative", DIFF, derivative_power, (t.differentiate_line,),
             ("power_rule_no_decrement", "arithmetic_slip")),
    Template("derivative_chain_linear", "derivative", DIFF, derivative_chain_linear,
             (t.differentiate_line, t.expand_derivative),
             ("chain_rule_omitted", "power_rule_no_decrement", "arithmetic_slip")),
    Template("derivative_product", "derivative", DIFF, derivative_product, (t.differentiate_line, t.factor_derivative),
             ("product_rule_as_product", "power_rule_no_decrement")),
    Template("derivative_chain_function", "derivative", DIFF, derivative_chain_function, (t.differentiate_line,),
             ("chain_rule_omitted", "arithmetic_slip")),
    Template("inequality_linear", "inequality", "Solve the inequality", inequality_linear, LINEAR,
             ("inequality_not_flipped", "sign_not_flipped_on_move", "arithmetic_slip")),
    Template("inequality_bracket", "inequality", "Solve the inequality", inequality_bracket, LINEAR,
             ("distribute_first_term_only", "inequality_not_flipped", "arithmetic_slip")),
)
