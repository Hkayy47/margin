"""Could a step that looks wrong just be the OCR misreading a correct line?

For an invalid-looking step we re-check it with a few alternative readings of
each line. If one of them makes the step correct, the verifier abstains.

Always on: misreads of the anticipated kind that still produce normal-looking
    LaTeX, e.g. dropped braces turning x^{4+6} into x^4+6.
Strict (opt-in): single-character confusions that are *also* classic student
    mistakes: similar digits (5/6, 1/7, 3/8, 4/9, 0/6, 2/7), a dropped minus sign,
    a dropped exponent. This buys safety when OCR confidence is not available,
    at the price of missing real sign errors and slips.
"""

from __future__ import annotations

import re

_SIMILAR_DIGITS = {"1": "7", "7": "1", "3": "8", "8": "3", "5": "6", "6": "5", "4": "9", "9": "4", "0": "6", "2": "7"}
# 'x^4 + 6' / 'x^3 \cdot 2': was the exponent '{4 + 6}' / '{3 \cdot 2}' before the braces got lost?
_EXPONENT_SUM = re.compile(r"\^\s*([0-9a-zA-Z])\s*([+-]|\\cdot)\s*([0-9a-zA-Z]+)")
_MISSING_OPERATOR = re.compile(r"(?<=[0-9a-zA-Z})])\s+(?=[0-9a-zA-Z(\\])")  # 'x 3': was it 'x - 3'?
_SIDE_START = re.compile(r"(^|=|<|>|\\leq|\\geq|\(|\{)\s*(?=[0-9a-zA-Z(\\])")


def alternative_readings(text: str, strict: bool = False) -> list[tuple[str, str]]:
    """(repair name, repaired text) pairs; each changes one spot of `text`."""
    readings = []
    for match in _EXPONENT_SUM.finditer(text):
        braced = "^{" + match.group(1) + " " + match.group(2) + " " + match.group(3) + "}"
        readings.append(("exponent_braces", _splice(text, match, braced)))
    if strict:
        for match in re.finditer(r"\d", text):
            readings.append(("similar_digit", _splice(text, match, _SIMILAR_DIGITS[match.group(0)])))
        for match in _MISSING_OPERATOR.finditer(text):
            readings.append(("dropped_minus", _splice(text, match, " - ")))
        for match in _SIDE_START.finditer(text):
            readings.append(("dropped_minus", _splice(text, match, match.group(1) + "-")))
        for match in re.finditer(r"(?<![\\a-zA-Z])x(?!\s*\^)|\)(?!\s*\^)", text):
            for power in ("^{2}", "^{3}"):
                readings.append(("dropped_exponent", _splice(text, match, match.group(0) + power)))
    return readings


def _splice(text: str, match: re.Match[str], replacement: str) -> str:
    return text[: match.start()] + replacement + text[match.end() :]
