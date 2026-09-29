"""The mal-rule library: classic student mistakes, written as buggy transformations.

Each rule turns the *previous* line into the wrong lines a student applying that
mistake could write. The same function serves two purposes:
  * diagnosis - if one of the candidates is equivalent to the student's line,
    that rule explains the error (verifier.py);
  * injection - pick one candidate to create a realistic wrong step (synth/).

Rules come in four shapes:
  expression rules  expr -> [expr]              (work anywhere, incl. equation sides)
  relation rules    (lhs, op, rhs), x -> [branches]   (equations / inequalities)
  derivative rules  f, x -> [wrong f']
  arithmetic_slip   special: the *student's* line is one small constant away from right.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from itertools import combinations

import sympy as sp

from margin_verifier.calculus import buggy_derivatives
from margin_verifier.equivalence import evaluated
from margin_verifier.tree import add, fraction, mul, replace_at, split_fraction, terms_of, walk

SurfaceBranch = tuple[sp.Expr, str, sp.Expr]  # (lhs, op, rhs) as written (unevaluated)

EXPRESSION, RELATION, DERIVATIVE, SLIP = "expression", "relation", "derivative", "slip"


@dataclass(frozen=True)
class MalRule:
    id: str
    kind: str  # EXPRESSION | RELATION | DERIVATIVE | SLIP
    hint: str  # what the app may say: a nudge, never the answer
    candidates: Callable[..., list] | None  # see module docstring for the signature per kind


# --------------------------------------------------------------------------- expression rules


def _distribute_to_one_term(expr: sp.Expr) -> list[sp.Expr]:
    """a(b + c) -> ab + c : the multiplier reaches only one term of the bracket."""
    out = []
    for path, node in walk(expr):
        if not isinstance(node, sp.Mul):
            continue
        for k, factor in enumerate(node.args):
            if not isinstance(factor, sp.Add):
                continue
            multiplier = mul(*(node.args[:k] + node.args[k + 1 :]))
            if multiplier.has(sp.Add):
                continue  # (a + b)(c + d) is a different skill (FOIL), not this mistake
            for i, term in enumerate(factor.args):
                others = factor.args[:i] + factor.args[i + 1 :]
                out.append(replace_at(expr, path, add(mul(multiplier, term), *others)))
    return out


def _square_each_term(expr: sp.Expr) -> list[sp.Expr]:
    """(a + b)^2 -> a^2 + b^2   (and the sign-keeping variant (a - b)^2 -> a^2 - b^2)."""
    out = []
    for path, node in walk(expr):
        if isinstance(node, sp.Pow) and node.exp == 2 and isinstance(node.base, sp.Add):
            terms = node.base.args
            out.append(replace_at(expr, path, add(*[sp.Pow(t, 2, evaluate=False) for t in terms])))
            signed = [_signed_square(t) for t in terms]
            out.append(replace_at(expr, path, add(*signed)))
    return out


def _signed_square(term: sp.Expr) -> sp.Expr:
    value = evaluated(term)
    if value.could_extract_minus_sign():
        return mul(sp.Integer(-1), sp.Pow(-value, 2, evaluate=False))
    return sp.Pow(term, 2, evaluate=False)


def _sqrt_each_term(expr: sp.Expr) -> list[sp.Expr]:
    """sqrt(a^2 + b^2) -> a + b."""
    out = []
    for path, node in walk(expr):
        if isinstance(node, sp.Pow) and node.exp == sp.Rational(1, 2) and isinstance(node.base, sp.Add):
            roots = [sp.Pow(t, sp.Rational(1, 2), evaluate=False) for t in node.base.args]
            out.append(replace_at(expr, path, add(*roots)))
    return out


def _cancel_added_terms(expr: sp.Expr) -> list[sp.Expr]:
    """(x^2 + 3)/(x^2 + 5) -> 3/5 : 'cancelling' a term that is added, not a factor."""
    out = []
    for path, node in walk(expr):
        parts = split_fraction(node)
        if parts is None:
            continue
        top, bottom = terms_of(parts[0]), terms_of(parts[1])
        if len(top) + len(bottom) < 3:
            continue  # need a sum on at least one side
        for i, t in enumerate(top):
            for j, b in enumerate(bottom):
                if evaluated(t) != evaluated(b):
                    continue
                new_top = add(*(top[:i] + top[i + 1 :])) if len(top) > 1 else sp.Integer(1)
                new_bottom = add(*(bottom[:j] + bottom[j + 1 :])) if len(bottom) > 1 else sp.Integer(1)
                out.append(replace_at(expr, path, fraction(new_top, new_bottom)))
    return out


def _add_across(expr: sp.Expr) -> list[sp.Expr]:
    """a/b + c/d -> (a + c)/(b + d)."""
    out = []
    for path, node in walk(expr):
        if not isinstance(node, sp.Add):
            continue
        fractions = [(k, split_fraction(t)) for k, t in enumerate(node.args)]
        fractions = [(k, parts) for k, parts in fractions if parts is not None]
        for (i, (a, b)), (j, (c, d)) in combinations(fractions, 2):
            merged = fraction(add(a, c), add(b, d))
            rest = [t for k, t in enumerate(node.args) if k not in (i, j)]
            out.append(replace_at(expr, path, add(merged, *rest)))
    return out


def _multiply_exponents(expr: sp.Expr) -> list[sp.Expr]:
    """x^a * x^b -> x^(ab)   and   x^a / x^b -> x^(a/b)."""
    out = []
    for path, node in walk(expr):
        if not isinstance(node, sp.Mul):
            continue
        factors = _flat_factors(node)
        powers = [(k, *_base_and_exponent(f)) for k, f in enumerate(factors)]
        for (i, base1, exp1), (j, base2, exp2) in combinations(powers, 2):
            if not base1.free_symbols or evaluated(base1) != evaluated(base2):
                continue
            if (exp1 == 1 and exp2 == 1) or exp1 == -1 or exp2 == -1:
                continue
            if exp2.could_extract_minus_sign():
                wrong = sp.Pow(base1, fraction(exp1, -exp2), evaluate=False)
            else:
                wrong = sp.Pow(base1, mul(exp1, exp2), evaluate=False)
            rest = [f for k, f in enumerate(factors) if k not in (i, j)]
            out.append(replace_at(expr, path, mul(*rest, wrong)))
    return out


def _flat_factors(node: sp.Mul) -> list[sp.Expr]:
    """Factors of a product, looking inside nested products: (5x^3)(2x^6) -> 5, x^3, 2, x^6."""
    factors: list[sp.Expr] = []
    for factor in node.args:
        factors.extend(_flat_factors(factor) if isinstance(factor, sp.Mul) else [factor])
    return factors


def _base_and_exponent(factor: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """x^3 -> (x, 3); (x^2)^-1 -> (x, -2); x -> (x, 1)."""
    if isinstance(factor, sp.Pow):
        base, exponent = factor.args
        if isinstance(base, sp.Pow) and exponent == -1:
            return base.base, -base.exp
        return base, exponent
    return factor, sp.Integer(1)


def _divide_one_term_expression(expr: sp.Expr) -> list[sp.Expr]:
    """(2x + 4)/2 -> x + 4 : only one term of the numerator gets divided."""
    out = []
    for path, node in walk(expr):
        parts = split_fraction(node)
        if parts is None or not evaluated(parts[1]).is_number:
            continue
        top, divisor = terms_of(parts[0]), parts[1]
        if len(top) < 2:
            continue
        for i, term in enumerate(top):
            divided = fraction(term, divisor)
            out.append(replace_at(expr, path, add(*(top[:i] + (divided,) + top[i + 1 :]))))
    return out


# ----------------------------------------------------------------------------- relation rules


def _move_without_sign_change(branch: SurfaceBranch, x: sp.Symbol) -> list[tuple[SurfaceBranch, ...]]:
    """2x + 3 = 7 -> 2x = 7 + 3 : a term crosses the relation sign keeping its sign."""
    lhs, op, rhs = branch
    out = []
    left, right = terms_of(lhs), terms_of(rhs)
    for i, term in enumerate(left if len(left) > 1 else ()):  # a term moved out of a sum
        out.append(((add(*(left[:i] + left[i + 1 :])), op, add(rhs, term)),))
    for i, term in enumerate(right if len(right) > 1 else ()):
        out.append(((add(lhs, term), op, add(*(right[:i] + right[i + 1 :]))),))
    return out


def _divide_part(branch: SurfaceBranch, x: sp.Symbol) -> list[tuple[SurfaceBranch, ...]]:
    """2x + 4 = 10 -> x + 4 = 5 : dividing by a constant, but not every term."""
    lhs, op, rhs = branch
    out = []
    for c in _coefficients(branch, x):
        for side_index, side in ((0, lhs), (1, rhs)):
            other = rhs if side_index == 0 else lhs
            terms = terms_of(side)
            if len(terms) < 2:
                continue
            for i in range(len(terms)):
                divided = add(*(terms[:i] + (fraction(terms[i], c),) + terms[i + 1 :]))
                if side_index == 0:
                    out.append(((divided, _flip_if(op, c), fraction(other, c)),))
                else:
                    out.append(((fraction(other, c), _flip_if(op, c), divided),))
        out.append(((fraction(lhs, c), _flip_if(op, c), rhs),))  # one side not divided at all
        out.append(((lhs, _flip_if(op, c), fraction(rhs, c)),))
    return out


def _coefficients(branch: SurfaceBranch, x: sp.Symbol) -> list[sp.Expr]:
    """Numeric coefficients of the x-terms: the numbers a student would divide by."""
    found: list[sp.Expr] = []
    for side in (branch[0], branch[2]):
        for term in terms_of(evaluated(side)):
            coefficient = term.as_coeff_Mul()[0]
            if term.has(x) and coefficient not in (0, 1, -1) and coefficient not in found:
                found.append(coefficient)
    return found


def _flip_if(op: str, c: sp.Expr) -> str:
    """Correct direction after dividing by c (so this rule models only the 'part' error)."""
    if op in ("=", "!=") or c > 0:
        return op
    return {"<": ">", ">": "<", "<=": ">=", ">=": "<="}[op]


def _root_without_pm(branch: SurfaceBranch, x: sp.Symbol) -> list[tuple[SurfaceBranch, ...]]:
    """x^2 = 9 -> x = 3 ;  (x+1)^2 = 16 -> x + 1 = 4  (the negative root is forgotten)."""
    lhs, op, rhs = (evaluated(branch[0]), branch[1], evaluated(branch[2]))
    if op != "=":
        return []
    out = []
    for square, other in ((lhs, rhs), (rhs, lhs)):
        if isinstance(square, sp.Pow) and square.exp == 2 and square.has(x) and not other.has(x):
            out.append(((square.base, "=", sp.sqrt(other)),))
    return out


def _divide_by_x_factor(branch: SurfaceBranch, x: sp.Symbol) -> list[tuple[SurfaceBranch, ...]]:
    """x^2 = 4x -> x = 4 : dividing both sides by something that can be zero."""
    lhs, op, rhs = (evaluated(branch[0]), branch[1], evaluated(branch[2]))
    if op != "=" or not (lhs.is_polynomial(x) and rhs.is_polynomial(x)):
        return []
    common = lhs if rhs == 0 else rhs if lhs == 0 else sp.gcd(lhs, rhs)
    out = []
    for factor, _ in sp.factor_list(common, x)[1]:
        if not factor.has(x):
            continue
        new_lhs, new_rhs = sp.cancel(lhs / factor), sp.cancel(rhs / factor)
        if new_lhs.has(x) or new_rhs.has(x):
            out.append(((new_lhs, "=", new_rhs),))
    return out


def _keep_inequality_direction(branch: SurfaceBranch, x: sp.Symbol) -> list[tuple[SurfaceBranch, ...]]:
    """-2x > 4 -> x > -2 : divided by a negative number without flipping the sign."""
    lhs, op, rhs = (evaluated(branch[0]), branch[1], evaluated(branch[2]))
    if op not in ("<", "<=", ">", ">="):
        return []
    residual = sp.expand(lhs - rhs)
    if not residual.is_polynomial(x) or sp.degree(residual, x) != 1:
        return []
    a, b = residual.coeff(x, 1), residual.coeff(x, 0)
    if not (a.is_number and a < 0):
        return []
    return [((x, op, -b / a),)]


# ---------------------------------------------------------------------------- derivative rules


def _derivative_rule(bug: str) -> Callable[[sp.Expr, sp.Symbol], list[sp.Expr]]:
    def candidates(function: sp.Expr, x: sp.Symbol) -> list[sp.Expr]:
        return buggy_derivatives(evaluated(function), x, bug)

    return candidates


# -------------------------------------------------------------------------------- the library

RULES: tuple[MalRule, ...] = (
    MalRule("sqrt_missing_pm", RELATION,
            "Taking a square root gives two possibilities: a positive and a negative one.",
            _root_without_pm),
    MalRule("divide_by_variable", RELATION,
            "Dividing both sides by an expression with x in it can lose a solution. What if it is 0?",
            _divide_by_x_factor),
    MalRule("inequality_not_flipped", RELATION,
            "Multiplying or dividing an inequality by a negative number flips the inequality sign.",
            _keep_inequality_direction),
    MalRule("sign_not_flipped_on_move", RELATION,
            "When a term moves to the other side, its sign changes.",
            _move_without_sign_change),
    MalRule("divide_one_term_only", RELATION,
            "When you divide, every term on both sides has to be divided.",
            _divide_part),
    MalRule("divide_one_term_only", EXPRESSION,
            "When you divide, every term of the numerator has to be divided.",
            _divide_one_term_expression),
    MalRule("distribute_first_term_only", EXPRESSION,
            "Multiply the factor outside the brackets by every term inside.",
            _distribute_to_one_term),
    MalRule("square_of_sum", EXPRESSION,
            "(a + b)^2 means (a + b)(a + b). Is there a middle term?",
            _square_each_term),
    MalRule("sqrt_of_sum", EXPRESSION,
            "The square root of a sum is not the sum of the square roots.",
            _sqrt_each_term),
    MalRule("cancel_across_addition", EXPRESSION,
            "Only common factors cancel, not terms that are added.",
            _cancel_added_terms),
    MalRule("add_fractions_add_denominators", EXPRESSION,
            "To add fractions, use a common denominator; denominators are not added.",
            _add_across),
    MalRule("exponent_product_multiply", EXPRESSION,
            "Multiplying powers of the same base: add the exponents (dividing: subtract).",
            _multiply_exponents),
    MalRule("power_rule_no_decrement", DERIVATIVE,
            "Power rule: bring the exponent down and lower the exponent by one.",
            _derivative_rule("power_no_decrement")),
    MalRule("chain_rule_omitted", DERIVATIVE,
            "The inside is not just x. Remember the chain rule.",
            _derivative_rule("chain_omitted")),
    MalRule("product_rule_as_product", DERIVATIVE,
            "The derivative of a product is not the product of the derivatives.",
            _derivative_rule("product_as_product")),
    MalRule("arithmetic_slip", SLIP, "Double-check the arithmetic in this step.", None),
)

RULE_IDS: tuple[str, ...] = tuple(dict.fromkeys(rule.id for rule in RULES))


def hint_for(rule_id: str) -> str | None:
    for rule in RULES:
        if rule.id == rule_id:
            return rule.hint
    return None


# ------------------------------------------------------------------------ candidate generation


def expression_candidates(rule: MalRule, expr: sp.Expr) -> list[sp.Expr]:
    return rule.candidates(expr) if rule.kind == EXPRESSION else []


def relation_candidates(
    rule: MalRule, branches: tuple[SurfaceBranch, ...], x: sp.Symbol
) -> list[tuple[SurfaceBranch, ...]]:
    """Wrong next lines for an equation/inequality line (one branch changed at a time)."""
    out: list[tuple[SurfaceBranch, ...]] = []
    for index, branch in enumerate(branches):
        if rule.kind == RELATION:
            replacements = rule.candidates(branch, x)
        elif rule.kind == EXPRESSION:
            lhs, op, rhs = branch
            replacements = [((new, op, rhs),) for new in rule.candidates(lhs)]
            replacements += [((lhs, op, new),) for new in rule.candidates(rhs)]
        else:
            replacements = []
        for replacement in replacements:
            out.append(branches[:index] + replacement + branches[index + 1 :])
    return out


def derivative_candidates(rule: MalRule, function: sp.Expr, x: sp.Symbol) -> list[sp.Expr]:
    return rule.candidates(function, x) if rule.kind == DERIVATIVE else []


# ------------------------------------------------------------------------------ arithmetic slip

_SLIP_DELTAS = (1, -1, 2, -2)


def slip_variants(expr: sp.Expr) -> list[sp.Expr]:
    """Copies of `expr` with one number changed a little (k+-1, k+-2, -k).

    Used backwards for diagnosis (does fixing one number make the step right?)
    and forwards for injection (break one number of a correct line)."""
    out = []
    for path, node in walk(expr):
        if not isinstance(node, sp.Rational) or _parent_is(expr, path, sp.Pow):
            continue  # exponents have their own rules (and b^-1 is just notation)
        for new in [node + d for d in _SLIP_DELTAS] + [-node]:
            if new == node or (new == 0 and _parent_is(expr, path, sp.Mul)):
                continue  # a coefficient slipping to 0 would be a dropped term, not a slip
            out.append(replace_at(expr, path, new))
    return out


def _parent_is(expr: sp.Expr, path: tuple[int, ...], kind: type) -> bool:
    """Is the node at `path` an exponent (kind=Pow) or a factor (kind=Mul) of its parent?"""
    if not path:
        return False
    parent = expr
    for index in path[:-1]:
        parent = parent.args[index]
    if kind is sp.Pow:
        return isinstance(parent, sp.Pow) and path[-1] == 1
    return isinstance(parent, kind)
