# Results: Margin step verifier spike

Reproduce with `uv run python scripts/evaluate.py` (seeded, about 3 minutes on 12 processes). The tables at the bottom are generated. Everything above them is written by hand.

## Setup

- **Data.** 1,250 seeded synthetic solutions from 25 templates in 7 families: linear equations, quadratics (including completing the square and a radical equation solved by squaring and checking), rational expressions, polynomial expansion and factoring, powers and roots, derivatives, and linear inequalities.
  - Half are fully correct. The other half have **exactly one** error, injected with a mal-rule at a random applicable step. Later lines continue consistently from the wrong line, as a student would.
  - That gives 3,326 steps: 625 error steps and 2,701 correct steps.
- **Labels.** They come from how each solution was built, confirmed by separate SymPy checks inside the generator (`simplify`/`solveset` on its own trees), never from the verifier. Every generated line is also parsed back to check that the printed LaTeX means what its label says.
- **Conditions.**
  - `clean`.
  - `ocr_noise`: 35% of lines get one of the listed recognition errors: missing braces, `x2` for `x^2`, unicode minus, `\cdot` added or removed, l/1, O/0, S/5, stray spaces.
  - `held_out_noise`: 35% of lines get a misread the verifier was **not** designed for: a digit replaced by a look-alike (5/6, 1/7, 3/8, ...), a dropped minus sign, or a dropped exponent. These produce valid LaTeX with different maths.
  - A sweep at 2%, 5% and 10% of lines.
  - The two opt-in policies, `strict_ocr` and `confirm_with_next_line`.
- **Metrics.**
  - recall@line: share of error steps flagged `invalid` on exactly the injected line.
  - precision: share of `invalid` flags that fall on the injected error.
  - FA/correct step: false alarms per correct step.
  - FA/correct solution: share of fully correct solutions that get at least one false alarm.
  - uncertain rate.
  - diagnosis accuracy: share of detected errors whose `error_type` equals the injected rule.
- **Independent hand-written checks** (in `tests/`, written without the generator): 15 realistic student solutions, 51 tricky *correct* steps, and 30 wrong steps.

## Headline

| condition | recall@line | precision | FA / correct step | FA / correct solution | uncertain on correct steps | diagnosis acc. |
|---|---|---|---|---|---|---|
| clean | **1.000** | **1.000** | **0 / 2,701** | **0 / 625** | 0.0% | 93.1% |
| anticipated OCR noise (35% of lines) | 0.763 | 1.000 | **0 / 2,701** | **0 / 625** | 18.0% | 92.2% |
| held-out OCR misreads (35% of lines) | 0.958 | 0.296 | 52.7% | 74.9% | 1.3% | 43.6% |
| held-out misreads, 5% of lines | 0.992 | 0.709 | 9.4% | 15.5% | 0.1% | 83.1% |
| held-out misreads, 5%, `confirm_with_next_line` | 0.990 | 0.824 | 4.9% | 8.8% | 4.7% | 83.0% |

Hand-written sets:
- 51 tricky correct cases (55 steps): **0 flagged** (54 valid, 1 uncertain).
- 15 realistic correct solutions (40 steps): all valid.
- 3 realistic solutions with one error: exactly one alarm each, on the right line.
- 30 hand-written wrong steps: **30/30 flagged**, all with the expected diagnosis (23 name a mal-rule, 7 are correctly `unclassified`).

Two of the 30 wrong-step labels were first written by hand as "slip" and "unclassified"; the verifier's diagnoses Two of the 30 wrong-step labels were first written by hand as "slip" and "unclassified"; the verifier's diagnoses (`distribute_first_term_only` for `-(x+1) -> -x+1`, and `cancel_across_addition`) were the better ones, so the labels were corrected.

Latency on a desktop CPU, single process: 16 ms per step on average, 50 ms at p95. Import takes 0.6 s.

## How to read these numbers

