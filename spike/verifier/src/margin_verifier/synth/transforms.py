"""Correct solution steps used by the generator.

Each transform takes the current line (and the lines so far) and returns the
next line, or None when it does not apply. A solver is a priority list of
transforms applied until none fires, so it can also carry on from a *wrong*
line, like a student who does not notice their mistake.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import reduce

import sympy as sp

from margin_verifier.synth.lines import X, Line, ev, ordered, relation_line, single_branch, terms
from margin_verifier.synth.render import latex, negate
from margin_verifier.tree import add, fraction, mul, split_fraction, walk

Transform = Callable[[Line, list[Line]], "Line | None"]

_FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<=", "=": "=", "!=": "!="}


def _has_bracket_product(expr: sp.Expr) -> bool:
    """Something like 3(x + 2) or (x + 1)^2 that can be multiplied out.
    A plain fraction of a sum, (x + 1)/2, does not count."""
    for _, node in walk(expr):
        if isinstance(node, sp.Mul) and any(isinstance(f, sp.Add) for f in node.args):
            multipliers = [f for f in node.args if not isinstance(f, sp.Add) and not _is_reciprocal(f)]
            if multipliers or sum(isinstance(f, sp.Add) for f in node.args) > 1:
                return True
        if isinstance(node, sp.Pow) and isinstance(node.base, sp.Add) and node.exp.is_Integer and node.exp > 0:
            return True
    return False


def _is_reciprocal(factor: sp.Expr) -> bool:
    return isinstance(factor, sp.Pow) and factor.exp.is_Integer and factor.exp < 0


def _scaled(side: sp.Expr, factor: sp.Expr) -> sp.Expr:
    """Every term of `side` multiplied by `factor`, written in textbook order."""
    return add(*[ordered(term * factor) for term in terms(ordered(sp.expand(ev(side))))])


def _only_reordered(before: sp.Expr, after: sp.Expr) -> bool:
    return sorted(latex(t) for t in terms(before)) == sorted(latex(t) for t in terms(after))


# ------------------------------------------------------------------ linear equations / inequalities


def expand_brackets(line: Line, history: list[Line]) -> Line | None:
    branch = single_branch(line)
    if branch is None or not (_has_bracket_product(branch[0]) or _has_bracket_product(branch[2])):
        return None
    lhs, op, rhs = branch
    return relation_line(ordered(sp.expand(ev(lhs))), ordered(sp.expand(ev(rhs))), op)


def clear_fractions(line: Line, history: list[Line]) -> Line | None:
    """x/2 + x/3 = 5  ->  3x + 2x = 30 (multiply every term by the LCD)."""
    branch = single_branch(line)
    if branch is None:
        return None
    lhs, op, rhs = branch
    if lhs == X and not rhs.has(X):
        return None  # already solved: 'x < 4/3' stays as it is
    all_terms = terms(sp.expand(ev(lhs))) + terms(sp.expand(ev(rhs)))
    denominators = [t.as_numer_denom()[1] for t in all_terms]
    if not all(d.is_Integer for d in denominators):
        return None
    lcd = reduce(sp.ilcm, [int(d) for d in denominators], 1)
    if lcd == 1:
        return None
    return relation_line(_scaled(lhs, lcd), _scaled(rhs, lcd), op)


def combine_like_terms(line: Line, history: list[Line]) -> Line | None:
    branch = single_branch(line)
    if branch is None:
        return None
    lhs, op, rhs = branch
    new_lhs, new_rhs = ordered(ev(lhs)), ordered(ev(rhs))
    if _only_reordered(lhs, new_lhs) and _only_reordered(rhs, new_rhs):
        return None
    return relation_line(new_lhs, new_rhs, op)


def divide_through(line: Line, history: list[Line]) -> Line | None:
    """2x + 4 = 10  ->  x + 2 = 5 (every term shares a factor)."""
    branch = single_branch(line)
    if branch is None:
        return None
    lhs, op, rhs = branch
    left, right = terms(sp.expand(ev(lhs))), terms(sp.expand(ev(rhs)))
    if len(left) < 2 or not any(t.has(X) for t in left):
        return None
    coefficients = [t.as_coeff_Mul()[0] for t in left + right]
    if not all(c.is_Integer for c in coefficients):
        return None
    divisor = reduce(sp.igcd, [abs(int(c)) for c in coefficients])
    if divisor <= 1:
        return None
    return relation_line(_scaled(lhs, sp.Rational(1, divisor)), _scaled(rhs, sp.Rational(1, divisor)), op)


def swap_sides(line: Line, history: list[Line]) -> Line | None:
    branch = single_branch(line)
    if branch is None or ev(branch[0]).has(X) or not ev(branch[2]).has(X):
        return None
    lhs, op, rhs = branch
    return relation_line(rhs, lhs, _FLIP[op])


def move_terms(line: Line, history: list[Line]) -> Line | None:
    """x-terms to the left, numbers to the right: 3x + 6 = 2x - 5 -> 3x - 2x = -5 - 6."""
    branch = single_branch(line)
    if branch is None:
        return None
    lhs, op, rhs = branch
    left, right = terms(ordered(ev(lhs))), terms(ordered(ev(rhs)))
    left_x = [t for t in left if t.has(X)]
    left_numbers = [t for t in left if not t.has(X) and t != 0]
    right_x = [t for t in right if t.has(X)]
    right_numbers = [t for t in right if not t.has(X) and t != 0]
    if not left_x or (not right_x and not left_numbers):
        return None
    new_lhs = add(*left_x, *[negate(t) for t in right_x])
    new_rhs = add(*right_numbers, *[negate(t) for t in left_numbers])
    return relation_line(new_lhs, new_rhs, op)


def divide_by_coefficient(line: Line, history: list[Line]) -> Line | None:
    """3x = 12 -> x = 4 ; -2x > 4 -> x < -2."""
    branch = single_branch(line)
    if branch is None:
        return None
    lhs, op, rhs = branch
    coefficient, rest = ev(lhs).as_coeff_Mul()
    if rest != X or coefficient in (0, 1) or ev(rhs).has(X):
        return None
    new_op = _FLIP[op] if coefficient < 0 else op
    return relation_line(X, ordered(ev(rhs) / coefficient), new_op)


# ------------------------------------------------------------------------------------- quadratics


def _is_solved(branch) -> bool:
    lhs, op, rhs = branch
    return op == "=" and lhs == X and not rhs.has(X) and rhs == ev(rhs)


def solve_linear_branches(line: Line, history: list[Line]) -> Line | None:
    """x - 2 = 0 or x - 3 = 0 -> x = 2 or x = 3 (also a single linear equation)."""
    if line.kind != "relation" or all(_is_solved(b) for b in line.branches):
        return None
    values = []
    for lhs, op, rhs in line.branches:
        residual = sp.expand(ev(lhs) - ev(rhs))
        if op != "=" or not residual.is_polynomial(X) or sp.degree(residual, X) != 1:
            return None
        value = sp.solve(residual, X)[0]
        if value not in values:
            values.append(value)
    return Line("relation", branches=tuple((X, "=", ordered(v)) for v in values))


def isolate_pm(line: Line, history: list[Line]) -> Line | None:
    """x + 1 = \\pm 4 -> x = -1 \\pm 4."""
    if line.pm is None or line.branches[0][0] == X:
        return None
    shift = ev(line.branches[0][0]) - X
    if shift.has(X) or shift == 0:
        return None
    offset = line.pm[1]
    branches = ((X, "=", add(-shift, offset)), (X, "=", add(-shift, negate(offset))))
    return Line("relation", branches=branches, pm=(-shift, offset))


def square_root_both_sides(line: Line, history: list[Line]) -> Line | None:
    """(x + 1)^2 = 16 -> x + 1 = \\pm 4."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=":
        return None
    square, value = ev(branch[0]), ev(branch[2])
    if not (isinstance(square, sp.Pow) and square.exp == 2 and square.base.has(X)):
        return None
    if value.has(X) or value < 0:
        return None
    root = sp.sqrt(value)
    base = ordered(square.base)
    if root == 0:
        return relation_line(base, sp.Integer(0))
    return Line("relation", branches=((base, "=", root), (base, "=", -root)), pm=(sp.Integer(0), root))


