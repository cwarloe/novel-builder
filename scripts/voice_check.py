#!/usr/bin/env python3
"""Flag machine-prose tells in a scene. Heuristic — a reading aid, never a gate.

Ported from learning-narrative-kit, where the same tells were measured against a
control chapter. The detectors are form-agnostic; the thresholds are not, and this
kit has no calibrated targets yet. See VOICE-TELLS.md.

Usage:
  python3 scripts/voice_check.py books/<slug>/manuscript/E-S01.CANDIDATE.md
  python3 scripts/voice_check.py books/<slug>/manuscript/*.md --summary

Detects the patterns that make generated prose legible as generated:
  1. verbless fragments (noun-phrase drumbeat)
  2. runs of consecutive fragments
  3. determiner-dropped subjects ("Rain hits..." for "The rain hits...")
  4. section-final aphorisms (every beat landing on a portable moral)
  5. antithesis tics ("not X, Y" / "X is not Y, it is Z")
  6. tricolon (three-beat lists and three-short-sentence runs)
  7. sentence-length flatness (low variance = drumbeat)
  8. repeated sentence openings
"""

from __future__ import annotations

import argparse
import re
import statistics
import sys
from pathlib import Path

# Finite-verb detection: a sentence with none of these is probably verbless.
AUX = {
    "is","are","was","were","be","been","being","am","'s","'re","'m",
    "has","have","had","do","does","did","can","could","will","would",
    "shall","should","may","might","must","ain't","isn't","aren't","wasn't",
    "weren't","hasn't","haven't","hadn't","doesn't","don't","didn't","won't",
    "wouldn't","can't","couldn't","shouldn't","let","lets",
}
VERB_SUFFIX = re.compile(r"(?:s|es|ed|ing)$")

FUNCTION_STARTS = {
    "the","a","an","i","he","she","it","they","we","you","this","that","these",
    "those","there","here","my","his","her","their","our","your","its","and",
    "but","or","so","then","when","if","while","after","before","because","as",
    "at","in","on","by","for","from","with","to","of","not","no","every","each",
    "some","any","one","two","three","most","more","less","all","both","what",
    "who","how","why","where","which","now","later","still","just","even","only",
    "nobody","nothing","someone","somebody","everyone","anyone","half","another",
}

ABSTRACT_HINT = re.compile(
    r"\b(point|job|thing|way|answer|question|problem|rule|truth|difference|"
    r"decision|decisions|choice|habit|trust|risk|cost|work|lesson)\b", re.I)


def clean(text: str) -> str:
    # Scene front matter is metadata, not prose: drop "key: value" lines.
    text = re.sub(r"^[a-z_]+:.*$", "", text, flags=re.M)
    text = re.sub(r"^#+ .*$", "", text, flags=re.M)      # headings
    text = re.sub(r"^\s*\*.*\*\s*$", "", text, flags=re.M)  # italic standalone lines
    text = re.sub(r"[*_`]", "", text)
    return text


