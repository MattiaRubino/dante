# LifeOS — Frontend Architecture Handoff — 2026-08-18

**Status:** operational handoff / current Phase 4 continuation checkpoint  
**Branch:** `prototype/phase-4-today-home`  
**Supersedes for continuation:** `docs/phase-4/frontend-architecture-handoff-2026-08-17.md`  
**Current approved working artifact:** `docs/phase-4/home-vnext-orientation-day-ribbon-v1.md`

---

## 1. Current saved state

The current continuation reference is **Home vNext Orientation + Day Ribbon v1**, using the corrected exact HTML supplied by the user on 2026-08-18.

Exact artifact:

`lifeos_home_vnext_orientation_day_ribbon_v1.html`

Archive:

`prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/`

Identity:

```text
size          748625 bytes
SHA-256       986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob SHA  fd9788212fbbd1ee40e53271cc39cedd9275b341
```

The first uploaded variant was replaced by the user on commit `cb58b1528292398ccedeaedb60b44a4ff6e6235f`. The corrective delta changes exactly the `drRoadGrad` definition to use `gradientUnits:'userSpaceOnUse'` and percentage x coordinates. The corrected blob above is authoritative.

Do not continue from a rejected/intermediate conversation preview or reconstruct this state by hand.

---

## 2. Source precedence for the next frontend iteration

Read in this order for Phase 4 work:

1. current `main` Product/North Star and accepted Domain/Logical/architecture semantics where relevant;
2. `docs/workstreams/today-home.md`;
3. `docs/phase-4/home-vnext-orientation-day-ribbon-v1.md`;
4. exact archived checkpoint HTML;
5. `docs/phase-4/interaction-architecture-decisions-v0.md`;
6. `docs/phase-4/frontend-architecture-requirements-v0.md`;
7. `docs/phase-4/cross-platform-interaction-rule-v0.md`;
8. `docs/phase-4/interaction-architecture-guide-v0.md` as research/rationale, not as an automatic accepted-decision log;
9. `docs/phase-4/frontend-master.md`, `docs/phase-4/today-v21.md` and regression tests for mature timeline guarantees;
10. older checkpoints only as historical/regression references.

Repository truth outranks conversation memory where they disagree.

---

## 3. Product/research direction to preserve

The next design decisions should continue from the established evidence rather than from generic dashboard conventions.

Core direction:

```text
one structured personal reality
+ stable interaction semantics
+ multiple projections
+ adaptive/contextual presentation
+ natural language over the same reality
+ first-class GUI control
```

Important constraints:

- LifeOS is not a calendar, task manager, dashboard, database browser or chatbot with widgets;
- time is foundational but not the container of life;
- current situation may include more than scheduled blocks;
- the system may know more than it exposes;
- persistent UI should serve recurring user needs, not mirror internal entity types;
- generated/adaptive UI remains inside a controlled grammar;
- AI recommendation/attention does not imply action authority;
- meaningful state changes become inspectable structured LifeOS reality rather than transcript-only state;
- simple users must not pay continuously for expert complexity;
- Mobile/Web may differ in representation while preserving semantic behavior;
- prototype vocabulary does not automatically become accepted product/domain vocabulary.

---

## 4. Current visual/product posture

The accepted artifact should feel like a sellable personal system rather than an accumulated prototype control panel.

When modifying it:

- preserve accepted geometry outside the requested scope;
- avoid adding standalone controls without a clear hierarchy/placement rationale;
- prefer progressive disclosure over permanent secondary chrome;
- avoid heavy enterprise cockpit composition;
- avoid toy/gamified visual treatment as the default product language;
- maintain professional clarity with restrained personal warmth;
- do not revive rejected Home wing expansion unless explicitly requested;
- keep timeline controls and group geometry synchronized rather than positioned independently by eye.

The exact archived HTML wins over prose if there is uncertainty about current visual state.

---

## 5. Timeline protection

The integrated artifact currently carries the mature timeline lineage, including 24-hour labels, group controls, event cards and anchored time editing.

`Today v21` remains historical/regression authority for that timeline behavior; it is not a second current Home surface name.

Do not remove/simplify mature behavior merely to solve a visual Home problem.

The complete `today-v21-regression.py` suite was **not run as part of this checkpoint save or the corrective replacement**; do not manufacture that PASS.

---

## 6. QA state

Corrected artifact static QA:

```text
size                                      748625 bytes
SHA-256                                   986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob SHA                              fd9788212fbbd1ee40e53271cc39cedd9275b341
duplicate DOM IDs                         0
CSS parse errors                          0
inline JS syntax failures                 0
exact reconstruction → remote blob        PASS
```

Important qualification: the integrated Chromium smoke recorded immediately before the corrective replacement belongs to the previous blob and has **not** been relabelled as a fresh run on the corrected blob. The correction is a single `drRoadGrad` source-line change; current corrected evidence is exact byte reconstruction plus static validation.

See `prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/qa-static.json` for the exact record.

---

## 7. Immediate continuation

**Await the user's next explicit direction.**

Do not independently resume an older planned task merely because it appeared in a previous handoff.

The safe next iteration is:

```text
open exact corrected archived checkpoint
→ receive explicit scope
→ preserve out-of-scope accepted regions
→ implement/test
→ user visual review
→ checkpoint accepted result
```

Normal Git writes continue to require the exact LifeOS PRE-SCOPE/write gate and post-write path QA.
