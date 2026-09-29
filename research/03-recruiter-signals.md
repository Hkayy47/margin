# 03: Recruiter and hiring-manager signals for AI portfolio projects (as of 2026-09-28)

**Scope.** This file covers what makes an AI portfolio project stand out in 2026, which AI projects are now noise, which skills real 2026 postings ask for, how to present a project, and how the signals differ for new grads and FDE roles.
**Target reader.** The lead agent, choosing a project for a CS student going for AI Engineer, FDE, or SWE roles at AI-heavy companies (internship or new-grad level).

**Evidence-strength legend**
- **[S] strong.** Primary source: live job-posting text, a first-party company page, or a data report with a stated method.
- **[M] medium.** Practitioner or newsletter commentary, recruiter-agency guides, or hiring-manager comments on HN.
- **[W] weak.** SEO/career blogs and statistics with no source.
- Anything marked **Inference** is my reading of the evidence, not a claim made by a source.

**Method**
1. **Job postings.**
   - On 2026-09-28 I pulled every live posting from the public ATS APIs of 27 companies: Greenhouse `boards-api.greenhouse.io/v1/boards/<co>/jobs?content=true`, Ashby `api.ashbyhq.com/posting-api/job-board/<co>`, and Amazon `amazon.jobs/en/search.json`.
   - I filtered to FDE/Deployed, AI Engineer/Applied AI/Agent SWE, New-grad/Early-career, and SWE/ML Intern titles, and removed duplicates that differed only by location. This left **202 unique postings from 26 companies**. 89% were first published in 2026.
   - I tagged skills with regexes (§3). I also read about 35 postings in full by hand, including Amazon and Palantir.
2. **Commentary.** I read practitioner and hiring commentary: Pragmatic Engineer, SignalFire, HBR, Hamel Husain, Eugene Yan, swyx/Latent Space, Exponent, KORE1, and others.
3. **Hacker News as the practitioner forum.** I used HN comment threads from 2026 through the Algolia API.

**Limitations**
- **Reddit was blocked** for both fetch and search: the domain is not reachable from this tool, and old.reddit.com redirects to a login page. Reddit sentiment therefore appears only second-hand. X and LinkedIn were not reachable either.
- The shared WebSearch budget ran out part-way. Later evidence came from direct fetches, ATS APIs, and HN Algolia.
- The SEO blogs that turn up for "AI portfolio 2026" quote statistics with no source (for example "70% have a ChatGPT wrapper" and "75% rejected before a human reads"). I flag these as [W] and don't rely on them.

