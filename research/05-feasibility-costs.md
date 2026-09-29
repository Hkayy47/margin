# 05: Feasibility and cost of shipping an AI app to a phone from Windows (no Mac)

*Research slice for the portfolio-project decision. All sources were read on **2026-09-28** unless noted. Prices are USD list prices on that date. "Official" means vendor docs or pricing pages. "3rd-party" means blogs, trackers or forums, and those are flagged where used. Numbers marked **(est.)** are my own calculations from official unit prices. This is not legal advice.*

Developer constraints I assumed: Windows 11 with no Mac, TypeScript/Node and Python, an RTX 5070 laptop (8 GB), Docker, 3–6 weeks of solo work with AI coding agents, phone type unknown, and a budget that could be as low as $0–20/month.

---

## 0. TL;DR

1. **A PWA (installable web app) is the only path that reaches both iPhone and Android for $0 from Windows and lets a recruiter try it in under 30 seconds** (open a link or scan a QR code). Since iOS 26, *every* site added to the Home Screen opens as a web app [68]. WebGPU ships in Safari 26 on iOS [68] and Chrome 121+ on Android [73]. Web Push has worked on iOS 16.4+ once the app is added to the Home Screen [70][72]. The gaps are real: iOS has no install prompt, iOS audio stops when the PWA is backgrounded or the screen locks, push works only after install, and a PWA can't reach Apple's on-device model.
2. **Any native app on an iPhone costs $99/yr** (Apple Developer Program [58]; fee waivers exist only for organizations, not individuals or students [59]). EAS Build compiles iOS apps in the cloud, so Windows is fine. Three constraints apply, though. **Expo Go on the App Store is stuck at SDK 54** because SDK 55+ has not been approved [53][54]. TestFlight external testing needs Beta App Review [60]. Builds expire after about 90 days [61].
3. **Android is cheap but gated.** A new personal Play account must run a **closed test with 12 testers for 14 days** before production [62]. Sideloaded APKs will need a **verified developer**: enforcement starts 2026-09-30 in Brazil, Indonesia, Singapore and Thailand, and goes global in 2027. ADB installs are exempt, and a free "limited distribution" account covers up to 20 devices [63].
4. **Tokens are cheap at demo scale.** GPT-6 Luna costs $0.10/$0.50 per 1M input/output tokens, Gemini 3.1 Flash-Lite $0.25/$1.50, Claude Haiku 4.5 $1/$5, Sonnet 5.5 $2/$10, Opus 5.5 $4/$20 and Fable 5.1 $10/$50 [1][5][11]. 100 users with light use comes to **about $0–25/month** in tokens.
5. **Realtime voice is where costs get mispriced.** Gemini 3.8 Live's sticker price is $0.005/min of audio in and $0.018/min of audio out, with a free tier [11]. OpenAI's gpt-realtime-2.1-mini is $10/$20 per 1M audio tokens [5]. Both, however, **re-bill the conversation context on every turn** [8][18]. Realistic costs are about **$0.02–0.04/min for Gemini Live on short sessions (est.)** and **$0.05–0.08/min measured for OpenAI mini** [10]. A DIY STT→LLM→TTS pipeline runs about **$0.01–0.03/min (est.)**, and managed voice-agent APIs cost $0.05–0.08/min [26][28][29][30][31].
6. **On-device AI on phones works, but only in narrow cases.**
   - **Apple Foundation Models:** about 3B parameters, about 30 tok/s on an iPhone 15 Pro [77], a 4K-token context, and Apple-Intelligence iPhones only [78]. The API is Swift, but Expo can reach it through community modules built on EAS.
   - **Gemini Nano via the ML Kit GenAI Prompt API:** in beta, on select devices, foreground-only, with quotas [75].
   - **Chrome's built-in AI is not available on Android or iOS** [74].
   - **In-browser WebGPU LLMs on phones** run at **4–17 tok/s for models of 1.7B or smaller** [81], and iPhone Safari crashes on 3B models [82].

---

## 1. Delivery paths without a Mac

### 1.1 Feasibility matrix

| Path | Build from Windows? | Get it onto an **iPhone** | Get it onto **Android** | Time for a recruiter to try it | Mic / camera | Background audio | Push | On-device AI access | Fit for a TS/Python dev |
|---|---|---|---|---|---|---|---|---|---|
| **PWA** | ✅ Fully | **Free.** Open the URL; install via Share → Add to Home Screen (iOS 26+: every Home Screen site opens as a web app [68]) | **Free.** Open the URL; Chrome shows an install prompt | **~10 s** (tap link or scan QR) | ✅ `getUserMedia` over HTTPS. iOS standalone mode has known permission re-prompt bugs [86b] | Android OK. **iOS stops audio when minimized or locked** (community reports through iOS 26.x [86]) | Android ✅. iOS only after Add to Home Screen (16.4+), and permission must come from a user gesture [72] | WebGPU/WASM small models only. **No** Apple Foundation Models. **No** Chrome built-in AI on mobile [74] | ★★★★★ |
| **Expo / React Native + EAS** | ✅ EAS builds iOS in the cloud; Android builds locally or on EAS. No iOS Simulator on Windows | **$99/yr**, then either TestFlight (≤100 internal, ≤10,000 external, public link, Beta App Review for external [60]) or ad hoc (≤100 registered iPhones/yr [55]). Expo Go on the App Store runs SDK 54 only [53] | **Free** APK link via EAS internal distribution [55]. Play costs $25 plus the 12-tester/14-day rule [62] | iOS: ~1–3 min via TestFlight public link (after review). Android: ~1–2 min for an APK plus warnings | ✅ Native | ✅ Native background modes | ✅ APNs/FCM | Apple Foundation Models via `@react-native-ai/apple` [80]. Gemini Nano via a custom Kotlin module | ★★★★☆ |
| **Capacitor** (wraps the web app) | Android ✅. iOS needs **Xcode 26 on macOS** [64], so use a cloud Mac: Codemagic (500 free M2 min/mo [66]), GitHub macOS runners, or Capawesome. Ionic Appflow is sunsetting [67] | $99/yr plus a cloud Mac | Free APK or Play | Same as native | ✅ Plugins | ✅ Plugins | ✅ | Via plugins | ★★★☆☆. Reuses the PWA, but you can't debug iOS locally |
| **Flutter** | Android ✅. iOS needs macOS + Xcode [65], so Codemagic | $99/yr plus a cloud Mac | Free APK or Play | Same as native | ✅ | ✅ | ✅ | Via plugins | ★★☆☆☆. Dart is a new language, so it's slower to ship |
| **Native Android** (Kotlin/Compose) | ✅ Android Studio | ❌ | APK or Play | ~1–2 min (APK) | ✅ | ✅ | ✅ FCM | **Best on Android:** ML Kit GenAI/AICore, LiteRT, NPU | ★★★☆☆ (Kotlin is new) |
| **Native iOS** (Swift) | ❌ Xcode is macOS-only | – | – | – | – | – | – | Direct Apple Foundation Models | Not feasible |

### 1.2 What PWAs can do in 2026

