"""Meaning-preserving cleanup of OCR-produced LaTeX, plus OCR red flags.

Every line goes through `clean_latex` before parsing. Cleanup only makes changes
that cannot alter the maths (unicode minus -> '-', '\\left(' -> '(', ...).
Anything that *might* be a recognition error is never silently "fixed"; it is
reported as a flag so the verifier can abstain instead of raising a false alarm.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CleanLatex:
    text: str  # cleaned LaTeX, ready for the parser
    flags: tuple[str, ...]  # OCR red flags found while cleaning (empty = looks clean)


_UNICODE = {
    "\u2212": "-",  # minus sign
    "\u2013": "-",  # en dash
    "\u2014": "-",  # em dash
    "\u2010": "-",  # hyphen
    "\uff0d": "-",  # full-width hyphen-minus
    "\u00d7": r" \cdot ",
    "\u00b7": r" \cdot ",
    "\u22c5": r" \cdot ",
    "\u00f7": r" \div ",
    "\u2264": r" \leq ",
    "\u2265": r" \geq ",
    "\u2260": r" \neq ",
    "\u00b1": r" \pm ",
    "\u2213": r" \mp ",
    "\u03c0": r" \pi ",
    "\u221a": r"\sqrt",
    "\u00b2": "^{2}",
    "\u00b3": "^{3}",
}

# (pattern, replacement) pairs applied in order. All are meaning-preserving.
_REWRITES: list[tuple[str, str]] = [
    (r"\$", " "),  # $...$ delimiters
    (r"\\[\[\]()]", " "),  # \( \) \[ \] delimiters
    (r"\\(?:displaystyle|textstyle)", " "),
    (r"\\(?:left|right|bigl|bigr|Bigl|Bigr|big|Big)\s*\.", " "),  # invisible \left.
    (r"\\(?:left|right|bigl|bigr|Bigl|Bigr|big|Big)(?![a-zA-Z])", ""),  # keep delimiter
    (r"\\[dt]frac(?![a-zA-Z])", r"\\frac"),
    (r"\\[,;:! ]|\\q?quad(?![a-zA-Z])|~", " "),  # spacing commands
    (r"\\(?:times|ast)(?![a-zA-Z])|\*", r" \\cdot "),
    (r"\\(?:geqslant|geq|ge)(?![a-zA-Z])", r" \\geq "),
    (r"\\(?:leqslant|leq|le)(?![a-zA-Z])", r" \\leq "),
    (r"\\(?:neq|ne)(?![a-zA-Z])", r" \\neq "),
    (r"\\gt(?![a-zA-Z])", " > "),
    (r"\\lt(?![a-zA-Z])", " < "),
    (r"\\mathrm\s*\{\s*d\s*\}", "d"),
    (r"\\(?:text|textrm|mathrm|mbox)\s*\{\s*or\s*\}|\\vee(?![a-zA-Z])", r" \\lor "),
    (r"\\(?:text|textrm|mathrm|mbox)\s*\{\s*and\s*\}|\\wedge(?![a-zA-Z])", r" \\land "),
    # Leading "therefore"-style arrows carry no maths for a single line.
    (r"^\s*(?:\\Rightarrow|\\implies|\\therefore|\\Longrightarrow|\\rightarrow|\\to"
     r"|\\iff|\\Leftrightarrow|=>)(?![a-zA-Z])", " "),
]

_TOKEN = re.compile(r"\\[a-zA-Z]+|\\.|\s+|.", re.DOTALL)


def clean_latex(raw: str) -> CleanLatex:
    """Normalise one OCR line and collect OCR red flags."""
    flags: list[str] = []
    text = raw
    for char, replacement in _UNICODE.items():
        text = text.replace(char, replacement)
    for pattern, replacement in _REWRITES:
        text = re.sub(pattern, replacement, text)
    text = re.sub(r"[\s.,;]+$", "", text).strip()

    # "3 4" is 34 in LaTeX, but OCR often produces it from "3 \cdot 4": ambiguous.
    if re.search(r"\d\s+\d", text):
        flags.append("digits_separated_by_space")
        text = re.sub(r"(?<=\d)\s+(?=\d)", "", text)
    # "x2" is almost always a misread "x^2" (students write 2x, not x2).
    if re.search(r"(?<![\\a-zA-Z])[a-zA-Z]\d", text):
        flags.append("letter_followed_by_digit")
    # "2\frac{1}{2}": mixed number or product? Ambiguous in handwriting.
    if re.search(r"\d\s*\\frac\s*\{\s*\d+\s*\}\s*\{\s*\d+\s*\}", text):
        flags.append("possible_mixed_number")

    text, brace_flags = _brace_arguments(text)
    flags.extend(brace_flags)
    if not _brackets_balanced(text):
        flags.append("unbalanced_brackets")

    # latex2sympy2 reads "2(3)" and "2\frac{1}{2}" as mixed numbers (5 and 5/2).
    # In algebra, juxtaposition means multiplication, so make it explicit.
    text = re.sub(r"(?<=[\d)])\s*(?=\(|\\frac(?![a-zA-Z]))", r" \\cdot ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return CleanLatex(text=text, flags=tuple(dict.fromkeys(flags)))


def _brace_arguments(text: str) -> tuple[str, list[str]]:
    """Wrap single-token arguments in braces: '\\frac12' -> '\\frac{1}{2}'.

    This follows TeX semantics (an unbraced argument is one token). OCR output
    that relies on it is unusual, so unbraced \\frac/\\sqrt arguments and
    exponents followed by more letters/digits ('x^2x', 'x^12') are flagged.
    """
    tokens = _TOKEN.findall(text)
    out: list[str] = []
    flags: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        out.append(token)
        i += 1
        if token not in ("\\frac", "\\sqrt", "^", "_"):
            continue
        if token == "\\sqrt":
            i = _copy_optional_index(tokens, i, out)
        for _ in range(2 if token == "\\frac" else 1):
            i = _skip_spaces(tokens, i)
            if i >= len(tokens):
                flags.append("missing_argument")
                break
            if tokens[i] == "{":
                end = _matching(tokens, i, "{", "}")
                if end is None:
                    flags.append("unbalanced_brackets")
                    return text, flags
                out.extend(tokens[i : end + 1])
                i = end + 1
                continue
            argument = tokens[i]
            follows = tokens[i + 1] if i + 1 < len(tokens) else ""
            if token in ("^", "_") and follows[:1].isalnum():
                flags.append("ambiguous_exponent")  # 'x^12': x^{12} or x^{1}2 ?
                break
            if argument in ("\\frac", "\\sqrt"):
                flags.append("unbraced_argument")  # e.g. '\sqrt\frac{1}{2}': leave as is
                break
            if token in ("\\frac", "\\sqrt"):
                flags.append("unbraced_argument")
            out.append("{" + argument + "}")
            i += 1
    return "".join(out), flags


def _copy_optional_index(tokens: list[str], i: int, out: list[str]) -> int:
    """Copy an optional '[n]' after \\sqrt; return the next index."""
    j = _skip_spaces(tokens, i)
    if j < len(tokens) and tokens[j] == "[":
        end = _matching(tokens, j, "[", "]")
        if end is not None:
            out.extend(tokens[j : end + 1])
            return end + 1
    return i


def _skip_spaces(tokens: list[str], i: int) -> int:
    while i < len(tokens) and tokens[i].isspace():
        i += 1
    return i


def _matching(tokens: list[str], start: int, open_: str, close: str) -> int | None:
    depth = 0
    for j in range(start, len(tokens)):
        if tokens[j] == open_:
            depth += 1
        elif tokens[j] == close:
            depth -= 1
            if depth == 0:
                return j
    return None


def _brackets_balanced(text: str) -> bool:
    stack: list[str] = []
    pairs = {")": "(", "}": "{", "]": "["}
    for token in _TOKEN.findall(text):
        if token in "({[":
            stack.append(token)
        elif token in pairs:
            if not stack or stack.pop() != pairs[token]:
                return False
    return not stack
