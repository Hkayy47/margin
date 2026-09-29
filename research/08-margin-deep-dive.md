# 08 · Margin deep dive: competitors, data, models, verifier, pedagogy, integrity, camera

_Research slice for **Margin**, the phone-over-notebook math coach that verifies every handwritten line and only speaks up when a step is wrong. Compiled **2026-09-28**. Scope: questions 1–8 from the lead agent. No code was written. A separate agent owns the SymPy verifier prototype._

**How to read this**
- **Evidence labels:** **[S]** strong (official page, paper, store listing, primary source); **[M]** medium (credible secondary source, user reports, vendor marketing claims); **[W]** weak (background knowledge or a single unverified mention). Each section keeps **Evidence** separate from **Inference**.
- **Licenses** are recorded separately for code, weights and data wherever they differ. "NC" means non-commercial.
- **Method caveat:** the shared WebSearch budget was already exhausted (200/200) when this slice started. Everything below comes from direct fetches of official pages, app-store listings (Google Play, the Apple iTunes API), vendor help centers, the YC directory (yc-oss mirror), Hacker News (Algolia API), the Wayback Machine, arXiv and Semantic Scholar APIs, the Hugging Face API, PyPI and the `gh` CLI. Items we could not verify are marked **[W]** or "unverified." Nothing was invented to fill a gap.
- Prior slices this builds on: [06-capability-unlocks](06-capability-unlocks.md) (Seed 1), [05-feasibility-costs](05-feasibility-costs.md) (API prices) and [07-android-and-trainable-ml](07-android-and-trainable-ml.md) (on-device runtimes, Unsloth VRAM).

---

## TL;DR

1. **The concept is not unclaimed any more, but the paper-and-camera version is.**
   - **Chiron (YC S25)** ships a live, line-by-line, symbolic-engine-checked, hints-only handwriting tutor on the **iPad with Apple Pencil**.
   - **Goodnotes Math Assist** (iOS) underlines wrong lines live, but hands out answers.
   - **Frizzle (YC S25)** reads paper steps from photos, but only for teachers, after class.
   - We found **no product doing live, CAS-verified coaching on real paper through a phone camera, and nothing on Android.** (§1)
2. **The #1 technical risk is faithful transcription, not math reasoning.**
   - VLMs "fix" students' mistakes (42–66 % of FERMAT transcripts).
   - 87 % of LLM grading errors on handwritten math are transcription.
   - SOTA recognizers drop from about 80 % ExpRate on benchmarks to **24 % zero-shot on real phone photos**, recovering to about 75 % after a LoRA on about 1.1k images. (§3–4)
3. **Model choice:** **Uni-MuMER-Qwen3.5-2B** (Apache-2.0 weights, 84/81/80 % on CROHME 2014/16/19, GGUF+mmproj for llama.rn, LoRA about 5 GB), plus an **MIT specialist (GryphOne/SSAN)** as the fast first pass. Several popular specialist repos (CoMER, TAMER, ICAL) have **no license**, and PosFormer is academic-only. (§3)
4. **Datasets:**
   - **FERMAT (CC BY 4.0)** is the best external error-detection eval.
   - The big recognition sets (MathWriting, CROHME, M2E) are **NC**.
   - **Margin must build its own golden set** (protocol in §2.4). Size it at 250+ injected errors and 300+ clean pages.
5. **Verifier:**
   - Use `latex2sympy2_extended` 1.11 (MIT) with safe flags.
   - Return **EQUIVALENT / NOT_EQUIVALENT / UNKNOWN**; compare **real solution sets** for equations; speak only with a counterexample.
   - Diagnose errors by applying mal-rules to the previous line (Aplusix-style).
   - SymPy 1.14's LaTeX parsers have many open bugs. (§5)
6. **Pedagogy:**
   - Flag at line end, not mid-stroke, and give a short window to self-correct.
   - Use a 4-rung ladder that never shows the corrected line; move up only after new ink.
   - **False alarms per page is the primary guardrail metric.**
   - Guardrails decide whether AI helps or harms (Bastani, PNAS 2025: −17 % unguarded). (§6)
7. **Correction:** the "Dartmouth 0.71–1.30 SD AI tutor" cited in IDEAS.md is an **observational** study of LLM-graded stats quizzes. Don't cite it as RCT evidence. Use Harvard (Kestin 2025) and Bastani instead. (§6)
8. **Integrity:** UMD presumes GenAI is **not allowed on graded work** unless the syllabus says so, but calls practice use "common." **Frame Margin as a practice & exam-prep coach**, hints-only by construction, with no photo-a-problem solving. (§7)
9. **Camera:**
   - OpenCV quad detection plus warp is enough; skip neural dewarping (the popular ones are NC).
   - Detect a finished line with ink diff, MediaPipe hand mask and a dwell timer.
   - **Track at low resolution and recognize from a 12 MP still** (a 1920-px stream gives about 15 px exponents).
   - Overhead mounts hide the screen, so voice is primary. (§8)
10. **Cost ≈ $0.002–0.02 per page**; the budget is not a constraint. (§9.3)

---

## 1. Competitors (2024–2026) and what is still unclaimed

### 1.1 Snap-and-solve / answer-first apps (photo → answer)

