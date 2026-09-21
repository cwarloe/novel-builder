---
name: auditor
description: Auditor mode for novel-builder — check CANDIDATE prose (or a CANDIDATE beat, for draft-readiness) against the locked bible and ledger, writing a diff report to audit/reports/. Use when verifying a scene for era bleed, epistemic leaks, unlisted inventory, timeline order, or entities without IDs.
argument-hint: "[scene-id]"
allowed-tools: Read Grep Glob Bash(python3 scripts/check_ids.py *)
---

## Auditor brief

```!
cat prompts/auditor.system.md
```

## How to run this mode

The scene is `$1` when given; otherwise ask which scene, or audit the book's current CANDIDATE.

1. Work the numbered checklist above in order. Every finding cites **file plus ID** — "two files disagree" without both IDs is not a usable report.
2. Run the mechanical pass alongside your reading:
   ```bash
   python3 scripts/check_ids.py books/<slug>
   ```
   It flags Title Case names in `manuscript/` that don't appear in `bible/`. A clean run proves nothing on its own; it's a net for one specific mistake, not a canon check.
3. Write the report to that book's `audit/reports/` as a diff. If you audited a beat rather than prose, note `kind: beat-readiness`.
4. Propose OPTIONS. **Do not patch the bible yourself** — the author locks canon, not you.
5. If two locked files disagree, stop and write both IDs into that book's `G-OPEN-QUESTIONS.md`.

## Prose pass

Canon compliance and prose quality are separate failures, and a scene can pass every check above and still read as generated. When auditing prose rather than a beat, add a second section to the report covering `VOICE-TELLS.md`:

```bash
python3 scripts/voice_check.py books/<slug>/manuscript/<scene>.md
```

Report its numbers as description — this kit has no calibrated targets, and short sentences in a tense scene are a craft choice, not a tell. Then judge the two things the checker cannot see:

- **Does any beat land on a portable moral?** Quote the line. Most beats should end flat.
- **Does the scene resolve something the story hasn't paid for?** A problem opened and closed in one scene, a mind changed by a good explanation, an antagonist relenting under no pressure. Name what it would have cost if it were real.

Keep this separate from the canon findings. A prose note is never a reason to hold a scene that is canon-clean, and never a reason to pass one that isn't.

If the brief above came through empty, read `prompts/auditor.system.md` directly before continuing.
