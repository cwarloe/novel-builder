---
name: canon-check
description: Run novel-builder's mechanical ID check over a book — flags Title Case names in manuscript/ that don't appear in bible/. Use for a quick pass on a draft before a full audit, or when checking whether a scene introduced an unlocked name.
argument-hint: "[book-slug]"
allowed-tools: Bash(python3 scripts/check_ids.py *) Read Grep
---

## Books in this kit

```!
ls -1 books/ 2>/dev/null || echo "(none yet)"
```

## Run it

The book is `$1` when given; otherwise pick from the list above, asking if more than one could be meant.

```bash
python3 scripts/check_ids.py books/<slug>
```

## Reading the result

This is a **heuristic, not a canon check.** It matches Title Case word pairs, so it will:

- miss a single-word name, a lowercase one, and any era or inventory violation
- flag ordinary prose that happens to start a sentence with a proper noun

So treat a hit as a question, not a verdict. For each one, say whether it's a real unlocked entity or a false positive, citing the bible file you checked. A clean run means only that this one net caught nothing — it is not evidence the scene is canon-compliant. That's `/auditor`.

If it reports unlocked names that are genuinely new, they are `[UNKNOWN]` for the author to lock. Do not add them to `bible/` yourself.