**2026 context worth knowing**
- SpaceX closed its $60B purchase of Cursor/Anysphere on 2026-08-14 and folded it into "SpaceXAI". Cursor's postings now say "SpaceXAI" ([TechCrunch](https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo/), [AI Weekly](https://aiweekly.co/alerts/spacex-closes-60b-cursor-deal-folds-it-into-spacexai-unit)).
- GPT-6 is out. An HN front-page item from Sep 2026 was an "earth exploration site built in 5 prompts" ([HN](https://news.ycombinator.com/item?id=49665756)).

---

## 0. Ranked key findings

1. **The portfolio matters most at exactly this candidate's level.** [S]
   - In the 202-posting sample, **67% of new-grad/early-career postings and 50% of intern postings explicitly ask for evidence of things you built** (side projects, a live app, OSS, hackathons, a "demo we can try"). Only 7–9% of experienced FDE and AI-Engineer postings do.
   - Cursor's new-grad posting makes it **required**: "You've already built something great — an app, OSS, or shipped product we can open and review (required)" ([Cursor NG 2027](https://jobs.ashbyhq.com/cursor/d0e5b41d-84ab-4887-bd3a-55589b11dd7b)).
   - Replit: "Show us something you've built. Replit, GitHub, a live URL, your call" ([Replit NG 2027](https://jobs.ashbyhq.com/replit/b5e81eae-06f9-4798-8988-2d06ca936dbc)).
2. **Real, checkable users are the scarcest and most valued proof.** [S/M]
   - Perplexity wants "shipped side projects with actual users" ([Perplexity early-career](https://jobs.ashbyhq.com/perplexity/daa9120e-94ff-46e0-b4bd-4d2d290cb409)).
   - Vapi spells out the bar. At least one of these should be "easy to verify": "1,000+ active users", revenue from paying customers, or a product "a real company depended on" ([Vapi FDE](https://jobs.ashbyhq.com/vapi/854a9bf5-e330-4afa-9c0f-38c3d6084808)).
   - An HN interviewer with 100+ SWE first rounds rates resumes as "zero signal" and "built something with paying users" as the medium signal. Personal referrals are the highest ([HN, Jun 2026](https://news.ycombinator.com/item?id=48621545)).
3. **Agents are table stakes. Evals separate you from the rest.** [S]
   - Agents, tool use, or MCP appear in **74% of postings and at all 26 companies**.
   - Model and agent evaluation appears in 40% of postings (58% of AI-Engineer roles) and at **19/26 companies**.
   - Cursor, Scale, and Perplexity describe the exact eval stack they want: golden datasets, offline replay, scorers/judges, regression alerts, and tracing ([Cursor Agent Eval](https://jobs.ashbyhq.com/cursor/2bbe9f02-83a5-4173-98be-9085d1cb5693), [Scale](https://job-boards.greenhouse.io/scaleai/jobs/4720573005), [Perplexity](https://jobs.ashbyhq.com/perplexity/5c561bd0-c180-4ee1-b079-647f3c20bdc0)).
   - One reviewer's summary: "If your AI project has no evals, no traces, no metrics, no failure cases, and no deployment story, it probably reads as a demo" ([AI Engineering Insider, May 2026](https://aiengineeringinsider.substack.com/p/the-ai-engineer-job-market-has-moved)) [M].
4. **Visual polish and raw code volume no longer count as signals.** [M]
   - A GPT-6 earth-exploration site built "in 5 prompts" drew the reaction that this would once have been "portfolio-worthy… today it's 'pretty cool', said with a shrug" ([HN](https://news.ycombinator.com/item?id=49666385)).
   - "The visual bar is no longer a signal" ([Pickuma, Jun 2026](https://pickuma.com/for-junior/side-projects-that-impress-hiring-managers-2026/)) [W/M].
   - Hiring managers ask for hosted apps rather than vibe-coded repos ([HN](https://news.ycombinator.com/item?id=47054682)).
   - Show HN volume is up about 4× since 2023, and 37% of posts stall at 1 point ([analysis](https://www.arthurcnops.blog/death-of-show-hn/)).
5. **Production-ops artifacts show depth.** [S]
   - The artifacts: tracing and replay, latency and cost budgets, guardrails and permissions. Observability appears in 26% of postings, latency/cost in 31%, and guardrails/safety in 20%.
   - Perplexity: "Define offline and online evaluations for task completion, correctness, safety, latency, cost, and user satisfaction… Develop tracing, replay, and monitoring infrastructure."
6. **Taste plus AI-coding fluency with judgment.** [S]
   - "Product taste", "great taste", and "craftsmanship" recur at Perplexity, Cursor, Sierra, Replit, and Cognition (34% of postings mention product sense, taste, or UX).
   - 39% of new-grad postings expect daily AI-coding-agent use, for example: "use agents and coding models aggressively… sound judgment about when their output is wrong" (Perplexity).
   - Anthropic's live interviews are "all you—no AI assistance" ([Anthropic](https://www.anthropic.com/candidate-ai-guidance)), so you must be able to defend every line.
7. **FDE is mostly an experienced-hire title, but new-grad paths into FDE-style work exist.** [S]
   - 60% of FDE/Deployed postings in the sample require **5+ years**, and Databricks' AI FDE is "not intended for internship, new graduate, or entry-level applicants."
   - New grads get in through ElevenLabs FDE, Bland, LangChain Deployed Engineer (Early Career, 1–3 yrs), Palantir FDSE New Grad, Sierra APX / SWE-Agent New Grad, and Decagon new-grad Agent Engineering.
   - FDE postings list the artifacts they expect you to produce: eval plans, runbooks, architecture diagrams, demos, and MCP servers. A portfolio packaged the same way signals FDE readiness (**Inference**, grounded in [Ramp](https://jobs.ashbyhq.com/ramp/b614563f-3ce6-4dca-b5ba-0e5a6c8bda27) and [Anthropic](https://job-boards.greenhouse.io/anthropic/jobs/5391021008)).
8. **Market context raises the bar.** [S]
   - New-grad hiring is down about 65% at big tech and about 76% at early-stage startups versus 2019, while FDE roles are up about 30% ([SignalFire, Jun 2026](https://www.signalfire.com/blog/signalfire-state-of-talent-report-2026)).
   - SignalFire's advice to candidates: "Build a verifiable portfolio of shipped applications, active open-source contributions, custom agent workflows, and documented customer discovery."

---

## 1. Hire-me checklist (ranked)

Ranking criteria:
- (a) How explicitly new-grad and intern postings ask for it.
- (b) How scarce it is among candidates, which makes it a differentiator.
- (c) How strong the evidence is.

| # | Signal | What "good" looks like, concretely | Evidence | Strength |
|---|---|---|---|---|
| 1 | **Shipped, live, openable in one tap** | Public URL or installable app; no-login demo mode; works on a phone | Cursor NG: "we can open and review (required)"; Replit NG: "a live URL"; Perplexity: "a demo we can try"; HN: "just ask for a link to a hosted application" ([Cursor](https://jobs.ashbyhq.com/cursor/d0e5b41d-84ab-4887-bd3a-55589b11dd7b), [Replit](https://jobs.ashbyhq.com/replit/b5e81eae-06f9-4798-8988-2d06ca936dbc), [HN](https://news.ycombinator.com/item?id=47054682)) | S |
| 2 | **Real users you can verify** | Named cohort (e.g., 20–100 weekly actives), retention chart, testimonials, or a partner org that depends on it | Vapi's "easy to verify" bar; Perplexity: "shipped side projects with actual users"; HN interviewer ranks "built something with paying users" above resumes; "If you have a personal project that gets users, that is definitely something worth talking about" ([Vapi](https://jobs.ashbyhq.com/vapi/854a9bf5-e330-4afa-9c0f-38c3d6084808), [HN](https://news.ycombinator.com/item?id=48621545), [HN](https://news.ycombinator.com/item?id=46623164)) | S/M |
| 3 | **Agentic depth beyond a single API call** | Tool calling / MCP, multi-step plans, state and memory, retries, error recovery, human-in-the-loop for risky actions | 74% of postings. LangChain early-career: "beyond simple API calls, including multi-step workflows, orchestration, and failure handling" ([LangChain](https://jobs.ashbyhq.com/langchain/0f35c8e1-9318-411d-929b-04c60e6d8522)). Anthropic FDEs "Deliver… MCP servers, sub-agents, and agent skills" | S |
| 4 | **Evals and error analysis with published numbers** | Golden set (hundreds of cases), CI regression gate, LLM-judge checked against human labels, failure taxonomy, before/after table | Cursor: "curated datasets, offline replay, scorers / judges, regression alerts, and dashboards"; Scale: "golden datasets, regression suites, LLM-as-a-Judge, and human evaluation… ablation studies"; Notion early-career AI: "build or extend an evaluation set, run experiments"; KORE1 anecdote: one JD line requiring an eval harness on "at least a 500-question reference set" changed the candidate slate ([KORE1](https://www.kore1.com/how-to-hire-ai-engineer-2026/)) [M]; Hamel: "Error analysis is the single most valuable activity in AI development" ([Hamel, 2025](https://hamel.dev/blog/posts/field-guide/)) | S |
| 5 | **Production-ops signals** | Traces and replay viewer, p50/p95 latency and $/task shown in the app or README, guardrails and permissions for actions, rollback | Perplexity Applied AI ("tracing, replay, and monitoring"; "permissions and safeguards for sensitive actions"); Notion ("add monitoring + guardrails, or improve latency/cost/reliability"); Decagon voice ("timing, responsiveness… observability standards for live voice") | S |
| 6 | **Product taste and UX craft** | The first 10 seconds feel magical, the UI is opinionated, the rough edges of AI are handled (streaming, interruption, undo, confidence) | Perplexity: "Product taste. You can tell a good interface from a bad one"; Cursor: "great taste"; Sierra values "Craftsmanship… We have good taste" ([Sierra APX](https://jobs.ashbyhq.com/sierra/d9c445da-c7b4-43a3-8d71-d367681c3015)); 34% of postings | S |
| 7 | **A decision and trade-off write-up (plus architecture diagram and eval report)** | One-page design doc or ADR log, architecture diagram, eval report, "what I'd do next" | Anthropic Applied AI deliverables: "evaluation suites, AI engineering techniques, and architecture diagrams" ([Anthropic](https://job-boards.greenhouse.io/anthropic/jobs/5432575008)); Ramp FDE artifact list; "A 200-line decisions document is often more valuable than 2,000 lines of well-commented code" ([TryCrucible](https://trycrucible.io/blog/how-to-get-hired-as-ai-engineer-2026)) [W/M] | S/M |
| 8 | **AI-coding fluency with judgment, and you can defend every line** | README states how agents were used and what you verified; tests and CI; you can whiteboard any module | Perplexity, Cursor, Decagon ("Experience using AI coding agents"), Notion ("Cursor, Claude Code"); SignalFire: "audit automated code outputs"; Anthropic live interviews are AI-free; HBR: AI broke remote-interview signals, so in-person checks are back ([HBR, Jun 2026](https://hbr.org/2026/06/ai-has-broken-hiring-heres-how-to-fix-it)) | S/M |
| 9 | **Evidence of customer or user discovery (the FDE signal)** | Interview notes with 5–10 target users, problem statement, a "what users asked for → what I shipped" log | SignalFire: "documented customer discovery"; ElevenLabs FDE: "It's ok if you only worked with customers in student clubs or side projects" ([ElevenLabs](https://jobs.ashbyhq.com/elevenlabs/6c4c57c1-ec72-42ba-af3a-eb7aebbde2e6)); Exponent: the strongest early-career FDE predictor is "having shipped a real product end-to-end and talked to its users directly" ([Exponent](https://www.tryexponent.com/blog/forward-deployed-engineer-interview-the-definitive-2026-guide-fde)) [M] | S/M |
| 10 | **Public track record** (blog post, short video, talk) | A technical write-up of the eval and architecture; a 60–90s phone-screen video | Perplexity: "A public track record we can read, such as GitHub, a technical blog, or a demo we can try"; OpenAI Applied AI (Codex) role centres on "live demos, workshops, hackathons" ([OpenAI](https://jobs.ashbyhq.com/openai/d801f26e-951e-452c-9924-9449b55edc5a)); LangChain DE: "Build and run tailored demos" | S (as ask) / M (video format) |
| 11 | **Domain alignment with target employers** | Voice or multimodal agents (Sierra, Decagon, Bland, Vapi, ElevenLabs, Sesame); agent-quality tooling (Cursor, Glean, LangChain); agents on mobile surfaces (OpenAI, Perplexity, Sierra) | Voice appears in only 11% of postings overall, but at 7 companies, all of them voice-agent players. Sierra example project: "embedded voice mode in mobile apps… talk, tap and text with our agents" ([Sierra](https://jobs.ashbyhq.com/sierra/d2dc9baf-30d4-4708-9227-62a946b4b37e)) | S (postings) / Inference (priority) |
| 12 | *(lowest)* GitHub stars, followers, contribution graph | Nice if organic; never the headline | No posting in the sample asks for stars. The "87% of recruiters check GitHub"-type statistics come from unsourced blogs | W |

---

## 2. Avoid list (overdone, or read as red flags in 2026)

| Pattern | Why it is noise or a red flag | Evidence | Strength |
|---|---|---|---|
| **Thin LLM wrapper** (chat UI on top of an API) | "The candidate has called the OpenAI SDK from a Next.js app. That is not the same as owning a production AI system with evals, monitoring, and rollback" | [KORE1](https://www.kore1.com/how-to-hire-ai-engineer-2026/); HN: "any new grad can whip up an impressive sounding project using ai with zero paying users" ([HN](https://news.ycombinator.com/item?id=48520474)) | M |
| **Chat-with-PDF / basic RAG Q&A with no evals** | Basic RAG is expected, not a differentiator. Reviewers look for hybrid retrieval, citation grounding, and measured recall/faithfulness. "RAG isn't just `similarity_search()`" | [dev.to, Mar 2026](https://dev.to/klement_gunndu/5-ai-portfolio-projects-that-actually-get-you-hired-in-2026-5bpl); [AI Eng Insider](https://aiengineeringinsider.substack.com/p/the-ai-engineer-job-market-has-moved). *Counterpoint:* some SEO guides still call a RAG chatbot "the single most valuable project" ([dglearning](https://dglearning.substack.com/p/6-side-projects-that-actually-get)); treat that advice as dated | M |
| **"Chat with my resume" / portfolio chatbot** | Heavily saturated (many public repos and tutorials), and it solves no user problem | Examples: [dev.to](https://dev.to/okasputra/stop-sending-static-resumes-how-i-built-a-chat-with-my-resume-bot-nextjs-rag-4kdm), [GitHub](https://github.com/seanbearden/resume-chatbot); saturation is **Inference** | W |
| **Generic chatbot, sentiment analyzer, "fine-tuned a model on HF"; MNIST/Titanic/Iris/Kaggle clones** | "Your AI portfolio has a chatbot, a sentiment analyzer, and a fine-tuned model on Hugging Face. So does every other candidate's." "These datasets signal that you followed a tutorial" | [dev.to](https://dev.to/klement_gunndu/5-ai-portfolio-projects-that-actually-get-you-hired-in-2026-5bpl), [Upskillist](https://www.upskillist.com/blog/10-ai-portfolio-examples-impress-recruiters/) | W/M |
| **Tutorial clones** (to-do, weather dashboard, e-commerce) | Reviewers "have seen the exact same project forty times" | [Pickuma](https://pickuma.com/for-junior/side-projects-that-impress-hiring-managers-2026/) | W |
| **Visual-only "wow"** (globes, 3D maps, generative scenes) with no hard engineering underneath | Now reproducible in a few prompts: "It looks cool but I just can't be that bothered to engage with something that contains so little of a human's input" | [HN GPT-6 earth site](https://news.ycombinator.com/item?id=49666381) | M |
| **Vibe-coded repos the author hasn't read and can't defend** | "I just have no interest in seeing code that hasn't even been read by the author"; interviews are moving to formats where AI can't help ("can you talk through trade-offs"); Anthropic live rounds are AI-free | [HN](https://news.ycombinator.com/item?id=47054682), [HN](https://news.ycombinator.com/item?id=48663942), [Anthropic](https://www.anthropic.com/candidate-ai-guidance) | M/S |
| **Agent demos with no evals, traces, or failure cases** (including "multi-agent CrewAI/LangGraph demo") | "Reads as a demo" | [AI Eng Insider](https://aiengineeringinsider.substack.com/p/the-ai-engineer-job-market-has-moved) | M |
| **Vanity or gamed metrics** (a benchmark you designed, speed claims that fail on common inputs) | An HN example: a "fast" PDF parser that failed on common PDFs and gamed its speed metric. Scale: "Measure success through business outcomes, not benchmark scores"; Hamel warns about "vanity metrics" | [HN](https://news.ycombinator.com/item?id=47054682), [Scale](https://job-boards.greenhouse.io/scaleai/jobs/4720573005), [Hamel](https://hamel.dev/blog/posts/field-guide/) | M/S |
| **AI trading bots and "autonomous agent that makes money"** demos | Commonly dismissed as "vibe-coded slop"; hard to evaluate honestly | [HN](https://news.ycombinator.com/item?id=49247087); pattern is **Inference** | W |
| **Tool-list resumes and AI-tuned resume "slop"** | "zero signal: resume & cover letter… New grads are the biggest offenders of the resume slop"; "Hire for ownership, not tools" | [HN](https://news.ycombinator.com/item?id=48624358), [KORE1](https://www.kore1.com/how-to-hire-ai-engineer-2026/) | M |
| **"Launch on Show HN and hope"** as the whole distribution plan | About 4× volume since Feb 2023; 37.2% of Show HN posts stuck at 1 point; about 3.1 comments per post; "don't expect to get hired by OpenAI or Meta" from vibe-coded Show HN projects | [Show HN analysis](https://www.arthurcnops.blog/death-of-show-hn/), [HN](https://news.ycombinator.com/item?id=47326731) | M |

**Inference, specific to this developer.** The existing Cesium globe is exactly the category that a "5-prompt GPT-6 earth site" now makes cheap, even though it has real SSE/data engineering underneath. The new project's wow should come from **AI behaviour plus real usage**, not rendering. That supports the lead's no-more-visualizations rule.

---

## 3. Skills in demand: tally of real 2026 postings

### 3.1 Sample
- **202 unique postings from 26 companies**, all live on 2026-09-28; 89% first published in 2026.
- Companies: Anthropic, OpenAI, Perplexity, Cursor (SpaceXAI), Decagon, Sierra, Bland, Vapi, ElevenLabs, Scale AI, Glean, Harvey, Replit, Cognition, Cohere, LangChain, Notion, Ramp, Stripe, Databricks, Figma, Together AI, Modal, Baseten, Writer, Sesame.
- Role buckets: FDE/Deployed (68), AI Eng/Applied AI/Agent SWE (88), New-grad/Early-career (18), Intern (28). Manager, architect, research, and sales titles were excluded.
- Skew: OpenAI (31) and Databricks (28) are over-represented, so the company-coverage column is the fairer view. Amazon (3) and Palantir (1) were read by hand and are not in the regex counts.
- Regex keyword tagging over the full posting text is approximate. The "customer-facing" bucket includes generic "stakeholders", and the "evals" bucket includes "simulations" and "graders".

### 3.2 Aggregate tally (share of postings mentioning each skill)

| Skill | All (n=202) | FDE/Deployed (68) | AI Eng / Applied AI (88) | New grad / early (18) | Intern (28) | Companies (of 26) |
|---|---|---|---|---|---|---|
| Agents / agentic / tool use / MCP | **74%** | 74% | **89%** | 78% | 29% | **26** |
| Evals (model/agent evaluation, judges, simulations) | **40%** | 32% | **58%** | 28% | 11% | **19** |
| RAG / retrieval / search quality | 30% | 38% | 27% | 28% | 18% | 16 |
| Fine-tuning / post-training | 17% | 18% | 16% | 11% | 21% | 9 |
| RL / RL environments | 8% | 3% | 8% | 11% | 21% | 5 |
| Inference / latency / cost | 31% | 22% | 39% | 28% | 29% | 19 |
| On-device / mobile | **3%** | 0% | 5% | 0% | 11% | 6 |
| Voice / speech / telephony | 11% | 4% | 18% | 11% | 4% | 7 (all voice-agent cos) |
| Multimodal / vision | 11% | 1% | 19% | 6% | 11% | 6 |
| Observability / tracing / monitoring | 26% | 24% | 36% | 11% | 7% | 20 |
| Safety / guardrails / red-teaming | 20% | 15% | 28% | 22% | 4% | 12 |
| Prompt / context engineering | 20% | 15% | 33% | 6% | 4% | 14 |
| Product sense / taste / UX | 34% | 28% | 45% | 39% | 11% | 20 |
| Customer-facing / stakeholders | 76% | **93%** | 62% | 83% | 71% | 23 |
| Full-stack web (React/TS/Node/frontend) | 68% | 71% | 68% | **89%** | 50% | 24 |
| Python | 60% | 74% | 56% | 50% | 50% | 25 |
| Prototyping / demos / POCs | 42% | 46% | 49% | 28% | 21% | 20 |
| **Evidence of building** (side projects / portfolio / OSS / hackathons / live app) | 19% | 7% | 9% | **67%** | **50%** | 17 |
| AI coding tools as daily workflow | 25% | 9% | 34% | 39% | 29% | 16 |
| Startup / founder / 0→1 | 31% | 24% | 40% | 39% | 18% | 20 |

**Narrow-term counts (all 202)**

| Term | Share | Companies |
|---|---|---|
| Literal "eval/evals" | 20% | 17 |
| MCP | 10% | 11: Anthropic, Baseten, Cognition, Databricks, Figma, Notion, OpenAI, Replit, Scale, Sierra, Vapi |
| LLM-as-judge / graders / scorers | 5% | Anthropic, Cursor, Databricks, OpenAI, Scale |
| "Context engineering" | 5% | Anthropic, Databricks, OpenAI, Perplexity, Scale |
| "Simulations" (agent testing) | 2% | Decagon, OpenAI, Sierra, Vapi |
| "Latency" | 19% | 13 |
| "Taste" | 12% | Cognition, Cohere, Cursor, OpenAI, Perplexity, Replit, Sesame, Sierra, Stripe |
| TypeScript | 42% | 22 |

**Years of experience**

| Role bucket | 5+ yrs | 3–4 yrs | ≤2 yrs | Not stated |
|---|---|---|---|---|
| FDE/Deployed (n=68) | 60% | 12% | 4% | 24% |
| AI Eng/Applied AI (n=88) | 48% | 18% | 2% | 32% |

**What the tally says (evidence)**
- **Agents** are the common language of 2026 AI hiring.
- **Evals, observability, latency/cost, and guardrails** are how employers describe "production-grade".
- **Full-stack TypeScript and Python** are the base for new grads (89% full-stack).
- **Customer-facing** is near-universal for FDE roles (93%).
- **On-device/mobile is almost never asked for (3%).** Where mobile does appear, it is as a *surface* for agents:
  - OpenAI: "control and observe agents across web, desktop, and mobile".
  - Perplexity: agents across "desktop, mobile, headless cloud".
  - Sierra: "embedded voice mode in mobile apps".
- **Inference.** Mobile should be the delivery vehicle for the phone demo, not the headline technical claim. Fine-tuning and RL show up mainly at infra/model companies (Together, Baseten, Modal, Scale, Databricks, OpenAI), not in product and FDE roles.

### 3.3 Named postings sampled (verbatim asks; all accessed 2026-09-28)

| Company / role (level) | Posted | Key asks, verbatim or near-verbatim |
|---|---|---|
| [Anthropic, Forward Deployed Engineer](https://job-boards.greenhouse.io/anthropic/jobs/5391021008) (8+ yrs) | 2026-08-17 | "Deliver technical artifacts for customers like MCP servers, sub-agents, and agent skills"; "Production experience with LLMs including advanced prompt engineering, agent development, evaluation frameworks, and deployment at scale"; travel 25–50% |
| [Anthropic, Applied AI Engineer, Startups](https://job-boards.greenhouse.io/anthropic/jobs/5432575008) (4+ yrs) | 2026-09-23 | "prompting, context engineering, agent architectures, evaluation frameworks"; builds "evaluation suites… and architecture diagrams"; "Builder credibility… you've shipped products" |
| [OpenAI, Forward Deployed SWE, SF](https://jobs.ashbyhq.com/openai/00207abc-49b7-465c-a219-f7c1140f8047) (7+ yrs) | 2025-11-15 | full-stack; "Former founder, or early engineer… built a product from scratch is a plus"; travel up to 50% |
| [OpenAI, Applied AI Engineer, Startups (Codex)](https://jobs.ashbyhq.com/openai/d801f26e-951e-452c-9924-9449b55edc5a) | 2026-09-24 | "technical talks, live demos, workshops, hackathons"; "active user of Codex or other AI coding tools" |
| [OpenAI, Full Stack SWE, Agent Enablement](https://jobs.ashbyhq.com/openai/2d7f1028-ce9b-49c7-acc8-782714ca1cf4) | 2026-06-17 | "user experiences to control and observe agents across web, desktop, and mobile" |
| [Perplexity, MTS AI Products (Early Career, 1+ yr industry)](https://jobs.ashbyhq.com/perplexity/daa9120e-94ff-46e0-b4bd-4d2d290cb409) | 2026-09-23 | "Real evidence of building… shipped side projects with actual users… hackathon wins"; "use real usage data and evals to decide what survives"; "Product taste"; "A public track record we can read, such as GitHub, a technical blog, or a demo we can try" |
| [Perplexity, MTS New Grad portal](https://jobs.ashbyhq.com/perplexity/b539e100-4b8c-4701-a5a8-52b9a72f435e) | 2026-09-27 | Focus-school portals; otherwise "GPA of ≥3.92… A or A+ in… algorithms", or "other evidence of exceptional ability" |
| [Perplexity, Applied AI Engineer, Agent Capabilities](https://jobs.ashbyhq.com/perplexity/5c561bd0-c180-4ee1-b079-647f3c20bdc0) (6+, "exceptional candidates with less experience… encouraged") | 2026-09-10 | "offline and online evaluations for task completion, correctness, safety, latency, cost, and user satisfaction"; "tracing, replay, and monitoring infrastructure"; "permissions and safeguards for sensitive actions" |
| [Cursor, SWE New Grad 2027](https://jobs.ashbyhq.com/cursor/d0e5b41d-84ab-4887-bd3a-55589b11dd7b) | 2026-09-08 | "an app, OSS, or shipped product we can open and review (required)"; "great taste"; "AI tools as leverage without giving up correctness" |
| [Cursor, SWE Agent Evaluation & Quality](https://jobs.ashbyhq.com/cursor/2bbe9f02-83a5-4173-98be-9085d1cb5693) | 2026-04-13 | "curated datasets, offline replay, scorers / judges, regression alerts, and dashboards"; "feedback loops from real usage"; "clustering themes" of failures |
| [Cursor, Forward Deployed Engineer](https://jobs.ashbyhq.com/cursor/34cecd0c-c392-4454-8ef5-261310541011) | 2026-03-13 | 5+ yrs, including 2+ yrs customer-facing |
| [Decagon, MTS New Grad (2027)](https://jobs.ashbyhq.com/decagon/a8ff946f-d6b1-4059-bc9f-fe6b11504f2f) | 2026-08-18 | "Python, TypeScript, and asynchronous programming"; "Track record of building and shipping… personal projects"; "Experience using AI coding agents"; bonus multimodal, 0→1; teams include orchestration ("tools and guardrails… low-latency") and real-time voice infra |
| [Decagon, Staff SWE, Voice Agent](https://jobs.ashbyhq.com/decagon/2351ca53-b7fd-4835-b967-4ae2b976b5b4) | 2025-12-01 | "real-time voice runtime"; "VAD, streaming protocols"; "low-latency"; "testing, and observability standards for live voice" |
| [Sierra, SWE Agent (New Grad 2027)](https://jobs.ashbyhq.com/sierra/149f368c-52d5-408f-ba26-ad888f318a00) | 2026-08-31 | "eval frameworks, agent tooling, RAG pipelines, and prompt engineering"; "Experiment with the latest voice models"; "Comfort working directly with customers" |
| [Sierra, APX (New Grad 2027)](https://jobs.ashbyhq.com/sierra/d9c445da-c7b4-43a3-8d71-d367681c3015) | 2026-08-31 | Rotational "AI builders"; "Demonstrated curiosity and interest in AI applications (e.g., research, jobs, side projects)" |
| [Sierra, SWE Agent, Travel & Hospitality](https://jobs.ashbyhq.com/sierra/d2dc9baf-30d4-4708-9227-62a946b4b37e) | 2026-09-23 | "embedded voice mode in mobile apps… talk, tap and text with our agents all in a single view"; "MCP UI" |
| [Bland, Agent Solutions Engineer](https://jobs.ashbyhq.com/bland/824f7ebb-6d71-4484-bc7d-a2bcd4441a70) (3–10 yrs, "Exceptional new grads… welcome") | 2026-05-28 | "A portfolio of personal or side projects that showcase creativity, technical depth, and persistence"; "Prototype fast, iterate faster" |
| [Vapi, MTS Forward Deployed](https://jobs.ashbyhq.com/vapi/854a9bf5-e330-4afa-9c0f-38c3d6084808) (5+ yrs) | 2026-05-21 | "real-time, latency-sensitive systems… speech-to-text, LLMs, text-to-speech, telephony"; "evals and simulations, observability, CLI and MCP tooling"; verifiable real-user bar |
| [ElevenLabs, FDE, North America](https://jobs.ashbyhq.com/elevenlabs/6c4c57c1-ec72-42ba-af3a-eb7aebbde2e6) | 2026-09-08 | "It's ok if you only worked with customers in student clubs or side projects"; Python; APIs integration |
| [Scale AI, SWE New Grad](https://job-boards.greenhouse.io/scaleai/jobs/4730862005) | 2026-09-14 | "Hands-on experience with LLMs, evaluations, or agentic systems — whether from internships, research, or personal projects"; "a portfolio of shipped side projects" |
| [Scale AI, Frontier Agents Engineer (Applied AI)](https://job-boards.greenhouse.io/scaleai/jobs/4720573005) | 2026-07-31 | "golden datasets, regression suites, LLM-as-a-Judge, and human evaluation"; "ablation studies"; "Measure success through business outcomes, not benchmark scores" |
| [Glean, SWE Agents](https://job-boards.greenhouse.io/gleanwork/jobs/4712442005) (6+ yrs) | 2026-07-10 | "help users evaluate agent quality, inspect results, and understand failure modes"; interview includes "a brief AI-focused exercise" |
| [Harvey, Senior SWE, Agents](https://jobs.ashbyhq.com/harvey/04eb457b-e985-4e3b-9635-0a2b867ada97) | 2026-01-31 | Keyword hits: agents, evals, RAG, latency/cost, observability, prompt/context (regex-tagged, not read in full) |
| [Replit, SWE New Grad (2027)](https://jobs.ashbyhq.com/replit/b5e81eae-06f9-4798-8988-2d06ca936dbc) | 2026-09-09 | "Show us something you've built. Replit, GitHub, a live URL"; React, Node.js, databases; "genuine instinct for working alongside AI agents" |
| [Replit, FDE](https://jobs.ashbyhq.com/replit/9a56d0ac-db44-4dc1-b960-2364557bf4c8) (5+ yrs) | 2026-08-24 | "Hands-on work with LLM applications in production: retrieval, tool calls, and evals" |
| [LangChain, Deployed Engineer (Early Career)](https://jobs.ashbyhq.com/langchain/0f35c8e1-9318-411d-929b-04c60e6d8522) (1–3 yrs) | 2026-08-17 | "beyond simple API calls, including multi-step workflows, orchestration, and failure handling"; "Build and run tailored demos"; "builder credibility"; 40% travel |
| [Notion, SWE Early Career (AI)](https://jobs.ashbyhq.com/notion/85947779-6b87-466a-98bc-30a640448c28) (0–2 YOE) | 2026-07-06 | "build or extend an evaluation set"; "add monitoring + guardrails, or improve latency/cost/reliability"; AI/ML "through coursework, projects, internships, or hackathons"; "Cursor, Claude Code" |
| [Ramp, Applied AI Engineer](https://jobs.ashbyhq.com/ramp/d204e136-2749-42de-82b4-88a0dd352090) | 2026-01-12 | "We care less about where you trained and more about what you've built"; "track record of working on full-stack AI projects" |
| [Ramp, SWE Forward Deployed AI Solutions](https://jobs.ashbyhq.com/ramp/b614563f-3ce6-4dca-b5ba-0e5a6c8bda27) | 2026-07-28 | Artifacts: "System context and data flow diagrams… Security model… Evaluation plan covering quality metrics, acceptance tests, and red-teaming… Operational plan covering monitoring, alerting, incident response, and runbooks"; "RAG, agents, monitoring, and evals" |
| [Cognition, Deployed Engineer](https://jobs.ashbyhq.com/cognition/d72d584c-bb11-4b6a-b043-d81425ea884a) | 2025-07-10 | "track record of exceptional performance in whatever you've pursued"; "Customer empathy"; travel 25–50% |
| [Databricks, AI Engineer, FDE](https://databricks.com/company/careers/open-positions/job?gh_jid=8546367002) | 2026-05-13 | "not intended for internship, new graduate, or entry-level applicants" |
| [Baseten, FDE (Training)](https://jobs.ashbyhq.com/baseten/11ab2593-6648-4943-ab4a-284fe7e89720) | 2026-08-19 | "Minimum 1-2 years of software engineering experience" (a junior-accessible FDE) |
| **Big tech:** [Amazon, SDE, AWS Forward Deployed Engineering](https://www.amazon.jobs/en/jobs/10523580/software-development-engineer-aws-forward-deployed-engineering) (3+ yrs) | 2026-09-01 | "Agentic AI… Orchestration and workflow… Platform infrastructure"; preferred "agentic workflows, RAG pipelines, or foundation model integration"; "on-site watching it work, debugging it in real time" |
| **Big tech:** [Amazon, FDE, US Government](https://www.amazon.jobs/en/jobs/10517550/forward-deployed-engineer-fde-us-government) (3+ yrs, TS/SCI) | 2026-08-27 | "Experience with AI tools: eval frameworks, agent tooling, RAG pipelines, and prompt engineering"; 30–50% travel |
| **Big tech:** [Amazon, SWE, AWS Applied AI Solutions](https://www.amazon.jobs/en/jobs/10501368/software-engineer-aws-applied-ai-solutions) | 2026-08-13 | AI agents as CRDT co-editors; "deliver code with agents at high speed, but without sacrificing the quality" |
| **Big tech:** [Palantir, FDSE New Grad](https://jobs.lever.co/palantir/e500bcf3-19d8-4d3c-b340-4d76e4a55b40) | live | "Build custom applications, LLM workflows, and production solutions"; "Own relationships with stakeholders" |
| **Big tech:** [Stripe, SWE New Grad](https://stripe.com/jobs/search?gh_jid=8130881) | 2026-08-31 | "Experience and familiarity with programming, either through side projects or classwork" (the traditional baseline, for contrast) |

---

## 4. Presentation: what convinces a skimming reviewer

### 4.1 How reviewers skim (evidence)
- **Triage takes 10 seconds to 2 minutes per project.** Reviewers weigh, in order: judgment in problem choice, a working live URL, a README that "states the problem, shows the decision you made, and admits one tradeoff", and real usage ("Ten real users you can name beats a thousand imaginary ones") ([Pickuma, 2026-06-09](https://pickuma.com/for-junior/side-projects-that-impress-hiring-managers-2026/)). [W/M]
- **What gets looked at on GitHub:** pinned repos ("Four polished projects beat six random ones"), a README with problem, architecture, and proof, a **live demo** ("one of the highest-value additions"), and tests/CI ("Even a modest test suite says you think about regression risk") ([Underdog.io, 2026-06-19](https://underdog.io/blog/what-hiring-managers-look-for-on-github)). [M]
- **Hiring managers would rather click a hosted app than read a vibe-coded repo** ([HN, Feb 2026](https://news.ycombinator.com/item?id=47054682)). [M]
- **Specific numbers beat claims.** "improved recall from 61% to 84%" beats "I built a RAG system" ([TryCrucible](https://trycrucible.io/blog/how-to-get-hired-as-ai-engineer-2026)). [W/M]
- **An eval-portfolio walkthrough is a real screening step for evals roles.** One recruiter guide describes asking candidates "which metric turned out to be misleading" ([HeroHunt](https://www.herohunt.ai/blog/how-to-recruit-ai-evals-engineers-2026/)). [W]
- **Expect the project to be probed live.**
  - HBR (Jun 2026): generative AI is "undermining the reliability of traditional hiring signals", and companies (Google and McKinsey are named in the article's text as quoted on HN) are bringing back in-person interviews ([HBR](https://hbr.org/2026/06/ai-has-broken-hiring-heres-how-to-fix-it), [HN thread](https://news.ycombinator.com/item?id=48620142)). [M]
  - Anthropic: take-homes and live interviews without AI unless told otherwise ([Anthropic](https://www.anthropic.com/candidate-ai-guidance)). [S]

### 4.2 What employers literally ask you to submit (evidence) [S]
- Cursor: "share an example of an exceptional technical project… (GitHub, live app, OSS, or shipped product)."
- Replit: "Replit, GitHub, a live URL, your call."
- Perplexity: "GitHub, a technical blog, or a demo we can try."
- Vapi: user or revenue proof that is "easy to verify."
- Perplexity new-grad portal: non-focus-school applicants should describe "evidence of exceptional ability" in the "Anything Else" field. **Inference:** a strong, verifiable project is the natural thing to put there.

### 4.3 Recommended packaging
**Inference**, assembled from the asks above and the FDE artifact lists in §3.3.
1. **One-tap live demo on a phone.** A QR code at the top of the README, a no-login "demo mode", and a seeded account.
2. **A 60–90s screen recording from a real phone.** No source gives hard data on video length. It is aligned with the "demo we can try" and "live demos" asks, and it covers reviewers who won't install anything.
3. **Top block of the README, visible without scrolling:**
   - one-line problem
   - who uses it (N weekly users; link to testimonials)
   - three headline metrics: eval pass rate or quality score, p50/p95 latency, $/task
   - architecture diagram
4. **Eval report page.** Dataset size and source, rubric, judge-vs-human agreement, failure taxonomy, before/after table, and the regression check wired into CI. This is Hamel-style: error analysis first, binary pass/fail judgments, and a custom data viewer ([Hamel](https://hamel.dev/blog/posts/field-guide/)).
5. **Ops page.** Trace/replay screenshots, cost and latency budget, guardrails and permission model, incident log. This mirrors [Ramp FDE's artifact list](https://jobs.ashbyhq.com/ramp/b614563f-3ce6-4dca-b5ba-0e5a6c8bda27).
6. **Decision log / ADRs**, including "what I'd do next" and "what didn't work."
7. **A "How I used AI coding agents" note:** what was delegated, and how it was verified (tests, reviews). This covers the "sound judgment about when their output is wrong" ask.
8. **One public technical write-up** (blog, or X/LinkedIn thread) that links to all of the above.

### 4.4 Resume, LinkedIn, X, HN (evidence and gaps)
- **Resumes are low-signal on their own.** "zero signal: resume & cover letter… medium signal: top 15 school / top N internship experience / built something with paying users… highest signal: personal referrals" ([HN interviewer](https://news.ycombinator.com/item?id=48621545)). [M]
  - **Inference:** use the project to *create* referrals. Send it directly to engineers at target companies, and use it in FDE-style outreach.
- **Show HN is saturated:** volume went from about 1,200 (Feb 2023) to about 4,800 (Jan 2026), roughly 4×. 37.2% of posts get stuck at 1 point, and posts stay about 2.9h on the front page at peak ([analysis](https://www.arthurcnops.blog/death-of-show-hn/)). [M]
- **X and LinkedIn:** I could not fetch them directly, so I have no 2026 primary evidence on what gets noticed there.
  - The LinkedIn-exec advice CNBC ran in Jan 2026 was only a search result I didn't open ([CNBC](https://www.cnbc.com/2026/01/11/ai-dominate-hiring-2026-linkedin-execs-top-tips-stand-out.html)).
  - **Inference:** a phone-screen video clip plus a hard number ("p95 540 ms voice round-trip, 91% task pass on 400-case eval") is the format most likely to travel. GitHub stars are a byproduct, not a goal.

---

## 5. New grads and interns vs experienced hires; FDE specifics

### 5.1 Market context
- **New-grad hiring is down about 65% at big tech and about 76% at early-stage startups vs 2019.** New grads are "twice as likely to be a 'founder'" as at the 2022 peak, and FDE roles are up about 30% ([SignalFire, 2026-06-22](https://www.signalfire.com/blog/signalfire-state-of-talent-report-2026)). [S]
- SignalFire tells employers to "Reframe junior talent as agent operators" and to hire "AI-native new grads who can manage autonomous workflows, run rapid prototyping experiments, and audit automated code outputs." [S]
- FDE demand is still rising in 2026: Pragmatic Engineer's "Forward deployed engineering heats up again", 2026-05-14 (paywalled) ([PE](https://newsletter.pragmaticengineer.com/p/the-pulse-forward-deployed-engineering)). [M]
  - A search snippet also mentioned an AWS $1B FDE org (**unverified**). Amazon's live "AWS Forward Deployed Engineering" postings do confirm the org exists.
  - The FDE surge traces back to a16z's June 2025 "Trading Margin for Moat" ([a16z](https://a16z.com/services-led-growth/)).

### 5.2 What changes at new-grad and intern level (evidence)
- **Evidence of building is the main ask:** 67% of new-grad and 50% of intern postings, vs 7–9% of experienced roles (§3.2). Experienced roles instead ask for years of "production experience with LLMs" (Anthropic, Replit, Glean). [S]
- **Pedigree filters still exist at the most selective shops.** Perplexity's new-grad portal favors focus schools or GPA ≥3.92, but explicitly accepts "evidence of exceptional ability" instead. [S]
- **New grads are expected to be fluent with AI coding agents** (39% of new-grad postings) and still able to judge correctness. [S]
- **Base stack:** full-stack TypeScript/React plus Python (89% of new-grad postings mention full-stack/web). [S]
- **The value of personal projects fades once you have work experience,** unless they have users ([HN](https://news.ycombinator.com/item?id=46623164)). [M] For this candidate that argues for one high-signal project with users, rather than many small ones.

### 5.3 FDE seniority reality and junior entry points
- **Most FDE roles are senior** (FDE/Deployed bucket, n=68):

  | Minimum experience | Share of postings |
  |---|---|
  | 5+ yrs | 60% |
  | 3–4 yrs | 12% |
  | ≤2 yrs | 4% |
  | Not stated | 24% |

  Named senior requirements: Anthropic FDE 8+ yrs, OpenAI FDSWE 7+, Cursor FDE 5+, Replit FDE 5+, Vapi FD 5+. Databricks' AI FDE explicitly excludes new grads. [S]
- **Junior-accessible FDE and FDE-like tracks** [S/M]:
  - [ElevenLabs FDE](https://jobs.ashbyhq.com/elevenlabs/6c4c57c1-ec72-42ba-af3a-eb7aebbde2e6) (customer work from "student clubs or side projects" counts)
  - [Bland Agent Solutions](https://jobs.ashbyhq.com/bland/824f7ebb-6d71-4484-bc7d-a2bcd4441a70) ("Exceptional new grads… welcome")
  - [LangChain Deployed Engineer, Early Career](https://jobs.ashbyhq.com/langchain/0f35c8e1-9318-411d-929b-04c60e6d8522) (1–3 yrs)
  - [Baseten FDE (Training)](https://jobs.ashbyhq.com/baseten/11ab2593-6648-4943-ab4a-284fe7e89720) (1–2 yrs)
  - [Palantir FDSE New Grad](https://jobs.lever.co/palantir/e500bcf3-19d8-4d3c-b340-4d76e4a55b40)
  - [Sierra SWE-Agent New Grad](https://jobs.ashbyhq.com/sierra/149f368c-52d5-408f-ba26-ad888f318a00) and [APX](https://jobs.ashbyhq.com/sierra/d9c445da-c7b4-43a3-8d71-d367681c3015) (customer-facing agent building)
  - [Decagon MTS New Grad](https://jobs.ashbyhq.com/decagon/a8ff946f-d6b1-4059-bc9f-fe6b11504f2f) (the Agent Engineering team works "directly with customers")
  - FDE New Grad postings at [Netic](https://jobs.ashbyhq.com/netic/f2d170eb-c4c3-4715-9d2e-84dd4fe857c8) and [Domino](https://builtin.com/job/forward-deployed-engineer-new-grad-campus-recruiting-2026/7292257)
  - Salesforce "Associate FDE", per [Exponent](https://www.tryexponent.com/blog/forward-deployed-engineer-interview-the-definitive-2026-guide-fde)
  - Pragmatic Engineer (Aug 2025): Palantir has hired FDEs with "as little as one year" of experience, and Ramp "hires some exceptional new grads" ([PE](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers)).

### 5.4 FDE interview and artifacts, and what that means for the portfolio
- **Interview shape.** A decomposition or open-ended case round (the "make-or-break" round), a client-simulation role-play, real-world system design, and coding plus behavioural. Early-career predictor: "having shipped a real product end-to-end and talked to its users directly" ([Exponent](https://www.tryexponent.com/blog/forward-deployed-engineer-interview-the-definitive-2026-guide-fde)). [M]
- **What FDEs actually produce** [S]:
  - MCP servers, sub-agents, agent skills (Anthropic)
  - eval plans, security models, runbooks, data-flow diagrams (Ramp)
  - POCs, tailored demos, workshops (LangChain)
  - GitOps configs, evals and simulations, observability, MCP tooling (Vapi)
  - voice-model evals for a call-center customer (an OpenAI FDE example, [PE 2025](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers))
- **Inference.** Package the project as a "deployment": discovery notes → requirements → architecture and security model → eval plan → launch → runbook → iteration log with user feedback. That reads as FDE-ready and helps for AI-Engineer and SWE roles too.
- **Travel is part of the job:** 25–50% at Anthropic, Cognition, OpenAI, Amazon; 40% at LangChain. [S]

---

## 6. Implications for this developer (Inference, mapped to the lead's hard requirements)

**Signal spec for the new project**
1. **Useful every day, for people you can name** (requirement 3 → checklist #2). Recruit a real cohort (classmates, a club, a campus org), instrument usage, and show weekly actives and retention. This is the scarcest signal and the one postings ask to verify.
2. **An agentic core, not a wrapper** (requirement 4 → checklist #3). Tool use, ideally through the developer's own MCP server(s), since MCP is named by 11 companies. Add state and memory, failure handling, and confirmation or permissions for risky actions.
3. **Evals as a first-class feature** (requirement 4/5 → checklist #4).
   - A golden set of a few hundred cases built from real usage.
   - A CI regression gate, an LLM judge checked against human labels, and a published failure taxonomy.
   - Where it fits, agent **simulations** (a Sierra/Decagon/Vapi practice).
4. **Ops you can show:** traces and replay, p50/p95 latency, and $/task visible in-app ("nerd mode") and in the README (checklist #5).
5. **Wow in 10 seconds on a phone** (requirements 1–2). The strongest match to employer demand is a **voice + tap + text agent on mobile**, the pattern Sierra is building ("talk, tap and text with our agents all in a single view"), with sub-second turn-taking.
   - This lines up with voice-agent employers (Sierra, Decagon, Bland, Vapi, ElevenLabs, Sesame).
   - It can reuse the planned Bland voice-call tool gateway.
   - Mobile itself is rarely a required skill (3%), so frame the phone as the *surface* and the agent, evals, and latency work as the *substance*.
6. **FDE-style packaging:** discovery notes, architecture and security model, eval plan, runbook, decision log, 60–90s phone video, QR code (checklist #7, #9, #10).
7. **Avoid:** another visualization, generic RAG chat, a thin wrapper, or AI-written code you can't defend in an AI-free interview.

**Fit with the 3–6 week constraint.** Scope the eval harness and the ops views as v1 deliverables, not extras. Postings treat them as proof that the thing is production-grade. Leave fine-tuning and RL out unless the project specifically targets infra/model companies (Together, Baseten, Modal): only 17% and 8% of postings mention them.

---

## 7. Sources (accessed 2026-09-28 unless noted)

**Job postings and ATS data [S]**
- Every posting linked in §3.3.
- Bulk pulls: Greenhouse (`boards-api.greenhouse.io/v1/boards/{anthropic,scaleai,gleanwork,databricks,stripe,figma,togetherai}/jobs?content=true`), Ashby (`api.ashbyhq.com/posting-api/job-board/{openai,perplexity,cursor,decagon,sierra,bland,vapi,elevenlabs,harvey,replit,cognition,cohere,langchain,notion,ramp,modal,baseten,writer,lovable,sesame}`), and Amazon (`amazon.jobs/en/search.json`).

**Reports, first-party pages, and newsletters**

| Source | Date | Strength |
|---|---|---|
| [SignalFire State of Tech Talent 2026](https://www.signalfire.com/blog/signalfire-state-of-talent-report-2026) | 2026-06-22 | S |
| [Anthropic: Guidance on Candidates' AI Usage](https://www.anthropic.com/candidate-ai-guidance) | 2025-07-10 | S |
| [HBR: AI Has Broken Hiring](https://hbr.org/2026/06/ai-has-broken-hiring-heres-how-to-fix-it) (partly paywalled) | 2026-06-08 | M |
| [Pragmatic Engineer: What are FDEs](https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers) | 2025-08-12 | M/S |
| [Pragmatic Engineer: FDE heats up again](https://newsletter.pragmaticengineer.com/p/the-pulse-forward-deployed-engineering) (paywalled) | 2026-05-14 | M |
| [a16z: Trading Margin for Moat](https://a16z.com/services-led-growth/) | 2025-06 | M |
| [Hamel Husain: Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/) | 2025-03-24 | S (practitioner) |
| [Hamel: Evals FAQ](https://hamel.dev/blog/posts/evals-faq/) | n/a | M |
| [Eugene Yan: How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/) (hunger, judgment, empathy; eval ownership) | 2024-07 (older) | M |
| [Chip Huyen: AI Engineering resources](https://github.com/chiphuyen/aie-book) (evaluation-driven development) | 2025 | M |
| [swyx: Scaling without Slop](https://www.latent.space/p/2026) (taste, anti-slop) | 2026-01-23 | M |
| [Latent Space: AIE Europe debrief](https://www.latent.space/p/unsupervised-learning-2026) (harness/context engineering, evals, observability tracks) | 2026-04-23 | M |
| [Sierra: Meet the AI agent engineer](https://sierra.ai/blog/meet-the-ai-agent-engineer) | 2024-07-11 | M |
| [Exponent: FDE Interview Guide 2026](https://www.tryexponent.com/blog/forward-deployed-engineer-interview-the-definitive-2026-guide-fde) | 2026 | M |
| [AI Engineering Insider: job market moved past prompting](https://aiengineeringinsider.substack.com/p/the-ai-engineer-job-market-has-moved) | 2026-05-08 | M |
| [KORE1: How to Hire an AI Engineer 2026](https://www.kore1.com/how-to-hire-ai-engineer-2026/) | 2026-05-27, updated 2026-08-06 | M |
| [Underdog.io: What hiring managers look for on GitHub](https://underdog.io/blog/what-hiring-managers-look-for-on-github) | 2026-06-19 | M |
| [TryCrucible](https://trycrucible.io/blog/how-to-get-hired-as-ai-engineer-2026) | 2026-07-14 | W/M |
| [Pickuma](https://pickuma.com/for-junior/side-projects-that-impress-hiring-managers-2026/) | 2026-06-09 | W/M |
| [dev.to: 5 AI portfolio projects](https://dev.to/klement_gunndu/5-ai-portfolio-projects-that-actually-get-you-hired-in-2026-5bpl) | 2026-03-07 | W |
| [Upskillist](https://www.upskillist.com/blog/10-ai-portfolio-examples-impress-recruiters/) (unsourced stats) | 2026-07 | W |
| [HeroHunt: recruiting evals engineers](https://www.herohunt.ai/blog/how-to-recruit-ai-evals-engineers-2026/) | 2026 | W |
| [dglearning: 6 side projects](https://dglearning.substack.com/p/6-side-projects-that-actually-get) (contrarian RAG claim) | 2026 | W |

**Hacker News, 2026 [M]**
- [Interviewer's signal ranking](https://news.ycombinator.com/item?id=48621545) and [follow-up](https://news.ycombinator.com/item?id=48624358)
- ["zero paying users" comment](https://news.ycombinator.com/item?id=48520474)
- ["ask for a link to a hosted application"](https://news.ycombinator.com/item?id=47054682)
- [Trade-off-based interviews](https://news.ycombinator.com/item?id=48663942)
- [Personal projects with users](https://news.ycombinator.com/item?id=46623164)
- [GPT-6 earth site thread](https://news.ycombinator.com/item?id=49665756), with comments [1](https://news.ycombinator.com/item?id=49666385) and [2](https://news.ycombinator.com/item?id=49666381)
- [Show HN drowning analysis](https://www.arthurcnops.blog/death-of-show-hn/) ([thread](https://news.ycombinator.com/item?id=47045804))
- [Vibe-coded Show HN won't get you hired at OpenAI/Meta](https://news.ycombinator.com/item?id=47326731)
- Hiring posts: [Akur8](https://news.ycombinator.com/item?id=47603501) ("evals… things you actually have opinions on"), [Jefit](https://news.ycombinator.com/item?id=48373447) ("solo side projects count… AI-coding-assistant fluency is non-negotiable")

**Context**
- [TechCrunch: SpaceX to acquire Cursor](https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo/)
- [AI Weekly: deal closed](https://aiweekly.co/alerts/spacex-closes-60b-cursor-deal-folds-it-into-spacexai-unit)

**Not reachable:** Reddit (blocked for both fetch and search), X, and LinkedIn. A Medium article, ["The AI Portfolio Projects That Instantly Tell Recruiters You're a Junior" (Sep 2026)](https://medium.com/write-a-catalyst/the-ai-portfolio-projects-that-instantly-tells-recruiters-youre-a-junior-f9629b9a38da), returned 403, so only its title was seen.