| Capability | iOS / iPadOS (Safari, Home Screen web app) | Chrome on Android | Source |
|---|---|---|---|
| Install | No prompt. The user goes to Share → Add to Home Screen. **In iOS 26 every site added this way opens as a web app, and a manifest isn't required** ("zero requirements for installability"). Third-party browsers can offer Add to Home Screen (16.4+) | Install prompt / WebAPK | [68][70] |
| Mic and camera | `getUserMedia` works. Standalone mode has a long-standing bug that re-prompts for permission (WebKit bug 215884) | ✅ | [86b] |
| Recording / codecs | Safari 26 added ALAC/PCM in MediaRecorder and WebCodecs AudioEncoder/Decoder | ✅ | [68] |
| **Background audio** | ❌ Unreliable. Home Screen apps stop audio when minimized or locked. It improved in 26.1, but sequential playback still fails while locked (3rd-party reports) | ✅ with Media Session | [86] |
| Web Push | ✅ Only for Home Screen web apps (16.4+). Permission must be requested on a user gesture. Declarative Web Push (no service worker) arrived in 18.4 | ✅ Also works without install | [70][71][72] |
| Badging, Wake Lock | ✅ 16.4+ | ✅ | [70] |
| WebGPU | ✅ Safari 26 (iOS, iPadOS, macOS, visionOS), with compute shaders | ✅ Chrome 121+ on Android 12+ with Qualcomm or ARM GPUs | [68][73] |
| WASM | SIMD 16.4+. **JSPI in Safari 27** (2026-09-17) | SIMD/threads long supported | [69][70] |
| Built-in on-device LLM | ❌ | ❌ The Prompt API/Gemini Nano is desktop-only ("Chrome for Android, iOS… not yet supported"; page updated 2026-08-26) | [74] |
| Safari 27 (2026-09-17) | A "quality" release with 1,100+ fixes, Service Worker static routing, WASM JSPI, and the `<model>` element. **No new PWA, push or audio capabilities** | – | [69] |

### 1.3 Expo / React Native specifics (the realistic native path from Windows)

- **EAS Build.** You can build and submit iOS apps from any OS; Expo's FAQ points Windows and Linux users to EAS Build and EAS Submit [56]. The free plan includes **15 iOS and 15 Android builds per month** on a low-priority queue with a 45-minute timeout. Starter costs $19/mo and includes $45 of build credit. Pay-as-you-go builds cost $2 for a medium iOS build and $1 for a medium Android build [52].
- **Expo Go is not a distribution channel in 2026.** A version of Expo Go for SDK 55 was still "waiting for approval" on the App Store in May 2026. Expo now describes Expo Go as a learning playground, and "SDK 55 and higher are not available on the Apple App Store" [53][54]. `eas go` builds a personal copy of Expo Go for any SDK and pushes it to *your* TestFlight team, which requires the $99 account [54]. EAS Update URLs open in Expo Go **on Android only** [56]. You *can* still prototype on your own iPhone for free with App Store Expo Go if you stay on SDK 54 and avoid custom native modules (no WebRTC, no Apple Foundation Models).
- **Internal distribution:** iOS ad hoc builds need a paid account, device UDIDs, and **at most 100 iPhones per year**. Android builds are a plain APK link [55].
- **TestFlight:** up to 100 internal testers (team members) and up to 10,000 external testers via a public link. The first external build must pass App Review [60], and builds expire after 90 days (3rd-party guides [61]).

### 1.4 Android distribution specifics

- **Play Console** costs $25 once. **Personal accounts created after 2023-11-13 must run a closed test with ≥12 testers opted in for 14 continuous days before production.** The requirement dropped from 20 testers in December 2024 [62].
- **Developer verification** covers apps installed on *certified* Android devices [63]:
  - **Timeline:** limited-distribution accounts and the "advanced flow" launched in August 2026. **Enforcement starts 2026-09-30 in Brazil, Indonesia, Singapore and Thailand**, and the global rollout follows in 2027.
  - **ADB installs are exempt.**
  - **Free "limited distribution" account:** for students and hobbyists, covering up to 20 devices with no government ID and no fee.
  - **Full distribution account:** $25.
  - **Advanced flow:** users who install unverified apps face a one-time 24-hour wait.
  - For a US recruiter nothing changes in 2026, but APK sideloading carries more friction every year.

### 1.5 "Can a recruiter try it in 30 seconds?" ranking

1. **PWA URL or QR code, ~10 s.** Add a guest or demo mode so there's no signup wall, and add per-IP quotas plus a CAPTCHA (e.g., Cloudflare Turnstile) so the endpoint isn't abused.
2. **A phone number for a voice agent, ~20 s.** The recruiter dials and talks, with nothing to install. It costs about $1–1.15/mo for the number plus per-minute fees (§3.4). Inbound calls avoid most TCPA risk (§3.5).
3. **A web build of the native app** (Expo web export) at a URL, ~10–20 s.
4. **Android APK link, ~1–2 min.** The recruiter has to allow unknown sources and click through Play Protect warnings.
5. **TestFlight public link, ~2–3 min.** It needs the TestFlight app, and only works after Beta App Review.

In every case, also put a 60–90 s screen recording at the top of the README.

---

## 2. Model APIs and pricing (per 1M tokens, standard tier, 2026-09-28)

### 2.1 Text and vision LLMs

| Provider | Model | Input | Cached input | Output | Notes |
|---|---|---|---|---|---|
| Anthropic [1] | **Claude Haiku 4.5** | $1.00 | $0.10 | $5.00 | 200K context. Uses the older tokenizer |
| | **Claude Sonnet 5.5** | $2.00 | $0.20 | $10.00 | 1M context. Its tokenizer produces about 30% more tokens for the same text (Claude 4.7+) [1]. `thinking:{type:"disabled"}` returns a 400, so use `between_tools` or low effort [4] |
| | Claude Sonnet 5 | $2.00 | $0.20 | $10.00 | The $2/$10 introductory price became standard, and the planned 9/1 increase was cancelled [1] |
| | **Claude Opus 5.5** | $4.00 | $0.20 | $20.00 | Thinking is always on and effort defaults to medium. Fast mode costs $8/$40 [1][4] |
| | **Claude Fable 5.1** | $10.00 | $0.25 | $50.00 | Most capable. Thinking is always on [1][4] |
| | *Extras* | | | | Batch API is 50% off. Web search costs $10 per 1k searches; web fetch is free. New users get a small amount of free credit [1] |
| OpenAI [5][6] | **GPT-6 Luna** | $0.10 | $0.01 | $0.50 | "Most efficient… high-volume" |
| | **GPT-6 Sol** | $2.00 | $0.20 | $10.00 | Coding and agentic work |
| | GPT-6 Astra | $10.00 | $1.00 | $50.00 | Top model. Long-context rates are 2× |
| | GPT-5.6 Sol (previous generation) | $4.00 | $0.40 | $20.00 | Promotional pricing runs "at least through Nov 21, 2026" [5] |
| Google [11][12] | **Gemini 3.8 Flash** | $0.75 (**$1.50 from 2027-01-01**) | $0.075 | $3.75 (**$7.50 from 2027**) | Free tier ✅ |
| | Gemini 3.5 Flash-Lite | $0.30 | $0.03 | $2.50 | Free tier ✅ |
| | **Gemini 3.1 Flash-Lite** | $0.25 ($0.50 audio) | $0.025 | $1.50 | Free tier ✅ |
| | Gemini 2.5 Flash-Lite | $0.10 ($0.30 audio) | – | $0.40 | Free tier ✅ |
| | Gemini 3.1 Pro Preview | $2.00 (≤200k) | $0.20 | $12.00 | **No free tier** |
| | Gemma 4 | free tier only | – | – | [11] |
| Groq [21][22] | GPT-OSS-120B / GPT-OSS-20B | $0.15 / $0.075 | – | $0.60 / $0.30 | ~500 / ~1,000 tok/s. Free plan allows 30 RPM, 1K RPD and 200K tokens/day. Whisper v3 Turbo costs $0.04/hr |
| Cerebras [23] | GPT-OSS-120B, Qwen 3.8-27B | 3rd-party rate card: $0.35 in / $0.75 out for 120B | – | – | **The open free tier was replaced by a Free Trial:** $5 in credits, requires a card, expires in 30 days, capped at 1M tokens/day and 5 RPM (change dated July 2026 per 3rd-party [95]) |
| Cloudflare Workers AI [25] | Llama 3.1 8B fp8 / Llama 3.2 1B | $0.045 / $0.027 | – | $0.384 / $0.201 | **10,000 neurons/day free** (about $0.11/day of usage), then $0.011 per 1k neurons. Whisper $0.0005/min, MeloTTS $0.0002/min |
| OpenRouter [24] | Pass-through pricing | – | – | – | 5.5% fee on card top-ups. `:free` models allow **50 req/day** (1,000/day after buying ≥$10 of credits) |
| Vercel AI Gateway [27] | Any model | list price | – | list price | No markup. Free tier covers a subset of models with a monthly free credit (3rd-party: $5 per 30 days), which **stops once you buy credits** |
| xAI [26] | grok-4.3 | $1.25 | – | – | Voice: $0.08/min (see §3) |

