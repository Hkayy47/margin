# Margin

A practice and exam-prep coach. Your phone sits on a stand over your paper and watches you do math by hand. It speaks up only when a step is **provably** wrong, with a hint, never the answer.

Status: **M0 (foundations)**. See [`PLAN.md`](PLAN.md) for the full plan and [`docs/specs/M0.md`](docs/specs/M0.md) for the current milestone.

## Layout

| Folder | What | Milestone |
|---|---|---|
| `verifier/` | Step checker: LaTeX lines in, *valid / invalid / unknown* out (SymPy). 356 tests. | done (spike) |
| `app/` | Android app (Expo dev build, TypeScript) | M0 → M2 |
| `server/` | `margin-api` (FastAPI): `/verify`, `/read`, `/hint`, `/events` | M2 |
| `ml/` | Data tools, LoRA training, GGUF/ONNX export | M4 |
| `evals/` | Eval harness and reports (E1–E7 in the plan) | M1 → M5 |
| `docs/` | Milestone specs, decision log, threat model | ongoing |
| `research/` | Background research behind the plan | done |

## Run the verifier

```sh
cd verifier
uv sync
uv run pytest -q
```
