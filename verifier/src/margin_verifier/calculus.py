"""A small differentiator that can make classic student mistakes on purpose.

With bug=None it agrees with sympy.diff (see tests). The bugs model:
  power_no_decrement:  d/dx u^n  -> n u^n u'      (exponent not reduced)
  chain_omitted:       d/dx f(u) -> f'(u)         (inner derivative forgotten)
  product_as_product:  d/dx (u v) -> u' v'
"""

from __future__ import annotations

import sympy as sp

BUGS = ("power_no_decrement", "chain_omitted", "product_as_product")


def differentiate(expr: sp.Expr, x: sp.Symbol, bug: str | None = None) -> sp.Expr:
    """d/dx expr using textbook rules, optionally applying one `bug` everywhere."""
    if not expr.has(x):
        return sp.Integer(0)
    if expr == x:
        return sp.Integer(1)
    if isinstance(expr, sp.Add):
        return sp.Add(*[differentiate(term, x, bug) for term in expr.args])
    if isinstance(expr, sp.Mul):
        return _product(expr, x, bug)
    if isinstance(expr, sp.Pow):
        return _power(expr, x, bug)
    if isinstance(expr, sp.Function) and len(expr.args) == 1:
        inner = expr.args[0]
        t = sp.Dummy("t")
        outer = sp.diff(expr.func(t), t).subs(t, inner)
        return outer * _inner_factor(inner, x, bug)
    return sp.diff(expr, x)  # anything exotic: no student-bug model


def _product(expr: sp.Mul, x: sp.Symbol, bug: str | None) -> sp.Expr:
    constant, rest = expr.as_independent(x, as_Add=False)
    if constant != 1:
        return constant * differentiate(rest, x, bug)
    first, *others = rest.args
    second = sp.Mul(*others)
    d_first, d_second = differentiate(first, x, bug), differentiate(second, x, bug)
    if bug == "product_as_product":
        return d_first * d_second
    return d_first * second + first * d_second


def _power(expr: sp.Pow, x: sp.Symbol, bug: str | None) -> sp.Expr:
    base, exponent = expr.args
    if exponent.has(x) and base.has(x):
        return sp.diff(expr, x)  # x^x style: no student-bug model
    if exponent.has(x):  # a^u
        return expr * sp.log(base) * _inner_factor(exponent, x, bug)
    new_exponent = exponent if bug == "power_no_decrement" else exponent - 1
    return exponent * base**new_exponent * _inner_factor(base, x, bug)


def _inner_factor(inner: sp.Expr, x: sp.Symbol, bug: str | None) -> sp.Expr:
    """The chain-rule factor u' (dropped when modelling the chain-rule bug)."""
    if bug == "chain_omitted" and inner != x:
        return sp.Integer(1)
    return differentiate(inner, x, bug)


def buggy_derivatives(function: sp.Expr, x: sp.Symbol, bug: str) -> list[sp.Expr]:
    """Wrong derivatives a student could produce with `bug`: applied to every
    term, or to just one term of a sum. Only results that are actually wrong."""
    correct = sp.expand(differentiate(function, x))
    candidates = [differentiate(function, x, bug)]
    terms = function.args if isinstance(function, sp.Add) else ()
    for index in range(len(terms)):
        candidates.append(
            sp.Add(*[differentiate(t, x, bug if i == index else None) for i, t in enumerate(terms)])
        )
    unique: list[sp.Expr] = []
    for candidate in candidates:
        if sp.expand(candidate - correct) != 0 and candidate not in unique:
            unique.append(candidate)
    return unique
