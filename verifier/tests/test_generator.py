import random

import pytest

from conftest import verdicts
from margin_verifier.synth.generator import generate
from margin_verifier.synth.noise import add_noise
from margin_verifier.synth.templates import TEMPLATES


def test_generation_is_deterministic():
    assert generate(11).lines == generate(11).lines


@pytest.mark.parametrize("index", range(0, 2 * len(TEMPLATES), 2))  # one correct solution per template
def test_correct_solutions_are_not_flagged(index):
    solution = generate(index)
    assert solution.error_step is None
    assert "invalid" not in verdicts(solution.lines, solution.task)


@pytest.mark.parametrize("index", range(1, 2 * len(TEMPLATES), 2))  # one wrong solution per template
def test_injected_error_is_caught_on_its_line(index):
    solution = generate(index)
    results = verdicts(solution.lines, solution.task)
    assert results[solution.error_step - 1] == "invalid", (solution.lines, solution.error_rule)
    assert results.count("invalid") == 1  # later lines continue consistently: no repeat alarms


def test_noise_examples():
    rng = random.Random(0)
    assert add_noise("x^{2} + 1", "x2_for_x_squared", rng) == "x2 + 1"
    assert add_noise("2x - 1", "unicode_minus", rng) == "2x − 1"
    assert add_noise("x = 5", "S_for_5", rng) == "x = S"
    assert add_noise("x = 5", "l_for_1", rng) is None