**Reasoning tokens:** Opus 5.5, Fable 5.1, Sonnet 5.5, Gemini 3.x and GPT-6 bill thinking tokens as output. On chat routes, use low effort or minimal thinking, or visible-output costs can grow 2–5× (est.).

### 2.2 Cost per 1,000 typical app requests (3,000 input + 400 output tokens) (est.)

The cached column assumes 2,000 of the 3,000 input tokens are cache reads, and it ignores cache-write surcharges (Claude charges 1.25× on 5-minute cache writes).

| Model | No caching | With ~2/3 of input cached |
|---|---|---|
| Workers AI Llama 3.1 8B | $0.29 | – |
| GPT-6 Luna | $0.50 | $0.32 |
| Groq GPT-OSS-120B | $0.69 | – |
| Gemini 3.1 Flash-Lite | $1.35 | ~$0.90 |
| Gemini 3.5 Flash-Lite | $1.90 | ~$1.36 |
| Gemini 3.8 Flash (2026 price) | $3.75 | ~$2.40 |
| **Claude Haiku 4.5** | $5.00 | ~$3.20 |
| Claude Sonnet 5.5 / GPT-6 Sol | $10.00 | ~$6.40 |
| Gemini 3.1 Pro Preview | $10.80 | – |
| Claude Opus 5.5 | $20.00 | ~$12.40 |
| Claude Fable 5.1 / GPT-6 Astra | $50.00 | – |

### 2.3 Vision

- **Claude** [3] charges `⌈w/28⌉×⌈h/28⌉` tokens per image.
  - A 1000×1000 image is **1,296 tokens**.
  - A 1920×1080 image is 1,560 tokens on standard-tier models such as Haiku 4.5, but **2,691** on high-resolution models (Claude 4.7 and later, which includes Sonnet 5.5, Opus 5.5 and Fable 5.1).
  - Per 1,000 one-megapixel photos: Haiku about $1.30, Sonnet 5.5 about $2.60, Opus 5.5 about $5.20.
  - Downscale phone photos to about 1–1.5 MP before upload.
- **OpenAI realtime image input:** $5/1M on gpt-realtime-2.1 and $0.80/1M on mini [5].
- **Gemini Live image/video input:** $1.00/1M, which works out to about **$0.002/min** of camera video [11].

### 2.4 Free tiers and account gotchas

- **Gemini** [11][13][14]:
  - **Coverage:** the free tier includes Flash, Flash-Lite, Live and TTS. Pro is not free.
  - **Limits:** per-model limits appear only in AI Studio. 3rd-party trackers disagree, citing roughly 10–15 RPM and 1,000–1,500 RPD for Flash-class models [94].
  - **Data use:** **free-tier content is used to improve Google products.**
  - **Paid tier:** requires a $5 prepayment. Tier 1 is capped at $250/mo.
  - **Cloud credits:** Google Cloud's $300 credit **can't be spent on the Gemini API for accounts opened after 2026-03-02** [14].
- **Anthropic** [2]:
  - New organizations may start in a lower "Evaluation" tier.
  - The Start tier's standard limit is 1,000 RPM (2M ITPM for Haiku 4.5 and Sonnet 5.5) with a **$500/mo spend cap**. You can set a lower cap yourself.
  - Cached reads don't count toward ITPM.
- **OpenAI:** there is no general free tier. Organizations that opt into data sharing may qualify for complimentary daily tokens on some models, but the official help page returned 403, so current terms are unverified [92].

### 2.5 Student credits and programs

| Program | What you get | Caveats | Source |
|---|---|---|---|
| GitHub Student Developer Pack | Azure $100 credit; Heroku $13/mo for 24 months; MongoDB Atlas $50; free domain (Namecheap .me, .TECH, Name.com); Sentry; New Relic; Datadog Pro (2 yrs); Copilot Student; Codespaces Pro; Appwrite Education | – | [87] |
| Azure for Students | **$100 for 12 months, no credit card**, renewable while a student | Can't be spent on **Marketplace offers**. Claude in Foundry is billed via Marketplace, so it's likely excluded | [88][1] |
| AWS Free Tier (new accounts after 2025-07-15) | Up to **$200** ($100 at signup + $100 for guided tasks); usable on Bedrock | Free-plan accounts **close after 6 months** | [89] |
| Google Cloud | $300 for 90 days | **Not usable for the Gemini API** on accounts opened after 2026-03-02. Use the Gemini free tier instead | [14][90] |
| Anthropic Claude Campus / Builder Clubs | Ambassadors get a $3,600 stipend; clubs share API credits | 2026–27 applications **closed 2026-09-12** (3rd-party) | [91] |
| Modal | **$30/mo free compute** (Starter). Academics (grad students and labs) can get up to $10k | – | [50] |
| Vendor trial credits | Deepgram **$200**; AssemblyAI $50; Cerebras $5 (30 days); LiveKit Cloud 1,000 agent-min/mo + $2.50 of inference; ElevenLabs 10k credits/mo (free plan, **no commercial license**); Cartesia 20K credits/mo | – | [28][29][23][32][30][31] |

---

## 3. Realtime voice

### 3.1 Speech-to-speech options (per conversation-minute: assumes 50/50 talk and ~4 turns/min)

| Option | Unit price | Sticker $/min | Realistic $/min | Notes |
|---|---|---|---|---|
| **Gemini 3.8 Live** (stable; launched 2026-09-15) [11][15][19] | Audio in $3/1M (≈$0.005/min); audio out $12/1M (≈$0.018/min); text in $0.75; video in ≈$0.002/min | ~$0.014 | **~$0.02–0.04 for 1–3 min sessions; ~$0.10 for 10-min sessions without context limits (est.)** | **Free tier: "Free of charge"** (data used to improve Google products). Function calling and Search grounding supported. **Ephemeral tokens let the browser or phone connect directly** [17]. Sessions are limited to 15 min audio-only and **2 min audio+video** without compression; connections last ~10 min, with 2-h resumption tokens [16]. Also available: "Extended Thinking" variant at the same price |
| OpenAI gpt-realtime-2.1-mini [5][8] | Audio $10 in / $0.30 cached / $20 out per 1M; 600 tokens/min in, 1,200 tokens/min out | ~$0.018 floor (est.) | **$0.05–0.08 typical; up to ~$0.15 with heavy context (measured, 4,000 sessions)** [10] | WebRTC from browsers using server-minted ephemeral client secrets [9] |
| OpenAI gpt-realtime-2.1 | Audio $32 in / $0.40 cached / $64 out per 1M | ~$0.05 floor (est.) | **~$0.15–0.25** (about 3× mini [10]) | Too expensive for a $0–20/mo budget |
| OpenAI GPT-Live 1 [7] | $0.05/min, billed per second | $0.05 + backend model | – | Full-duplex. Reasoning and tools are delegated to a backend model, which is billed separately |
| xAI grok-voice-think-fast-2.0 [26] | $0.08/min | $0.08 | – | The 1.0 model was $0.05/min (3rd-party) |
| Deepgram Voice Agent API [28] | $0.075/min ($0.05 with your own LLM+TTS) | $0.05–0.075 | same | Managed STT + LLM + TTS. Covered by the $200 credit |
| AssemblyAI Voice Agent API [29] | $0.075/min all-in | $0.075 | same | – |
| ElevenLabs Agents [30] | $0.08/min beyond included minutes | $0.08 | – | – |
| Cartesia Agents [31] | $0.06/min (+$0.014/min for Cartesia phone numbers) | $0.06 | – | – |

