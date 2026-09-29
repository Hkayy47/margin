# 06 — Capability Unlocks (Jan–Sep 2026) → "Only-possible-in-2026" Project Seeds

*Prepared 2026-09-28. Slice: what became newly possible or newly cheap in 2026, how saturated each opportunity already is, and 10 project seeds that fit the hard requirements (wow in 10 s, live phone demo, daily-useful, real engineering depth, recruiter signal, 3–6 weeks for one person + coding agents).*

**Evidence legend:** **[S] strong** = official blog, changelog, docs or pricing page, or tier-1 press (CNBC, Fortune, TechCrunch, Reuters, BBC). **[M] medium** = reputable secondary source (Wikipedia, a16z, Latent Space, trade press, primary engineering blogs, HN Show HN posts with a repo). **[W] weak** = aggregator or SEO blog, single unverified source, or conflicting claims.
**Convention:** "Evidence" means what a source says. "Inference" means my own reasoning. Items dated before 2026 are labeled with their date.
**Method:** about 40 web searches (the session search budget then ran out), about 50 page fetches including 15+ Hacker News Algolia queries (Jan 1–Sep 28, 2026), plus the official Gemini API changelog, OpenAI API changelog and Gemini pricing page, which I read in full.

---

## 0. TL;DR

1. **Realtime voice now feels like a real conversation and costs pennies.** OpenAI's **GPT-Live-1** (Sep 10) is *full-duplex* (it listens while it speaks, backchannels, and handles interruptions) at **$0.05/min**. Google's **Gemini 3.8 Live** (Sep 15) adds near-real-time *visual grounding* and *background tool calls while talking* at **$0.005/min audio in and $0.018/min audio out, with a free tier**. This is the biggest phone-first unlock of 2026. [S]
2. **The generic "camera + voice assistant" is already taken.** Gemini Live's "Guided Vision" highlights objects on the camera feed. Google's Gemini Live Agent Challenge drew **1,536 submissions** (Feb–Mar 2026). The open space is **narrow daily workflows with a deterministic verifier and evals**, not another general assistant. [S]
3. **On-device and in-browser AI became real on phones.** Relevant releases: **WebGPU in iOS Safari 26** (Sep 2025), **Gemma 4 E2B/E4B** with audio and vision input under Apache 2.0 (Apr 2), **Needle 2**, a 14 MB tool-calling model (Aug), **Kitten TTS** under 25 MB (Mar), and **Apple Foundation Models** with image input plus free Private Cloud Compute (June; Swift only). Hybrid local-plus-cloud is now practical, and it is a strong engineering signal. [S/M]
4. **Price floor collapse.** GPT-6 Luna costs **$0.10 in / $0.50 out per M tokens** (Sep 22). DeepSeek V4 Flash is about $0.14/$0.28, and Gemini 3.5 Flash-Lite is $0.30/$2.50. You can now afford a reasoning call per event or keyframe in a consumer app. [S/M]
5. **New distribution surfaces opened, with little competition yet.**
   - Meta Ray-Ban Display **Web Apps** (plain HTML/JS, May 14).
   - **Wearables Device Access Toolkit 1.0** (rolling out Sep 30).
   - **Meta AI Connectors** and **WebMCP**, both in developer preview.
   - **MCP Apps**, which render your UI inside Claude and ChatGPT (Jan 26; formalized in the 2026-07-28 spec).

   All of these are gated or early, so treat them as a bonus layer, not the core demo. [S/M]
6. **Crowded lanes to avoid:**
   - 24/7 personal agents (OpenClaw, Gemini Spark, Manus, Genspark, Claude Cowork Dispatch).
   - Memory and lifelogging (ChatGPT "Dreaming", Claude memory, Gemini Personal Intelligence, Apple Watch Siri Recap, Bee/Plaud).
   - Translation, language tutors, agentic browsers, and image or video generation apps.
   - Phone-calling agents (these also overlap the planned Bland gateway). [S/M]
7. **Watch items:** **OpenAI DevDay is tomorrow (Sep 29, 2026)** and **Meta DAT 1.0 rolls out Sep 30**. Re-check realtime, vision, agent and apps APIs after both. [M/S]

---

## 1. 2026 timeline at a glance