- **The clean row is an upper bound, not a forecast.** The generator and the verifier share the mal-rule library, the LaTeX conventions and their author. A student's real mistakes, notation and handwriting will be messier. The hand-written sets are independent but small. The first real test needs real student photos with labels.
- **With the anticipated noise, "never flag a correct step" held: 0 false alarms in 2,701 correct steps.** The cost is abstention.
  - 1,560 of the 2,701 correct steps had a noisy line. 31% of those came back `uncertain` and the rest `valid`.
  - Recall on errors whose lines were touched by noise fell to 61% (231/376). On untouched error steps it stayed at 99% (246/249).
  - Confusable letters (`S`, `l`, `O`) and `x2` send about 100% of affected steps to `uncertain` (see the noise-type table). Unicode minus, `\cdot` changes and stray spaces are almost always read correctly.
- **The held-out misreads are the real risk.** A `4` read as `9`, a dropped minus or a dropped exponent turns a correct line into a different *valid* formula. No step-level check can tell that apart from a student's slip. At a 5% line misread rate, 15.5% of perfectly correct solutions would get a false alarm.

## Failure-mode analysis

1. **OCR misreads that produce valid but different maths.** This is the dominant failure, and it is not fixable inside the verifier alone.
   - False alarms grow roughly linearly with the misread rate: about 5% of correct solutions at 2% of lines misread, 16% at 5%, and 28% at 10%.
   - Two mitigations were measured:
     - `confirm_with_next_line` roughly halves false alarms at realistic misread rates (≤ 10% of lines), at almost no recall cost. It uses the fact that a misread middle line causes two alarms in a row that disappear when the line is skipped, while a real mistake is followed by consistent work.
     - `strict_ocr`, which abstains when a one-character confusion would fix the step, cuts false alarms to 14% of correct steps at 35% noise. But it costs 19.5% of recall even on clean data, because real slips are often one character away from right.
   - With confirmation on, the false alarms that remain sit on **line 0 (the problem statement) or on the final line**: at 5% misreads, 110 of 132 of them (see "Where the false alarms..." below). Those lines have no neighbour on one side to cross-check against.
2. **Abstentions under anticipated noise are mostly safe by design.** The top reasons are:
   - `could_not_solve` (316): a misread `S`/`l`/`O` turns a one-variable equation into a two-variable one.
   - `possible_misread` (186): an OCR flag or a repaired reading makes the step correct.
   - `unreadable_line` (31).
   - `cannot_check_dropped_root` (4): rejecting a root cannot be verified because an earlier line was misread.
3. **Diagnosis confusions.** Detection is fine, but naming the error is not. `arithmetic_slip` is diagnosed correctly 88% of the time.
   - It is confused with `sign_not_flipped_on_move` (11 cases): a sign slip on a moved constant is the same line.
   - It comes back `unclassified` (24 cases): the slip happened inside a combined step, so the student's line is not one number away from a correct line.
   - Diagnosis by solution set alone blamed a wrong factoring (`x^2-9=0 -> (x-3)^2=0`) on "divided by x+3", because both give the same roots. This was fixed by requiring the rule's output to be the same equation up to a constant factor. It is still a sign that hints should be phrased so a wrong diagnosis does little harm.
4. **Bugs the evaluation caught during the spike** (all fixed, with regression tests). Each one would have produced false alarms or crashes on real input:
   - A lone `S` in a line was picked as "the variable", so the confusable-letter guard did not fire.
   - Dropped braces turned `x^{4+6}` into `x^4 + 6`, a valid formula that is not flagged.
   - An OCR `I` became the imaginary unit and crashed the root finder.
   - Rejecting an extraneous root was judged against an earlier line that was itself misread.
   - Prose ("Let x be the number") was read as a product of letters.
   - Repaired readings that were only implication-valid were used to excuse errors.
   - `solveset` ran for minutes on some radical equations, so there is now a 2 s budget. Cubics created by repaired readings took about 50 s per solution; they are now solved by exact root isolation.
   - The parser's mixed-number rule read `2(3)` as 5.
5. **Scope limits.** These abstain rather than fail:
   - equations with parameters or a second unknown, 2×2 systems, compound inequalities `1 < x < 3`, and trig equations with infinitely many solutions;
   - lines with words;
   - `sqrt(x^2) = x` and similar steps that are only true for positive values.

   Not handled at all: final-answer checking. An extraneous root that the student never rejects is only listed in `extra_candidates`.

## Recommendations for the product

