# Voice — prose that doesn't read as generated

A scene can pass `/auditor`, contradict nothing in `bible/`, invent no IDs, and still fail:
it reads like a machine wrote it. Canon accountability and prose quality are separate
problems, and this kit only had machinery for the first one.

This file is the second. It is **kit-level** — it holds for any book started from
`HOW-TO.md`, not just The Watch.

## Where this came from

The tell list was developed in [`learning-narrative-kit`](https://github.com/cwarloe/learning-narrative-kit)
(`schema/VOICE.md`), where two chapters by the same author — one written before a house
style set in, one after — gave a control group and a measurable drift. The method
transfers. The numbers do not: those targets are for 2,000-word training narratives, and
a novel legitimately runs longer sentences, different rhythm, different dash rate.

The two repos are separate projects and stay separate. What's shared is the research, not
a contract.

## The thresholds here are not calibrated yet

`scripts/voice_check.py` reports measurements. This kit has **no target numbers**, because
The Watch's manuscript is one 280-word candidate scene and statistics on 280 words are
noise.

So: read the numbers as description, not as a verdict. Once there are five or six scenes
you're happy with, measure them and write the ranges into this file — your own control
group, the way the other kit built its.

```bash
python3 scripts/voice_check.py books/<slug>/manuscript/*.md --summary
```

## Sentence-level tells

These come straight across from the source kit; they are about prose, not form.

1. **Dropped determiners.** A subject noun loses its article and the sentence takes on a
   telegraphic register. *Rain hits the windows* → *The rain hits the windows.* English is
   not an article-free language; prose that drops them reads as translated.
2. **Verbless fragments in runs.** One is a choice. Four in a row is a drumbeat. Give them
   verbs or cut them.
3. **Every beat landing on a portable moral.** The most damaging and least noticed. Real
   scenes end on someone leaving, or on an unresolved thing, or on nothing. **Let most
   beats end flat.** A beat that ends on "she said she'd think about it" has not failed.
4. **The "X is not Y" formula.** Antithesis as a tic. One is a line; five is a house style.
5. **Characters who speak only in epigrams.** A line is quotable because the narrator marks
   it as memorable. If every line is quotable, none is. Real people mostly say boring
   operational things. Let a character be wrong once, or distracted, or genuinely not know.
6. **Trying too hard.** *Rain hits the windows like it has opinions.* The
   inanimate-object-with-attitude simile is a signature of generated prose. When a simile
   reaches, cut it — plain statement is nearly always better.
7. **Character sheets read aloud.** Stacked appositives delivering biography. Nobody
   narrates themselves that way. Let facts arrive when they matter.
8. **Em-dashes as a default connector.** The dash earns its place as interruption, as an
   appositive already containing commas, or as a turn the sentence didn't promise. It does
   not earn its place as a general connector, and especially not as the hitch that
   delivers a summarizing clause — that construction is how tell 3 gets delivered. Cut the
   clause, not just the dash.

## The structural tell

Neither kit had this one. It is the failure most specific to long-form, and the checker
cannot see it — it lives above the sentence.

**Resolution the story hasn't paid for.** A scene, a chapter, or a book that wraps up
quickly and neatly, in the shape of a fairy tale: the conflict lands, the lesson registers,
someone says the thing that makes it mean something, and the problem is closed. It reads
tidy and it reads false, because the cost was never charged.

What it looks like:

- A problem introduced in a scene is resolved inside the same scene.
- A character changes their mind because someone explained something well.
- The antagonist relents, or turns out to have been reasonable all along, on no pressure.
- Nobody loses anything they cared about.
- The last line tells you how to feel about what just happened.
- A hard thing is survived and nothing afterwards is different.

What to do instead:

- **Charge for it.** If the change is real, something has to be spent — a relationship, a
  belief, a possibility that's now closed. Name what it cost.
- **Let it stay open.** Most scenes should end with the problem still running. A scene
  that resolves is a spent card; you don't have many.
- **Split the beat.** If something must resolve, put the cost in one scene and the
  resolution several scenes later, so the reader carries it in between.
- **Cut the last line.** When a scene ends on a line that explains the scene, delete it and
  read again. The scene almost always ends better one line earlier.

For a middle-grade or YA book this tell is a live risk, because the form invites tidiness
and the audience is assumed to want it. They don't. A twelve-year-old reader knows when a
thing has been made easy.

## What not to trade away

Voice repair must not cost canon. Everything in `KERNEL.md` still binds: a scene that reads
beautifully and invents a fact is worse than one that reads flat and doesn't. If a repair
needs a fact that isn't locked, that's `[UNKNOWN]` and a question, same as anywhere else.

And the checker is a reading aid. It produces false positives by design — short sentences in
a tense scene are a craft choice, not a tell. Never treat a number from it as a gate.
