# LifeOS — Home vNext Orientation + Day Ribbon v1

**Date:** 2026-08-18  
**Branch:** `prototype/phase-4-today-home`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT — current Phase 4 continuation artifact**  
**Supersedes for continuation:** `docs/phase-4/home-vnext-adesso-main-stage-v1.md`  
**Nature:** standalone HTML/CSS/JavaScript UX prototype; not production React/Next.js code and not final Information Architecture/product vocabulary

---

## 1. Purpose

This checkpoint freezes the exact user-supplied prototype accepted on 2026-08-18 and makes it the deterministic starting point for the next Phase 4 iteration.

Do not reconstruct this state approximately from screenshots, old conversation previews or earlier checkpoints. Open the exact archived HTML artifact.

Exact identity:

```text
filename
lifeos_home_vnext_orientation_day_ribbon_v1.html

size
748625 bytes

SHA-256
986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
```

Archive:

`prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/`

The exact HTML is stored directly as:

`prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/lifeos_home_vnext_orientation_day_ribbon_v1.html`

Current Git blob SHA: `fd9788212fbbd1ee40e53271cc39cedd9275b341`.

The initially checkpointed HTML was replaced by the user on commit `cb58b1528292398ccedeaedb60b44a4ff6e6235f` because the wrong local variant had been uploaded first. The corrective commit changes exactly one source line: `drRoadGrad` now uses `gradientUnits:'userSpaceOnUse'` with percentage x coordinates. The corrected blob above is the current exact source of truth.

---

## 2. Relationship to previous checkpoints

This checkpoint is later than:

- Home + Today Integrated v1;
- Home vNext Soft Surfaces v1;
- Home vNext Timeline Toolbar v8;
- Home vNext Adesso + Main Stage v1.

Those checkpoints remain valid historical/regression anchors. They are not the next working base unless an explicit rollback/comparison scope selects one.

The mature Today v21 contract remains the behavioral regression authority for the timeline engine where applicable:

- `docs/phase-4/frontend-master.md`;
- `docs/phase-4/today-v21.md`;
- `tests/prototypes/today-v21-regression.py`.

Saving this integrated checkpoint does not rewrite Today v21 history and does not claim that the complete Today v21 suite was rerun here.

---

## 3. What the current artifact visibly carries forward

The exact artifact is authoritative. At a high level it contains the current integrated direction, including:

- global Home shell and professional conversational AI surface;
- current-situation composition around `Ora` / immediate continuation, attention and contextual/dynamic information;
- carried-forward central stage with current prototype `Worlds` / `Stats` modes and their carousel/navigation behavior;
- current Home orientation strip and synchronized day context;
- dedicated day ribbon / week navigation;
- contextual `Ora` return-to-current-time control;
- calendar navigation;
- 24-hour timeline;
- nonlinear temporal density and overlap handling;
- group chips, filters/reordering and grouped timeline expansion;
- timeline panel expansion;
- event focus/subtasks;
- drag/move behavior and Undo lineage;
- zoom and manual time editing with anchored picker;
- existing environmental/path context;
- current side/secondary surfaces present in the supplied artifact.

This is an index only. It is not permission to reimplement the artifact approximately.

---

## 4. Architecture and research constraints that continue to govern design

The checkpoint is evaluated inside the already-documented Phase 4 research direction rather than becoming architecture by screenshot.

Current durable/working constraints include:

### One reality, multiple projections

Home, temporal views, contextual surfaces, natural language and future Mobile/Web representations operate on the same underlying LifeOS reality. Presentation state is not a competing source of truth.

### Time is primary, not sovereign

The timeline is a powerful operational projection, but LifeOS is not reducible to calendar blocks. Persistent realities may matter without being scheduled.

### Current situation is broader than the timeline

What the user needs to understand now may include current/next temporal reality plus meaningful changes, constraints, risks, mismatches, opportunities or unresolved matters.

### Stable semantics + adaptive presentation

Context may change relevance, density, ordering and composition, but it must not continually reinvent fundamental interaction meaning. Adaptive/generated UI uses a controlled grammar.

### GUI remains first-class

AI/natural language can interrogate and modify LifeOS, but frequent, state-oriented and precision-sensitive operations retain structured GUI paths. Essential control does not depend exclusively on prompting.

### User authority remains visible

Attention, recommendation and action authority are distinct. High relevance or AI confidence does not silently grant permission to act.

### Progressive disclosure without an infinite dashboard

LifeOS may know and reason over much more than Home exposes. Do not add permanent widgets merely because data/functionality exists. Complexity appears when it creates value.

### Do not expose ontology by convenience

Internal Domain Model concepts do not automatically become top-level navigation, permanent panels or final product nouns.

---

## 5. Prototype vocabulary qualification

The exact UI contains working/prototype labels. Their presence does not canonize them.

In particular:

- `Worlds` is not accepted as a Domain primitive or final product noun;
- `Stats` describes a prototype surface, not a finalized IA destination;
- `Per te` / contextual copy is presentation vocabulary subject to later product/brand review;
- current visual composition is evidence and approved prototype work, not by itself a final Information Architecture decision.

Future terminology changes require deliberate scope; do not silently rename the current checkpoint while editing unrelated behavior.

---

## 6. Visual/product guardrails

Continue to preserve the direction already established through research and interactive review:

- professional rather than toy-like;
- warm/personal without infantilization;
- capable without enterprise/cockpit heaviness;
- no decorative button accumulation;
- no equal-weight dashboard grid for every available concept;
- no obvious AI supremacy over user control;
- restraint in panel chrome, dividers and decorative effects;
- hierarchy should come from relevance, scale, spacing, typography and controlled accent before adding more containers;
- avoid modifying accepted regions while solving a local problem elsewhere;
- no new Home wing expansion or other large structural behavior unless explicitly requested in a later scope.

The exact artifact remains the visual reference when these prose guardrails are ambiguous.

---

## 7. QA recorded for the corrected checkpoint source

Exact source/static validation on the corrected artifact:

```text
size                         748625 bytes
SHA-256                      986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob SHA                 fd9788212fbbd1ee40e53271cc39cedd9275b341
DOM IDs                      67
duplicate DOM IDs            0
style blocks                 37
CSS parse errors             0
inline scripts               20
inline JS syntax failures    0
Git blob reconstruction      PASS
```

The integrated Chromium smoke previously recorded for this checkpoint lineage was executed before the corrective one-line HTML replacement. It must **not** be represented as having been rerun on the corrected blob. The corrected source passed exact byte reconstruction and static validation; a fresh browser regression remains separate evidence if/when required by the next functional or visual iteration.

The complete `today-v21-regression.py` suite was also **NOT RUN** as part of this corrective replacement.

Detailed record: `prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/qa-static.json`.

---

## 8. Next continuation rule

The next Phase 4 modification starts from this exact corrected checkpoint and from the user's next explicitly defined scope.

Before editing:

1. open/copy the exact archived HTML artifact;
2. identify the requested local problem/goal;
3. list the existing behaviors/visual regions that must not regress;
4. apply only the requested change;
5. use browser verification appropriate to the change;
6. create a new checkpoint instead of overwriting this one when the result is accepted.

Do not independently continue old plans merely because a previous handoff listed them. The user now defines the next scope.