**Must abstain in v1.** The verifier already does all of these:
- any line with OCR red flags, unreadable text, prose or `\text{}`;
- letters that look like digits, or letters that appear from nowhere;
- steps with more than one unknown;
- steps that are only true for positive values;
- dropped roots that cannot be checked against a trustworthy earlier line;
- solver timeouts and any internal error.

**Before the app speaks, the product needs:**
1. **A confidence gate from the OCR.** Speak only if the recogniser is confident about the tokens that changed between the two lines (`explanation.term_diff`, the lost/extra values). The verifier cannot see this, and it is the only real defence against held-out misreads.
2. **Wait for the next line** (`confirm_with_next_line=True`). This halves misread false alarms, and not interrupting mid-thought is good UX anyway.
3. **Confirm line 0 and the final line with the student.** Ask "Is this the problem?" at the start, and before commenting on a final answer, show the recognised line ("I read x = 7. Is that what you wrote?"). This targets most of the false alarms that remain with confirmation on. A one-tap confirmation before any hint is a cheap universal safety net: it costs one interaction per alarm, and alarms are rare for good students.
4. **Budget.** The OCR should misread well under 2% of lines in digit- or sign-changing ways, or the confirmation step must be mandatory.

**Scope that is safe for v1:**
- one-variable linear equations and inequalities;
- quadratics (factoring, square roots with ±, completing the square);
- polynomial expansion and factoring;
- rational-expression simplification;
- exponent rules;
- power, chain and product rule derivatives.

These are the areas with measured zero false alarms on clean and anticipated-noise data, and full coverage by hand-written tests.

Defer to later versions: systems of equations, word problems, trig identities and trig equations, and anything with parameters. Treat radical and rational equations (which can add extraneous roots) as "hint only when the student has clearly finished". Also add a final-answer check against the original problem.

**Next steps to make these numbers mean something:**
- Collect 100 to 200 real photographed student solutions and run them end-to-end through the chosen OCR. Measure the real misread rate and the false alarms per session. Calibrate `confidence` on those.
- Replace this synthetic noise model with the confusion matrix measured from that OCR.

## Generated tables

<!-- BEGIN GENERATED -->
_Generated by `scripts/evaluate.py --solutions 1250 --seed 7` (1250 solutions per condition, 162s wall time)._

### Headline

| group | solutions | error steps | correct steps | recall@line | precision | false alarms | FA/correct step | FA/correct solution | uncertain (correct) | uncertain (error) | errors called valid | diagnosis acc. | s/step mean | s/step p95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 1250 | 625 | 2701 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.931 | 0.016 | 0.050 |
| ocr_noise | 1250 | 625 | 2701 | 0.763 | 1.000 | 0 | 0.000 | 0.000 | 0.180 | 0.237 | 0 | 0.922 | 0.011 | 0.033 |
| held_out_noise | 1250 | 625 | 2701 | 0.958 | 0.296 | 1424 | 0.527 | 0.749 | 0.013 | 0.010 | 20 | 0.436 | 0.044 | 0.151 |
| clean | strict | 1250 | 625 | 2701 | 0.805 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.195 | 0 | 0.932 | 0.053 | 0.233 |
| clean | confirm | 1250 | 625 | 2701 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.931 | 0.008 | 0.024 |
| ocr_noise | confirm | 1250 | 625 | 2701 | 0.763 | 1.000 | 0 | 0.000 | 0.000 | 0.180 | 0.237 | 0 | 0.922 | 0.009 | 0.027 |
| held_out_noise | strict | 1250 | 625 | 2701 | 0.848 | 0.584 | 377 | 0.140 | 0.309 | 0.400 | 0.120 | 20 | 0.402 | 0.124 | 0.428 |
| held_out_noise | confirm | 1250 | 625 | 2701 | 0.952 | 0.370 | 1011 | 0.374 | 0.606 | 0.165 | 0.016 | 20 | 0.434 | 0.020 | 0.048 |
| held_out_noise | strict+confirm | 1250 | 625 | 2701 | 0.848 | 0.602 | 351 | 0.130 | 0.294 | 0.410 | 0.120 | 20 | 0.402 | 0.084 | 0.272 |

