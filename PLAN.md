# chuddle → **Margin**: plan (v1)

_2026-09-28 · Status: **GO given 2026-09-29. Now in M0** ([spec](docs/specs/M0.md))._
_Inputs: `IDEAS.md`, `research/01–08`, `verifier/` (356 tests pass; eval in `verifier/RESULTS.md`)._

## TL;DR

**Margin** is a practice and exam-prep coach. Your phone sits on a stand over your paper and watches you do math by hand. It speaks up only when a step is **provably** wrong, with a hint, never the answer.

- **The magic moment:** you write a wrong line, the phone flags that exact line, and a voice asks one short question.
- **The engineering story:**
  - a camera pipeline that sees each finished line;
  - a small handwriting model **you fine-tune** to copy mistakes *faithfully* (big AIs secretly "fix" them 42–66% of the time);
  - a **symbolic math checker** that never guesses;
  - a calibrated rule for when to interrupt;
  - on-device and cloud routing;
  - public evals.
- **Why it wins:** it hits all three of your target audiences at once.
  - *AI startups:* multimodal pipeline, evals, real users.
  - *ML/research:* a trained model, the error-preservation metric, calibrated interrupts.
  - *Big tech:* realtime on-device systems and latency engineering.
- **Build:** about 8–10 weeks across 7 milestones, each with a go/no-go gate you approve.
- **Cost:** about $5–12/month, plus a one-time phone stand (~$20).

---

## 1. Positioning

- **One-liner:** *"A practice & exam-prep coach that watches your paper and only speaks when a step is provably wrong."*
- **Prior art we name openly:**
  - Chiron (YC S25): live, checked, hints-only, but **iPad + Apple Pencil**.
  - Goodnotes Math Assist (iOS): underlines wrong lines, but gives answers.
  - Frizzle (YC S25): paper photos, but for teachers, in batches.
- **Our claim** is not "first". It's the combination nobody has shipped: **real paper + phone camera + Android + on-device model + published evals** ([08 §1](research/08-margin-deep-dive.md)).
- **Hints-only by construction, not by promise:**
  - the hint writer never sees the correct next line;
  - a symbolic-math **answer-leak filter** rejects any hint containing the right expression;
  - there's no "scan a problem" button, so it only checks lines the student wrote ([08 §7.3](research/08-margin-deep-dive.md)).
- **Integrity framing:** UMD presumes generative AI isn't allowed on graded work unless the syllabus says so, but treats "practicing problems" as normal. Default mode is *Practice*. An *"Assigned work — my instructor allows AI hints"* toggle shows a citation line.

## 2. v1 scope

