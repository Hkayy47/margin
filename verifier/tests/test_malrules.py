"""Every mal-rule: used for diagnosis (hand-written wrong steps) and for injection (generator)."""

import random

import pytest
import sympy as sp

from margin_verifier import check_solution
from margin_verifier.malrules import RULE_IDS, RULES, hint_for, slip_variants
from margin_verifier.synth.generator import inject, solve
from margin_verifier.synth.templates import TEMPLATES
from margin_verifier.tree import add, mul

x = sp.Symbol("x")

DIAGNOSIS_CASES = [
    ("sign_not_flipped_on_move", "solve for x", ["2x + 3 = 7", "2x = 7 + 3"]),
    ("distribute_first_term_only", "solve for x", ["3(x+2) = 2x - 5", "3x + 2 = 2x - 5"]),
    ("distribute_first_term_only", "simplify", ["-(x - 4) + 2x", "-x - 4 + 2x"]),
    ("divide_one_term_only", "solve for x", ["2x + 4 = 10", "x + 4 = 5"]),
    ("divide_one_term_only", "simplify", [r"\frac{2x + 4}{2}", "x + 4"]),
    ("square_of_sum", "expand", ["(x+3)^2", "x^2 + 9"]),
    ("square_of_sum", "expand", ["(x-5)^2", "x^2 - 25"]),
    ("sqrt_of_sum", "simplify", [r"\sqrt{3^2 + 4^2}", "3 + 4"]),
    ("cancel_across_addition", "simplify", [r"\frac{x^2 + 3}{x^2 + 5}", r"\frac{3}{5}"]),
    ("sqrt_missing_pm", "solve for x", ["x^2 = 9", "x = 3"]),
    ("sqrt_missing_pm", "solve for x", ["(x+1)^2 = 16", "x + 1 = 4"]),
    ("add_fractions_add_denominators", "simplify", [r"\frac{1}{x} + \frac{2}{x+1}", r"\frac{3}{2x+1}"]),
    ("add_fractions_add_denominators", "solve for x", [r"\frac{x}{2} + \frac{x}{3} = 5", r"\frac{2x}{5} = 5"]),
    ("exponent_product_multiply", "simplify", [r"x^2 \cdot x^3", "x^6"]),
    ("exponent_product_multiply", "simplify", [r"\frac{x^6}{x^2}", "x^3"]),
    ("power_rule_no_decrement", "differentiate", ["f(x) = x^3", "f'(x) = 3x^3"]),
    ("chain_rule_omitted", "differentiate", ["f(x) = (2x+1)^3", "f'(x) = 3(2x+1)^2"]),
    ("chain_rule_omitted", "differentiate", [r"f(x) = \sin(x^2)", r"f'(x) = \cos(x^2)"]),
    ("product_rule_as_product", "differentiate", [r"f(x) = x^2 \sin x", r"f'(x) = 2x \cos x"]),
    ("divide_by_variable", "solve for x", ["x^2 = 4x", "x = 4"]),
    ("inequality_not_flipped", "solve the inequality", ["-2x > 4", "x > -2"]),
    ("arithmetic_slip", "solve for x", ["3x = 12 + 6", "3x = 19"]),
    ("arithmetic_slip", "simplify", ["2x - 8 + 3x + 3", "5x - 4"]),
]


def test_library_has_at_least_twelve_rules_with_hints():
    assert len(RULE_IDS) >= 12
    assert all(rule.hint for rule in RULES)


@pytest.mark.parametrize("rule_id, task, lines", DIAGNOSIS_CASES)
def test_diagnosis(rule_id, task, lines):
    (result,) = check_solution(lines, task)
    assert result.verdict.value == "invalid"
    assert result.error_type == rule_id
    assert result.hint == hint_for(rule_id)


def test_candidates_reproduce_the_textbook_mistake():
    square = {r.id: r for r in RULES}["square_of_sum"]
    outputs = {sp.expand(c.doit()) for c in square.candidates(sp.Pow(x + 3, 2, evaluate=False))}
    assert x**2 + 9 in outputs

    distribute = next(r for r in RULES if r.id == "distribute_first_term_only")
    written = mul(sp.Integer(3), add(x, sp.Integer(2)))
    assert 3 * x + 2 in {c.doit() for c in distribute.candidates(written)}


def test_slip_variants_change_one_number_by_a_little():
    variants = {v.doit() for v in slip_variants(add(mul(sp.Integer(5), x), sp.Integer(-4)))}
    assert 5 * x - 5 in variants and 5 * x - 3 in variants and 6 * x - 4 in variants
    assert 5 * x + 4 in variants  # sign slip


def _injected_step(rule_id: str):
    """A (task, previous line, wrong line) produced by injecting `rule_id` in a template."""
    rng = random.Random(0)
    for template in TEMPLATES:
        if rule_id not in template.rules:
            continue
        for _ in range(40):
            lines = solve([template.start(rng)], template.solver)
            for step in range(1, len(lines)):
                wrong = inject(rule_id, lines[step - 1], lines[step], rng)
                if wrong is not None:
                    return template.task, lines[step - 1].render(), wrong.render()
    raise AssertionError(f"no template could inject {rule_id}")


@pytest.mark.parametrize("rule_id", RULE_IDS)
def test_injection_round_trip(rule_id):
    task, previous, wrong = _injected_step(rule_id)
    (result,) = check_solution([previous, wrong], task)
    assert result.verdict.value == "invalid", (previous, wrong, result.explanation)
    assert rule_id in result.explanation.get("matching_rules", []), (previous, wrong, result.explanation)
