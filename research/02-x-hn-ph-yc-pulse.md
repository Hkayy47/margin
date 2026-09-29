# 02 · Builder Zeitgeist: X, Hacker News, Product Hunt, YC

*Research slice for project selection. Compiled 2026-09-28. Window: Jan–Sep 2026, weighted toward Mar–Sep.*

## How to read this

- **Evidence tags.**
  - **[S] strong:** primary data, meaning the HN Algolia API (pulled 2026-09-28), Product Hunt leaderboards, YC's own RFS page, or Wikipedia with citations. Also used when several independent sources agree.
  - **[M] medium:** one reputable secondary source, such as TechCrunch, Latent Space/AINews, Fortune or MIT Tech Review.
  - **[W] weak:** an aggregator or SEO blog, or a search-snippet summary. Numbers are not independently checked.
- **X engagement.** X blocks direct fetches (xcancel returned HTTP 451), so every X number here comes from an article or newsletter that quotes the post. Treat view counts as rough.
- **Product Hunt ranks by a weighted score,** so raw upvote counts don't always follow rank order.
- **Inference is labeled.** Anything marked **Inference:** is my interpretation, kept separate from evidence.
- **Research limits.** The WebSearch budget ran out partway through. The remaining checks used direct fetches of the HN Algolia API, PH leaderboards, YC's RFS page and articles. The `last30days` skill couldn't be used because no X credentials are configured and its first-run wizard needs a person to answer it.

---

## TL;DR

1. **2026's biggest consumer-AI story is the agent that acts, reached from your phone.** Examples: OpenClaw over WhatsApp/iMessage, Poke over iMessage, Claude Dispatch, Cursor for iOS, the Acti keyboard and Meta Muse. By September every big lab ships a general version: Meta Muse, Google Gemini Spark, ChatGPT Work and Claude Cowork/Dispatch. **The general "personal agent" is taken. Vertical and physical-world versions are still open.**
2. **The demos that spread most were shot in one take on the builder's own real input,** such as their screen, city, garden or inbox. The AI then **crossed into the physical or social world**: it pointed at the screen, drove the computer by voice, or emailed and negotiated with a real person.
3. **HN rewards craft, local/on-device models and "I built X from scratch" engineering write-ups.** On-device and small-model posts make up the densest cluster of high-scoring AI Show HNs in 2026. There is also a growing **anti-slop and privacy counter-trend**: two "Hacker News without AI" launches on the same day in September.
4. **Product Hunt is dominated by agent tooling and B2B.** Mobile AI rarely wins. When it does, it's a **daily utility with a one-gesture hook**, for example Acti (#1 in July), Claude Dispatch and PollyReach.
5. **YC batches are about 60–90% AI (by different counts) but only about 5% consumer,** and hard tech and robotics are surging. Yet YC's own Fall 2026 RFS says consumer AI is under-built ("three years in, the only new icon on your home screen is ChatGPT"). Its Spring 2026 RFS asks for **"AI guidance for physical work"** delivered through phones, AirPods or glasses.
6. **Warnings:**
   - A wow with no retention dies. OpenAI shut the Sora app on 2026-04-26 after 30-day retention fell to single digits.
   - Camera apps built on a single model call get replaced by one frontier-model call. Karpathy's MenuGen is the example.
   - Glasses and face-recognition demos trigger strong backlash.

---

## 1. Themes ranked by momentum

