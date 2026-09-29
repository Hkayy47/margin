"""Plausible OCR recognition errors applied to clean LaTeX lines.

ANTICIPATED noise is the list the verifier was designed against (its OCR guard
knows these patterns). HELD_OUT noise is deliberately *not* handled, to measure
what happens when OCR makes a mistake that turns one valid formula into another.
"""

from __future__ import annotations

import random
import re

ANTICIPATED = (
    "missing_braces",
    "x2_for_x_squared",
    "unicode_minus",
    "cdot_toggle",
    "l_for_1",
    "O_for_0",
    "S_for_5",
    "stray_spaces",
)
HELD_OUT = ("digit_swap", "dropped_minus", "dropped_exponent")

_SIMILAR_DIGITS = {"1": "7", "7": "1", "3": "8", "8": "3", "5": "6", "6": "5", "4": "9", "9": "4", "0": "6", "2": "7"}
_TOKEN = re.compile(r"\\[a-zA-Z]+|\\.|\s+|.", re.DOTALL)


def add_noise(line: str, kind: str, rng: random.Random) -> str | None:
    """`line` with one error of type `kind`, or None if that error cannot occur here."""
    if kind == "missing_braces":
        return _drop_argument_braces(line, rng)
    if kind == "x2_for_x_squared":
        return _replace_one(line, r"([a-zA-Z])\^\{?2\}?(?![0-9])", lambda m: m.group(1) + "2", rng)
    if kind == "unicode_minus":
        return line.replace("-", "−") if "-" in line else None
    if kind == "cdot_toggle":
        if "\\cdot" in line:
            return _replace_one(line, r"\s*\\cdot\s*", lambda m: " ", rng)
        return _replace_one(line, r"(\d)(?=[a-zA-Z(])", lambda m: m.group(1) + r" \cdot ", rng)
    if kind == "l_for_1":
        return _replace_one(line, r"(?<![\\a-zA-Z])1", lambda m: "l", rng)
    if kind == "O_for_0":
        return _replace_one(line, r"(?<![\\a-zA-Z])0", lambda m: "O", rng)
    if kind == "S_for_5":
        return _replace_one(line, r"(?<![\\a-zA-Z])5", lambda m: "S", rng)
    if kind == "stray_spaces":
        return _stray_spaces(line, rng)
    if kind == "digit_swap":
        return _replace_one(line, r"\d", lambda m: _SIMILAR_DIGITS[m.group(0)], rng)
    if kind == "dropped_minus":
        return _replace_one(line, r"-", lambda m: "", rng)
    if kind == "dropped_exponent":
        return _replace_one(line, r"\^(\{[^{}]*\}|[0-9a-zA-Z])", lambda m: "", rng)
    raise ValueError(f"unknown noise kind {kind!r}")


def noisy_solution(lines: list[str], kinds: tuple[str, ...], rate: float, rng: random.Random):
    """Each line gets one random applicable error with probability `rate`.

    Returns (noisy lines, noise kind per line or None)."""
    noisy, applied = [], []
    for line in lines:
        kind = None
        if rng.random() < rate:
            options = list(kinds)
            rng.shuffle(options)
            for option in options:
                changed = add_noise(line, option, rng)
                if changed is not None and changed != line:
                    line, kind = changed, option
                    break
        noisy.append(line)
        applied.append(kind)
    return noisy, applied


def _replace_one(line: str, pattern: str, replacement, rng: random.Random) -> str | None:
    matches = list(re.finditer(pattern, line))
    if not matches:
        return None
    match = rng.choice(matches)
    return line[: match.start()] + replacement(match) + line[match.end() :]


def _drop_argument_braces(line: str, rng: random.Random) -> str | None:
    """Remove one {...} that holds an argument of ^, _, \\frac or \\sqrt."""
    tokens = _TOKEN.findall(line)
    openings = []
    for i, token in enumerate(tokens):
        if token != "{":
            continue
        before = next((tokens[j] for j in range(i - 1, -1, -1) if not tokens[j].isspace()), "")
        if before in ("^", "_", "\\frac", "\\sqrt", "}"):
            openings.append(i)
    rng.shuffle(openings)
    for start in openings:
        depth = 0
        for end in range(start, len(tokens)):
            depth += {"{": 1, "}": -1}.get(tokens[end], 0)
            if depth == 0:
                kept = tokens[:start] + tokens[start + 1 : end] + tokens[end + 1 :]
                return "".join(kept)
    return None


def _stray_spaces(line: str, rng: random.Random) -> str | None:
    tokens = _TOKEN.findall(line)
    if len(tokens) < 3:
        return None
    for _ in range(rng.randint(1, 3)):
        position = rng.randint(1, len(tokens) - 1)
        tokens.insert(position, " ")
    return "".join(tokens)
