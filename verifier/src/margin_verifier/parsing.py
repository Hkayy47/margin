"""Turn one OCR line of LaTeX into a small structured statement.

We do the *line structure* ourselves (relations, "or" lists, \\pm, f'(x) heads)
and hand each side to latex2sympy2_extended, which builds an **unevaluated**
SymPy tree: '3(x+2)' stays Mul(3, x+2) instead of becoming 3x+6. Keeping the
surface form is what lets the mal-rules see what the student actually wrote.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import sympy as sp
from latex2sympy2_extended import latex2sympy
from latex2sympy2_extended.latex2sympy2 import ConversionConfig

from margin_verifier.latex_clean import clean_latex

_CONVERSION = ConversionConfig(
    interpret_as_mixed_fractions=False,
    interpret_simple_eq_as_assignment=False,
    interpret_contains_as_eq=False,
    lowercase_symbols=False,  # keep 'S' vs 's' so OCR confusions stay visible
)

# Relation tokens, longest first so '\leq' is not read as '<'.
_RELATIONS = {r"\leq": "<=", r"\geq": ">=", r"\neq": "!=", "<": "<", ">": ">", "=": "="}
_RELATION_RE = re.compile(r"\\leq|\\geq|\\neq|<|>|=")
# f(x) =, f'(x) =, f''(x) =  (single-letter function of a single-letter variable)
_FUNCTION_HEAD = re.compile(r"^([fghy])\s*('*)\s*\(\s*([a-zA-Z])\s*\)\s*=")
_Y_HEAD = re.compile(r"^y\s*('*)\s*=")
_DY_DX_HEAD = re.compile(r"^\\frac\s*\{\s*d\s*([a-zA-Z])\s*\}\s*\{\s*d\s*([a-zA-Z])\s*\}\s*=")
_SUBSCRIPTED = re.compile(r"^([a-zA-Z])_\{?\d+\}?$")


class ParseError(ValueError):
    """The line could not be turned into maths we understand."""


@dataclass(frozen=True)
class Relation:
    """Sides joined by relation operators: 'a = b' or '2x + 1 < 5' or just 'a'."""

    sides: tuple[sp.Expr, ...]  # unevaluated SymPy trees, as written
    ops: tuple[str, ...]  # one op between each pair of sides: '=', '<', '<=', ...


@dataclass(frozen=True)
class Head:
    """A leading function marker such as 'f(x) =', "f'(x) =", 'dy/dx ='."""

    name: str  # 'f', 'y', ...
    order: int  # 0 for f(x) / y, 1 for f'(x) / y' / dy/dx, 2 for f''(x)
    variable: str | None  # 'x' when written, e.g. f'(x); None for plain y


@dataclass(frozen=True)
class ParsedLine:
    raw: str
    clean: str
    flags: tuple[str, ...]  # OCR red flags (see latex_clean)
    branches: tuple[Relation, ...]  # alternatives joined by 'or', ',' or \pm
    continuation: bool  # the line starts with '=' and continues the previous one
    head: Head | None

    @property
    def is_list(self) -> bool:
        return len(self.branches) > 1


def parse_line(raw: str, allow_heads: bool = True) -> ParsedLine:
    """Parse one OCR line. Raises ParseError when we cannot read it.

    `allow_heads` turns on 'f(x) =' / "f'(x) =" markers (derivative problems only)."""
    cleaned = clean_latex(raw)
    text = cleaned.text
    if not text:
        raise ParseError("empty line")
    if "\\text" in text or "\\mathrm" in text:
        raise ParseError("line contains words we do not interpret")
    if re.search(r"(?<![\\a-zA-Z])[a-zA-Z]{3,}", text):
        # 'Let x be the number' would otherwise parse as L*e*t*x*b*e*...
        raise ParseError("line looks like words, not maths")

    continuation = text.startswith("=")
    if continuation:
        text = text[1:].strip()
    head, text = _split_head(text) if allow_heads else (None, text)

    parts, joiner = _split_list(text)
    branches: list[Relation] = []
    for part in parts:
        for variant in _expand_plus_minus(part):
            branches.append(_parse_relation(variant))
    if len(branches) > 1:
        if joiner == "and" and not all(r.ops == ("=",) for r in branches):
            raise ParseError("'and' between inequalities (intersection) is not supported")
        branches = [_unsubscript(r) for r in branches]
    return ParsedLine(
        raw=raw,
        clean=cleaned.text,
        flags=cleaned.flags,
        branches=tuple(branches),
        continuation=continuation,
        head=head,
    )


def parse_expression(latex: str) -> sp.Expr:
    """Parse a single side (no relation symbols) into an unevaluated SymPy tree."""
    if not latex.strip():
        raise ParseError("empty expression")
    try:
        result = latex2sympy(latex, normalization_config=None, conversion_config=_CONVERSION)
    except Exception as error:  # the ANTLR-based parser raises bare Exception
        raise ParseError(f"cannot parse {latex!r}") from error
    if not isinstance(result, sp.Expr):
        raise ParseError(f"{latex!r} is not an expression")
    return result


def _split_head(text: str) -> tuple[Head | None, str]:
    match = _FUNCTION_HEAD.match(text)
    if match:
        name, primes, variable = match.groups()
        return Head(name, len(primes), variable), text[match.end() :].strip()
    match = _Y_HEAD.match(text)
    if match:
        return Head("y", len(match.group(1)), None), text[match.end() :].strip()
    match = _DY_DX_HEAD.match(text)
    if match:
        name, variable = match.groups()
        return Head(name, 1, variable), text[match.end() :].strip()
    return None, text


def _split_list(text: str) -> tuple[list[str], str]:
    """Split 'x=2 \\lor x=-2' or 'x=2, x=-2' at top level."""
    joiner = "and" if "\\land" in text else "or"
    parts = _split_top_level(text, re.compile(r"\\lor(?![a-zA-Z])|\\land(?![a-zA-Z])|,|;"))
    parts = [p.strip() for p in parts]
    if any(not p for p in parts):
        raise ParseError("empty item in a list")
    return parts, joiner


def _expand_plus_minus(text: str) -> list[str]:
    """'x = -1 \\pm 4' -> ['x = -1 + 4', 'x = -1 - 4'] (all \\pm share one sign)."""
    if "\\pm" not in text and "\\mp" not in text:
        return [text]
    plus = re.sub(r"\\mp(?![a-zA-Z])", "-", re.sub(r"\\pm(?![a-zA-Z])", "+", text))
    minus = re.sub(r"\\mp(?![a-zA-Z])", "+", re.sub(r"\\pm(?![a-zA-Z])", "-", text))
    return [plus, minus]


def _parse_relation(text: str) -> Relation:
    pieces = _split_top_level(text, _RELATION_RE, keep_separators=True)
    sides = [parse_expression(piece) for piece in pieces[0::2]]
    ops = [_RELATIONS[op] for op in pieces[1::2]]
    return Relation(sides=tuple(sides), ops=tuple(ops))


def _unsubscript(relation: Relation) -> Relation:
    """In solution lists, 'x_1 = 2, x_2 = -2' means 'x = 2 or x = -2'."""
    renames = {}
    for side in relation.sides:
        for symbol in side.free_symbols:
            match = _SUBSCRIPTED.match(symbol.name)
            if match:
                renames[symbol] = sp.Symbol(match.group(1))
    if not renames:
        return relation
    with sp.evaluate(False):
        sides = tuple(side.xreplace(renames) for side in relation.sides)
    return Relation(sides=sides, ops=relation.ops)


def _split_top_level(text: str, separator: re.Pattern[str], keep_separators: bool = False) -> list[str]:
    """Split on `separator` only outside (), {}, [] groups."""
    pieces: list[str] = []
    depth = 0
    start = 0
    i = 0
    while i < len(text):
        char = text[i]
        if text.startswith(("\\{", "\\}"), i):
            depth += 1 if text[i + 1] == "{" else -1
            i += 2
            continue
        if char in "({[":
            depth += 1
        elif char in ")}]":
            depth -= 1
        elif depth == 0:
            match = separator.match(text, i)
            if match and match.end() > i:
                pieces.append(text[start:i])
                if keep_separators:
                    pieces.append(match.group(0))
                start = i = match.end()
                continue
        i += 1
    pieces.append(text[start:])
    return pieces
