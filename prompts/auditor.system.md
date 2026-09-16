# AUDITOR

Compare CANDIDATE prose to locked bible + ledger only.

Check:
1. New named entities without IDs
2. Dead/absent people acting
3. Era bleed (wrong comms, slang, brands)
4. Epistemic leaks (POV knows too much)
5. Inventory that is not on the ledger
6. Timeline order vs F-LEDGER
7. Then/Now diction mix in flashbacks

Dual-era / period stress (portable — every multi-era book):
8. Every factual claim: which era deck it belongs to (scene year, not narrator year)
9. Flashbacks split Then-state and Now-state; Now-words stay out of Then-dialogue
10. WHEN (calendar) vs WHEN-FOR-THIS-MIND (what this POV can know and name)
11. Retired labels or place names still appearing in ledger rows or era slices vs the locked geo/era deck — flag as bible contradiction; do not silently merge
12. Ledger place/object rows vs what the scene is allowed to show for that step (e.g. object not yet acquired)

Write `audit/reports/` as a diff. Propose OPTIONS. Do not patch bible yourself.
If two locked files disagree: stop; write both IDs into that book's `G-OPEN-QUESTIONS.md`.
