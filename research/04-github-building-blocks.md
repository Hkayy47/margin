# 04 — Open-source building blocks (GitHub) for a phone-first AI product

**Snapshot date: 2026-09-28.** I pulled stars, last push and license live from the GitHub API (`gh api repos/<owner>/<repo>`) on this date. Package versions come from the npm registry. Capability claims come from each repo's README or docs, and numbers the vendors report themselves are marked **(vendor)**. Most model weights live on Hugging Face rather than GitHub, so they get their own table (§3.2).

**How to read the tables**
- **Phone demo:** **High** means it runs on the phone or is directly visible in a phone demo. **Med** means it runs on a laptop or server but powers the phone experience. **Low** means it is a dev-time or infra piece that nobody sees in a demo.
- **Status:** unlabeled means pushed within roughly the last 6 months. **SLOWING** means the last push was 6–12 months ago. **STALE** means more than 12 months or archived. "(renamed)" means the old URL now redirects.
- Star counts are rounded (for example, 129.8k).

---

## 0. TL;DR

- **The biggest constraint is the platform, not the model.** From a Windows laptop with no Mac, **Android is first-class**: local builds, ADB, phone-use agents and native modules all work. **An iPhone needs either EAS cloud builds plus a paid $99/yr Apple Developer account, or a WebGPU PWA**, which works because iOS 26+ Safari ships WebGPU. Pick the stack once the phone type is known, and keep the core demo portable (Expo + TypeScript + cloud fallback).
- **What changed in 2026:** on-device multimodal is now real and permissively licensed.
  - **Gemma 4 E2B/E4B** (Apache-2.0, image + audio input, Apr 2026) runs at about 50 tok/s decode on flagship phone GPUs using about 0.6–1.7 GB peak memory **(vendor)**.
  - **Qwen3.5 0.8B–9B** (Apache-2.0, natively multimodal, Mar 2026) and **LFM2.5** (Jan 2026) fill the other small-model slots.
  - Apple's **iOS 27 Foundation Models** adds vision input, a free Private Cloud Compute tier, and a `LanguageModel` protocol with Claude and Gemini providers.
- **The RN/Expo tooling is ready.** llama.rn 0.13, React Native ExecuTorch 0.10, VisionCamera v5, LiveKit RN 3.0 and sherpa-onnx are all actively maintained, and Expo SDK 57 is stable with 58 in beta.
- **The hottest 2026 signal is agents that do things.** OpenClaw has 390k★, Hermes Agent 250k★, and phone-use agents (Mobilerun, mobile-use, Open-AutoGLM, phone-harness) plus MCP Apps are trending. Phone-use is **Android-only from Windows**.
- **Licenses need care.** Avoid these in the core:
  - AGPL code: Ultralytics YOLO, YOLOE, ChatterUI.
  - Non-commercial weights: Depth Anything L/G, fish-speech, F5-TTS.
  - Revenue-capped "source-available" SDKs: Cactus (<$2M), RunAnywhere (<$1M). These are fine for a student portfolio but a trap later.
- **Top 12 shortlist:** see §5.

---

## 1. What is new since 2025 (don't rely on older memory)

