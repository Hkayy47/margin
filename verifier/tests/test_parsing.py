import pytest
import sympy as sp

from margin_verifier.parsing import ParseError, parse_line

x = sp.Symbol("x")


def test_equation_keeps_the_written_form():
    line = parse_line("3(x+2) = 2x - 5")
    (relation,) = line.branches
    assert relation.ops == ("=",)
    assert isinstance(relation.sides[0], sp.Mul)  # not expanded to 3x + 6
    assert relation.sides[0].doit() == 3 * x + 6


@pytest.mark.parametrize(
    "text",
    [r"x = 2 \text{ or } x = -2", "x = 2, x = -2", r"x = \pm 2", "x_1 = 2, x_2 = -2", r"x = 2 \lor x = -2"],
)
def test_solution_lists_become_branches(text):
    line = parse_line(text)
    values = sorted(r.sides[1].doit() for r in line.branches)
    assert values == [-2, 2]
    assert all(r.sides[0] == x for r in line.branches)


def test_plus_minus_with_a_shift():
    line = parse_line(r"x = -1 \pm 4")
    assert sorted(r.sides[1].doit() for r in line.branches) == [-5, 3]


def test_inequality_operators():
    assert parse_line(r"-2x + 3 \geq 7").branches[0].ops == (">=",)
    assert parse_line(r"x \le -2").branches[0].ops == ("<=",)


def test_continuation_line():
    line = parse_line("= 3x^2 + 2")
    assert line.continuation
    assert line.branches[0].sides[0].doit() == 3 * x**2 + 2


@pytest.mark.parametrize(
    "text, name, order",
    [("f(x) = x^2", "f", 0), ("f'(x) = 2x", "f", 1), ("f''(x) = 2", "f", 2), ("y' = 2x", "y", 1),
     (r"\frac{dy}{dx} = 2x", "y", 1)],
)
def test_derivative_heads(text, name, order):
    line = parse_line(text, allow_heads=True)
    assert (line.head.name, line.head.order) == (name, order)


def test_heads_are_off_outside_derivative_problems():
    assert parse_line("f(x) = 2", allow_heads=False).head is None


def test_d_dx_operator_is_an_unevaluated_derivative():
    side = parse_line(r"\frac{d}{dx}(x^3 + 2x)").branches[0].sides[0]
    assert isinstance(side, sp.Derivative)
    assert side.doit() == 3 * x**2 + 2


@pytest.mark.parametrize("text", [r"\text{check: } x = 3", "", r"x = \frac{"])
def test_unreadable_lines_raise(text):
    with pytest.raises(ParseError):
        parse_line(text)


def test_plain_words_are_not_read_as_a_product_of_letters():
    with pytest.raises(ParseError):
        parse_line("Let x be the number")
    assert parse_line(r"\sin x + \cos x").branches  # commands are fine