| # | Theme | Momentum | Key evidence | Fit for this developer (**Inference**) |
|---|---|---|---|---|
| 1 | **Phone-reachable personal agents that act** (messaging, iMessage/SMS, keyboard, lock screen) | ▲▲▲. Peaked Jan–Mar and is now consolidating into Big Tech. | OpenClaw had 247K GitHub stars by Mar 2 [S] and passed React as the most-starred software project ([star-history](https://star-history.com/blog/openclaw-surpasses-react-most-starred-software), HN 291) [S]. Poke became the first agent on Apple Messages for Business, then Cognition acquired it [M]. Claude Dispatch launched Mar 17 [S]. Cursor iOS got 3.9M views [M]. Acti was PH #1 of July [S]. Meta Muse launched in Sept [M]. | Strong demo and hiring signal, but it has to be **vertical**. A generic assistant now competes with Meta, Google, OpenAI and Anthropic. |
| 2 | **Real-time voice as the default interface** | ▲▲▲ | GPT-Realtime-2 launched May 8 [M]. HeyClicky got about 3M views [M]. The "sub-500ms voice agent from scratch" post scored HN 570 [S]. PH's first Orbit Award category was AI Dictation [S]. Voice-typing apps (Voiskey, MosMos, Wispr Flow Notetaker) appear in Aug–Sep top-10s [S]. | High fit. Latency engineering is depth people can *see* in a demo. |
| 3 | **On-device / small models / hybrid routing** | ▲▲ on HN, with platform tailwinds | Needle (26M-parameter tool-calling model): HN 776. Needle2: 537. TurboFieldfare (Gemma 4 26B in 2 GB RAM): 919. Colibri: 937. Apfel: 743. Kitten TTS: 561. Parlor: 298 [S]. Apple's Foundation Models now take image input and are free on Private Cloud Compute for small developers [M]. Gemini Nano runs on Android [M]. | Strong AI-engineer signal. The RTX 5070 makes distillation and fine-tuning practical. |
| 4 | **"See what I see" multimodal guidance** (phone camera, glasses) | ▲▲ rising | YC Spring 2026 RFS "AI Guidance for Physical Work" [S]. Clicky's point-at-the-screen wow [M]. Android XR glasses ship fall 2026 [M]. Meta Ray-Ban Display SDK [S]. PH launches: Hand Wave (sign language → speech on glasses) and CoachAI (form coaching) [S/W]. | The best physical-world wow you can show on a phone. It needs state, memory and verification to avoid the MenuGen trap. |
| 5 | **Agent infrastructure / "software for agents"** | ▲▲▲ at YC and PH, but B2B | 41.5% of YC W26 builds agent infrastructure [M]. YC Summer RFS "Software for Agents" [S]. PH launches: Publora, Bluerails, BrowserAct, Clipto MCP, Unabyss [S]. | Poor fit as the product. Good as a component. |
| 6 | **Physical AI / robotics / hard tech** | ▲▲▲ at YC | YC S26 had 45 physical-product companies and 24 robotics/physical-AI companies [M]. All 9 of TechCrunch's "buzziest" S26 picks are hard tech [M]. | Not doable solo in 3–6 weeks. |
| 7 | **Generative media / world models** | ▲ viral, poor retention | Seedance 2.0, Nano Banana 2, Project Genie, the #EarthZoomOut trend (1.2B views) [W/M]. The Sora app was shut down [M]. | Poor fit for "daily utility". |
| 8 | **Counter-trend: anti-slop, privacy, local-first** | ▲ rising | Two "HN without AI" launches on 2026-09-11 (207 and 198 points) [S]. Weedout: 185 [S]. Nearby Glasses: 433 [S]. ZuckOff: 400 [S]. Fugleramme stresses that "no art is AI-generated" [S]. | A design constraint: privacy-by-design and visible craft win builder respect. |

---

## 2. (a) Viral AI demos on X in 2026, with emphasis on phone and physical-world demos

| # | When | Who | The 10-second "wow" | Rough engagement | Links | Evidence |
|---|---|---|---|---|---|---|
| 1 | Jan 22 | **Andy Coenen** (@_coenen), solo | Zoom around a giant SimCity-2000-style pixel-art NYC. The post said he "didn't write a single line of code". He fine-tuned an image model on 40 examples and generated the city tile by tile. | HN 1,325 pts; wide press (PC Gamer, Gigazine) | [X post](https://x.com/_coenen/status/2014359718697799989) · [HN](https://news.ycombinator.com/item?id=46721802) · [Oxen write-up](https://www.oxen.ai/blog/isometric-nyc) | S (HN) / M (X) |
| 2 | Jan 25–30 | **Clawdbot → Moltbot → OpenClaw** (Peter Steinberger, @steipete). The viral trigger was @ImSh4yy's "agent on a Mac mini in my garage" post. | Text your agent on WhatsApp/iMessage and it does real work 24/7 on your own machine: email, bookings, flight check-in. People bought Mac minis just to run it. | 9K stars in 24h, 247K by Mar 2. Steinberger's "I'm joining OpenAI" post scored HN 1,449. PH #7 of January (831). | [Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) · [Slashdot: Mac mini craze](https://tech.slashdot.org/story/26/01/28/0510226/clawdbot-has-ai-techies-buying-mac-minis) · [steipete.me](https://steipete.me/posts/2026/openclaw) | S |
| 3 | Jan 28–31 | **Moltbook** (Matt Schlicht) | Screenshots of AI agents posting to each other on a Reddit-style forum. Karpathy: "genuinely the most incredible sci-fi takeoff-adjacent thing I have seen recently". He later called it "a dumpster fire". | 2.9M registered accounts by June. Meta acquired it on Mar 10. | [Wikipedia](https://en.wikipedia.org/wiki/Moltbook) · [MIT Tech Review: "peak AI theater"](https://www.technologyreview.com/2026/02/06/1132448/moltbook-was-peak-ai-theater/) | S |
| 4 | Jan 29 | **Google DeepMind, Project Genie** | Type a prompt and walk around a playable world. The viral clips were Mario 64 and Zelda imitations. | Viral clips (no reliable counts) | [9to5Google](https://9to5google.com/2026/01/29/google-project-genie/) | M |
| 5 | Mar 17 | **Anthropic, Claude Dispatch** | Text Claude from your phone and your desktop does the work: files, browser, GitHub. | PH #7 of March (646) | [Claude help center](https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork) · [PH March](https://www.producthunt.com/leaderboard/monthly/2026/3) | S |
| 6 | Apr 7 | **Farza Majeed** (@FarzaTV), **Clicky** | An AI "teacher" that sits next to your cursor, sees your screen, talks, and **physically points at the button you need** (he used it to learn DaVinci Resolve). Open-sourced within days. | ~2.9M views. GitHub: 7.7K stars, 1.5K forks. | [X post](https://x.com/FarzaTV/status/2041314633978659092) · [open-source post](https://x.com/FarzaTV/status/2041691382008705321) · [repo](https://github.com/farzaa/clicky) | S (stars) / W–M (views) |
| 7 | Apr 30 – May | **Karpathy's MenuGen, "Software 3.0" clip** (reposted by @vitrupo and @itsolelehmann) | His own photo-a-menu → see-the-dishes app is made pointless when Gemini/Nano Banana draws the dishes straight onto the photo in one call. "The more work the neural network does, the less software exists." | Widely reshared clip | [vitrupo](https://x.com/vitrupo/status/2051320789203595389) · [Ole Lehmann](https://x.com/itsolelehmann/status/2049957182926667811) · [Karpathy's own notes](https://karpathy.bearblog.dev/sequoia-ascent-2026/) | S (primary notes) |
| 8 | May 8 | **GPT-Realtime-2 launch demos** (@Vimeo live dubbing; @kwindla: "first OpenAI speech-to-speech model good enough for real work"; Genspark "Call For Me") | Live speech-to-speech translation and dubbing. Voice agents that make phone calls with parallel tool calls. | Genspark reported +26% effective conversation rate | [AINews](https://www.latent.space/p/ainews-gpt-realtime-2-translate-and) · [OpenAI](https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/) | M |
| 9 | May 19 | **PollyReach** | "Book me a table for 7pm": it finds the number, **calls the restaurant**, handles the conversation, and sends back a summary, recording and transcript. | PH #1 of the day (526); #2 of the week (786) | [PH](https://www.producthunt.com/products/pollyreach) · [PH week 21](https://www.producthunt.com/leaderboard/weekly/2026/21) | S |
| 10 | May 30 | **Farza, HeyClicky voice control** | A 104-second single take: fully hands-free "open VS Code, make the snake blue, play Spotify" on GPT-Realtime-2. Greg Brockman: **"real magic."** | ~3M views | [explainx write-up](https://explainx.ai/blog/heyclicky-voice-control-mac-gpt-realtime-2-demo-2026) · [@heyclicky](https://x.com/heyclicky) | M |
| 11 | Jun 4 | **Poke** (Interaction Co.) | "Text it like a friend": it manages your calendar and email and controls Hue/Sonos over iMessage/SMS. It became the first AI agent Apple approved for Messages for Business. | Sign-ups up 10× in two months. Acquired by Cognition on Jul 23. | [TechCrunch (Apple approval)](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/) · [TechCrunch (Apr)](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/) | M |
| 12 | Jun 29 | **Cursor for iOS** (official account plus Ben Lang). Demo by Eric Zakariasson. | Dictate a coding task while out on a walk. A cloud agent builds it, and you review and merge the PR from your lock screen. | Official post ~3.9M views (quoted by Elon Musk) | [explainx write-up](https://explainx.ai/blog/cursor-big-day-ben-lang-composer-3-spacex-june-2026) | M |
| 13 | Jun 30 – Jul 1 | **Acti** "agentic keyboard" (founder previously scaled Baidu's Facemoji keyboard) | In any chat, long-press the keyboard bar and an agent runs multi-step actions across 150+ tools without leaving the conversation. | PH #1 for the day, week and month (804). $5.3M seed. 1,000+ user-built Skills in two weeks. | [TechCrunch](https://techcrunch.com/2026/06/30/acti-puts-ai-agents-directly-into-your-smartphone-keyboard/) · [PH](https://www.producthunt.com/products/acti-2) | S |
| 14 | Sep 15 | **Arne Giacomo Munthe-Kaas, Fugleramme** (solo) | A picture frame in a Bergen kitchen window **hears birds** (BirdNET, fully local on a Raspberry Pi) and draws them as real 1800s natural-history plates on e-ink. | **HN 2,391 pts, #2 Show HN of 2026**; Boing Boing and other press | [HN](https://news.ycombinator.com/item?id=49711544) · [repo](https://github.com/arnegiacomo/fugleramme) · [site](https://arnegiacomo.dev/fugleramme/) | S |
| 15 | Sep 23–24 | **Meta Connect 2026, Muse agent** (@andrew_n_carr) | Asked to "find a small-batch embroiderer", Muse **found, emailed and negotiated with a semi-retired tradesman**, who replied "how in the world did you find me?" Also announced: the Muse Charm keychain and Ray-Ban Meta Gen 3. | @finkd's keynote recap drew ~15.9K engagements | [AINews](https://www.latent.space/p/ainews-meta-connect-2026-muse-glasses) · [TechCrunch](https://techcrunch.com/2026/09/23/everything-new-coming-to-metas-ai-agent-muse/) | M |
| 16 | RSAC (spring) | **ESET's Jake Moore**, a counter-example | Meta Ray-Bans plus off-the-shelf face recognition identify strangers in real time. This fed a backlash: HN "Meta ships facial recognition on smart glasses" (332), "Nearby Glasses" detector (433), ZuckOff (400). | Press and HN outrage | [State of Surveillance](https://stateofsurveillance.org/news/rsac-meta-smart-glasses-facial-recognition-hacked-live-demo-2026/) · [HN](https://news.ycombinator.com/item?id=48403588) | M |

**Also relevant (smaller or supporting):**
- Software Mansion's Argent agent tool can now drive a physical iPhone over USB ([X](https://x.com/swmansion/status/2096974561971523981), Sep 2026) [W].
- Kilo Code shipped iOS/Android apps to "start coding agents, control sessions, review PRs. Anywhere" (PH week 38 #6) [S].
- Nano Banana 2 (Feb 26) and Seedance 2.0 (Feb) kept AI image and video trends on everyone's feeds ([Wikipedia](https://en.wikipedia.org/wiki/Nano_Banana), [Wikipedia](https://en.wikipedia.org/wiki/Seedance_2.0)) [M].

**What made these spread (evidence-backed patterns):**
1. **The AI crosses a boundary into the real world:**
   - pointing at the screen (Clicky)
   - driving the machine by voice (HeyClicky)
   - calling or emailing a real human (PollyReach, Muse)
   - a physical object (Fugleramme)
   - acting while you're away from your laptop (OpenClaw, Cursor iOS, Dispatch)
2. **One continuous take on real input:** the builder's own screen, garden or city, not a canned prompt.
3. **Voice and hands-free** make it read as sci-fi. Brockman's "real magic" line was about a voice demo.
4. **The phone as the control surface** for work that happens elsewhere: iMessage, the keyboard, the lock screen.
5. **Builder credibility plus open source.** Clicky was MIT-licensed within days and reached 7.7K stars. OpenClaw, Fugleramme and isometric.nyc all published write-ups. Star counts and remixes then create a *second* viral wave.
6. **A notable account quotes it:** Brockman, Karpathy, Musk, YC partners.
7. **Controversy speeds things up but also caps them.** Moltbook, OpenClaw security bugs and glasses privacy all spread fast, then drew backlash.

---

## 3. Anatomy of a viral AI demo in 2026

**Inference, drawn from the 16 cases above.**

1. **Seconds 0–3, the result first.** Show the thing already happening (cursor moving, frame drawing, agent on a call). No logo and no UI tour.
2. **Seconds 3–10, the boundary crossing.** The AI touches something outside the chat box: a real screen, a camera view, a phone call to a human, a physical display, or a message sent for you.
3. **Real, personal input.** The builder's own garden, city, inbox or broken appliance. Generic prompts read as slop in 2026.
4. **Voice, not typing,** ideally with sub-second turn-taking. Latency is the magic.
5. **One take, 60–110 seconds, filmed on a phone.** HeyClicky was 104 s. Cuts read as fake, especially after the 2026 fights over AI-demo authenticity (Moltbook; Apple's $250M false-ad settlement in [TechCrunch's WWDC coverage](https://techcrunch.com/2026/06/08/apples-wwdc-ai-demos-looked-more-real-after-250m-false-ad-settlement/)).
6. **A human reaction beat.** The embroiderer's "how in the world did you find me?", or the builder laughing.
7. **A one-line claim that compresses effort:**
   - "I didn't write a single line of code"
   - "sub-500ms, built from scratch"
   - "runs fully local on a Pi"
8. **Open source plus a write-up within 72 hours.** This turns views into stars and HN points, which drives a second wave.
9. **Trust signals built in:** local or private processing, visible confirmation before actions. This matters because the 2026 backlash targets glasses, face recognition and agent security.
10. **Durable virality needs daily use.** Sora, Moltbook and most AI-video templates spiked and faded. OpenClaw, Poke, Acti and Wispr-style dictation kept users.

---

## 4. (b) Show HN AI projects in 2026: who scored, who was solo, and themes

**Source:** the [HN Algolia API](https://hn.algolia.com/api/v1/search?query=AI&tags=show_hn&numericFilters=created_at_i%3E1767225600,points%3E200), queried for AI, LLM, agent, voice, phone, camera, on-device, iOS, Android, Gemma, Claude, health and memory [S].

**Context:** the top Show HNs of 2026 overall are mostly *physical-world craft*:
- ESP32 bowling-alley system: 2,935 (not AI)
- **Fugleramme bird frame: 2,391 (AI, local)**
- Elevators: 1,680
- **isometric.nyc: 1,325 (AI)**

| Pts | Project (date) | What | Solo/indie? |
|---|---|---|---|
| 2,391 | [Fugleramme](https://news.ycombinator.com/item?id=49711544) (Sep 15) | Local BirdNET on a Pi → e-ink 1800s bird plates | Solo |
| 1,325 | [isometric.nyc](https://news.ycombinator.com/item?id=46721802) (Jan 22) | AI-generated pixel-art NYC | Solo |
| 937 | [Colibri: GLM 5.2 on a slow computer](https://github.com/JustVugg/colibri) (Jul 9) | Run a frontier open model on weak hardware | Solo |
| 919 | [TurboFieldfare](https://news.ycombinator.com/item?id=49098510) (Jul 29) | Gemma 4 26B in 2 GB RAM on M-series Macs | Indie |
| 915 | [GuppyLM](https://github.com/arman-bd/guppylm) (Apr 6) | A tiny LLM built to demystify how LLMs work | Solo |
| 776 | [Needle](https://github.com/cactus-compute/needle) (May 12) | Gemini tool-calling distilled into a 26M model | Startup (Cactus Compute) |
| 743 | [Apfel](https://news.ycombinator.com/item?id=47624645) (Apr 3) | "The free AI already on your Mac" (Apple's on-device model) | Solo |
| 710 | [Load-bearing vocabulary of Claude](https://news.ycombinator.com/item?id=49461817) (Aug 27) | Analysis of Claude's word choices | Solo |
| 687 | [Forge](https://news.ycombinator.com/item?id=48192383) (May 19) | Guardrails lift an 8B model from 53% → 99% on agentic tasks | Solo/indie |
| 598 | [Piano autocomplete](https://news.ycombinator.com/item?id=49373456) (Aug 20) | A 125M model trained to autocomplete piano, **on-device** | Solo |
| 570 | [Sub-500ms voice agent from scratch](https://news.ycombinator.com/item?id=47224295) (Mar 2) | Deepgram Flux + Groq + ElevenLabs over a streaming pipeline, ~400 ms end to end, ~$100 in API spend | Solo (Nick Tikhonov) |
| 561 | [Kitten TTS](https://news.ycombinator.com/item?id=47441546) (Mar 19) | TTS models under 25 MB | Small team |
| 537 | [Needle2](https://news.ycombinator.com/item?id=49246804) (Aug 10) | A 14 MB agentic LLM for phones, wearables and robots | Startup |
| 533 | [NanoClaw](https://github.com/gavrielc/nanoclaw) (Feb 1) | Clawdbot in 500 lines of TypeScript with container isolation | Solo |
| 524 | [Trails: 100 books](https://news.ycombinator.com/item?id=46567400) (Jan 10) | Claude Code finds connections across 100 books | Solo |
| 495 | [RYS: topped the HF leaderboard on two gaming GPUs](https://news.ycombinator.com/item?id=47322887) (Mar 10) | Layer surgery with no training | Solo |
| 467 | [Ghost Pepper](https://news.ycombinator.com/item?id=47666024) (Apr 6) | Local hold-to-talk speech-to-text for macOS | Solo |
| 438 | [SentrySearch](https://news.ycombinator.com/item?id=47503617) (Mar 24) | Natural-language search over dashcam/Tesla Sentry footage (Gemini video embeddings); 4.5K stars | Solo |
| 402 | [Lathe](https://news.ycombinator.com/item?id=48433756) (Jun 7) | "Use LLMs to learn a new domain, not skip past it" | Solo |
| 386 | [Continue? Y/N](https://news.ycombinator.com/item?id=48308376) (May 28) | A 60-second game about agent-permission fatigue | Indie |
| 305 | [Now I Get It](https://news.ycombinator.com/item?id=47195123) (Feb 28) | Research paper → plain-language explainer | Solo |
| 298 | [Parlor](https://news.ycombinator.com/item?id=47652007) (Apr 5) | Real-time audio/video in, voice out, fully local (Gemma E2B, Kokoro TTS; ~0.7 s to first audio on an M3 Pro) | Solo |
| 215 | [Whodunnit AI](https://news.ycombinator.com/item?id=49238851) (Aug 10) | Interrogate AI murder-mystery suspects by voice | Indie |
| 205 | [Trace](https://news.ycombinator.com/item?id=48521236) (Jun 13) | Offline meeting transcripts you can flag mid-call | Indie |
| 124 | [Off Grid](https://news.ycombinator.com/item?id=47019133) (Feb 14) | Text, image generation and vision fully offline on your phone | Solo |

**Startup/lab posts that also did well:**
- 1-bit Bonsai (PrismML): 430
- Semble: 445
- Whiteboard (YC W26): 421
- OpenKnowledge (Inkeep): 381
- Microsoft Flint: 350
- Mastra 1.0: 213
- LemonSlice (real-time video avatars): 133

**Themes (evidence [S], interpretation marked):**
1. **Local, on-device and small models are the densest high-scoring cluster:** Needle ×3, TurboFieldfare, Colibri, Apfel, Kitten TTS, Parlor, Ghost Pepper, Yap, Trace, Off Grid, whichllm (283), and the piano model.
2. **Engineering write-ups beat launches.** "I built X from scratch and here's the latency or accuracy number": sub-500ms voice, Forge 53→99%, RYS, GuppyLM.
3. **Agent-harness do-it-yourself work after OpenClaw:** NanoClaw, LocalGPT (331), nullclaw on IRC (340), Clawk VMs (226), Oak (216), cq (225). The HN mood is heavy on security (for example "OpenClaw is a security nightmare", 397).
4. **"Help me understand, don't replace me":** GuppyLM, "How LLMs Work" (245), Lathe, Now I Get It, the attention visualizer.
5. **Physical-world plus AI craft wins the biggest scores:** Fugleramme, isometric.nyc, CarWatch (a Raspberry Pi with Qwen as a local car AI, 146), Nightcrawler (a local pentest agent on a phone, 120).
6. **Counter-trend:** "HN without AI" ×2 (207 and 198), Weedout (185), TERMy "does not use LLMs" (225).
7. **Mobile consumer AI is thin on HN.** Off Grid (124) and phone breath-biofeedback (67) are about it. **Inference:** a polished, phone-first AI product with a real engineering write-up would stand out on HN because so few exist.
8. **Saturation signal for this developer:** another real-time 3D globe, [Metiq](https://metiq.space), got only 148 points. The globe and dashboard genre is crowded.

---

## 5. (c) Product Hunt: top AI launches of 2026

**Monthly #1s** ([leaderboards](https://www.producthunt.com/leaderboard/monthly/2026/1)) [S]:

| Month | #1 (score) | Other notable top-10 entries |
|---|---|---|
| Jan | **Cowork**: "Turn Claude into your digital coworker" (1,094) | Mom Clock (iOS accountability, 734); Cal.com native apps; **OpenClaw** (831); 1Code |
| Feb | **happycapy**: "agent-native computer for the rest of us" (1,359) | **Rork Max**: "Best AI for iOS apps. Website that replaces Xcode" (1,418); KiloClaw (hosted OpenClaw); **Lovon AI Therapy** (791); Claude Opus/Sonnet 4.6 |
| Mar | **Stitch 2.0 by Google** (854) | Claude Import Memory; Tobira ("AI agents find deals for their humans"); **Claude Dispatch** (Android/phone, 646); Littlebird |
| Apr | **Brila**: one-page websites from Google Maps reviews (1,361) | Fathom 3.0; Clera (iMessage hiring agent); **NovaVoice**; Figma for Agents; **Open Wearables** (630) |
| May | **Kilo Code for VS Code** (889) | StoreClaw; **PollyReach** (786); Unabyss (MCP memory); OpenHuman; Velo 2.0 (voice + screen) |
| Jun | **Fundraisly**: AI agent that finds investors and books meetings (1,531) | Upstream ("inbox for humans and agents"); Goldfish ("knows your work and replies like you"); Bond ("to-do list that does itself"); Publora; Bluerails; BrowserAct |
| Jul | **Acti**: agentic mobile keyboard (804) | Pazi; OpenSEO; Glaze by Raycast (make your own Mac apps by chatting) |
| Aug | **Clipto MCP** / **Hey Noah** (proactive executive assistant) | Dograh (open-source Vapi alternative); **Wispr Flow Notetaker**; Grok Bot; **x1: "Lovable for iPhone apps"** |
| Sep (to date) | **Ami AI**: "Lovable for getting customers" (645) | tiun. / CREEM (payments for AI builders); **Voiskey** (voice typing); **Kilo Code for iOS/Android**; MosMos (voice writing) |

**Yearly top-10 to date** ([yearly](https://www.producthunt.com/leaderboard/yearly/2026)):
- PostSyncer
- **Mom Clock** (iOS)
- Cowork
- Livedocs
- MiroMiro
- Atlas.new
- 2-b.ai
- **Joodle** (iOS: "turn years of memories into personal doodles")
- ChatGPT Health
- SEORCE

**Awards:** Product Hunt replaced the Golden Kitties with the quarterly **Orbit Awards**, judged on traction. The **first category was AI Dictation** (finalists: Wispr Flow, Willow, Aqua Voice, Superwhisper and others) ([PH](https://www.producthunt.com/stories/introducing-the-orbit-awards)) [S].

**Mobile/physical launches worth noting:**
- Hand Wave: "Turn sign language into speech with smart glasses" (Aug 3, #10)
- Scriptly: voice-controlled iOS teleprompter (Sep 7, #2)
- CoachAI: iPhone camera watches your form rep by rep (Aug) [W]

**Patterns:**
1. **"Agents that do it for you."** Cowork, Bond, Hey Noah, Fundraisly, Tasklet-style tools, PollyReach. The tagline template is "X that does itself".
2. **Tools for the agent economy:** payments, publishing APIs, browsers, search and memory for agents.
3. **Vibe-coding for every surface:** iOS (Rork Max, x1), Mac (Glaze), business operations (Pazi), websites (Brila).
4. **Voice input everywhere:** dictation won the first award category, and voice apps keep showing up in 2026 top-10s.
5. **Memory and context layers:** Unabyss, Claude Import Memory, Littlebird, Goldfish.
6. **The phone as remote control for agents:** Claude Dispatch, Cursor/Kilo mobile, Acti.
7. **When consumer mobile wins, it's one simple daily habit** (Mom Clock, Joodle, Acti), not a feature list.

**Inference:** Product Hunt is a weak signal for engineering depth, but a good check on whether the one-line hook lands.

---

## 6. (d) YC: 2026 Requests for Startups and batch composition

**RFS by season [S]:**
- **Spring 2026** (Feb). For the first time, YC founders co-wrote the list ([Jared Friedman on X](https://x.com/snowmaker/status/2018502910733377642)). Ideas: Cursor for PMs · AI-native hedge funds · AI-native agencies · stablecoin financial services · AI for government · modern metal mills · **AI Guidance for Physical Work** (Jared Friedman) · infrastructure for government fraud hunters ([Modelence summary](https://modelence.com/yc-rfs-spring-2026)).
  - **AI Guidance for Physical Work:** AI that "sees what workers see and coaches them through the job: 'turn off that valve,' 'use the ⅜ inch wrench'". The pitch is that multimodal models are now reliable, phones/AirPods/smart glasses are everywhere, and skilled labor is short ([Modelence](https://modelence.com/yc-rfs-spring-2026/ai-guidance-for-physical-work); the six-pillar architecture on that page is Modelence's own expansion, not YC's text).
- **Summer 2026** (Apr 28), 15 ideas ([VC Corner](https://www.thevccorner.com/p/yc-summer-2026-requests-for-startups-ideas)): AI for low-pesticide agriculture · AI-native service companies · AI personalized medicine · **Company Brain** · counter-swarm defense · **Dynamic Software Interfaces** · electronics in space · hardware supply chain · industrial capabilities in space · inference chips for agent workflows · SaaS challengers · **Software for Agents** · selling to huge companies · semiconductor supply chain · AI OS for companies. No consumer, mobile or voice item.
- **Fall 2026** (current, [ycombinator.com/rfs](https://www.ycombinator.com/rfs)): The Primer (an adaptive AI tutor for young kids) · American defense (written by the US Secretary of the Army) · A Cloud for Small Software · **Multiplayer AI** · Compute at Sea · **AI-Powered Consumer Products for 1 Billion People** · **AI for the Aging Population** · New OS for the Physical World · crypto · Data for the Real World · **Proving You're Human** · AI-native compliance · Self-maintaining APIs.
  - **Raphael Schaad, verbatim:** "AI is the biggest shift YET. But three years in, the only new icon on your home screen is ChatGPT… Intelligence just got good enough: you can treat an agent like a person. And it's about to get cheap enough, too: today, the magic can run $1,000 a month in tokens for each user, but that is falling 10x a year… CONSUMER is going to be so back."
  - **Max Kolysh (aging), verbatim:** "voice interfaces that can hold real conversations, monitoring that helps older adults stay safe and independent… software that helps family caregivers coordinate care."
  - **Aaron Epstein (multiplayer):** "Anyone on a team should be able to drop into the same live agent session to watch it work, redirect it, and hand it off."

**Batch composition [M]. These are third-party counts and differ slightly.**

| Batch (Demo Day) | Size | Key stats | Notable/standout companies |
|---|---|---|---|
| W26 (Mar 2026) | ~190–194 | 60% AI-focused; 41.5% agent infrastructure; 64% B2B; **~5% consumer**; robotics/physical AI rose from 6.6% to 18.1% ([analysis](https://www.buildmvpfast.com/blog/yc-w26-batch-agent-infrastructure-boom)) | [TechCrunch 16](https://techcrunch.com/2026/03/26/16-of-the-most-interesting-startups-from-yc-w26-demo-day/): **Button Computer** (wearable voice automation), **Doomersion** (TikTok-style language learning), **Lexius** (AI on security cameras detects theft and falls), Opalite Health (medical translator), CodeWisp (describe a game and get it) |
| Spring 2026 (Jun) | — | 45% built autonomous agents | [TechCrunch 11](https://techcrunch.com/2026/06/18/the-11-standout-startups-from-ycs-demo-day-according-to-vcs/): 9 Mothers (counter-drone, ~$200M valuation), Superset (runs 100+ coding agents), Tasklet, Silmaril, Arga Labs. **No consumer picks.** |
| S26 (Sep 10) | 235–236 | 91% AI-related; agents fell to 33%; application layer fell 55% → 39%; model layer rose 8% → 20%; industrials 23–24%; **consumer 5.5%**; 52% B2B; **37% students or recent grads**; 45 physical-product and 24 robotics companies ([ChainCatcher via KuCoin](https://www.kucoin.com/news/flash/yc-2026-summer-batch-analysis-91-ai-related-application-layer-drops-to-39)) | [TechCrunch 9 buzziest](https://techcrunch.com/2026/09/13/the-9-buzziest-startups-from-y-combinators-latest-demo-day-according-to-vcs/): Atomarine (floating nuclear data centers), Dipole Labs, Isengard, Lamb Labs (weights hard-coded into chips), Praxis Robotics, **Nori ($1,600 humanoid)**, Cosmic Robotics, Parasma, Waddle Labs. **All hard tech.** |

**Where founders and VCs are betting:**
1. Agent infrastructure (W26), shifting to the model layer, inference and custom chips (S26).
2. Physical AI, robotics and defense.
3. AI-native services, meaning companies that sell finished work instead of software.
4. Vertical B2B.

**Inference:** consumer AI is under-built *relative to YC's own stated thesis*. A polished, phone-first consumer AI product sits in a visible gap. It also lines up with YC's Fall 2026 asks (consumer for a billion people, aging, The Primer, proving you're human) and the Spring ask (AI guidance for physical work).

---

## 7. (e) What prominent voices say is next or most under-built

| Who | Claim | Source |
|---|---|---|
| **Andrej Karpathy**, Sequoia AI Ascent, Apr 30 | "Software 3.0": the context window is the program. Some apps "disappear into direct model transformations" (his MenuGen example). Build **agent-native surfaces** (APIs, CLIs, headless). Go after **verifiable but under-trained domains**. Rethink workflows around **sensors and actuators**. "You can outsource your thinking, but you can't outsource your understanding." | [karpathy.bearblog.dev](https://karpathy.bearblog.dev/sequoia-ascent-2026/) [S] |
| **Karpathy**, Mar 17 | "Autoresearch" loop: an agent ran 700 experiments in 2 days and found 20 optimizations. "All LLM frontier labs will do this. It's the final boss battle." Also reported (secondary sources only): he runs his home (lights, HVAC, pool) through one WhatsApp agent he calls "Dobby". | [Fortune](https://fortune.com/2026/03/17/andrej-karpathy-loop-autonomous-ai-agents-future/) [M]; Dobby [W] |
| **Sonya Huang / Pat Grady (Sequoia)** | "2026 is the year of agents": models, tools and harnesses have converged. Services, not software, are the market ($10T). Personal agents are taking over inboxes, calendars, finances and taxes. | [Sequoia](https://sequoiacap.com/article/ai-ascent-2026) [M] |
| **a16z Big Ideas 2026** | Marc Andrusko: **"prompt-free, proactive" apps**, the death of the prompt box. Olivia Moore: **voice agents take over workflows**. Josh Lu: **"the year of me"** (hyper-personal products). Anish Acharya: **ChatGPT, Apple mini-apps and AI SDKs as the new app store**. | [a16z Part 1](https://a16z.com/newsletter/big-ideas-2026-part-1/), [Part 2](https://a16z.com/newsletter/big-ideas-2026-part-2/), [summary](https://www.the-ai-corner.com/p/a16z-ai-ideas-2026-partners) [M] |
| **YC partners** | Consumer is under-built (Schaad). Real-time AI guidance for physical work (Friedman). Multiplayer agent sessions (Epstein). AI for aging, and proving you're human (Kolysh). Adaptive tutor for kids (Miklas). | [YC RFS](https://www.ycombinator.com/rfs) [S] |
| **Ethan He (xAI) on Latent Space**, Jun 1 | "The next Sora won't be a better video model, but a video agent." Real-time generative interfaces and world models are next. | [Latent Space](https://www.latent.space/p/video-agents) [M] |
| **Latent Space**, Jul–Aug | Websites will assemble themselves per visitor ("It's not the future, it's the present now"). ChatGPT Work is "a preview of how ChatGPT's billion weekly users will soon use the app", and its **weak plugin discovery** is under-built. | [website of the future](https://www.latent.space/p/the-website-of-the-future), [ChatGPT Work](https://www.latent.space/p/unpacking-chatgpt-work) [M] |
| **Simon Willison**, Jan 8 predictions | 2026: coding agents' code quality becomes undeniable. **Sandboxing gets solved.** A major prompt-injection or agent security incident arrives. (An OpenAI-reported autonomous agent cyberattack followed on Jul 21, per [Wikipedia](https://en.wikipedia.org/wiki/2026_in_artificial_intelligence).) | [simonwillison.net](https://simonwillison.net/2026/Jan/8/llm-predictions-for-2026/) [S] |
| **Greg Brockman** on HeyClicky | "real magic": voice plus real control of the computer | [explainx write-up](https://explainx.ai/blog/heyclicky-voice-control-mac-gpt-realtime-2-demo-2026) [M] |

**Platform tailwinds for Sep–Dec 2026 [M]:**
- **Apple (WWDC, Jun 9):**
  - Foundation Models now take **image input**.
  - One Swift API reaches the on-device model, Claude or Gemini.
  - **Free Private Cloud Compute** for developers under 2M first-time downloads ([MacRumors](https://www.macrumors.com/2026/06/09/apple-outlines-major-ai-and-developer-tool-updates/)).
  - The Gemini-based Siri gains on-screen awareness in iOS 26.4 and iOS 27.
- **Google (I/O, May 20):**
  - Gemini 3.5 Flash.
  - Gemini Spark, a 24/7 cloud agent.
  - On-device Gemini Nano for Android.
  - Android XR glasses shipping this fall ([AINews](https://www.latent.space/p/ainews-google-io-2026-gemini-35-flash), [TechCrunch](https://techcrunch.com/2026/05/22/we-tried-googles-ai-glasses-and-theyre-almost-there/)).
- **Meta:** the Ray-Ban Display developer preview supports both native mobile apps and web apps ([Meta](https://developers.meta.com/blog/build-for-display-glasses/)).
- **OpenAI:** its screenless "companion" device is expected in the second half of 2026 ([MacDailyNews](https://macdailynews.com/2026/01/21/openais-jony-ive-designed-always-listening-ai-device-on-track-for-late-2026/)) [W–M].

---

## 8. Cautionary tales (what *not* to copy)

- **Sora app (OpenAI):**
  - Downloads peaked above 3.3M in Nov 2025 and fell to ~1.1M by Feb 2026.
  - 30-day retention hit **single digits**.
  - The app shut down on 2026-04-26.
  - Lesson: an amazing model plus a feed with no daily job equals churn ([TechCrunch](https://techcrunch.com/2026/03/24/openais-sora-was-the-creepiest-app-on-your-phone-now-its-shutting-down/), [analysis](https://www.digitalapplied.com/blog/openai-kills-sora-ai-video-app-died-six-months-analysis)) [M].
- **Moltbook:**
  - Viral for weeks, then human-written "agent" posts and two database breaches (1.5M API tokens exposed).
  - Karpathy went from "incredible" to "dumpster fire" ([Wikipedia](https://en.wikipedia.org/wiki/Moltbook)) [S].
- **MenuGen:** a photo → AI → UI wrapper gets replaced by one frontier-model call (Karpathy) [S].
  - **Inference:** a camera project's depth has to live in things one call can't do: real-time loops, memory and state across sessions, verification, tool use and actions, on-device and cost engineering.
- **Glasses and face recognition:**
  - Courts are banning smart glasses (Philadelphia, HN 416).
  - Advocacy groups have filed criminal complaints in Germany.
  - Bystander-detector apps (Nearby Glasses, ZuckOff) went viral.
  - Keep bystanders out of the loop, and never identify people.
- **OpenClaw security:**
  - CVEs, a malware skill as the top ClawHub download (HN 334), and China restricting government use.
  - Agent products need visible permission and confirmation design. HN even made a game about "permission fatigue" (386).
- **Big-Tech crowding of general assistants:** Meta Muse (1,500+ connectors, free), Google Spark, ChatGPT Work and Claude Cowork/Dispatch are all general personal agents shipped between Mar and Sep.

---

## 9. Implications for picking the project (all **Inference**)

- **The strongest open slot:** a phone-first product where the AI **sees or hears the real world and acts in it**, narrowed to one concrete daily job. It should be demonstrable in one take on a phone, and its depth should show in:
  - latency (a sub-second voice loop)
  - state and memory across sessions
  - grounding and verification (boxes or arrows drawn on the live camera; checking a step actually happened)
  - hybrid on-device/cloud cost engineering. This answers YC's "$1,000/month in tokens" constraint and plays to the RTX 5070 for distilling or fine-tuning small models.
- **Evidence-backed shapes that fit the brief:**
  - **"Clicky for the physical world"** (camera plus voice guidance with on-screen pointing, the YC Spring RFS shape), aimed at a *daily* activity rather than one-off repairs. Cooking, workout form, homework tutoring (The Primer) or caregiving (the aging RFS) all qualify.
  - **A phone-native agent that crosses into the physical/social world** with a human reaction beat, for example it calls or texts real businesses for you. This builds on the developer's planned Bland AI voice gateway and Canvas MCP, but must be vertical so it doesn't compete with Muse, Spark or ChatGPT Work.
- **Avoid:**
  - general "personal agent" clones
  - AI-video or feed apps
  - single-call camera wrappers
  - anything using face recognition
  - another dashboard or globe
- **Launch playbook drawn from the evidence:**
  - a 60–100 s single-take phone video posted on X, results first
  - open-source the repo and publish an engineering write-up with hard numbers (latency, accuracy, cost per session) within 72 h
  - post a Show HN leading with the engineering story
  - post on Product Hunt with a one-line daily-habit hook
- **Platform note:** several of 2026's most viral "AI buddy" demos were **Mac-only** (Clicky, HeyClicky, Apfel, Ghost Pepper). A **phone-first** equivalent is noticeably under-built. Without a Mac, Android, a PWA with WebRTC camera and mic, or Expo with EAS cloud builds are the realistic routes to demoing on a phone.
