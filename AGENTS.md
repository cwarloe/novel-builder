# Agent / LLM handoff — novel-builder

You are infrastructure, not a novelist. This kit produces **human-locked canon**, not generated fiction.

Policy lives in [`KERNEL.md`](KERNEL.md) and wins if anything here conflicts.

## What this repo is

A portable kit for LLM-assisted fiction where the human owns every story fact. The machine's job is to ask, derive, and flag contradictions — never to fill gaps with plausible invention.

Two layers, and they must not mix:

| Layer | Files | Rule |
|-------|-------|------|
| **Kit** (reusable) | `KERNEL.md`, `HOW-TO.md`, `templates/`, `prompts/`, `scripts/` | Must work for a second, unrelated novel |
| **Book** (one story) | `books/<slug>/` | Everything story-specific lives here |

**Never bake book-specific rules into `KERNEL.md` or `templates/`.** The Watch is the pilot, not the spec. If a rule only makes sense for The Watch, it belongs in `books/the-watch/bible/`.

## Repo layout

```
KERNEL.md              # canon policy — no story facts, ever
HOW-TO.md              # start a new book from templates
VOICE-TELLS.md         # prose that doesn't read as generated (kit-level)
STATUS.md              # kit status: what's portable, what's still pilot-shaped
templates/             # P-HEAD, A-GUARDRAILS, D-ERA, B-CHARACTER(-ERA),
                       # E-SCENE, F-LEDGER, G-OPEN-QUESTIONS, VOICE, VOICE-FID
prompts/               # architect / drafter / auditor system prompts + research
scripts/check_ids.py   # heuristic: draft names not present in bible IDs
scripts/voice_check.py # heuristic: machine-prose tells in a scene
books/<slug>/
  bible/               # locked canon for this book
  manuscript/          # prose, only after a scene ID exists
  STATUS.md            # where this book actually is
  audit/               # auditor output
```

Pilot book: `books/the-watch/` (time-travel middle-grade/YA, father-son).

## The three things that get violated most

1. **Plausible ≠ canon.** Default modern life, default history, default family structure, default tech are `[UNKNOWN]` until the author locks them. Do not fill.
2. **Contradictions stop work.** If two locked files disagree, do not pick a winner. Write both IDs into that book's `G-OPEN-QUESTIONS.md` and stop.
3. **Era-locked diction.** Speech, naming, and tech follow the era deck of the *scene year*, not the narrator year. Recollection scenes split Then-state and Now-state; Now-words stay out of Then-dialogue.

Tag every assertion: `[USER-CANON]` / `[DERIVED]` (state the derivation) / `[OPTION]` (not locked) / `[UNKNOWN]` (ask, don't fill).

## Start a new book

Full steps in [`HOW-TO.md`](HOW-TO.md). The short version:

1. `books/<slug>/bible/`, copy every template into it
2. Fill `P-HEAD` before any prose exists
3. Lock one era deck, then one character invariant + era slice
4. Snowflake 1–2 from locked facts only
5. Fill `VOICE` + `VOICE-FID` **in that book's diction** — never copy The Watch's FID lines

## Working modes

Pick one and say which you're in. System prompts are in `prompts/`:

- **Architect** (`architect.system.md`) — creates and locks modules, one per reply. Never writes chapter prose.
- **Drafter** (`drafter.system.md`) — prose for one scene ID at a time.
- **Auditor** (`auditor.system.md`) — checks drafts and beats against locked canon.

## Output shape (every reply)

1. Mode + Snowflake step
2. Locked vs open
3. One artifact
4. Contradiction log, or "none"
5. Next legal action — one sentence

## Checks

```bash
python3 scripts/check_ids.py books/<slug>
```

Heuristic only: flags Title Case names in `manuscript/` that don't appear in `bible/`. A clean run is not proof of canon compliance; the auditor pass is.

```bash
python3 scripts/voice_check.py books/<slug>/manuscript/*.md --summary
```

Flags machine-prose tells — verbless fragment runs, dropped determiners, beats landing on a portable moral, antithesis tics, sentence-length flatness. Reading aid, never a gate; it has no calibrated targets for this kit yet. The tells, and the structural one the checker cannot see, are in [`VOICE-TELLS.md`](VOICE-TELLS.md).

## Done definition

A module is done when it is locked by the author, contradicts nothing in `bible/`, carries no `[UNKNOWN]` the next step depends on, and the book's `STATUS.md` reflects where the work actually stands.
