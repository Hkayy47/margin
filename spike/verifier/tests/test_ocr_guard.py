"""OCR noise: a correct step that was misread must come back valid or uncertain, never invalid."""

import random

import pytest

from conftest import only, verdicts
from margin_verifier.synth.noise import ANTICIPATED, add_noise

CORRECT = [
    ("solve for x", ["2x + 15 = 21", "2x = 6", "x = 3"]),
    ("solve for x", ["x^{2} - 5x + 6 = 0", "(x - 2)(x - 3) = 0", r"x = 2 \text{ or } x = 3"]),
    ("simplify", [r"\frac{x^{2} - 9}{x + 3}", "x - 3"]),
    ("simplify", [r"\sqrt{5^{2} + 12^{2}}", r"\sqrt{25 + 144}", r"\sqrt{169}", "13"]),
    ("simplify", [r"x^{4} \cdot x^{6}", "x^{4 + 6}", "x^{10}"]),
    ("expand", ["(x + 10)^{2}", "x^{2} + 20x + 100"]),
    ("differentiate", ["f(x) = 5x^{3} - 10x", "f'(x) = 15x^{2} - 10"]),
]


@pytest.mark.parametrize("kind", ANTICIPATED)
@pytest.mark.parametrize("task, lines", CORRECT)
def test_anticipated_noise_never_causes_a_false_alarm(kind, task, lines):
    rng = random.Random(kind)
    for index in range(len(lines)):
        for _ in range(3):
            noisy = add_noise(lines[index], kind, rng)
            if noisy is None:
                continue
            trial = lines[:index] + [noisy] + lines[index + 1 :]
            assert "invalid" not in verdicts(trial, task), (kind, trial)


def test_confusable_letter_blocks_the_alarm():
    result = only([r"\sqrt{S^{2} + 12^{2}}", r"\sqrt{25 + 144}"], "simplify")
    assert result.verdict.value == "uncertain"
    assert "confusable_letter:S" in result.explanation["ocr_flags"]


def test_dropped_exponent_braces_are_recognised_as_a_possible_misread():
    result = only([r"x^{4} \cdot x^{6}", "x^4 + 6"], "simplify")  # was x^{4+6}
    assert result.verdict.value == "uncertain"
    assert result.explanation["misread_that_fixes_step"].startswith("exponent_braces")


def test_strict_mode_also_abstains_on_similar_digit_confusions():
    lines = ["3x = 15", "x = 6"]  # a misread 5, or a real slip? We cannot tell.
    assert verdicts(lines, "solve for x") == ["invalid"]
    assert verdicts(lines, "solve for x", strict_ocr=True) == ["uncertain"]


def test_unreadable_line_is_uncertain_not_invalid():
    result = only(["2x + 3 = 7", r"2x = \frac{4"], "solve for x")
    assert result.verdict.value == "uncertain"
    assert result.explanation["reason"] == "unreadable_line"


def test_next_line_confirmation_separates_misreads_from_mistakes():
    misread = ["2x + 3 = 7", "2x = 9", "x = 2"]  # '4' misread as '9': two alarms, skipping it is fine
    mistake = ["2x + 3 = 7", "2x = 10", "x = 5"]  # real error, then consistent work: one alarm
    assert verdicts(misread, "solve for x") == ["invalid", "invalid"]
    assert verdicts(misread, "solve for x", confirm_with_next_line=True) == ["uncertain", "uncertain"]
    assert verdicts(mistake, "solve for x", confirm_with_next_line=True) == ["invalid", "valid"]