def split_zero_product(line: Line, history: list[Line]) -> Line | None:
    """(x - 2)(x - 3) = 0 -> x - 2 = 0 or x - 3 = 0."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=" or ev(branch[2]) != 0 or not isinstance(branch[0], sp.Mul):
        return None
    factors = []
    for factor in branch[0].args:
        base = factor.base if isinstance(factor, sp.Pow) and factor.exp.is_Integer else factor
        if base.has(X) and base not in factors:
            factors.append(base)
    if len(factors) < 2:
        return None
    return Line("relation", branches=tuple((f, "=", sp.Integer(0)) for f in factors))


def isolate_square(line: Line, history: list[Line]) -> Line | None:
    """2x^2 - 18 = 0 -> x^2 = 9 (no x term)."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=":
        return None
    residual = sp.expand(ev(branch[0]) - ev(branch[2]))
    if not residual.is_polynomial(X) or sp.degree(residual, X) != 2 or residual.coeff(X, 1) != 0:
        return None
    if ev(branch[0]) == X**2:
        return None
    a, c = residual.coeff(X, 2), residual.coeff(X, 0)
    return relation_line(X**2, ordered(-c / a))


def move_everything_left(line: Line, history: list[Line]) -> Line | None:
    """x + 3 = x^2 - 6x + 9 -> x^2 - 7x + 6 = 0 (leading coefficient kept positive)."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=" or ev(branch[2]) == 0:
        return None
    lhs, rhs = ev(branch[0]), ev(branch[2])
    if isinstance(lhs, sp.Pow) and lhs.exp == 2 and not rhs.has(X):
        return None  # a square equal to a number: take the square root instead
    residual = sp.expand(lhs - rhs)
    if not residual.is_polynomial(X) or sp.degree(residual, X) < 2:
        return None
    if sp.LC(residual, X) < 0:
        residual = -residual
    return relation_line(ordered(residual), sp.Integer(0))


def factor_polynomial(line: Line, history: list[Line]) -> Line | None:
    """x^2 - 5x + 6 = 0 -> (x - 2)(x - 3) = 0 (only into linear factors)."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=" or ev(branch[2]) != 0 or isinstance(branch[0], sp.Mul):
        return None
    polynomial = sp.expand(ev(branch[0]))
    if not polynomial.is_polynomial(X) or sp.degree(polynomial, X) != 2:
        return None
    factored = sp.factor(polynomial)
    linear = [f for f in sp.Mul.make_args(factored) if f.has(X)]
    if len(linear) < 2 and not any(isinstance(f, sp.Pow) for f in linear):
        return None
    if not all(sp.degree(f.base if isinstance(f, sp.Pow) else f, X) == 1 for f in linear):
        return None
    return relation_line(ordered(factored), sp.Integer(0))