**Why the sticker price isn't the bill**

- **Gemini Live** "charges you per turn for all tokens present in the session context window… past tokens are re-processed" at the audio input rate. Audio accumulates at about 25 tokens/s. Google recommends `contextWindowCompression`, for example a 25k-token trigger with an 8k sliding window [18].
  - *Worked example (est.):* a 3-minute call with 12 turns accumulates context at about 1,500 tokens/min. Summed over all turns, that is about 29k audio tokens billed (≈$0.09), plus 1.5 min of output (≈$0.03), for **≈$0.12 per call, or ≈$0.04/min**. A 10-minute call with no compression costs about $1.
  - Set a low compression trigger and cap session length.
- **OpenAI** also resends the whole conversation on every response, but cached audio input costs only $0.30–0.40/1M, and `retention_ratio` helps keep cache hits [8]. Measured sessions show that capping history (e.g., 10 items) and response length avoids "5–10×" cost blowups [10].

### 3.2 DIY pipeline (STT → LLM → TTS) components

| Stage | Options (per minute of that stage) | Source |
|---|---|---|
| **STT (streaming)** | AssemblyAI Universal-Streaming **$0.0025**; OpenAI gpt-4o-mini-transcribe $0.003 (gpt-transcribe $0.0045; live-transcribe $0.017); Deepgram Nova-3 $0.0048 promo / $0.0077 regular; **Deepgram Flux** (turn-taking) $0.0065 promo; ElevenLabs Scribe v2 Realtime $0.0065; Gemini 3.5 Transcribe Live about $0.009 blended. Batch: Workers AI Whisper $0.0005; Groq Whisper v3 Turbo $0.00067 | [29][5][28][30][11][25][21] |
| **LLM** (≈8k input + 240 output tokens per voice-minute) | GPT-6 Luna **~$0.001**; Gemini 3.1 Flash-Lite ~$0.0024; Groq GPT-OSS-20B ~$0.0007; **Claude Haiku 4.5 ~$0.004 cached / $0.009 uncached**; Sonnet 5.5 ~$0.008–0.018 (est.) | [1][5][11][21] |
| **TTS** (0.5 min of assistant speech ≈ 450 chars) | Workers AI MeloTTS ~$0.0001; **Gemini 3.8 Flash-Lite TTS $0.0045** (= $0.0015 per 10 s; free tier; price doubles on 2027-01-01); Gemini 3.8 Flash TTS $0.0068; OpenAI gpt-4o-mini-tts ~$0.0075 ($12/1M audio tokens); Deepgram Aura-2 $0.0135 ($0.030 per 1k chars); ElevenLabs Flash $0.018 ($0.04 per 1k chars); Cartesia ~$0.018–0.023 | [25][11][5][28][30][31] |
| **Transport / orchestration** | LiveKit Cloud Build (free): **1,000 agent-min/mo, 5 concurrent sessions, 5,000 WebRTC participant-min, $2.50 of inference credit**, then $0.01/agent-min. Ship plan $50/mo. Alternatively self-host Pipecat or LiveKit Agents (Fly.io ~$4–6/mo per small VM, or Modal) | [32][47] |
| **Total** | **Budget ≈ $0.008/min** (AssemblyAI + GPT-6 Luna + Gemini Flash-Lite TTS). **Mid ≈ $0.025/min** (Deepgram Flux + Haiku 4.5 + Aura-2). **Premium ≈ $0.04/min** (Scribe RT + Sonnet 5.5 + ElevenLabs). Add $0–0.01/min for orchestration (est.) | – |

An open-source local TTS (e.g., Kokoro) or Whisper on the RTX 5070 is fine for **development and evals**, but not for hosting a public demo (see Traps).

### 3.3 Telephony (US)

| Carrier | Number | Inbound | Outbound | Media stream | Recording | Source |
|---|---|---|---|---|---|---|
| Twilio | $1.15/mo local; $2.15 toll-free | $0.0085/min local; $0.022 toll-free | $0.014/min | Media Streams $0.0044/min. ConversationRelay (managed STT/TTS bridge) $0.07/min | $0.0025/min | [33] |
| Telnyx | $1.00/mo | $0.0032/min* | $0.005/min* | $0.0035/min | $0.002/min | [34] |
| Bundled | Cartesia $0.014/min on its own numbers; LiveKit third-party SIP $0.004/min | – | – | – | – | [31][32] |

*The Telnyx page labels these rates "SIP trunk." Programmable call-control rates may be slightly higher.*

For 1,000 inbound minutes, Twilio (voice + Media Streams) costs about $12.90 plus $1.15 for the number, and Telnyx about $6.70 plus $1.

### 3.4 Legal notes for AI voice (US, not legal advice)

- **TCPA.** The FCC's Declaratory Ruling FCC 24-17 (adopted 2024-02-08) treats AI-generated voices as **"artificial or prerecorded voice."** Calls using them therefore need the called party's **prior express consent** (and prior express **written** consent for telemarketing), absent an emergency or an exemption. The FCC, state attorneys general and private plaintiffs can all enforce this [35].
- **Pending AI rules.** An FCC NPRM from August 2024 proposes an AI disclosure at the start of calls and AI-specific consent language. It is **still pending**, and its timing is uncertain [36].
- **Recording and interception.** Streaming a call to an STT/LLM vendor is effectively recording it. **All-party consent states include Maryland (relevant for a UMD student), California, Florida, Illinois, Massachusetts, Montana, Nevada, New Hampshire, Pennsylvania, Washington and Delaware.** Connecticut, Michigan, Oregon and Vermont are mixed (3rd-party compilation [37]). Open every call with something like *"You're talking to an AI assistant; this call is recorded and transcribed."*
- **SMS.** Texting US numbers from a 10-digit number requires **A2P 10DLC registration**: about $4.50 for a sole-proprietor brand, a **$15** campaign vetting fee, and $2–10/month per campaign. Approval can take days [38].
- **Portfolio-safe design:**
  - Use **inbound** calls ("call this number") or **in-app** voice.
  - **Never auto-dial consumers or third parties** (for example, "AI calls restaurants for you" is a legal and ethical minefield).
  - If you call the user back, only call their own verified number after an explicit, logged opt-in, and support STOP.

---

## 4. Hosting free tiers (2026-09-28)

