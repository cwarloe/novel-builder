@AGENTS.md

## Claude-specific notes

`AGENTS.md` above is the shared playbook every coding agent reads; it is the source of truth. Keep Claude-only instructions below this line so the two don't drift.

- This repo's constraints are about **restraint**, not throughput. Producing more locked canon than the author asked for is a failure, not progress. When a fact is missing, the correct output is `[UNKNOWN]` and a question — not a well-reasoned guess.
- Do not open a PR that adds story facts to `books/<slug>/bible/` unless the author stated them in the request. Kit changes (`KERNEL.md`, `templates/`, `prompts/`, `scripts/`) and mechanical fixes are fair game.
- Before changing anything in `templates/` or `KERNEL.md`, test the change against `books/the-watch/` **and** against a second, unrelated novel you imagine starting from `HOW-TO.md`. If it only holds for The Watch, it's a book rule and belongs in that book's `bible/`.
- Cite file + ID when you report a contradiction. "Two files disagree" without both IDs is not usable.
