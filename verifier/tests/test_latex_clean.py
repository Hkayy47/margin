from margin_verifier.latex_clean import clean_latex


def test_cosmetic_cleanup_keeps_meaning_and_raises_no_flags():
    result = clean_latex(r"$\left(x+1\right)^{2} \ge \dfrac{1}{2}$")
    assert result.text == r"(x+1)^{2} \geq \frac{1}{2}"
    assert result.flags == ()


def test_unicode_minus_and_times_are_normalised():
    assert clean_latex("−2x × 3").text == r"-2x \cdot 3"


def test_or_between_solutions_becomes_lor():
    assert clean_latex(r"x = 2 \text{ or } x = -2").text == r"x = 2 \lor x = -2"


def test_single_token_arguments_get_braces():
    assert clean_latex(r"\frac12").text == r"\frac{1}{2}"


def test_juxtaposed_numbers_get_explicit_multiplication():
    # latex2sympy2 would read 2(3) as the mixed number 2 3 = 5
    assert clean_latex("2(3)").text == r"2 \cdot (3)"


def test_ocr_red_flags():
    assert "letter_followed_by_digit" in clean_latex("x2 + 1").flags
    assert "digits_separated_by_space" in clean_latex("3 4").flags
    assert "ambiguous_exponent" in clean_latex("x^12").flags
    assert "unbraced_argument" in clean_latex(r"\sqrt x+1").flags
    assert "unbalanced_brackets" in clean_latex("(x + 1").flags
    assert "possible_mixed_number" in clean_latex(r"2\frac{1}{2}").flags
