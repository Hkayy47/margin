"""One line of a generated solution: the maths (a SymPy tree) plus how it is written."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from margin_verifier.synth.render import latex, relation
from margin_verifier.tree import add

X = sp.Symbol("x")

Branch = tuple[sp.Expr, str, sp.Expr]


@dataclass(frozen=True)
class Line:
    kind: str  # "expr" | "relation" | "function" | "operator" | "derivative"
    expr: sp.Expr | None = None  # expr / function body / derivative value
    branches: tuple[Branch, ...] = ()  # relation lines: 'or'-joined (lhs, op, rhs)
    pm: tuple[sp.Expr, sp.Expr] | None = None  # write 2 branches as 'lhs = center \pm offset'
    continuation: bool = False  # derivative written as '= ...' (after a d/dx line)

    def render(self) -> str:
        if self.kind == "expr":
            return latex(self.expr)
        if self.kind == "function":
            return f"f(x) = {latex(self.expr)}"
        if self.kind == "operator":
            return r"\frac{d}{dx}\left(" + latex(self.expr) + r"\right)"
        if self.kind == "derivative":
            return ("= " if self.continuation else "f'(x) = ") + latex(self.expr)
        if self.pm is not None:
            center, offset = self.pm
            left = latex(self.branches[0][0])
            middle = "" if center == 0 else latex(center) + " "
            return f"{left} = {middle}\\pm {latex(offset)}"
        return r" \text{ or } ".join(relation(*branch) for branch in self.branches)


def relation_line(lhs: sp.Expr, rhs: sp.Expr, op: str = "=") -> Line:
    return Line("relation", branches=((lhs, op, rhs),))


def single_branch(line: Line) -> Branch | None:
    if line.kind == "relation" and len(line.branches) == 1:
        return line.branches[0]
    return None


def ev(expr: sp.Expr) -> sp.Expr:
    """Evaluate a displayed (unevaluated) tree."""
    return expr.doit()


def ordered(expr: sp.Expr) -> sp.Expr:
    """An evaluated expression rebuilt so sums print in textbook order (x^2 - 5x + 6)."""
    if isinstance(expr, sp.Add):
        return add(*[ordered(term) for term in expr.as_ordered_terms()])
    if isinstance(expr, sp.Mul):
        numbers = [f for f in expr.args if f.is_Number]
        others = [ordered(f) for f in expr.args if not f.is_Number]
        return sp.Mul(*(numbers + others), evaluate=False) if len(numbers + others) > 1 else (numbers + others)[0]
    if isinstance(expr, sp.Pow):
        return sp.Pow(ordered(expr.base), expr.exp, evaluate=False)
    if isinstance(expr, sp.Function):
        return expr.func(*[ordered(a) for a in expr.args], evaluate=False)
    return expr


def terms(expr: sp.Expr) -> tuple[sp.Expr, ...]:
    return expr.args if isinstance(expr, sp.Add) else (expr,)