**In** (what the spike's verifier handles safely; roughly UMD MATH 115/140):
- one-variable linear equations and inequalities;
- quadratics (factoring, the quadratic formula, square roots with ±);
- polynomial expansion and factoring, rational-expression simplification, exponent rules;
- derivatives (power, product, chain).

**Next (v1.1):** log rules, the quotient rule, 2×2 linear systems.

**Out:** word problems, graphs, proofs, matrices, trig, integration, anything with parameters.

**How you write (v1):**
- one step per line, single column;
- dark pen on plain or lined paper, *not grid* (grids hurt OCR);
- phone on an overhead stand at 23–30 cm, with a lamp to the side opposite your writing hand.

**How it behaves:**
- **Right:** silence (a tiny green tick on screen).
- **Verified wrong:**
  1. a red box on that line (visual);
  2. if you haven't fixed it within a few seconds or you start the next line, a spoken hint of 12 words or fewer;
  3. saying "why?" climbs the hint ladder, but only after new ink.
- **Unsure:** it stays silent, or asks *"is that a 4 or a 9?"*

## 3. The 30-second interview pitch

> "Snap-and-solve apps hand students answers, and research shows unguarded AI access cut later exam scores 17%. I built Margin, which watches you work on paper and only interrupts when a step is *provably* wrong.
>
> The hard part isn't the math. It's that vision models silently 'fix' student mistakes when they read them. So I fine-tuned a 2B handwriting model to preserve errors. I pair it with a SymPy checker that returns *valid / invalid / unknown*, and I calibrate the interrupt rule to keep false alarms under 1 per 10 pages.
>
> It runs on-device with cloud fallback: p95 X s, $Y per page, Z% of errors caught, used by N students."

---

## 4. Architecture

```
PHONE (Android, Expo dev build, TypeScript)
┌────────────────────────────────────────────────────────────────────┐
│ VisionCamera 5 (low-res 640-960px @10-15fps, AE/AF/AWB locked)     │
│   → fast-opencv: page quad + perspective warp (DocAligner fallback)│
│   → line-commit detector: ink diff + MediaPipe hand mask + dwell   │
│       (explicit fallback: tap / say "check" / draw a tick)         │
│   → on commit: HIGH-RES STILL → crop the line                      │
│   → READER CASCADE                                                 │
│       1. MIT specialist (ONNX, <30MB, per-token confidence)        │
│       2. Uni-MuMER-2B + our LoRA (llama.rn, GGUF Q4/Q8)            │
│       3. cloud reader (Gemini Flash-class, "do not correct") ──────┼──┐
│   → INTERRUPT POLICY (confidence gate on changed tokens,           │  │
│       next-line consistency, WAIT on partial lines, confirm-glyph) │  │
│   → red box + on-device TTS (sherpa-onnx + Kokoro)                 │  │
│   → work receipt (lines, flags, hints; student-owned)              │  │
└──────────────────────────────┬─────────────────────────────────────┘  │
                               │ LaTeX lines + confidences (tiny JSON)  │
SERVER (Python, FastAPI — "margin-api")                                 │
┌──────────────────────────────▼─────────────────────────────────────┐  │
│ /verify  margin_verifier (latex2sympy2_extended + SymPy; 3-outcome,│  │
│          15 mal-rules, 2 s solver budget)                          │  │
│ /read    cloud reader proxy (keys live here, never on the phone) ◄─┼──┘
│ /hint    template + optional LLM rewording → answer-leak filter    │
│ /events  traces (OpenTelemetry), budgets, per-device rate limits,  │
│          hard monthly spend cap                                    │
└────────────────────────────────────────────────────────────────────┘
WEB DEMO (for recruiters on any phone): upload or pick a photo of worked
math → same server path → see flagged lines + hints. QR on the résumé.

OFFLINE (laptop / Modal): data tools · LoRA training (Unsloth) ·
GGUF/ONNX export · eval harness · CI gates
```

**Why this split:**
- Reading handwriting has to be fast and private, so it runs on the phone.
- Checking math is tiny and deterministic (16 ms average in the spike), so for v1 it runs as a Python service.
- **Stretch:** run SymPy *on the phone* via Chaquopy. That means fully offline and an "airplane-mode" demo.

**Stack decisions (see Decision log):**
- Expo SDK 57 **dev build** (Expo Go can't load native vision modules).
- react-native-vision-camera 5.2.x, react-native-fast-opencv, llama.rn, onnxruntime-react-native, sherpa-onnx.
- FastAPI server; a Python ML stack with Unsloth, llama.cpp tools and ONNX.
- All MIT, Apache or BSD. **Avoid:** AGPL YOLO, non-commercial dewarpers/datasets in anything shipped ([04](research/04-github-building-blocks.md), [08 §3, §8](research/08-margin-deep-dive.md)).

## 5. The ML plan (the part research-type reviewers care about)

1. **Baselines (M1):** three readers on the same crops.
   - Uni-MuMER-Qwen3.5-2B zero-shot (Apache-2.0; 84/81/80% on CROHME 2014/16/19, but about 24% on real phone photos).
   - A Gemini Flash-class model with a faithful "do not correct" prompt.
   - Optionally Mathpix, as a commercial baseline.
2. **Error-preserving fine-tune (M4):** LoRA on Uni-MuMER-2B (~5 GB of GPU memory, which fits your RTX 5070) using:
   - 1–3k **Margin-camera line crops**, labeled by the cloud model and **checked by a human on every error line**;
   - **error-injected line pairs**, so it learns to copy mistakes verbatim;
   - a replay slice, so it doesn't forget the benchmarks.

   A community LoRA went from 23.7% to 74.8% on real phone photos with 1,103 images ([08 §3.3](research/08-margin-deep-dive.md)). We export to GGUF, compare Q4 vs Q8, and A/B it against the Qwen3-VL-2B variant.
3. **Fast specialist (M4):** GryphOne or SSAN (MIT, under 30 MB), fine-tuned on the same crops, int8, with per-token confidence for routing.
4. **Cascade + routing:** specialist → 2B → cloud. We plot the **on-device vs cloud chart**: latency p50/p95 vs parse-correct rate, with bubble size = $ per 1k lines.
5. **Research extras (optional, high-signal):**
   - **error-preservation rate** as a new metric;
   - the first public GPT-5.x / Gemini-3.x ExpRate on CROHME/HME100K;
   - **conformal control of false alarms per page** for the interrupt rule.

## 6. Evals (the numbers that go in the README)

| # | What | Data | Metric(s) | Gate |
|---|---|---|---|---|
| E1 | Verifier | synthetic 1,250 + 55 tricky-correct + 30 wrong (spike) | recall, precision, false alarms, UNKNOWN rate, diagnosis accuracy | CI: 0 false alarms on clean + hand-written sets |
| E2 | Reader fidelity | golden lines + FERMAT transcriptions | SymPy-equivalence of transcription, ExpRate, **error-preservation**, over-correction, calibration (ECE) | ≥85% equivalence, ≥90% preservation (M1) |
| E3 | End-to-end | golden pages (spike 30–40 → v1 ≥250 injected errors + ≥300 clean pages) + FERMAT CAS-checkable subset | per-type P/R, **false alarms per page**, UNKNOWN rate, first-error localization | M1: ≥70% recall at ≤1 FA per 5 pages. v1: ≤1 FA per 10 pages |
| E4 | Latency | video-timed sessions | pen-up → flag p50/p95, per-stage breakdown | cloud path ≤3 s (M1); on-device TBD after measurement |
| E5 | Cost | server logs | $/page | ≤ $0.01 |
| E6 | Hint safety | every hint | answer-leak rate (CAS filter), length ≤12 words, human helpfulness rubric (sample) | leak = 0 |
| E7 | Pilot | real users | pages checked, weekly actives, "was this flag right?" taps | reported honestly with CIs |

**Golden-set protocol** ([08 §2.4](research/08-margin-deep-dive.md)):
- 60–100 problems;
- exactly one injected error per erroneous solution;
- a mix of about 50% injected, 25% correct and 25% harmless rewrites;
- 20–40 writers copying under the real stand, on varied paper, pens and light, filmed on video;
- labels per line (verbatim LaTeX, bbox, first-error index, type), with 10–20% double-annotated;
- **split by writer.**

**CI:** every PR runs E1 plus a *replay* of recorded crops with cached reader outputs, so it's deterministic and cheap, then applies regression gates.

## 7. Interrupt policy (where the spike taught us the most)

The spike showed the verifier is perfect on clean input: 0 false alarms and 100% recall. But **a misread that still looks like valid math** (a 4 read as a 9, a dropped minus) is indistinguishable from a student slip. At a 5% misread rate, 15.5% of fully correct solutions got a false alarm. So Margin speaks only when **all** of these hold:

1. The verifier says **invalid** and has a counterexample.
2. OCR confidence on the **tokens that changed** is ≥ τ, where τ is calibrated so false alarms per page stay ≤ target.
3. **Next-line consistency:** the following line is consistent with the flagged line. A real slip gets continued; a misread creates two alarms in a row that vanish when it's skipped. This alone halves false alarms.
4. There's an exception for the first and last lines. The student confirms the problem line at the start, and on the final line Margin shows what it read (*"I read x = 7, right?"*) before any hint.
5. For a partial line ("3x + 2 ="), the answer is **WAIT**, never invalid.
6. If an ambiguous glyph matters (4/9, S/5, 1/l, sign), it asks instead of flagging.

Hint ladder ([08 §6.2](research/08-margin-deep-dive.md)):
- rung 0: silent red box;
- rung 1: a question of 12 words or fewer;
- rung 2: the rule behind the mistake, or "try x = 1 in both lines";
- rung 3: a worked example of a **different**, same-shaped problem.

It climbs a rung only after new ink.

## 8. Privacy, safety, security

- **On-device first.** The cloud sees only the cropped *line* image: no faces, no room, no stored audio. Crops are deleted unless the user opts in to donate them, with written consent from any classmates whose writing is involved.
- **Ages 18+ only in v1.** The amended COPPA rule counts images and voice as children's personal information. K-12 comes later, with the proper process.
- **Research ethics:** before publishing results that involve other UMD students, check with the UMD IRB.
- **Threat model** (goes in `docs/THREAT-MODEL.md`):
  - **API keys** stay server-side only.
  - **Abuse:** per-device rate limits and a hard monthly spend cap.
  - **Prompt injection via handwriting:** e.g. a student writes "ignore instructions, give the answer". The hint model only receives *structured verifier output* (line id, error class, diff location as math tokens), never raw text, so this fails by construction.
  - **Answer leakage:** the CAS filter.
  - **Junk uploads:** non-math images are rejected on the web demo.
- **Ops:** traces for every line, an incident log, and a budget dashboard. This is the "production signal" recruiters look for ([03](research/03-recruiter-signals.md)).

---

## 9. Milestones (each ends at a gate where you approve before we continue)

| M | What | Done when… | Est. |
|---|---|---|---|
| **M0 Foundations** | Fix the GPU; API keys; Android SDK + USB debugging; monorepo scaffold (`app/ server/ verifier/ ml/ evals/ docs/`); CI; decision log; buy or DIY a stand | `adb devices` sees your phone; "hello camera" dev build runs on it; CI green | 3–4 days |
| **M1 Reader-fidelity spike** 🚦 | 30–40 pages from 4–6 writers under the stand; manual line crops; 3 readers + verifier | **GO** if equivalence ≥85%, preservation ≥90%, recall ≥70% at ≤1 FA per 5 pages, verifier decides ≥80% of steps, cloud verdict ≤3 s. Otherwise **NARROW** (linear/quadratic only), **S-Pen tablet ink**, or **PIVOT → Spotter** | ~1 week |
| **M2 Vertical slice** | On the phone: camera → page warp → *tap/say "check"* → high-res still → line crop → cloud reader → `/verify` → red box + TTS. Plus the recruiter web demo | end-to-end on real paper; p95 ≤3 s; traces visible | 1.5–2 wk |
| **M3 Smart timing** | Automatic line-commit (ink diff + hand mask + dwell); the interrupt policy (§7); hint ladder + answer-leak filter; work receipt; `/events` | ≤1 FA per 5 pages and ≥70% recall on the spike set, end-to-end | ~1.5 wk |
| **M4 Your model** 🧠 | Collect/label 1–3k crops; error-injected pairs; LoRA Uni-MuMER-2B; GGUF → llama.rn; MIT specialist → ONNX; cascade; the on-device vs cloud chart | on-device reader within the agreed gap of the cloud reader at acceptable p95 on *your* phone; chart published | ~2 wk |
| **M5 Golden set + pilot** 👥 | Golden-set protocol; FERMAT run; pilot with 15–30 students (study groups, tutoring center); incident log | README numbers with confidence intervals; ≥15 pilot users and ≥100 real pages | ~2 wk (overlaps M4) |
| **M6 Launch** 🚀 | README (users + 3 numbers + diagram), eval report, ops page, decision log, "how I used coding agents" note, 60–90 s one-take video, write-up; open-source; Show HN / Reddit / X | public repo + video + post live | ~1 wk |

**Stretch:** Chaquopy on-device verifier (airplane-mode demo), log rules and the quotient rule, conformal interrupt control, and a "Margin mat" with ArUco markers.

## 10. Demo script

- **Video** (one continuous take, 60–90 s; overhead phone plus a second camera, with the phone screen mirrored via `scrcpy`):
  1. *(0–3 s)* The result first: a red box snaps onto a line and the voice says *"When the 3 moves across, what happens to its sign?"*
  2. *(3–40 s)* The rewind: solve a quadratic by hand. It stays silent on correct lines, then you make a sign slip, it flags it, you fix it, and a green tick appears.
  3. *(40–60 s)* Hand the pen to a friend: *"write any algebra with a mistake."* Their slip gets caught, and you capture their reaction.
  4. *(60–80 s)* Numbers card: errors caught, false alarms per page, p95 latency, $/page, number of students.
  5. End on the QR code for the web demo and the repo.
- **In person (interviews):** a napkin, a pen and your phone on a stand. *"Write any algebra with a mistake."*
- **Remote:** a QR code to the web demo that works on any phone in 10 seconds.

## 11. How the agents will work (build + review)

- **One spec per milestone** (`docs/specs/Mx.md`): goal, interfaces, acceptance tests and non-goals. You see a kid-simple summary before anything starts.
- **Builder agents** work in isolated git worktrees, in parallel tracks where independent: `app/` (TypeScript), `server/` + `verifier/` (Python), `ml/` + `evals/` (Python).
- **Reviewer agents** look at every change:
  - correctness against the spec;
  - security, meaning keys, injection and privacy (your gstack `/cso` and `/review` skills fit here);
  - "can the owner explain every line?" readability.
- **An eval agent** runs the gates and writes the numbers into `evals/reports/`.
- **Plan stress-test before M0:** reviewers role-play product (YC partner), engineering (staff engineer), security, and a recruiter (your gstack `/plan-ceo-review` and `/plan-eng-review` fit here). I fold their findings into this file.
- **Your job at each gate:** read my simple summary, ask questions, and approve or redirect. Nothing merges to `main` without passing CI and your OK at gates.
- **House rules:**
  - small PRs, tests required, CI green;
  - no secrets in the repo;
  - every decision logged;
  - AI-written code gets the same review as human code, and you should be able to defend it (Anthropic's interviews are AI-free).

## 12. What I need from you (third-party checklist)

| # | Item | Why | Cost | When |
|---|---|---|---|---|
| 1 | **Fix the NVIDIA GPU**: restart; if Device Manager still shows Code 43, reinstall the driver via the NVIDIA App | Laptop inference and training (fallback: Modal credits) | $0 | M0 |
| 2 | **Gemini API key** from AI Studio, **with billing on** (the free tier may use your data for training, which isn't OK for other people's handwriting) | cloud reader + hint rewording | ~$1–3/mo | M0 |
| 3 | Anthropic API key (optional) | second cloud reader to compare (Haiku 4.5) | ~$0–2/mo | M1 |
| 4 | Hugging Face account + token | download Uni-MuMER and FERMAT | $0 | M0 |
| 5 | **Android Studio** (SDK, platform-tools/adb, JDK 17) + **Developer options → USB debugging** on your phone | build and install the app | $0 (~15 GB disk) | M0 |
| 6 | Expo account (optional) | EAS cloud builds | $0 | M2 |
| 7 | Server hosting: a small always-on Python container (pick in M0 from [05](research/05-feasibility-costs.md); warm during demos) | `/verify`, `/read`, `/hint` | ~$0–5/mo | M2 |
| 8 | **Phone stand** (overhead/gooseneck, 23–30 cm) + dark pens + plain paper | camera geometry | ~$20 one-time (or DIY) | M0 |
| 9 | **4–6 friends** to write 30–40 pages (spike), and later 20–40 writers (golden set), with a consent form | data you can't download | pizza 🍕 | M1 / M5 |
| 10 | Your **phone model** | on-device model size (8 GB vs 12 GB+ RAM) | — | now |
| 11 | UMD IRB check (only before *publishing* results about other students) | research ethics | $0 | M5 |

**Monthly running cost:** about $5–12 (cloud reader ~$0.002/page; hosting $0–5; training on your GPU or Modal's free $30/mo credit).

## 13. Top risks

| Risk | Likelihood × impact | Mitigation | Tripwire |
|---|---|---|---|
| Reader misreads or "fixes" errors on real paper | High × High | error-preserving LoRA, confidence gate, next-line check, glyph confirmation, cloud faithful prompt | M1 gates fail → narrow, tablet ink, or pivot to Spotter |
| False alarms annoy users | Med × High | the interrupt policy (§7); FA/page is the primary metric; calibrated τ | >1 FA per 5 pages after M3 |
| Verifier says UNKNOWN too often, so it stays silent and misses errors | Med × Med | scope discipline; more mal-rules; stay silent rather than guess | UNKNOWN > 20% in-scope |
| Latency on a mid-range phone | Med × Med | specialist first pass; cloud fallback; measure p95 early (M2) | p95 > 5 s |
| Novelty vs Chiron/Goodnotes | Med × Low–Med | claim the combination (paper + Android + on-device + open evals), not "first" | — |
| Setup friction (stand, lighting) | Med × Med | explicit "check" trigger fallback; setup wizard with live framing feedback | pilot drop-off after the first session |
| Academic-integrity backlash | Low × Med | Practice-mode default, hints-only by construction, work receipt | any complaint → review framing |
| Heat/battery | Med × Low | low-res tracking, and inference only on commit | >10%/30 min battery |

## 14. Decision log (append-only)

| Date | Decision | Why | Alternatives |
|---|---|---|---|
| 2026-09-29 | Build **Margin** (GO given); product name stays "Margin" | Highest score (37/45) across wow, use, depth, ML, evals; fills the portfolio gap | Spotter 36, Guardrail 33, Nudge 33 |
| 2026-09-28 | Android-first; Expo dev build + VisionCamera 5 | Your phone; TS strengths; mature camera stack | native Kotlin; PWA (too limited for live vision) |
| 2026-09-28 | Parser = `latex2sympy2_extended` | Spike: 42/42 OCR-style inputs vs 36/42 (Lark); keeps written form; 3× faster | SymPy Lark/ANTLR parsers |
| 2026-09-28 | Verifier as a Python service in v1; Chaquopy later | 16 ms/step; tiny payloads; fastest path | port to a JS CAS (loses tested code) |
| 2026-09-28 | Base model Uni-MuMER-Qwen3.5-2B + MIT specialist | Apache-2.0, GGUF-ready, best open accuracy; avoid NC/AGPL | Gemma 4 E2B (no HME evidence), TAMER/PosFormer (license) |
| 2026-09-28 | Hints-only **by construction** | Bastani: unguarded AI cut exam scores 17% | "trust us" hints |
| 2026-09-28 | Primary guardrail metric = **false alarms per page** | The spike shows misreads, not the math, cause false alarms | accuracy-only metrics |

## 15. Open questions for you

1. **GO on Margin?** Or switch to Spotter, Guardrail or Nudge (`IDEAS.md`).
2. Which **phone model**?
3. OK writing a little **Kotlin** later, for the hand-tracking plugin and on-device SymPy (Chaquopy)? I'd write it with you and walk you through it.
4. Product **name**: "Margin" or something else? (`chuddle` can stay the repo name.)
5. **Public repo from day 1**, or private until launch?
6. Who could be your **4–6 spike writers**?