| Date (2026) | Release | Why it matters for a phone-first AI product | Evidence |
|---|---|---|---|
| Jan 13 | Veo 4K output in the Gemini API | Video generation reaches production quality (Veo later deprecated in favor of Omni) | [S] [Gemini changelog](https://ai.google.dev/gemini-api/docs/changelog) |
| Jan 14 | Gemini memory rebranded and expanded as "Personal Intelligence" | Consumer memory becomes table stakes | [M] [memoryplugin](https://blog.memoryplugin.com/claude-vs-chatgpt-vs-gemini-memory/) |
| Jan 26 | **MCP Apps**, the first official MCP extension, for interactive UI inside chat (Claude web/desktop, Goose, VS Code Insiders, ChatGPT) | Your UI can live inside the assistants | [S] [MCP blog](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) |
| Jan 29 | **Project Genie** (Genie 3 interactive worlds, AI Ultra US only, no API) | World models reach consumers but are not programmable | [S] [Google](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/) |
| Jan 29 | Gemini API Computer Use tool for Gemini 3 Pro and Flash previews | Cheap computer use | [S] changelog |
| Feb (Chrome 146) | **WebMCP** early preview (`navigator.modelContext`, later `document.modelContext`) | Websites expose typed tools to agents | [M] [Spronta](https://www.spronta.com/blog/state-of-webmcp-july-2026/) |
| Feb 10 | OpenAI Responses API: Skills, hosted shell, server-side compaction | Agent infrastructure becomes a commodity | [S] [OpenAI changelog](https://developers.openai.com/api/docs/changelog) |
| Feb 25 | **Android AppFunctions** (on-device, MCP-like) plus agent UI automation (Galaxy S26, Pixel 10) | OS-level phone agents, owned by the platform | [S] [Android blog](https://developer.android.com/blog/posts/the-intelligent-os-making-ai-agents-more-helpful-for-android-apps) |
| Feb 26 | **Nano Banana 2** (`gemini-3.1-flash-image`) | Strong image editing at $0.067 per image | [S] changelog, [pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| Feb | NVIDIA **PersonaPlex**, an open full-duplex speech model built on Moshi, with personas and voice cloning | Open full-duplex voice | [M] [HF](https://huggingface.co/kyutai/personaplex-rl-seamless), [review](https://ai.ksopyla.com/posts/voice-to-voice-models-2026-review/) |
| Mar 2 | Claude chat memory for all plans, including free | Memory becomes a commodity | [W/M] memoryplugin |
| Mar 5 | GPT-5.4 with built-in computer use and 1M context | | [S] OpenAI changelog |
| Mar 10 → Apr 22 GA | **gemini-embedding-2**: one embedding space for text, image, video, audio and PDF | Cheap multimodal retrieval over your own video and audio | [S] changelog, pricing |
| Mar 12 | Sora 2 API: 20 s clips, character references, 1080p, video edit endpoint | | [S] OpenAI changelog |
| Mar 19 | Kitten TTS, with the smallest model under 25 MB | On-device TTS for web and mobile | [M] [GitHub](https://github.com/KittenML/KittenTTS) (HN 561 pts) |
| Mar 25 | Lyria 3 music generation in the API | | [S] changelog |
| Mar 26 | `gemini-3.1-flash-live-preview` | Cheaper live audio | [S] changelog |
| Mar 30 | Qwen3.5-Omni (30B-A3B, omni input with speech output; open-weight status unclear) | Possible open "GPT-4o-class" omni model | [W] [WaveSpeed](https://wavespeed.ai/blog/posts/what-is-qwen3-5-omni/) |
| **Apr 2** | **Gemma 4** (E2B/E4B/26B-A4B/31B). Edge models take **audio, image and video input**, have 128K context, support function calling, and ship under Apache 2.0 | Serious multimodal on-device model | [S] [Google](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) |
| Apr 8 | Meta **Muse Spark** (first Meta Superintelligence Labs model; 1.1 on Jul 9; 1.3 in Sep) | | [S] [Meta](https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/) |
| Apr 21–22 | **GPT Image 2** in the API and ChatGPT Images 2.0 | Accurate text rendering, reasoning-planned edits | [M/S] [OpenAI model page](https://developers.openai.com/api/docs/models/gpt-image-2) |
| Apr 23 | **Claude Managed Agents Memory** (public beta); "Dreaming" memory consolidation followed in May | Hosted agents with persistent memory | [S] [Claude blog](https://claude.com/blog/claude-managed-agents-memory) |
| Apr 24 | **DeepSeek V4** Pro (1.6T/49B active) and Flash (284B/13B active), 1M context, open weights | Near-frontier open model at low price | [S] [DeepSeek](https://api-docs.deepseek.com/news/news260424/) |
| May 5 | Gemini File Search goes multimodal (native image embeddings) | Managed multimodal RAG | [S] changelog |
| **May 7** | **GPT-Realtime-2** (GPT-5-class reasoning voice, 128K context), **-Translate** (70+ → 13 languages, $0.034/min), **-Whisper** (streaming, $0.017/min). Realtime API reaches GA | Voice agents that can actually reason | [S] OpenAI changelog; [M] [Latent Space](https://www.latent.space/p/ainews-gpt-realtime-2-translate-and) |
| May 12 | Cactus **Needle**, which distills Gemini tool calling into a 26M-parameter model | Tiny local tool callers | [M] [GitHub](https://github.com/cactus-compute/needle) (HN 776 pts) |
| **May 14** | **Meta Ray-Ban Display opened to developers**: display APIs plus **Web Apps (HTML/CSS/JS)**, camera, audio, Neural Band input | Web developers can target consumer glasses | [S] [Meta](https://developers.meta.com/blog/build-for-display-glasses/) |
| **May 19–20** | **Google I/O**: Gemini 3.5 Flash GA, **Gemini Omni** (any-to-video), **Managed Agents**, Antigravity 2.0, **Gemini Spark** (24/7 agent), WebMCP, Android XR DP4, Gemini Nano 4 preview, AppFunctions early access | | [S] [100 announcements](https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/), [dev keynote](https://developers.googleblog.com/all-the-news-from-the-google-io-2026-developer-keynote/), [Android](https://android-developers.googleblog.com/2026/05/17-things-android-developers-google-io.html) |
| **Jun 8–9 (WWDC)** | **Foundation Models**: image input, free **Private Cloud Compute** model (32K context) for apps under 2M first-time downloads, Claude and Gemini behind the same Swift API, Dynamic Profiles, Evaluations framework, open source. **iOS 27**: Siri on-screen awareness, App Intents 2.0 and View Annotations | | [S] [WWDC26 video](https://developer.apple.com/videos/play/wwdc2026/241/), [MacRumors](https://www.macrumors.com/2026/06/09/apple-outlines-major-ai-and-developer-tool-updates/) |
| Jun 9 / Jun 30 / Jul 24 | Claude Fable 5 and Mythos 5 / Sonnet 5 / **Opus 5** ($5/$25, state of the art on OSWorld 2.0) | Frontier computer-use agents | [S] [Anthropic](https://www.anthropic.com/news/claude-opus-5); [M] [Wikipedia](https://en.wikipedia.org/wiki/Claude_(language_model)) |
| June | ChatGPT "Dreaming" memory (curates memory in the background) | Memory saturation | [W] memoryplugin |
| Jun 16 | Snap Specs priced at $2,195, shipping fall 2026 | Consumer AR glasses running OpenAI and Gemini | [M] [Road to VR](https://roadtovr.com/snap-specs-2026-ar-glasses-release-date-price/) |
| Jun 24 | Gemini 3.5 Flash computer use enters public preview | Cheap browser agents | [S] changelog |
| Jun 30 | `gemini-omni-flash-preview` in the API; Veo models shut down | | [S] changelog |
| Jul 9 | GPT-5.6 family (Sol, Terra, Luna) | | [S] OpenAI changelog |
| Jul 16 | Kimi K3 (reported as a 2.8T-parameter open model) | | [W/M] aggregators |
| Jul 28 | `gpt-transcribe` and `gpt-live-transcribe` (context and keyword hints). **MCP spec 2026-07-28** makes the core stateless and formalizes MCP Apps | | [S] OpenAI changelog; [M] [Scott Logic](https://blog.scottlogic.com/2026/09/16/mcp-apps-your-ui-their-chat.html) |
| Aug 11 | **Needle 2** (45M params, 14 MB binary, 28 MB RAM; runs on iOS, Android and WASM) | Tool calling in any PWA | [M] [MarkTechPost](https://www.marktechpost.com/2026/08/13/cactus-compute-needle-2-45m-parameter-tool-calling-model/) (HN 537 pts) |
| Aug 26 | `gemini-3.5-transcribe(-live)` GA: 4.0% streaming word error rate, bias list of 1,000 terms | | [S] changelog, [Google](https://blog.google/innovation-and-ai/technology/developers-tools/build-real-time-voice-applications-gemini-audio/) |
| Aug 27 | Gemini Omni 1.1 Flash GA (video extension, interpolation) | | [S] changelog |
| **Sep 1** | **Agentic video understanding** (Flash-Lite navigates a video timeline dynamically). **World Labs Atlas** (omni world model, early access) | | [S] changelog, [World Labs](https://www.worldlabs.ai/blog/atlas) |
| Sep 3–4 | **GPT-6 Astra**, headlined by computer use. **Lyria 3.5** GA with full-length songs at $0.08 per song | | [S] [CNBC](https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html), [Fortune](https://fortune.com/2026/09/03/openai-debuts-gpt-6-astra-computer-use-greg-brockman-says-start-of-agi/), pricing |
| Sep 8 | GPT Image 2.5 | | [S] OpenAI changelog |
| Sep 9–10 | **Apple Watch Siri Recap**: always-listening conversation summaries | Ambient memory now built into the OS | [S] [TechCrunch](https://techcrunch.com/2026/09/09/apple-watchs-new-feature-listens-to-your-chats-and-recaps-them/) |
| **Sep 10** | **GPT-Live-1**, full-duplex, **$0.05/min billed per second**. **OpenAI Agents API** beta with durable sessions and hosted sandboxes | Human-like voice turn-taking | [S] OpenAI changelog; [M] [TestingCatalog](https://www.testingcatalog.com/openai-launches-gpt-live-1-for-full-duplex-voice-agents/) |
| **Sep 15** | **Gemini 3.8 Live** plus Extended Thinking: speech-to-speech with visual grounding, async tools, 97 languages, #1 on the Artificial Analysis S2S index (82.6) | Voice plus camera at pennies per minute | [S] [Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/) |
| Sep 22 | **GPT-6 Sol ($2/$10) and Luna ($0.10/$0.50)**. Claude Opus 5.5. Gemini 3.8 Flash TTS with voice design and voice replication | Price floor | [S] OpenAI changelog, Gemini changelog; [M] Wikipedia |
| Sep 23–24 | **Meta Connect**: DAT 1.0 (rolling out Sep 30), Web Apps UI toolkit and simulator, **Meta AI Connectors**, WebMCP developer preview, Muse Glimmer (open 30B), Meta Model API GA, a $1M hackathon. **Gemini 3.8 Live Avatar** GA (Sep 24) | | [S] [Meta recap](https://developers.meta.com/blog/meta-connect-recap/), [glasses recap](https://developers.meta.com/blog/meta-connect-recap-ai-glasses/), [Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-8-live-with-live-avatar-is-now-generally-available) |
| Sep 28 | Claude Sonnet 5.5 | | [M] Wikipedia, [LLM Gateway](https://llmgateway.io/timeline) |
| **Sep 29 (tomorrow)** | **OpenAI DevDay 2026** | Expect new realtime, agent and apps APIs; re-check | [M] [Fortune](https://fortune.com/2026/09/24/openai-launching-gpt-6-cyber-model-and-security-product-devday/) |

---

## 2. Unlock catalog (by category)

Each unlock covers: **what it is · date · link · app category it newly enables · saturation, with who has already built it · evidence strength.**

### A. Realtime conversational voice (full-duplex) at pennies per minute

**A1. OpenAI GPT-Live-1 (Sep 10, 2026)** [S] [changelog](https://developers.openai.com/api/docs/changelog); [M] [TestingCatalog](https://www.testingcatalog.com/openai-launches-gpt-live-1-for-full-duplex-voice-agents/); official post [openai.com/index/introducing-gpt-live](https://openai.com/index/introducing-gpt-live/) (returned 403 to my fetcher)
- **What:** A full-duplex speech model that listens and speaks at the same time. It handles interruptions, backchannels ("mm-hm") and changes of direction. It can **delegate** deeper reasoning or actions to backend models such as GPT-6 Astra or Codex.
  - Built-in telephony and 12 voices; custom voices require contacting sales.
  - Price is **$0.05/min billed per second**, plus backend model charges.
  - Early users: Yelp Host, Speak, Intercom Fin, Cognition's Devin. One customer reportedly cut 23,000 lines of voice code.
  - Vision input is **not mentioned**.
- **Newly enables:** Conversations where *timing* is the product. Examples: a tutor who interrupts at the right moment, a coach who backchannels, turn-taking for kids.
- **Saturation:** High for customer-service voice agents (Intercom, Yelp). High for language learning (Speak ships on it). Low to medium for consumer vertical coaches.

**A2. Google Gemini 3.8 Live and 3.8 Live Extended Thinking (Sep 15, 2026)** [S] [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/), [pricing](https://ai.google.dev/gemini-api/docs/pricing), [Live API docs](https://ai.google.dev/gemini-api/docs/live-api), [session docs](https://ai.google.dev/gemini-api/docs/live-session)
- **What:** Speech-to-speech with visual input processed "in near real-time." It **executes tools in the background while continuing the conversation** (async function calling). Extended Thinking narrates progress ("Let me check that…").
  - Supports 97 languages with automatic language switching.
  - Scores 82.6 on the Artificial Analysis S2S index and 97.7% on Big Bench Audio.
- **Developer specifics** [S]:
  - Input is 16 kHz PCM audio plus **JPEG frames at up to 1 fps**. **Ephemeral tokens** let a browser or phone connect directly.
  - Barge-in, proactive audio and affective dialog are supported.
  - **Limits:**
    - Audio-only sessions: 15 min.
    - **Audio+video sessions: 2 min** unless you enable context compression.
    - Connection lifetime: about 10 min.
    - Resumption tokens stay valid for 2 h.
  - **Price:** audio in $0.005/min, audio out $0.018/min, and **a free tier**.
- **Availability conflict:** The changelog lists `gemini-3.8-live-extended-thinking` as GA in the Gemini API. Google Cloud says Extended Thinking is private preview in Gemini Enterprise. Both can be true, since these are different surfaces. [S]
- **Newly enables:** Always-on camera-plus-voice copilots at roughly 2–4¢ per minute.
- **Saturation:** Medium to high for *generic* camera assistants.
  - Gemini Live already draws highlight boxes on the camera feed ("Guided Vision"; Pixel 10 since Aug 2025, expanding in 2026). [M] [Android Authority](https://www.androidauthority.com/gemini-live-guided-vision-2-3705480/), [Google, Aug 2025](https://blog.google/products-and-platforms/products/gemini/gemini-live-updates-august-2025/)
  - The **Gemini Live Agent Challenge** (Feb 16–Mar 16, 2026) had 11,878 participants and **1,536 submissions**. Winners included a surgical voice copilot, a drone copilot, a webcam electronics "lab partner" (Relay), a voice-controlled desktop navigator, and a 3D memory palace. [S] [Google Cloud](https://cloud.google.com/blog/topics/developers-practitioners/winners-and-highlights-of-the-gemini-live-agent-challenge)
  - A realtime workout-form coach ("Chaos Fit") was built for the same challenge. [M] [Medium](https://medium.com/@elisheba.t.anderson/chaos-fit-building-a-real-time-ai-workout-coach-with-gemini-live-dd595c3f97b6)

**A3. GPT-Realtime-2 / -Translate / -Whisper (May 7, 2026)** [S] OpenAI changelog; [M] [Latent Space](https://www.latent.space/p/ainews-gpt-realtime-2-translate-and)
- **What:** GPT-5-class reasoning inside a voice model, with 128K context (up from 32K), five reasoning levels, spoken preambles and tool transparency.
  - Time to first audio: 1.12 s at minimal reasoning, 2.33 s at high.
  - Audio pricing is unchanged: about $1.15/h in and $4.61/h out, which is roughly $0.019 and $0.077 per minute.
  - Translate: 70+ input languages to 13 output languages, $0.034/min. Whisper streaming: $0.017/min.
- **Saturation:** High in voice agents and live translation.

**A4. Open-source voice stacks** [M]
- Full-duplex: NVIDIA **PersonaPlex** (Feb 2026, built on Moshi, persona and voice-cloning prompts) and Kyutai "rl-seamless" RL post-trained variants (Jun 2026). [HF](https://huggingface.co/kyutai/personaplex-rl-seamless), [architecture review](https://ai.ksopyla.com/posts/voice-to-voice-models-2026-review/)
- Local speech-to-speech: **parlor** (Gemma 4 E2B with Kokoro TTS). It reaches first audio in about 0.7 s on an M3 Pro, but runs on a desktop, not a phone. [GitHub](https://github.com/fikrikarim/parlor) (HN 298 pts, Apr 2026)
- On-device voice pipeline: RunAnywhere (YC W26) [HN 240 pts](https://github.com/RunanywhereAI/rcli).
- Demand signal: "Ask HN: best local/open speech-to-speech setup?" (Jan 2026, 265 pts).
- **Engineering craft signals:**
  - "I built a sub-500ms latency voice agent from scratch" (HN 570 pts). Techniques: pipelining, pre-warmed TTS sockets, and instant cancellation on barge-in. [ntik.me](https://www.ntik.me/posts/voice-agent)
  - **Ello**, "Teaching a child in 1000 ms" (Jul 2026): a converser agent plus an async planner, pre-generated answer branches, and safety checks that gate *execution* rather than generation. [Ello](https://www.ello.com/blog/teaching-a-child-in-1000-ms)
- **Saturation:** Low for polished consumer apps built on open duplex models.

### B. Realtime video understanding and visual grounding

- **Gemini 3.8 Live** visual grounding (see A2). Its frame cap (1 fps) and 2-minute A/V session limit force real engineering: event-driven frames, compression and resumption. [S]
- **Agentic video understanding (Sep 1, 2026):** Flash-Lite models navigate long videos with dynamic timeline navigation. [S] [changelog](https://ai.google.dev/gemini-api/docs/changelog)
  - *Newly enables:* "Import from video" (recipes, tutorials, walkthroughs) and hour-long video Q&A at Flash-Lite prices.
- **Gemini Robotics-ER 1.6 (Apr 14) and ER 2 (Jul 30):** improved spatial reasoning with points and trajectories. [S] changelog.
  - *Inference:* usable to point at objects in phone frames for AR-style overlays.
- **Video billing:** 258 tokens per second at 1 fps, about 15.5K tokens per minute. [M] [Gemini token docs](https://ai.google.dev/gemini-api/docs/tokens)
- **Saturation:** "Point the camera and ask" is **high** (Gemini Live, ChatGPT voice with camera, Apple Visual Intelligence, Google Lens). *Vertical perception plus verification* is **low to medium** (inference).

### C. On-device and in-browser AI (phones, PWAs)

- **Gemma 4 (Apr 2, 2026)** [S] [Google](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/), [HF blog](https://huggingface.co/blog/gemma4)
  - E2B and E4B take **native audio input** plus image and video. 128K context on the edge models. Function calling and JSON output. Apache 2.0.
  - Runs on LiteRT-LM, llama.cpp, MLX, Ollama and others.
  - Community signals [M]: "Gemma 4 26B in 2 GB RAM on M-series Macs" (HN 919 pts, Jul 29); Cactus Hybrid, which teaches Gemma 4 "to know when it's wrong" for cloud fallback (HN 191 pts, Jul 22).
- **Needle / Needle 2 / Needle 3 (May 12, Aug 11, Sep 18)** [M]
  - Tool-calling models from 26M to 45M parameters. Needle 2 is a 14 MB binary that needs 28 MB RAM and runs at 300–1,500 tok/s on phones. Builds exist for **iOS, Android and WebAssembly**.
  - On BFCL v4 it scores 42.6%, against 61.7% for Apple's on-device model. It is strong on consumer device-action tasks.
  - HN reception: 776, 537 and 236 points. [MarkTechPost](https://www.marktechpost.com/2026/08/13/cactus-compute-needle-2-45m-parameter-tool-calling-model/), [HN](https://news.ycombinator.com/item?id=49246804)
- **Apple Foundation Models (WWDC, June 2026)** [S] [WWDC26 session](https://developer.apple.com/videos/play/wwdc2026/241/)
  - On-device context of **8,192 tokens**, image input, and OCR, barcode and Spotlight-RAG tools.
  - PCC server model with **32K context and reasoning levels**, free for apps under 2M first-time downloads.
  - A `LanguageModel` protocol with **Anthropic and Google Swift packages**. Dynamic Profiles for agentic mode switching, an **Evaluations framework**, and an open-source release.
  - **Swift-only for iOS**; the Python SDK and CLI are for macOS.
  - Hardware floor reportedly iPhone 15 Pro. [W] [ofox](https://ofox.ai/blog/apple-foundation-models-3-wwdc-2026-developer-read/)
- **Android on-device:** Gemini Nano 4 preview, ML Kit GenAI, Firebase AI Logic, plus the A2UI and AG-UI protocols in Android's generative-AI stack (I/O 2026). [S] [Android](https://android-developers.googleblog.com/2026/05/17-things-android-developers-google-io.html)
- **Chrome Prompt API** (Gemini Nano): multimodal image input from Chrome 148+. Audio is not yet exposed to JavaScript. [S/M] [Chrome docs](https://developer.chrome.com/docs/ai/prompt-api)
- **WebGPU everywhere:** Safari 26 (Sep 2025) ships WebGPU on **iOS 26**; Transformers.js, ONNX Runtime Web, Three.js and PlayCanvas all work. [S] [WebKit](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) Mobile GPU memory limits remain a constraint. [M]
- **Tiny TTS:** Kitten TTS under 25 MB (Mar 19). [M] [GitHub](https://github.com/KittenML/KittenTTS)
- **Newly enables:** Instant, offline and private PWAs; cascade routing (local model first, cheap cloud second); per-app tiny models distilled from frontier-model traces.
- **Saturation:** **Low** for consumer products built on these. Medium for local-LLM chat apps (LocalGPT HN 331 pts; Enclave).

### D. Transcription, translation and TTS

- `gpt-transcribe` and `gpt-live-transcribe` (Jul 28; free-form context, keyword hints). [S]
- `gemini-3.5-transcribe-live` (Aug 26): 4.0% streaming word error rate, custom vocabulary of up to 1,000 terms, code-switching. [S]
- **Gemini 3.8 Flash TTS** (Sep 22): **voice design and voice replication**, 150+ voices. [S]
- Meta Muse Voice Transcribe (Sep). [S]
- **Saturation: High.**
  - Notes and transcription: Otter, Granola, Plaud; Apple Watch **Siri Recap** in Sep 2026. [S] [TechCrunch](https://techcrunch.com/2026/09/09/apple-watchs-new-feature-listens-to-your-chats-and-recaps-them/)
  - Live translation: Google, Apple, Pixel, and Android XR glasses with "speaker-matched audio." [S] [Google](https://blog.google/products-and-platforms/platforms/android/android-xr-io-2026/)

### E. Computer and phone use, and OS-level agents

- **Frontier computer use:**
  - GPT-6 Astra (Sep 3–4). [S]
  - GPT-5.4 built-in computer use (Mar 5). [S]
  - Gemini 3.5 Flash computer use public preview (Jun 24). [S]
  - Claude Opus 5, state of the art on OSWorld 2.0 (Jul 24). [S]
- **Android:** AppFunctions (on-device MCP-style tools) and agent **UI automation** that needs no developer code.
  - Initial beta covers food delivery, grocery and rideshare, in the US and Korea, on Galaxy S26 and Pixel 10.
  - The Gemini integration is private preview behind an Early Access Program.
  - The Android 17 "Halo" agent-status layer is due later in 2026. [S] [Android](https://developer.android.com/blog/posts/the-intelligent-os-making-ai-agents-more-helpful-for-android-apps); [M] [TNW](https://thenextweb.com/news/google-gemini-spark-agentic-assistant-gmail-io-2026)
- **iOS 27:** App Intents 2.0 (streaming, multi-turn follow-ups) and **View Annotations** for on-screen awareness ("the third one"). [S] [WWDC26 App Intents](https://developer.apple.com/videos/play/wwdc2026/343/); [M] [heise](https://www.heise.de/en/news/iOS-27-Siri-finally-understands-what-s-on-the-screen-11338491.html)
- **Gemini Spark:** a 24/7 cloud agent on Gemini 3.5 Flash, in AI Ultra US beta. [M] [TNW](https://thenextweb.com/news/google-gemini-spark-agentic-assistant-gmail-io-2026)
  - Some aggregators describe Spark as an "on-device small model." This conflicts with the official description; trust the official one. [W]
- **Mobile agentic browsing:** Chrome auto-browse on Android (end of June), Comet for Android (Aug 19), and ChatGPT Atlas retired as a standalone app on Aug 9. [W] single aggregator: [tech-insider](https://tech-insider.org/ca/chatgpt-atlas-vs-perplexity-comet-vs-gemini-chrome-2026/)
- **Risk signal:** Google proposes restricting on-device ADB loopback after CVE-2026-0073. This threatens Shizuku- and ADB-based phone-agent tricks. [M] [blog](https://kitsumed.github.io/blog/posts/android-may-soon-restrict-on-device-adb/) (HN 1,010 pts)
- **Saturation:** **High** for generic phone task agents, which the platforms own and gate for third parties.

### F. Hosted agents and memory

- **Hosted agent infrastructure:**
  - **OpenAI Agents API** beta (Sep 10: durable sessions, hosted sandboxes). [S]
  - **Gemini Managed Agents** (May 19: one call provisions a remote Linux sandbox). [S]
  - **Claude Managed Agents with Memory** (Apr 23) and "Dreaming" consolidation (May). [S/M]
  - *Inference:* long-running background agents are now commodity infrastructure. Use them; don't sell them.
- **Consumer memory:**
  - Claude memory for all plans (Mar 2). [W/M]
  - Gemini Personal Intelligence (Jan 14) plus ChatGPT and Claude import tools (Mar 31). [M]
  - ChatGPT "Dreaming" (June). [W]
  - Apple Watch Siri Recap (Sep). [S]
  - Pendants: Bee (Amazon, $49.99), Plaud, Omi; Limitless was bought by Meta in Dec 2025 and discontinued. [M]
- **Personal agents:**
  - **OpenClaw**: 68k GitHub stars within weeks and "acquired by OpenAI" according to a16z. [M] [a16z](https://www.a16z.news/p/top-100-gen-ai-consumer-apps-march)
  - Manus, reportedly acquired by Meta for about $2B. Genspark at $100M run rate. [M]
- **Saturation: High.**

### G. Protocols and distribution surfaces

- **MCP Apps** (Jan 26) [S] [MCP blog](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)
  - Tools return `ui://` resources rendered in sandboxed iframes, talking JSON-RPC over `postMessage`.
  - Hosts: Claude (web and desktop), ChatGPT (now native MCP Apps), VS Code and Goose.
  - Formalized in the 2026-07-28 spec.
  - As of Sep 2026, support is "lacklustre and still catching up." [M] [Scott Logic](https://blog.scottlogic.com/2026/09/16/mcp-apps-your-ui-their-chat.html)
  - *Inference:* rendering in mobile chat clients is unconfirmed, so don't rely on it for the phone demo.
  - Fun proof of the surface: DOOM running as an MCP app (HN 93 pts).
- **WebMCP:** a W3C Community Group proposal. Chrome 146 early preview, then an origin trial for Chrome 149–156. The API was renamed to `document.modelContext` in Aug. [M]
  - As of May, mainstream agents weren't calling it. [W] [reality check](https://studiomeyer.io/en/blog/webmcp-reality-check-may-2026)
  - However, **Meta AI on glasses uses WebMCP** (developer preview). [S]
- **A2UI** (Google, Dec 2025) and **AG-UI**: agent-to-UI payload and runtime protocols, now referenced in Android's generative-AI stack. [S] [Google](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/)
- **Meta AI Connectors:** connect an API or MCP server so Meta AI can call it hands-free on glasses, web and the app. Early access. [S]
- **ChatGPT app directory:** 800–900M weekly users; only physical goods can be sold in-chat, and digital services must use external checkout. [M]
- **Saturation:** Low for high-quality *consumer* MCP Apps and glasses connectors. Medium for enterprise connectors (Asana, Figma, Canva, Slack).

### H. Wearables and glasses

- **Meta** [S] [build for display](https://developers.meta.com/blog/build-for-display-glasses/), [Connect glasses recap](https://developers.meta.com/blog/meta-connect-recap-ai-glasses/), [FAQ](https://developers.meta.com/wearables/faq/)
  - **Web Apps for Ray-Ban Display** (May 14): HTML/CSS/JS with motion and orientation data, phone GPS, Neural Band gestures and local storage. Share them via **password-protected URLs**.
  - Native **DAT** builds can go to up to 100 testers. **DAT 1.0** (stable) rolls out Sep 30 with camera capture, voice commands and "Hey Meta" invocation.
  - A Mock Device Kit and browser simulator mean hardware is optional.
  - Public discovery surfaces are "coming soon."
- **Meta hardware** [M] [VR.org](https://vr.org/articles/meta-glasses-three-tiers-wearables-toolkit-publishing-connect-2026): Ray-Ban Meta Gen 3 $449 (camera), Display $799, Audio $349 (no camera). The DAT device list isn't yet updated for the new models.
- **Android XR:** audio glasses launch in fall 2026 (Samsung, Gentle Monster, Warby Parker), with display glasses to follow. Jetpack Projected and Glimmer. SDK DP4 (May 19) with a Geospatial API plus Gemini Live API for "audio-guided walking tours." [S] [DP4](https://android-developers.googleblog.com/2026/05/android-xr-sdk-developer-preview-4-updates.html)
- **Snap Specs:** $2,195, shipping fall 2026. [M]
- **Backlash (strong signal):**
  - Meta glasses privacy story (HN 1,448 pts, Mar). [BBC, Apr](https://www.bbc.com/news/articles/c5y7yvgy0w6o)
  - German criminal complaint. [Reuters, Aug](https://www.reuters.com/legal/government/german-advocacy-group-lodges-criminal-complaint-over-meta-ai-glasses-2026-08-12/)
  - US police concerns. [Guardian, Sep](https://www.theguardian.com/technology/2026/sep/08/us-law-enforcement-meta-smart-glasses)
  - Philadelphia courts ban smart glasses (Mar), and the "ZuckOff" glasses-detector app. [Wired ME, Sep](https://www.wired.me/story/meta-smart-glasses-detector-app-zuckoff) [S]
- **Saturation: Low.** No "Ray-Ban Display" developer posts above 20 points on HN in 2026 [M]. Risks are hardware cost, social acceptability, and publishing gates. Avoid face recognition entirely.

### I. Generative media

- **Images:**
  - **GPT Image 2** (Apr 21) with near-perfect text rendering and multi-turn edits. [M/S]
  - GPT Image 2.5 (Sep 8; sketch-to-image). [S]
  - **Nano Banana 2** (Feb 26), about $0.067 per image. [S]
- **Video:**
  - **Gemini Omni** (May 19): any input to physics-aware video you can edit conversationally. API preview Jun 30, 1.1 GA Aug 27, about $0.10 per second of output. [S] [Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/)
  - Sora 2 API upgrades (Mar 12). [S]
- **Music:** Lyria 3 (Mar 25) and **Lyria 3.5** (Sep 3), with full songs at **$0.08 per song**. [S]
- **Avatars:** Gemini 3.8 Live **Avatar** (Sep 24): lip-synced avatars in 97 languages. Custom avatars are enterprise-allowlisted. [S]
- **Saturation: High.** a16z reports standalone image-generation apps contracting as ChatGPT and Gemini bundled image generation; Midjourney fell from the top 10 to #46. CapCut and Canva dominate. [S] [a16z](https://www.a16z.news/p/top-100-gen-ai-consumer-apps-march)

### J. 3D and world models

- **Project Genie** (Jan 29): Genie 3 at 720p/24 fps, AI Ultra only, **no API**. [S]
- **World Labs Atlas** (Sep 1): an omni world model producing 1-minute 1440p video, depth and Gaussian splats. Early access only. [S]
- **NVIDIA SANA-WM** (May): an open 2.6B world model, 1-minute 720p video. [M] [NVlabs](https://nvlabs.github.io/Sana/WM/)
- **Single-image 3D:**
  - Apple SHARP (Dec 2025) now **runs in the browser via ONNX Runtime Web** (Show HN, May 3, 2026). [M] [GitHub](https://github.com/bring-shrubbery/ml-sharp-web)
  - SAM 3D (Nov 2025). [M]
  - TRELLIS.2 (Dec 2025, MIT license) and Hunyuan3D. [M]
- **Gaussian splats are culturally hot on HN:** the A$AP Rocky video (772 pts), a splat strawberry (530), splat-to-videogame (236). [M]
- **Saturation:** Low to medium for *useful* consumer apps; high novelty. World-model APIs are gated.

### K. Frontier and open-weights models, and the price floor

| Model (date) | Price per 1M tokens (in/out) | Notes | Evidence |
|---|---|---|---|
| GPT-6 Luna (Sep 22) | **$0.10 / $0.50** (cached $0.01) | Text and image input; the new API price floor | [S] OpenAI changelog |
| GPT-6 Sol (Sep 22) | $2 / $10 | | [S] |
| GPT-6 Astra (Sep 3) | not stated in the sources read | Computer use; "generational leap" | [S] press |
| Gemini 3.8 Flash (Sep 2) | $0.75 / $3.75 (intro through Dec 31, 2026; doubles Jan 1) | Free tier available | [S] pricing; [W] doubling claim |
| Gemini 3.5 Flash-Lite (Jul 21) | $0.30 / $2.50 | Free tier | [S] |
| Claude Opus 5 (Jul 24) | $5 / $25 | Effort control; memory self-management | [S] |
| Claude Opus 5.5 (Sep 22) | reportedly $4 / $20 | | [W] aggregator |
| DeepSeek V4 Flash / Pro (Apr 24; Flash-0731) | about $0.14/$0.28 and $0.435/$0.87 | Open weights, 1M context | [S] release; [M] prices |
| Muse Spark 1.3 (Sep) | reportedly about $0.10 blended | Meta Model API now GA | [S] release; [W] price |
| Kimi K3 (Jul 16), MiMo v2.6 (Sep 21), GLM-5.3, Qwen3.8 | cheap open weights | | [W/M] [local-ai-zone](https://local-ai-zone.github.io/blog/September_2026_AI_Model_Updates.html) |

- **Inference:** At $0.10–$0.75 per M input tokens, one "is this step correct?" call costs about $0.0001–$0.001. That is small enough to run per event or per keyframe inside a consumer app.

### L. Multimodal embeddings and retrieval

- **gemini-embedding-2** (preview Mar 10, **GA Apr 22**). One space for text ($0.20/M), images ($0.00012 each), audio ($0.00016/s) and **video ($0.00079 per frame)**. [S] [pricing](https://ai.google.dev/gemini-api/docs/pricing)
- **File Search goes multimodal** (May 5). [S]
- **Newly enables:** Cheap "search my space or footage by meaning" with no custom vision pipeline.
- **Saturation:** Photo-library search is high (Google and Apple Photos). Retrieval over *your physical space* is low to medium.

---

## 3. Price and latency cheat-sheet (what is newly practical)

| Capability | 2026 price or latency | Source |
|---|---|---|
| Full-duplex voice (GPT-Live-1) | **$0.05/min**, billed per second, plus backend model | [S] OpenAI changelog |
| Voice with vision (Gemini 3.8 Live) | audio **$0.005/min in, $0.018/min out**; frames at 1 fps; **free tier** | [S] pricing |
| Reasoning voice (GPT-Realtime-2) | about $0.019/min in, $0.077/min out; time to first audio 1.1–2.3 s | [M] Latent Space |
| Live translate / streaming STT | $0.034/min / $0.017/min | [M/S] |
| Cheapest capable LLM | GPT-6 Luna $0.10 / $0.50 per M | [S] |
| Multimodal embedding of video | $0.00079 per frame | [S] |
| Image edit / video gen / song | $0.067 per image / about $0.10 per second / $0.08 per song | [S] |
| On-device tool calling | Needle 2: 14 MB, 300–1,500 tok/s on phones | [M] |
| On-device voice loop | about 0.7–1.4 s to first audio (Gemma 4 E2B on an M3 Pro, not a phone) | [M] parlor |

**Worked example (inference):** A 20-minute Gemini 3.8 Live tutoring session.
- With continuous 1-fps video:
  - Video: 15.5K tokens/min × 20 min at an assumed $0.75/M ≈ **$0.23**.
  - Audio in: 20 min × $0.005 = **$0.10**.
  - Audio out, if the model speaks 25% of the time: 5 min × $0.018 = **$0.09**.
  - Total ≈ **$0.42 per session**.
- With event-driven frames, sending about 10% of frames only when something changes, the total falls to about **$0.21**.
- On GPT-Live-1 the same session costs about **$1.00** plus backend reasoning.
- Assumptions to verify: the video token rate for Live models, and whether accumulated context is re-billed each turn.

---

## 4. Saturation map (avoid vs. open)

| Lane | Saturation | Evidence |
|---|---|---|
| Generic "point camera and ask" assistant | **High** | Gemini Live Guided Vision [M]; ChatGPT, Apple Visual Intelligence and Lens (background); 1,536 Gemini Live Agent Challenge entries [S] |
| 24/7 personal agent / "does tasks for you" | **High** | OpenClaw, Manus, Genspark [M]; Gemini Spark [M]; Claude Cowork Dispatch [M]; OpenAI, Gemini and Claude hosted agents [S] |
| Memory, lifelogging, meeting notes | **High** | Siri Recap [S]; ChatGPT Dreaming [W]; Claude and Gemini memory [M]; Bee, Plaud, Omi [M] |
| Live translation | **High** | GPT-Realtime-Translate [S]; Android XR glasses translation [S]; Apple and Pixel (background) |
| Language tutors | **High** | Speak runs on GPT-Live-1 [M]; Duolingo and Praktika (background) |
| Kids' reading and math tutors | **Medium–High** | Ello's realtime tutor for ages 4–9 [M]; Bloomy (YC S26) [M]; "tutoring company tells parents to use AI instead" (HN, Sep) [M] |
| Mobile agentic browsing and phone task automation | **High** (platform-owned) | Chrome auto-browse on Android and Comet Android [W]; AppFunctions and UI automation [S] |
| Image, video or music generation apps | **High** | a16z contraction data [S] |
| Phone-calling agents | **High**, and overlaps the planned Bland gateway | GPT-Live-1 telephony; Yelp Host [M] |
| Vertical realtime coach **with a verifier** (math steps, lifts, music) | **Low–Medium** | Hackathon-level demos only (Chaos Fit, Relay) [M]; no shipped verifier-grade products found (inference) |
| Hybrid on-device/cloud action apps as PWAs | **Low–Medium** | Strong dev interest (Needle HN 776/537) but few products (inference) |
| Glasses web apps and Meta AI Connectors | **Low** | Opened May–Sep 2026 [S]; no HN developer activity [M] |
| Multimodal "memory of my space" retrieval | **Low–Medium** | Astra demo (2024, background); photo search is saturated |

---

## 5. Builder constraints for this developer (inference unless noted)

- **No Mac:** Apple Foundation Models is Swift-only [S], and native iOS development needs Xcode. **Build a PWA**:
  - Camera via `getUserMedia`, WebSocket or WebRTC to the Live APIs with **ephemeral tokens** [S], and WebGPU on iOS 26 [S].
  - It runs on iPhone and Android, and the *same web app* can target **Meta Ray-Ban Display Web Apps** [S].
  - Android-native Kotlin is a viable second target for AppFunctions or Gemini Nano.
  - Expo EAS can build iOS in the cloud but complicates debugging on-device native modules (background knowledge).
- **RTX 5070 8 GB:** Enough to run Gemma 4 E2B/E4B locally with llama.cpp for development, and to **LoRA fine-tune or distill a tiny task model** (step classifier, tool caller) with Unsloth. The distillation story ("we distilled Gemini tool calling into 26M params") is a proven Hacker News magnet [M].
- **Cost:** Development can be close to $0 using Gemini Live and Flash free tiers [S]; check the free-tier data-use terms. GPT-Live-1 is paid-only.
- **Live API gotchas that double as depth:**
  - The 2-minute A/V session cap and roughly 10-minute connection lifetime require context compression, resumption tokens and reconnects [S].
  - Frames are capped at 1 fps [S].
  - GPT-Live-1 has no documented vision input [M], so camera products either need Gemini Live or a split design (vision pipeline → text events → voice model).
- **Recommended architecture pattern (inference): "Perception → Events → Conversation."**
  1. Cheap on-device detectors (ink change, pose and reps, step completion, audio onsets) decide *when* something happened.
  2. A cheap VLM or LLM on keyframes decides *what* happened, as structured output.
  3. A deterministic **verifier** (CAS, kinematics, score alignment) decides whether it is *right*.
  4. The full-duplex voice layer speaks only on verified events.

  This addresses cost, session limits and hallucinated corrections, and it yields event-level evals. It is what separates a product from an API wrapper.

---

## 6. Project seeds (10), "only possible in 2026"

*The scores and saturation calls below are inference, backed by the evidence above.*

### Seed 1: "Margin", an over-the-shoulder tutor that verifies every handwritten step
- **Pitch:** Prop your phone over your notebook. A full-duplex voice tutor watches you work and speaks up **only when a step is actually wrong**, and each step is checked symbolically first.
- **10-second demo:** Write `3(x+2)=12`, then `3x+2=12`. Before you finish the next line, the phone says "hold on, distribute the 3 to both terms" and a red box snaps around line 2. Interrupt with "wait, why?" and it answers mid-sentence.
- **Why useful:** Nightly problem sets. The builder is the target user and can recruit classmates for real usage. It can pull assignments through the existing Canvas-LMS MCP.
- **Technical depth:**
  - An on-device ink-change detector (page rectification and frame differencing in WebGPU/WASM), so frames go out only when new work appears.
  - A VLM that turns handwriting into LaTeX with per-line bounding boxes.
  - A **SymPy step-equivalence verifier** as a neuro-symbolic guardrail, so the tutor never "corrects" a correct step.
  - A tuned interruption policy.
  - Long-session management: compression, resumption and reconnect.
  - An **eval set** of worked solutions with injected errors, measuring precision, recall, time-to-flag and cost per session.
- **2026 unlocks:** Gemini 3.8 Live (visual grounding, async tools, free tier) and/or GPT-Live-1 duplex; GPT-6 Luna or Flash-Lite for cheap OCR and reasoning; WebGPU on iOS.
- **Saturation: Medium.**
  - Snap-and-solve is saturated (Photomath, Gauth, ChatGPT Study Mode, Gemini Guided Learning; background knowledge).
  - AI tutoring is hot (Bloomy, Ello, and a Dartmouth AI-tutor study at 0.71–1.30 SD, HN Jul 2026).
  - OpenAI and Khan Academy demoed a live GPT-4o tutor in May 2024 (background).
  - A shipped, verified "watch my paper" tutor was not found; HN has no handwriting-tutor hits.
- **Main risk:** Messy handwriting, glare and camera angle; scope creep beyond algebra and intro calculus; academic-integrity optics, so ship it hints-only.

### Seed 2: "Spotter", a camera auto-logging strength tracker
- **Pitch:** Lean your phone against a plate and lift. It logs exercise, reps, load and bar speed automatically, and talks only when form breaks.
- **10-second demo:** Do 5 squats and a card slides up: "Back squat · 5 reps · 135 lb (plates read) · depth ✓ · rep 4 slowed 22%." Say "that was 185" and it fixes the log mid-set.
- **Why useful:** Lifters log every set, and the popular loggers (Strong, Hevy) are manual (background knowledge).
- **Technical depth:**
  - 30-fps on-device pose estimation in the browser, with rep segmentation from joint-angle time series.
  - A cloud VLM *only on keyframes*, for exercise ID and plate or dumbbell reading, with hybrid routing and cost tracking.
  - Offline-first sync.
  - An eval harness on recorded sets: rep-count error, exercise-ID accuracy, load-read accuracy.
- **2026 unlocks:** WebGPU on iOS 26; Flash-Lite at $0.30/M or GPT-6 Luna; Gemma 4 E2B as an on-device fallback; realtime voice at pennies per minute.
- **Saturation: Medium.** Form-coach demos are common (Chaos Fit). Auto-logging including *load recognition* is uncommon (inference).
- **Main risk:** Occlusion and camera angle; gym filming etiquette; the temptation to become a full "AI trainer."

### Seed 3: "Airplane Mode", an offline-first voice-to-action agent
- **Pitch:** Say it and it's done: expenses, bill splits, lists, reminders. It is parsed **on-device in a few hundred ms** by a 14 MB tool caller and escalates to the cloud only when unsure.
- **10-second demo:** Turn airplane mode on and say "Paid 42 for dinner with Sam and Priya, split it." The split card appears instantly. Turn the network back on, and it syncs and drafts payment requests.
- **Why useful:** Daily quick capture that is private by default.
- **Technical depth:**
  - WASM/WebGPU inference plus on-device STT, with schema-constrained decoding.
  - **Calibrated confidence plus a cascade router**: local model first, then GPT-6 Luna or Flash-Lite.
  - **Distilling a task-specific tiny model on the RTX 5070** from frontier-model traces.
  - An eval dashboard charting accuracy against latency and cost.
  - Local-first CRDT sync.
  - An optional MCP server plus MCP App so Claude or ChatGPT can query the ledger.
- **2026 unlocks:** Needle 2 (Aug); Gemma 4 E2B audio input (Apr); Kitten TTS (Mar); WebGPU on iOS; GPT-6 Luna (Sep).
- **Saturation: Low–Medium.** OS assistants are moving this way (App Intents 2.0, AppFunctions) but are gated; few third-party on-device tool-calling apps exist (inference).
- **Main risk:** The "wow" is subtler (lean on the airplane-mode moment); iPhone WebGPU memory ceilings; accuracy on unusual phrasings.

### Seed 4: "Mise", a hands-free cooking copilot (phone now, glasses-ready)
- **Pitch:** Paste or film any recipe. It becomes a timed step graph plus a full-duplex sous-chef that watches your cutting board, runs parallel timers, and replans when things go wrong.
- **10-second demo:** Mid-sentence, say "wait, I burned the garlic." It stops instantly, replans, and two on-screen timers rebalance.
- **Why useful:** Nightly for home cooks.
- **Technical depth:**
  - A recipe-to-DAG compiler with validation.
  - A realtime state machine, a multi-timer scheduler and barge-in handling.
  - Vision checks for step completion at up to 1 fps.
  - **Import from video** via agentic video understanding.
  - Session-replay evals.
  - The same codebase ships as a Meta Ray-Ban Display Web App.
- **2026 unlocks:** GPT-Live-1 or Gemini 3.8 Live async tools; agentic video understanding (Sep 1); Display Web Apps (May 14) and DAT 1.0 (Sep 30).
- **Saturation: Medium–High.** Gemini Live coaches cooking generically, there are many recipe apps, and Meta itself lists "cooking guides" as a target glasses use case [S].
- **Main risk:** Differentiating from Gemini Live; kitchen noise; reliable step detection.

### Seed 5: "Walkthrough", talk-and-point condition reports (the FDE-flavored seed)
- **Pitch:** Walk a room talking. It fills a structured condition report with cropped evidence photos, severities and timestamps, and exports a PDF for your landlord.
- **10-second demo:** Pan across a wall and say "scuff here." A row appears live with the cropped scuff and "Minor · Living room · East wall."
- **Why useful:** Renters protecting deposits, small landlords, Airbnb hosts. It generalizes to field inspections, which is the classic forward-deployed-engineer (FDE) pattern.
- **Technical depth:**
  - Streaming multimodal input into **schema-constrained form filling**.
  - Keyframe selection and evidence linking, with deduplication via multimodal embeddings.
  - An offline upload queue and human-in-the-loop edits.
  - Evals on labeled walkthrough videos.
- **2026 unlocks:** Gemini 3.8 Live (video plus async tools); gemini-embedding-2; DAT 1.0 for point-of-view capture; Meta AI Connectors.
- **Saturation: Medium** for inspection SaaS (inference); **Low** on glasses.
- **Main risk:** Not a daily use for most people; credibility needs a real design partner (which is also the FDE story).

### Seed 6: "Findr", a spatial memory for your stuff
- **Pitch:** Do a 60-second walk-through video. Later ask "where's my passport?" and see the exact frame with the object circled.
- **10-second demo:** A voice query jumps to a frame and highlights the object: "bedroom desk, second drawer, seen Tuesday 9:12 PM."
- **Why useful:** Finding things; a home inventory for insurance or moving.
- **Technical depth:**
  - Video ingestion: keyframes plus blur and duplicate filtering.
  - Multimodal embeddings, VLM captions and open-vocabulary localization.
  - Reranking and temporal "object moved" updates.
  - Retrieval evals (recall@k).
- **2026 unlocks:** gemini-embedding-2 (video at $0.00079 per frame); multimodal File Search; agentic video understanding; SAM 3 (Nov 2025).
- **Saturation: Low–Medium.** Project Astra showed "where did I leave my glasses" in 2024 (background), and photo search is saturated.
- **Main risk:** Habit (it needs rescans) and staleness; privacy of home video.

### Seed 7: "Encore", an instrument practice coach
- **Pitch:** Play a passage. It follows the score, paints mistakes on the sheet, and a voice coach names the *one* thing to fix next.
- **10-second demo:** Play 8 bars and the notes turn red or green within a second: "bar 5, you rushed the triplet, try 80 bpm." A metronome starts.
- **Why useful:** Daily practice for music students.
- **Technical depth:**
  - Realtime onset and pitch DSP in WebAudio/WASM.
  - **Online dynamic-time-warping score following**.
  - LLM feedback grounded in alignment data.
  - Longitudinal practice memory.
  - Evals by synthetic error injection.
- **2026 unlocks:** Cheap reasoning plus duplex voice. On-device music models are proven practical (HN: a 125M on-device piano model, 598 pts, Aug 2026). WebGPU on iOS.
- **Saturation: Medium.** Yousician and Simply Piano detect notes; LLM coaching is rare (inference).
- **Main risk:** Polyphonic detection through phone mics; a smaller audience.

### Seed 8: "Babel Table", a multi-party live interpretation room
- **Pitch:** Everyone joins by QR code and hears everyone else in their own language, with a shared live transcript.
- **10-second demo:** Two phones. Speak Spanish into one, and the other speaks English about a second later.
- **Why useful:** International students and families, clinics, group travel.
- **Technical depth:** WebRTC fan-out, per-listener translation streams, diarization, latency and cost budgets, consented voice replication.
- **2026 unlocks:** GPT-Realtime-Translate ($0.034/min); Gemini Transcribe Live; Gemini TTS voice replication.
- **Saturation: High.** Google, Apple, Pixel, Meta and Android XR all ship live translation, and Microsoft Translator has had multi-device conversations since the 2010s (background).
- **Main risk:** It is a commodity next to platform features.

### Seed 9: "Spin", one photo to a 3D marketplace listing
- **Pitch:** Snap an item and get a spinnable 3D splat plus an auto-written listing with price comparisons, shareable as a link.
- **10-second demo:** Snap a sneaker; within about 5 seconds you're spinning it in 3D, and listing text plus a price appear.
- **Why useful:** Weekly for student resellers and marketplace sellers.
- **Technical depth:**
  - In-browser single-image-to-splat inference (SHARP via ONNX Runtime Web on WebGPU).
  - Splat compression and streaming, plus background cleanup.
  - A pricing agent using web search.
  - Share pages with Open Graph previews.
- **2026 unlocks:** SHARP running in the browser (May 2026); WebGPU on iOS; Nano Banana 2 or GPT Image 2 for cleanup; cheap LLMs.
- **Saturation: Medium.** Polycam, Luma and KIRI do multi-view capture, and marketplaces have 3D viewers (background).
- **Main risk:** Hallucinated back sides; marketplaces won't embed the 3D model; cool but not daily.

### Seed 10: "Read With Me", a read-aloud buddy for kids
- **Pitch:** A child reads a real book aloud. The phone follows along, backchannels "mm-hm," helps with hard words at the right moment, and tracks fluency.
- **10-second demo:** The child stumbles on "enormous." The phone gently models the word and highlights it on a page overlay.
- **Why useful:** Daily for families and teachers.
- **Technical depth:** Page OCR plus forced alignment against streaming ASR, miscue detection, a backchannel and turn-taking policy, robustness to child speech, and miscue precision/recall evals.
- **2026 unlocks:** Full-duplex voice (GPT-Live-1; open PersonaPlex "seamless" models); streaming ASR with custom vocabulary (Aug).
- **Saturation: Medium–High.** Ello [M], plus Amira, Microsoft Reading Coach and Google Read Along (background).
- **Main risk:** COPPA and child data; strong incumbents; testing with children.

### Scoring matrix (inference; 5 = best)

| Seed | Wow in 10 s | Live phone demo | Daily use | Eng depth | Recruiter signal | Ships in 3–6 wk | Saturation |
|---|---|---|---|---|---|---|---|
| 1 Margin (verified tutor) | 5 | 5 | 4 | **5** | **5** | 4 | M |
| 2 Spotter (auto-log lifts) | 5 | 5 | 4 | 4 | 4 | 4 | M |
| 3 Airplane Mode (on-device actions) | 3 | 5 | **5** | **5** | **5** | 4 | L–M |
| 4 Mise (cooking copilot) | 4 | 5 | 4 | 4 | 4 | 4 | M–H |
| 5 Walkthrough (inspection reports) | 4 | 5 | 2 | 4 | 5 (FDE) | 4 | M |
| 6 Findr (spatial memory) | 5 | 5 | 2 | 4 | 4 | 4 | L–M |
| 7 Encore (music coach) | 4 | 5 | 4 | 5 | 4 | 3 | M |
| 8 Babel Table (interpretation) | 4 | 5 | 2 | 4 | 3 | 4 | H |
| 9 Spin (photo to 3D listing) | 5 | 5 | 2 | 4 | 4 | 3 | M |
| 10 Read With Me (kids) | 4 | 5 | 4 | 4 | 3 | 3 | M–H |

**Shortlist (inference):** Seed 1 (Margin), Seed 2 (Spotter), Seed 3 (Airplane Mode). Seeds 1 and 2 can reuse Seed 3's hybrid on-device engine as internal infrastructure, which yields one flagship product with a deep technical story.

---

## 7. Top 3 takeaways for picking the project

1. **Build on the realtime voice-plus-vision unlock, but add a verifier.** Duplex voice at $0.05/min (GPT-Live-1) and voice plus vision at about 2–4¢/min with a free tier (Gemini 3.8 Live) are the 2026 unlocks that deliver a 10-second phone "wow." The *generic* camera assistant is already a platform feature and a hackathon cliché (1,536 entries). Pick one narrow daily workflow and add a **deterministic verifier** (CAS, kinematics, score alignment) plus an **eval harness**. That turns "wrapper" into "engineering."
2. **Architect "perception → events → conversation" with hybrid on-device/cloud, shipped as a PWA.** WebGPU on iOS 26, Gemma 4 E2B and 14 MB Needle-class models decide *when* something happened. GPT-6 Luna or Flash-Lite ($0.10–$0.30/M) decides *what* happened. The voice layer speaks only on verified events. This gets around Live API limits (2-minute A/V sessions, about 10-minute connections), cuts cost 2–5× (inference), and gives measurable evals. The RTX 5070 is enough to distill a tiny task model, a proven HN-magnet story. No Mac is needed.
3. **Avoid the crowded lanes, and use new surfaces as a bonus layer only.**
   - Crowded: personal 24/7 agents, memory and lifelogging, translation, language tutors, agentic browsers, generative-media apps, and phone-calling agents (which also overlap the Bland gateway).
   - Bonus layer: the same web app on **Meta Ray-Ban Display (Web Apps; DAT 1.0 from Sep 30)** and inside **ChatGPT/Claude via MCP Apps**. These are low-saturation and highly novel to recruiters, but gated and hardware-dependent, so never the only demo path.
   - **Re-check after OpenAI DevDay (Sep 29).**

---

## 8. Watch list (next 2–8 weeks)

- **OpenAI DevDay, Sep 29:** possible vision for GPT-Live, realtime video, Agents API GA, Apps SDK or MCP changes, and a GPT-6 Cyber model. [M] [Fortune](https://fortune.com/2026/09/24/openai-launching-gpt-6-cyber-model-and-security-product-devday/)
- **Meta DAT 1.0 rollout (Sep 30)**, the timing of the public discovery surfaces, and Meta's $1M Global AI Developer Hackathon (free Model API credits), which is a possible submission venue. [S] [Meta recap](https://developers.meta.com/blog/meta-connect-recap/)
- **Android XR audio glasses (fall 2026)** and the **Android 17 Halo** agent surface; opening of AppFunctions early access. [S]
- **WebMCP origin trial (Chrome 149–156)** and whether any major agent starts calling it. [M]
- **The Foundation Models open-source release** could let Swift-on-Linux run PCC-style sessions server-side. [S]
- Reported **OpenAI hardware delay to 2027** (Wired, via search summary; not verified) [W]. OpenAI bought camera maker Glass Imaging for $300M (Sep 14). [M] [TechCrunch](https://techcrunch.com/2026/09/14/openai-buys-smartphone-camera-maker-glass-imaging-for-300-million-report-says/)

## 9. Conflicts and low-confidence claims

- **Gemini Spark:** Some blogs call it an on-device small model with sub-50 ms latency (MindStudio, aggregators). Official and tier-1 coverage describes a **24/7 cloud agent on Gemini 3.5 Flash**. Trust the latter.
- **Gemini 3.8 Live Extended Thinking:** GA in the Gemini API per the changelog, but private preview in Gemini Enterprise per Google Cloud. Surface-dependent.
- **Unverified numbers:**
  - GPT-6 Astra "1.05M context" (SEO blog).
  - Opus 5.5 at $4/$20 and Muse Spark 1.3 at $0.10 blended (aggregator).
  - Gemini 3.8 Flash "doubles Jan 1, 2027" (aggregator; the official page only says the intro price runs through 12/31/26).
- **Apple "AFM 3 Core Advanced, 20B sparse"** comes from a third-party blog. The official WWDC session only confirms 8,192 tokens on-device and 32K on PCC.
- **ChatGPT Atlas shutdown (Aug 9), Comet Android (Aug 19), Chrome auto-browse on Android (June):** each from a single aggregator.
- **Qwen3.5-Omni** open-weight status is unconfirmed. **Kimi K3** at 2.8T parameters comes from aggregators.
- **Live API video pricing:** I assumed video input bills at the $0.75/M text/image rate for Live models. Verify, and also verify whether accumulated context is re-billed each turn.

## 10. Source index (primary sources first)

- **Changelogs and pricing:**
  - [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog)
  - [OpenAI API changelog](https://developers.openai.com/api/docs/changelog)
  - [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
  - [Live API](https://ai.google.dev/gemini-api/docs/live-api) and [sessions](https://ai.google.dev/gemini-api/docs/live-session)
- **Google:**
  - [I/O 2026: 100 announcements](https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/)
  - [Developer keynote](https://developers.googleblog.com/all-the-news-from-the-google-io-2026-developer-keynote/)
  - [Gemini 3.8 Live](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/)
  - [Gemini audio for developers](https://blog.google/innovation-and-ai/technology/developers-tools/build-real-time-voice-applications-gemini-audio/)
  - [Live Avatar](https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-8-live-with-live-avatar-is-now-generally-available)
  - [Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)
  - [Gemini Omni](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/)
  - [Project Genie](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/)
  - [Android XR eyewear](https://blog.google/products-and-platforms/platforms/android/android-xr-io-2026/)
  - [Android XR DP4](https://android-developers.googleblog.com/2026/05/android-xr-sdk-developer-preview-4-updates.html)
  - [17 Android things](https://android-developers.googleblog.com/2026/05/17-things-android-developers-google-io.html)
  - [Intelligent OS / AppFunctions](https://developer.android.com/blog/posts/the-intelligent-os-making-ai-agents-more-helpful-for-android-apps)
  - [Gemini Live Agent Challenge winners](https://cloud.google.com/blog/topics/developers-practitioners/winners-and-highlights-of-the-gemini-live-agent-challenge)
  - [Chrome Prompt API](https://developer.chrome.com/docs/ai/prompt-api)
  - [A2UI](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/)
- **OpenAI:**
  - [GPT-Live](https://openai.com/index/introducing-gpt-live/)
  - [Voice models, May](https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/)
  - [GPT-6 Astra (CNBC)](https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html)
  - [Fortune](https://fortune.com/2026/09/03/openai-debuts-gpt-6-astra-computer-use-greg-brockman-says-start-of-agi/)
  - [GPT Image 2](https://developers.openai.com/api/docs/models/gpt-image-2)
- **Anthropic:**
  - [Claude Opus 5](https://www.anthropic.com/news/claude-opus-5)
  - [Managed Agents memory](https://claude.com/blog/claude-managed-agents-memory)
  - [Managed Agents docs](https://platform.claude.com/docs/en/managed-agents/overview)
- **Apple:**
  - [WWDC26 Foundation Models](https://developer.apple.com/videos/play/wwdc2026/241/)
  - [WWDC26 App Intents](https://developer.apple.com/videos/play/wwdc2026/343/)
  - [MacRumors SOTU](https://www.macrumors.com/2026/06/09/apple-outlines-major-ai-and-developer-tool-updates/)
  - [WebKit Safari 26 (WebGPU)](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/)
  - [Siri Recap (TechCrunch)](https://techcrunch.com/2026/09/09/apple-watchs-new-feature-listens-to-your-chats-and-recaps-them/)
- **Meta:**
  - [Build for display glasses](https://developers.meta.com/blog/build-for-display-glasses/)
  - [Connect recap](https://developers.meta.com/blog/meta-connect-recap/)
  - [Glasses recap](https://developers.meta.com/blog/meta-connect-recap-ai-glasses/)
  - [Wearables FAQ](https://developers.meta.com/wearables/faq/)
  - [Muse Spark](https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/)
- **Protocols:**
  - [MCP Apps](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)
  - [MCP Apps status, Sep 2026](https://blog.scottlogic.com/2026/09/16/mcp-apps-your-ui-their-chat.html)
  - [WebMCP state, Jul 2026](https://www.spronta.com/blog/state-of-webmcp-july-2026/)
- **Open and on-device:**
  - [DeepSeek V4](https://api-docs.deepseek.com/news/news260424/)
  - [Needle 2](https://www.marktechpost.com/2026/08/13/cactus-compute-needle-2-45m-parameter-tool-calling-model/)
  - [Kitten TTS](https://github.com/KittenML/KittenTTS)
  - [parlor](https://github.com/fikrikarim/parlor)
  - [ml-sharp-web](https://github.com/bring-shrubbery/ml-sharp-web)
  - [PersonaPlex seamless](https://huggingface.co/kyutai/personaplex-rl-seamless)
  - [World Labs Atlas](https://www.worldlabs.ai/blog/atlas)
  - [SANA-WM](https://nvlabs.github.io/Sana/WM/)
- **Market and saturation:**
  - [a16z Top 100, Mar 2026](https://www.a16z.news/p/top-100-gen-ai-consumer-apps-march)
  - [OpenClaw](https://en.wikipedia.org/wiki/OpenClaw)
  - [Ello realtime tutor](https://www.ello.com/blog/teaching-a-child-in-1000-ms)
  - [Sub-500 ms voice agent](https://www.ntik.me/posts/voice-agent)
  - [S2S architectures 2026](https://ai.ksopyla.com/posts/voice-to-voice-models-2026-review/)
  - [Guided Vision](https://www.androidauthority.com/gemini-live-guided-vision-2-3705480/)
  - [ADB restriction](https://kitsumed.github.io/blog/posts/android-may-soon-restrict-on-device-adb/)
  - [AI pendants 2026](https://www.layer3labs.io/guides/best-ai-wearable-pendants-2026)
  - Glasses backlash: [BBC](https://www.bbc.com/news/articles/c5y7yvgy0w6o), [Reuters](https://www.reuters.com/legal/government/german-advocacy-group-lodges-criminal-complaint-over-meta-ai-glasses-2026-08-12/), [Guardian](https://www.theguardian.com/technology/2026/sep/08/us-law-enforcement-meta-smart-glasses)
- **Aggregators (weak; used only for cross-checks):**
  - [local-ai-zone Sep 2026](https://local-ai-zone.github.io/blog/September_2026_AI_Model_Updates.html)
  - [LLM Gateway timeline](https://llmgateway.io/timeline)
  - [tech-insider AI browsers](https://tech-insider.org/ca/chatgpt-atlas-vs-perplexity-comet-vs-gemini-chrome-2026/)