| Service | Free tier | Cheapest paid | Sleep / expiry gotchas | Best use | Source |
|---|---|---|---|---|---|
| **Cloudflare Workers** | 100k requests/day; **10 ms CPU per invocation** (awaiting I/O doesn't count) | $5/mo: 10M requests + 30M CPU-ms | None, no cold-start sleep | API and LLM proxy, token minting, static PWA hosting | [40] |
| Cloudflare D1 | 5M rows read/day, 100k written/day, 5 GB | Included in $5 plan | Scales to zero | Relational app data | [41] |
| Cloudflare R2 | 10 GB-month, 1M Class A ops, 10M Class B ops, **free egress** | $0.015/GB-month | – | Uploads, **hosting on-device model weights** | [42] |
| Cloudflare Durable Objects | SQLite-backed DOs on the free plan: 100k requests/day, 13k GB-s/day, 5 GB | $5 plan | WebSocket messages billed 20:1; hibernation supported | Realtime rooms, rate limits, per-user state | [43] |
| Cloudflare Workers AI | 10k neurons/day | $0.011 per 1k neurons | – | Cheap LLM, Whisper, TTS fallback | [25] |
| **Vercel Hobby** | 1M function invocations, 4 active-CPU-hrs, 100 GB transfer, 300 s max duration | Pro $20/mo | **Non-commercial, personal use only.** If you hit a limit you usually wait 30 days | Next.js frontend | [39] |
| **Supabase Free** | 500 MB DB, 50k MAU auth, 1 GB storage, 500k Edge invocations, 200 realtime connections, 2 projects | Pro $25/mo | **Projects pause after 1 week of inactivity** | Postgres + auth + pgvector | [44] |
| **Convex Free** | 1M function calls, 0.5 GB DB, 1 GB files, 20 GB-hrs actions, 1 GB egress | $25 per dev per month | – | Reactive TS backend | [45] |
| **Neon Free** | 100 projects; 100 CU-hrs per project; 0.5 GB per project; 5 GB egress | Launch: pay-as-you-go $0.106/CU-hr | Scales to zero after 5 min (brief cold start) | Serverless Postgres | [46] |
| Fly.io | No documented ongoing free allowance (trial only) | shared-cpu-1x 256 MB ≈ $3.89/mo; 1 GB ≈ $11.66/mo | – | Long-lived voice-agent worker | [47] |
| Railway | $5 trial credit for 30 days (no card), then $1/mo of credit | Hobby $5/mo (includes $5 usage) | The trial ends | Container backend | [48] |
| Render | 750 instance-hours/mo | – | **Spins down after 15 min** (slow cold start). **Free Postgres expires after 30 days.** Key Value is in-memory only | Avoid for live demos | [49] |
| **Modal** | **$30/mo free compute** | Per-second GPU: T4 ≈ $0.59/hr, L4 ≈ $0.80/hr, A10 ≈ $1.10/hr, L40S ≈ $1.95/hr, H100 ≈ $3.95/hr | Cold starts on scale-to-zero GPUs | Bursty GPU inference (Whisper, TTS, small VLMs), batch evals | [50] |
| Hugging Face Spaces | CPU Basic (2 vCPU, 16 GB) sleeps when idle. **ZeroGPU:** free accounts can host 2 Spaces (Gradio only). Visitors get 2 min/day unauthenticated, 5 min/day free, 40 min/day PRO | PRO $9/mo; T4 Space $0.40/hr | Queues, daily quotas, Gradio-only | ML demo side-page or model card, not an app backend | [51] |

---

## 5. On-device AI on phones in 2026

### 5.1 Apple Foundation Models

- **Model:** Apple's model is about 3B parameters. On an iPhone 15 Pro it reaches **~0.6 ms per prompt token to first token and ~30 tokens/s** [77].
- **Context:** the on-device window is **4,096 tokens**, shared between prompt and response. At WWDC26, iOS 27 added **image input** and a `LanguageModel` protocol that also wraps cloud models (3rd-party WWDC26 summaries [79]).
- **Devices:** **iPhone 15 Pro/Pro Max and iPhone 16 models or later**, with device and Siri language matched. Apple's support page now lists iOS 27 for Apple Intelligence [78]; the framework itself shipped with iOS 26.
- **Does it need Swift, Xcode or a Mac?** The API is Swift, and building normally needs Xcode, which runs only on macOS. **But** community React Native/Expo modules exist: `@react-native-ai/apple` from Callstack is a Vercel AI SDK provider with streaming and structured output, and needs RN 0.80+ with the New Architecture [80]. Others include expo-foundation-models and react-native-apple-llm. **EAS Build compiles them on Expo's cloud Macs, so it's feasible from Windows.** You still need:
  - the $99 account;
  - a physical Apple-Intelligence iPhone;
  - patience, because there is no simulator or local Swift debugging.

### 5.2 Gemini Nano via ML Kit GenAI / AICore (Android)

- **APIs:** Summarization, Proofreading, Rewriting and Image Description are in **beta**. **The Prompt API is beta** and takes text or image + text, returning text or structured output [75].
- **Devices** (sample): Pixel 9/10/11 series, Galaxy S25/S26 and Z Fold7/8 and Z Flip8, OnePlus 13/15, Xiaomi 15/17, plus OPPO, vivo, Motorola, Honor and others. Gemini Nano versions v2, v3 and v4 vary by device [75].
- **Restrictions:** **inference is allowed only while the app is the top foreground app.** AICore enforces a **per-app inference quota** (returns `BUSY`) and a **battery quota** [75].
- **Access:** it requires native Android code (Kotlin), which you can write in an **Expo Module built in Android Studio on Windows**. It is **not reachable from the web.**

### 5.3 Chrome built-in AI on mobile

- **Not available.** Chrome's docs state: "Chrome for Android, iOS… are not yet supported by the APIs which use foundation models."
- Desktop requires more than 4 GB of VRAM, 16 GB of RAM and 22 GB of free disk. The Prompt API has been stable since Chrome 138 on desktop [74].

### 5.4 WebGPU / WASM LLMs in mobile browsers

- **Speed:** the LlamaWeb paper (arXiv 2605.20706, May 2026) grouped mobile GPUs into a "low cluster" with **4–17 tok/s decode**. That covers only the smallest models (Gemma3-270M, LFM2.5-350M, Qwen3-0.6B, Bonsai-1.7B). The paper also reports iOS Safari tab memory **below 500 MB** [81].
- **Crashes:** WebLLM on iOS 26 Safari runs SmolLM2-135M, but **Qwen2.5-3B crashes the tab after downloading** [82].
- **Binding limits:** phones cap storage bindings around 256 MB (3rd-party dev notes [86c]).
- **Verdict:** in a phone browser, stick to **≤1B models or task-specific small models** (VAD, embeddings, OCR, classifiers, tiny STT). Don't run chat LLMs there.

### 5.5 Realistic tokens/s (decode) for 1–4B models on phones

| Runtime / device | Model | tok/s | Source |
|---|---|---|---|
| Apple FM, iPhone 15 Pro (native) | ~3B Apple on-device model | ~30 | [77] official |
| MLC Chat on Hexagon NPU, Galaxy S25 Ultra (Snapdragon 8 Elite) | Qwen3 1.7B | ~40 | [83] 3rd-party |
| Snapdragon 8 Elite (NPU, Qualcomm AI Hub) | Llama 3.2 1B (w4 / w4a16) | 34 / 54 | [84] |
| Snapdragon 8 Elite | Llama 3.2 3B | ~10 | [85] 3rd-party |
| Galaxy S25 Ultra: CPU → NPU across apps | Phi-4-mini (3.8B, Q4) | 10–22 | [83] 3rd-party |
| Pixel (Tensor), CPU-only apps | Phi-4-mini | 10–18 | [83] 3rd-party |
| Mobile browser WebGPU (iPhone 17 Pro Max, Galaxy S24, Mali, PowerVR) | ≤1.7B | 4–17 | [81] |

### 5.6 Where on-device actually earns its place

Good jobs for on-device models:
- Voice activity detection or barge-in
- Wake word
- OCR (ML Kit or Vision)
- Embeddings for local search
- PII redaction before upload
- Offline summarization or rewrite on supported flagships

Keep reasoning and tool use in the cloud. A "works in airplane mode" demo is a strong talking point, but always ship a cloud fallback.

---

## 6. Monthly cost at demo scale (~100 users, light use) (est.)

**Assumptions:**
- **Text:** 5,000 LLM requests/month (50 per user), each 3k input + 400 output tokens; 1,000 of them include a ~1 MP photo.
- **Voice:** 1,500 voice-minutes/month (15 min per user).
- **Hybrid:** 60% of requests handled on-device.
- **Excluded:** one-time costs other than the ones shown.

| Line item | **A. PWA + serverless + cheap LLM** | **B. Expo app + realtime voice** | **C. On-device-first + cloud fallback** |
|---|---|---|---|
| Store / developer fees | $0 | Apple **$8.25/mo** ($99/yr). Play $25 once (optional) | $8.25/mo if iPhone; **$0 Android-only** (APK or limited-distribution account) |
| Build | $0 | EAS free (15+15 builds/mo) | EAS free |
| Hosting + DB + auth | $0 (Workers/D1/R2, or Supabase/Neon/Convex free) | $0–5 | $0 (R2 or HF for weights) |
| LLM / vision tokens | **Free tier $0** (Gemini free, Workers AI). **GPT-6 Luna ~$3.** Gemini 3.1 Flash-Lite ~$7. Haiku 4.5 ~$17–27. Sonnet 5.5 / GPT-6 Sol ~$35–55 | Small, if any, outside voice | 40% fallback: GPT-6 Luna ~$1; Flash-Lite ~$3; Haiku ~$7–10 |
| Voice (1,500 min) | – (optional: Gemini Live from the browser, same as B) | **Gemini Live free tier $0.** Gemini Live paid ~$30–60. **DIY pipeline ~$15–45** (Deepgram's $200 credit covers months). OpenAI realtime-mini ~$75–120. OpenAI realtime full ~$225–375 | – |
| Optional phone line | – | Twilio ≈ $21/mo (number + 1,500 min + Media Streams). Telnyx ≈ $11 | – |
| Domain | $0 (Student Pack) to ~$1 | same | same |
| **Total (low / typical / high)** | **$0 / ~$3–10 / ~$30–55** | **~$8 / ~$40–75 / $100–400** | **$0 / ~$10–15 / ~$20** |

Rule of thumb: text AI at this scale is effectively free. **Voice minutes and the Apple fee are the only things that break a $20/month budget.**

---

## 7. Recommended default stacks

### Stack 1: web-first PWA (default pick; $0–10/mo)
- **Frontend:** Vite + React (or Next.js) PWA via `vite-plugin-pwa`, mobile-first UI, installable, Web Push, camera and mic.
- **Backend:** Cloudflare Workers (Hono) + D1/R2 + Durable Objects for sessions and rate limits. Supabase or Convex are alternatives if you want auth, Postgres or a reactive DB. Beware Supabase's 1-week pause.
- **AI:** a server-side model router:
  - Gemini 3.x Flash-Lite/Flash for bulk work (free tier in development);
  - GPT-6 Luna or Claude Haiku 4.5 as the cheap production tier;
  - Claude Sonnet 5.5 for hard reasoning or tool-use steps, with prompt caching.
- **Voice (optional):** Gemini 3.8 Live over WebSocket, using **ephemeral tokens minted by the Worker** so no key ships to the client.
- **Why:**
  - it reaches **any phone with zero install, gives a recruiter a ~10 s try, and has no Apple or Google fees and no Mac**;
  - it's all TypeScript, so you can iterate fastest with AI agents;
  - it shows AI-engineering depth (routing, caching, evals, cost dashboards, streaming).
- **Accepts:** iOS PWAs can't play audio in the background or lock screen, iOS push needs Add to Home Screen first, and there's no access to Apple's or Google's on-device models.

### Stack 2: Expo native + voice ($8–60/mo)
- **App:** an Expo SDK 56 **development build** (not Expo Go). Distribute with EAS Build free, a TestFlight public link ($99/yr), and an Android APK link. Also ship **Expo web** so recruiters have a URL.
- **Voice:** either Gemini 3.8 Live (WebSocket), or LiveKit Agents / Pipecat running Deepgram Flux → Haiku 4.5 or GPT-6 Luna → Aura-2 or Gemini Flash-Lite TTS.
- **Backend:** Workers or Convex.
- **Pick this when** the product *needs* native: background or lock-screen audio, reliable push, share sheet, widgets, or on-device models.
- **Budget for:** the $99 fee, a few days for Beta App Review, rebuilds every 90 days, and **per-user minute caps**.

### Stack 3: hybrid on-device-first (Android-first; $0–20/mo)
- **App:** Expo with custom Expo Modules. A Kotlin module calls the ML Kit GenAI Prompt API (Gemini Nano). A Swift module (via `@react-native-ai/apple`) calls Apple Foundation Models.
- **Fallback:** cloud calls through a Worker, with on-device perception (VAD, OCR, embeddings) everywhere.
- **Pick this when** the story is privacy, offline use or zero marginal cost, **and** your own phone is a supported device (Pixel 9+ or Galaxy S25+, or iPhone 15 Pro and newer).
- **Risks:** beta APIs, a 4K context, foreground-only execution and quotas, limited device coverage, and Swift without local debugging. Always keep a cloud path and a video demo.

**Decision by phone.**
- **Android phone:** Stack 1 or Stack 3 is free end to end.
- **iPhone:** Stack 1 is free. Stack 2 or 3 costs $99/yr. For free iPhone prototyping, App Store Expo Go works on SDK 54 only.
- **Don't pick:** Flutter (a new language, and iOS still needs a cloud Mac), Capacitor (only worth it later, to wrap an existing PWA), or native iOS (impossible without a Mac).

---

## 8. Traps to avoid

1. **Treating Expo Go as a distribution channel.** Expo Go on the iOS App Store is frozen at SDK 54 (as of 2026). On iOS it can't open other people's projects, and it can't load custom native code. Real iPhone installs need the $99 account with TestFlight or ad hoc [53][54][56].
2. **Assuming TestFlight is instant or permanent.** External testers need Beta App Review, and builds expire after about 90 days [60][61]. Ad hoc builds are capped at 100 iPhones per year [55].
3. **Planning on a Play Store listing within the build window.** New personal accounts need 12 testers opted in for 14 days first [62]. Use an APK link or Play internal testing for the demo.
4. **Designing around iOS PWA features that don't exist:**
   - no install prompt;
   - push only after Add to Home Screen;
   - audio dies when the phone locks;
   - microphone permission can re-prompt;
   - WebGPU tabs have tight memory (Safari reloads the tab; 3B models crash) [81][82][86];
   - Chrome's built-in AI (Gemini Nano) is **not** on mobile [74].
5. **On-device hype.** Phones realistically run 1–4B models at 10–40 tok/s natively and ≤1.7B models at 4–17 tok/s in the browser. Apple Foundation Models has a 4K context, and ML Kit is foreground-only with quotas. Coverage is limited to recent flagships [75][77][78][81][83].
6. **Trusting voice sticker prices.** Both Gemini Live and OpenAI Realtime re-bill context on every turn. Cap session length and history, use Gemini context compression (§3.1) and OpenAI `retention_ratio`, and set **per-user daily minute limits** and provider spend caps [8][10][18]. Also note that Gemini Live audio+video sessions stop after 2 minutes unless compression is on [16].
7. **Free tiers that sleep, pause or expire right when a recruiter clicks:**
   - Supabase pauses after 1 week of inactivity [44];
   - Render sleeps after 15 min, and its free Postgres dies after 30 days [49];
   - HF Spaces sleep; Modal has GPU cold starts;
   - Railway's trial is $5 for 30 days [48];
   - the Cerebras free tier is now a 30-day $5 trial [23];
   - the Google Cloud $300 credit doesn't cover Gemini for new accounts [14].
8. **Vercel Hobby is non-commercial only** [39]. That's fine for a portfolio, but move to Cloudflare or Pro if you monetize.
9. **Sending real users' data through free tiers that train on it.** Gemini free-tier content is used to improve Google products [11][14]. Disclose this, or use the paid tier (a $5 prepay) once real users arrive.
10. **Shipping API keys to the client.** Use Gemini Live ephemeral tokens [17] and OpenAI Realtime client secrets [9], proxy everything else, and set spend limits (Anthropic's own spend limit and $500 Start-tier cap [2], Gemini tier caps [14], Vercel AI Gateway budgets [27]).
11. **Letting thinking tokens run unchecked.** Opus 5.5 and Fable 5.1 always think, and Sonnet 5.5 can't simply disable thinking (use `between_tools` or low effort) [4]. On chat routes, set low effort; Claude 4.7+ also tokenizes about 30% heavier [1].
12. **Outbound AI calling.** AI voice counts as "artificial voice" under the TCPA, so outbound calls need prior express (written, for marketing) consent [35]. Maryland and 10+ other states require all-party consent to record [37]. SMS needs A2P 10DLC [38]. Keep calls inbound or in-app, and open with an AI and recording disclosure.
13. **Using the laptop GPU as production.** A tunnel to your RTX 5070 dies when the laptop sleeps. Use it for development, evals, fine-tuning (QLoRA on 1–4B models) and batch jobs, not for the live demo.
14. **Firebase AI Logic**, if you use it, **requires App Check from 2026-11-02** [20].
15. **Using OpenRouter `:free` or the Groq free plan as the production tier.** They allow 50 req/day [24] and 1K req/day / 200K tokens/day [22] respectively. That's fine for development but not for 100 users at once.
16. **Gemini 3.8 Flash and Flash TTS prices double on 2027-01-01** [11]. Budget for 2027 if the demo lives on.

---

## 9. Source conflicts and open questions

- **OpenAI naming.** A summarized fetch first returned GPT-5.6-Sol and GPT-5.6-Luna as the flagships. The raw pricing HTML and the models page list **GPT-6 Astra, Sol and Luna** first, with GPT-5.6 as the previous generation [5][6]. I used GPT-6 prices from the raw page. The `gpt-4o-mini-tts` price ($12/1M audio tokens) comes from the page's collapsed "All models" section.
- **Gemini free-tier limits** aren't published per model in the docs (only in AI Studio). 3rd-party trackers conflict: about 10–15 RPM and about 1,000–1,500 RPD [13][94]. Verify in AI Studio before relying on the free tier for a live demo, especially for **Live API concurrency**.
- **Gemini Live's realistic cost is my estimate**, derived from the official "re-bill context per turn" rule [18]. I found no measured public dataset. Log `usage_metadata` in week 1.
- **Cerebras.** A 3rd-party source says the 1M tokens/day free tier was replaced on 2026-07-21. The official page shows a "Free Trial" with 1M TPD **and** $5 credits that expire in 30 days [23][95].
- **iOS PWA background audio and mic re-prompts** come from community reports and a WebKit bug, not from Apple docs [86]. Test on the actual phone.
- **Mobile WebGPU memory.** The LlamaWeb paper reports iOS Safari tabs below 500 MB [81]. Other developers report a 1 GB `maxBufferSize` on some iPhones (3rd-party). Either way, 3B models crashed [82].
- **Apple Intelligence minimum OS.** The support page now says iOS 27 [78], while Foundation Models shipped in iOS 26 and `@react-native-ai/apple` targets iOS 26 [80].
- **Unverified pricing and program details:**
  - xAI's 1.0 voice price ($0.05/min) is 3rd-party; 2.0 at $0.08/min is official [26].
  - The Vercel AI Gateway "$5 per 30 days" figure is 3rd-party; the official page only says there's a monthly free credit [27].
  - TestFlight's 90-day expiry comes from 3rd-party guides [61].
  - Claude Campus details are 3rd-party [91].
  - The OpenAI complimentary-token program is unverified (403) [92].
  - The Appflow sunset dates (no new apps from 2026-10-01; shutdown 2027-12-31) come from Capawesome, Ionic's migration partner [67].

---

## 10. Sources (all accessed 2026-09-28)

**Anthropic**
- [1] Anthropic Pricing: https://platform.claude.com/docs/en/about-claude/pricing
- [2] Anthropic Rate limits: https://platform.claude.com/docs/en/api/rate-limits
- [3] Anthropic Vision: https://platform.claude.com/docs/en/build-with-claude/vision
- [4] Anthropic `claude-api` skill reference, model table and API notes (cached 2026-09-25)

**OpenAI**
- [5] OpenAI API Pricing (raw HTML parsed): https://developers.openai.com/api/docs/pricing
- [6] OpenAI Models: https://developers.openai.com/api/docs/models
- [7] OpenAI GPT-Live 1: https://developers.openai.com/api/docs/models/gpt-live-1
- [8] OpenAI Realtime costs guide: https://developers.openai.com/api/docs/guides/realtime-costs
- [9] OpenAI Realtime (WebRTC, client secrets): https://developers.openai.com/api/docs/guides/realtime
- [10] 3rd-party: "OpenAI Realtime API Pricing in 2026: Real-World Data From 4,000 Measured Sessions," https://hackernoon.com/openai-realtime-api-pricing-in-2026-real-world-data-from-4000-measured-sessions

**Google / Gemini**
- [11] Gemini API pricing (raw HTML parsed): https://ai.google.dev/gemini-api/docs/pricing
- [12] Gemini models: https://ai.google.dev/gemini-api/docs/models
- [13] Gemini rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- [14] Gemini billing: https://ai.google.dev/gemini-api/docs/billing
- [15] Gemini 3.8 Live: https://ai.google.dev/gemini-api/docs/models/gemini-3.8-live
- [16] Live API session management: https://ai.google.dev/gemini-api/docs/live-api/session-management
- [17] Live API ephemeral tokens: https://ai.google.dev/gemini-api/docs/live-api/ephemeral-tokens
- [18] Live API best practices (billing): https://ai.google.dev/gemini-api/docs/live-api/best-practices
- [19] Google blog, Gemini 3.8 Live launch: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/ (launch date 2026-09-15 per 3rd-party coverage)
- [20] Firebase AI Logic Live API limits: https://firebase.google.com/docs/ai-logic/live-api/limits-and-specs

**Other model and AI-infrastructure providers**
- [21] Groq models: https://console.groq.com/docs/models
- [22] Groq rate limits: https://console.groq.com/docs/rate-limits
- [23] Cerebras rate limits / free trial: https://inference-docs.cerebras.ai/support/rate-limits
- [24] OpenRouter FAQ: https://openrouter.ai/docs/faq
- [25] Cloudflare Workers AI pricing: https://developers.cloudflare.com/workers-ai/platform/pricing/
- [26] xAI API pricing: https://docs.x.ai/developers/pricing
- [27] Vercel AI Gateway pricing: https://vercel.com/docs/ai-gateway/pricing

**Voice and telephony**
- [28] Deepgram pricing: https://deepgram.com/pricing
- [29] AssemblyAI pricing: https://www.assemblyai.com/pricing
- [30] ElevenLabs API pricing: https://elevenlabs.io/pricing/api and plans: https://elevenlabs.io/pricing
- [31] Cartesia pricing: https://cartesia.ai/pricing
- [32] LiveKit Cloud pricing: https://livekit.com/pricing
- [33] Twilio US voice pricing: https://www.twilio.com/en-us/voice/pricing/us
- [34] Telnyx call control pricing: https://telnyx.com/pricing/call-control

**Legal**
- [35] FCC Declaratory Ruling FCC 24-17: https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf and https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal
- [36] FCC AI robocall NPRM (Federal Register, 2024-09-10): https://www.federalregister.gov/documents/2024/09/10/2024-19028/implications-of-artificial-intelligence-technologies-on-protecting-consumers-from-unwanted-robocalls
- [37] 3rd-party state recording-consent compilation: https://callsprout.com/blog/call-recording-laws-by-state (and similar 2026 guides)
- [38] Twilio A2P 10DLC vetting FAQ: https://help.twilio.com/articles/11587910480155-A2P-10DLC-Campaign-Vetting-FAQ (fees per Twilio and 3rd-party summaries)

**Hosting**
- [39] Vercel pricing: https://vercel.com/pricing and Hobby plan: https://vercel.com/docs/plans/hobby
- [40] Cloudflare Workers pricing: https://developers.cloudflare.com/workers/platform/pricing/
- [41] Cloudflare D1 pricing: https://developers.cloudflare.com/d1/platform/pricing/
- [42] Cloudflare R2 pricing: https://developers.cloudflare.com/r2/pricing/
- [43] Cloudflare Durable Objects pricing: https://developers.cloudflare.com/durable-objects/platform/pricing/
- [44] Supabase pricing: https://supabase.com/pricing
- [45] Convex pricing: https://www.convex.dev/pricing
- [46] Neon pricing: https://neon.com/pricing
- [47] Fly.io pricing: https://docs.fly.io/about/pricing/
- [48] Railway pricing: https://railway.com/pricing
- [49] Render free tier: https://render.com/docs/free
- [50] Modal pricing: https://modal.com/pricing
- [51] Hugging Face pricing: https://huggingface.co/pricing and ZeroGPU: https://huggingface.co/docs/hub/spaces-zerogpu

**Mobile delivery**
- [52] Expo EAS pricing: https://expo.dev/pricing
- [53] Expo changelog, "Expo Go and the App Store in May 2026": https://expo.dev/changelog/expo-go-and-app-store-may-2026
- [54] expo/fyi, Deploy Expo Go to TestFlight (`eas go`): https://github.com/expo/fyi/blob/main/deploy-expo-go-testflight.md
- [55] Expo internal distribution: https://docs.expo.dev/build/internal-distribution/
- [56] Expo FAQ: https://docs.expo.dev/faq/
- [57] Expo build setup: https://docs.expo.dev/build/setup/
- [58] Apple Developer Program: https://developer.apple.com/programs/
- [59] Apple fee waivers: https://developer.apple.com/help/account/membership/fee-waivers/ (via search summary)
- [60] Apple TestFlight: https://developer.apple.com/testflight/
- [61] 3rd-party TestFlight guides on 90-day expiry, e.g. https://techconcepts.org/blog/testflight-guide
- [62] Google Play testing requirements for new personal accounts: https://support.google.com/googleplay/android-developer/answer/14151465
- [63] Android developer verification: https://developer.android.com/developer-verification and FAQ: https://developer.android.com/developer-verification/guides/faq
- [64] Capacitor environment setup: https://capacitorjs.com/docs/getting-started/environment-setup
- [65] Flutter iOS setup: https://docs.flutter.dev/platform-integration/ios/setup
- [66] Codemagic pricing: https://codemagic.io/pricing/
- [67] Appflow sunset and alternatives: https://capawesome.io/blog/alternative-to-appflow/ (3rd-party; Ionic migration partner)

**Web platform**
- [68] WebKit, Safari 26.0 features: https://webkit.org/blog/17333/webkit-features-in-safari-26-0/
- [69] WebKit, Safari 27.0 features (released 2026-09-17): https://webkit.org/blog/18325/webkit-features-for-safari-27-0/
- [70] WebKit, Safari 16.4 features: https://webkit.org/blog/13966/webkit-features-in-safari-16-4/
- [71] WebKit, Safari 18.4 features (Declarative Web Push): https://webkit.org/blog/16574/webkit-features-in-safari-18-4/
- [72] WebKit, Web Push for web apps on iOS: https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/
- [73] Chrome, What's New in WebGPU (Chrome 121, Android): https://developer.chrome.com/blog/new-in-webgpu-121
- [74] Chrome Prompt API (built-in AI requirements; last updated 2026-08-26): https://developer.chrome.com/docs/ai/prompt-api

**On-device AI**
- [75] ML Kit GenAI (devices, limits): https://developers.google.com/ml-kit/genai and Prompt API: https://developers.google.com/ml-kit/genai/prompt/android
- [76] Android Gemini Nano: https://developer.android.com/ai/gemini-nano
- [77] Apple ML Research, "Introducing Apple's On-Device and Server Foundation Models": https://machinelearning.apple.com/research/introducing-apple-foundation-models
- [78] Apple Intelligence device requirements: https://support.apple.com/en-us/121115
- [79] WWDC26, "What's new in the Foundation Models framework": https://developer.apple.com/videos/play/wwdc2026/241/ plus 3rd-party summaries (e.g., https://ivanmagda.dev/posts/wwdc26-foundation-models-year-two/)
- [80] Callstack `@react-native-ai/apple`: https://www.callstack.com/blog/on-device-apple-llm-support-comes-to-react-native and https://ai-sdk.dev/providers/community-providers/react-native-apple
- [81] "Llamas on the Web" (LlamaWeb), arXiv 2605.20706: https://arxiv.org/html/2605.20706v1
- [82] mlc-ai/web-llm issue #753 (iOS 26 Safari crash on 3B): https://github.com/mlc-ai/web-llm/issues/753
- [83] 3rd-party Android local LLM benchmarks 2026: https://www.promptquorum.com/power-local-llm/best-local-llm-apps-android-2026
- [84] Qualcomm AI Hub, Llama-v3.2-1B-Instruct: https://huggingface.co/qualcomm/Llama-v3.2-1B-Instruct
- [85] 3rd-party, LLMs on Snapdragon 8 Elite: https://grapeup.com/blog/running-llms-on-device-with-qualcomm-snapdragon-8-elite

**iOS PWA community reports**
- [86] MacRumors forum, "iOS 26 audio issues in PWA web apps": https://forums.macrumors.com/threads/ios-26-audio-issues-in-pwa-web-apps-not-fixed-in-26-1-or-26-2-but-much-better.2466839/ and prototyp.digital PWA audio write-up
- [86b] WebKit bug 215884 (standalone getUserMedia re-prompts): https://bugs.webkit.org/show_bug.cgi?id=215884
- [86c] 3rd-party phone WebGPU notes: https://github.com/Nehanth/swarmllm/issues/65

**Student credits and programs**
- [87] GitHub Student Developer Pack: https://education.github.com/pack
- [88] Azure for Students: https://azure.microsoft.com/en-us/free/students
- [89] AWS Free Tier ($200 credits, 6-month free plan): https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/
- [90] Google Cloud free program: https://docs.cloud.google.com/free/docs/free-cloud-features
- [91] 3rd-party, Claude Campus Ambassador program 2026: https://www.opportunitiesforafricans.com/the-claude-anthropic-campus-ambassador-program-2026/
- [92] OpenAI data-sharing help article (403 on fetch): https://help.openai.com/en/articles/10306912 and community thread https://community.openai.com/t/good-news-extended-free-tokens-on-traffic-shared-with-openai/1241322
- [93] Modal academic credits: https://modal.com/pricing (see [50])
- [94] 3rd-party Gemini free-tier trackers, e.g. https://pecollective.com/tools/gemini-free-tier-guide/ and https://tokenmix.ai/blog/gemini-api-free-tier-limits
- [95] 3rd-party, Cerebras free-tier change: https://costbench.com/software/llm-api-providers/cerebras-inference/free-plan/