| Area | 2026 change | Why it matters |
|---|---|---|
| Small models | **Gemma 4** (Apr 2 2026): E2B/E4B edge models with image + **audio** input, plus 26B-A4B MoE and 31B, **Apache-2.0** (earlier Gemma used custom terms). **Qwen3.5 small** (Mar 2 2026): 0.8B/2B/4B/9B, Apache-2.0, natively multimodal, 262K context, tool calling. **LFM2.5** (Jan 2026): 1.2B Instruct/Thinking, VL-1.6B, Audio-1.5B, then 2.6B agentic (Aug 2026). | A single ~2–4 GB model can see, hear and call tools on-device. |
| Google runtime | **LiteRT-LM** is Google's LLM runtime: Kotlin stable, **Swift + JS/WebGPU APIs** in preview since May 2026, NPU on Android, MTP drafters up to 2.2–3x faster decode. The Gallery app ships on Android and iOS. | A native path for Gemma 4 on both OSes. |
| Apple | **WWDC26 / iOS 27 Foundation Models**: rebuilt on-device model (8K context) with **vision input**; **Private Cloud Compute** access (32K context, reasoning) **free for devs with <2M first-time downloads**; `LanguageModel` protocol with **Anthropic and Google Swift packages** ([anthropics/ClaudeForFoundationModels](https://github.com/anthropics/ClaudeForFoundationModels)); Dynamic Profiles; system tools (OCR, barcode, Spotlight RAG); an evals framework; a Python SDK and `fm` CLI on macOS 27; the framework is being open-sourced. There is also a new **Core AI** framework (`.aimodel`, [apple/coreai-models](https://github.com/apple/coreai-models)). | Free, private on-device + cloud LLM on iPhone 15 Pro and later. Swift-only, so from Windows you need an RN/Expo wrapper. |
| Web | **WebGPU in Safari 26 (iOS 26)**; Chrome Android since 121 on Android 12+ Qualcomm/ARM GPUs. **transformers.js v4** has a new C++ WebGPU runtime, and 4.3 (Sep 2026) enabled Safari 26 WebGPU. | A PWA can now do real on-device inference on iPhone. |
| Voice | New or updated models: **Kyutai Pocket TTS** (100M, CPU), **Qwen3-TTS** (97 ms streaming), **Qwen3-ASR**, **OmniVoice** (600+ languages), **MOSS-TTS-Nano**, **Chatterbox Turbo/Nano/Multilingual V3**, **VibeVoice Realtime-0.5B + ASR**, **NVIDIA Parakeet-unified / Nemotron streaming ASR**, **Moonshine** streaming (MIT, all platforms), **smart-turn v3.2**, **LiveKit audio turn detector**. | Sub-second local voice loops. Parlor shows about 0.7 s from end of speech to first audio **(vendor)**. |
| Vision | **SAM 3** (Nov 2025) → **SAM 3.1** (Mar 2026, faster multi-object tracking), SAM 3D; **Depth Anything 3**; **YOLO26** (Jan 2026, NMS-free) and YOLO27 (both AGPL); **RF-DETR** detection + segmentation (Apache); OCR VLMs (DeepSeek-OCR 2, GLM-OCR, PaddleOCR-VL, Baidu Unlimited-OCR). | "Segment anything by text" is a 10-second wow moment. |
| Agents | "Claw" personal agents dominate GitHub: [openclaw/openclaw](https://github.com/openclaw/openclaw) 390k★, [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) 250k★, [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) 239k★. Phone-use agents: Open-AutoGLM (Dec 2025), DroidRun → **Mobilerun**, mobile-use (claims 100% AndroidWorld), **phone-harness** (Aug 2026), Callstack **agent-device**, Software Mansion **argent**. | "It operates my phone" is the zeitgeist, and recruiters will recognize it. |
| Gen UI / MCP | **MCP Apps** is the official MCP extension (SEP-1865, stable 2026-01-26), hosted by Claude, ChatGPT, VS Code, Goose and others. **json-render** (Vercel Labs, 18k★) renders to **React Native**. **A2UI v0.9** (Google). **AI SDK v7**. | Generative UI can run natively on the phone and inside Claude/ChatGPT. |
| Mobile | **Expo SDK 57** (Jun 30 2026, RN 0.86) is stable and **SDK 58 beta** landed Sep 15 2026. RN 0.87 is out, and the RN repo moved to `react/react-native`. VisionCamera **v5**. | Everything assumes the New Architecture. |
| Renames/moves | `argmaxinc/WhisperKit` → [argmax-oss-swift](https://github.com/argmaxinc/argmax-oss-swift); `NVIDIA/NeMo` → [NVIDIA-NeMo/Speech](https://github.com/NVIDIA-NeMo/Speech); `vikhyat/moondream` → [m87-labs/moondream](https://github.com/m87-labs/moondream); Apple ML repos → `apple-aiml-research/*`; `droidrun/droidrun` → [droidrun/mobilerun](https://github.com/droidrun/mobilerun); `NexaAI/nexa-sdk` now resolves to [qualcomm/GenieX](https://github.com/qualcomm/GenieX); `google-ai-edge/ai-edge-torch` → [litert-torch](https://github.com/google-ai-edge/litert-torch); `rhasspy/piper` archived → [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl) (GPL); PartyKit → [cloudflare/partykit](https://github.com/cloudflare/partykit). | Use the new URLs. |

---

## 2. Platform reality check (Windows 11 laptop, no Mac, phone type unknown)

| Capability | Android phone | iPhone |
|---|---|---|
| Native build and install | Local `npx expo run:android` / Android Studio + USB; APK sideload in seconds | **EAS Build (cloud)** only. *"All builds that run on an iPhone device require a paid Apple Developer account"* (Expo docs); ad hoc/TestFlight distribution |
| Expo Go (no native modules) | Works | Works, but **no custom native code**: no llama.rn, ExecuTorch or VisionCamera frame processors |
| Swift-only libs (Apple FM iOS 27 APIs, MLX Swift, WhisperKit, Core AI, FastVLM app) | n/a | Only through an Expo native module compiled blind on EAS. High friction without Xcode |
| On-device LLM/VLM | llama.rn (OpenCL on Adreno, experimental Hexagon NPU), ExecuTorch (Vulkan), LiteRT-LM (GPU/NPU) | llama.rn (Metal), ExecuTorch (Core ML/MLX), LiteRT-LM Swift preview, Apple FM |
| System LLM | Gemini Nano via **ML Kit GenAI Prompt API** (beta, device allowlist; text + image) | **Apple Foundation Models** (Apple Intelligence devices: iPhone 15 Pro and later), PCC free tier |
| In-browser (PWA) | Chrome WebGPU (Android 12+, Qualcomm/ARM GPUs) | Safari 26+ WebGPU (all iOS browsers use WebKit) |
| Phone-use agents (AI operating other apps) | **Yes**, via ADB/accessibility from the laptop or a Portal app | **No from Windows.** Needs macOS (XCUITest/WebDriverAgent, or iPhone Mirroring for phone-harness). The iOS sandbox blocks app-to-app control |
| Background mic/camera | Foreground service with a notification | Tightly restricted; PWAs get no background execution |

---

## 3. Categorized building blocks

### 3.1 On-device and in-browser inference runtimes

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 129.8k | 2026-09-28 | MIT | C/C++ LLM/VLM engine (GGUF); Metal, Vulkan, OpenCL, CUDA; the base for llama.rn, wllama and many apps. Also serves models on the RTX 5070 laptop | High (via bindings) |
| [mybigday/llama.rn](https://github.com/mybigday/llama.rn) | 1.0k | 2026-09-28 (v0.13.0-rc.6) | MIT | RN binding: chat, **vision/audio via mtmd projectors**, tool calling (Jinja), GBNF/JSON-schema output, embeddings/rerank, MTP speculative decoding, **experimental TTS** (OuteTTS, Qwen3-TTS, Chatterbox, NeuTTS…), Metal / OpenCL (Adreno) / Hexagon NPU (SM8450+, experimental). **Expo config plugin**; New Architecture required | High |
| [software-mansion/react-native-executorch](https://github.com/software-mansion/react-native-executorch) | 1.75k | 2026-09-28 (v0.10.4) | MIT | Hooks + **pre-exported model catalog**: LLM/VLM (e.g. `LFM2_5_1_2B`, Llama, Phi, Gemma 4), **Whisper STT, Kokoro TTS**, OCR, detection (YOLO, RF-DETR), segmentation, classification, text/image embeddings. XNNPACK, Core ML, MLX, Vulkan. **Expo SDK 55+ dev build**, iOS 17+, Android 13+, RN 0.83+ | High |
| [pytorch/executorch](https://github.com/pytorch/executorch) | 5.1k | 2026-09-28 | BSD-3 | Meta's on-device PyTorch runtime and export (Core ML, MPS, XNNPACK, Vulkan, QNN backends) | Med (use through RN ExecuTorch) |
| [google-ai-edge/LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM) | 6.5k | 2026-09-28 (v0.17.1) | Apache-2.0 | Google's on-device LLM runtime: Gemma 4 E2B/E4B, Gemma 3n, Qwen, Phi-4, Llama; **vision + audio input**; function calling; CPU/GPU/NPU. APIs: Kotlin (stable), C++, Python, **Swift and JS/WebGPU (preview)**, Flutter (community) | High (native) |
| [google-ai-edge/LiteRT](https://github.com/google-ai-edge/LiteRT) | 3.5k | 2026-09-28 | Apache-2.0 | TFLite successor for general on-device ML | Med |
| [google-ai-edge/litert-torch](https://github.com/google-ai-edge/litert-torch) (renamed) | 1.1k | 2026-09-28 | Apache-2.0 | PyTorch → LiteRT conversion | Low |
| [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | 37.1k | 2026-09-28 | Apache-2.0 | Vision tasks (hand, pose, face landmarks, gestures, segmentation, interactive segmentation, detection), audio/text tasks; Android, iOS, Web, Python. RN wrappers are community-only (e.g. [cdiddy77/react-native-mediapipe](https://github.com/cdiddy77/react-native-mediapipe), 80★) | High (web or native) |
| [mlc-ai/web-llm](https://github.com/mlc-ai/web-llm) | 19.2k | 2026-09-15 (v0.2.85) | Apache-2.0 | WebGPU LLM engine in the browser with an OpenAI-style API | High (PWA) |
| [huggingface/transformers.js](https://github.com/huggingface/transformers.js) | 16.3k | 2026-09-28 (v4.3.0) | Apache-2.0 | v4 C++ WebGPU runtime. Model families include **Gemma 4, Gemma 3n, Qwen3.5, LFM2/LFM2-VL, SmolVLM, Florence-2, SAM/SAM 2/SAM 3, RF-DETR, D-FINE, Depth Anything, DINOv3, Whisper, Moonshine, Parakeet, Voxtral Realtime, Chatterbox**; structured output; Safari 26 WebGPU enabled | High (PWA) |
| [mlc-ai/mlc-llm](https://github.com/mlc-ai/mlc-llm) | 23.2k | 2026-08-17 | Apache-2.0 | TVM-compiled LLMs for iOS, Android and web. The compile toolchain is heavy (and painful on Windows) | Med |
| [ngxson/wllama](https://github.com/ngxson/wllama) | 1.3k | 2026-09-27 | MIT | llama.cpp → WebAssembly (CPU) in the browser | Med |
| [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) | 21.9k | 2026-09-28 (v1.30) | MIT | ORT Web (WebGPU/WASM), mobile, `onnxruntime-react-native`. **The RN package lags at 1.24.3** | Med |
| [microsoft/onnxruntime-genai](https://github.com/microsoft/onnxruntime-genai) | 1.1k | 2026-09-28 | MIT | `generate()` loop for ONNX LLMs | Med |
| [callstackincubator/ai](https://github.com/callstackincubator/ai) | 1.4k | 2026-07-07 | MIT | **Vercel AI SDK providers for RN**: `@react-native-ai/apple` (Apple FM text, embeddings, STT, TTS), `/llama` (llama.rn), `/mlc`. npm was last published 2026-02 (v0.12), so **iOS 27 FM features (vision, PCC) are likely not wrapped yet** | High |
| [alibaba/MNN](https://github.com/alibaba/MNN) | 16.2k | 2026-09-23 | Apache-2.0 | Alibaba's engine; MNN Chat Android app; strong Qwen support | Med |
| [qualcomm/GenieX](https://github.com/qualcomm/GenieX) (ex nexa-sdk) | 8.4k | 2026-09-28 | BSD-3 | LLM/VLM on Qualcomm NPU/GPU/CPU | Med (Snapdragon only) |
| [qualcomm/ai-hub-apps](https://github.com/qualcomm/ai-hub-apps) | 461 | 2026-09-28 | BSD-3 | Snapdragon-optimized sample apps | Low |
| [cactus-compute/cactus](https://github.com/cactus-compute/cactus) | 6.1k | 2026-09-26 | **Source-available**: free for individuals, students, and orgs with <$2M funding and <$2M revenue | Hybrid edge/cloud engine. RN, Flutter, Swift, Kotlin, Python, Rust SDKs; **confidence-based cloud handoff**; iPhone 17 Pro ~37 tok/s decode, ~640 MB RAM **(vendor)** | High (license cap) |
| [cactus-compute/needle](https://github.com/cactus-compute/needle) | 12.8k | 2026-09-28 | Apache-2.0 | 26M-param on-device **tool-calling / extraction** model (2-bit, 8–29 MB) | High (niche) |
| [RunanywhereAI/runanywhere-sdks](https://github.com/RunanywhereAI/runanywhere-sdks) | 10.3k | 2026-09-24 | **Source-available** (RunAnywhere License; free under $1M funding/revenue) | One C++ core, 8 SDKs (RN, Flutter, Swift, Kotlin, Web…): LLM/VLM, STT, TTS, VAD, **voice-agent pipeline**, RAG; engines llama.cpp / MLX / sherpa-ONNX / Hexagon | High (license cap) |
| [UbiquitousLearning/mllm](https://github.com/UbiquitousLearning/mllm) | 1.6k | 2026-09-08 | MIT | Research engine for mobile multimodal LLMs (NPU) | Low |
| [Tencent/ncnn](https://github.com/Tencent/ncnn) | 23.9k | 2026-09-24 | BSD-3 | Mobile NN inference (Vulkan); common for YOLO ports | Med |
| [margelo/react-native-fast-tflite](https://github.com/margelo/react-native-fast-tflite) | 1.2k | 2026-09-11 | MIT | TFLite/LiteRT models in RN with GPU delegates; plugs into VisionCamera frame processors | High |
| [wcandillon/react-native-webgpu](https://github.com/wcandillon/react-native-webgpu) | 1.2k | 2026-09-22 | MIT | WebGPU (Dawn) inside RN for GPU compute and shaders | Med |
| [anthropics/ClaudeForFoundationModels](https://github.com/anthropics/ClaudeForFoundationModels) | 309 | 2026-09-28 | Apache-2.0 | Claude as a provider inside Apple's FM framework (iOS 27 `LanguageModel` protocol) | Med (Swift) |
| [apple/python-apple-fm-sdk](https://github.com/apple/python-apple-fm-sdk) | 1.3k | 2026-09-25 | Apache-2.0 | Python access to Apple's on-device model (macOS 27) | Low (Mac-only) |
| [apple/coreai-models](https://github.com/apple/coreai-models) | 2.2k | 2026-09-28 | BSD-3 | Core AI export recipes + Swift runtime utilities (iOS/macOS 27, Xcode 27) | Low (Mac-only) |
| [ml-explore/mlx-swift](https://github.com/ml-explore/mlx-swift) | 2.0k | 2026-09-28 | MIT | MLX on iOS/macOS (Apple GPU) | Low (Mac-only) |
| [huggingface/transformers.js-examples](https://github.com/huggingface/transformers.js-examples) | 2.1k | 2026-02-17 **SLOWING** | Apache-2.0 | Demo apps for transformers.js | Med |

### 3.2 Small models to run on phones (weights are mostly on Hugging Face)

| Model | Released | License | Notes for phones |
|---|---|---|---|
| **Gemma 4 E2B / E4B** | 2026-04-02 | **Apache-2.0** | Text + image + **audio** input. `.litertlm` files are 2.58 GB (E2B) and 3.65 GB (E4B). LiteRT-LM benchmarks **(vendor)**: E2B decode 52 tok/s GPU on Galaxy S26 Ultra (676 MB peak) and 56 tok/s GPU on iPhone 17 Pro (1.45 GB peak; CPU 25 tok/s at 607 MB). E4B decode 22–25 tok/s GPU. Supported in llama.cpp, transformers.js, LiteRT-LM and RN ExecuTorch |
| Gemma 4 26B-A4B / 31B | 2026-04 | Apache-2.0 | Laptop/server class. On 8 GB VRAM the MoE needs expert offload to the 32 GB system RAM (slower) |
| **Qwen3.5 0.8B / 2B / 4B / 9B** | 2026-03-02 | Apache-2.0 | Natively multimodal (text, image, video), 262K context, tool calling, thinking mode off by default (2B is "prone to thinking loops" when on). 4B is about a 3.4 GB download |
| **LFM2.5** 1.2B (Instruct/Thinking/JP), VL-1.6B, Audio-1.5B; LFM2.5-2.6B agentic | 2026-01-05 → 2026-08 | **LFM Open License v1.0** (custom, with a commercial revenue threshold; check terms) | GGUF, MLX and ONNX day one. It is the default LLM in RN ExecuTorch's quick-start |
| SmolLM3-3B / SmolVLM2 ([huggingface/smollm](https://github.com/huggingface/smollm), 3.9k★, active) | 2025 | Apache-2.0 | Fully open training recipe |
| Phi-4-mini 3.8B | 2025 | MIT | A third-party guide reports ~13–18 tok/s at Q4 on iPhone 17 Pro |
| FunctionGemma 270M | late 2025 | Gemma terms | On-device function calling; powers "Mobile Actions" in Google's Gallery |
| Moondream 2 (2B) / Moondream 3 (9B-A2B MoE) | 2025–26 | Apache-2.0 / **BSL-1.1** (no competing hosted API) | Pointing, detection and counting VLM ([m87-labs/moondream](https://github.com/m87-labs/moondream), 10.1k★) |
| Florence-2 (HF only) | 2024 | MIT | Old but still handy for captioning, OCR and grounding in transformers.js; superseded by the Qwen3.5 and Gemma 4 VLMs |
| Apple on-device model (iOS 27) | 2026-09 | Proprietary, free API | 8K context, vision input, tool calling. **PCC** gives 32K context with reasoning, free under 2M downloads |
| Gemini Nano (ML Kit GenAI Prompt API) | beta | Proprietary | Text + image; device allowlist only |

### 3.3 Voice — speech-to-text

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) | 54.0k | 2026-09-28 | MIT | Whisper in C/C++ on every platform | High |
| [mybigday/whisper.rn](https://github.com/mybigday/whisper.rn) | 804 | 2026-09-17 (v0.7.4) | MIT | RN binding for whisper.cpp (realtime transcription, VAD) | High |
| [moonshine-ai/moonshine](https://github.com/moonshine-ai/moonshine) | 11.2k | 2026-08-31 | **MIT** (code + models by default; legacy exceptions) | **Low-latency streaming STT** ("does work while the user is still talking"), tiny (1 MB) to Whisper-large-class models, plus **intent recognition + TTS**. SDKs for Python, JS/WASM, iOS, Android, Windows | High |
| [NVIDIA-NeMo/Speech](https://github.com/NVIDIA-NeMo/Speech) (renamed) | 18.5k | 2026-09-28 | Apache-2.0 | Parakeet-TDT-0.6B-v3 (25 EU languages), **Parakeet-unified-en-0.6b** (offline + streaming, ≥160 ms), **Nemotron-3.5-ASR-Streaming-0.6B** (40 languages, Jun 2026), Canary-Qwen-2.5B, MagpieTTS | Med (GPU server) |
| [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) | 15.0k | 2026-09-22 (v1.13.8) | Apache-2.0 | **Offline speech Swiss-army knife**: streaming Zipformer ASR, Whisper, Moonshine, Parakeet, SenseVoice; TTS (Kokoro, Kitten, Piper, Matcha, Pocket TTS); VAD; keyword spotting; diarization. Android, iOS, WASM, Flutter, RN; 12 language bindings. RN wrappers are community-made ([XDcobra/react-native-sherpa-onnx](https://github.com/XDcobra/react-native-sherpa-onnx), 40★) | High |
| [QwenLM/Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) | 3.6k | 2026-06-26 | Apache-2.0 | Multilingual ASR family | Med |
| [QwenAudio/SenseVoice](https://github.com/QwenAudio/SenseVoice) | 9.4k | 2026-09-22 | MIT | Fast ASR + emotion and audio-event tags (zh/en/ja/ko/yue) | Med |
| [handy-computer/transcribe.cpp](https://github.com/handy-computer/transcribe.cpp) | 2.0k | 2026-09-28 | MIT | ggml STT for 16+ families (Whisper, Parakeet, Moonshine, Canary, Voxtral, Qwen3-ASR…). Desktop only (Metal/Vulkan/CUDA) | Med (laptop) |
| [cjpais/Handy](https://github.com/cjpais/Handy) | 32.4k | 2026-09-28 | MIT | Offline desktop dictation app; a good UX reference | Low |
| [argmaxinc/argmax-oss-swift](https://github.com/argmaxinc/argmax-oss-swift) (ex WhisperKit) | 6.4k | 2026-09-24 | MIT | Apple-silicon speech (Swift) | Low (Mac needed) |
| [antirez/voxtral.c](https://github.com/antirez/voxtral.c) | 1.7k | 2026-02-15 **SLOWING** | MIT | Mistral Voxtral Realtime 4B in pure C | Med |
| [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 25.6k | 2025-11-19 **SLOWING** | MIT | CTranslate2 Whisper on the server | Med |
| [jamsch/expo-speech-recognition](https://github.com/jamsch/expo-speech-recognition) | 684 | 2026-09-16 | MIT | Native iOS/Android speech recognizers (including on-device) in Expo; zero model download | High |
| [microsoft/VibeVoice](https://github.com/microsoft/VibeVoice) (ASR) | 54.5k | 2026-09-03 | MIT | VibeVoice-ASR-7B (60-min single pass, 50+ languages), ASR-Streaming with speakers, **ASR-BitNet** (CPU, 1.58 GB) | Med |

### 3.4 Voice — text-to-speech

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [hexgrad/kokoro](https://github.com/hexgrad/kokoro) | 9.1k | 2025-08-06 **STALE (code)** | Apache-2.0 | Kokoro-82M, still the default small TTS. Use it through ports: [thewh1teagle/kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) (2.7k, MIT, active), sherpa-onnx, RN ExecuTorch. `kokoro-js` npm was last published 2025-05 | High (via ports) |
| [KittenML/KittenTTS](https://github.com/KittenML/KittenTTS) | 15.5k | 2026-08-19 | Apache-2.0 | 15M–80M params (25–80 MB), ONNX CPU, 8 voices, **English only**, mobile SDK on the roadmap | High |
| [kyutai-labs/pocket-tts](https://github.com/kyutai-labs/pocket-tts) | 9.7k | 2026-09-28 | MIT | 100M params; CPU ~6x realtime on M4; **~200 ms to first chunk**; voice cloning; 6 languages; streaming. Browser via community ports | Med–High |
| [resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox) | 26.6k | 2026-07-21 | MIT | **Turbo 350M** (low latency, paralinguistic tags like `[laugh]`), **Nano 110M** (CPU, 3x realtime), **Multilingual V3 500M** (23+ languages), voice cloning, emotion exaggeration, **PerTh watermark** on every output | Med (laptop GPU); Nano could go on-device |
| [QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | 13.6k | 2026-03-17 (model repo) | Apache-2.0 | 0.6B/1.7B; **97 ms streaming**; 10 languages; 3-second cloning and voice design by prompt | Med (laptop GPU) |
| [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice) | 14.0k | 2026-09-28 | Apache-2.0 | Voice-cloning TTS for 600+ languages | Med |
| [OpenMOSS/MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano) | 4.4k | 2026-09-06 | Apache-2.0 | 100M realtime CPU TTS with cloning, 48 kHz | Med–High |
| [microsoft/VibeVoice](https://github.com/microsoft/VibeVoice) (TTS) | 54.5k | 2026-09-03 | MIT | Realtime-0.5B (~300 ms), long-form 1.5B. **TTS code was removed from the repo after misuse**, and Microsoft advises against commercial use without further testing | Med |
| [neuphonic/neutts](https://github.com/neuphonic/neutts) | 6.3k | 2026-07-30 | NeuTTS Open License v1.0 (custom) | On-device TTS with cloning | High (check license) |
| [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl) (rhasspy/piper archived) | 5.7k | 2026-09-28 | **GPL-3.0** | Fast local VITS voices | High (copyleft) |
| [QwenAudio/CosyVoice](https://github.com/QwenAudio/CosyVoice) | 23.8k | 2026-05-25 | Apache-2.0 | Multilingual streaming TTS (server) | Med |
| [boson-ai/higgs-audio](https://github.com/boson-ai/higgs-audio) | 8.4k | 2026-06-05 | Apache-2.0 | Expressive text-audio model (server) | Med |
| [0xShug0/audio.cpp](https://github.com/0xShug0/audio.cpp) | 3.1k | 2026-09-28 | Apache-2.0 | ggml engine for TTS, STT, VAD and voice conversion | Med |
| [Blaizzy/mlx-audio](https://github.com/Blaizzy/mlx-audio) | 8.0k | 2026-09-28 | MIT | TTS/STT/STS on MLX | Low (Mac) |
| [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) | 32.9k | 2026-09-16 | **Fish Audio Research License (non-commercial)** | High-quality cloning | Med (license) |
| [index-tts/index-tts](https://github.com/index-tts/index-tts) | 24.2k | 2026-08-18 | **bilibili Model Use License** | Controllable zero-shot TTS | Med (license) |
| [SWivid/F5-TTS](https://github.com/SWivid/F5-TTS) | 15.3k | 2026-09-21 | MIT code, **CC-BY-NC weights** (per HF card) | Flow-matching cloning TTS | Med (license) |
| [nari-labs/dia](https://github.com/nari-labs/dia) / [dia2](https://github.com/nari-labs/dia2) | 19.4k / 1.2k | 2025-11 **SLOWING** | Apache-2.0 | Dialogue TTS (streaming in dia2) | Med |
| [canopyai/Orpheus-TTS](https://github.com/canopyai/Orpheus-TTS) | 6.3k | 2025-12-05 **SLOWING** | Apache-2.0 | LLM-based emotive TTS | Med |
| [SesameAILabs/csm](https://github.com/SesameAILabs/csm) | 14.7k | 2025-05-27 **STALE** | Apache-2.0 | Conversational speech model | Low |
| [Zyphra/Zonos](https://github.com/Zyphra/Zonos) | 7.2k | 2025-03-05 **STALE** | Apache-2.0 | — | Low |
| [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | 43.9k | 2026-09-28 | **AGPL-3.0** | Local ElevenLabs-style app (reference only) | Low |

### 3.5 Realtime voice pipelines, VAD and turn-taking

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [livekit/agents](https://github.com/livekit/agents) | 14.4k | 2026-09-28 (1.8.3) | Apache-2.0 | Production voice/video agents over WebRTC: VAD, **audio turn detector** (`v1` on LiveKit Inference; **`v1-mini` runs locally on CPU** under the LiveKit Model License; 14 languages), interruptions, any STT/LLM/TTS or realtime speech-to-speech model | High (with RN client) |
| [livekit/agents-js](https://github.com/livekit/agents-js) | 937 | 2026-09-27 | Apache-2.0 | Node/TS version of Agents | High |
| [livekit/livekit](https://github.com/livekit/livekit) | 21.2k | 2026-09-28 | Apache-2.0 | Self-hostable SFU (LiveKit Cloud has a free tier) | Med |
| [livekit/client-sdk-react-native](https://github.com/livekit/client-sdk-react-native) | 289 | 2026-09-28 | Apache-2.0 | `@livekit/react-native` 3.0 + `@livekit/react-native-expo-plugin` | High |
| [pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat) | 15.9k | 2026-09-28 (v1.12.0) | BSD-2 | Python voice/multimodal pipelines: dozens of STT/LLM/TTS providers, local Whisper/Moonshine/Piper, S2S (OpenAI Realtime, Gemini Live, Nova Sonic, Ultravox), Daily / LiveKit / SmallWebRTC / WebSocket transports. Clients for JS, React, RN, Swift, Kotlin | High |
| [pipecat-ai/smart-turn](https://github.com/pipecat-ai/smart-turn) | 1.6k | 2026-01-29 (model stable) | BSD-2 (weights too) | **Smart Turn v3.2**: ~8M params (Whisper-tiny encoder + classifier), 8 MB int8, **~10–100 ms on CPU**, 23 languages. Semantic end-of-turn detection | High (server or local) |
| [pipecat-ai/voice-ui-kit](https://github.com/pipecat-ai/voice-ui-kit) | 417 | 2026-09-28 | BSD-2 | React components and templates for voice UIs | Med |
| [pipecat-ai/pipecat-client-react-native-transports](https://github.com/pipecat-ai/pipecat-client-react-native-transports) | 20 | 2026-09-28 | BSD-2 | RN transports (`@pipecat-ai/react-native-small-webrtc-transport`, `-daily-transport` 1.8.0). Small community | High |
| [pipecat-ai/pipecat-flows](https://github.com/pipecat-ai/pipecat-flows) | 626 | **ARCHIVED** (2026-07) | BSD-2 | Structured dialogue flows (archived) | — |
| [snakers4/silero-vad](https://github.com/snakers4/silero-vad) | 10.3k | 2026-09-23 | MIT | The default VAD (ONNX, tiny) | High |
| [ricky0123/vad](https://github.com/ricky0123/vad) | 2.1k | 2026-09-12 | ISC | Silero VAD in the browser (`@ricky0123/vad-web` / `vad-react`) | High (PWA) |
| [TEN-framework/ten-vad](https://github.com/TEN-framework/ten-vad) | 2.3k | 2026-02-02 **SLOWING** | Apache-2.0 **+ non-compete conditions (Agora)** | Low-latency VAD | Med (license) |
| [TEN-framework/ten-framework](https://github.com/TEN-framework/ten-framework) | 11.1k | 2026-09-28 | Apache-2.0 with extra conditions | Conversational voice agent framework | Med |
| [huggingface/speech-to-speech](https://github.com/huggingface/speech-to-speech) | 13.3k | 2026-09-28 | Apache-2.0 | Voice agents built from open models | Med |
| [kyutai-labs/unmute](https://github.com/kyutai-labs/unmute) | 1.5k | 2026-09-09 | MIT | Wraps any text LLM with Kyutai streaming STT and TTS | Med |
| [kyutai-labs/moshi](https://github.com/kyutai-labs/moshi) | 11.2k | 2026-09-09 | MIT/Apache code, **CC-BY-4.0 weights** | Full-duplex speech model (GPU) | Med |
| [kyutai-labs/delayed-streams-modeling](https://github.com/kyutai-labs/delayed-streams-modeling) | 3.0k | 2026-01-26 **SLOWING** | Apache-2.0 | Kyutai streaming STT/TTS | Med |
| [NVIDIA/personaplex](https://github.com/NVIDIA/personaplex) | 10.6k | 2026-03-02 **SLOWING** | MIT (code) | Full-duplex persona speech-to-speech (big GPU) | Low |
| [QwenLM/Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni) | 4.0k | 2026-04-23 | Apache-2.0 | End-to-end omni model (server) | Med |
| [QwenAudio/qwen-audio-agent](https://github.com/QwenAudio/qwen-audio-agent) | 2.8k | 2026-09-28 | Apache-2.0 | Realtime voice runtime for agents | Med |
| [fixie-ai/ultravox](https://github.com/fixie-ai/ultravox) | 4.6k | 2025-12-12 **SLOWING** | MIT | Speech-native LLM | Med |
| [gradio-app/fastrtc](https://github.com/gradio-app/fastrtc) | 4.6k | 2026-01-12 **SLOWING** | MIT | Python realtime WebRTC/WebSocket helpers | Med |
| [openai/openai-realtime-agents](https://github.com/openai/openai-realtime-agents) | 7.0k | 2026-01-07 **SLOWING** | MIT | Reference agent patterns on the Realtime API | Med |
| [google-gemini/live-api-web-console](https://github.com/google-gemini/live-api-web-console) | 2.6k | 2026-06-21 | Apache-2.0 | React starter for the Gemini Live API (voice + camera) | High (web) |
| [software-mansion/react-native-audio-api](https://github.com/software-mansion/react-native-audio-api) | 844 | 2026-09-28 (0.13.6) | MIT | Web Audio API for RN: low-latency record, playback and streaming (needed for custom local voice loops) | High |
| [vocodedev/vocode-core](https://github.com/vocodedev/vocode-core) | 3.8k | 2024-11-15 **STALE** | MIT | — | — |

### 3.6 Vision (segmentation, detection, depth, VLMs, pose, OCR)

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [facebookresearch/sam3](https://github.com/facebookresearch/sam3) | 11.8k | 2026-09-18 | **SAM License** (royalty-free, commercial use allowed; gated weights; trade-control/ITAR limits) | **Text- or exemplar-prompted segmentation and tracking** ("all the red cups"). 848M params, so it fits 8 GB VRAM. **SAM 3.1** (Mar 2026) adds faster multi-object tracking. Also in transformers.js | High (laptop GPU → phone) |
| [facebookresearch/sam2](https://github.com/facebookresearch/sam2) | 19.9k | 2026-05-30 | Apache-2.0 | Click-prompted image/video segmentation | Med |
| [facebookresearch/EdgeTAM](https://github.com/facebookresearch/EdgeTAM) | 989 | 2026-01-27 **SLOWING** | Apache-2.0 | **On-device** track-anything model, a SAM 2 variant (CVPR'25) | High |
| [ChaoningZhang/MobileSAM](https://github.com/ChaoningZhang/MobileSAM) | 5.9k | 2026-05-05 | Apache-2.0 | Lightweight SAM for mobile | High |
| [PABannier/sam3.cpp](https://github.com/PABannier/sam3.cpp) | 374 | 2026-09-16 | MIT | SAM 3 in portable C/C++ | Med |
| [SimonZeng7108/efficientsam3](https://github.com/SimonZeng7108/efficientsam3) | 688 | 2026-08-11 | **No license (do not copy)** | Distilled SAM 3 for edge | — |
| [facebookresearch/sam-3d-objects](https://github.com/facebookresearch/sam-3d-objects) / [sam-3d-body](https://github.com/facebookresearch/sam-3d-body) | 7.5k / 3.6k | 2026-06 / 2026-02 | SAM License | Single image → 3D object or human mesh | Med (wow, server) |
| [m87-labs/moondream](https://github.com/m87-labs/moondream) (renamed) | 10.1k | 2026-04-20 | Apache-2.0 (code, MD2) / **BSL-1.1 (MD3 weights)** | Tiny VLM: caption, query, detect, point, count | Med–High |
| [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) | 62.1k | 2026-09-28 | **AGPL-3.0** (or paid) | YOLO26 (Jan 2026, NMS-free, edge-optimized), YOLO27, YOLO11; export to Core ML, TFLite, ONNX | High (**license trap**) |
| [roboflow/rf-detr](https://github.com/roboflow/rf-detr) | 9.6k | 2026-09-28 | **Apache-2.0** (N–L sizes); PML-1.0 for XL/2XL | Real-time detection + instance segmentation. The permissive YOLO alternative; in transformers.js and RN ExecuTorch | High |
| [lyuwenyu/RT-DETR](https://github.com/lyuwenyu/RT-DETR) / [Peterande/D-FINE](https://github.com/Peterande/D-FINE) | 5.6k / 3.3k | 2026-09 / 2026-08 | Apache-2.0 | Real-time DETR detectors | High |
| [THU-MIG/yoloe](https://github.com/THU-MIG/yoloe) | 2.3k | 2025-06-26 **STALE** | AGPL-3.0 | Open-vocabulary YOLO | — |
| [IDEA-Research/GroundingDINO](https://github.com/IDEA-Research/GroundingDINO) | 10.6k | 2024-08-12 **STALE** | Apache-2.0 | Open-vocab detection (superseded by SAM 3) | — |
| [ByteDance-Seed/Depth-Anything-3](https://github.com/ByteDance-Seed/Depth-Anything-3) | 6.4k | 2026-07-27 | Apache code; **Small/Base Apache, Large/Giant CC-BY-NC** | Mono, metric and multi-view depth (0.08B–1.4B) | Med–High |
| [DepthAnything/Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | 8.9k | 2026-03-24 **SLOWING** | Apache code; Small Apache, others CC-BY-NC | Mono depth; small model runs in the browser | High (Small) |
| [apple-aiml-research/ml-fastvlm](https://github.com/apple-aiml-research/ml-fastvlm) | 7.4k | 2026-09-11 | Apple sample-code license + model license | Fast VLM with an **iOS demo app** (needs Xcode) | Low (Mac) |
| [apple-aiml-research/ml-depth-pro](https://github.com/apple-aiml-research/ml-depth-pro) | 5.7k | 2026-09-11 | Apple license | Sharp metric depth | Med |
| [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | 37.1k | 2026-09-28 | Apache-2.0 | Hands, pose, face mesh and gestures at 30+ FPS in the browser or natively | **High** |
| [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 90.4k | 2026-09-16 | Apache-2.0 | PP-OCRv5 (mobile models) + PaddleOCR-VL document parsing | High (mobile OCR) |
| [mindee/doctr](https://github.com/mindee/doctr) | 6.4k | 2026-09-28 | Apache-2.0 | OCR (PyTorch/ONNX) | Med |
| [datalab-to/surya](https://github.com/datalab-to/surya) | 21.4k | 2026-09-11 | Apache code, **OpenRAIL-M-style weights with commercial terms** | OCR, layout and tables in 90+ languages | Med |
| [JaidedAI/EasyOCR](https://github.com/JaidedAI/EasyOCR) | 30.0k | 2025-12-05 **SLOWING** | Apache-2.0 | Classic OCR | Med |
| [deepseek-ai/DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) / [-OCR-2](https://github.com/deepseek-ai/DeepSeek-OCR-2) | 23.9k / 3.4k | 2026-01 / 2026-02 **SLOWING** | MIT / Apache-2.0 | OCR VLMs (server) | Med |
| [zai-org/GLM-OCR](https://github.com/zai-org/GLM-OCR) | 7.5k | 2026-04-21 | Apache-2.0 | OCR VLM | Med |
| [studio-dots-ai/dots.ocr](https://github.com/studio-dots-ai/dots.ocr) | 9.2k | 2026-03-24 **SLOWING** | MIT | Layout-parsing VLM | Med |
| [baidu/Unlimited-OCR](https://github.com/baidu/Unlimited-OCR) | 26.5k | 2026-07-29 | MIT | Long-horizon document parsing | Med |
| [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | 80.8k | 2026-09-28 | Apache-2.0 **+ extra commercial-threshold terms** | PDF/Office → Markdown/JSON | Low |
| [allenai/olmocr](https://github.com/allenai/olmocr) | 19.7k | 2026-03-25 **SLOWING** | Apache-2.0 | PDF linearization | Low |
| [QwenLM/Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) | 20.0k | 2026-01-30 **SLOWING** | Apache-2.0 | VLMs (superseded by natively multimodal Qwen3.5) | Med |
| [facebookresearch/dinov3](https://github.com/facebookresearch/dinov3) | 11.5k | 2026-07-15 | DINOv3 License (custom) | Dense visual features (few-shot segmentation, retrieval) | Med |
| [ngxson/smolvlm-realtime-webcam](https://github.com/ngxson/smolvlm-realtime-webcam) | 5.6k | 2025-05-12 **STALE** | none stated | Viral 2025 webcam + VLM demo (pattern only) | — |

### 3.7 Agent frameworks (server or edge "brain")

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [anthropics/claude-agent-sdk-typescript](https://github.com/anthropics/claude-agent-sdk-typescript) | 1.8k | 2026-09-28 (npm 0.3.284) | **Anthropic Commercial Terms (not OSS)** | Claude Code's agent loop, tools, MCP, subagents, skills and hooks, as a library (Node) | Med |
| [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | 8.2k | 2026-09-28 | MIT | Same, in Python | Med |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) / [-js](https://github.com/openai/openai-agents-js) | 29.7k / 3.9k | 2026-09-28 / 2026-09-25 (0.18.0) | MIT | Agents, handoffs, guardrails, sessions, tracing, MCP; **realtime voice agents** (browser WebRTC); sandbox agents | Med–High |
| [vercel/ai](https://github.com/vercel/ai) | 27.0k | 2026-09-28 (ai 7.0.x) | Apache-2.0 | TS streaming, tools, structured output, agents; **works in Expo**; RN on-device providers via callstackincubator/ai | High |
| [mastra-ai/mastra](https://github.com/mastra-ai/mastra) | 28.4k | 2026-09-28 (core 1.71) | Apache-2.0 **+ Enterprise License for `ee/` dirs** | TS agents, workflows, observational memory, RAG, voice, MCP, evals, Studio | Med |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) / [langgraphjs](https://github.com/langchain-ai/langgraphjs) | 42.4k / 3.3k | 2026-09-28 | MIT | Durable, stateful agent graphs | Med |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) | 20.2k | 2026-09-28 | MIT | Typed Python agents, now including realtime voice | Med |
| [google/adk-python](https://github.com/google/adk-python) / [adk-js](https://github.com/google/adk-js) | 21.7k / 1.4k | 2026-09-28 | Apache-2.0 | Google ADK (with Gemini Live streaming) | Med |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | 13.8k | 2026-09-28 | MIT | .NET/Python agents and workflows | Low |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) / [agno-agi/agno](https://github.com/agno-agi/agno) / [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) / [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk) | 29.6k / 42.4k / 59.1k / 8.5k | 2026-09 | Apache / Apache / MIT / Apache | Alternatives | Low |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 116.6k | 2026-09-26 | MIT | Browser agents (cloud browser, live view can be streamed to the phone) | Med |
| [browserbase/stagehand](https://github.com/browserbase/stagehand) | 25.4k | 2026-09-28 | MIT | TS browser automation SDK (act, extract, observe) | Med |
| [openclaw/openclaw](https://github.com/openclaw/openclaw) | 390.7k | 2026-09-28 | MIT | Personal agent **gateway**: 20+ chat channels (WhatsApp, Telegram, iMessage…), skills and plugins, and **iOS/Android node apps** (voice, camera, canvas) | High (as platform or inspiration) |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) / [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 249.8k / 238.7k | 2026-09-28 | MIT | 2026's viral agent harnesses (context for "what's hot") | Low |
| [open-jarvis/OpenJarvis](https://github.com/open-jarvis/OpenJarvis) | 10.3k | 2026-09-28 | Apache-2.0 | "Personal AI on personal devices" | Med |

### 3.8 Phone-use and GUI agents

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [droidrun/mobilerun](https://github.com/droidrun/mobilerun) (ex DroidRun) | 9.5k | 2026-09-28 | MIT | LLM-agnostic agent that controls **Android** through a Portal app (accessibility tree, screenshots, gestures) + ADB; an iOS Portal flow; Python API/CLI; cloud phones | **High** |
| [minitap-ai/mobile-use](https://github.com/minitap-ai/mobile-use) | 3.2k | 2026-09-14 | Apache-2.0 | Android real devices and emulators; **iOS simulators only (macOS)**; claims **100% on AndroidWorld** **(vendor)**; multi-provider | **High** (Android) |
| [zai-org/Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) | 26.3k | 2026-03-06 **SLOWING** | Apache-2.0 | AutoGLM-Phone-9B (+Multilingual) phone agent over ADB/HDC; 50+ Chinese apps. Self-hosting needs **24 GB+ VRAM**; a hosted API exists (Zhipu, ModelScope) | High (Android; China-centric) |
| [ShawnPana/phone-harness](https://github.com/ShawnPana/phone-harness) | 3.1k | 2026-09-27 | MIT | Lets Claude Code or Codex (MCP/skill) drive a phone: **Android via ADB**; iPhone via **macOS iPhone Mirroring** (Mac only). No phone-side install | High (Android) |
| [callstack/agent-device](https://github.com/callstack/agent-device) | 4.8k | 2026-09-28 | MIT | CLI, MCP and Node API for coding agents to drive and verify iOS/Android apps (accessibility snapshots, RN component trees). iOS needs macOS | Low (dev/QA; great for testing your own app) |
| [software-mansion/argent](https://github.com/software-mansion/argent) | 2.9k | 2026-09-28 | Apache-2.0 | Agentic toolkit to control, debug and profile iOS/Android apps | Low (dev) |
| [mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp) | 8.3k | 2026-09-23 | Apache-2.0 | MCP server for mobile automation (devices, emulators, simulators) | Med |
| [X-PLUG/MobileAgent](https://github.com/X-PLUG/MobileAgent) | 9.3k | 2026-07-07 | MIT | Mobile-Agent-v3 / GUI-Owl research family | Med |
| [bytedance/UI-TARS](https://github.com/bytedance/UI-TARS) / [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | 11.5k / 39.1k | 2026-01 **SLOWING** / 2026-09-24 | Apache-2.0 | GUI agent model / desktop agent stack | Med |
| [simular-ai/Agent-S](https://github.com/simular-ai/Agent-S) | 12.4k | 2026-09-05 | Apache-2.0 | Computer-use agent framework | Low |
| [OpenBMB/AgentCPM-GUI](https://github.com/OpenBMB/AgentCPM-GUI) | 1.4k | 2026-01-11 **SLOWING** | Apache-2.0 | On-device Android GUI agent model | Med |
| [IPADS-SAI/MobiAgent](https://github.com/IPADS-SAI/MobiAgent) | 1.9k | 2026-07-17 | Apache-2.0 | Mobile GUI agent | Med |
| [kellyvv/PhoneClaw](https://github.com/kellyvv/PhoneClaw) | 1.3k | 2026-08-06 | Apache-2.0 | iOS (Swift) local agent runtime with on-device models and "skills" | Low (Mac) |
| [google-research/android_world](https://github.com/google-research/android_world) | 936 | 2026-09-28 | Apache-2.0 | Benchmark and eval environment. Use it to **show evals** | Low (credibility) |
| [TencentQQGYLab/AppAgent](https://github.com/TencentQQGYLab/AppAgent) | 6.9k | 2025-03-19 **STALE** | MIT | — | — |

### 3.9 Memory

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | 66.2k | 2026-09-25 | Apache-2.0 | User, session and agent memory; new algorithm (Apr 2026) reports **LoCoMo 92.5 / LongMemEval 94.4** **(vendor)**; Python + TS SDK (`mem0ai` 3.3.1); self-host or cloud; OpenMemory MCP | Med (invisible but makes the app "know you") |
| [getzep/graphiti](https://github.com/getzep/graphiti) | 31.3k | 2026-09-28 | Apache-2.0 | **Temporal knowledge graph** (facts with validity windows and provenance); Neo4j, FalkorDB or Neptune (Kuzu deprecated); MCP server; sub-second queries | Med |
| [getzep/zep](https://github.com/getzep/zep) | 4.9k | 2026-09-18 | Apache-2.0 | Now examples and integrations; Zep itself is the hosted product (Community Edition discontinued) | Low |
| [letta-ai/letta](https://github.com/letta-ai/letta) | 25.0k | 2026-09-10 | Apache-2.0 | Stateful agents with self-editing memory (MemGPT lineage) | Med |
| [topoteretes/cognee](https://github.com/topoteretes/cognee) / [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) / [MemTensor/MemOS](https://github.com/MemTensor/MemOS) | 31.1k / 31.0k / 11.6k | 2026-09 | Apache / MIT / Apache | Alternatives (graph+vector memory; local memory engine + app; memory OS) | Med |
| [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory) | 4.1k | 2026-09-28 | **AGPL-3.0** | Markdown-based memory via MCP | Low |
| [asg017/sqlite-vec](https://github.com/asg017/sqlite-vec) | 8.1k | 2026-05-18 | Apache-2.0 | **On-device vector search**. Bundled with `expo-sqlite`; plugin for [op-sqlite](https://github.com/OP-Engineering/op-sqlite) | High (offline RAG) |

### 3.10 MCP frameworks

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) / [python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 13.5k / 24.4k | 2026-09-28 / 2026-09-25 | MIT → Apache-2.0 transition | Official SDKs | Med |
| [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp) (ex jlowin) | 27.9k | 2026-09-28 | Apache-2.0 | Pythonic MCP servers and clients | Med |
| [punkpeye/fastmcp](https://github.com/punkpeye/fastmcp) | 3.3k | 2026-09-26 | MIT | TS MCP server framework | Med |
| [mcp-use/mcp-use](https://github.com/mcp-use/mcp-use) | 10.7k | 2026-09-28 | MIT | Full-stack MCP: build MCP Apps for ChatGPT/Claude plus agent clients | Med |
| [cloudflare/agents](https://github.com/cloudflare/agents) | 5.7k | 2026-09-28 | MIT | Stateful agents on Durable Objects, remote MCP hosting, state sync to clients, scheduling | Med |
| [modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps) (**MCP Apps**) | 2.9k | 2026-09-25 (npm 2.0.3) | MIT → Apache | SEP-1865, stable 2026-01-26: `ui://` resources rendered in sandboxed iframes; hosts include Claude, ChatGPT, VS Code, Goose, Postman, MCPJam | Med (shows up in Claude/ChatGPT **mobile** apps) |
| [MCP-UI-Org/mcp-ui](https://github.com/MCP-UI-Org/mcp-ui) | 5.2k | 2026-09-16 | Apache-2.0 | MCP Apps-compatible client/server SDK | Med |
| [openai/openai-apps-sdk-examples](https://github.com/openai/openai-apps-sdk-examples) | 2.3k | 2026-04-15 | MIT | ChatGPT Apps examples (Apps SDK aligns with MCP Apps) | Med |

### 3.11 Generative UI

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [vercel-labs/json-render](https://github.com/vercel-labs/json-render) | 18.4k | 2026-09-25 | Apache-2.0 | Zod-defined **component catalog → LLM emits a JSON spec → streamed progressive render**. Renderers for React, **React Native**, Vue, Svelte, Remotion, PDF, email, Ink | **High** (native generative UI) |
| [a2ui-project/a2ui](https://github.com/a2ui-project/a2ui) (Google) | 16.5k | 2026-09-28 | Apache-2.0 | Declarative agent → UI protocol v0.9.1 (v1.0 RC); Flutter GenUI, Angular, Lit; `@a2ui/react` 0.12 on npm; SwiftUI/Compose planned | Med |
| [CopilotKit/CopilotKit](https://github.com/CopilotKit/CopilotKit) + [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | 37.6k / 16.1k | 2026-09-28 | MIT | Agent ↔ frontend protocol (AG-UI) + React stack | Med |
| [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui) | 12.3k | 2026-09-28 | MIT | Chat UI primitives (React) | Med |
| [thesysdev/openui](https://github.com/thesysdev/openui) | 9.9k | 2026-09-28 | MIT | "Open standard for generative UI" (Thesys) | Med |
| [tambo-ai/tambo](https://github.com/tambo-ai/tambo) | 11.2k | 2026-09-26 | MIT | Generative UI SDK for React | Med |
| [vercel/chatbot](https://github.com/vercel/chatbot) | 21.0k | 2026-07-08 | Apache-2.0 | Full Next.js AI chatbot reference | Low |

### 3.12 Realtime sync and backend

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [get-convex/convex-backend](https://github.com/get-convex/convex-backend) | 12.6k | 2026-09-28 | **FSL-1.1-Apache-2.0** (client `convex-js` Apache-2.0) | Reactive DB + functions; live queries to RN; good for agent-state streaming | Med |
| [instantdb/instant](https://github.com/instantdb/instant) | 10.5k | 2026-09-28 | Apache-2.0 | Realtime DB with auth, presence, storage; `@instantdb/react-native` | Med |
| [yjs/yjs](https://github.com/yjs/yjs) | 22.9k | 2026-09-28 | MIT | CRDTs for collaborative state | Med |
| [liveblocks/liveblocks](https://github.com/liveblocks/liveblocks) | 4.7k | 2026-09-28 | Apache-2.0 clients; **AGPL server/CLI** | Hosted multiplayer + AI agent presence | Med |
| [electric-sql/electric](https://github.com/electric-sql/electric) / [rocicorp/mono](https://github.com/rocicorp/mono) (Zero) | 10.4k / 3.4k | 2026-09-28 | Apache-2.0 | Postgres sync engines | Low–Med |
| [tinyplex/tinybase](https://github.com/tinyplex/tinybase) / [livestorejs/livestore](https://github.com/livestorejs/livestore) / [powersync-ja/powersync-js](https://github.com/powersync-ja/powersync-js) | 5.2k / 3.7k / 725 | 2026-09 | MIT / Apache / Apache | Local-first reactive stores with Expo adapters | Med |
| [partykit/partykit](https://github.com/partykit/partykit) → [cloudflare/partykit](https://github.com/cloudflare/partykit) | 5.7k → 1.3k | 2026-01 **SLOWING** → 2026-08 | MIT / ISC | Multiplayer rooms on Workers | Low |

### 3.13 Mobile frameworks and native plumbing

| Repo | Stars | Last push | License | What it enables | Phone demo |
|---|---|---|---|---|---|
| [expo/expo](https://github.com/expo/expo) | 52.5k | 2026-09-28 | MIT | **SDK 57** (Jun 30 2026, RN 0.86), **SDK 58 beta** (Sep 15 2026); dev client, config plugins, expo-camera/audio/sqlite (with sqlite-vec), EAS Build/Update | **High (the shell)** |
| [react/react-native](https://github.com/react/react-native) (moved) | 126.8k | 2026-09-28 | MIT | RN 0.87.1; New Architecture only | High |
| [margelo/react-native-vision-camera](https://github.com/margelo/react-native-vision-camera) | 9.6k | 2026-09-14 (v5.2.3) | MIT | 30–240 FPS **frame processors** (JS worklets), GPU resizer (Metal/Vulkan), drawing and shaders on frames, barcode scanning | **High** |
| [margelo/nitro](https://github.com/margelo/nitro) | 2.0k | 2026-09-26 | MIT | Fast native modules (C++/Swift/Kotlin) over JSI, for wrapping any native SDK | Med |
| [software-mansion/react-native-reanimated](https://github.com/software-mansion/react-native-reanimated) / [Shopify/react-native-skia](https://github.com/Shopify/react-native-skia) | 11.0k / 8.6k | 2026-09-28 | MIT | 60–120 FPS animation and GPU drawing (overlays, masks, voice orbs) | High (polish) |
| [OP-Engineering/op-sqlite](https://github.com/OP-Engineering/op-sqlite) | 1.0k | 2026-09-27 | MIT | Fast SQLite with a sqlite-vec plugin | Med |
| [ionic-team/capacitor](https://github.com/ionic-team/capacitor) | 16.7k | 2026-09-28 | MIT | v8.5: wrap a web app natively. iOS still needs a Mac or paid cloud CI | Med |
| [vite-pwa/vite-plugin-pwa](https://github.com/vite-pwa/vite-plugin-pwa) / [serwist/serwist](https://github.com/serwist/serwist) | 4.3k / 1.5k | 2026-05-05 / 2026-07-22 | MIT | PWA service workers and manifest (Vite / Next) | High (PWA path) |
| [tauri-apps/tauri](https://github.com/tauri-apps/tauri) / [lynx-family/lynx](https://github.com/lynx-family/lynx) | 111.5k / 15.1k | 2026-09 | Apache/MIT, Apache | Alternatives (Rust + web mobile; ByteDance Lynx) | Low |

### 3.14 Dev and demo utilities

| Repo | Stars | License | Why |
|---|---|---|---|
| [Genymobile/scrcpy](https://github.com/Genymobile/scrcpy) | 150.6k | Apache-2.0 | Mirror and record the Android screen on the laptop for demo videos, and show phone-use agents live |
| [cloudflare/cloudflared](https://github.com/cloudflare/cloudflared) / [tailscale/tailscale](https://github.com/tailscale/tailscale) | 16.0k / 37.0k | Apache-2.0 / BSD-3 | Expose the RTX 5070 laptop server (SAM 3, TTS, LLM) to the phone over HTTPS or a private network |
| [ollama/ollama](https://github.com/ollama/ollama) | 181.9k | MIT | Easiest local model server on Windows |
| [vllm-project/vllm](https://github.com/vllm-project/vllm) / [sgl-project/sglang](https://github.com/sgl-project/sglang) | 92.9k / 36.5k | Apache-2.0 | High-throughput serving. **Linux-first, so use WSL2/Docker on Windows** |

---

## 4. Reference apps to fork or learn from

Primary five (a phone-first AI app shape, decent code quality, permissive license), then two product-pattern references.

1. **[google-ai-edge/gallery](https://github.com/google-ai-edge/gallery)**: 24.8k★, Apache-2.0, pushed 2026-09-27 (v1.0.19). Kotlin/Compose Android source. An iOS build is on the App Store (iOS 17+), but I found only Android source in the repo.
   - **Features:** Ask Image (camera), Audio Scribe (live transcription and translation), AI Chat with thinking mode, Prompt Lab, **Agent Skills** (SKILL.md, JS skills that can return images or webviews, native skills), **experimental MCP client** (on-device model calling Streamable-HTTP MCP servers), **Mobile Actions** (FunctionGemma 270M), model allowlist + on-device benchmarks.
   - **Borrow:** model download/management UX, the skill system design, on-device tool-calling patterns, Gemma 4 + LiteRT-LM integration.
   - **Caveat:** native Kotlin, not RN.
2. **[a-ghorbani/pocketpal-ai](https://github.com/a-ghorbani/pocketpal-ai)**: 8.4k★, MIT, pushed 2026-09-28. React Native + llama.rn (TypeScript; `__tests__`, `e2e`, fastlane, docs). Mature on-device app: *"Chat with language models, give them a voice, and let them use tools — all on-device"*. Includes HF model browsing and downloads, per-model settings, a public benchmark leaderboard, and "Pals" personas (PalsHub). On the App Store and Google Play.
   - **Borrow:** download/storage and memory-pressure handling, and llama.rn wiring on both OSes.
3. **[off-grid-ai/OGAM](https://github.com/off-grid-ai/OGAM)** ("Off Grid"): 3.2k★, MIT, pushed 2026-09-28. RN + llama.rn + whisper.rn + on-device Stable Diffusion (MNN / Core ML). Has vision (SmolVLM, Qwen3-VL), tool calling, a document knowledge base, and OpenCL/Metal/Hexagon acceleration. Jest/RNTL + JUnit + XCTest in CI, codecov, AGENTS.md, and App Store/Play listings.
   - **Borrow:** the multi-modality on-device architecture and its testing setup.
   - **Caveat:** a paid Pro tier (Kokoro TTS, sync, MCP drafts) exists, so check which code is actually in the repo.
4. **[software-mansion-labs/private-mind](https://github.com/software-mansion-labs/private-mind)**: 384★, MIT, pushed 2026-09-28. **Expo + React Native ExecuTorch + SQLite**: offline chat, chat-with-your-docs RAG (PDF/TXT/MD/CSV), voice input, benchmarks, conversation branching. Has CLAUDE.md, tests, and App Store + Play listings.
   - **Borrow:** the cleanest Expo + ExecuTorch reference.
5. **[livekit-examples/agent-starter-react-native](https://github.com/livekit-examples/agent-starter-react-native)** + [livekit/agents](https://github.com/livekit/agents): MIT/Apache, pushed 2026-09-25. **Expo 57, RN 0.86.3, `@livekit/react-native` 3.0 + Expo plugin**. A voice-assistant UI (visualizer, transcripts) against a Python/Node agent. `lk app create --template agent-starter-react-native` gets you talking in minutes.
   - **Borrow:** the realtime voice client and token-server pattern.

Bonus (product patterns, not direct forks):

6. **[BasedHardware/omi](https://github.com/BasedHardware/omi)**: 13.6k★, MIT. Flutter app + FastAPI/Firebase backend + firmware. Covers conversation capture → transcription (Deepgram) → memories, action items and an apps/plugins ecosystem. It is the best open reference for a *daily-use* capture-to-memory assistant. The codebase is large and Flutter, so learn from it rather than fork it.
7. **[fikrikarim/parlor](https://github.com/fikrikarim/parlor)**: 2.1k★, Apache-2.0. A local "GPT-Live" clone: browser client (Silero VAD) → FastAPI → llama.cpp **Gemma 4 E2B/E4B hearing and seeing**, **smart-turn v3** (~20 ms), **Kokoro** TTS, and an "action head" that emits grammar-forced JSON separately from speech. It reports **~0.7 s end-of-speech → first audio** on an M3 Pro with E2B **(vendor)**. It runs on the RTX 5070 laptop with the phone as the browser client, which makes it an excellent blueprint for a realtime multimodal demo.

Also noted: [Vali-98/ChatterUI](https://github.com/Vali-98/ChatterUI) (2.8k, **AGPL**), [Mobile-Artificial-Intelligence/maid](https://github.com/Mobile-Artificial-Intelligence/maid) (2.7k, MIT, Flutter), [gluonfield/enchanted](https://github.com/gluonfield/enchanted) (6.0k, Swift), [dabit3/react-native-ai](https://github.com/dabit3/react-native-ai) (1.3k, MIT: `npx rn-ai` full-stack Expo + server scaffold with multi-provider chat and image generation), [karakeep-app/karakeep](https://github.com/karakeep-app/karakeep) (29.3k, **AGPL**, Expo app + AI tagging), [RunAnywhere sample apps](https://github.com/RunanywhereAI/runanywhere-sdks) (license-capped).

---

## 5. Top 12 building blocks (shortlist)

Selection criteria: phone wow, daily usefulness, engineering depth, recruiter signal, 3–6 week feasibility, and it has to work from Windows.

| # | Building block | Why it makes the cut |
|---|---|---|
| 1 | **Expo SDK 57/58 + EAS Build + dev client** ([expo/expo](https://github.com/expo/expo), MIT) | One TypeScript codebase for *either* phone. Android builds locally; iPhone builds in EAS cloud (needs a paid Apple account). Config plugins exist for llama.rn, VisionCamera and LiveKit. Shows production RN skill (New Architecture, native modules). |
| 2 | **VisionCamera v5** ([margelo/react-native-vision-camera](https://github.com/margelo/react-native-vision-camera), MIT) | The base of any "point your phone at X" wow: 30–240 FPS frame processors, GPU resize, and drawing on frames. Pairs with fast-tflite or ExecuTorch for per-frame inference and Skia for overlays. |
| 3 | **React Native ExecuTorch 0.10** ([software-mansion/react-native-executorch](https://github.com/software-mansion/react-native-executorch), MIT) | The fastest route to *many* on-device modalities without writing C++: hooks for LLM/VLM, Whisper STT, Kokoro TTS, OCR, RF-DETR/YOLO detection, segmentation and embeddings, with a pre-exported catalog. Private Mind proves it ships. |
| 4 | **llama.rn 0.13 on llama.cpp** ([mybigday/llama.rn](https://github.com/mybigday/llama.rn), MIT) | The most flexible on-device reasoning engine: any GGUF (Gemma 4, Qwen3.5, LFM2.5), image/audio projectors, **grammar-constrained JSON + tool calling**, embeddings/rerank, Metal/OpenCL/Hexagon. Makes "offline agent on the phone" credible. |
| 5 | **Gemma 4 E2B/E4B + LiteRT-LM** ([google-ai-edge/LiteRT-LM](https://github.com/google-ai-edge/LiteRT-LM), Apache-2.0) | The default 2026 on-device multimodal model. Apache-2.0, **hears and sees**, about 50 tok/s GPU decode on flagships **(vendor)**. LiteRT-LM adds NPU and MTP. The Gallery app is the reference, and GGUF builds also run through llama.rn and transformers.js. |
| 6 | **sherpa-onnx + Moonshine** ([k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) Apache-2.0; [moonshine-ai/moonshine](https://github.com/moonshine-ai/moonshine) MIT) | Offline speech end to end (streaming STT, Kokoro/Kitten/Pocket TTS, VAD, wake word, diarization) on Android, iOS and WASM. Moonshine adds streaming STT tuned for live voice UIs. This gives a voice experience that works in airplane mode. |
| 7 | **LiveKit Agents + `@livekit/react-native`** ([livekit/agents](https://github.com/livekit/agents), Apache-2.0) *(alt: Pipecat + smart-turn v3.2, BSD-2)* | A production realtime voice/video agent stack with WebRTC, **semantic turn detection** (local CPU `v1-mini`), interruptions, and any STT/LLM/TTS or speech-to-speech model. It has an **Expo 57 starter**. Turn-taking and latency are the "technically smart" talking points. |
| 8 | **transformers.js v4 (WebGPU)** ([huggingface/transformers.js](https://github.com/huggingface/transformers.js), Apache-2.0) | The **iPhone-without-Mac escape hatch** and a shareable web demo link. It runs Gemma 4, Qwen3.5, Moonshine, Parakeet, Whisper, SAM 3, RF-DETR and Depth Anything in the browser, and v4.3 enables Safari 26 WebGPU. |
| 9 | **SAM 3.1 on the laptop GPU + RF-DETR / EdgeTAM on-device** ([facebookresearch/sam3](https://github.com/facebookresearch/sam3) SAM License; [roboflow/rf-detr](https://github.com/roboflow/rf-detr) Apache-2.0; [EdgeTAM](https://github.com/facebookresearch/EdgeTAM)) | The strongest visual 10-second wow: say "the cables" and every cable gets masked and tracked. SAM 3 (848M) fits in 8 GB VRAM, and its license allows commercial use. RF-DETR avoids the Ultralytics AGPL trap for on-device detection. |
| 10 | **Mobilerun (ex-DroidRun) or mobile-use** ([droidrun/mobilerun](https://github.com/droidrun/mobilerun) MIT; [minitap-ai/mobile-use](https://github.com/minitap-ai/mobile-use) Apache-2.0) | The most visceral 2026 "AI does things" demo: the agent drives real Android apps through the accessibility tree and screenshots. Works from Windows. Scope it to one narrow, reliable workflow and **show AndroidWorld-style evals**. |
| 11 | **Vercel AI SDK v7 + MCP TS SDK + json-render** ([vercel/ai](https://github.com/vercel/ai), [typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk), [vercel-labs/json-render](https://github.com/vercel-labs/json-render); Apache/MIT) | The TS agent layer: streaming, tools and structured output, with on-device providers via `@react-native-ai/*`. MCP lets the app consume or expose tools, including Claude/ChatGPT through MCP Apps, which is FDE-relevant. json-render renders **catalog-constrained generative UI as native RN components**. |
| 12 | **mem0 (or Graphiti)** ([mem0ai/mem0](https://github.com/mem0ai/mem0), [getzep/graphiti](https://github.com/getzep/graphiti); Apache-2.0) | Daily usefulness comes from remembering the user. mem0 is the simple SDK path with strong self-reported benchmarks. Graphiti's temporal graph fits apps whose facts change (schedules, habits, relationships). Pair with sqlite-vec for on-device recall. |

**Honorable mentions:**
- **Apple Foundation Models via `@react-native-ai/apple`**: an iPhone 15 Pro+ freebie. iOS 27 adds vision and a free PCC reasoning model, but the wrapper probably lags iOS 27.
- **Chatterbox Turbo / Qwen3-TTS / Pocket TTS**: high-quality TTS on the laptop GPU or CPU.
- **Claude Agent SDK / OpenAI Agents SDK**: server agents. OpenAI's JS SDK also covers browser realtime voice.
- **Convex / InstantDB**: live agent state on the phone.
- **MediaPipe**: hands, pose and face at 30+ FPS; a web-demo wow.
- **OpenClaw**: build a node or skill for it, or learn its gateway/channel architecture.
- **Cactus / RunAnywhere**: polished, but source-available with revenue caps.

---

## 6. Reference stacks built from these blocks (to speed up project selection)

- **A. Camera-first "understand anything" assistant (hybrid on-device/cloud).** Expo dev build → VisionCamera v5 frame processors → RN ExecuTorch (RF-DETR detection, OCR, image embeddings) for instant on-device overlays → llama.rn with Gemma 4 E2B or Qwen3.5-2B-VL for offline Q&A → escalate hard queries to Claude/Gemini via AI SDK (confidence routing, the way Cactus does it) → SAM 3.1 served from the RTX 5070 via cloudflared for "segment by text". Memory: mem0 + sqlite-vec. Depth to showcase: on-device/cloud routing, latency budgets, and an eval set.
- **B. Realtime voice agent that acts.** `agent-starter-react-native` (Expo) ↔ LiveKit Agents (Python) on the laptop or LiveKit Cloud: Parakeet/Moonshine STT (or a cloud STT), Claude/GPT with MCP tools, smart-turn or the LiveKit turn detector, and Chatterbox Turbo, Kokoro or Pocket TTS. Add mem0 for memory and json-render cards pushed to the phone mid-conversation. Depth to showcase: barge-in handling, end-to-end latency traces, tool reliability evals.
- **C. Phone-use agent ("do it for me").** Android phone + Mobilerun Portal or mobile-use driven from the laptop (ADB/Wi-Fi), triggered by voice from the phone, and screen-recorded with scrcpy. Keep it to one vertical (for example, "turn this screenshot/email into calendar + reminders + a reply"), with an eval harness modeled on AndroidWorld and an MCP interface so Claude can call it. Android-only.
- **D. PWA fallback (iPhone, no $99 account).** Vite/Next PWA (vite-plugin-pwa/Serwist) + transformers.js v4 (WebGPU; Safari 26+) + `@ricky0123/vad-web` + WebLLM, with a cloud fallback for older phones. Everything installs from a URL. The trade-off is weaker background and permission behavior.

---

## 7. Gotchas

### 7.1 Licenses (check before borrowing)

- **AGPL-3.0 (copyleft over the network):** [ultralytics](https://github.com/ultralytics/ultralytics) YOLO26/27/11, [YOLOE](https://github.com/THU-MIG/yoloe), YOLOv10/12/13, [ChatterUI](https://github.com/Vali-98/ChatterUI), [karakeep](https://github.com/karakeep-app/karakeep), [immich](https://github.com/immich-app/immich), [basic-memory](https://github.com/basicmachines-co/basic-memory), [VoiceStudio](https://github.com/debpalash/VoiceStudio), and the Liveblocks server. **GPL-3.0:** [piper1-gpl](https://github.com/OHF-Voice/piper1-gpl), YOLOv9. If the portfolio repo is public and MIT, avoid pulling these in. RF-DETR (Apache) replaces YOLO; Kokoro/Kitten replace Piper.
- **Non-commercial or restricted weights:**
  - Depth Anything V2 Base/Large/Giant and DA3 Large/Giant (**CC-BY-NC**)
  - fish-speech (research license)
  - F5-TTS weights (CC-BY-NC)
  - IndexTTS (bilibili license)
  - Moondream 3 (**BSL-1.1**, no competing hosted API)
  - Surya (OpenRAIL-M with commercial terms)
  - MinerU (extra commercial thresholds)
  - Apple FastVLM / Depth Pro (Apple research licenses)
  - DINOv3 and SAM 3 (custom Meta licenses: commercial OK, gated weights, trade-control clauses)
- **Source-available with revenue caps:** Cactus (free under $2M funding and revenue) and RunAnywhere (free under $1M). Fine for a student demo, but a problem if the project becomes a startup.
- **Custom or "open with conditions":** TEN VAD / TEN framework (Apache + **Agora non-compete**), LiveKit turn-detector weights (LiveKit Model License), LFM2.5 (LFM Open License with revenue threshold), NeuTTS Open License, Gemma-3-era FunctionGemma terms, Open WebUI and LobeHub (branding/community licenses), Convex backend (**FSL**, converts to Apache after 2 years), Mastra `ee/` directories (enterprise license).
- **Not open source:** the Claude Agent SDK (TS) is governed by **Anthropic Commercial Terms**, while the Python SDK repo is MIT. Apple FM and Gemini Nano are proprietary system models (free APIs).
- **No license at all:** [efficientsam3](https://github.com/SimonZeng7108/efficientsam3), [smolvlm-realtime-webcam](https://github.com/ngxson/smolvlm-realtime-webcam) and several small RN wrappers. Treat them as reference only.
- **Now permissive:** Gemma 4 moved to **Apache-2.0**, and Qwen3.5, Moonshine models, KittenTTS, Pocket TTS, Chatterbox and Qwen3-TTS are MIT or Apache. Prefer these.
- **VibeVoice:** the TTS code was pulled after misuse, and Microsoft discourages commercial use. Chatterbox watermarks all output (PerTh), which is actually a good "responsible AI" talking point.

### 7.2 Platform limits and iOS vs Android differences

- **iPhone from Windows:**
  - Device builds need the **$99/yr Apple Developer Program** plus EAS cloud builds. The free tier has monthly build caps and queues, so check current limits.
  - Expo Go can't load llama.rn, ExecuTorch, VisionCamera frame processors or LiveKit.
  - Every native tweak costs a cloud build cycle, and there is no Xcode debugger.
  - Swift-only libraries (iOS 27 FM vision/PCC/Dynamic Profiles, ClaudeForFoundationModels, MLX Swift, WhisperKit, Core AI) need a custom Expo module written blind.
- **Phone-use agents are effectively Android-only.** iOS apps cannot control other apps. The iOS routes (XCUITest/WebDriverAgent, iPhone Mirroring for phone-harness, mobile-use simulators) all need macOS. Google Play restricts AccessibilityService automation, so sideload the APK for demos.
- **System LLMs:**
  - **Apple FM** runs only on Apple Intelligence devices (iPhone 15 Pro and later) with Apple Intelligence enabled. On-device context is 8K; PCC is 32K.
  - **Gemini Nano** (ML Kit GenAI Prompt API) is **beta** and limited to an allowlist of flagship devices.
  - Neither is available on every phone, so always ship a fallback.
- **Accelerators are fragmented on Android.** llama.cpp OpenCL is Adreno-only (Q4_0/Q6_K), and Hexagon NPU is experimental (SM8450+). ExecuTorch uses Vulkan, and Mali GPUs are weaker. iOS is uniform (Metal / Core ML / ANE).
- **Background execution:** iOS kills long-running mic or camera work in the background, and PWAs get none. Android can run a foreground service with a notification, which matters for "always listening" or "ambient capture" ideas.
- **PWA on iPhone:** WebGPU requires **iOS 26+**. Heavy WebGPU models risk tab or process eviction under memory pressure. Cache weights with the Cache API or OPFS and expect occasional eviction. Camera and mic need HTTPS plus a user gesture, and Web Push works only for installed PWAs. Chrome on Android has WebGPU on Android 12+ with Qualcomm/ARM GPUs.
- **App-store ready vs demo ready:** 1–4 GB model downloads must happen on first run with progress and resume, not be bundled. Thermals throttle sustained decode after minutes, and battery drain is visible in demos.

### 7.3 Model sizes vs phone RAM (practical guide)

| Phone class (RAM) | Comfortable on-device model (4-bit) | Notes |
|---|---|---|
| iPhone 15 and older, budget Android (≤6 GB) | 0.3–1.2B (Qwen3.5-0.8B, LFM2.5-1.2B, needle 26M for tool calls) | iOS kills apps well below physical RAM |
| iPhone 15 Pro / 16 / 17, mid-range Android (8 GB) | ~1–2.6B (Gemma 4 **E2B**, Qwen3.5-2B, LFM2.5-VL-1.6B) | E2B's .litertlm is 2.58 GB on disk but ~0.6–1.7 GB peak RAM depending on backend **(vendor)**. On iOS request the `increased-memory-limit` entitlement (llama.rn's Expo plugin has an entitlements option; MLC requires it) |
| iPhone 17 Pro / Air, flagship Android (12–16 GB) | 4B class (Gemma 4 **E4B** at 3.65 GB, Qwen3.5-4B at ~3.4 GB, Phi-4-mini) | E4B decode is about 22–25 tok/s on GPU **(vendor)**. Keep context short; KV cache grows fast with image and audio tokens |
| Laptop RTX 5070, 8 GB VRAM + 32 GB RAM | ≤9B at Q4 fully on GPU (Qwen3.5-9B, Gemma 4 E4B), SAM 3 (848M), Chatterbox Turbo (350M), Qwen3-TTS-1.7B, Parakeet 0.6B | Running STT + LLM + TTS at once needs careful quantization. Gemma 4 26B-A4B needs MoE expert offload to system RAM. AutoGLM-Phone-9B under vLLM wants 24 GB+, so use the hosted API or a 4-bit GGUF |

### 7.4 Windows-dev issues

- **No local iOS toolchain.** See above. Plan for EAS cloud or the PWA route.
- **Android native builds on Windows** work, but C++-heavy modules (llama.rn, ExecuTorch, sherpa-onnx) can hit the **260-char path limit** during CMake/NDK builds. Keep the project at a short path (for example `C:\dev\app`), enable `LongPathsEnabled`, set `git config core.longpaths true`, and use JDK 17. The first native build can take 10–20+ minutes.
- **RTX 5070 is Blackwell (sm_120).** It needs **CUDA ≥ 12.8 and PyTorch ≥ 2.7 (cu128+) wheels**. Many research repos (TTS and vision) pin older torch, so bump the pins or use a CUDA 12.8+ Docker image. flash-attn, xformers and triton wheels on Windows are spotty.
- **Serving engines** vLLM and SGLang are Linux-first, so use WSL2 or Docker (GPU passthrough). Ollama and llama.cpp run natively on Windows.
- **Model export toolchains** (ExecuTorch export, LiteRT conversion, MLC compile) are Linux/macOS-first. Prefer pre-exported models: RN ExecuTorch's catalog, `litert-community/*` on Hugging Face, and GGUF from the Unsloth or ggml orgs. Otherwise run exports in WSL2.
- **Phone ↔ laptop networking for demos:** campus Wi-Fi often isolates clients. Use cloudflared or Tailscale for HTTP. WebRTC needs TURN, so use LiveKit Cloud or Daily's free tiers instead of self-hosting for demos. PWAs require HTTPS for camera and mic.

### 7.5 Stale, renamed, or risky dependencies

- **Stale:** Sesame CSM, Zonos, GroundingDINO, YOLOE, EfficientSAM, AppAgent, vocode, OpenInterpreter 01, openai-realtime-console, smolvlm-realtime-webcam, `kokoro-js` npm (last published 2025-05), hexgrad/kokoro code (the model is fine via ports).
- **Archived:** rhasspy/piper, pipecat-flows, huggingface/chat-macOS.
- **Slowing:** faster-whisper, Ultravox, Open-AutoGLM, UI-TARS (model), EdgeTAM, TEN VAD, DeepSeek-OCR.
- **Wrapper lag:** `@react-native-ai/*` was last published 2026-02 (before iOS 27); `onnxruntime-react-native` 1.24 trails core 1.30; RN wrappers for MediaPipe and sherpa-onnx are community-made with under 100★. Budget time to write a thin Nitro or Expo module if you depend on them.
- **Very new and unproven:** [expo-ai-runtime](https://github.com/stewartmoreland/expo-ai-runtime) (unified Apple FM / Gemini Nano runtime for Expo, 0★), [saidkaban/expo-ai-kit](https://github.com/saidkaban/expo-ai-kit) (88★). Worth watching, but risky as a core dependency.

---

## 8. Sources

- GitHub API and npm registry, queried 2026-09-28: all star, last-push and license figures, plus versions (Expo 57.0.25, RN 0.87.1, ai 7.0.122, llama.rn 0.13.0-rc.6, react-native-executorch 0.10.4, @huggingface/transformers 4.3.0, @livekit/react-native 3.0.0, VisionCamera 5.2.3, @modelcontextprotocol/ext-apps 2.0.3, @anthropic-ai/claude-agent-sdk 0.3.284).
- Gemma 4: [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/), [LiteRT-LM Gemma 4 model page (benchmarks)](https://developers.google.com/edge/litert-lm/models/gemma-4), [LiteRT-LM blog, 2026-05-19](https://developers.googleblog.com/blazing-fast-on-device-genai-with-litert-lm/), [Edge AI & Vision Alliance](https://www.edge-ai-vision.com/2026/04/google-pushes-multimodal-ai-further-onto-edge-devices-with-gemma-4/).
- Apple: [WWDC26 "What's new in the Foundation Models framework"](https://developer.apple.com/videos/play/wwdc2026/241/), [MacRumors SotU recap](https://www.macrumors.com/2026/06/09/apple-outlines-major-ai-and-developer-tool-updates/), [expo-ai-runtime announcement](https://www.stewmore.dev/blog/announcing-expo-ai-runtime).
- Small models: [Qwen3.5 small (Artificial Analysis)](https://artificialanalysis.ai/articles/qwen3-5-small-models), [Qwen3.5-2B card](https://huggingface.co/Qwen/Qwen3.5-2B), [Liquid AI LFM2.5 blog](https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai), [LFM2.5-2.6B (MarkTechPost)](https://www.marktechpost.com/2026/08/06/liquid-ai-lfm2-5-2-6b-on-device-agentic-model/), [LFM2.5-1.2B card](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct), [Phi-4-mini phone speeds (third-party)](https://www.promptquorum.com/power-local-llm/mobile-llm-models-phi4-gemma-smollm).
- Web: [web.dev: WebGPU in all major browsers](https://web.dev/blog/webgpu-supported-major-browsers), [caniuse WebGPU](https://caniuse.com/webgpu), [transformers.js releases](https://github.com/huggingface/transformers.js/releases).
- Expo: [dev builds on devices need a paid Apple account](https://docs.expo.dev/develop/development-builds/create-a-build/), [EAS setup](https://docs.expo.dev/build/setup/), [SDK 57 changelog](https://expo.dev/changelog/sdk-57), [changelog index (SDK 58 beta)](https://expo.dev/changelog).
- Voice: [LiveKit turn detector docs](https://docs.livekit.io/agents/build/turns/turn-detector/), READMEs of smart-turn, Pipecat, Moonshine, Pocket TTS, KittenTTS, Chatterbox, Qwen3-TTS, VibeVoice, NVIDIA-NeMo/Speech, sherpa-onnx, transcribe.cpp, Parlor.
- Vision: [SAM 3 repo and license](https://github.com/facebookresearch/sam3), [SAM 3.1 report](https://the-agent-report.com/2026/05/meta-sam-3-1-video-detection-multiplexing-may21/), [Moondream 3 license](https://huggingface.co/moondream/moondream3-preview), [YOLO26 (Roboflow)](https://blog.roboflow.com/yolo26/), [RF-DETR vs YOLO26 licensing](https://codersera.com/blog/rf-detr-vs-yolo26-object-detection-comparison-2026/), Depth-Anything-3 README.
- Android system AI: [ML Kit GenAI Prompt API](https://developers.google.com/ml-kit/genai/prompt/android).
- Agents and trends: READMEs of Mobilerun, mobile-use, Open-AutoGLM, phone-harness, agent-device, OpenClaw, Claude Agent SDK, OpenAI Agents JS, Mastra, mem0, Graphiti, MCP ext-apps, json-render, A2UI; [Analytics Vidhya trending (Jul 2026)](https://www.analyticsvidhya.com/blog/2026/07/trending-ai-github-repositories/) and [(Aug 2026)](https://www.analyticsvidhya.com/blog/2026/09/top-github-repositories-august-2026/), [Firecrawl trending repos 2026](https://www.firecrawl.dev/blog/best-github-repos).