### False alarms vs. OCR misread rate (held-out noise on a given share of lines)

| group | solutions | error steps | correct steps | recall@line | precision | false alarms | FA/correct step | FA/correct solution | uncertain (correct) | uncertain (error) | errors called valid | diagnosis acc. | s/step mean | s/step p95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| held_out@2% | 1250 | 625 | 2701 | 0.998 | 0.891 | 76 | 0.028 | 0.051 | 0.001 | 0.000 | 1 | 0.905 | 0.010 | 0.029 |
| held_out@2% | confirm | 1250 | 625 | 2701 | 0.997 | 0.934 | 44 | 0.016 | 0.034 | 0.013 | 0.002 | 1 | 0.905 | 0.009 | 0.028 |
| held_out@5% | 1250 | 625 | 2701 | 0.992 | 0.709 | 255 | 0.094 | 0.155 | 0.001 | 0.002 | 4 | 0.831 | 0.015 | 0.039 |
| held_out@5% | confirm | 1250 | 625 | 2701 | 0.990 | 0.824 | 132 | 0.049 | 0.088 | 0.047 | 0.003 | 4 | 0.830 | 0.011 | 0.032 |
| held_out@10% | 1250 | 625 | 2701 | 0.990 | 0.568 | 471 | 0.174 | 0.283 | 0.005 | 0.003 | 4 | 0.758 | 0.020 | 0.056 |
| held_out@10% | confirm | 1250 | 625 | 2701 | 0.986 | 0.711 | 250 | 0.093 | 0.181 | 0.087 | 0.008 | 4 | 0.758 | 0.013 | 0.035 |

### Clean data, by problem family

| group | solutions | error steps | correct steps | recall@line | precision | false alarms | FA/correct step | FA/correct solution | uncertain (correct) | uncertain (error) | errors called valid | diagnosis acc. | s/step mean | s/step p95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| derivative | 200 | 100 | 162 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 1.000 | 0.029 | 0.055 |
| inequality | 100 | 50 | 288 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.920 | 0.041 | 0.158 |
| linear_equation | 250 | 125 | 749 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.944 | 0.009 | 0.025 |
| polynomial | 200 | 100 | 233 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.940 | 0.013 | 0.030 |
| powers_roots | 100 | 50 | 170 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.880 | 0.007 | 0.019 |
| quadratic_equation | 250 | 125 | 903 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.912 | 0.012 | 0.035 |
| rational_expression | 150 | 75 | 196 | 1.000 | 1.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.880 | 0.019 | 0.061 |

### Clean data, by injected mal-rule

| mal-rule | n | recall@line | uncertain | errors called valid | diagnosis acc. | most confused with |
|---|---|---|---|---|---|---|
| add_fractions_add_denominators | 17 | 1.000 | 0.000 | 0 | 1.000 | - |
| arithmetic_slip | 355 | 1.000 | 0.000 | 0 | 0.882 | unclassified (24), sign_not_flipped_on_move (11), distribute_first_term_only (3) |
| cancel_across_addition | 12 | 1.000 | 0.000 | 0 | 1.000 | - |
| chain_rule_omitted | 17 | 1.000 | 0.000 | 0 | 1.000 | - |
| distribute_first_term_only | 22 | 1.000 | 0.000 | 0 | 0.955 | divide_one_term_only (1) |
| divide_by_variable | 11 | 1.000 | 0.000 | 0 | 1.000 | - |
| divide_one_term_only | 28 | 1.000 | 0.000 | 0 | 1.000 | - |
| exponent_product_multiply | 11 | 1.000 | 0.000 | 0 | 1.000 | - |
| inequality_not_flipped | 15 | 1.000 | 0.000 | 0 | 1.000 | - |
| power_rule_no_decrement | 35 | 1.000 | 0.000 | 0 | 1.000 | - |
| product_rule_as_product | 12 | 1.000 | 0.000 | 0 | 1.000 | - |
| sign_not_flipped_on_move | 60 | 1.000 | 0.000 | 0 | 1.000 | - |
| sqrt_missing_pm | 7 | 1.000 | 0.000 | 0 | 1.000 | - |
| sqrt_of_sum | 9 | 1.000 | 0.000 | 0 | 1.000 | - |
| square_of_sum | 14 | 1.000 | 0.000 | 0 | 1.000 | - |

