# 01 · Reddit Pulse — demand, excitement & fatigue for AI apps (esp. on phones)

*Research date: 2026-09-28 · Slice: Reddit · Window: Sep 2025 → Sep 2026, weighted to Mar–Sep 2026 · Scores = upvotes ("pts") and comments ("c") as archived; see method notes.*

---

## TL;DR — ranked findings

1. **Backlash against low-effort AI is the loudest signal on Reddit in 2026 — Strong.** Builder subs are in open revolt against wrappers and vibe-coded slop (r/selfhosted's Huntarr security fiasco: 8,603 pts; *"Apparently we can't call out apps as AI slop anymore…"*: 2,797 pts / 1,011 c; r/SideProject *"Petition to ban AI wrappers from the sub wholesale"*: 642). Mainstream subs are hostile to AI being pushed on them (doctor's-office AI consent: 20,426; *"I fired my therapist because she told me to use AI"*: 24,472; r/apple *"Why is Apple asking me to pay more for Big Tech's AI obsession?"*: 4,339). **Implication:** the project must be visibly *not slop* — a real problem, engineering rigor, privacy, no dark-pattern subscription, and lead with the outcome rather than "AI".
2. **The new LLM phone assistants are "smarter but worse at the basics" — Strong, very fresh.** Siri AI (Gemini-powered, shipped with iOS 27 on Sep 14–15 behind a waitlist) and Gemini (fully replaced Google Assistant this month) get hammered for slow, wordy, unreliable execution of simple commands: r/GooglePixel *"Probabilistic LLMs do not belong in a virtual assistant"* (638), r/Android *"Gemini is failing at a basic task Android could do in 2014"* (1,692), r/iphone *"Apple Intelligence is not impressive"* (599 / 271 c; top comment: *"90% of my Siri use is 'set timer for 15 minutes'"*). Where they *do* delight, it's cross-app personal context and camera→action (*"New Siri Camera can log my blood pressure"*: 1,003). **Implication:** the gap is reliable, fast, verifiable *action* — not more chat — and don't fight Siri/Gemini head-on.
3. **What wins the "wow" on Reddit is real-time perception of the physical world, not chat — Strong.** Top AI-flavoured builds: live politician fact-checker (12,146), handwriting notebook where Claude writes back (3,881), neural net that erases the cage from fight footage (2,728), head-tracking parallax wallpaper (2,395), phone-camera lifting-form checker (1,341, Sep 26), push-up duels counted by the camera (369), DeepMind sign-language-to-text on phones (3,151).
4. **"Remember it for me and nudge me at the right moment" is the deepest recurring need — Strong need, but trust gates it.** r/ADHD *"I wish there was an app that would take the mental load of having to remember everything"* (1,963; *"I… literally ignore every push notification… If only there was app that would call me like a personal assistant would"*); r/productivity's *"What do you still do manually because every app for it is bad?"* → top answer *"todo lists… and random things i want to remember"* (264). Meanwhile, memory features spook people (ChatGPT/Gemini leaking a stranger's data into chats: 718 / 440 c; *"Deleting a ChatGPT conversation doesn't mean ChatGPT forgets it"*: 585).
5. **"AI got me a concrete win" advocate/triage stories dominate the positive posts — Strong.** Health (calf strain → suspected clot: 6,582; *"25 years… one Claude conversation cracked it"*: 4,818; stroke caught: 2,457; *"Gemini saved my life"*: 3,064) and money (photo of a $1,800 dealer quote → goodwill warranty: 2,609). People love AI when it turns a scary document or situation into the next right action.
6. **Privacy / local / open-source is table stakes for anything with deep phone access — Medium-Strong.** On an Android "AI controls your phone" app: *"Needs to be open source to even be considered for an app that takes over my phone"* (572 on a 232-pt post). On-device is now credible (PokeClaw: Gemma 4 on-device driving Android, 323; Bonsai 27B on an iPhone, 729; 2.6B tool-calling model at 30 tok/s on a phone, 220).
7. **Students: logistics, reading load and loneliness are the real pains; AI-as-cheating is radioactive — Medium.** Canvas outage during finals (2,088), *"attending the wrong class section all semester"* (2,616), r/GradSchool *"How in the world do you read?"* (151 / 80 c), a UMD anti-loneliness app (136) — versus *"I wish ai never existed"* (786), capstone tests faked with Claude (900), Turnitin false accusations (812).

---

## How this was researched (and caveats)

