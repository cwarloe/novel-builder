# NARRATIVE-CORE — shared contract

**Status:** draft contract, v0.1. Shared verbatim between `novel-builder` and `learning-narrative-kit`.
Neither repo fully conforms yet. See [Conformance](#conformance) for the current deltas.

This file is the **product contract**. The two repos are testbeds for it. Where a repo's
current behavior disagrees with this spec, the spec is the target and the repo is the
thing that moves — but nothing here licenses churning a live manuscript or a shipped
unit before the abstraction has earned it.

---

## 1. What this is

Both repos build the same thing: **prose that is accountable to a fact bank.**

A novel bible and a course glossary are the same object — a set of ID'd facts with
provenance. A scene and a training narrative are the same object — prose that references
those facts and may not exceed them. "Reliable narrative" means the prose can be
mechanically proven not to have invented anything.

The domain vocabulary differs. The machine does not.

| Machine part | novel-builder calls it | learning-narrative-kit calls it |
|---|---|---|
| The bank | `bible/` — `B-MARK`, `D-ERA-1993`, `O-WATCH` | `glossary.yaml` — `ssh`, `telnet`, `port` |
| Provenance | `[USER-CANON]` `[DERIVED]` `[OPTION]` `[UNKNOWN]` | `sources:`, `refs:`, `tier:` |
| The mark | *(none — plain names in prose)* | `[[term_id\|surface text]]` |
| Validity window | era decks, `eras_present:` | *(none)* |
| Knower's horizon | `WHEN-FOR-THIS-MIND` | *(none — stated in `constraints:` prose)* |
| Contradiction ledger | `G-OPEN-QUESTIONS.md` | *(none)* |
| Stage ladder | Snowflake 1–10 | README "generation order" 1–6 |
| Validator | `scripts/check_ids.py` (heuristic) | `tools/validate_unit.py` (exact) |
| Renderer | *(none)* | `tools/render_unit.py` → `docs/` |

The two repos are strong in complementary places. novel-builder has the reliability
discipline and no mechanism; learning-narrative-kit has the mechanism and no discipline.

---

## 2. Primitives

### 2.1 Entity

The atom of the bank. Every fact the prose is allowed to use is an entity.

```yaml
- id: string             # stable; NEVER renamed once status is `locked`
  kind: string           # profile-defined (see §4)
  status: locked | option | unknown
  source:                # required when status: locked
    kind: author | document | derived
    ref: string          # who said so, or the derivation
  window:                # optional; see §2.3
    axis: year | sequence
    from: <point>
    to: <point>          # omit for open-ended
  # ...arbitrary domain fields below this line
```

**`status` is the provenance gate.** It is novel-builder's tag system made machine-readable:

| KERNEL tag | spec |
|---|---|
| `[USER-CANON]` | `status: locked`, `source.kind: author` |
| `[DERIVED]` | `status: locked`, `source.kind: derived`, `ref` states the derivation |
| `[OPTION]` | `status: option` |
| `[UNKNOWN]` | `status: unknown` |

`unknown` entities exist so the bank can hold a *named hole*. That is the point of
KERNEL's "plausible ≠ canon" law: the absence of a fact is itself a fact, and it must be
addressable by ID so prose can be refused for depending on it.

### 2.2 Mark

Prose references the bank by ID, explicitly:

```
[[ssh|SSH]]              →  entity `ssh`, rendered as "SSH"
[[B-MARK|Mark]]          →  entity `B-MARK`, rendered as "Mark"
```

- The id **must** resolve to a bank entity. This is what makes grounding provable.
- Surface text is prose and may differ freely from the entity's display name.
- **Mark policy** — profiles set how often. Marking every occurrence of a protagonist's
  name would be unreadable, so the default is **first reference per section** (per scene
  in fiction, per `##` section in learning); later occurrences may be marked or not.
- Marks render as a **tint, not a link**. The reader keeps full sentence context without
  hovering. Hover is optional lookup, never a required click path.

Marks are the fix for `check_ids.py`. A regex over Title-Case words is a guess; a mark is
a proof. Adopting the syntax in drafts turns novel-builder's weakest check into its
strongest.

### 2.3 Window — validity across an axis

An entity may only be referenced within a window on a declared axis.

```yaml
# fiction: the pager exists 1986–1994
window: {axis: year, from: 1986, to: 1994}

# learning: TLS may not appear before unit 3
window: {axis: sequence, from: unit-03}
```

**This is one check with two names.** novel-builder's *era bleed* (§8–11 of the auditor)
and learning-narrative-kit's unwritten *prerequisite order* are the same rule: an entity
carries a validity window, and prose may not reference it outside that window. In fiction
the axis is a calendar year; in training it is a position in the curriculum.

### 2.4 Position — where a piece of prose sits

Every prose file declares two points on the axis:

```yaml
position:
  at:       {axis: year, value: 1993}    # WHEN — the calendar
  known_to: {axis: year, value: 1987}    # WHEN-FOR-THIS-MIND — what this mind can name
```

`at` is where the prose happens. `known_to` is the horizon of the mind carrying it —
the POV character in fiction, **the learner in training**.

They usually match. When they don't, that gap is the thing both projects care most about:

- Fiction: a 1993 scene narrated by a mind that only has 1987 words. Now-words stay out of
  Then-dialogue.
- Training: a unit-05 narrative whose reader has only completed unit-03. The narrator may
  be lost; **the reader must never be confused by an unexplained reference.**

That last line is already a Portland Desk constraint, written in prose and enforced by
nobody. `known_to` is how it becomes mechanical.

### 2.5 Open question — the contradiction ledger

```yaml
- id: Q-001
  question: string
  blocks: [E-S01, stage:draft]      # targets that may not proceed
  conflict: [D-ERA-1993, F-0007]    # entity ids that disagree, when applicable
  options: [string]
  status: open | decided
  decision: string                  # required when status: decided
```

This is `G-OPEN-QUESTIONS.md` made enforceable. KERNEL's contradiction rule — *if two
locked files disagree, stop; do not pick a winner* — is only a rule if something refuses
to move. `blocks:` is that refusal.

learning-narrative-kit has no equivalent today and needs one: two study sources that
disagree about a port number is exactly this case, and the current answer is a silent
authorial choice.

### 2.6 Stage

Each profile declares an ordered stage ladder. The project head records `stage_locked: N`.
Prose may not be generated below the drafting stage, and once at or above it, every marked
entity must be `locked`.

This is "no draft until the user names a scene ID and says DRAFT," generalized.

---

## 3. Checks

A conforming validator runs these against (bank, prose, questions, stage).

| # | Check | Rule | fiction | learning |
|---|---|---|---|---|
| 1 | **Grounding** | every mark resolves to a bank entity | fail | fail |
| 2 | **Coverage** | every bank entity is marked ≥1 | off | fail |
| 3 | **Status** | at stage ≥ draft, no mark resolves to `option`/`unknown` | fail | fail |
| 4 | **Window** | every mark's window contains `position.at` | fail | fail |
| 5 | **Epistemic** | every mark's window contains `position.known_to` | fail | fail |
| 6 | **Contradiction** | no `status: open` question `blocks` this target | fail | fail |
| — | Density | marks per 100 words | report | report (~2.0) |
| — | Cover test | strip marks; prose still carries meaning | human | human |

**Grounding is the reliability property. Coverage is the pedagogy property.** That is the
whole difference between the two profiles, and it is why coverage is off for fiction: a
bible legitimately holds facts the draft never surfaces. A glossary does not.

Checks 1–2 are what `validate_unit.py` already does exactly. Checks 3–6 are what
novel-builder does by discipline, prompt, and human audit. Neither repo does all six.

---

## 4. Profiles

```yaml
profile: fiction
  kinds: [character, era, place, object, scene, fact]
  axis: year
  coverage: off
  mark_policy: first-reference-per-scene
  stages: [spine-1, spine-5, char-1pager, synopsis, pov-synopsis,
           long-synopsis, char-charts, scene-list, beats, draft]

profile: learning
  kinds: [term, concept, procedure]
  axis: sequence
  coverage: required
  mark_policy: first-reference-per-section
  density_target: 2.0
  stages: [term-set, situation, narrative, glossary, qa, render]
```

Profiles carry domain vocabulary and gate settings only. They do not add checks.

Domain-specific fields stay domain-specific: `tier: exam|support`, `pov:`, `lie:`,
`body_tells_when_lying:` are all free-form entity fields the core never inspects.

---

## 5. Audit

The mechanical checks in §3 cover what is provable. The remaining checks in
`prompts/auditor.system.md` are judgment and stay with a reviewing agent. Of its twelve:

- **1, 5, 6** (unnamed entities, off-ledger inventory, timeline order) → mechanized by
  checks 1 and 3.
- **3, 8, 11** (era bleed, era-deck attribution, retired labels) → mechanized by check 4.
- **4, 7, 10** (epistemic leaks, Then/Now diction, WHEN vs WHEN-FOR-THIS-MIND) → partly
  mechanized by check 5; diction remains judgment.
- **2, 9, 12** (dead people acting, claim attribution, ledger vs scene step) → judgment.

The auditor's standing orders are profile-independent and should be stated once, here:
**propose options, never patch the bank, and on a contradiction between locked facts,
stop and file an open question rather than choosing.**

---

## 6. Conformance

Current state against this contract. Nothing below is scheduled work; it is the delta.

### novel-builder

| Part | State |
|---|---|
| Entity bank, stable IDs | ✅ `bible/`, disciplined ID scheme |
| Provenance | ⚠️ tags exist in KERNEL prose, not as machine-readable fields |
| Marks | ❌ none — prose uses plain names; `check_ids.py` guesses via Title-Case regex |
| Window | ⚠️ era decks exist as documents; no per-entity `window` field |
| Position | ⚠️ `when` / `when_for_this_mind` on `E-SCENE` — right idea, not machine-read |
| Open questions | ✅ `G-OPEN-QUESTIONS.md` — but `blocks:` is prose, gates nothing |
| Stages | ✅ Snowflake ladder, enforced by prompt discipline |
| Checks 1–6 | 1 heuristic; 2 N/A; 3–6 by human audit |
| Renderer | ❌ none |

Highest-value single change: **adopt `[[id|surface]]` in drafts.** It converts check 1
from a heuristic to a proof and makes 3–5 possible at all.

### learning-narrative-kit

| Part | State |
|---|---|
| Entity bank, stable IDs | ✅ `glossary.yaml` |
| Provenance | ⚠️ bank-level `source:` and per-term `refs:`; no per-term `status` — every term is implicitly locked, and there is no way to mark one unverified |
| Marks | ✅ `[[id\|surface]]`, exactly as specified |
| Window | ❌ none — no prerequisite-order check |
| Position | ❌ none — reader horizon stated in `constraints:` prose, enforced by nobody |
| Open questions | ❌ none — conflicting sources resolved silently |
| Stages | ⚠️ generation order in README; nothing enforces it |
| Checks 1–6 | 1 ✅, 2 ✅, 3–6 ❌ |
| Renderer | ✅ `render_unit.py` → Pages |

Highest-value single change: **per-term `status` + an open-questions file.** Today a
glossary cannot say "unverified," which is the same gap KERNEL's *plausible ≠ canon* law
exists to close.

---

## 7. Open questions about this spec

Filed here rather than decided, per §2.5.

| id | question |
|---|---|
| S-001 | Is `known_to` (check 5) a hard fail in the learning profile, or a warning? A term used one unit early may be a deliberate teaching move. |
| S-002 | Does fiction need coverage at all, in a weaker form — e.g. warn on locked entities never referenced by any beat, as a dead-canon detector? |
| S-003 | Should `window.axis: sequence` points be unit ids (`unit-03`) or integers? Ids are readable; integers compare without a lookup table. |
| S-004 | Marks in fiction drafts: does first-reference-per-scene survive contact with real prose, or does it fight the line? Untested. |
| S-005 | Where does `tier: exam|support` live — a free-form entity field, or a core concept? It is doing real filtering work in the renderer. |
