#!/usr/bin/env python3
"""Fail if a draft uses Title Case names that are not in bible IDs. Heuristic only."""
import re, sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
bible = ""
for p in (root / "bible").rglob("*"):
    if p.is_file():
        bible += p.read_text(encoding="utf-8", errors="ignore") + "\n"

locked = set(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", bible))
locked |= set(re.findall(r"display_names:\s*(.+)", bible))

drafts = list((root / "manuscript").rglob("*.md")) if (root / "manuscript").exists() else []
unknown = []
for d in drafts:
    text = d.read_text(encoding="utf-8", errors="ignore")
    names = set(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b", text))
    for n in sorted(names):
        if n not in bible and n not in {"Chapter Title"}:
            unknown.append((d.name, n))

if unknown:
    print("Possible unnamed entities:")
    for fn, n in unknown:
        print(f"  {fn}: {n}")
    sys.exit(1)
print("No extra Title-Case names found (heuristic).")