- **Access.** WebFetch to reddit.com is blocked and Reddit's JSON API returns 403, so I pulled data two other ways:
  - **Reddit RSS** (`/top/.rss?t=year|month`, `/search.rss?restrict_sr=on&sort=top&t=year`) — **81 listings/searches** across 40+ subreddits: r/SideProject, r/LocalLLaMA, r/ChatGPT, r/ClaudeAI, r/OpenAI, r/singularity, r/artificial, r/AI_Agents, r/androidapps, r/iphone, r/apple, r/Android, r/GooglePixel, r/Siri, r/GeminiAI, r/productivity, r/ADHD, r/selfhosted, r/indiehackers, r/AppIdeas, r/vibecoding, r/college, r/csMajors, r/GradSchool, r/UMD, and others. Top listings are rank-ordered by score.
  - The **Arctic Shift** Reddit archive API, used for scores (6,460 posts), comment trees (**~53 threads read with top comments**), and full post dumps for student subs (r/college Jan–Apr and Aug 13–Sep 28, 2026; r/UMD and r/GradSchool Aug 13–Sep 28, 2026; ~13.5k posts).
  - About a dozen WebSearch/WebFetch calls covered non-Reddit context (WWDC/iOS 27, the Gemini transition, a16z's March 2026 list, AI-wearable news). The session's shared web-search budget then ran out. Everything else here came from the direct Reddit pulls.
- **Metrics.** "pts" is the net upvote score captured by the archive about 36 h after posting, so final scores can be higher. Comment scores on very recent threads (last ~3 days) are under-counted. "Top of year" means the past 365 days, so some items date from Oct–Dec 2025; I labelled those.
- **Biases.** High upvote counts skew toward memes and news. Some subs suppress AI talk (r/ADHD returns almost nothing for "AI"; r/GradSchool pushes it into a weekly megathread; r/college barely discusses it), which under-counts AI demand from those groups. Builder subs over-represent builders.
- **Evidence-strength rubric.** **Strong** = several subs, ≥1k-pt threads, and the pattern recurs over months. **Medium** = one or two subs, hundreds of points, or a consistent low-engagement drumbeat. **Weak** = a single thread, low engagement, or my own inference.
- Sections marked *Evidence* are what Reddit shows. Sections marked *What this means for our pick* are my inference.

---

## 2026 context that shapes Reddit sentiment

| When | Event (Reddit thread / source) |
|---|---|
| Jan 2026 | OpenClaw (ex-Clawdbot) goes viral as a personal agent in WhatsApp/Telegram. OpenAI acquires it on Feb 15 ([r/OpenAI, 1,849 pts](https://www.reddit.com/r/OpenAI/comments/1r5rnbl/)). |
| Jan 12 | *"Apple picks Google's Gemini to run AI-powered Siri"* ([r/apple, 3,219 / 574 c](https://www.reddit.com/r/apple/comments/1qaxp5a/)) |
| Feb 28 | *"Cancel your ChatGPT Plus… switch to Claude"* ([r/ChatGPT, 25,153 / 1,621 c](https://www.reddit.com/r/ChatGPT/comments/1rh60py/)); Claude hits #1 in the App Store ([r/ClaudeAI, 5,644](https://www.reddit.com/r/ClaudeAI/comments/1rhgsjz/)) |
| Apr 2 | Gemma 4 released; on-device agents follow ([r/LocalLLaMA, 2,177 / 630 c](https://www.reddit.com/r/LocalLLaMA/comments/1salgre/)) |
| May 20 | Google I/O 2026 backlash: *"Makes me want to sell my phone"* ([r/Android, 1,498 / 350 c](https://www.reddit.com/r/Android/comments/1ti82w9/)) |
| Jun 8 | WWDC: "Siri AI" (Gemini-based, personal context, in-app actions, dedicated Siri app) ([r/iphone, 1,173 / 370 c](https://www.reddit.com/r/iphone/comments/1u0ff2x/); [Business Standard](https://www.business-standard.com/technology/tech-news/wwdc-2026-apple-unveils-siri-ai-gemini-powered-apple-intelligence-more-126060900042_1.html)) |
| Aug 5 | *"Google Assistant shutting down on Android and Wear OS in September"* ([r/Android, 1,286 / 460 c](https://www.reddit.com/r/Android/comments/1vfx659/)) |
| Sep 3–22 | GPT-6 Astra, then Sol/Luna; Claude Opus 5.5 ships Sep 22 and Sonnet 5.5 Sep 28. Frontier models now one-shot games and apps, which makes "look what I built" less impressive by itself. |
| Sep 14–15 | iOS 27 ships Siri AI, **waitlisted, English-only, no EU** ([MacRumors](https://www.macrumors.com/2026/09/15/ios-27-siri-ai-has-waitlist-how-to-join/), [Engadget](https://www.engadget.com/2261054/why-siri-ai-ios-27-waitlist/)) |
| Sep 24 | Pixel 11 tests "Call for Me", where Gemini phones businesses on your behalf ([r/Android, 141](https://www.reddit.com/r/Android/comments/1wp921u/)) |
| Sep 28 | *"Gemini fully replaces Google Assistant on Android"* ([r/Android](https://www.reddit.com/r/Android/comments/1wsqo9y/)) |

---

## Part A — Which AI projects/apps got traction in 2026, and why (ranked)

### A1. Real-time perception of the physical world (camera / mic → instant feedback) — **Strong**

*Evidence*

| Thread | Sub | Date | pts / c |
|---|---|---|---|
| [built a factchecker that catches politicians lying in real time](https://www.reddit.com/r/ClaudeAI/comments/1u9esua/) | r/ClaudeAI | 2026-06-18 | 12,146 / 696 |
| [I built a handwriting notebook app where Claude writes back](https://www.reddit.com/r/ClaudeAI/comments/1vxqbzs/) | r/ClaudeAI | 2026-08-25 | 3,881 / 207 |
| [DeepMind SL2T: deaf users can now sign into their phones instead of typing](https://www.reddit.com/r/singularity/comments/1vmflo1/) | r/singularity | 2026-08-12 | 3,151 / 177 |
| [Claude Code skill that turns a photo of your handwriting into an installable font](https://www.reddit.com/r/ClaudeAI/comments/1v55he0/) | r/ClaudeAI | 2026-07-24 | 2,884 / 147 |
| [Training a custom neural network to erase the cage from fight footage](https://www.reddit.com/r/SideProject/comments/1rluzt2/) | r/SideProject | 2026-03-05 | 2,728 / 149 |
| [I used Astra to build a Yu-Gi-Oh! AR app for SPECS](https://www.reddit.com/r/OpenAI/comments/1wpg5k8/) | r/OpenAI | 2026-09-24 | 2,577 / 127 |
| [Wallpaper that shifts perspective when you move your head](https://www.reddit.com/r/SideProject/comments/1rs969i/) | r/SideProject | 2026-03-13 | 2,395 / 217 |
| [Automated pigeon defense system (CV + water gun)](https://www.reddit.com/r/SideProject/comments/1s9ywir/) | r/SideProject | 2026-04-01 | 2,200 / 112 |
| [I built an app that tells me when my lifting form is wrong](https://www.reddit.com/r/SideProject/comments/1wqsd4f/) | r/SideProject | 2026-09-26 | 1,341 / 108 |
| [Website that turns hand movements into electronic music](https://www.reddit.com/r/SideProject/comments/1veanaw/) | r/SideProject | 2026-08-03 | 1,166 / 139 |
| [New Siri Camera can log my blood pressure](https://www.reddit.com/r/iphone/comments/1wp1zpx/) | r/iphone | 2026-09-24 | 1,003 / 42 |
| [Digital body measurements from two images](https://www.reddit.com/r/SideProject/comments/1tkw5uv/) | r/SideProject | 2026-05-22 | 814 / 78 |
| [I accidentally built something Huawei is now adding to their camera (posing guide)](https://www.reddit.com/r/SideProject/comments/1sufbg4/) | r/SideProject | 2026-04-24 | 784 / 81 |
| [Draw math in the air with your finger, AI solves it on the board](https://www.reddit.com/r/SideProject/comments/1u88cf5/) | r/SideProject | 2026-06-17 | 703 / 94 |
| [Push-ups against a random stranger, live; the camera counts for both](https://www.reddit.com/r/SideProject/comments/1w74cif/) | r/SideProject | 2026-09-04 | 369 / 80 |

What the comments add:
- Fact-checker: *"This needs to be made into something that can run on a phone using the mic."*
- Lifting-form app: *"Would be cool if the beep… could be a spoken cue… in your earbud you hear 'back too arched'."* Skeptics called it *"probably… arbitrarily selected acceptable angle ranges"* and *"vibe coded"*.
- Push-up duel: the dev says *"Most of the dev time went into [rep validation]… I keep a folder of videos"* — in effect an eval set.
- Siri Camera BP: *"That's genius"* (206); *"small automation that makes health tracking much more realistic without buying new… hardware."*
- r/AppIdeas asked explicitly for a [*"zero mental load" AI barbell coach](https://www.reddit.com/r/AppIdeas/comments/1t100ns/) (May 2026): camera rep counting, earbud tempo tones, and auto weight selection.

*Why it resonated (inference):* the value shows up in a 5–15 s video with no explanation needed, it's clearly not a chat wrapper, and it has a visible "hard part" (CV, latency, consistency) that commenters respect.

*What this means for our pick:* build the demo around a live camera/mic moment on the phone, with the output overlaid or spoken back immediately. Expect skeptics to ask "how do you know it's right?", so plan a labelled eval set and publish accuracy numbers. That is also the engineering-depth story.

### A2. "AI got me a concrete win" — advocate & triage in stressful moments — **Strong**

| Thread | Sub | Date | pts / c |
|---|---|---|---|
| [ChatGPT talked me out of toughing out a calf strain… suspected a blood clot](https://www.reddit.com/r/ChatGPT/comments/1r2mooz/) | r/ChatGPT | 2026-02-12 | 6,582 / 387 |
| [25 years. Multiple specialists. Zero answers. One Claude conversation cracked it.](https://www.reddit.com/r/ClaudeAI/comments/1s41fny/) | r/ClaudeAI | 2026-03-26 | 4,818 / 1,019 |
| [Gemini Saved My Life (oven fumes)](https://www.reddit.com/r/GeminiAI/comments/1rngalv/) | r/GeminiAI | 2026-03-07 | 3,064 / 341 |
| [Claude ran mock interviews for a job I badly wanted… I got it](https://www.reddit.com/r/ClaudeAI/comments/1v7fo9i/) | r/ClaudeAI | 2026-07-26 | 2,888 / 123 |
| [Claude helped me get a traffic light reprogrammed in my town](https://www.reddit.com/r/ClaudeAI/comments/1rphxvk/) | r/ClaudeAI | 2026-03-10 | 2,883 / 141 |
| [ChatGPT saved me $1800 (screenshot of dealer quote → goodwill warranty)](https://www.reddit.com/r/ChatGPT/comments/1w4867a/) | r/ChatGPT | 2026-09-01 | 2,609 / 167 |
| [We almost let my dad sleep through a stroke. ChatGPT is the reason we didn't.](https://www.reddit.com/r/ChatGPT/comments/1wmxjs0/) | r/ChatGPT | 2026-09-22 | 2,457 / 186 |
| [An LLM saved my ass in a roller-coaster queue (urgent invoice, phone only)](https://www.reddit.com/r/ClaudeAI/comments/1uqt53j/) | r/ClaudeAI | 2026-07-08 | 1,974 / 301 |
| [Codex saved me from spending $2,000 on an internet problem I've had for 8 years](https://www.reddit.com/r/ChatGPT/comments/1wbpbxz/) | r/ChatGPT | 2026-09-09 | 985 / 209 |

Comment on the $1,800 thread: *"When my brother died, I wish I had someone/something to tell me what I needed to do."*

*What this means for our pick:* the loved pattern is *photo, screenshot or situation → plain-language meaning → next action (a drafted message, a deadline, a call)*. Today it happens ad hoc in a chat app. A product that makes this reliable, structured and follow-up-able on a phone fits the demand. It needs a safety posture, especially for health, where r/productivity commenters warn *"please don't recommend AI as a mental health resource."*

### A3. Hyper-personal software ("useless to you, perfect for me") — **Medium-Strong**

- [The thing you built with Claude is useless to me… and that's the point](https://www.reddit.com/r/ClaudeAI/comments/1tp3en9/) (r/ClaudeAI, 2026-05-27, 1,273 / 245). Examples: *"An HTML file on someone's phone correlating migraines with barometric pressure, because the App Store wanted 80 bucks a year… A grocery list sorted by the aisle layout of one specific supermarket."*
- [What tool have you built for yourself… that removes so much headache?](https://www.reddit.com/r/ClaudeAI/comments/1wrckhp/) (2026-09-27, 1,062 / 518 — two days old). The OP's tool reads school and activity emails → shared calendar → WhatsApp reminders the day before, including the lunch menu. Other answers: a self-hosted finance app, auto-activating store coupons, an offline "read selected text aloud" app, and an email-anxiety tool from an autistic user.
- [Compiss — compass app to the nearest toilet](https://www.reddit.com/r/ClaudeAI/comments/1vi5guo/) (4,733 / 252); [Monarch-style finance dashboard for <$20](https://www.reddit.com/r/ClaudeAI/comments/1wr140j/) (2,220 / 262); [CapCut replacement people are ditching CapCut for](https://www.reddit.com/r/ClaudeAI/comments/1wgu8g3/) (1,551 / 141); [poker app where phones are the chip stacks](https://www.reddit.com/r/ClaudeAI/comments/1vii2zl/) (1,039).
- Physical output delights: [agentic "Daily Brief" for my kids on a receipt printer](https://www.reddit.com/r/artificial/comments/1tbasiz/) (r/artificial, 658 / 234); [fully local thermal-printer appliance — no cloud, no subscriptions, no accounts](https://www.reddit.com/r/selfhosted/comments/1s9jz4f/) (r/selfhosted, 3,241).

*What this means for our pick:* specificity beats horizontal. A product that feels hand-built for one painful routine (school logistics, bills, one sport) gets love, especially when it replaces a subscription.

### A4. Delightful mobile experiences tied to the real world (mostly non-AI) — **Medium**

[Fog-of-war map of your walks](https://www.reddit.com/r/SideProject/comments/1wbu40o/) (1,855 / 199, 2026-09-09) · [collect every cat you meet as stickers](https://www.reddit.com/r/SideProject/comments/1ntm0tk/) (3,038, Sep 2025) · [ScreenWall: old phones as synced widgets](https://www.reddit.com/r/SideProject/comments/1v66kqo/) (1,415) · [alarm that only stops when you walk to the toilet](https://www.reddit.com/r/SideProject/comments/1s9kov9/) (1,284 / 239).

*What this means for our pick:* the "wow" can be the interaction design (maps, collections, physical gestures), not the model. A polished, playful UI on the phone is part of the signal.

### A5. Local / on-device AI on phones — **Medium** (strong inside r/LocalLLaMA)

- [PokeClaw: Gemma 4 autonomously controls an Android phone, fully on-device](https://www.reddit.com/r/LocalLLaMA/comments/1sdv3lo/) (323 / 144). It uses LiteRT plus the Accessibility API, and NotificationListenerService to read incoming WhatsApp messages. It needs about 8 GB of RAM for Gemma 4 E2B.
- [Bonsai 27B runs locally on an iPhone (3.9 GB)](https://www.reddit.com/r/LocalLLaMA/comments/1uyz9n2/) (729); [2.6B model with tool calling + 128K ctx at 30 tok/s on a phone](https://www.reddit.com/r/LocalLLaMA/comments/1vfn9vc/) (220); [Needle: Gemini tool-calling distilled into a 26M model](https://www.reddit.com/r/LocalLLaMA/comments/1tb9b0r/) (358).
- Use cases people cite: [emergency advice as the sensible reason for an LLM on your phone](https://www.reddit.com/r/LocalLLaMA/comments/1sausgd/) (442 / 164); [offline survival AI, 14k App Store users](https://www.reddit.com/r/SideProject/comments/1qv9yi5/) (874 / 157); [offline Kokoro-TTS audiobook reader](https://www.reddit.com/r/LocalLLaMA/comments/1rop1rp/) (229).
- Ideology: [*"This is why we need local models and opensource harnesses"*](https://www.reddit.com/r/LocalLLaMA/comments/1uvlwz0/) (3,161 / 389); [*"The best model is the one you can actually run"*](https://www.reddit.com/r/LocalLLaMA/comments/1ux9xze/) (1,821).

*What this means for our pick:* an on-device component (OCR/VLM, pose, a small tool-caller) is credible in 2026 and earns goodwill. "Your data never leaves the phone for X" is a strong claim when it's true and testable.

### A6. Personal agents (the OpenClaw effect) — **Medium** among builders, **Weak** among end users

Builders are excited:
- [Claude Code spawned 3 agents that talked to each other](https://www.reddit.com/r/AI_Agents/comments/1qydazj/) (769)
- [I built MARVIN, my personal agent; 4 colleagues use it](https://www.reddit.com/r/AI_Agents/comments/1qluizt/) (296)
- [People underestimate how easy it is to automate your PC with AI now](https://www.reddit.com/r/AI_Agents/comments/1vcvjb9/) (450 / 227)
- [agent that negotiates with my ISP](https://www.reddit.com/r/AI_Agents/comments/1qnz0tf/) (97)
- [AI job-search system, 740+ offers scored, landed a job, open-sourced](https://www.reddit.com/r/ClaudeAI/comments/1sd2f37/) (2,245)

Users are skeptical (see C7). The agent-security incidents people discuss are real: [internal bot leaked the unannounced reorg plan](https://www.reddit.com/r/AI_Agents/comments/1waini0/), [agent deleted an AML control](https://www.reddit.com/r/AI_Agents/comments/1wbh26b/), [Notion's MCP connector prompt-injects ads mid-task](https://www.reddit.com/r/ClaudeAI/comments/1w9dluw/) (2,157), and [self-replicating prompt-injection "AI worms"](https://www.reddit.com/r/artificial/comments/1wr7ayr/).

*What this means for our pick:* agentic features should be scoped, visible, reversible and permissioned. Injection-hardening and idempotent actions are differentiators, not hygiene.

---

## Part B — Unmet needs: "is there an app that…", "I wish AI could…", "why can't Siri/Gemini just…" (ranked)

### B1. Assistants that reliably *do* basic things, fast — **Strong** (Siri AI + Gemini, Jun–Sep 2026)

*Evidence*
- [Probabilistic LLMs do not belong in a virtual assistant](https://www.reddit.com/r/GooglePixel/comments/1vqu4a5/) (r/GooglePixel, 2026-08-17, 638 / 167). The post is a navigation loop in which Gemini says *"Okay, navigating to Dad's *does nothing*"*, asks for confirmation, then fails again.
- [Gemini is failing at a basic task Android could do in 2014](https://www.reddit.com/r/Android/comments/1u6od30/) (1,692 / 309). Comments: *"Call [name]… Before Gemini, it would do this instantly"*; *"so long winded and wordy"*; *"the infuriating 'let me search the web for you'."*
- [Google is getting rid of Google assistant and forcing you to use Gemini now](https://www.reddit.com/r/GooglePixel/comments/1vggv4l/) (812 / 534); [Gemini sucks and is getting worse](https://www.reddit.com/r/GooglePixel/comments/1v13iqf/) (415); [Who else just refuse to use Gemini?](https://www.reddit.com/r/GooglePixel/comments/1u2rvt6/) (395 / 282); [hating the new Gemini Android Auto](https://www.reddit.com/r/GooglePixel/comments/1tjnfy7/) (351 / 206).
- [The power of the new Siri AI…](https://www.reddit.com/r/iphone/comments/1wlo17s/) (r/iphone, 2026-09-20, 3,819 / 320). The image is a gallery I couldn't see. The title reads as sarcastic and the comments are mixed: *"my favourite part is when you try to ask it a question and it just disappears"*, *"Almost useless"*, against *"Personally I'm impressed…"*.
- [Apple Intelligence is not impressive](https://www.reddit.com/r/iphone/comments/1wqmkb1/) (2026-09-26, 599 / 271):
  - The post: *"I had to ask it three times in three different ways to find an email… I could have scrolled… in less time."*
  - Top comment: *"90% of my Siri use is 'set timer for 15 minutes'"* (135).
  - *"Siri AI managed to turn a 'Set a reminder to feed the cats at 6pm' to calling someone I haven't seen in 6 years on whatsapp."*
  - *"it has to process intent (the slow part) first before it can route the request internally."*
- [New Siri AI is somehow better and worse at the same time](https://www.reddit.com/r/iphone/comments/1wo7059/) (65 / 116): *"more accurate than old Siri, and yet somehow still less useful… much slower."* [How do you feel about Siri AI?](https://www.reddit.com/r/iphone/comments/1wmxz7m/) (76 / 90): *"my biggest grief is how SLOW it is"*; *"'You'll need to unlock your iPhone first.' What is the point of hands-free 'hey siri'…"*
- Collateral damage: [iPhone feels like brand new after disabling Apple Intelligence](https://www.reddit.com/r/iphone/comments/1vx9qyu/) (748 / 180); [action button, and Siri still can't control silent mode?](https://www.reddit.com/r/iphone/comments/1s8k4fs/) (1,082). A post from today reads [*"ChatGPT understands 'twenty to eight' instantly. Siri, 15 years in, still sets the wrong alarm"*](https://www.reddit.com/r/ChatGPT/comments/1wsfb6m/).
- Counter-signal: where Siri AI works it wows. [Siri AI transforms the iPhone](https://www.reddit.com/r/apple/comments/1uwi8dh/) (1,532 / 465); [New Siri is honestly impressive](https://www.reddit.com/r/iphone/comments/1ur4nqh/) (627); in [The coolest things I've used the new Siri for](https://www.reddit.com/r/Siri/comments/1wk0ezv/) users report *"take all of my travel emails… put all the relevant information… into a note"* and *"look through my 30,000ish photos… find those screenshots [of book pages]… convert… into [a note]."*

*What this means for our pick:* reliability engineering is a legible, demo-able differentiator: a deterministic fast path, measured p50/p95 latency, confirmations only for risky actions, and success-rate evals. But the OS-assistant slot is platform-locked, and Siri AI is strong at "personal context over Apple apps". Pick a bounded domain where we own the actions and can prove reliability. Don't build "a better Siri".

### B2. External memory + proactive nudges ("take the mental load") — **Strong need**, solutions **Medium**

*Evidence*
- [I wish there was an app that would take the mental load of having to remember everything](https://www.reddit.com/r/ADHD/comments/1o01xfa/) (r/ADHD, **2025-10-07**, 1,963 / 135): *"I've tried a billion reminder and task management apps and literally ignore every push notification… If only there was app that would call me like a personal assistant would."*
- [Time blindness is ruining my life](https://www.reddit.com/r/ADHD/comments/1r15pi6/) (1,878 / 275); [Anyone love setting up "systems", only to lose interest?](https://www.reddit.com/r/ADHD/comments/1upheer/) (1,283 / 130; *"The app/system slowly becomes another thing I have to check, and then I start avoiding it"*).
- [do any of you actually USE your task apps…?](https://www.reddit.com/r/ADHD/comments/1q8co2q/) (161 / 102): *"a graveyard of productivity apps"*, *"the app feels like my disappointed mother."* The only apps that stuck for commenters were Finch (a self-care pet) and home-made Excel checklists. *"I spend more time 'gardening' the app than doing the work."*
- [I need everything to exist in front of me or it doesn't exist](https://www.reddit.com/r/ADHD/comments/1ttupa5/) (257): *"if I have to click through five things… I will probably never look at it again."*
- [What do you still do manually because every app for it is bad?](https://www.reddit.com/r/productivity/comments/1vblphw/) (2026-07-31, 152 / 81) → *"todo lists… and random things i want to remember"* (264), budgeting spreadsheets (124), a shared paper calendar *"everyone at home can check at a glance"* (83).
- AI memory demand:
  - [I built ChatGPT a "Save Game" memory layer](https://www.reddit.com/r/ChatGPT/comments/1r1b3gl/) (1,402 / 237)
  - [open-source memory system scoring 100% on LongMemEval](https://www.reddit.com/r/singularity/comments/1sexr5v/) (5,923 / 544)
  - [I tested 12 AI memory systems across 1,800 tasks — a plain Markdown wiki tied for first](https://www.reddit.com/r/AI_Agents/comments/1wjq4vh/) (Sep 2026). 61% of failures were the agent *not recalling* information it had.
- Trust brakes:
  - [ChatGPT and Gemini both leaked "Alice's" data into my chats](https://www.reddit.com/r/ChatGPT/comments/1u2ra19/) (718 / 440)
  - [ChatGPT can access memories outside "project-only" memory](https://www.reddit.com/r/ChatGPT/comments/1rdei2p/) (644)
  - [PSA: Deleting a ChatGPT conversation doesn't mean ChatGPT forgets it](https://www.reddit.com/r/ChatGPT/comments/1wmfmji/) (585)
  - [You can view a lot of shared [Claude] conversations via Google](https://www.reddit.com/r/ClaudeAI/comments/1v6fiyj/) (7,286 / 1,169)
- Anti-pattern: [I've recorded every class and meeting for six years… it has frozen my life](https://www.reddit.com/r/productivity/comments/1wk3nx2/) (Sep 2026, 177 / 66). Capture without processing or resurfacing makes things worse.

*What this means for our pick:* the need is *resurfacing at the right moment through a channel that cuts through* (a widget or lock-screen presence, then escalation such as a phone call), not more capture. Memory must be inspectable, editable and deletable. Keep a simple store (a markdown or SQLite wiki is competitive) and invest in recall policy and evals. The "call me" ask overlaps the planned Bland voice gateway and could reuse it as an escalation channel rather than being a separate project.

### B3. Point-and-act: camera / screenshot / document → structured action — **Medium-Strong**

*Evidence:*
- Siri Camera → Health BP log (1,003).
- The $1,800 quote screenshot (2,609).
- Siri pulling travel details from emails into a note (r/Siri).
- The school-email → calendar tool (r/ClaudeAI, Sep 27).
- r/AppIdeas complaint-mining lists [*"is this clause normal?" contract red-flag scanner](https://www.reddit.com/r/AppIdeas/comments/1r73tui/) (claims threads with 1,200+ pts in r/freelance) and recurring-task reminders over SMS/WhatsApp (*"the word 'overkill'"* keeps coming up about Notion/Asana).
- Sherlock warning: a low-score r/iphone post argues [*"Apple's new Siri + Visual Intelligence basically killed a ton of nutrition tracking apps"*](https://www.reddit.com/r/iphone/comments/1u0qpg3/) (Weak).

*What this means for our pick:* this is the most phone-native "10-second wow" (point → structured result → one tap to act). To avoid being sherlocked, go deep on a domain Apple/Google won't (non-Apple sources like Gmail, Canvas and school portals; Android plus web; households or shared groups), and add verification: every extracted fact links back to the source pixel or line.

### B4. Trust: privacy, local processing, open source, inspectability — **Medium-Strong**

*Evidence:*
- [What do you actually want from a private AI chat on your phone?](https://www.reddit.com/r/LocalLLaMA/comments/1qmir5d/) (zerotap, an Android AI-controls-your-phone app, 232 / 82). Top comments: *"Needs to be open source to even be considered for an app that takes over my phone"* (572); *"I don't think I'd want some random dude's AI having full control over my phone"* (121); *"first think of a problem to solve before building an app without purpose"* (101); *"open source, work offline, have an ui that's not ass and buggy. that's it"* (41).
- I/O backlash: *"I don't want Spark always on 24/7 even when my phone is locked. I don't want Google's AI reading my emails"* ([1,498 / 350](https://www.reddit.com/r/Android/comments/1ti82w9/)).
- [Doctor's office AI: consent to feed records into training/advertising or else](https://www.reddit.com/r/mildlyinfuriating/comments/1tv3fg4/) (20,426 / 763).
- Security: [don't allow Gemini on the lock screen (PSA)](https://www.reddit.com/r/Android/comments/1vgkua2/) (395); [Gemini could send SMS without a PIN from the lock screen](https://www.reddit.com/r/Android/comments/1uz44ex/).
- [Are iPhones more private and less AI-infused than Androids?](https://www.reddit.com/r/iphone/comments/1w9qyr1/) (114 / 66).
- A UMD student tool drew *"I'm really concerned with data privacy… the transcript upload thing was genuinely the only thing stopping me"* ([Orbit](https://www.reddit.com/r/UMD/comments/1u7glxy/)).

*What this means for our pick:* default to local-first. Use a transparent server boundary (what leaves the device, and why), open-source the client, add a one-tap "forget", and let users inspect the model's memory and actions. These are also strong README and interview talking points.

### B5. Life-admin plumbing: emails, LMS, schedules → calendar & reminders — **Medium**

*Evidence:*
- The r/ClaudeAI school-email → calendar + WhatsApp tool (above).
- r/college: [Just found out I've been attending the wrong class section all semester](https://www.reddit.com/r/college/comments/1rdhorc/) (2,616); [Canvas Hacked](https://www.reddit.com/r/college/comments/1t6orzl/) (2,088 / 155) — *"it literally happened when i went to grab the rubrics for two papers… due in a few days"* (609); [Canvas notifications going crazy](https://www.reddit.com/r/college/comments/1w32ur1/) (54: *"71 notifications and counting"*).
- Many low-score "how do I plan assignments / track what to study" posts, e.g. [*"planner for assignments besides doing it manually?"*](https://www.reddit.com/r/college/comments/1q78hzr/).
- UMD students already build scheduling tools (Orbit; Jupiterp), which shows the space is contested.

*What this means for our pick:* strong daily-use potential and a natural fit with the developer's Canvas-MCP experience. Deduping, conflict detection and "what do I need to do tonight?" are the valuable parts; raw sync is table stakes. Avoid scheduling/degree-audit tools, which already exist on campus.

### B6. Communication overwhelm (texting and email backlog) — **Medium** (fresh)

*Evidence:*
- [I feel completely overwhelmed by texting people back](https://www.reddit.com/r/ADHD/comments/1wm31ed/) (2026-09-21, 1,118 / 88): *"The more messages I have waiting for me, the more overwhelmed I become… slow processor"*; *"I ruined an old friendship… because of this"* (70).
- [Avoid messages when overwhelmed?](https://www.reddit.com/r/ADHD/comments/1w3smml/) (2026-08-31, 1,149 / 154).
- The autistic user's email-anxiety tool in the r/ClaudeAI thread.
- Tension: AI-written messages are resented. [Is my boss using Gemini to email me?](https://www.reddit.com/r/GeminiAI/comments/1sufzsi/) (2,995 / 371); [I almost let ChatGPT write a condolence email](https://www.reddit.com/r/ChatGPT/comments/1quusc6/) (665 / 258).

*What this means for our pick:* the help people want is *triage and permission* (who is waiting on me, what's urgent, a tiny next step), not ghost-writing. If drafting is included, keep the user's voice and control.

### B7. Proactive, context-aware help without asking ("Google Now" nostalgia) — **Medium-Weak**

*Evidence:* recurring comments in Gemini threads: *"Google Now was straight up scary good, and way ahead of its time"*; *"Google Now… detected I was on a highway that had a major accident and alerted me just in time"*; *"No AI and it would still somehow learn from your usage and give you traffic updates"* ([1vqu4a5](https://www.reddit.com/r/GooglePixel/comments/1vqu4a5/), [1u6od30](https://www.reddit.com/r/Android/comments/1u6od30/)). Proactivity is wanted when it is accurate and quiet. Always-on ambient AI (I/O's "Spark") draws privacy fire.

### B8. Typing over talking in public; latency matters — **Weak-Medium**

*Evidence:* [Does anyone here actually use the Siri feature?](https://www.reddit.com/r/iphone/comments/1tvpdpe/) (392 / 856; *"embarrassed to be using it in public"*); *"The best thing about the Siri AI upgrade is I can type questions… I don't want people around me hearing all my dumb questions"* (r/iphone). Dictation demand persists ([free Wispr Flow alternative for Android?](https://www.reddit.com/r/androidapps/comments/1unewye/)).

*What this means for our pick:* make voice optional. Camera, share-sheet and widget inputs are more socially acceptable than talking.

---

## Part C — Fatigue & backlash: what Redditors mock or ignore (ranked)

### C1. Vibe-coded slop and AI wrappers flooding builder communities — **Strong**

- r/selfhosted:
  - [Huntarr: API keys exposed to anyone on your network](https://www.reddit.com/r/selfhosted/comments/1rckopd/) (8,603 / 1,261). A security review of a *"100% vibe-coded project"* found an auth bypass; the dev *"nuked their repo, and disappeared."*
  - [Apparently we can't call out apps as AI slop anymore…](https://www.reddit.com/r/selfhosted/comments/1rmiwgb/) (2,797 / 1,011): *"vibe-coded projects can introduce very extensive security vulnerabilities… the maintainer doesn't have the capability to fix the issue."*
  - [Mods introduce "Vibe Code Friday"](https://www.reddit.com/r/selfhosted/comments/1qfp2t0/) (1,842); [ban vibe-coded app posts?](https://www.reddit.com/r/selfhosted/comments/1olb7v0/) (1,534, Nov 2025); [im tired of this sub](https://www.reddit.com/r/selfhosted/comments/1rpsky6/) (1,693 / 445); [This subreddit used to be fun](https://www.reddit.com/r/selfhosted/comments/1uwhvce/) (1,394 / 314); [So sick of every other post being written by AI](https://www.reddit.com/r/selfhosted/comments/1rsyb28/) (1,161).
- r/SideProject:
  - [Petition to ban AI wrappers](https://www.reddit.com/r/SideProject/comments/1pgbvrl/) (642 / 132, Dec 2025): *"every single post is a wrapper for ChatGPT. A vibe coded UI and a problem invented so that someone might have the chance to make some money."* Top reply: *"soulless, pointless, and even potentially dangerous security-wise"* (207).
  - [Rant: Stop building useless apps](https://www.reddit.com/r/SideProject/comments/1wgxzx9/) (2026-09-15, 664 / 383); [Your AI generated SaaS is 99.9% likely a waste](https://www.reddit.com/r/SideProject/comments/1w2rwg0/) (228 / 338).
  - Builders now add disclaimers like *"(**Not an AI Wrapper)"* ([example](https://www.reddit.com/r/SideProject/comments/1q46eiu/)).
- r/ClaudeAI itself: [Why the majority of vibe coded projects fail](https://www.reddit.com/r/ClaudeAI/comments/1rt31th/) (6,167 / 579); [Vibe Coding vs. Production reality](https://www.reddit.com/r/ClaudeAI/comments/1t3bk3x/) (3,094); [No one cares what you built](https://www.reddit.com/r/ClaudeAI/comments/1rtey4g/) (881 / 218).
- r/singularity: [POV: When you try using a Vibe Coded Website](https://www.reddit.com/r/singularity/comments/1w2dz61/) (2,394).
- r/UMD: a student team pitched [Third Space](https://www.reddit.com/r/UMD/comments/1s1s6a3/) as a reaction to *"soulless ai slop vibe coded ahh apps"* (136).

*What this means for our pick:* ship like a professional. Publish a security review or threat model, tests and CI, an eval report, "how AI was used in building this", and real usage data. The slop flood raises the value of visible rigor.

### C2. AI shoved into devices and apps (off-switches, battery, ads, subscriptions) — **Strong**

- [Why is Apple asking me to pay more for Big Tech's AI obsession?](https://www.reddit.com/r/apple/comments/1uh4frw/) (4,339 / 774); [iPhone feels like brand new after disabling Apple Intelligence](https://www.reddit.com/r/iphone/comments/1vx9qyu/) (748); [Battery life dethroned price as the #1 purchase driver — and AI doesn't come close](https://www.reddit.com/r/Android/comments/1s53jua/) (956 / 287); [Can't turn off the AI-"enhance" feature on my phone's camera](https://www.reddit.com/r/mildlyinfuriating/comments/1orsc2m/) (20,082, Nov 2025).
- r/androidapps: [tired of apps filled with ads, tracking, subscriptions and AI stuffed into everything](https://www.reddit.com/r/androidapps/comments/1ux4zl5/); [texting apps that don't have AI?](https://www.reddit.com/r/androidapps/comments/1uctku5/); [wallpaper app that doesn't allow AI?](https://www.reddit.com/r/androidapps/comments/1qq0mup/); [What app has no business being a subscription?](https://www.reddit.com/r/androidapps/comments/1wj4ri4/) (70 / 64).
- r/productivity: ["AI features" are making productivity apps worse](https://www.reddit.com/r/productivity/comments/1sbe3ey/); ["Removing AI from your app is an upgrade"?](https://www.reddit.com/r/productivity/comments/1pzevm2/).
- Ads creeping into assistants: [Is Siri showing ads now?](https://www.reddit.com/r/iphone/comments/1r7x4t6/) (239); [Gemini's chat may not stay ad-free](https://www.reddit.com/r/Android/comments/1t0o2ye/) (280).
- [95% of canceled annual app subscribers never come back](https://www.reddit.com/r/apple/comments/1tpm6l9/) (3,888 / 473).

### C3. Institutional "AI slop" and AI cheating — **Strong** in student and professional subs

[Tired of authors using ChatGPT in their books](https://www.reddit.com/r/ChatGPT/comments/1s2jnpg/) (6,963) · [Is my boss using Gemini to email me?](https://www.reddit.com/r/GeminiAI/comments/1sufzsi/) (2,995) · [UMD Career Center sending us AI slop](https://www.reddit.com/r/UMD/comments/1shisp2/) (181) · [Teammate used Claude to fake our capstone tests](https://www.reddit.com/r/csMajors/comments/1vzs7xh/) (900 / 173) · [I wanna sue Turnitin AI detector](https://www.reddit.com/r/GradSchool/comments/1oe93es/) (812, Oct 2025) · [ChatGPT is making my students stupider](https://www.reddit.com/r/GradSchool/comments/1ojr04m/) (932, Oct 2025) · [Failing grades soar at UC Berkeley CS as AI use rises](https://www.reddit.com/r/csMajors/comments/1tw5kkx/) (695) · [Stop using Cluely](https://www.reddit.com/r/csMajors/comments/1qaxuxf/) (608).

### C4. Dark-pattern AI subscription apps and astroturfing — **Medium**

[Fake "ADHD" creators on TikTok covertly promoting the Mindflow app](https://www.reddit.com/r/ADHD/comments/1rucyq6/) (368): *"a useless AI app… tricking ADHDers into… monthly/yearly subscription since we're more vulnerable into forgetting."*

### C5. AI companions / girlfriends — **Medium** (mocked, not demanded)

[Craig Federighi: Siri won't be your AI girlfriend](https://www.reddit.com/r/apple/comments/1u3dsjf/) (1,210); [Siri AI may remind you it's not a real person](https://www.reddit.com/r/apple/comments/1u7ebmi/) (995); [UMD asking new students whether they use AI for companionship/dating](https://www.reddit.com/r/UMD/comments/1v6od32/) (60); r/ChatGPT's ["Ai girlfriend"](https://www.reddit.com/r/ChatGPT/comments/1woe567/) (4,858) is a meme. The r/AppIdeas companion threads are NSFW-adjacent.

### C6. Record-everything note-takers and lifelogging — **Medium-Weak** on Reddit

The r/productivity "recorded every class for 6 years" thread (above) had replies like *"it's time for therapy"* (262) and *"please don't recommend AI as a mental health resource"*. Web context: Friend's pendant was mocked (*"why is this not just a phone app"*), Limitless went to Meta (Dec 2025), and Bee to Amazon ([RTÉ](https://www.rte.ie/news/business/2026/0112/1552620-ai-pendants-back-in-vogue-at-ces-after-early-setback/)). Meeting note-takers are a mature desktop category.

### C7. Agent hype versus users — **Medium-Strong** within r/AI_Agents

[Stop building AI agents](https://www.reddit.com/r/AI_Agents/comments/1taei9m/) (794) · [A client paid me to rip the AI out of the tool I built them](https://www.reddit.com/r/AI_Agents/comments/1u067cf/) (478) · [People building the tools are more excited than the people using them](https://www.reddit.com/r/AI_Agents/comments/1v81142/) (330) · [90% of agent projects don't need agents](https://www.reddit.com/r/AI_Agents/comments/1s4u5v4/) (235) · [99% of this sub is agents replying to agents](https://www.reddit.com/r/AI_Agents/comments/1w415b3/).

### C8. Mainstream anti-AI sentiment — **Strong**, and it matters for consumer framing

[I fired my therapist because she told me to use AI](https://www.reddit.com/r/GirlDinnerDiaries/comments/1wfuerk/) (24,472) · [The anti-AI movement has reached Hollywood](https://www.reddit.com/r/BeAmazed/comments/1ulcf8i/) (19,345) · [r/antiai: "Sora is dead. We're going to win"](https://www.reddit.com/r/antiai/comments/1s2p3sx/) (12,490) · [I hate AI and it's taking over everything](https://www.reddit.com/r/GirlDinnerDiaries/comments/1u1u69s/) (9,588 / 860) · [70% of Americans don't want AI data centers nearby](https://www.reddit.com/r/artificial/comments/1tdw8if/) (467). Secondary survey context: consumer "excitement about AI" fell to about 19% in 2026 ([Storyboard18](https://www.storyboard18.com/digital/ai-fatigue-rises-in-2026-as-consumer-excitement-drops-to-19-report-95162.htm); Weak).

*What this means for our pick (C2–C8):* name and market the product by the job it does, not "AI". Offer a free core with no bait subscription, never send unlabelled AI-authored text to other humans, avoid companionship features, and show restraint (do less, reliably).

---

## Part D — Student-life pain points (ranked by signal)

**D1. Logistics and LMS chaos — Medium-Strong.** Examples: the wrong class section all semester (2,616); the Canvas outage during finals (2,088; students couldn't reach rubrics); Canvas notification floods (54); *"Tips for Syllabus week"* ([100](https://www.reddit.com/r/college/comments/1vrur6d/)); *"Class with zero due dates and almost no content on canvas?"*; *"lab professor is ignoring the syllabus"*. The r/UMD dump is full of "is this schedule OK?" and "No canvas yet" posts.

**D2. Reading and note load — Medium (many low-score posts plus a few mid-score ones).** Examples: r/GradSchool [How in the world do you read?](https://www.reddit.com/r/GradSchool/comments/1wdx1v8/) (151 / 80); [lit-review screen fatigue](https://www.reddit.com/r/GradSchool/comments/1vzuv4u/) (78); [reading/notes/paper-organizing workflow](https://www.reddit.com/r/GradSchool/comments/1wmmhmv/) (60); [readings with eye problems/migraines](https://www.reddit.com/r/GradSchool/comments/1wl1o8s/); r/college [Does anyone actually read the textbooks AND take notes?](https://www.reddit.com/r/college/comments/1qbevp8/) (116 / 57); [read what's on screen, write it down and listen at once](https://www.reddit.com/r/college/comments/1rjtxak/); [SOS I lost my ability to think](https://www.reddit.com/r/GradSchool/comments/1wbitqq/) (169). The loved counterexample is the [handwriting notebook where Claude writes back](https://www.reddit.com/r/ClaudeAI/comments/1vxqbzs/) (3,881): *"the applications for studying are endless."*

**D3. Loneliness and belonging — Medium.** Examples: [Third Space pixel-art social app at UMD](https://www.reddit.com/r/UMD/comments/1s1s6a3/) (136); [Does anybody wanna hang out with me today](https://www.reddit.com/r/UMD/comments/1wjvwtu/) (76 / 52); *"Where to cry in college"* (139); *"Please tell me it gets better"* (124 / 91); *"just graduated, all my college friends left the city"* (285).

**D4. Job-market anxiety and the need to stand out — Strong in r/csMajors.** Examples: [4k apps, 700+ LeetCode, no offers](https://www.reddit.com/r/csMajors/comments/1t3gbbu/) (1,938 / 332); [Being "cracked" isn't going to get you a job](https://www.reddit.com/r/csMajors/comments/1ssm4am/) (1,764); [I wish ai never existed](https://www.reddit.com/r/csMajors/comments/1tl2qzi/) (786: *"it makes it so hard for entry level people to stand out"*); [my project got me a job with no prev experience](https://www.reddit.com/r/csMajors/comments/1scbizb/) (491); [accidentally made a successful website I can't put on my resume](https://www.reddit.com/r/csMajors/comments/1uhmxkv/) (902). Job-search tools that won big: [Indeed laid off my pregnant wife, so I built a competitor — 7,500 users](https://www.reddit.com/r/SideProject/comments/1w5efwo/) (689) and the open-sourced [AI job-search system](https://www.reddit.com/r/ClaudeAI/comments/1sd2f37/) (2,245).

**D5. AI-in-academia tension — Strong (see C3).** Any student-facing AI must be *pro-learning*: it explains, quizzes and organizes, and never writes graded work. [Students ask for exactly that](https://www.reddit.com/r/college/comments/1vp3u2h/) (*"What AI prompts actually help with studying (without writing your essays for you)?"*).

**D6. Money (tuition, textbooks, aid) — Strong but mostly not AI-solvable.** Examples: [Professor requiring us to buy their own book](https://www.reddit.com/r/college/comments/1vrg7ly/) (212 / 104); [Check your library for textbooks. I beg you.](https://www.reddit.com/r/GradSchool/comments/1vz9p5h/) (170).

*What this means for our pick:* a campus wedge works if it attacks D1 and D2 with verifiable, pro-learning outputs. Examples: syllabus, Canvas and email feed into one trustworthy "what's due and what to do tonight"; a camera or reader companion that explains and quizzes. The developer's Canvas-MCP work is a head start. Stay away from grading/detection, auto-writing, and scheduling/degree-audit clones (Orbit and Jupiterp exist at UMD).

---

## Synthesis for picking the project (inference)

**Filters distilled from Reddit:**
1. **The 10-second "wow" is perceptual and real-world:** camera or mic in, structured overlay or voice out, on a phone.
2. **It must solve a recurring pain someone already complains about.** The strongest are remembering and follow-through, life-admin documents, reliable actions, and study load.
3. **Reliability and trust are the product.** Measure success rate and latency. Keep data local-first, keep memory inspectable, confirm only risky actions, make actions idempotent, harden against injection, and open-source the client if it touches deep device data.
4. **Anti-slop presentation.** Frame by outcome, not "AI"; no bait subscription; publish evals, a threat model and an incident log. The r/AI_Agents thread on [what portfolio shows "this person knows production"](https://www.reddit.com/r/AI_Agents/comments/1wo286p/) (Sep 23) says: *"Everyone… has a portfolio full of 'Chat with your PDF'… that stuff isn't getting anyone hired"*; *"I'm looking for evidence the thing was live for a while: an incidents file, a retry that exists because of one specific outage, a metric that got added after something went wrong"*; *"Idempotency keys on tool calls…"*; *"Build a quality MCP server with an observability stack… red team it… security testing suite… in the CI"* (23).
5. **Don't compete head-on with the platforms' new strengths.** Siri AI now handles personal context over Apple Mail, Photos and Notes and camera→Health. Gemini has Personal Intelligence and "Call for Me". Differentiate where they're weak: Android plus web, non-Apple services (Gmail, Canvas), shared or household contexts, a specialized domain, open and local operation, and measurable reliability.

**Directions the evidence supports (for the lead to weigh; not a decision):**

| Direction | Evidence fit | Wow on phone | Eng. depth | Main risks |
|---|---|---|---|---|
| **Point-and-act life-admin copilot** (camera, screenshot, share-sheet, or email → facts + deadlines + next action → calendar/reminders, with source-linked verification; local OCR/VLM) | A2, B2, B3, B5, D1 (Strong/Medium) | Point at a syllabus, bill or flyer → structured plan in seconds | Extraction evals, provenance, local+cloud split, reminder engine, idempotent actions | Partial sherlock by Siri AI / Gemini; must be clearly better on reliability and non-Apple sources |
| **Real-time camera coach with voice cues** (form, reps, technique) | A1 (Strong), r/AppIdeas ask | Live overlay + earbud cues | On-device pose, rep segmentation, labelled video eval set, latency budget | Crowded fitness niche; "arbitrary angle ranges" critique unless validated |
| **Reliability-first bounded assistant** (deterministic fast path + tiny on-device tool-caller + LLM fallback, with published success/latency evals) | B1 (Strong), A5 | Side-by-side vs Siri/Gemini on the same commands | Router, evals, latency, on-device models | Platform access (Android Accessibility policy; iOS closed); trust bar requires open source |
| **Remember-and-nudge external memory** for ADHD / overwhelmed users (capture anything → inspectable local memory → resurfacing by time/place/context → escalation to a call) | B2, B6 (Strong need) | Nudge that finds you at the right moment | Recall policy + evals, memory store, notification strategy | Saturated planner market; r/ADHD hostile to app promotion; must avoid the "graveyard" pattern |

---

## Saturated — avoid (with evidence)

| Category | Why avoid (evidence) |
|---|---|
| ChatGPT wrappers / "chat with X" / generic AI chat UIs | The r/SideProject petition and rants (C1); r/AI_Agents: "Chat with your PDF… isn't getting anyone hired" |
| AI SaaS boilerplates and "AI agent builder" platforms | [OpenAI "killed half the agent-builder startups"](https://www.reddit.com/r/productivity/comments/1o2h2vk/) (594, Oct 2025); C7 |
| Multi-agent "virtual office" and agent-swarm demos | Novelty only ([726](https://www.reddit.com/r/SideProject/comments/1r3h4zj/)); C7 skepticism; production horror stories |
| AI note-takers, meeting recorders, lifelogging pendants | C6; consolidation (Limitless→Meta, Bee→Amazon); "record everything" backfires |
| AI companions / girlfriends / "AI therapist" | C5; mainstream backlash (24k-pt therapist thread) |
| Generic AI to-do / planner / ADHD app with a subscription | *"graveyard of productivity apps"*; Mindflow astroturfing backlash; [*"I deleted my to-do list apps. I'm 10x more productive"*](https://www.reddit.com/r/productivity/comments/1qvihmj/) |
| AI photo "enhance" / image generators / AI wallpapers / food-photo glamour | [20k-pt "can't turn off AI enhance"](https://www.reddit.com/r/mildlyinfuriating/comments/1orsc2m/); "food catfishing"; r/androidapps asks for *no-AI* apps |
| Calorie/nutrition photo loggers | Sherlock risk from Siri Visual Intelligence (Weak); crowded (inference) |
| AI news/article summarizers | Giveaway-spam tier on r/androidapps; platforms do summaries (and Apple now *refuses* URL summaries: [1,474](https://www.reddit.com/r/apple/comments/1uerozz/)) |
| Auto-apply job bots / interview-cheating tools | Cluely backlash; "cheated on interviews" discourse (C3) |
| AI that writes messages to other humans on your behalf | [Is my boss using Gemini to email me?](https://www.reddit.com/r/GeminiAI/comments/1sufzsi/) (2,995); condolence-email wake-up (665) |
| Vibe-coded self-hosted dashboards/tools | r/selfhosted "Vibe Code Friday", the Huntarr/BookLore fallout |
| A general "better Siri/Gemini" OS assistant | Platform lock-in plus Apple/Google shipping fast (Sep 2026); build a bounded domain instead |
| Scheduling / degree-audit tools at UMD | Orbit and Jupiterp already exist |

---

## Appendix A — Coverage

- **Top-of-year listings (100 posts each):** SideProject, LocalLLaMA, ChatGPT, ClaudeAI, OpenAI, singularity, artificial, AI_Agents, androidapps, iphone, apple, Android, productivity, ADHD, selfhosted, indiehackers, college, csMajors, GradSchool, GeminiAI, Siri, GooglePixel, AppIdeas, UMD, vibecoding.
- **Top-of-month listings (Aug 29–Sep 28, 2026):** SideProject, LocalLLaMA, ChatGPT, ClaudeAI, OpenAI, singularity, artificial, AI_Agents, androidapps, iphone, apple, Android, productivity, ADHD, selfhosted, indiehackers, college, csMajors, GradSchool.
- **Subreddit searches (top of year):** ADHD "app"/"AI"/"ChatGPT"; productivity "AI"; iphone "Siri"/"app AI"; apple "Siri"; Android "Gemini"; GooglePixel "Gemini"; ChatGPT "memory"/"slop"/"Siri"; LocalLLaMA "phone"; SideProject "AI"/"wrapper"/"vibe coded"; indiehackers "wrapper"; college "AI"/"ChatGPT"/"app"; csMajors "project"; GradSchool "AI"; androidapps "AI"; selfhosted "AI"; AI_Agents "phone"; ClaudeAI "iPhone"; UMD "AI"; singularity "phone". Plus Reddit-wide searches for "is there an app", "AI wrapper", "AI note taker", "AI companion app", "I wish Siri" and "is there an AI" (these were noisy; see caveats).
- **Full dumps (Arctic Shift):** r/college 2026-01-01→04-08 (9,447 posts) and 08-13→09-28 (2,982); r/UMD 08-13→09-28 (1,102); r/GradSchool 08-13→09-28 (1,462).

## Appendix B — Threads read in depth (post + top comments)

- **Siri / Gemini:** 1wlo17s, 1wqmkb1, 1wo7059, 1wmxz7m, 1vx9qyu, 1tvpdpe, 1u6od30, 1ti82w9, 1vqu4a5, 1wk0ezv, 1wp1zpx.
- **Needs:** 1o01xfa (via RSS), 1vblphw, 1q8co2q, 1upheer, 1ttupa5, 1w0o7xq, 1wm31ed, 1wk3nx2, 1qmir5d, 1sdv3lo, 1ve7jch, 1r1b3gl, 1wjq4vh.
- **Traction:** 1u9esua, 1wqsd4f, 1vi5guo, 1vxqbzs, 1tp3en9, 1uqt53j, 1wrckhp, 1wpaalh, 1w74cif, 1wbu40o, 1w4867a, 1wmxjs0, 1rngalv.
- **Fatigue:** 1rmiwgb, 1pgbvrl, 1wgxzx9, 1rckopd, 1w2rwg0, 1rucyq6.
- **Students / UMD:** 1qnfytt, 1t6orzl, 1tl2qzi, 1rdhorc, 1s1s6a3, 1u7glxy, 1w32ur1, 1wjvwtu.
- **Hiring signal:** 1wo286p, 1w4iw3m.
- **r/AppIdeas meta:** 1r73tui, 1rebahq, 1t100ns.

(Thread URL pattern: `https://www.reddit.com/comments/<id>/`)