def sections(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    out = []
    if parts[0].strip():
        out.append(("(opening)", parts[0]))
    for i in range(1, len(parts), 2):
        out.append((parts[i].strip(), parts[i + 1]))
    return out


def split_sentences(block: str) -> list[str]:
    block = clean(block)
    block = re.sub(r"\s+", " ", block)
    raw = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'“])", block)
    return [s.strip() for s in raw if s.strip() and len(s.strip()) > 1]


def words(s: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", s)


def has_finite_verb(s: str) -> bool:
    ws = [w.lower() for w in words(s)]
    if any(w in AUX for w in ws):
        return True
    # crude: any non-initial token with a verb-ish suffix that isn't a known plural noun
    return any(VERB_SUFFIX.search(w) and len(w) > 3 for w in ws[1:])


def build_proper_nouns(text: str) -> set[str]:
    """Words capitalized mid-sentence are probably proper nouns."""
    out: set[str] = set()
    for m in re.finditer(r"(?<![.!?\"']\s)(?<!^)\b([A-Z][a-z]{2,})\b", text, flags=re.M):
        out.add(m.group(1).lower())
    return out


def analyze(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    body = clean(text)
    proper = build_proper_nouns(body)

    all_sents: list[str] = []
    findings: dict[str, list] = {k: [] for k in (
        "fragment", "fragment_run", "no_determiner", "aphorism",
        "antithesis", "tricolon", "repeat_open")}

    for name, block in sections(text):
        sents = split_sentences(block)
        if not sents:
            continue
        all_sents.extend(sents)

        run: list[str] = []
        for s in sents:
            w = words(s)
            if not w:
                continue
            frag = not has_finite_verb(s) and len(w) <= 12
            if frag:
                findings["fragment"].append((name, s))
                run.append(s)
            else:
                if len(run) >= 2:
                    findings["fragment_run"].append((name, " / ".join(run)))
                run = []

            first = w[0].lower()
            if (first not in FUNCTION_STARTS and first not in proper
                    and s[0].isupper() and len(w) > 2 and not frag):
                findings["no_determiner"].append((name, s))

            if re.search(r"\bis not\b.*[,.]|\bnot\b [^,.]{2,30}[.,] (?:it|that|the) ", s, re.I) \
               or re.match(r"^Not [a-z]", s):
                findings["antithesis"].append((name, s))

            if len(re.findall(r",", s)) >= 2 and len(w) <= 14:
                findings["tricolon"].append((name, s))
        if len(run) >= 2:
            findings["fragment_run"].append((name, " / ".join(run)))

        last = sents[-1]
        lw = words(last)
        if len(lw) <= 16 and (ABSTRACT_HINT.search(last)
                              or re.search(r"\b(is|are|was|not)\b", last, re.I)):
            findings["aphorism"].append((name, last))

    opens: dict[str, int] = {}
    for s in all_sents:
        w = words(s)
        if w:
            opens[w[0].lower()] = opens.get(w[0].lower(), 0) + 1
    findings["repeat_open"] = sorted(
        ((k, v) for k, v in opens.items() if v >= 8), key=lambda x: -x[1])

    lens = [len(words(s)) for s in all_sents if words(s)]
    return {
        "path": path,
        "sentences": len(all_sents),
        "mean_len": statistics.mean(lens) if lens else 0,
        "stdev_len": statistics.pstdev(lens) if len(lens) > 1 else 0,
        "pct_short": 100 * sum(1 for l in lens if l <= 6) / len(lens) if lens else 0,
        "em_dash_per_1k": 1000 * body.count("—") / max(len(words(body)), 1),
        "findings": findings,
    }


def report(r: dict, verbose: bool) -> None:
    f = r["findings"]
    print(f"\n=== {r['path'].stem} ===")
    print(f"sentences={r['sentences']}  mean={r['mean_len']:.1f}w  "
          f"sd={r['stdev_len']:.1f}  short(<=6w)={r['pct_short']:.0f}%  "
          f"em-dash/1k={r['em_dash_per_1k']:.1f}")
    print(f"fragments={len(f['fragment'])}  frag-runs={len(f['fragment_run'])}  "
          f"no-determiner={len(f['no_determiner'])}  aphorisms={len(f['aphorism'])}  "
          f"antithesis={len(f['antithesis'])}  tricolon={len(f['tricolon'])}")
    if f["repeat_open"]:
        print("  repeated openings: " +
              ", ".join(f"{k}x{v}" for k, v in f["repeat_open"][:6]))
    if not verbose:
        return
    for key, label in (("no_determiner", "DETERMINER-DROPPED SUBJECT"),
                       ("fragment_run", "FRAGMENT RUN"),
                       ("aphorism", "SECTION-FINAL APHORISM"),
                       ("antithesis", "ANTITHESIS")):
        if f[key]:
            print(f"\n  -- {label} --")
            for name, s in f[key][:12]:
                print(f"   [{name[:28]}] {s[:110]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Flag machine-prose tells (heuristic).")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--summary", action="store_true", help="counts only")
    args = ap.parse_args()
    for p in args.paths:
        if p.is_file():
            report(analyze(p), verbose=not args.summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
