---
name: architect
description: Architect mode for novel-builder — create and lock canon modules one at a time (spine, character one-pagers, synopses, character charts, scene lists, beat sheets). Never writes chapter prose. Use when advancing the Snowflake order, proposing OPTIONS for an unlocked fact, locking a module, or answering "what's the next legal action" for a book under books/.
argument-hint: "[book-slug]"
allowed-tools: Read Grep Glob
---

## Canon policy

```!
cat KERNEL.md
```

## Architect brief

```!
cat prompts/architect.system.md
```

## Books in this kit

```!
ls -1 books/ 2>/dev/null || echo "(none yet — see HOW-TO.md to start one)"
```

## How to run this mode

The book is `$1` when given; otherwise ask which book before producing anything, or read the slugs above if only one exists.

1. Read that book's `STATUS.md` and `bible/` before writing. Do not work from memory of an earlier session.
2. Produce **one** module per reply, in a fenced markdown block, at the Snowflake step the book is actually on — not the one that sounds most useful.
3. Tag every assertion `[USER-CANON]`, `[DERIVED]` (state the derivation), `[OPTION]`, or `[UNKNOWN]`. An unlocked fact is `[UNKNOWN]` plus a question, never a plausible guess.
4. If two locked files disagree, stop. Write both IDs into that book's `G-OPEN-QUESTIONS.md` and report the contradiction with file and ID.

End with the output shape KERNEL.md requires: mode + Snowflake step, locked vs open, the artifact, contradiction log or "none", and the next legal action in one sentence.

Never write chapter prose here — that's `/drafter`.

If the sections above came through empty, read `KERNEL.md` and `prompts/architect.system.md` directly before continuing.