| Product (owner) | Input | Feedback | Live? | Platforms | Price and scale (Sep 2026) | Evidence |
|---|---|---|---|---|---|---|
| **Photomath** (Google LLC) | Camera photo of a printed or **handwritten** problem, or a calculator | Full solution plus steps: basic steps free, Plus adds animated tutorials and textbook solutions | Snapshot | Android, iOS | Photomath Plus in-app tiers **$5.99–$9.99**; **100M+** Play installs; 4.8★ from 733k iOS ratings; iOS v8.47.0 (2026-08-31) | [S] [Play](https://play.google.com/store/apps/details?id=com.microblink.photomath), [App Store](https://apps.apple.com/us/app/photomath/id919087726) |
| **Gauth** (listed developer GAUTHTECH PTE. LTD.; reported to be ByteDance's: [Forbes 2024-04](https://www.forbes.com/sites/emilybaker-white/2024/04/03/gauth-bytedance-tiktok-homework-app/), [Wired 2024-08](https://www.wired.com/story/gauth-ai-math-homework-app/) [M]) | Photo, voice | Answers plus animated explanations; "**AI Live Tutor: interactive voice & whiteboard**"; 24/7 human experts | Snapshot plus explainer | Android, iOS, web | Gauth Plus **$11.99/mo, $31.99/quarter, $99.99/yr**; **100M+** Play installs; 4.8★ from 1.5M iOS ratings | [S] [Play](https://play.google.com/store/apps/details?id=com.education.android.h.intelligence), [App Store](https://apps.apple.com/us/app/id1542571008) |
| **Mathway** (Chegg) | Typed or photo | Answers; steps are paywalled | Snapshot | Android, iOS, web | "Steps" **$9.99–19.99/mo, $39.99–79.99/yr**; 50M+ installs | [S] [App Store](https://apps.apple.com/us/app/id467329677) |
| **Symbolab** (Eqsquest / Learneo) | Typed or photo | Step-by-step solver (500+ calculators) plus "AI-powered personalized assessments" | Snapshot | Android, iOS, web | $2.49/wk, $7.99–9.99/mo, $34.99–39.99/yr | [S] [App Store](https://apps.apple.com/us/app/id876942533) |
| **Brainly** | Photo or typed | Steps plus **human tutors**; marketed to parents ("Real human tutors. Smart AI.") | Snapshot plus human | Android, iOS, web | Plus $9.99/mo or $39.99/yr; Tutor $29.99/mo or $95.99/yr; 100M+ installs | [S] [App Store](https://apps.apple.com/us/app/id745089947) |
| **Microsoft Math Solver** | Photo or ink | — | — | **Retired 2025-07-07.** The banner read "Math Solver will be retired on July 7, 2025. Solve math equations with Math Assistant in OneNote." The site now returns 404 and the apps are delisted | — | [S] [Wayback capture 2025-06-26](http://web.archive.org/web/20250626060816/https://mathsolver.microsoft.com/en) |
| **Samsung Notes "Math Solver"** (Galaxy AI) | S Pen handwriting or typed equation | Solves it. Footnote: "Legibility of handwriting can impact accuracy of calculations" | Snapshot | Galaxy tablets and phones (Tab S10 Lite, Aug 2025; Tab A11+, Dec 2025) | Bundled | [S] [Samsung Newsroom, Aug 2025](https://news.samsung.com/us/samsung-galaxy-tab-s10-lite-value-packed-tablet-for-everyday-needs/), [Dec 2025](https://news.samsung.com/us/samsung-welcomes-galaxy-a17-5g-galaxy-tab-a11-galaxy-ecosystem/) |
| Google Lens / Circle to Search homework help | Camera or screen | Step-by-step answers | Snapshot | Android, iOS | Free | [M] background; Circle to Search is referenced in the Samsung footnotes above |

### 1.2 Stylus / digital-ink math (the closest thing to "live step checking")

| Product | Input | What it does with your work | Live? | Platforms | Price | Evidence |
|---|---|---|---|---|---|---|
| **Chiron** (YC Spring 2025, London; App Store "Project Chiron" v0.9.10, 2026-09-24) | **Apple Pencil on iPad** (iPhone also listed); the camera is used only to snap the *problem statement* | "Reads every line as you go and steps in only when it helps: a nudge when you're stuck, a question when you're close, a quiet check when you're not sure." Strokes → LaTeX → "a million symbolic questions" in **Wolfram Language** against the problem's ground truth. "**Real-time feedback on every stroke (<300 ms)**." Catches "the sign you flipped, the solution you gained, the step that doesn't follow." **Hints-only**: "pointed at the slip, not handed the answer." Voice: "Ask out loud… and talk it through." Covers algebra through ODEs | **Live, proactive** | iOS / iPadOS only | Free (no in-app purchases listed); **0 US ratings** | [S] [YC launch page](https://www.ycombinator.com/companies/chiron), [App Store](https://apps.apple.com/us/app/id6502346822), [site](https://projectchiron.org) |
| **Goodnotes Math Assist** (created 2024-09-19, updated 2026-06-19) | Apple Pencil | Recognizes equations (they "glow blue") and writes answers in your handwriting. It can "complete any intermediate step," and it **underlines lines as incorrect**. Its help doc admits that misrecognition "can result in lines of your equation being **improperly underlined as incorrect**." Covers arithmetic through integrals and limits; no inequalities, matrices or ODEs. Institution admins can disable it through MDM | Live | **iOS / iPadOS / macOS only** | Essential $11.99/yr; Pro $35.99/yr; AI Pass $9.99/mo | [S] [How to use Math Assist](https://support.goodnotes.com/hc/en-us/articles/10779567357199-How-to-use-Math-Assist), [recognition FAQ](https://support.goodnotes.com/hc/en-us/articles/10779297639567-Why-isn-t-my-math-being-recognized-by-Math-Assist) |
| Goodnotes **AI Math Assistance** (Nov 2023, "experimental") | Apple Pencil, exam-prep content (SAT, HK DSE, CSAT) | "Works similarly to **spellcheck, but for math**… checking your handwritten math work in real-time." It **runs locally on the device** and offers hints and step-by-step help. Design insight from its user tests: students "chose to leave the mistake on the page… and write the correction on the next line" | Live | iPad | Premium | [S] [Goodnotes design blog](https://www.goodnotes.com/blog/how-its-made-ai-math-assistance) |
| Goodnotes **AI for Math**: Solve + Teach Me (2025-09-29) | Lasso a handwritten problem, or type one | "Solve" gives full steps; "Teach Me" is Socratic. A **confirmation card shows how it read your problem** before computing, and **Wolfram\|Alpha's LLM API** does the math | User-initiated | Goodnotes AI | AI Pass | [S] [blog](https://www.goodnotes.com/blog/math-ai-that-builds-understanding), [help](https://support.goodnotes.com/hc/en-us/articles/13683534670223-Goodnotes-AI-for-Math) |
| **Apple Math Notes** (iPadOS 18, June 2024; 3D graphing added in iPadOS 26) | Apple Pencil or typing | Evaluates an expression when you write "="; supports variables and graphs. It does **no step checking**, and a detailed review notes it "doesn't even cover a lot of useful math (e.g. calculus)" | Live calculator | iPad, iPhone, Mac | Free | [S] [Apple Newsroom](https://www.apple.com/newsroom/2024/06/ipados-18-introduces-powerful-intelligence-features-and-apps-for-apple-pencil/); [M] [review](https://mlajtos.mu/posts/new-kind-of-paper-5) |
| **OneNote Math Assistant** (Microsoft) | Pen or finger ink, or typing; you lasso an equation | Solves it and shows steps, plus graphs. Teachers can watch Class Notebooks live. "Some Math Assistant features, such as generating practice quizzes, might be temporarily unavailable" | User-initiated | Windows, web, iPad | Microsoft 365 | [S] [Microsoft Learn module (2026-04)](https://learn.microsoft.com/en-us/training/modules/independent-learning-math-tools-onenote/) |
| Notability | Stylus | Handwriting recognition and "math conversion" to typed math; no checking | — | Apple, web | Subscription tiers | [S] App Store listing |
| Links (Show HN, Apr 2025) | On-screen "digital blackboard" | Gemini 2.0 Flash reads the child's handwriting and gives hints for K–3 arithmetic | Live | Web | — | [S] [HN](https://news.ycombinator.com/item?id=43759921) (1 pt) |
| Snorkl | Whiteboard plus voice recording | AI feedback on students' recorded explanations; a teacher tool claiming "10,000+ schools" | After recording | Web | — | [M] [site](https://snorkl.app) |
| **AmIWrite** (CHI 2026 research prototype; UC Irvine + Purdue) | Handwriting on a **tablet** plus speech | "LLM-powered AI tutoring system… real-time co-speech handwriting interactions on tablet devices." Within-subjects N = 40, linear algebra, against a text-based tutor. The abstract reports only that it "can preserve the pedagogical benefits of handwriting-based math tutoring" | Live | Tablet | Research | [S] abstract ([doi:10.1145/3772318.3790935](https://doi.org/10.1145/3772318.3790935), [project](https://engineering.purdue.edu/cdesign/wp/amiwrite/)). A possibly related unlicensed repo uses **GPT-4o alone** to find errors and "provide the correct value." That is [W], unconfirmed as the paper's system |

### 1.3 Chat and voice AI tutors (Socratic; typed or photo input)

| Product | What it is | Status and evidence |
|---|---|---|
| **Khanmigo** (Khan Academy) | Typed chat grounded in Khan content; "challenges you… without giving you direct answers." **$4/mo or $44/yr** for learners and families; free for teachers | [S] [pricing](https://www.khanmigo.ai/pricing). **Sal Khan, April 2026: "For a lot of students, it was a non-event… They just didn't use it much."** One teacher said students found it frustrating because it "sometimes made mistakes, but also wouldn't give away the answer" [S] [Chalkbeat 2026-04-09](https://www.chalkbeat.org/2026/04/09/sal-khan-reflects-on-ai-in-schools-and-khanmigo/) |
| **ChatGPT** (OpenAI) | Photo upload plus voice with camera. **Study Mode** launched 2025-07-29 as a Socratic mode. On 2026-03-10 it gained interactive visuals for 70+ math and science concepts: "**Each week, 140 million people use ChatGPT to help them understand math and science concepts**" | [S] [OpenAI Mar 2026](https://openai.com/index/new-ways-to-learn-math-and-science-in-chatgpt/). **Study Mode was reportedly removed in Apr 2026**: [M/W] ["Tell HN: OpenAI silently removed Study Mode," 189 pts](https://news.ycombinator.com/item?id=47739305). This is **contested**: a Sep-2026 HN comment says the web app still has it, and the help center returned 403, so it could not be confirmed. GPT-Live-1 (2026-09-10) is full-duplex voice with **no documented vision input** [M] (see [06](06-capability-unlocks.md)) |
| **Gemini** (Google) | **Guided Learning** (2025-08-06), built on LearnLM: probing questions, step-by-step breakdowns, visuals, quizzes. Gemini Live shares the camera, and "Guided Vision" draws highlights on the camera feed. **Gemini 3.8 Live** (2026-09-15) adds visual grounding, but frames arrive at **1 fps** and audio+video sessions **stop after 2 minutes** unless context compression is on | [S] [Google blog](https://blog.google/outreach-initiatives/education/guided-learning/); [06](06-capability-unlocks.md), [05](05-feasibility-costs.md); the Gemini Play listing (2026-08-31) shows Gemini 3.6 and "share your screen/camera" |
| **Claude learning mode** (Anthropic) | Socratic "Learning" style. It launched in Apr 2025 for Claude for Education and opened to all Claude.ai users on 2025-08-14 | [S] [Anthropic](https://www.anthropic.com/news/introducing-claude-for-education), [Engadget](https://www.engadget.com/ai/anthropic-brings-claudes-learning-mode-to-regular-users-and-devs-170018471.html) |
| **Bloomy** (YC S26; [Launch HN](https://news.ycombinator.com/item?id=48981136) 2026-07-20, 102 pts) | Screen-based K–12 mastery platform. BloomyBot **engages proactively only after 3 mistakes in a row**. Its ladder: ask what the student tried → point at the concept → suggest a strategy → work one step together → heavier scaffolding. It is **disabled during mastery assessments**. Models: Anthropic and OpenAI, with zero-data-retention agreements. ELA costs $39/mo or $279/yr; math launched 2026-07-31 at the same price | [S] Launch HN text. An HN commenter proposed VLMs "'looking over the shoulder' of students as they work… by hand through a camera." The founder replied that districts have asked about paper workbooks, "so this is already on our radar," and that "**The VLM idea is especially interesting… We'll definitely take a closer look at this.**" A parent asked for "an analogue paper version" [S] |
| **Ello** | A real-time voice tutor that teaches **math and reading** to ages 4–9. Engineering lessons: frontier models' 2–3 s time to first token caused 3–4 s of dead air; "a smaller, faster model… was constantly giving the answer away"; the fix was streamed actions, an async planner and safety checks that gate *execution* | [S] [Ello blog 2026-07-07](https://www.ello.com/blog/teaching-a-child-in-1000-ms) (HN 155 pts) |
| Small 2025–26 Show HNs | Marcus (Feb 2026), Hope (Aug 2026, grades 2–10), Calyxa (Jul 2026, a Chrome extension with voice), Socratix (Sep 2026), Thinkercan (an LLM+CAS *solver*, 2024–25) | [S] they exist; each has single-digit HN points |

### 1.4 Paper plus camera

| Product | What it does | Why it is not Margin | Evidence |
|---|---|---|---|
| **Frizzle** (YC S25) | "Students keep working on paper." The teacher photographs a stack (phone, document camera or scanner). Frizzle "reads every step of student work," tags misconceptions and credits multiple valid solution paths in about 8 min per class. FERPA/COPPA compliant; free for individual teachers; claims 2,419 teachers | **Teacher-facing batch grading after the fact**, not live coaching for the student | [S] [site](https://www.frizzle.com), [YC](https://www.ycombinator.com/companies/frizzle) |
| EdLight | Teacher-facing AI analysis of photographed student math work | Batch and teacher-facing | [M] [site](https://www.edlight.com) |
| ToughTongue AI demo ([Show HN 2025-12-30](https://news.ycombinator.com/item?id=46438007)) | "Connected a document camera so the AI tutor watches me solve math on pen & paper, then guides me through mistakes" | A generic voice-agent demo with no symbolic verifier and no evals (1 pt) | [S] it exists |
| Generic live assistants (Gemini Live, ChatGPT voice with camera) | Can be pointed at a notebook | Unverified, not proactive by default, and limited by 1 fps frames and session caps | [M] |
| Chinese K–12 "AI study lamps" and learning tablets with desk-facing cameras | Homework answer-checking for younger grades (background knowledge) | K-12 answer-checking, not algebra step verification | **[W], unverified this session** (no accessible English sources) |

### 1.5 What is still unclaimed

**Evidence**
- Snap-and-solve is saturated, with 100M+ installs each for Photomath, Gauth and Brainly. Microsoft left the standalone solver market in July 2025.
- **Live, line-by-line, CAS-verified, hints-only tutoring of handwritten math already ships on the iPad (Chiron, YC S25).** Goodnotes Math Assist also underlines incorrect lines live, but it hands out answers and runs only on Apple devices.
- **Step-level reading of paper work from photos already ships for teachers (Frizzle)**, as an after-class batch.
- We found **no product doing hands-free, live, CAS-verified coaching on real paper through a phone camera**, and **nothing on Android that does live step verification**. Goodnotes Math Assist and Chiron are iOS-only; Samsung's Math Solver only returns answers.
- Bloomy's founder said paper workbooks are "already on our radar" and called VLM "over-the-shoulder" observation of handwritten work "especially interesting" (July 2026).

**Inference**
- Margin can no longer honestly claim to be "the first verified step-checker." The defensible claim is: **Chiron-grade verification for the paper notebook students already use, on the Android phone they already own, with an on-device recognizer and *published* error-detection evals.** None of the competitors we found publish precision, recall or false-alarm rates.
- The novelty window is moderate. Chiron already uses the camera for problem snaps and could add a paper mode, and Bloomy is looking. For a portfolio, lean on *measured engineering* (evals, calibration, latency) rather than "first-ever" claims. Name Chiron and Goodnotes in the README as prior art.
- Competitor documents confirm Margin's two biggest risks:
  1. **Recognition errors produce false "incorrect" flags.** Goodnotes says so even with clean stylus ink, and camera-captured paper is harder.
  2. **An AI tutor has to be proactive and also correct.** Khanmigo was a "non-event" because students had to go and ask. Chiron: "AI is rubbish at spotting your mistakes… LLMs are… much worse at pulling out an error within the many lines of messy student reasoning."
- UX patterns worth borrowing:
  - Goodnotes' **confirmation card** (show what was read).
  - Chiron's **"quiet check when you're not sure"** and **smallest-hint** stance.
  - Goodnotes' finding that students **cross out a mistake and rewrite it on the next line**, which Margin's line tracker must handle.
  - Bloomy's **hint ladder** and its **lock-out during assessments**.
  - Ello's **streamed actions and async planner** for latency.
- Price anchors if Margin ever charges: $4/mo (Khanmigo) to $12/mo (Gauth). The Mathpix OCR API costs **$0.002 per image** ([pricing](https://mathpix.com/pricing/api)), a useful cloud baseline for line OCR. Check its ToS before using its outputs as training labels.

---

## 2. Datasets and benchmarks

**Key findings**
1. **FERMAT is the best public external eval for Margin's core task.**
   - It has **2,244 *photographed* handwritten solutions** (grades 7–12; 609 problems; 43 writers; varied pens, paper and lighting).
   - Injected perturbations: computational 611, conceptual 609, notational 255, presentation 429, and **340 "superficial" non-errors**, which let us count false alarms.
   - License: **CC BY 4.0** (HF, gated with auto-approval); code MIT. [S] verified on the [HF API](https://huggingface.co/datasets/ai4bharat/FERMAT).
2. **No public set matches Margin's setting.** Every real-student error set is small and mismatched in at least one way: K-12, non-English, NC-licensed, or typed rather than handwritten. **None shows US college algebra or calculus on paper under a phone camera**, so Margin must build its own golden set (§2.4). [S]
3. **The large recognition training sets are almost all non-commercial.**
   - MathWriting and CROHME are **CC BY-NC-SA**; M2E is **CC BY-NC**; HME100K and MLHME-38K have no stated license.
   - The only commercial-friendly paper-photo set is **Aida** (CDLA-Sharing-1.0; synthetic calculus limits).
   - **HF mirrors relabel licenses**: UniMER is tagged Apache-2.0 while containing CROHME. Always trace back to the original source. [S]
4. **Good sources exist for error taxonomies and for injecting realistic errors.**
   - **MalruleLib** (Jan 2026): 101 executable mal-rules over 498 templates, drawn from 67 education-research sources. The paper is CC BY 4.0; **the repo has no license**.
   - **MaE**: 55 algebra misconceptions, MIT.
   - **Eedi Misconceptions Graph v1.0**: 8,117 misconceptions, **CC BY 4.0**, released **2026-09-16** (verified on HF).
   - [S]
5. **Once steps are clean typed text, first-wrong-step detection is largely solved at school level.** On [ProcessBench](https://arxiv.org/abs/2412.06559), o1-mini scores F1 93.2 on GSM8K and 88.9 on MATH. **The bottleneck is faithful transcription, not reasoning** (see §4). [S]

### 2.1 Recognition datasets (handwriting → LaTeX)

| Name (year, link) | Size & contents | License (exact) | Access | Fit for Margin | Ev. |
|---|---|---|---|---|---|
| **MathWriting** (Google; [arXiv 2404.10690](https://arxiv.org/abs/2404.10690), Apr 2024) | 230k human train, 396k synthetic, 16k valid, 8k test inks. Single expressions, online ink (InkML) that can be rasterized. Baselines: PaliGemma-3B CER 5.97 / exact match 69 %; Google Cloud OCR 7.17 / 53 % | **CC BY-NC-SA 4.0** | [mathwriting-2024.tgz](https://storage.googleapis.com/mathwriting_data/mathwriting-2024.tgz) (2.9 GB) | Train (largest, most diverse). Clean digital ink, so apply pen, paper and camera augmentation. Also an eval | S |
| **CROHME 2011–2019** ([TC11](https://tc11.cvc.uab.es/datasets/ICDAR2019-CROHME-TDF_1)) | Train 8,836. Test 986 (2014), 1,147 (2016), 1,199 (2019). Online ink plus rendered images | **CC BY-NC-SA 3.0** | TC11 (364 MB) | Standard ExpRate comparison | S |
| **CROHME 2023** ([Zenodo 8428035](https://zenodo.org/records/8428035)) | 3,905 new equations plus earlier data. Online, **offline (scanned paper)** and bimodal tasks. About 17k human and 147k synthetic inks | **CC BY-NC-SA 3.0** | Zenodo (1.8 GB) | Train and eval; the scanned-paper offline split is closer to our setting | S |
| **HME100K** (TAL; CVPR 2022) | 99,109 **camera photos of paper** (74,502 / 24,607), 245 symbols, "tens of thousands of writers." Some labels contain Chinese characters | **Not stated** (TAL platform terms). Treat as research-only | [ai.100tal.com](https://ai.100tal.com/dataset) | Best real-camera match. Drop samples with Chinese characters | M; license W |
| **M2E** (SCUT, ACM MM 2023) | 99,956 **multi-line** phone photos of exam papers and exercise books, with multi-step derivations | **CC BY-NC 4.0** | [ModelScope](https://www.modelscope.cn/datasets/Wente47/M2E) | Multi-line recognition and line splitting. Closest public analogue to notebook derivations | S |
| **MLHME-38K** (TAL, ICDAR 2023) | 38k user-uploaded photos (9,931 multi-line) | Competition terms only | [ai.100tal.com/icdar](https://ai.100tal.com/icdar) | Supplementary | M; license W |
| **UniMER-1M / UniMER-Test** (Apr 2024) | 1.06M pairs. Handwritten part is CROHME plus HME100K train. Handwritten test split (HWE) is 6,332 | HF tag Apache-2.0, **but** the handwritten parts inherit NC-SA / TAL terms | [HF](https://huggingface.co/datasets/wanderkid/UniMER_Dataset) | Convenient handwritten eval split | S |
| **Aida Calculus** (Pearson, 2020) | 100k *synthetic* photos of handwritten limit expressions on paper. LaTeX plus per-character boxes and masks (13.8 GB) | **CDLA-Sharing-1.0** (commercial OK; share-alike on data) | [Kaggle](https://www.kaggle.com/datasets/aidapearson/ocr-data) | The only commercial-friendly paper-photo set; narrow topic | S |
| linxy/LaTeX_OCR | `synthetic_handwrite` 76k/9.6k/9.6k; `human_handwrite` 1.2k | HF tag Apache-2.0; provenance unclear | [HF](https://huggingface.co/datasets/linxy/LaTeX_OCR) | Cheap pretraining | M |
| **University-HMER-RealClassroom** (2026-07-24) | 1,636 phone-camera crops of university calculus (1,103 / 259 / 274) | **"other"**; the card says an explicit license is still needed | [HF](https://huggingface.co/datasets/tuan3110/University-HMER-RealClassroom) | Closest domain match (see §3). Ask the author before relying on it | S (card) |
| **OmniHandwritingOCR** (CIKM 2026, [2608.18586](https://arxiv.org/abs/2608.18586)) | 77,572 images, multi-line easy / medium / hard. **Labels keep writers' own mistakes** ("fact-based" annotation) | **Not released yet**: the linked repo was missing on 2026-09-28 | — | Adopt its labeling principle; watch for release | S (paper) |

### 2.2 Handwritten error and grading datasets

| Name (year, link) | Size & contents | License | Fit for Margin | Ev. |
|---|---|---|---|---|
| **FERMAT** ([2501.07244](https://arxiv.org/abs/2501.07244), Jan 2025) | 2,244 photographed pages (above). Tasks: error detection, localization, correction. The perturbed text is known, so transcription can also be scored | **CC BY 4.0**; code MIT | **Primary external eval.** Report the CAS-checkable subset separately (inference: roughly 700–900 of the error cases) | S |
| **DrawEduMath** (NAACL 2025) + "Aftermath" ([2603.00925](https://arxiv.org/abs/2603.00925), Mar 2026) | 2,030 real US student images (ASSISTments, grade 2 to high school); 11,661 teacher QA pairs | **CC BY-NC 4.0** | Secondary: faithful perception of erroneous work; drawing-heavy | S |
| **ScratchMath** ([2603.24961](https://arxiv.org/abs/2603.24961), AIED 2026) | 1,720 real Chinese K-9 scratchwork images; 7 error-cause types (procedural, calculation, logical, transcription, comprehension, conceptual, attention) | **CC BY-NC-SA 4.0** | Taxonomy and real-error eval; language and grade mismatch | S |
| **EDU-CIRCUIT-HW** ([2602.00095](https://arxiv.org/abs/2602.00095), ACL Findings 2026) | 1,334 real *university* circuits solutions; 513 with expert verbatim transcriptions | **Apache-2.0** | Best public test of *transcription faithfulness* on college pages | S |
| **ErrorRadar** ([2410.04509](https://arxiv.org/abs/2410.04509)) | 2,500 K-12 problems with real students' incorrect *typed* steps, the error step, and 5 categories | **No license on HF** | Taxonomy; first-wrong-step eval for the text path | S; license W |
| HG-Bench ([2606.25491](https://arxiv.org/abs/2606.25491), Jun 2026) | 500 multi-page K-12 homework samples with step-level boxes | No release found | Design reference for step-grounding evals | M |
| UC Irvine calculus ([2603.00895](https://arxiv.org/abs/2603.00895), Mar 2026) | Thousands of real Calc I/II quiz solutions (about 800 students) with OCR, rubrics and TA grades | Release *planned* (clean and noisy-OCR tracks) | **Watch closely**: the closest domain match | M |
| MathCog, VEHME / AIHub | Korean middle-school responses / Korean grading data | Unknown or restricted | Low fit | M |

### 2.3 Typed step-error sets and misconception sources (for the verifier)

| Name | Size & contents | License | Fit | Ev. |
|---|---|---|---|---|
| PRM800K (OpenAI, 2023) | 800K step labels on about 75K MATH solutions | **MIT** | LLM-critic fallback for steps SymPy can't parse; prose-heavy | S |
| **ProcessBench** (ACL 2025) | 3,400 solutions with the earliest wrong step labeled | **Apache-2.0** (HF) | First-wrong-step logic; use the GSM8K and MATH splits | S |
| PRMBench (ACL 2025) | 6,216 problems, 83,456 step labels, fine-grained error types | Apache-2.0 | Error-type ideas; competition level | S |
| MR-GSM8K / MR-Ben | First error step plus reason | Apache-2.0 / MIT | Word-problem level | S |
| BIG-Bench Mistake | CoT traces with first-mistake index | Apache-2.0 | Low fit | S |
| VisualProcessBench / VisualPRM400K | 2,866 human-labeled / about 400K auto-labeled | MIT / MIT | Low–moderate | S |
| MathDial | 2,861 tutoring dialogues with students' incorrect solutions | **CC BY 4.0** | Eval of hint and tutor moves | S |
| CoMTA (Khan, 2024) | 188 Khanmigo conversations (Algebra 45, Calculus 35…) | **Evaluation-only**, non-commercial | Eval only; training not allowed | S |
| **Eedi Misconceptions Graph v1.0** (2026-09-16) | 8,117 misconceptions × 2,258 constructs | **CC BY 4.0** | Error-type labels and hint text | S |
| **MaE** (Dec 2024) | 55 algebra misconceptions, 220 diagnostic examples | **MIT** | Seed list for error injection | S |
| **MalruleLib** ([2601.03217](https://arxiv.org/abs/2601.03217), Jan 2026) | 101 executable mal-rules (37 algebra) × 498 templates; paired correct and mal-rule traces | Paper CC BY 4.0; **repo has no license** | **Best source for realistic injected errors.** Reimplement from the paper or ask the authors | S |
| open-misconceptions (Sep 2026) | Misconception catalog with "slip vs misconception" discriminators (mostly drafts) | CC BY 4.0 / MIT | Hint tone | S |

**Non-commercial flags.**
- NC-licensed: MathWriting, CROHME, M2E, DrawEduMath, ScratchMath and Hard2Verify. CoMTA is evaluation-only. HME100K and MLHME-38K are unclear.
- Fine for a free portfolio.
- **If Margin ever charges, or ships weights trained on NC/NC-SA data, that becomes a liability.** Whether trained weights are "adapted material" under ShareAlike is legally unsettled (inference).
- Mitigation: document a **"clean" recipe** (Aida + our own consented pages + permissively licensed synthetic data) and a data-lineage model card.

### 2.4 Recommended data plan and golden-set protocol

**Train the line recognizer in stages.**
1. **Synthetic and digital ink:** MathWriting (rendered with pen, paper, blur and perspective augmentation) plus CROHME 2019/2023 plus the LaTeX_OCR synthetic split.
2. **Real photos:** HME100K (filtered), M2E cut into single lines, MLHME-38K, and Aida.
3. **Domain:** consented Margin-stand captures, labeled by a cloud VLM and **checked by a human on every error line**.
- In practice: start from Uni-MuMER-2B (§3), which already absorbed stages 1–2, and add stage 3 plus replay.
- **Add error-injected line pairs** (e.g., the line after "3(x+2)=12" rendered as "3x+2=12") so the model learns to transcribe the *wrong* step verbatim.

**Recognition eval.**
- CROHME 14/16/19 for comparability, and HME100K for photo realism.
- **FERMAT transcriptions with a PINK-style over-correction check.**
- Margin's own golden lines as the primary eval.

**Error-detection eval.**
- FERMAT's algebra, calculus and trig items (about 1,092). Report the CAS-checkable subset separately; use the 340 superficial items plus the correct pages for false alarms.
- **Margin's golden set** (below).
- Verifier unit tests on MalruleLib/MaE-style *typed* step pairs, run before any vision work.
- ProcessBench GSM8K and MATH splits for the LLM-fallback path.

**Golden-set protocol (inference, built from FERMAT's design).**
1. Take about 60–100 problems on UMD MATH 1xx/2xx topics and generate correct solutions with the CAS.
2. Inject **exactly one** error per solution at a known step, using the mal-rule taxonomy in §6.1.
3. Include both *propagated* and *non-propagated* versions, so we can check that only the first wrong line is flagged.
4. Mix the set as about **50 % injected, 25 % fully correct, and 25 % superficial** (equivalent rewrites, skipped trivial steps, renamed variables).
5. Have **20–40 writers copy them by hand, verbatim, under the real stand**. Vary lined, grid and blank paper, pen and pencil, and lighting. **Record video** so pen-up latency can be measured.
6. Label, per line: verbatim LaTeX (errors kept, cross-outs marked), bounding box, first-error index and error type. Double-annotate 10–20 % and report κ.
7. **Split by writer.**

**Size.**
- **About 250+ injected errors** gives recall within roughly ±5 points at 95 % confidence.
- **About 300 or more clean pages** supports a claim of fewer than 0.1 false alarms per page: by the rule of three, zero alarms in 300 pages bounds the rate at 0.01 per page.

**Metrics.**
- Line ExpRate (normalized) and **SymPy-equivalence of the transcription**.
- **Error-preservation rate** (a proposed new metric) and **over-correction rate**.
- Per-type precision and recall; first-error localization.
- **False alarms per page**; pen-up → flag p50/p95; $ per page.
- Tip from the ETH calculus study: **background grids hurt OCR**, so the golden set should stratify by paper type [S].

---

## 3. Open-source handwritten-math recognition (HMER) models

**Key findings**
1. **Start from a model that already exists.** Uni-MuMER (NeurIPS 2025 spotlight) released 2B variants on **2026-04-13**, built on Qwen3.5-2B and Qwen3-VL-2B. They score **83.98 / 81.17 / 80.15 % ExpRate** on CROHME 2014/16/19 and **70.43 % on HME100K**, about 20 points above the best specialist models (around 60–65 %). The weights are **Apache-2.0**, as are the base models, and community GGUF+mmproj quantizations exist, so the model runs in llama.cpp and llama.rn. [S] Verified today on the [HF API](https://huggingface.co/phxember/Uni-MuMER-Qwen3.5-2B) and the [README](https://github.com/BFlameSwift/Uni-MuMER), repo Apache-2.0, 45★.
2. **Benchmark accuracy collapses on real phone photos unless you add in-domain data.** On [University-HMER-RealClassroom](https://huggingface.co/datasets/tuan3110/University-HMER-RealClassroom) (created 2026-07-24; 1,636 phone-camera crops of university calculus; license "other," and the card says it "must be replaced by an explicit license before any public release"), blind test ExpRate was:

   | Model | Before fine-tuning (zero-shot) | After fine-tuning |
   |---|---|---|
   | TAMER | 4.38 % | 71.17 % |
   | Uni-MuMER | 23.72 % | **74.82 %** (LoRA on only **1,103** images) |

   [M] Community project numbers, verified on the card. Uni-MuMER's own ablation agrees: dropping HME100K, its camera-photo dataset, cuts HME100K accuracy (visual-match metric, CDM) from 74.3 to 52.4 [S].
3. **Small specialist models are the fast path.** A fine-tuned TAMER reached **71.2 % at 0.31 s per image**, versus 74.8 % at 2.55 s for the 2B model; hardware was not stated [M]. CoMER has 6.39M parameters and TAMER 8.23M [S].
4. **Several specialist codebases can't legally be reused as-is.**
   - CoMER, TAMER, ICAL, SAN and MFH have **no license file**, which means all rights reserved.
   - **PosFormer is "only free for academic research purposes"** per its README, even though it also names BSD-2.
   - **BTTR, CAN, SSAN and GryphOne are MIT.** GryphOne is an ECCV 2026 poster, released 2026-09-23 [S, gh].
5. **All the strong training data is non-commercial.** CROHME is CC BY-NC-SA 3.0, MathWriting is CC BY-NC-SA 4.0, and HME100K's terms are unverified (TAL's portal). Uni-MuMER-Data is labeled MIT on Hugging Face but repackages those same sets. The original **Uni-MuMER-3B is built on Qwen2.5-VL-3B, which is under the non-commercial Qwen Research license.** All of this is fine for a non-commercial portfolio; see §2 for detail.
6. **Document-reading VLMs and printed-formula OCR fail on handwriting.** On OmniHandwritingOCR (CIKM 2026), character error rate on single-line handwritten formulas was [S] ([arXiv 2608.18586](https://arxiv.org/html/2608.18586v1)):

   | Model | Error rate |
   |---|---|
   | PaddleOCR-VL | 116.8 % |
   | DeepSeek-OCR | 154.8 % |
   | MinerU2.5 | 132.7 % |
   | GOT-OCR2 | 57.3 % |
   | GPT-4o | 79.2 % |
   | Kimi-VL-A3B (best) | 10.9 % |

   pix2tex and texify score 0.012 and 0.341 BLEU on handwritten expressions.
7. **The worst failure mode for Margin: OCR that silently fixes the student's mistake.** The same benchmark reports large VLMs (Qwen2.5-VL-72B, InternVL3-78B) transcribing *corrected* versions of visible writer mistakes [S]. If the reader repairs an error, Margin never flags it. **The eval therefore needs an "error-preservation rate."**
8. **Every strong model reads one expression at a time.** All systems degrade sharply on multi-line handwritten formulas [S]. Margin should segment the page into lines first and recognize each line crop separately.
9. **A 2B LoRA fits the RTX 5070 (8 GB).** Unsloth's documented bf16 LoRA memory: Qwen3.5-0.8B about 3 GB and **2B about 5 GB**; 4B needs 10 GB; Gemma 4 E2B is borderline at 8–10 GB [S] (see [07](07-android-and-trainable-ml.md)). Fix the Code 43 driver fault first.

### 3.1 Model table

- ExpRate is exact match, in %. "n/r" means not reported in the sources checked; "NC" means non-commercial.
- The MathWriting column is error rate / exact match from GryphOne's side-by-side reimplementations [S]. Uni-MuMER's MathWriting figure uses a different LaTeX normalization, so the two aren't comparable.
- "ONNX by hand" means export the encoder plus a one-step decoder and write the beam search in app code.

| Model (year, link) | CROHME 14/16/19 ExpRate | HME100K | MathWriting | Params / size | License code / weights | Export path | Multi-line? | Repo activity | Ev. |
|---|---|---|---|---|---|---|---|---|---|
| **Specialist models** | | | | | | | | | |
| [BTTR](https://github.com/Green-Wood/BTTR) (2021) | 53.96/52.31/52.96 | n/r | 6.85 / 53.4 | ~6.5M; 25 MB GGUF | MIT / trained on CROHME (NC data) | ONNX by hand; GGUF via CrispEmbed | single | 129★, 2024-01 | S |
| [CAN](https://github.com/LBH1024/CAN) (2022) | 57.26/56.15/55.96 (CAN-ABM) | n/r | — | small (DWAP class) | MIT / NC data | GRU decoder, should export easily [W] | single | 387★, 2024-08 | S |
| [CoMER](https://github.com/Green-Wood/CoMER) (2022) | 59.33/59.81/62.97 (aug) | 68.12 | 6.50 / 54.5 | 6.39M; 52 MB | **no license** | ONNX by hand; decoder state carried across steps | single | 136★, 2022-09 | S |
| [ICAL](https://github.com/qingzhenduyu/ICAL) (2024) | 60.63/58.79/60.51 | 69.06 | 6.03 / 57.7 | ~60 MB | **no license** | ONNX by hand | single | 29★, 2024-08 | S |
| [PosFormer](https://github.com/SJTU-DeepVisionLab/PosFormer) (2024) | 62.74/61.03/64.97 (aug) | n/r | 6.30 / 56.2 | ~6.5M; 78 MB | **academic-only** (README) plus BSD-2 | ONNX by hand; GGUF via CrispEmbed | single; also tested on the multi-line M2E set | 85★, 2025-04 | S |
| [TAMER](https://github.com/qingzhenduyu/TAMER) (AAAI 2025) | 61.36/59.54/60.13 | 69.50 | 6.35 / 55.6 | 8.23M | **no license** | ONNX by hand; beam search plus tree scoring | single | 37★, 2025-07 | S; real-photo result M |
| [SSAN](https://github.com/Howrunz/SSAN) (AAAI 2025) | 62.58/62.51/65.30 (aug) | n/r | — | small | **MIT** | GRU decoder, should export easily [W] | single | 16★, 2025-01 | S |
| NAMER (ECCV 2024) | 60.5/60.2/61.7 | n/r | — | — | code not found | parallel (non-autoregressive) decoder | single | — | M |
| [GryphOne](https://github.com/JG1VPP/GryphOne) (ECCV 2026) | 65.2/61.4/61.8; CROHME 2023 61.2 (trained on MathWriting only) | n/r | **5.51 / 59.9** | small ViT + 5-block decoder, 118 MB (~30M, estimated); 73 images/s on a V100 | **MIT** / weights trained on NC MathWriting | fixed step count and 224×224 input should make ONNX easy [W] | single | 2★, released 2026-09-23 | S |
| **Formula-OCR toolkits** | | | | | | | | | |
| [UniMERNet](https://github.com/opendatalab/UniMERNet) tiny/small/base | 67.4/68.4/65.4 (with extra training data) | in its training data | — | 107M/202M/325M | Apache-2.0 / Apache-2.0 | HF or Paddle; community ONNX port of tiny | formula crop | 503★ | S |
| [TexTeller 3](https://github.com/OleehyO/TexTeller) | **contaminated**: the README says training included the CROHME and HME100K *test* sets | — | — | 298M; ONNX int8 88+229 MB | Apache-2.0 | [ONNX exists](https://huggingface.co/onnx-community/TexTeller3-ONNX) | formula; separate page detector | 761★ | S |
| PP-FormulaNet(_plus) S/M/L | no handwritten eval | — | — | 224–698 MB; S takes 254 ms on a Xeon CPU | Apache-2.0 | Paddle Lite / Paddle2ONNX [M] | formula crop | PaddleOCR 90.4k★ | S |
| pix2tex | printed only | — | — | — | MIT | ONNX via RapidLaTeXOCR | formula | 16.6k★ | S |
| texify → [Surya 2](https://github.com/datalab-to/surya) | no handwritten-math eval | — | — | 650M | code Apache-2.0 / weights **modified OpenRAIL-M** (free under a $5M revenue cap) | — | full page | 21.4k★ | S |
| [TrOCR-Math](https://huggingface.co/fhswf/TrOCR_Math_handwritten) | no metrics published | — | trained on part of MathWriting | 609M | AFL-3.0 | GGUF exists | line | — | M |
| Document VLMs: PaddleOCR-VL 0.9B, DeepSeek-OCR 3.3B, MinerU2.5 1.2B, GOT-OCR2 0.58B | error rate 116.8 / 154.8 / 132.7 / 57.3 % on handwritten lines | — | — | — | Apache / MIT / **AGPL-3.0** / Apache | official GGUF for PaddleOCR-VL | full page | — | S |
| **Small VLMs (fit on an 8 GB phone)** | | | | | | | | | |
| [**Uni-MuMER-Qwen3.5-2B**](https://huggingface.co/phxember/Uni-MuMER-Qwen3.5-2B) | **83.98/81.17/80.15**; CROHME 2023 69.43 | **70.43** | 51.84 exact | 2.2B; ~1.27 GB Q4_K_M + ~365 MB mmproj Q8 | **Apache-2.0 / Apache-2.0** (NC training data) | llama.rn (GGUF+mmproj); MNN | single | 45★, 2026-05 | S; real-photo LoRA M |
| [Uni-MuMER-Qwen3-VL-2B](https://huggingface.co/phxember/Uni-MuMER-Qwen3-VL-2B) | 83.27/78.55/79.40; CROHME 2023 **70.96** | 69.31 | 50.66 | 2.1B; ~1.11 GB + ~445 MB | Apache-2.0 | same | single | 3,749 downloads | S |
| Uni-MuMER-Qwen2.5-VL-3B | 82.25/78.29/79.82 | 69.50 | 53.03 | 3.4B | tagged Apache, but **base model is NC** | GGUF exists | single | — | S |
| Qwen2.5-VL 3B / 7B, zero-shot | 38.64/37.75/37.45 and 55.98/50.92/49.62 | 44.42 and 54.57 | — | — | NC / Apache | — | — | — | S |
| Qwen3.5-0.8B, Gemma 4 E2B | **no handwritten-math eval found** | — | — | 0.87B; 5.1B total (2B effective) | Apache / Apache | llama.cpp; Gemma also pre-exported for LiteRT-LM and RN-ExecuTorch | — | — | S |
| SmolVLM2, Florence-2, LFM2.5-VL, Moondream | no handwritten-math eval found | — | — | 0.26–2.2B | Apache / MIT / LFM1.0 / **moondream3 is NC** | — | — | — | S |

Sources:
- The [Uni-MuMER paper, Table 1](https://arxiv.org/html/2505.23566v4) and the [README](https://github.com/BFlameSwift/Uni-MuMER) give the CROHME and HME100K numbers. The README also lists 4B variants (Qwen3.5-4B scores 82.56/78.20/75.98).
- The MathWriting numbers come from [GryphOne](https://arxiv.org/html/2602.03370v2).
- The document-VLM error rates come from [OmniHandwritingOCR](https://arxiv.org/html/2608.18586v1).

**Commercial references**
- **Mathpix:** $0.002 per image, $0.002 per ink-stroke request, $0.005 per PDF page [S] ([pricing](https://mathpix.com/pricing/api)).
- **Google Cloud OCR:** 7.17 % error rate and 53 % exact match on the MathWriting test set [S].
- **Google ML Kit digital ink:** has **no math model** [S].
- **MyScript iink:** digital ink strokes only; pricing not loaded [W].

### 3.2 Phone deployment

| Runtime | Version and date | License | What it can run | Role for Margin |
|---|---|---|---|---|
| **llama.rn** | 0.12.9 (2026-08-04); 0.13.0-rc.6 (2026-09-26) | MIT | GGUF vision models (Qwen3-VL, Qwen3.5, Gemma 4, PaddleOCR-VL); Adreno GPU via OpenCL; experimental Hexagon NPU; Expo plugin | **Main runtime for the 2B model** |
| **onnxruntime-react-native** | 1.24.3 (2026-03-05) | MIT | small specialist models; TexTeller ONNX | **Main runtime for the fast specialist** |
| react-native-executorch | 0.10.4 (2026-09-28) | MIT | pre-exported Gemma 4 E2B vision and LFM2.5-VL-1.6B; exporting a custom fine-tune is manual | Alternative (the Gemma route) |
| LiteRT-LM | — | Apache-2.0 | Gemma 4 vision; community Qwen2-VL-2B, SmolVLM2-500M, FastVLM-0.5B | **No Qwen3-VL or Qwen3.5 vision conversions** as of 2026-09-28 |
| MNN | 3.6.1 (2026-07-23) | Apache-2.0 | Qwen3-VL and Qwen3.5 | Native code only; performance fallback |
| CrispEmbed | 65★ | MIT | C++ ports of PosFormer, BTTR and Uni-MuMER; Android build script | Reference only; immature |

**Evidence**
- Off Grid, an open-source app built on llama.rn, reports vision answers in about 7 s on a flagship and about 15 s on a mid-range phone. Text generation runs at 15–30 tok/s on a flagship CPU and 20–40 tok/s on a Snapdragon 8 Gen 2+ GPU [M].
- Gemma 4 E2B on a Galaxy S26 Ultra decodes at 52 tok/s with 0.3 s to first token [S].
- Specialist models run at 5–8.5 images/s on a desktop GPU even with Python beam search [S].

**Inference [W]**
- Uni-MuMER-2B should take roughly **1–3 s per line on a flagship and 3–8 s on a mid-range phone**, because a line output is only about 20–40 tokens but the image encoder is heavy.
- A native specialist should take about **0.1–0.5 s per line**.
- The validation spike has to measure both on the actual phone.

**Export pain points**
- **Specialists:** the beam search and TAMER's tree scoring must be rewritten in app code. Greedy decoding costs accuracy: one BTTR reimplementation got 49.2 % against 53.96 % reported [M].
- **VLMs:** nobody has measured how 4-bit quantization affects symbol accuracy. Qwen3.5 mixes in a newer attention type that phone GPUs may not accelerate well [W]. Benchmark Qwen3-VL-2B, a standard transformer, alongside it.

### 3.3 Fine-tuning evidence and 8 GB feasibility
- **Uni-MuMER's own training** was a full fine-tune for one epoch on about 1.6M samples from about 392k images, on 8×A100-80GB [S]. You don't need to repeat it: **start from their checkpoint**.
- **How much each step helped** (CROHME average): zero-shot 37.95 → fine-tuned 68.64 → extra tasks 73.29 → extra data 79.74 [S].
- **Community LoRA on real phone photos:** 23.7 % → 74.8 % with 1,103 images [M].
- **On the 8 GB laptop GPU:** a 2B LoRA fits in about 5 GB. A 4B model or a full fine-tune goes to Modal. The 6–30M specialists train fully on 8 GB [W].
- **Getting the fine-tune onto the phone:** merge the LoRA, convert to GGUF with its mmproj, then quantize. The public quantizations of both 2B models suggest this path works [M].

### 3.4 Recommendation (models)
1. **Accuracy model: Uni-MuMER-Qwen3.5-2B plus a LoRA, in llama.rn.**
   - Train the LoRA on three kinds of data:
     - 1–3k *Margin-camera* line crops, labeled by a cloud model and checked by hand.
     - Lines with **injected math errors**, so the model learns to *preserve* mistakes.
     - A replay slice of Uni-MuMER-Data, so it doesn't forget the benchmarks.
   - Compare Q4 and Q8 quantization.
   - Repeat the recipe on the Qwen3-VL-2B variant and keep whichever has better p95 latency on the actual phone.
2. **Fast first-pass model: an MIT-licensed specialist under 30 MB (GryphOne or SSAN) via onnxruntime-react-native.** Fine-tune it on the same crops, export it to int8, and have it emit per-token confidence for routing. Keep TAMER and PosFormer as research baselines only, because of their licenses.
3. **Cascade:** specialist → (low confidence, or SymPy can't parse the line) → 2B model → (still unsure) → cloud (Gemini Flash-Lite or Haiku 4.5), with Mathpix as the commercial baseline.
4. **Avoid:**
   - Document VLMs: they fail on handwriting, and MinerU is AGPL.
   - pix2tex and texify: printed math only.
   - TrOCR-Math: no published metrics.
   - Uni-MuMER-3B: non-commercial base model.
   - Gemma 4 E2B as the OCR model: no handwritten-math evidence and a borderline LoRA memory budget.
5. **The on-device vs cloud chart:**
   - **Systems:** specialist, 0.8B, 2B at Q4 and Q8, cascade, Flash-Lite, Haiku 4.5 and Mathpix, each zero-shot and fine-tuned.
   - **Axes:** per-line latency (p50 and p95) on the phone, against the share of lines whose SymPy parse matches the truth. Bubble size is **$ per 1k lines**.
   - **Also report:** exact match, the visual-match rate (CDM), character error rate, the **error-preservation rate**, how well confidence predicts correctness (ECE), RAM, model size, and battery and heat over 30 minutes.
   - The **benchmark-to-real-photo gap** (about 80 % vs about 24 % zero-shot) is a headline story in itself.

---

## 4. How good are frontier VLMs at handwritten-math OCR and at finding the wrong step?

**Key findings**
1. **The bottleneck is faithful transcription, not reasoning.**
   - UIUC ([arXiv 2605.19043](https://arxiv.org/abs/2605.19043), AIED 2026) graded handwritten university work with GPT-5-mini, GPT-5.1 and Gemini-3-flash. **87 % of the best model's grading errors were transcription failures.**
   - On EDU-CIRCUIT-HW, the share of university solutions with at least one recognition error was: Gemini-3-Preview 37.6 %, Gemini-2.5-Pro 53.5 %, GPT-5.1 71.5 %, Claude-4.5-Sonnet 80.7 % [S; exact metric definition M].
2. **VLMs silently "fix" student mistakes.**
   - The PINK paper ([arXiv 2604.22774](https://arxiv.org/abs/2604.22774), Apr 2026) ran **15 VLMs on FERMAT: 42–66 % of transcriptions contain at least one over-correction.** Stronger models over-correct more, and "be faithful" prompts cut this by only about 4 points. GPT-4o is "heavily penalized for aggressive over-correction" and **Gemini 2.5 Flash is "the most faithful transcriber"** (abstract verified) [S].
   - UC Irvine ([2603.00895](https://arxiv.org/abs/2603.00895)): GPT-4.1-mini silently rewrote a student's "3+2=6" unless told "Do not correct any math…" [S].
   - Aftermath ([2603.00925](https://arxiv.org/abs/2603.00925)): 29–35 % of GPT-5, Gemini 2.5 Pro and Claude Sonnet 4.5 wrong answers about erroneous work matched what a *correct* student would have written [S].
   - OmniHandwritingOCR independently lists "correcting writer mistakes" and "inserting plausible intermediate steps" among four recurring error patterns (verified) [S].
   - **Inference: using a frontier VLM as Margin's reader is structurally risky.** It is the strongest technical justification for a fine-tuned *literal* transcriber plus SymPy.
3. **On exact-match recognition, zero-shot frontier VLMs trail small fine-tuned models.**
   - CROHME average ExpRate: GPT-4o 48.8, Gemini 2.5 Flash 55.3, Qwen2.5-VL-72B 56.4, against **79.7** for Uni-MuMER.
   - HME100K (paper photos): GPT-4o **23.0**, Gemini 2.5 Flash **28.1**, against TAMER 69.5.
   - Much of the gap is LaTeX style: CDM, the visual-match score, is still 83–85 %. A CAS needs the exact expression, though [S].
   - **No 2025–26 paper reports GPT-5.x or Gemini-3.x ExpRate on CROHME, HME100K or MathWriting.** Margin could fill that gap cheaply (inference).
4. **Frontier models are weak at locating steps on a page.** On HG-Bench ([2606.25491](https://arxiv.org/abs/2606.25491), Jun 2026), no zero-shot model (GPT-5.4, Gemini-3.0-Pro-Preview, Claude-Sonnet-4.6, Qwen3.5-397B) exceeds **48 % step-level F1**; a fine-tuned 9B model reaches 72 % [S]. **Do line segmentation in our own CV stage.**
5. **Aggregate grading is decent; faithful line-level reading is not.** GPT-5.5 physics totals correlate r = 0.91–0.97 with official marks (Aug 2026 study; the link wasn't captured) [M]. GPT-5 calculus grading reaches R² = 0.85 against TAs ([2510.05162](https://arxiv.org/abs/2510.05162)) [S]. Margin's line-level, error-seeking, silent-when-right task cannot absorb the transcription noise that aggregate grading tolerates (inference).

### 4.1 Results table

| Benchmark | Model | Metric | Score | Paper date | Source |
|---|---|---|---|---|---|
| CROHME 14/16/19 average, zero-shot | GPT-4o / Gemini 2.5 Flash / Qwen2.5-VL-72B | ExpRate | 48.8 / 55.3 / 56.4 (fine-tuned 3B: 73.3, or 79.7 with extra data) | May 2025 | [2505.23566](https://arxiv.org/abs/2505.23566) |
| HME100K test, zero-shot | GPT-4o / Gemini 2.5 Flash | ExpRate (CDM) | 23.0 (83.1) / 28.1 (85.4); TAMER 69.5 | May 2025 | same |
| MathWriting | Doubao-1.5-pro zero-shot vs Uni-MuMER | ExpRate@CDM | 26.3 vs 69.1 | May 2025 | same |
| OmniHandwritingOCR multi-line, hard (easy) | GPT-4o / Qwen3-VL-8B | CER | 75.6 % / 57.1 % (29.4 % / 25.0 %) | Aug 2026 | [2608.18586](https://arxiv.org/abs/2608.18586) |
| FERMAT multi-line OCR | Gemini 2.5 Flash / GPT-4o / Qwen2.5-VL-72B | PINK | 0.935 / 0.907 / 0.920; 42–66 % over-correction | Apr 2026 | [2604.22774](https://arxiv.org/abs/2604.22774) |
| FERMAT | GPT-4o | Detection / localization / correction | 0.65 / 0.45 / 0.66 (0.71 with an OCR step); Gemini-1.5-Pro correction 0.77 with OCR | Jan 2025 | [2501.07244](https://arxiv.org/abs/2501.07244) |
| FERMAT (VEHME protocol) | Gemini-2.5-Flash-Preview / GPT-4o | Detection / localization accuracy | 80.1 / 63.4 and 66.6 / 55.0 | Oct 2025 | [2510.22798](https://arxiv.org/abs/2510.22798) |
| EDU-CIRCUIT-HW | Gemini-3-Preview / Gemini-2.5-Pro / GPT-5.1 / Claude-4.5-Sonnet | Share of solutions with ≥1 recognition error | 37.6 / 53.5 / 71.5 / 80.7 % | Jan 2026 | [2602.00095](https://arxiv.org/abs/2602.00095) |
| DrawEduMath teacher QA | Gemini 3 Pro Preview / GPT-5 / Claude Opus 4.5 / GPT-5.2 | Accuracy | 0.713 / 0.640 / 0.578 / 0.564 | leaderboard 2025-12-23 | [drawedumath.org](https://drawedumath.org/) |
| ErrorRadar | GPT-4o (best) | Error-step / category accuracy | 55.1 / 53.1 (humans 69.8 / 60.7) | Oct 2024 | [2410.04509](https://arxiv.org/abs/2410.04509) |
| ScratchMath | o4-mini (explanation) / best model (classification) | Score | 71.8 (primary) / ≤49 (humans 89.3 / about 80) | Mar 2026 | [2603.24961](https://arxiv.org/abs/2603.24961) |
| HG-Bench | Best zero-shot (GPT-5.4, Gemini-3.0-Pro-Preview, Claude-Sonnet-4.6) | Answer-region / step F1 | ≤55.2 / ≤48.2 (fine-tuned 9B: 75.0 / 72.3) | Jun 2026 | [2606.25491](https://arxiv.org/abs/2606.25491) |
| UIUC university grading | Gemini-3-flash / GPT-5.1 | Rubric-item accuracy | 89–99 / 87–95; 87 % of errors are transcription | May 2026 | [2605.19043](https://arxiv.org/abs/2605.19043) |
| UC Irvine calculus OCR | GPT-4.1-mini vs Mathpix | Acceptable transcriptions (hard subset) | 84 % vs 55 % | Mar 2026 | [2603.00895](https://arxiv.org/abs/2603.00895) |
| ProcessBench (typed) | o1-mini / GPT-4o | F1 | 87.9 / 61.9 (GSM8K 93.2 / 79.2) | Dec 2024 | [2412.06559](https://arxiv.org/abs/2412.06559) |

### 4.2 Failure modes (evidence [S] unless noted)
1. **Over-correction and expectation bias**: "fixing" the student's error, inserting plausible missing steps.
2. **Symbol confusions**: dropped minus signs ("−V→V"), digit and letter swaps ("20000→2a000"), superscripts, units (EDU-CIRCUIT-HW).
3. **Structural flattening**: nested fractions restructured; accuracy falls as the line count grows.
4. **Hallucinated or omitted steps**, and mishandled equivalent expressions (UIUC; MathCog).
5. **Weak page and step grounding** (HG-Bench). Cross-problem interference on full pages, which UC Irvine avoided by cropping answer regions.
6. **Cautious under-flagging**: big models detect errors conservatively, so cascades lose recall (FERMAT).
7. **Worse on struggling students' work** (Aftermath).
8. **Paper and photo effects**: grid paper hurts OCR (ETH advice); there is a camera-vs-digital-ink domain gap ([2609.32513](https://arxiv.org/abs/2609.32513)).
9. **Error-type classification remains weak** (ErrorRadar, ScratchMath).

### 4.3 OCR-then-reason vs end-to-end (evidence)
- **FERMAT:** an explicit OCR step helps weaker models a lot and strong ones slightly. Accuracy ranks LaTeX text above printed images, and printed images above handwriting [S].
- **EDU-CIRCUIT-HW:** GPT-5.1 grading reaches 89.5 % agreement on expert transcripts, 87.9 % on Gemini-3 transcripts and 77.8 % on its own [S].
- **Inference:** a decoupled pipeline (literal transcriber → SymPy → LLM hint) lets Margin measure each stage separately. Disagreement between the on-device and cloud readers becomes a confidence signal for the interrupt policy. For the cloud fallback, prefer the **most faithful transcriber** (Gemini Flash class, per PINK) with an explicit "do not correct" prompt, and test it for over-correction on the golden set.

---

## 5. LaTeX → SymPy tooling and CAS step verification

**Key findings**
1. **No parser is safe on messy handwriting output out of the box.** [S]
   - SymPy's default ANTLR parser:
     - silently turns `x -` into `x` unless strict mode is on;
     - turns the line `2x=x+x` into `True` instead of an equation ([#22305](https://github.com/sympy/sympy/issues/22305));
     - reads `\pi` and `e` as plain symbols ([#15309](https://github.com/sympy/sympy/issues/15309), [#20306](https://github.com/sympy/sympy/issues/20306));
     - misreads `\cdot` ([#26220](https://github.com/sympy/sympy/issues/26220));
     - fails on `a = b = c` ([#21307](https://github.com/sympy/sympy/issues/21307));
     - crashes on deeply nested parentheses ([#30000](https://github.com/sympy/sympy/issues/30000)).
   - The **Lark** parser (added in SymPy 1.13.0, 2024-07-08) is stricter. A Sep-2026 audit of about 190 inputs ([#30486](https://github.com/sympy/sympy/issues/30486)) found it rejects `\pi`, chained relations, `a+-b`, `\sqrt x` and `(a+b)x^2`, and returns unresolved ambiguities. Fixes sit in open PRs for 1.15.
   - **SymPy 1.14.0 (2025-04-27) is still the latest release** (verified on PyPI).
2. **Use `latex2sympy2_extended` 1.11.0 for v1** (Hugging Face; MIT; 2026-01-10; verified on PyPI).
   - It handles chained relations, `\pm`, `\operatorname`, unevaluated equations, `e` as Euler's number, and degrees.
   - **Turn off these defaults:** `lowercase_symbols=True` (merges A/a), `interpret_as_mixed_fractions=True` (reads `3\frac{x}{2}` as 3½·…), and assignment reading.
   - **Avoid the original `latex2sympy2`** (1.9.1, 2023): parsing `x = 1` *sets x=1 for every later parse* [S].
3. **The checker needs three outcomes: EQUIVALENT / NOT_EQUIVALENT / UNKNOWN.** Speak only on NOT_EQUIVALENT with a **concrete counterexample**. The fork's SymPy 1.14 checks showed why [S]:
   - `.equals()` returns "don't know" on a true half-angle identity.
   - It returns *False* for log(xy)=log x+log y, because SymPy assumes complex numbers by default. In precalc that would be a false alarm.
   - SymPy computes the cube root of −8 as a complex number, not −2.
   - Rule-based answer checkers are over 99 % precise but miss about 14 % of correct answers ([M] Huang et al. 2025). **For Margin, those misses would become false alarms.**
4. **On-device CAS options exist.**
   - **CortexJS Compute Engine** (MIT; 0.140.0 on 2026-09-28; about 984k npm downloads/month) reads LaTeX natively and has a three-outcome `isIdenticallyEqual`. Its API changes frequently and React Native compatibility is unverified.
   - **SymPy via Chaquopy** (MIT; 17.0.0; Python 3.10–3.14) runs on Android; startup and memory costs are unmeasured.
   - **Giac is GPL.**
   - Running SymPy in the cloud is fine for v1 [S / W].

### 5.1 Tooling table

| Tool | License | Latest version & date | Strengths | Failure modes | Verdict |
|---|---|---|---|---|---|
| `sympy.parsing.latex`, ANTLR backend | BSD-3 | SymPy 1.14.0 (2025-04-27) | Default; derivatives, integrals, limits, sums; strict mode | Pins **ANTLR runtime 4.11** exactly ([#27026](https://github.com/sympy/sympy/issues/27026)); bugs listed above; silently repairs broken input | Fallback only (strict mode plus a cleanup pass) |
| Same, Lark backend | MIT (Lark) | Since 1.13.0 | Errors instead of guessing; grammar hooks | `\sin(x) y`→`sin(x*y)`; rejects `\pi`, chains, `\sqrt x`; no `\operatorname` | Re-check after 1.15 |
| [latex2sympy2](https://github.com/OrangeX4/latex2sympy) | MIT | 1.9.1 (2023-04-23) | Broad grammar | Stale; global variable-assignment side effect | **Avoid** |
| [**latex2sympy2_extended**](https://github.com/huggingface/latex2sympy2_extended) | MIT | **1.11.0 (2026-01-10)**; ANTLR 4.9.3 / 4.11 / 4.13.2 | Chained relations, `\pm`, `\operatorname`, unevaluated equations, `e`, degrees | Issue tracker disabled; defaults to override; `f(x)` read as a function call | **Use for v1** |
| [Math-Verify](https://github.com/huggingface/Math-Verify) | Apache-2.0 | 0.9.0 (2026-01-10) | Relation, set and interval comparison; solve-and-compare fallback | Built for final answers (one-directional; `x = 1 → 1`); Unix-only alarm timeouts; thread-safety and hang issues | Borrow ideas and test cases, not `verify()` |
| [CortexJS Compute Engine](https://github.com/cortex-js/compute-engine) | MIT | 0.140.0 (2026-09-28) | Native LaTeX; sampling-based three-outcome identity check | API churn; RN compatibility unverified | Best on-device JS fallback (pin it) |
| mathjs | Apache-2.0 | 15.2.0 (2026-04) | Fast numeric evaluation | No LaTeX; little symbolic math | Numeric spot checks |
| nerdamer-prime / Algebrite | MIT | 1.5.0 (2026-07) / 1.4.0 (2021) | Light | Algebrite stale | Backup / avoid |
| Giac/Xcas | GPL-3.0 [M] | — | Strong CAS | Copyleft | Only if GPL is OK |
| SymPy on Android | Chaquopy MIT / Pyodide MPL-2.0 | Chaquopy 17.0.0 (2025-12); Pyodide 0.29.5 (SymPy 1.13.3) | Pure-Python SymPy works | Startup and memory unmeasured; no signal-based timeouts | Cloud SymPy for v1; Chaquopy later |

No published benchmark of parser success rates on OCR output was found [W]. **Inference:**
- Define a fixed **"Margin LaTeX subset"** as the recognizer's training target.
- Run a regex cleanup, then a strict parse.
- **Any parse failure means UNKNOWN (silent), never "wrong."**

### 5.2 Verification approach (evidence → recipe)

**Why equivalence can't always be settled**
- Deciding whether an expression is zero is undecidable in general (Richardson 1968) [M]. SymPy's `simplify` is heuristic, and `.equals()` can return "don't know" [S].
- WeBWorK compares expressions at random points (default range −2 to 2) [S]. Compute Engine samples first and only then tries a proof [S].
- **A mismatch at a valid point is a definite counterexample.**

**Equations: compare the real solution sets, not the expressions** (fork's SymPy checks [S]):
- If the two lines' (left − right) sides differ only by a constant factor, the steps are equivalent.
- **Squaring adds roots:** √(x+2)=x has {2}, but x+2=x² has {−1, 2}.
- **Dividing by x loses a root:** x²=3x has {0, 3}, but x=3 has {3}.
- **Forgetting to flip an inequality** shows up as the wrong interval.
- Canceling (x²−1)/(x−1) quietly drops the x≠1 restriction.
- `cancel` took 2 ms where `simplify` took 39 ms.
- Equations SymPy can't solve (e.g., sin x = x/2) come back as a condition set, which means **UNKNOWN**.

**Calculus** (inference):
- Check a derivative line against SymPy's derivative of the previous line.
- Check an antiderivative by differentiating it, or accept any constant difference.
- Set assumptions per problem: variables real, and positive where the course allows.

**Recommended tiers** (inference):
1. Cheap normalizing (`expand`, `cancel`).
2. The constant-ratio test or a real solution-set comparison.
3. `simplify` under a hard time limit in a separate process.
4. High-precision numeric sampling at 20–50 points.

- **Flag only if a counterexample exists *and* the handwriting reading is high-confidence.**
- The counterexample doubles as a hint: *"try x = 2 in both lines."*
- **Mal-rule diagnosis:** apply each known buggy rule to the previous line. If the result is equivalent to what the student wrote, name that error type; otherwise report "not equivalent, unclassified." This follows Aplusix / Cognitive Tutor practice.

**LLMs alone are poor at locating student errors.**
- They struggle to find the first wrong step, and **grounding them in a verifier reduces hallucinated feedback** (Daheim et al., [2407.09136](https://arxiv.org/abs/2407.09136)) [S].
- They fail even when given the reference solution (Srivatsa et al., [2509.01395](https://arxiv.org/abs/2509.01395)) [S]. See also the BEA 2025 shared task ([2507.10579](https://arxiv.org/abs/2507.10579)).
- **Converting erroneous student equations into CAS form with LLMs:** no open model was accurate enough (McGinness & Baumgartner 2025) [S]. This is the same over-correction hazard as §4.

### 5.3 Prior art: CAS step-checking in tutors
- **STACK** (Moodle, GPL-3.0) [S]: "reasoning by equivalence" checks *typed* lines, but only polynomials and simple inequalities or linear systems; no logs or trig. Its docs say it has "no concept of 'a step'" ([docs](https://docs.stack-assessment.org/en/Specialist_tools/Equivalence_reasoning/)).
- **Aplusix** [M]: shows whether consecutive *typed* steps are equivalent ([2004](https://doi.org/10.1023/B:IJCO.0000040890.20374.37)). It diagnosed misconceptions by matching correct and buggy rules against steps ([ITS 2006](https://doi.org/10.1007/11774303_43)). This is **the closest precedent for mal-rule diagnosis.**
- **IDEAS** (Utrecht; Haskell; Apache-2.0; updated 2026-09-05) [S license]: strategies plus buggy-rule libraries behind a "diagnose" service ([2014](https://doi.org/10.1016/j.scico.2014.02.021)).
- **Andes** (physics) [M]: immediate red/green marking; equations checked by substituting the known solution; hints go "pointing → teaching → final answer."
- **Cognitive Tutor** [M]: model tracing with correct and buggy rules, immediate feedback, graded hints ending in a bottom-out answer ([Anderson et al. 1995](https://doi.org/10.1207/s15327809jls0402_2)).
- **Zinn's library of differentiation mistakes** ([2006](https://doi.org/10.1007/11774303_35)) [M].
- **Google/Socratic `mathsteps`** (Apache-2.0, archived): its step-type names are useful hint vocabulary.
- **Handwriting in Cognitive Tutors** (Anthony, Yang & Koedinger, [2012](https://doi.org/10.1016/j.ijhcs.2012.04.003)) [M]: use problem context to soften recognition errors. **Inference:** re-rank the recognizer's top few readings by consistency with the previous line, and **flag only if every plausible reading is wrong.**
- **Takeaway:** *typed* line-by-line checking is decades old. **Camera-read paper, checked live with named mistakes, is the new part**, alongside the stylus systems in §1.2.

---

## 6. Tutoring research: error taxonomy, feedback timing, hint ladder, AI-tutor evidence

**Key findings**
1. **Correction to prior slices.** The "Dartmouth AI tutor, 0.71–1.30 SD" cited in [06](06-capability-unlocks.md) and IDEAS.md is **not a math-tutor RCT**.
   - It is Jonah Bard, *Balancing Efficacy and Engagement in Interactive Texts* (iTextbooks'26 workshop; [pdf](https://intextbooks.science.uu.nl/workshop2026/files/itb26_s1s2.pdf)). "Phosphor" is a set of **LLM-graded embedded quizzes** (Claude Sonnet 4.6 grades constructed responses) in **Intro Statistics (MATH 010)**, Spring 2026, N=151 (138 analyzed).
   - Quoted verbatim today: *"This is an observational study of a pilot deployment… and lacks randomized controls. Self-selection is the central threat."*
   - 1.30 SD (unadjusted) and 0.71 SD (midterm-adjusted) are **modeled gaps between full and zero use**. The direct comparisons give d = 0.36–0.66 [S].
   - **PLAN.md should not cite it as tutoring RCT evidence.**
2. **Guardrails decide whether AI tutoring helps or harms.** [S]
   - **Bastani et al.** (PNAS 2025, about 1,000 Turkish high-school students): plain GPT-4 raised practice scores 48 % but **lowered the later unassisted exam 17 %**. The teacher-hint "GPT Tutor" removed the harm but gave no gain. Plain GPT-4 got those practice problems right **only 51 % of the time**.
   - **Harvard** (Kestin et al., Sci. Rep. 2025, N=194, 0.73–1.3 SD) **fed the tutor pre-written step solutions.**
   - Inference: SymPy verification gives Margin that grounding without hand-writing a solution for every problem.
3. **Step-level checking is the mechanism with evidence.** Step-based ITS reach d = 0.76 vs 0.79 for human tutoring (VanLehn 2011) [S]. Keep expectations modest: K-12 math ITS show g = 0.01–0.09 and college g = 0.32–0.37 (Steenbergen-Hu & Cooper 2013/2014) [S].
4. **Timing: flag at the end of a line, never mid-stroke, with a short window to self-correct** [S]:
   - Immediate beats delayed in classrooms (Kulik & Kulik 1988).
   - Delay reduces effects in computer-based learning, and explanatory feedback (g = 0.49) beats right/wrong (0.05) (Van der Kleij 2015).
   - Letting students catch reasonable errors themselves helps (Mathan & Koedinger 2005).
   - Feedback can hurt students who already know the method (Fyfe & Rittle-Johnson 2016).
   - **False alarms damage trust more than misses** (Dixon et al. 2007).
   - Wrong LLM explanations reduced learning (Kumar et al. 2023).
5. **Mal-rule catalogs are long-tailed and unstable.** Payne & Squibb (1990) found error frequencies "severely skewed" and "very unstable" [S]. Plan for **12–15 named mal-rules plus a generic "not equivalent" bucket.**

### 6.1 Proposed v1 Margin error taxonomy
**Detection (inference):** apply the buggy rule to the previous line and check whether the result is equivalent to the student's line.

| ID | Mistake (example) | Source |
|---|---|---|
| A1 | Partial distribution: 3(x+2)→3x+2 | Dawkins "Improper Distribution" [S]; Sleeman [M] |
| A2 | Minus sign over parentheses: −(x−4)→−x−4 | Dawkins [S]; Booth et al. 2014 [M] |
| A3 | Wrong inverse operation: x+5=12→x=12+5; 3x=12→x=12−3 | Sleeman; Payne & Squibb [M] |
| A4 | Over-applied distribution ("additive assumption"): (a+b)²→a²+b²; √(a+b)→√a+√b; log(a+b)→log a+log b | Matz [M]; Dawkins [S] |
| A5 | Illegal cancellation: (x+3)/3→x | Dawkins [S] |
| A6 | Combining unlike terms: 2x+3→5x; x+x²→x³ | Booth [M]; Eedi [S] |
| A7 | Exponent rules: x²·x³→x⁶; x⁻²→−x² | Eedi [S]; Dawkins [M] |
| A8 | Fraction addition: a/b+c/d→(a+c)/(b+d) | MaE [S]; Eedi [S] |
| A9 | Inequality not flipped: −2x<6→x<−3 | MaE [S] |
| A10 | Lost or extra roots: x²=3x→x=3; x²=9→x=3 | Dawkins [S]; STACK docs [S] |
| A11 | Arithmetic slip: 7·8=54 | Payne & Squibb [S] |
| T1 | Trig as multiplication: sin(a+b)→sin a+sin b; sin⁻¹x=1/sin x | Dawkins "Trig Errors" [S] |
| C1 | Chain rule missed: (sin 2x)′→cos 2x | Clark et al. [1997](https://doi.org/10.1016/S0732-3123(97)90012-2); Orton 1983 [M] |
| C2 | Product rule as a product: (fg)′→f′g′ (and ∫fg→∫f·∫g) | Dawkins "Calculus Errors" [S] |
| C3 | Power rule misuse, dropped +C or \|x\|: ∫x⁻¹dx→x⁰/0 | Dawkins [S] |

Sources:
- Classic foundations: BUGGY ([Brown & Burton 1978](https://doi.org/10.1016/S0364-0213(78)80004-4)), mal-rules ([Sleeman 1984](https://doi.org/10.1016/S0364-0213(84)80008-7)), [Payne & Squibb 1990](https://doi.org/10.1207/s15516709cog1403_4), [Booth et al. 2014](https://eric.ed.gov/?id=EJ1059995).
- Most calculus errors trace back to weak basic algebra ([Muzangwa & Chifamba 2012](https://eric.ed.gov/?id=EJ1054301)).
- Current CC BY taxonomy: the Eedi Misconceptions Graph (§2.3).
- A Jun-2026 study found classifiers caught only **57 %** of misconceptions hidden behind correct final answers ([2606.23205](https://arxiv.org/abs/2606.23205)) [S]. This supports checking every line.

### 6.2 Hint ladder (proposed, evidence-grounded)
0. **Silent red box** on the finished line. Start with the least help and allow self-correction (Wood & Wood 1999 [M]; Mathan & Koedinger [S]).
1. **Short spoken question** (≤12 words), e.g., *"Check how the 3 multiplies into the parentheses."* Modelled on Andes and Cognitive Tutor first hints [M]; tutors in the LearnLM UK study praised Socratic questions [S].
2. **The rule behind the diagnosed mal-rule, or a counterexample check** (*"try x = 1 in both lines"*). Explanatory feedback beats right/wrong [S].
3. **A worked example of a *different*, isomorphic problem**, generated by the CAS; **never the corrected line.**
   - Worked solutions help stronger students (Razzaq & Heffernan 2009) [S].
   - Bastani's tutor gave hints, not answers [S].

**Anti-abuse rule:** move up a rung **only after a new attempt**, i.e. visible new ink.
- Students misuse on-demand help (Aleven 2003) [S].
- "Gaming the system" goes with lower learning (Baker 2004/2008) [M].
- Help-seeking feedback improved help-seeking (Roll 2011) [S].

**Timing policy (inference):**
- Show the red box when the line is complete.
- **Speak** only if the student hasn't fixed it within a few seconds, or starts writing the next line.
- Stay silent on UNKNOWN.
- Make **false alarms per page the primary guardrail metric.**

### 6.3 AI-tutor evidence

| Study | Year | N | Setting | Effect | Caveats | Link |
|---|---|---|---|---|---|---|
| Kestin et al. (Harvard) | 2025 | 194 (each student tried both) | Intro physics; GPT-4 tutor with **pre-written step solutions** | **0.73–1.3 SD**; median 49 vs 60 min | Two lessons, one site | [Sci Rep](https://doi.org/10.1038/s41598-025-97652-6) |
| Bastani et al. | 2025 | ~1,000 | Turkish HS math | Practice +48 % / +127 %; exam **−17 %** (plain GPT-4) vs ≈0 (guarded tutor) | Four 90-min sessions | [PNAS](https://doi.org/10.1073/pnas.2422633122) |
| De Simone et al. (World Bank) | 2025 | n/v | Nigeria, 6 weeks, Copilot (English) | +0.31 SD overall | Not math; working paper | [WB](https://doi.org/10.1596/1813-9450-11125) |
| Tutor CoPilot | 2024 | 900 tutors / 1,800 students | AI assisting human K-12 math tutors | +4 pp mastery (+9 pp for weaker tutors) | Not student-facing | [arXiv](https://arxiv.org/abs/2410.03017) |
| LearnLM + Eedi | 2025-12 | 165 | UK math, human-supervised AI | Novel problems solved 66.2 % vs 60.7 % | Exploratory | [arXiv](https://arxiv.org/abs/2512.23633) |
| Bard ("Dartmouth") | 2026-06 | 151 | Intro stats, LLM-graded quizzes | 0.71–1.30 SD *modeled*; d 0.36–0.66 | **Observational**; self-selection | [pdf](https://intextbooks.science.uu.nl/workshop2026/files/itb26_s1s2.pdf) |
| StudentBench | 2026-09 | 2,383 | GRE prep | AI ≈ expert human tutors; "918× cheaper per point" | Preprint | [arXiv](https://arxiv.org/abs/2609.28470) |
| Xiao et al. | 2026-02 | 979 | CS1, prompting instruction | Better prompting; no exam difference | Not math | [arXiv](https://arxiv.org/abs/2602.16033) |
| **Roschelle et al. (ASSISTments)** | 2016 | 2,850 | 7th-grade online homework with **immediate hints, no LLM** | Significant state-test gain, largest for weaker students (≈0.18 SD [M]) | **Closest analogue to Margin** | [ERIC](https://eric.ed.gov/?id=EJ1194398) |

- Experts preferred Google's LearnLM over GPT-4o by 31 %, which is a preference rating, not a learning outcome [S].
- Anthropic's education report found about 47 % of student conversations were answer-seeking ("Direct") [S].
- **No outcome evidence was found for ChatGPT Study Mode or Gemini Guided Learning, and no trial of a paper-watching, step-checking tutor exists** [W]. That makes a small, careful Margin pilot with pre/post practice-set measurement genuinely novel (inference).

---

## 7. Academic integrity: UMD policy, competitor positioning, and Margin's framing

**Key findings**
1. **UMD's default rule restricts graded work and explicitly carves out practice.** Quotes verified verbatim today [S] from the [GenAI Guidelines for Use](https://ai.umd.edu/resources-guidelines/guidelines-for-use), approved and effective 2025-01-15:
   - "Students should assume that the use of GenAI tools to complete course assignments and assessments is **not allowed unless otherwise specified** in the course syllabus or assignment/assessment instructions."
   - "While using GenAI tools **as a learning aid—such as for practicing problems**, exploring concepts, or reviewing definitions—is a common practice, students should confer with their instructors…"
   - "Allegations of unauthorized use of GenAI will be treated similarly to allegations of unauthorized assistance (cheating) or plagiarism and investigated by the Office of Student Conduct."
   - "It will be at the course instructor's discretion to determine whether GenAI may be used, to what extent, and for which assignments and assessments."
   - "UMD strongly recommends that all students utilize UMD-approved tools for study…"
2. **The [Code of Academic Integrity](https://policies.umd.edu/academic-affairs/university-of-maryland-code-of-academic-integrity) has no AI-specific text** (amended 2023-05-25) [S]. It defines Cheating ("using or attempting to use unauthorized materials, information, or study aids…") and **Facilitating Academic Misconduct** ("Knowingly helping or attempting to help another individual to violate any provision of this Code"). A UMD student who *markets* Margin as a graded-homework checker brushes against "facilitating" (inference).
3. **No public UMD MATH 1xx/2xx AI policy was found.** The department pages for MATH 115, 140, 141, 241 and 246 say nothing about AI; section syllabi live in ELMS-Canvas [S, negative result]. The TLTC's [sample syllabus language](https://tltc.umd.edu/sample-syllabus-language-artificial-intelligence-policies) offers six templates, from "Master the fundamentals first without AI tools" to "Effective AI usage is a core skill" [S].
4. **UMD's approved tools** ([ai-resources.umd.edu](https://ai-resources.umd.edu/services.html)) include TerpAI (built with Cloudforce; open to the UMD community), Gemini, NotebookLM, M365 Copilot, ChatGPT Edu and Claude through department plans [S]. None of them checks handwritten steps [M].
5. **The evidence favors hints-only, provided the tool is proactive and correct.**
   - Bastani et al. ([PNAS 2025-06-25, doi:10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122)): students with unguarded GPT-4 access scored **17 % worse** once access was removed, and a guardrailed "GPT Tutor" largely mitigated the harm [S].
   - Khanmigo was a "non-event" for many students and "made mistakes, but also wouldn't give away the answer" [S].
   - Margin's differentiators, speaking up unprompted and CAS-gated interruptions, target exactly those two failure modes (inference).

### 7.1 How comparable tools position themselves

| Tool | Stance / mode | Gives final answers? | Evidence |
|---|---|---|---|
| Khanmigo | "never gives you the answer"; $4/mo | No | [S] [khanmigo.ai/learners](https://www.khanmigo.ai/learners) |
| ChatGPT Study Mode | Opt-in Socratic mode (2025-07-29) | Not inside the mode; one click back gives answers | [S] [launch](https://openai.com/index/chatgpt-study-mode/). Reported removed 2026-04 [M/W]: one Sep-2026 HN comment says the web app still has it, so this is **contested** |
| Gemini Guided Learning | "step-by-step breakdowns"; LearnLM | Guides; makes no no-answer promise | [S] |
| Claude learning mode | "Guiding rather than answering" | No, inside the mode | [S] |
| Chiron | "AI that does less. Just enough to get unstuck." "Pointed at the slip, not handed the answer" | No | [S] |
| Bloomy | Tutor "won't reveal answers" and is "completely absent from Summit assessments" | No | [S] Launch HN |
| Photomath, Gauth ("unlimited answers"), Brainly ("expert-verified answers instantly"), Chegg Study ("solved answers in as little as 30 minutes") | Answer-first | **Yes** | [S] Play listings. Chegg's brand is tied to exam-cheating incidents [M] ([Wikipedia](https://en.wikipedia.org/wiki/Chegg)) |
| Grammarly Authorship (analogous pattern) | Logs the writing *process*; "You decide when to share your Authorship Report" | n/a | [S] [grammarly.com/authorship](https://www.grammarly.com/authorship) |

### 7.2 Privacy (college now, K-12 later)
- **FERPA** covers education records held by schools and their "school officials." A student using a direct-to-consumer app on their own is generally outside it [M].
- **Maryland Education §4-131** (student data privacy) applies to operators *under contract with* PreK-12 schools [S] ([statute](https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=ged&section=4-131)).
- **Amended COPPA** ([FR 2025-04-22](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)): effective 2025-06-23; compliance due 2026-04-22 [S].
  - "A photograph, video, or audio file where such file contains a child's image or voice" is personal information.
  - The audio exception (§312.5(c)(9): use only to answer the request, then delete immediately) was **not extended to images**.
  - The school-authorization amendments were **not finalized**.
  - **K-12 therefore means verifiable parental consent, or a school-contract model.**
- **Tailwind:** the Department of Education's [final AI priority (2026-04-13)](https://www.federalregister.gov/documents/2026/04/13/2026-07087/final-priority-and-definitions-secretarys-supplemental-priority-and-definitions-on-advancing) lists AI "high-impact tutoring" as a fundable use [S].
- **Audio:** Maryland requires all-party consent to record private conversations (Cts. & Jud. Proc. §10-402) [M]. Never store ambient room audio.
- **Cloud fallback:** Gemini's *free tier* uses content to improve Google products ([05](05-feasibility-costs.md)) [S]. Use a paid tier, or a zero-retention provider, for student crops.

### 7.3 Recommended framing and guardrails (evidence → design)
1. **Say "practice & exam-prep coach" everywhere**: store copy, onboarding, README. Don't say "homework checker." *(UMD's default rule plus the learning-aid carve-out [S].)*
2. **Session-type toggle:** *Practice* (default), or *"Assigned work — my instructor allows AI hints."* The second shows a syllabus reminder and a one-tap citation line. *(UMD's "acknowledge and cite" [S].)*
3. **Make hints-only true by construction.**
   - The hint writer sees only the verifier's structured finding (line id, error class, where the two expressions differ), never the problem statement or the correct next line.
   - A CAS **answer-leak filter** rejects any hint that contains the correct expression or value.
   - *(Bastani [S]; Khanmigo [S].)*
4. **Never solve a printed problem statement.** Offer no "scan a problem" entry point, and check only transitions between lines the student wrote. *(All the answer-first leaders carry cheating baggage [S/M].)*
5. **Build a hint ladder with a floor** so students don't stall: nudge → pointed question → name the rule → a worked **isomorphic** example generated by the CAS (see §6). *(Khanmigo frustration [S].)*
6. **Stay silent unless verified.** When the reader is unsure, ask ("is that a 5 or an S?") or give a quiet visual check instead of a voice flag. *(Khanmigo "made mistakes" [S]; Chiron's "quiet check" [S].)*
7. **v1 is live and line-by-line only, with no batch "check my finished worksheet."** This limits its use as a pre-submission checker (inference).
8. **Student-owned "work receipt"** (lines written, flags, hints, times), shared only by the student. *(Grammarly Authorship pattern [S].)*
9. **Later: an instructor mode** with a hint-level cap and "off during exams" codes; Goodnotes already lets institution admins disable Math Assist [S].
10. **Privacy defaults.**
    - Process on-device first. The cloud gets only the cropped line image: no faces, no room, no stored audio.
    - Use push-to-talk or VAD for "wait, why?".
    - Delete crops unless the user opts in to donating them to the eval set, with written consent from classmates.
    - Publishing results that involve other UMD students may need IRB review (inference).

---

## 8. Paper-on-camera practicalities

**Key findings**
1. **Classical OpenCV is enough for v1 page tracking.**
   - Edges or adaptive threshold → `findContours` → `approxPolyDP` finds the page's four corners. `getPerspectiveTransform`/`warpPerspective` then gives a flat, top-down view.
   - Use **DocAligner** as a learned corner fallback: Apache-2.0 code, 1.7–4.9 MB ONNX [S].
   - **Skip neural dewarping.** Hao Feng's DocTr, DocTr++, DocGeoNet and DocScanner are **non-commercial** [S], and a notebook lying flat under an overhead stand barely curls.
2. **ML Kit Document Scanner is a UI flow only**, with no live frames or corner API [S]. It's usable only for "scan finished page."
3. **Pen-up detection has direct prior art.** Microsoft Research's real-time whiteboard capture ([He & Zhang, IEEE TMM 2007](https://doi.org/10.1109/tmm.2006.886385)) "classifies the pixels into whiteboard background, pen strokes and foreground objects… extracts newly written pen strokes" [S].
   - Port it to the rectified page, add a **MediaPipe Hand Landmarker** mask (Apache-2.0; **17 ms CPU / 12 ms GPU on a Pixel 6**) [S], and add a dwell timer.
   - Classifying pen-in-air from top-view video alone is still noisy, with event-level **F2 = 0.805** at best ([arXiv 2606.02342](http://arxiv.org/abs/2606.02342v1), June 2026) [S].
4. **Resolution: track on a low-res stream, recognize from a high-res still.** At about 23 cm, the main camera (82° FOV class, e.g. Pixel 9a) frames US Letter.
   - A 1920-px-wide stream gives **~6 px/mm**, so a 2.5 mm exponent is **~15 px**. That is below ML Kit's guideline of "at least 16x16 pixels" per character [S + inference].
   - A 12 MP still gives ~12.5 px/mm, about **31 px** for the same exponent.
5. **Overhead mounting gives the best pixels but hides the screen.** Voice therefore has to be the primary feedback channel. Angled mounts, or an **Osmo-style mirror**, keep the screen visible at a resolution cost.
6. **The React Native camera stack is mature on VisionCamera 5.** Version 5.2.3 (MIT, 2026-08-20) runs on Nitro Modules and CameraX, with a GPU resizer, AE/AF/AWB locks and an async runner. **react-native-fast-opencv 1.0.1** (MIT) targets VisionCamera 5 [S].

### 8.1 Tools

| Tool | What it does | License (code / weights) | Size / runtime | Phone fit | Activity | Ev. |
|---|---|---|---|---|---|---|
| OpenCV classical (quad detection, perspective warp, `absdiff`) | Page quad detection, rectification, ink diff | Apache-2.0 | ms per frame at ≤960 px | **Excellent** via react-native-fast-opencv | — | S |
| [DocAligner](https://github.com/DocsaidLab/DocAligner) | Heatmap-based document-corner detector | Apache-2.0 / weights auto-downloaded, license **not separately stated** [W] | LC050: 0.4M params, 1.7 MB, SmartDoc15 IoU 0.983. LC100: 4.9 MB, 0.989. FastViT_T8: 13.1 MB, 0.991 ([benchmark](https://docsaid.org/en/docs/docaligner/benchmark)) | Good (onnxruntime-react-native) | 115★; 2026-01 | S |
| docTR (Mindee) | Text detection and recognition. **Not dewarping** | Apache-2.0 (plus OnnxTR) | v1.1.0 (2026-08-21) | At most a line detector; trained on printed text | 6.4k★ | S |
| UVDoc (SIGGRAPH Asia 2023) | Grid-based unwarping of curved pages | MIT / MIT | ~32 MB checkpoint | Possible once per page (untested) | 240★; 2024-07 | S |
| DocTr, DocTr++, DocGeoNet, DocScanner | Unwarping plus illumination | **Custom non-commercial** | GPU transformers | **Avoid** (research baselines only) | 2025–26 | S |
| DewarpNet, PaperEdge | Unwarping baselines | MIT | Heavy | Research only | 2024 | S |
| DocRes (CVPR 2024) | Dewarp, deshadow, appearance, deblur, binarize | MIT / OneDrive weights, license **unstated** [W] | Heavy | Cloud only | 665★ | S |
| page_dewarp (mzucker) | Cubic-sheet optimization for book pages | MIT | Python/SciPy, seconds per page | No | 1.5k★ | S |
| DocShadow-SD7K (ICCV 2023) and its ONNX port | Shadow removal | MIT (repo archived) | High-res ONNX | Probably unnecessary | 209★ | S |
| Glare work | [Fast Glare Detection](http://arxiv.org/abs/1911.05189v1) (2019); [DocHR14K / L2HRNet](http://arxiv.org/abs/2504.14238v1) (2025, 14,902 pairs, uses diffusion); UnReflectAnything (CVPR 2026, MIT; weights pending) | — | Heavy | Detection yes; removal no (inference) | — | S |
| ML Kit Document Scanner | Full scan UI (edges, rotation, cleanup) | Google API (free) | Play-services models | **UI flow only** | Doc updated 2025-09 | S |
| ML Kit subject segmentation | Foreground segmentation | Google API, **beta** | ~200 ms on Pixel 7 Pro; **static images only** | No | 2024 | S |
| **MediaPipe Hand Landmarker** | 21 hand landmarks; LIVE_STREAM mode | Apache-2.0 / Apache-2.0 | **17.1 ms CPU / 12.3 ms GPU on Pixel 6** | Good. Needs a native Kotlin frame-processor plugin; the community RN wrapper (0.6.0, Dec 2024) is stale | 37k★ | S |
| [InkSight](https://github.com/google-research/inksight) (TMLR 2025) | Photo of handwriting → digital ink strokes | Apache-2.0 / Apache-2.0; dataset Apache-2.0 | ~0.67 GB TF SavedModel; TF 2.15–2.17 only | Server-side research only. Could *synthesize online-style data* for training | 1.0k★; 2026-09-19 | S |

### 8.2 Pen-up / "line finished" detection

**Prior art [S]:**
- Wellner, *DigitalDesk* (CACM 1993): an overhead camera reads paper on a desk.
- Munich & Perona ([TPAMI 2002](https://doi.org/10.1109/34.990134)): a camera tracks the pen tip and detects touch.
- Takao, Shi & Baker, *Tele-Graffiti* (IJCV 2003): video-rate paper tracking and "automatic session summarization."
- He & Zhang (2007): real-time extraction of new strokes from a whiteboard.
- Top-view pen-in-air classification (2026): F2 0.805.

**Design options (inference, ranked by v1 value):**
1. **Ink diff plus dwell (default).**
   - Keep a model of the rectified page: background, committed ink, occluder mask.
   - New dark, thin, stable pixels in the active line band become "pending ink."
   - **Commit** the line when there are **no new pixels for about 0.8–1.5 s** *and* the hand or pen has left the band.
   - Tune the dwell against a premature-commit rate. A **partial line** ("3x + 2 =") is the likeliest source of false alarms, so the verifier must return **WAIT** on incomplete or unparseable lines.
2. **Hand mask** from MediaPipe on a small frame at 10–15 fps. Only commit unoccluded pixels, and treat "hand moved to the next line's start" as a strong line-end cue.
3. **Pen-tip detection plus kinematics** as a secondary cue only. Use RF-DETR-class (Apache-2.0) or a small heatmap model, not AGPL YOLO.
4. **Explicit triggers**: tap, saying "check," or drawing a tick. This is also the reliable demo fallback.
5. **Fiducials** on an optional "Margin mat" or clipboard, e.g. ArUco, keep tracking alive when page corners are hidden. ArUco isn't exposed in fast-opencv, so it needs a native call.
6. **Hardware alternative:** Neo smartpen SDKs (GPL-3.0) give true pen-up events and online ink, but break the "any paper" premise.

**Implementation notes (inference):**
- **Lock AE/AWB/AF** after setup. VisionCamera 5 has `lockCurrentExposure`, `lockCurrentFocus` and `lockCurrentWhiteBalance` [S]. Otherwise a hand entering the frame shifts exposure and creates false diffs.
- Re-estimate the homography when the page moves.
- Handle erasures (negative diffs) and **cross-outs**. Goodnotes found students rewrite the corrected line underneath (§1.2).
- Test **left-handed writers** early. They occlude the text they just wrote.

### 8.3 Stand geometry
Pinhole math. Pixel 9a specs as an 8 GB reference phone [S]: main camera 48 MP, 82° FOV; ultrawide 13 MP, 120°; front 13 MP, 96°.

| Mount | Capture | px/mm | 4 mm glyph | 2.5 mm exponent |
|---|---|---|---|---|
| Overhead main, 23 cm | 12 MP still (4000 px) | 12.5 | 50 px | 31 px |
| Overhead main, 23 cm | 2560 px stream | 8.0 | 32 px | 20 px |
| Overhead main, 23 cm | 1920 px stream | 6.0 | 24 px | **15 px** |
| Overhead main, 23 cm | 1280 px stream | 4.0 | 16 px | **10 px** |
| Overhead main, 30 cm | 12 MP still | 9.6 | 38 px | 24 px |
| Angled, lens 30 cm up over the far edge, 12 MP | near / mid / student-side edge | 9.3 / 6.8 / **4.3** | — | — |

- **Target:** at least 16 px per character (ML Kit guideline [S]); aim for **≥24 px** on the smallest glyph (inference). Track at 640–960 px and 10–15 fps. **On commit, recognize from a high-res still** (VisionCamera photo or snapshot) or a ≥2560 px crop.
- **Ultrawide:** it needs only ~11 cm of height but sits in the hand's way, and brings distortion and softer optics. Not recommended.
- **Screen visibility:** overhead hides the screen, so **voice is the primary channel.** For a visible red box, prototype an angled mount and an **[Osmo](https://en.wikipedia.org/wiki/Osmo_(game_system))-style mirror** in front of the front camera [S].
- **Lighting:** lamp to the side, opposite the writing hand. Overhead light behind the phone shadows the page. **Default to a dark pen**, because graphite is shiny and low-contrast (inference).
- **Glare:**
  - Detect saturated low-texture blobs (V ≳ 245) on the rectified page or line crop, then prompt the user to adjust or route to the cloud.
  - Multi-frame fusion doesn't help with a fixed stand and fixed lights.
  - Cross-polarizers are impractical for users [M].

### 8.4 Reference apps and devices
- **Apple Desk View / Continuity Camera:** ultrawide plus perspective correction [M].
- **Osmo:** stand plus mirror [S].
- **Rocketbook:** page fiducials and QR for auto-crop [M].
- **Adobe Scan / Genius Scan:** live quad overlay plus stable-frame auto-capture [M].
- **Microsoft Lens:** **retired**. Leaving stores began 2026-01-09 and new scans ended 2026-03-09 ([MS](https://support.microsoft.com/en-us/topic/retirement-of-microsoft-lens-fc965de7-499d-4d38-aeae-f6e48271652d)) [S].
- None of these *continuously interpret new ink*; that is Margin's gap (inference).

### 8.5 React Native / Android plumbing

| Package | Version (date) | License | Notes |
|---|---|---|---|
| react-native-vision-camera | 5.2.3 (2026-08-20) | MIT | Nitro Modules and CameraX. `useFrameOutput`, `useAsyncRunner` (drops frames when busy), AE/AF/AWB locks, `takeSnapshot`. Expo needs a dev build [S] |
| react-native-vision-camera-worklets / -resizer | 5.2.3 | MIT | GPU resize and RGB conversion (Vulkan on Android) [S] |
| vision-camera-resize-plugin | 3.2.0 (2024-12) | MIT | v4 era, **superseded** [S] |
| react-native-fast-opencv | 1.0.1 (2026-08) | MIT | New architecture, RN ≥0.85, VisionCamera 5 examples. No optical flow, ArUco or CLAHE [S] |
| onnxruntime-react-native | 1.24.3 (2026-03) | MIT | DocAligner, specialist HMER [S] |
| llama.rn | 0.12.9 (2026-08-04) | MIT | The 2B VLM (§3.2) [S] |
| react-native-executorch | 0.10.4 (2026-09-28) | MIT | On-device models [S] |
| ML Kit document-scanner wrappers | 5.0.0 / 2.0.4 | MIT | Scan UI flow only [S] |
| Expo | 57.0.25 (2026-09-24) | MIT | — [S] |

---

## 9. Synthesis for PLAN.md

### 9.1 Go/no-go risks, ranked (likelihood × impact; inference grounded in the evidence above)

| # | Risk | Likelihood / impact | Evidence | Mitigation |
|---|---|---|---|---|
| 1 | **Faithful line reading from a phone camera on real paper** | High / fatal | Zero-shot collapse on real phone crops: Uni-MuMER 23.7 %, TAMER 4.4 % (§3). VLMs "fix" 42–66 % of transcripts (§4). 87 % of grading errors are transcription (§4) | LoRA on 1–3k own crops (community evidence 23.7→74.8 %); error-injected training; recognize from a **high-res still** of each line; dual readers; flag only if **every plausible reading** is wrong |
| 2 | **False alarms destroy trust** | High / high | Goodnotes' help doc: misreads cause lines "improperly underlined as incorrect" even with stylus ink (§1.2). False alarms hurt more than misses (Dixon 2007). Khanmigo "made mistakes" (§1.3) | Budget: **<1 false alarm per 10 pages ≈ <0.5 % per line** at about 20 lines per page. Three-outcome verifier; counterexample required; complete-line check; "quiet check" tier; calibrate thresholds on the golden set and report with CIs |
| 3 | **Verifier coverage and semantics** | Medium / high | Parser bugs; complex-domain defaults (log rule), root gain and loss, conditional solution sets, skipped steps (§5) | Margin LaTeX subset; `latex2sympy2_extended` with safe flags; real solution sets; numeric sampling; UNKNOWN means silence. **Track the UNKNOWN rate**: if many lines are undecidable, Margin stays silent and recall suffers |
| 4 | **Novelty / competition** | Medium / medium (portfolio) | Chiron (YC S25) ships the core idea on iPad; Goodnotes Math Assist ships live underlining on iOS; AmIWrite is a CHI prototype; Bloomy is "looking at" paper (§1) | Differentiate on **paper + Android + on-device reader + published evals**. Name the prior art in the README |
| 5 | **Pen-up / line segmentation and latency** | Medium / medium | Pen-in-air F2 only 0.805; partial lines; left-handed occlusion (§8). 2B reader estimated at 1–3 s/line on a flagship and 3–8 s mid-range [W] (§3) | Ink diff + dwell + hand mask; verifier returns WAIT on incomplete lines; specialist-first cascade; explicit "check" trigger as a fallback |
| 6 | **Adoption / setup friction** | Medium / medium | Khanmigo "non-event"; stand plus lighting requirements | Target exam-prep sessions and UMD study groups; 30-second setup; measure weekly active sessions |
| 7 | **Integrity optics** | Low–medium (with guardrails) | UMD presumes AI isn't allowed on graded work; practice is common (§7) | Practice framing; hints-only by construction; no photo-a-problem solving |
| 8 | **Device thermals and battery** | Medium / low | Continuous camera plus periodic 2B inference | Low-res tracking; recognize only on commit; measure 30-minute sessions |
| 9 | **Licensing** | Low (portfolio) / high (commercial) | NC data; unlicensed specialist repos; PosFormer academic-only (§2–3) | Apache/MIT models only; clean-data recipe documented |
| 10 | **Privacy (K-12 later)** | Low now / high later | Amended COPPA treats images and voice as personal information (§7.2) | On-device first; crop-only upload; no stored audio; defer K-12 |

### 9.2 Validation spike: proposed go/no-go thresholds (inference)
**Setup**
- 30–40 pages from 4–6 writers on v1 topics: about 50 % with one scripted error, 25 % correct, 25 % superficial variants.
- Shot from the real stand. Manual line crops are allowed in the spike.
- Readers: Uni-MuMER-2B zero-shot on the laptop GPU, a Gemini Flash-class model with a "do not correct" prompt, and Mathpix.
- Verifier: the other agent's SymPy prototype.

**GO if all hold**
- The best reader's line **SymPy-equivalence is ≥ 85 %**, zero-shot or after a quick LoRA on about 300 crops, **and error-preservation is ≥ 90 %**.
- End-to-end **recall is ≥ 70 % on injected errors at ≤ 1 false alarm per 5 pages**. This is spike level; the v1 target is ≤ 1 per 10 pages.
- The verifier returns a decision (not UNKNOWN) on **≥ 80 %** of in-scope transitions.
- The cloud path gives a verdict **≤ 3 s** after a line is committed.

**NARROW or PIVOT if**
- False alarms stay above 1 per page at any recall ≥ 50 % even with dual-reader gating.
- Options, in order:
  1. Narrow to single-equation linear or quadratic solving.
  2. Accept digital ink on an **Android S Pen tablet** (easier recognition, but head-to-head with Chiron and Goodnotes on iOS).
  3. Pivot to Spotter (IDEAS.md).

### 9.3 Top recommendations for PLAN.md
1. **Positioning:** "A practice & exam-prep coach that watches your paper and only speaks when a step is provably wrong."
   - Hints-only by construction (§7.3).
   - The README names Chiron and Goodnotes Math Assist as prior art and claims the **paper + Android + on-device + open-evals** combination, not "first."
2. **v1 scope.**
   - **Topics:** linear equations and inequalities; quadratics (factoring, the formula, square roots); polynomial and rational-expression simplification; exponent and log rules; derivatives (power, product, quotient, chain). This is roughly UMD MATH 115/140.
   - **Out of scope:** word problems, graphs, proofs, matrices, and integration beyond basics.
   - **Writing constraints:** one step per line, single column, dark pen, plain or lined paper (not grid).
   - **Setup:** overhead stand at 23–30 cm, side lighting.
   - **Behavior:** silent when right; red box plus a ≤12-word spoken rung-1 hint on a verified error; "why?" moves up the ladder only after new ink.
3. **Pipeline:**
   1. VisionCamera 5 low-res frames at 10–15 fps.
   2. fast-opencv page quad and perspective warp.
   3. Ink diff plus MediaPipe hand mask plus dwell, to decide when a line is committed.
   4. On commit: take a **high-res still** and crop the line.
   5. Read it: **MIT specialist (ONNX)**, then **Uni-MuMER-2B LoRA (llama.rn)**, then a **cloud reader** (faithful prompt, paid tier).
   6. Parse with `latex2sympy2_extended` (strict), then run the **three-outcome SymPy verifier** (cloud for v1; Chaquopy later) and mal-rule diagnosis.
   7. Interrupt policy.
   8. Hint template plus constrained LLM rewording with an **answer-leak filter**.
   9. On-device TTS.
4. **Model to fine-tune:** **Uni-MuMER-Qwen3.5-2B** (Apache-2.0; LoRA about 5 GB on the RTX 5070). A/B it against the Qwen3-VL-2B variant. Pair it with a **GryphOne or SSAN** specialist (MIT). Train on own consented crops, error-injected line pairs and replay data.
5. **Datasets:**
   - Eval: FERMAT (CC BY 4.0) plus the **own golden set** (§2.4) as primary, and CROHME/HME100K for comparability.
   - Verifier unit tests: MalruleLib/MaE/Eedi-derived typed step pairs.
   - Taxonomy and hint text: the Eedi Misconceptions Graph (CC BY 4.0).
   - Watch: the UC Irvine calculus release and OmniHandwritingOCR's release.
   - Ask about University-HMER-RealClassroom's license.
6. **README numbers and CI gates:**
   - Per-type precision and recall; **false alarms per page**; **error-preservation rate**; UNKNOWN rate.
   - Pen-up → flag **p50/p95**; **$/page**.
   - The on-device vs cloud chart (§3.4).
7. **Research extras for ML-leaning roles** (each fills a gap found above):
   - The first published **GPT-5.x / Gemini-3.x ExpRate** on CROHME/HME100K/MathWriting.
   - **Error preservation**: specialist vs 2B VLM vs frontier.
   - A **risk-controlled interrupt policy**, e.g. conformal control of false alarms per page.
8. **Cost (inference):** about 20 lines per page with 20–40 % cloud fallback.

   | Reader | $/line | $/page |
   |---|---|---|
   | Gemini Flash-Lite | ≈ $0.0002–0.0003 | ≈ $0.002 |
   | Haiku 4.5 | ≈ $0.0007 | ≈ $0.004 |
   | Mathpix | $0.002 | ≈ $0.012 |

   Hints add about $0.002–0.004 per page, and TTS is on-device. **Total ≈ $0.002–0.02 per page**, so the $20/month budget covers ≥ 1,000 pages. Image-token counts for Gemini depend on the media-resolution setting [W].
9. **Corrections to carry forward** from IDEAS.md and [06](06-capability-unlocks.md):
   - The "Dartmouth 0.71–1.30 SD" figure is observational statistics quizzes, not a tutor RCT (§6).
   - "No shipped verified watch-your-work tutor" no longer holds on iPad (Chiron) (§1).
   - ChatGPT Study Mode's removal is contested (§1.3).
   - Microsoft Math Solver was retired on 2025-07-07.
10. **Pilot:**
    - UMD study groups doing **practice sets / old exams only**.
    - Informed consent; opt-in crop donation.
    - Measure pre/post on a matched practice quiz, plus weekly return rate.
    - Talk to IRB before publishing anything with learning-outcome claims.
