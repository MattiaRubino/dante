# LifeOS — Home vNext Orientation + Day Ribbon v1

**Date:** 2026-08-18  
**Branch:** `prototype/phase-4-today-home`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT — current Phase 4 continuation artifact**  
**Supersedes for continuation:** `docs/phase-4/home-vnext-adesso-main-stage-v1.md`  
**Nature:** standalone HTML/CSS/JavaScript UX prototype; not production React/Next.js code and not final Information Architecture/product vocabulary

---

## 1. Purpose

This checkpoint freezes the exact user-supplied Home/Today prototype accepted on 2026-08-18 and makes it the deterministic starting point for the next Phase 4 iteration.

Do not reconstruct this state approximately from screenshots, old conversation previews or earlier checkpoints. Open the exact archived HTML artifact.

Exact identity:

```text
filename
lifeos_home_vnext_orientation_day_ribbon_v1.html

size
748590 bytes

SHA-256
88a88b4098672d26c7681cedd1d189c380f0b69e33ec9d6e536f5022ef93be17
```

Archive:

`prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/`

The exact HTML is stored directly as:

`prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/lifeos_home_vnext_orientation_day_ribbon_v1.html`

Git blob SHA: `8933e62c4d99d09e7ef07620fa779496d6179650`. The artifact was moved into this checkpoint by reusing that verified blob, so no byte transformation occurred.

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

The exact artifact is authoritative. At a high level it contains the current integrated Home/Today direction, including:

- global Home shell and professional conversational AI surface;
- current-situation composition around `Ora` / immediate continuation, attention and contextual/dynamic information;
- carried-forward central stage with current prototype `Worlds` / `Stats` modes and their carousel/navigation behavior;
- current Home orientation strip and synchronized day context;
- dedicated day ribbon / week navigation;
- contextual `Ora` return-to-current-time control;
- calendar navigation;
- 24-hour Today timeline;
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

Home, Today, temporal views, contextual surfaces, natural language and future Mobile/Web representations operate on the same underlying LifeOS reality. Presentation state is not a competing source of truth.

### Time is primary, not sovereign

Today/timeline is a powerful operational projection, but LifeOS is not reducible to calendar blocks. Persistent realities may matter without being scheduled.

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
- Home/Today visual composition is evidence and approved prototype work, not by itself a final Information Architecture decision.

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

## 7. QA recorded at checkpoint creation

Exact source/static validation:

```text
size                         748590 bytes
SHA-256                      88a88b4098672d26c7681cedd1d189c380f0b69e33ec9d6e536f5022ef93be17
DOM IDs                      67
duplicate DOM IDs            0
style blocks                 37
CSS parse errors             0
inline scripts               20
inline JS syntax failures    0
Git blob byte identity       PASS
```

Integrated Chromium smoke at `1575x945`:

```text
page/console errors          0
lifeos-today                 present
orientation day context      present
week strip                   present
Ora action                   present
split-groups control         present
rendered group chips         6
rendered event cards         24
time-edit controls           24
hour labels                  00:00 through 24:00
World layer                  present
Stats stage                  present
anchored time picker         opens / body portal PASS
split-groups toggle          aria state changes PASS

RESULT
PASS
```

Qualification: this is a real integrated smoke plus static gate. It is **not** relabelled as a full execution of `today-v21-regression.py`.

Detailed record: `prototypes/home/archive/home-vnext-orientation-day-ribbon-v1/qa-static.json`.

---

## 8. Next continuation rule

The next Phase 4 modification starts from this exact checkpoint and from the user's next explicitly defined scope.

Before editing:

1. open/copy the exact archived HTML artifact;
2. identify the requested local problem/goal;
3. list the existing behaviors/visual regions that must not regress;
4. apply only the requested change;
5. use browser verification appropriate to the change;
6. create a new checkpoint instead of overwriting this one when the result is accepted.

Do not independently continue old `Appunti` / `Review` plans or any older “next task” merely because a previous handoff listed them. The user now defines the next scope.
