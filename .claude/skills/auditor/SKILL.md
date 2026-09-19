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

If the brief above came through empty, read `prompts/auditor.system.md` directly before continuing.
