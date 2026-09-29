"""Print SymPy trees as the kind of LaTeX a handwriting OCR model emits.

SymPy's own printer reorders terms and adds \\left/\\right everywhere; we want
lines that look like a student's ('3x - 2x = -5 - 6', '\\frac{x-3}{x+2}'), with
terms kept in the order the generator built them.
"""

from __future__ import annotations

import sympy as sp

from margin_verifier.tree import split_fraction

_FUNCTIONS = {sp.sin: r"\sin", sp.cos: r"\cos", sp.tan: r"\tan", sp.log: r"\ln"}


def latex(expr: sp.Expr) -> str:
    if _is_negative(expr):
        return "-" + _factor(negate(expr))
    if isinstance(expr, sp.Add):
        return _sum(expr)
    return _product_or_atom(expr)


def negate(expr: sp.Expr) -> sp.Expr:
    """-expr, keeping the written form: -(2x) -> 2x rather than re-simplifying."""
    if isinstance(expr, sp.Number):
        return -expr
    if isinstance(expr, sp.Mul) and isinstance(expr.args[0], sp.Number):
        coefficient, rest = -expr.args[0], expr.args[1:]
        if coefficient == 1:
            return rest[0] if len(rest) == 1 else sp.Mul(*rest, evaluate=False)
        return sp.Mul(coefficient, *rest, evaluate=False)
    return sp.Mul(-1, expr, evaluate=False)


def _is_negative(expr: sp.Expr) -> bool:
    if isinstance(expr, sp.Number):
        return expr < 0
    if isinstance(expr, sp.Mul) and isinstance(expr.args[0], sp.Number):
        return expr.args[0] < 0
    return False


def _sum(expr: sp.Add) -> str:
    out = latex(expr.args[0])
    for term in expr.args[1:]:
        out += " - " + _product_or_atom(negate(term)) if _is_negative(term) else " + " + latex(term)
    return out


def _product_or_atom(expr: sp.Expr) -> str:
    parts = split_fraction(expr)
    if parts is not None and not isinstance(expr, sp.Integer):
        top, bottom = parts
        if _is_negative(top):
            return "-" + _product_or_atom(sp.Mul(negate(top), sp.Pow(bottom, -1, evaluate=False), evaluate=False))
        return r"\frac{" + latex(top) + "}{" + latex(bottom) + "}"
    if isinstance(expr, sp.Mul):
        return _product(expr)
    if isinstance(expr, sp.Pow):
        return _power(expr)
    if isinstance(expr, sp.exp):
        return "e^{" + latex(expr.args[0]) + "}"
    if expr.func in _FUNCTIONS:
        return _FUNCTIONS[expr.func] + "(" + latex(expr.args[0]) + ")"
    if expr is sp.pi:
        return r"\pi"
    if expr is sp.E:
        return "e"
    if isinstance(expr, (sp.Integer, sp.Symbol)):
        return str(expr)
    raise ValueError(f"cannot render {sp.srepr(expr)}")


def _product(expr: sp.Mul) -> str:
    out = ""
    for index, factor in enumerate(expr.args):
        text = _factor(factor)
        if index > 0 and (text[0].isdigit() or text.startswith(("-", r"\frac"))):
            out += r" \cdot "  # '3 \cdot 2', never '32'
        elif index > 0 and out[-1].isalpha() and text[0].isalpha():
            out += " "
        out += text
    return out


def _factor(expr: sp.Expr) -> str:
    """A factor inside a product: sums (and negative numbers) need brackets."""
    if isinstance(expr, sp.Add) or _is_negative(expr):
        return "(" + latex(expr) + ")"
    return _product_or_atom(expr)


def _power(expr: sp.Pow) -> str:
    base, exponent = expr.args
    if exponent == sp.Rational(1, 2):
        return r"\sqrt{" + latex(base) + "}"
    base_text = latex(base)
    needs_brackets = (
        isinstance(base, (sp.Add, sp.Mul, sp.Pow, sp.exp))
        or (isinstance(base, sp.Rational) and not base.is_Integer)
        or _is_negative(base)
        or base.func in _FUNCTIONS
    )
    if needs_brackets:
        base_text = "(" + base_text + ")"
    return base_text + "^{" + latex(exponent) + "}"  # OCR models brace exponents: x^{2}


def relation(lhs: sp.Expr, op: str, rhs: sp.Expr) -> str:
    symbol = {"=": "=", "<": "<", ">": ">", "<=": r"\leq", ">=": r"\geq", "!=": r"\neq"}[op]
    return f"{latex(lhs)} {symbol} {latex(rhs)}"
