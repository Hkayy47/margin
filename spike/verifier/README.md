# Margin step verifier (spike)

This is a prototype of the part of **Margin** that reads a student's handwritten solution line by line (as LaTeX from OCR) and decides, for each step, whether the new line follows from the previous one. The product rule is to speak up only when a step is wrong, and **never to flag a correct step**. When the verifier is unsure, it says `uncertain` and the app stays silent.

```python
from margin_verifier import check_solution

check_solution(["2x + 3 = 7", "2x = 7 + 3", "2x = 10", "x = 5"], task="Solve for x")
# step 1: invalid, error_type="sign_not_flipped_on_move", hint="When a term moves to the other side, its sign changes."
# step 2: valid   (consistent with the previous line, even though that line was wrong)
# step 3: valid
```

Measured results are in [RESULTS.md](RESULTS.md).

## Running it

Requires [uv](https://docs.astral.sh/uv/). Python 3.11 is pinned in `.python-version`.

```bash
uv sync                                                    # sympy, latex2sympy2_extended, pytest
uv run pytest                                              # 356 tests, ~20 s
uv run python scripts/evaluate.py                          # 1,250 seeded solutions x 15 conditions (~3 min, 12 processes)
uv run python scripts/evaluate.py --solutions 100          # quick run
uv run --group compare python scripts/compare_parsers.py   # the parser bake-off (needs `lark`)
```

`evaluate.py` rewrites the tables between the `GENERATED` markers in `RESULTS.md` and dumps every checked transition to `results/transitions.jsonl`, so failures can be inspected.

## API

```python
check_solution(lines: list[str], task: str | None = None, *,
               strict_ocr: bool = False, confirm_with_next_line: bool = False) -> list[StepVerdict]
```

- `lines`: one LaTeX string per handwritten line, as OCR produced it (`$...$`, `\left(`, unicode minus and so on are fine).
- `task`: optional context such as "Solve for x", "Simplify" or "Differentiate with respect to x". It picks the mode (equation / expression / derivative) and the variable. Without it, the mode is inferred from the notation (`=`, `f'(x)`, `\frac{d}{dx}`).
- It returns one `StepVerdict` per transition `lines[i-1] -> lines[i]`.

| field | meaning |
|---|---|
| `step` | index `i` of the line being judged |
| `verdict` | `valid`, `invalid` or `uncertain` |
| `error_type` | mal-rule id (see below) or `"unclassified"` when invalid, else `None` |
| `confidence` | heuristic evidence strength in [0, 1]. It is **not calibrated**; `uncertain` is always 0 |
| `hint` | a nudge for the student (invalid only). It never contains the answer |
| `explanation` | machine-readable details: `mode`, `reason`, `expected`/`got`, `counterexample`, `term_diff` (missing/unexpected terms), `solutions_before`/`after`, `lost`/`extra`, `matching_rules`, `ocr_flags`, and so on |

`explanation["expected"]` contains the correct value. It is for logs and analytics only; the UI must show `hint`, not `expected`.

The call is deterministic: sampling is seeded, and the only shared state is memoisation caches. It is also stateless: the app can re-send all lines each time a new line is recognised.

### Options

- `confirm_with_next_line=True` (recommended for the app): a misread line causes two alarms in a row, and skipping that line removes both. A real mistake causes one alarm, followed by consistent work. With this option the app waits for the line *after* a suspect line before speaking. That also avoids interrupting a student mid-thought.
- `strict_ocr=True`: also abstain when a one-character OCR confusion (similar digit, dropped minus, dropped exponent) would make the step correct. It is safer without OCR confidence scores, but costs about 20% of recall on clean input (see RESULTS).

## What the phone pipeline would call

```
camera frames -> page/line segmentation -> handwriting-to-LaTeX OCR (+ per-token confidence)
      -> [new or changed line?] -> check_solution(all_lines_so_far, task, confirm_with_next_line=True)
      -> policy: speak only if verdict == invalid AND the OCR is confident about the tokens in
         explanation.term_diff / the changed numbers AND the student has written the next line
         (or confirmed "I read: 2x = 9 - is that right?") -> show `hint`
```

Suggested wire format for a small service (Python can run server-side, or on-device via Chaquopy):

```json
POST /check  {"task": "Solve for x", "lines": ["2x + 3 = 7", "2x = 10"], "line_confidence": [0.98, 0.91]}
-> [{"step": 1, "verdict": "invalid", "error_type": "sign_not_flipped_on_move", "confidence": 0.97,
     "hint": "When a term moves to the other side, its sign changes.", "explanation": {...}}]
```

`line_confidence` is not used yet. It is where OCR confidence should enter the "speak or stay silent" policy (see Recommendations in RESULTS.md).

Latency, measured on a desktop CPU in one process: import 0.6 s, then about 16 ms per step on average and 50 ms at p95 (strict mode is about 3x slower). Radical equations have a 2 s solver budget. A phone running Python is likely 3 to 10x slower, which is still fine for one call per written line. The process should be kept warm.

## Design decisions

**Parser: `latex2sympy2_extended` (maintained fork of latex2sympy2), behind our own cleanup and line-structure layer.** In the bake-off (`scripts/compare_parsers.py`, `results/parser_comparison.md`), on 42 OCR-style inputs it read 42/42 correctly after our cleanup (38/42 raw). SymPy's Lark backend read 36/42 (34/42 raw). Lark fails on `x(x-4)` (ambiguous parse), `\sin x` without brackets, `e^{2x}`, `\pi r^2` and `2^{3}x`, and it mis-parsed `\left(` as `\le` + `ft`. The deciding point is that l2s builds **unevaluated** trees, so `3(x+2)` stays `3·(x+2)` and is not turned into `3x+6`. The mal-rules need that written form. Lark evaluates eagerly (0/4 on the written-form check). The l2s parser is also about 3x faster. The corpus was written by us, so treat these numbers as indicative only. We work around two l2s quirks in `latex_clean.py`:
- l2s reads juxtaposed numbers as mixed numbers (`2(3)` -> 5, `2\frac{1}{2}` -> 5/2), so we insert `\cdot`.
- It lowercases symbols by default (`S` would become `s`), so we switch that off.

SymPy's ANTLR backend needs antlr4 4.11, which conflicts with l2s's 4.13, so it was not tested.

**Written form vs value.** Every side is kept as the unevaluated tree the student wrote. `.doit()` gives its value for checking. Mal-rules rewrite the written tree (`tree.py`) inside `sympy.evaluate(False)`.

**Expression equivalence (`equivalence.py`).** Both sides are evaluated at 12 seeded random real points with 30-digit mpmath. Points where either side is undefined or non-real are skipped.
- "equal" needs 6 or more agreeing points. SymPy `simplify` then confirms it when the expression is small.
- "different" needs 2 or more counterexamples.
- If a counterexample involves `sqrt`, `|x|`, `log` or fractional powers and both sides agree for positive values (e.g. `sqrt(x^2) = x`), the answer is **unknown**, not different.

**Equations (`solutions.py`, `check_relation.py`).** Steps are judged by the real solution set. Polynomial and rational equations are solved by exact root isolation (fast; cubics come back as `CRootOf`, not slow Cardano formulas). Radical equations and inequalities use `solveset`.
- Same set: valid.
- Superset: valid, marked "may add roots". Squaring and clearing denominators are sound steps; the extra roots are listed in `extra_candidates`. The exception is a final `x = a or x = b` list for a polynomial equation, which must not contain non-solutions.
- Subset: valid only if every dropped root fails an earlier, trustworthy line (rejecting an extraneous root). Otherwise invalid (lost solution), or uncertain if an earlier line cannot be trusted.
- `x = \pm 3`, `x = 2 \text{ or } x = -2`, `x=2, x=-2` and `x_1 = 2, x_2 = -2` are all supported.

**Derivatives (`check_derivative.py`).** The notation (`f(x) =`, `f'(x) =`, `y'`, `dy/dx`, `f''`, `\frac{d}{dx}(...)`, `= ...`) sets the derivative order of each line. A step one order up is compared with `d/dx` of the previous line; a step at the same order is compared with the previous line. When bare lines leave the order open, either reading is accepted.

**Mal-rules (`malrules.py`).** 15 rules, each a single function from the previous line to the wrong lines that mistake produces:
- sign_not_flipped_on_move, distribute_first_term_only, divide_one_term_only, square_of_sum, sqrt_of_sum, cancel_across_addition, sqrt_missing_pm, divide_by_variable, add_fractions_add_denominators, exponent_product_multiply
- power_rule_no_decrement, chain_rule_omitted, product_rule_as_product
- inequality_not_flipped, arithmetic_slip

The same function drives **diagnosis**: a candidate equivalent to the student's line names the error. Relation candidates must be the same equation up to a constant factor, not merely share roots. It also drives **injection** in the generator. `arithmetic_slip` is checked in reverse: does changing one number of the student's line by ±1, ±2 or its sign make the step correct? The derivative rules come from a small differentiator with switchable bugs (`calculus.py`). When several rules match, the first in library order wins, and all matches are listed.

**OCR guard: how "never flag a correct step" survives OCR.**
1. `latex_clean.py` only makes meaning-preserving fixes (unicode minus, `\left(`, `\dfrac` and so on). It raises flags for patterns that often come from misreads: `x2`, `x^12`, `3 4`, unbraced `\frac`/`\sqrt` arguments, unbalanced brackets, `2\frac{1}{2}`.
2. The verifier also flags letters that OCR confuses with digits (`l I O o S Z B g q`, unless it is the task variable), letters that suddenly appear, and a parsed imaginary unit.
3. Before an alarm, `misreads.py` re-checks the step under a few alternative readings, for example `x^4 + 6` read as `x^{4+6}`. If any reading makes the step clearly correct, the answer is uncertain.
4. Any flag turns `invalid` into `uncertain`.
5. Unreadable lines, prose, `\text{...}` and any internal exception also become `uncertain`.

**Structure.** The code is small modules with one job each (see the module map below). The synthetic-data code (`margin_verifier/synth/`) is separate from the verifier and never used by it.

## Module map

| file | job |
|---|---|
| `verifier.py` | public `check_solution`; mode and variable detection; OCR guard; misread and next-line checks |
| `latex_clean.py` | meaning-preserving cleanup + OCR red flags |
| `parsing.py` | line structure (relations, `or` lists, `\pm`, `f'(x)` heads) -> unevaluated SymPy via l2s |
| `equivalence.py` | expression equality: seeded numeric testing + SymPy |
| `solutions.py` | real solution sets and how two relate |
| `check_expression.py`, `check_relation.py`, `check_derivative.py` | the three step checkers |
| `malrules.py`, `calculus.py`, `tree.py` | mal-rule library, buggy differentiator, tree surgery helpers |
| `misreads.py` | alternative OCR readings used before raising an alarm |
| `findings.py`, `verdict.py` | internal/public result types |
| `synth/` | templates, correct-step transforms, error injection, OCR noise, evaluation metrics |
| `scripts/evaluate.py`, `scripts/compare_parsers.py` | evaluation report, parser bake-off |

## Known limitations

- **The clean evaluation is optimistic by construction.** The generator and the verifier were written by the same person and share the mal-rule library, rendering conventions and LaTeX style, so 100% recall on clean synthetic data is an upper bound, not a forecast. The hand-written tests are a better sanity check but are small: 15 realistic solutions, 51 tricky correct steps and 30 wrong steps.
- **OCR misreads that turn one valid formula into another cause false alarms.** A 5 read as 6, a dropped minus, or a dropped exponent is indistinguishable from a student slip at the single-step level. See "held-out noise" in RESULTS. This is the main product risk, and it needs OCR confidence and/or confirming the line with the student.
- **Scope.** One variable per equation. Out of scope, and returned as uncertain: equations with parameters, 2×2 systems (the stretch goal was not done), compound inequalities `1 < x < 3`, trig equations with infinitely many solutions, word problems, units and matrices.
- **No final-answer check.** An extraneous root that the student never rejects is reported in `extra_candidates` but not flagged. The app should check the final line against the original problem.
- SymPy auto-cancels identical factors (`(x-2)^2/(x-2)` becomes `x-2` on evaluation), which hides the excluded point `x = 2`. Only real-number semantics are supported.
- Diagnosis is ambiguous at times: a sign slip versus "sign not flipped", and slips versus specific rules. Unmodelled errors come back as `unclassified`, with a generic hint.
- Time limits: `solveset` gets a 2 s budget (a timed-out solve keeps running in a daemon thread, since Python threads cannot be killed). Everything else relies on size guards (≤ 80 operations, polynomial degree ≤ 6). A production service should also put a whole-request budget around each call.
- `confidence` is a hand-set heuristic. Calibrate it on real, labelled student data before using it for any threshold.