def quadratic_formula(line: Line, history: list[Line]) -> Line | None:
    """Fallback for quadratics that do not factor nicely."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=" or ev(branch[2]) != 0:
        return None
    polynomial = sp.expand(ev(branch[0]))
    if not polynomial.is_polynomial(X) or sp.degree(polynomial, X) != 2:
        return None
    a, b, c = (polynomial.coeff(X, k) for k in (2, 1, 0))
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None
    center, offset = -b / (2 * a), sp.sqrt(discriminant) / (2 * a)
    if offset == 0:
        return relation_line(X, center)
    offset = abs(offset)
    return Line("relation", branches=((X, "=", center + offset), (X, "=", center - offset)), pm=(center, offset))


def move_constant_right(line: Line, history: list[Line]) -> Line | None:
    """x^2 + 6x + 5 = 0 -> x^2 + 6x = -5 (first step of completing the square)."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=" or ev(branch[2]) != 0:
        return None
    polynomial = sp.expand(ev(branch[0]))
    if not polynomial.is_polynomial(X) or sp.degree(polynomial, X) != 2:
        return None
    constant = polynomial.coeff(X, 0)
    if constant == 0 or polynomial.coeff(X, 1) == 0:
        return None
    return relation_line(ordered(polynomial - constant), -constant)