### With anticipated OCR noise, by problem family

| group | solutions | error steps | correct steps | recall@line | precision | false alarms | FA/correct step | FA/correct solution | uncertain (correct) | uncertain (error) | errors called valid | diagnosis acc. | s/step mean | s/step p95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| derivative | 200 | 100 | 162 | 0.790 | 1.000 | 0 | 0.000 | 0.000 | 0.136 | 0.210 | 0 | 1.000 | 0.030 | 0.073 |
| inequality | 100 | 50 | 288 | 0.800 | 1.000 | 0 | 0.000 | 0.000 | 0.135 | 0.200 | 0 | 0.950 | 0.012 | 0.013 |
| linear_equation | 250 | 125 | 749 | 0.768 | 1.000 | 0 | 0.000 | 0.000 | 0.163 | 0.232 | 0 | 0.948 | 0.007 | 0.022 |
| polynomial | 200 | 100 | 233 | 0.820 | 1.000 | 0 | 0.000 | 0.000 | 0.137 | 0.180 | 0 | 0.939 | 0.011 | 0.027 |
| powers_roots | 100 | 50 | 170 | 0.740 | 1.000 | 0 | 0.000 | 0.000 | 0.294 | 0.260 | 0 | 0.784 | 0.010 | 0.029 |
| quadratic_equation | 250 | 125 | 903 | 0.688 | 1.000 | 0 | 0.000 | 0.000 | 0.209 | 0.312 | 0 | 0.895 | 0.010 | 0.027 |
| rational_expression | 150 | 75 | 196 | 0.760 | 1.000 | 0 | 0.000 | 0.000 | 0.158 | 0.240 | 0 | 0.860 | 0.014 | 0.047 |

### With anticipated OCR noise, by mal-rule

| mal-rule | n | recall@line | uncertain | errors called valid | diagnosis acc. | most confused with |
|---|---|---|---|---|---|---|
| add_fractions_add_denominators | 17 | 0.529 | 0.471 | 0 | 1.000 | - |
| arithmetic_slip | 355 | 0.763 | 0.237 | 0 | 0.875 | unclassified (21), sign_not_flipped_on_move (9), distribute_first_term_only (2) |
| cancel_across_addition | 12 | 0.500 | 0.500 | 0 | 1.000 | - |
| chain_rule_omitted | 17 | 0.647 | 0.353 | 0 | 1.000 | - |
| distribute_first_term_only | 22 | 0.909 | 0.091 | 0 | 0.950 | divide_one_term_only (1) |
| divide_by_variable | 11 | 0.818 | 0.182 | 0 | 1.000 | - |
| divide_one_term_only | 28 | 0.786 | 0.214 | 0 | 1.000 | - |
| exponent_product_multiply | 11 | 0.818 | 0.182 | 0 | 0.778 | unclassified (2) |
| inequality_not_flipped | 15 | 0.867 | 0.133 | 0 | 1.000 | - |
| power_rule_no_decrement | 35 | 0.857 | 0.143 | 0 | 1.000 | - |
| product_rule_as_product | 12 | 1.000 | 0.000 | 0 | 1.000 | - |
| sign_not_flipped_on_move | 60 | 0.733 | 0.267 | 0 | 1.000 | - |
| sqrt_missing_pm | 7 | 0.714 | 0.286 | 0 | 1.000 | - |
| sqrt_of_sum | 9 | 0.444 | 0.556 | 0 | 1.000 | - |
| square_of_sum | 14 | 0.857 | 0.143 | 0 | 1.000 | - |

### Why the verifier abstained (top reasons for `uncertain`)

