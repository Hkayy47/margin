"""Bake-off: SymPy's Lark LaTeX parser vs latex2sympy2_extended on OCR-style inputs.

    uv run --group compare python scripts/compare_parsers.py

For each input we check that the parse means what a maths teacher would read,
with and without our own cleanup (margin_verifier.latex_clean). We also check
whether the parser keeps the written form (3(x+2) not expanded to 3x+6), which
the mal-rule diagnosis depends on. Writes results/parser_comparison.md.
"""

from __future__ import annotations

import time
import warnings
from pathlib import Path

import sympy as sp
from latex2sympy2_extended import latex2sympy
from latex2sympy2_extended.latex2sympy2 import ConversionConfig
from sympy.parsing.latex import parse_latex

from margin_verifier.latex_clean import clean_latex

x, r = sp.symbols("x r")
CASES: list[tuple[str, object]] = [
    ("2x + 3", 2 * x + 3),
    ("3(x+2)", 3 * (x + 2)),
    ("x(x-4)", x * (x - 4)),
    ("(x-2)(x-3)", (x - 2) * (x - 3)),
    (r"\frac{x^2-9}{x^2+5x+6}", (x**2 - 9) / (x**2 + 5 * x + 6)),
    (r"\frac{1}{x} + \frac{2}{x+1}", 1 / x + 2 / (x + 1)),
    (r"x^2 \cdot x^3", x**5),
    (r"\sqrt{x+3}", sp.sqrt(x + 3)),
    (r"\sqrt[3]{x}", x ** sp.Rational(1, 3)),
    (r"\left(x+1\right)^2", (x + 1) ** 2),
    (r"2\left(x - 4\right) + 3(x + 1)", 5 * x - 5),
    ("x^{12}", x**12),
    ("-2x + 3", -2 * x + 3),
    (r"\sin x", sp.sin(x)),
    (r"\sin(3x^2)", sp.sin(3 * x**2)),
    (r"\cos(3x^2) \cdot 6x", 6 * x * sp.cos(3 * x**2)),
    (r"3x^2 \sin x + x^3 \cos x", 3 * x**2 * sp.sin(x) + x**3 * sp.cos(x)),
    ("e^{2x}", sp.exp(2 * x)),
    (r"\ln x", sp.log(x)),
    (r"\ln(x^2 + 1)", sp.log(x**2 + 1)),
    ("|x - 1|", sp.Abs(x - 1)),
    (r"\frac{d}{dx}(x^3 + 2x)", 3 * x**2 + 2),
    ("2(3)", 6),
    (r"2 \cdot 3 + 4", 10),
    (r"\dfrac{1}{x}", 1 / x),
    ("x^2 - 5x + 6", x**2 - 5 * x + 6),
    (r"\frac{x}{2} + \frac{x}{3}", 5 * x / 6),
    ("-(x - 4)", 4 - x),
    ("x^{-1}", 1 / x),
    ("2^{3}x", 8 * x),
    (r"\pi r^2", sp.pi * r**2),
    (r"x \times 3", 3 * x),
    (r"6 \div 2", 3),
    (r"\frac{2x+4}{2}", x + 2),
    (r"\frac12", sp.Rational(1, 2)),
    ("2x + 3 = 7", sp.Eq(2 * x + 3, 7)),
    ("-2x + 3 > 7", sp.Gt(-2 * x + 3, 7)),
    (r"x \leq -2", sp.Le(x, -2)),
    (r"x \ge 2", sp.Ge(x, 2)),
    (r"\sqrt{x+3} = x - 3", sp.Eq(sp.sqrt(x + 3), x - 3)),
    ("(x-2)(x-3) = 0", sp.Eq((x - 2) * (x - 3), 0)),
    ("−2x + 1", -2 * x + 1),  # unicode minus from OCR
]
# (input, check) pairs: does the parser keep what the student wrote?
SURFACE_CASES = [
    ("3(x+2)", lambda e: isinstance(e, sp.Mul) and any(isinstance(a, sp.Add) for a in e.args)),
    (r"x^2 \cdot x^3", lambda e: isinstance(e, sp.Mul)),
    (r"\frac{x}{2} + \frac{x}{3}", lambda e: isinstance(e, sp.Add) and len(e.args) == 2),
    ("3x - 2x", lambda e: isinstance(e, sp.Add)),
]

L2S_CONFIG = ConversionConfig(interpret_as_mixed_fractions=False, interpret_simple_eq_as_assignment=False,
                              interpret_contains_as_eq=False, lowercase_symbols=False)


def lark(text: str):
    return parse_latex(text, backend="lark")


def l2s(text: str):
    return latex2sympy(text, normalization_config=None, conversion_config=L2S_CONFIG)


PARSERS = {"sympy-lark": lark, "latex2sympy2_extended": l2s}


def means_the_same(parsed, expected) -> bool:
    if isinstance(expected, sp.core.relational.Relational):
        if type(parsed) is not type(expected):
            return False
        return all(sp.simplify(a.doit() - b) == 0 for a, b in zip(parsed.args, expected.args))
    if not isinstance(parsed, sp.Expr):
        return False  # e.g. Lark's ambiguous Tree results
    return sp.simplify(parsed.doit() - sp.sympify(expected)) == 0


def run(parser, text: str, expected) -> tuple[bool, float]:
    """(parsed correctly?, seconds). Any exception counts as a failed parse."""
    start = time.perf_counter()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            parsed = parser(text)
        ok = means_the_same(parsed, expected)
    except Exception:
        ok = False
    return ok, time.perf_counter() - start


def main() -> None:
    rows = []
    failures: dict[str, list[str]] = {}
    for name, parser in PARSERS.items():
        parser(CASES[0][0])  # warm-up (grammar loading)
        for cleaned in (False, True):
            correct, seconds = 0, []
            for text, expected in CASES:
                source = clean_latex(text).text if cleaned else text
                ok, elapsed = run(parser, source, expected)
                correct += ok
                seconds.append(elapsed)
                if not ok:
                    label = f"{name} ({'after' if cleaned else 'without'} our cleanup)"
                    failures.setdefault(label, []).append(text)
            surface = sum(_keeps_surface(parser, text, check) for text, check in SURFACE_CASES)
            rows.append((name, "yes" if cleaned else "no", f"{correct}/{len(CASES)}",
                         f"{surface}/{len(SURFACE_CASES)}", f"{1000 * sum(seconds) / len(seconds):.1f}"))
    lines = [
        "| parser | our cleanup first | correct parses | keeps written form | ms / parse |",
        "|---|---|---|---|---|",
        *[f"| {' | '.join(row)} |" for row in rows],
        "",
        *[f"- {label} gets wrong: " + ", ".join(f"`{t}`" for t in texts) for label, texts in failures.items()],
    ]
    report = "\n".join(lines)
    out = Path(__file__).resolve().parent.parent / "results" / "parser_comparison.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("# Parser bake-off\n\n" + report + "\n", encoding="utf-8")
    print(report)


def _keeps_surface(parser, text: str, check) -> bool:
    try:
        return bool(check(parser(clean_latex(text).text)))
    except Exception:
        return False


if __name__ == "__main__":
    main()