def complete_the_square(line: Line, history: list[Line]) -> Line | None:
    """x^2 + 6x = -5 -> x^2 + 6x + 9 = -5 + 9."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=" or ev(branch[2]).has(X):
        return None
    polynomial = sp.expand(ev(branch[0]))
    if not polynomial.is_polynomial(X) or sp.degree(polynomial, X) != 2:
        return None
    a, b, c = (polynomial.coeff(X, k) for k in (2, 1, 0))
    if a != 1 or b == 0 or c != 0:
        return None
    square = (b / 2) ** 2
    return relation_line(add(*terms(ordered(polynomial)), square), add(branch[2], square))


def write_as_square(line: Line, history: list[Line]) -> Line | None:
    """x^2 + 6x + 9 = 4 -> (x + 3)^2 = 4."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=" or ev(branch[2]).has(X):
        return None
    polynomial = sp.expand(ev(branch[0]))
    if not polynomial.is_polynomial(X) or sp.degree(polynomial, X) != 2 or polynomial.coeff(X, 2) != 1:
        return None
    half = polynomial.coeff(X, 1) / 2
    if half == 0 or sp.expand(polynomial - (X + half) ** 2) != 0:
        return None
    return relation_line(sp.Pow(ordered(X + half), 2, evaluate=False), ordered(ev(branch[2])))


def square_both_sides(line: Line, history: list[Line]) -> Line | None:
    """sqrt(x + 3) = x - 3 -> x + 3 = (x - 3)^2 (may add an extraneous root)."""
    branch = single_branch(line)
    if branch is None or branch[1] != "=":
        return None
    lhs = branch[0]
    if not (isinstance(lhs, sp.Pow) and lhs.exp == sp.Rational(1, 2)):
        return None
    return relation_line(lhs.base, sp.Pow(branch[2], 2, evaluate=False))


def reject_extraneous(line: Line, history: list[Line]) -> Line | None:
    """Check each value in the original equation and keep the ones that work."""
    if line.kind != "relation" or len(line.branches) < 2 or not all(_is_solved(b) for b in line.branches):
        return None
    lhs, _, rhs = history[0].branches[0]
    keep = []
    for _, _, value in line.branches:
        left, right = ev(lhs).subs(X, value), ev(rhs).subs(X, value)
        if left.is_real and right.is_real and sp.simplify(left - right) == 0:
            keep.append(value)
    if not keep or len(keep) == len(line.branches):
        return None
    return Line("relation", branches=tuple((X, "=", v) for v in keep))


# ------------------------------------------------------------------------------------ expressions


def expand_each_term(line: Line, history: list[Line]) -> Line | None:
    """(x + 3)^2 - 2x -> x^2 + 6x + 9 - 2x ;  (x + 2)(x + 3) -> x^2 + 3x + 2x + 6."""
    if line.kind not in ("expr", "derivative") or not _has_bracket_product(line.expr):
        return None
    pieces: list[sp.Expr] = []
    for term in terms(line.expr):
        pieces.extend(_expand_term(term))
    return Line(line.kind, expr=add(*pieces), continuation=line.continuation)