| condition | on correct steps | on error steps |
|---|---|---|
| clean | - | - |
| clean | confirm | - | - |
| clean | strict | - | possible_misread (122) |
| held_out@10% | possible_misread (13) | possible_misread (2) |
| held_out@10% | confirm | isolated_misread (221), possible_misread (13) | isolated_misread (3), possible_misread (2) |
| held_out@2% | possible_misread (4) | - |
| held_out@2% | confirm | isolated_misread (32), possible_misread (4) | isolated_misread (1) |
| held_out@5% | possible_misread (3) | possible_misread (1) |
| held_out@5% | confirm | isolated_misread (123), possible_misread (3) | possible_misread (1), isolated_misread (1) |
| held_out_noise | possible_misread (32), unsupported_expression (2) | possible_misread (6) |
| held_out_noise | confirm | isolated_misread (413), possible_misread (32), unsupported_expression (2) | possible_misread (6), isolated_misread (4) |
| held_out_noise | strict | possible_misread (1079), unsupported_expression (2) | possible_misread (75) |
| held_out_noise | strict+confirm | possible_misread (1079), isolated_misread (26), unsupported_expression (2) | possible_misread (75) |
| ocr_noise | could_not_solve (293), possible_misread (159), unreadable_line (22), cannot_check_dropped_root (9) | possible_misread (83), could_not_solve (55), unreadable_line (6), cannot_check_dropped_root (4) |
| ocr_noise | confirm | could_not_solve (293), possible_misread (159), unreadable_line (22), cannot_check_dropped_root (9) | possible_misread (83), could_not_solve (55), unreadable_line (6), cannot_check_dropped_root (4) |

### Correct transitions touched by each noise type

| noise type | correct steps touched | valid | uncertain | false alarms |
|---|---|---|---|---|
| O_for_0 | 103 | 0.000 | 1.000 | 0 |
| S_for_5 | 128 | 0.000 | 1.000 | 0 |
| cdot_toggle | 246 | 0.947 | 0.053 | 0 |
| l_for_1 | 185 | 0.005 | 0.995 | 0 |
| missing_braces | 209 | 0.718 | 0.282 | 0 |
| stray_spaces | 558 | 0.896 | 0.104 | 0 |
| unicode_minus | 360 | 0.906 | 0.094 | 0 |
| x2_for_x_squared | 51 | 0.196 | 0.804 | 0 |
| digit_swap | 955 | 0.044 | 0.006 | 907 |
| dropped_exponent | 241 | 0.137 | 0.008 | 206 |
| dropped_minus | 525 | 0.088 | 0.061 | 447 |

### Where the false alarms under held-out noise are

| condition | false alarms | involve line 0 | involve the final line | both | middle only |
|---|---|---|---|---|---|
| held_out@10% | 471 | 133 | 145 | 19 | 174 |
| held_out@10% | confirm | 250 | 94 | 90 | 19 | 47 |
| held_out@2% | 76 | 25 | 25 | 1 | 25 |
| held_out@2% | confirm | 44 | 17 | 18 | 1 | 8 |
| held_out@5% | 255 | 76 | 77 | 11 | 91 |
| held_out@5% | confirm | 132 | 55 | 44 | 11 | 22 |
| held_out_noise | 1424 | 420 | 439 | 54 | 511 |
| held_out_noise | confirm | 1011 | 335 | 356 | 54 | 266 |
| held_out_noise | strict | 377 | 106 | 138 | 21 | 112 |
| held_out_noise | strict+confirm | 351 | 99 | 129 | 21 | 102 |

### False alarms (every one, all conditions)

- [held_out@10%] 471 false alarms (not listed; see results/transitions.jsonl)
- [held_out@10% | confirm] 250 false alarms (not listed; see results/transitions.jsonl)
- [held_out@2%] 76 false alarms (not listed; see results/transitions.jsonl)
- [held_out@2% | confirm] 44 false alarms (not listed; see results/transitions.jsonl)
- [held_out@5%] 255 false alarms (not listed; see results/transitions.jsonl)
- [held_out@5% | confirm] 132 false alarms (not listed; see results/transitions.jsonl)
- [held_out_noise] 1424 false alarms (not listed; see results/transitions.jsonl)
- [held_out_noise | confirm] 1011 false alarms (not listed; see results/transitions.jsonl)
- [held_out_noise | strict] 377 false alarms (not listed; see results/transitions.jsonl)
- [held_out_noise | strict+confirm] 351 false alarms (not listed; see results/transitions.jsonl)

### Missed errors on clean data (every one)

- none
<!-- END GENERATED -->
