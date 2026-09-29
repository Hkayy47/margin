"""Helpers for reading and rewriting *unevaluated* SymPy trees.

Mal-rules need to change one spot of what the student wrote ("this bracket",
"that fraction") without SymPy re-simplifying everything else, so all rebuilding
happens inside `sympy.evaluate(False)`.
"""

from __future__ import annotations

from collections.abc import Iterator

import sympy as sp

Path = tuple[int, ...]  # child indices from the root to a node


def walk(expr: sp.Basic) -> Iterator[tuple[Path, sp.Basic]]:
    """Every node with its path, parents before children."""
    stack: list[tuple[Path, sp.Basic]] = [((), expr)]
    while stack:
        path, node = stack.pop()
        yield path, node
        for index in reversed(range(len(node.args))):
            stack.append((path + (index,), node.args[index]))


def replace_at(expr: sp.Basic, path: Path, new: sp.Basic) -> sp.Basic:
    """Copy of `expr` with the node at `path` replaced by `new` (nothing re-simplified)."""
    if not path:
        return new
    args = list(expr.args)
    args[path[0]] = replace_at(args[path[0]], path[1:], new)
    return rebuild(expr, args)


def rebuild(node: sp.Basic, args: list[sp.Basic]) -> sp.Basic:
    with sp.evaluate(False):
        return node.func(*args)


def add(*terms: sp.Expr) -> sp.Expr:
    """Unevaluated sum; 0 for no terms, the term itself for one."""
    if not terms:
        return sp.Integer(0)
    if len(terms) == 1:
        return terms[0]
    return sp.Add(*terms, evaluate=False)


def mul(*factors: sp.Expr) -> sp.Expr:
    """Unevaluated product; 1 for no factors, the factor itself for one."""
    if not factors:
        return sp.Integer(1)
    if len(factors) == 1:
        return factors[0]
    return sp.Mul(*factors, evaluate=False)


def fraction(numerator: sp.Expr, denominator: sp.Expr) -> sp.Expr:
    """Unevaluated numerator / denominator (how '\\frac{a}{b}' is parsed)."""
    if denominator == 1:
        return numerator
    return mul(numerator, sp.Pow(denominator, -1, evaluate=False))


def terms_of(expr: sp.Expr) -> tuple[sp.Expr, ...]:
    """Additive terms as written ('a + b - c' -> a, b, -c)."""
    return expr.args if isinstance(expr, sp.Add) else (expr,)


def split_fraction(expr: sp.Expr) -> tuple[sp.Expr, sp.Expr] | None:
    """(numerator, denominator) if `expr` is written as a fraction, else None."""
    factors = expr.args if isinstance(expr, sp.Mul) else (expr,)
    top: list[sp.Expr] = []
    bottom: list[sp.Expr] = []
    for factor in factors:
        if isinstance(factor, sp.Pow) and factor.exp.is_Integer and factor.exp < 0:
            bottom.append(factor.base if factor.exp == -1 else sp.Pow(factor.base, -factor.exp, evaluate=False))
        elif isinstance(factor, sp.Rational) and not factor.is_Integer:
            if factor.p != 1:
                top.append(sp.Integer(factor.p))
            bottom.append(sp.Integer(factor.q))
        else:
            top.append(factor)
    if not bottom:
        return None
    return mul(*top), mul(*bottom)