def _expand_term(term: sp.Expr) -> list[sp.Expr]:
    sums = [f for f in sp.Mul.make_args(term) if isinstance(f, sp.Add)]
    if len(sums) == 2 and len(sp.Mul.make_args(term)) == 2:  # FOIL, written out
        first, second = sums
        return [ordered(sp.expand(a * b)) for a in first.args for b in second.args]
    if _has_bracket_product(term):
        return list(terms(ordered(sp.expand(ev(term)))))
    return [term]


def combine_terms(line: Line, history: list[Line]) -> Line | None:
    if line.kind not in ("expr", "derivative"):
        return None
    new = ordered(ev(line.expr))
    if _only_reordered(line.expr, new):
        return None
    return Line(line.kind, expr=new, continuation=line.continuation)


def factor_expression(line: Line, history: list[Line]) -> Line | None:
    if line.kind not in ("expr", "derivative") or isinstance(line.expr, sp.Mul):
        return None
    factored = sp.factor(ev(line.expr))
    if not isinstance(factored, sp.Mul) or latex(ordered(factored)) == latex(line.expr):
        return None
    return Line(line.kind, expr=ordered(factored), continuation=line.continuation)


def factor_fraction(line: Line, history: list[Line]) -> Line | None:
    """(x^2 - 9)/(x^2 + 5x + 6) -> (x - 3)(x + 3) / ((x + 2)(x + 3))  (not cancelled yet)."""
    parts = _written_fraction(line)
    if parts is None:
        return None
    new = fraction(ordered(sp.factor(parts[0])), ordered(sp.factor(parts[1])))
    if latex(new) == latex(line.expr):
        return None
    return Line("expr", expr=new)


def cancel_fraction(line: Line, history: list[Line]) -> Line | None:
    parts = _written_fraction(line)
    if parts is None:
        return None
    top, bottom = sp.fraction(sp.cancel(parts[0] / parts[1]))
    return Line("expr", expr=fraction(ordered(sp.factor(top)), ordered(sp.factor(bottom))))


def _written_fraction(line: Line) -> tuple[sp.Expr, sp.Expr] | None:
    """(numerator, denominator) as written, if they still share a factor.
    (Evaluating the whole fraction would cancel it silently.)"""
    if line.kind != "expr":
        return None
    parts = split_fraction(line.expr)
    if parts is None:
        return None
    top, bottom = ev(parts[0]), ev(parts[1])
    if not bottom.has(X) or sp.gcd(top, bottom) == 1:
        return None
    return top, bottom


def combine_fractions(line: Line, history: list[Line]) -> Line | None:
    """a/x + b/(x + 1) -> (a(x + 1) + bx) / (x(x + 1))."""
    if line.kind != "expr" or not isinstance(line.expr, sp.Add):
        return None
    parts = [sp.fraction(ev(t)) for t in line.expr.args]
    denominators = [d for _, d in parts]
    if len(set(denominators)) < 2 or not all(d.has(X) for d in denominators):
        return None
    lcd = reduce(sp.lcm, denominators)
    numerator_terms = []
    for top, bottom in parts:
        multiplier = sp.factor(sp.cancel(lcd / bottom))
        if multiplier == 1:
            numerator_terms.append(top)
        elif top == 1:
            numerator_terms.append(ordered(multiplier))
        else:
            numerator_terms.append(mul(top, ordered(multiplier)))
    return Line("expr", expr=fraction(add(*numerator_terms), ordered(sp.factor(lcd))))


def expand_numerator(line: Line, history: list[Line]) -> Line | None:
    """(5(x + 3) + 3x) / (x(x + 3)) -> (8x + 15) / (x(x + 3)); factored numerators stay."""
    if line.kind != "expr":
        return None
    numerator, denominator = sp.fraction(line.expr)
    if denominator == 1 or not isinstance(numerator, sp.Add) or not _has_bracket_product(numerator):
        return None
    return Line("expr", expr=fraction(ordered(sp.expand(ev(numerator))), denominator))


