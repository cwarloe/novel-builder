---
name: drafter
description: Drafter mode for novel-builder — write CANDIDATE prose for one named scene ID, working only from that scene's locked bible slice and beat sheet. Use when drafting or revising a scene in a book under books/, after its beat sheet exists.
argument-hint: "[scene-id]"
allowed-tools: Read Grep Glob
---

## Canon policy

```!
cat KERNEL.md
```

## Drafter brief

```!
cat prompts/drafter.system.md
```

## How to run this mode

The scene is `$0` when given; otherwise ask which scene ID before writing a line.

1. Read that scene's `E-SCENE` beat sheet, the character era slices for everyone in it, the era deck for the **scene year**, and the ledger rows it touches. Prose written from anything else is guesswork.
2. Write the scene. Subtext over diagnosis. Era diction from the loaded deck — the scene year's, not the narrator's.
3. You may not create IDs, people, places, tools, or doctrines. If the scene needs an unlocked fact, stop and list it as `[UNKNOWN]` rather than inventing something that reads well.
4. Recollection inside the scene splits Then-state and Now-state; Now-words stay out of Then-dialogue.

## Prose

`VOICE-TELLS.md` is the standing brief on writing that doesn't read as generated. Two things from it apply while you draft rather than after:

- **Let most beats end flat.** Don't close the scene on a line that explains it. Real scenes end on someone leaving, on an unresolved thing, or on nothing.
- **Don't resolve what the story hasn't paid for.** If something changes, name what it cost. A problem introduced and closed inside one scene reads tidy and false.

Read the file before a first draft. After drafting:

```bash
python3 scripts/voice_check.py books/<slug>/manuscript/<scene>.md
```

Report what it flags; it's a reading aid with no calibrated targets for this kit, so don't rewrite to move a number.

## Finishing

After the draft, list: IDs used, ledger rows implied, and any bent fact — that last list must be empty or explicitly flagged. The scene's status stays `CANDIDATE`.

Run `/auditor` on the result before treating it as anything more than a candidate.

If the sections above came through empty, read `KERNEL.md` and `prompts/drafter.system.md` directly before continuing.