def add_exponents(line: Line, history: list[Line]) -> Line | None:
    """x^2 \\cdot x^3 -> x^{2+3}  (then combine_terms gives x^5)."""
    if line.kind != "expr" or not isinstance(line.expr, sp.Mul):
        return None
    numbers = [f for f in line.expr.args if f.is_Number]
    powers = [f for f in line.expr.args if not f.is_Number]
    bases = {f.base if isinstance(f, sp.Pow) else f for f in powers}
    if len(bases) != 1 or len(powers) < 2:
        return None
    base = bases.pop()
    exponent = add(*[f.exp if isinstance(f, sp.Pow) else sp.Integer(1) for f in powers])
    power = sp.Pow(base, exponent, evaluate=False)
    coefficient = sp.Mul(*numbers)
    return Line("expr", expr=power if coefficient == 1 else mul(coefficient, power))


def divide_powers(line: Line, history: list[Line]) -> Line | None:
    """x^7 / x^3 -> x^{7-3}."""
    if line.kind != "expr":
        return None
    top, bottom = sp.fraction(line.expr)
    if bottom == 1 or not isinstance(top, sp.Pow) or not isinstance(bottom, sp.Pow) or top.base != bottom.base:
        return None
    return Line("expr", expr=sp.Pow(top.base, add(top.exp, negate(bottom.exp)), evaluate=False))


def evaluate_squares(line: Line, history: list[Line]) -> Line | None:
    """\\sqrt{3^2 + 4^2} -> \\sqrt{9 + 16} -> \\sqrt{25} -> 5."""
    if line.kind != "expr" or line.expr.free_symbols:
        return None
    expr = line.expr
    if isinstance(expr, sp.Pow) and expr.exp == sp.Rational(1, 2):
        inside = expr.base
        if any(isinstance(t, sp.Pow) for t in terms(inside)):
            return Line("expr", expr=sp.Pow(add(*[ev(t) for t in terms(inside)]), sp.Rational(1, 2), evaluate=False))
        if isinstance(inside, sp.Add):
            return Line("expr", expr=sp.Pow(ev(inside), sp.Rational(1, 2), evaluate=False))
    value = ev(expr)
    if value != expr and value.is_Integer:
        return Line("expr", expr=value)
    return None


# ------------------------------------------------------------------------------------ derivatives


def differentiate_line(line: Line, history: list[Line]) -> Line | None:
    if line.kind not in ("function", "operator"):
        return None
    derivative = sp.diff(ev(line.expr), X)
    return Line("derivative", expr=ordered(derivative), continuation=line.kind == "operator")


def expand_derivative(line: Line, history: list[Line]) -> Line | None:
    if line.kind != "derivative" or not _has_bracket_product(line.expr):
        return None
    return Line("derivative", expr=ordered(sp.expand(ev(line.expr))), continuation=line.continuation)


def factor_derivative(line: Line, history: list[Line]) -> Line | None:
    if line.kind != "derivative" or not isinstance(line.expr, sp.Add):
        return None
    factored = sp.factor(ev(line.expr))
    if not isinstance(factored, sp.Mul) or latex(ordered(factored)) == latex(line.expr):
        return None
    return Line("derivative", expr=ordered(factored), continuation=line.continuation)


def split_numeric_fraction(line: Line, history: list[Line]) -> Line | None:
    """(6x + 9)/3 + x -> 2x + 3 + x (divide every term of the numerator)."""
    if line.kind != "expr":
        return None
    pieces: list[sp.Expr] = []
    changed = False
    for term in terms(line.expr):
        parts = split_fraction(term)
        if parts is not None and ev(parts[1]).is_Integer and isinstance(parts[0], sp.Add):
            divisor = ev(parts[1])
            pieces.extend(ordered(ev(t) / divisor) for t in terms(parts[0]))
            changed = True
        else:
            pieces.append(term)
    return Line("expr", expr=add(*pieces)) if changed else None
