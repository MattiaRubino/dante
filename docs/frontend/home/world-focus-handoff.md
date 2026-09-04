# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M0 / M1 / POST-M1 SAFETY / M2 CLOSED — M3 ACTIVE / M3-1 + M3-2 + M3-3 + M3-4 VALIDATED / PRE-M3-3 SAFETY CLOSED / PASS / M3 FINAL HOSTILE CLOSURE NEXT  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This handoff lets a new chat/agent continue without reconstructing the workstream from conversation history. Read repository live before every write; this file defines current sequence and durable constraints, not a substitute for code inspection.

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-frontend-roadmap.md
4. world-focus-handoff.md
5. world-focus-evidence-index.md
6. current-checkpoint.md
7. world-focus-m3-4-integrated-adaptive-composition-review.md
8. world-focus-m2-shared-visual-primitives.md
9. world-focus-m0-materialization-mapping.md
10. product/platform/structure/geometry contracts as needed
```

Older phase-time `NEXT` prose is evidence only unless adopted by current checkpoint authority.

## 1. Current sequence

```text
WF0 / WF-G3                                FROZEN / LOCKED
B0 / WR0–WR2 / B1 / B2                    CLOSED / VALIDATED AS RECORDED
Workspace Platform                         ENGINEERING CLOSED
D0 / D1                                    ACCEPTED / CLOSED FOR SEQUENCING
WS0–WS8                                    CLOSED
M0                                         CLOSED
M1                                         CLOSED / VALIDATED
POST-M1 SAFETY                             CLOSED / PASS
M2                                         CLOSED / VALIDATED
M3                                         ACTIVE
M3-1 composition configuration             CLOSED / VALIDATED
M3-2 adaptive candidate resolver           CLOSED / VALIDATED
PRE-M3-3 customization safety              CLOSED / PASS
M3-3 Manual Customize UX                   CLOSED / VALIDATED
M3-4 integrated adaptive composition       CLOSED / VALIDATED
M3 final hostile closure                   NEXT / NOT STARTED
M4 D2–D6                                   BLOCKED BY M3
M5–M7                                      BLOCKED BY SEQUENCE
BACKEND                                    BLOCKED UNTIL M7
human/manual visual acceptance             NOT PERFORMED
```

## 2. Product compass

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

Core thesis:

> **A World is a shared coordinate system between user and DANTE, not a shared source of truth.**

World is not a Domain owner, folder, life taxonomy, DB partition, security boundary, AI memory bucket, chat room or mandatory Goal/KPI/time surface.

## 3. Permanent semantic barriers

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend AuthZ
offline != source absent
timeout != semantic negative
Proposal != Decision != effect
provider ACK != canonical completion
Comparison != Decision
missing trajectory position != zero
AI output != fact
client composition config != Domain state
client revision != backend persistence revision
renderer availability != mandatory mounting
adopt != semantic truth/AuthZ/persistence
```

## 4. Closed substrate

M1 owns non-visual production semantics/application seams. M2 owns bounded display-safe binding, presentation grammar, finite renderers and truthfulness qualifiers. Workspace Platform remains the only planning/packing/placement authority.

M3-1/M3-2/PRE-M3-3 own revisioned client composition metadata, canonical draft transaction, meaningful opportunity extraction and candidate resolution. M3-3 owns the explicit manual Customize UX over that transaction. M3-4 owns the live integration of these layers into normal World rendering.

No frontend layer becomes canonical Domain truth, AuthZ or durable persistence authority.

## 5. Canonical composition customization contract

Configuration:

```text
schemaVersion / revision / worldId / ordered entries
entry: instanceId / kind / visibility / pinned / prominenceOverride
```

Finite commands:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

Origins:

```text
manual
dante-proposed
```

One path:

```text
manual UI [M3-3] ----\
                       -> commands -> isolated DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

No hidden DANTE mutation route.

`adopt` receives an already-known meaningful opportunity and materializes only composition metadata. `restore` is base-relative. Apply requires World match, revision match and exact base snapshot. No implicit merge/rebase.

## 6. M3-2 candidate resolver retained

```text
validated M1 results
-> meaningful bounded opportunities
+ accepted/current M3 config
+ finite value signals
-> WorldFocusCompositionCandidate[]
-> existing planner
```

Finite signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

Precedence:

```text
hidden > signals
pinned > adaptive budget
configured order > adaptive ranking
configured + null override -> preserve opportunity.defaultProminence
configured + lead override -> lead
```

Sparse remains sparse. Pinned intent with no meaningful current projection remains unresolved intent, not fake content.

## 7. M3-3 Manual Customize UX — CLOSED / VALIDATED

M3-3 provides:

```text
explicit View -> Customize transition
one isolated route-scoped draft
lazy read of existing M1 projection seams
bounded opportunity reduction before UI state
explicit adopt
pin/unpin/hide/show/move/promote/restore
keyboard reorder independent of drag
moved-item focus preservation + screen-reader position announcement
Apply / Cancel terminals
revision conflict and invalid-state treatment
exact invoker focus return
wide sidecar / compact overlay via existing Workspace Platform
```

There is no drag dependency, localStorage, server persistence or fake durable state.

Evidence:

```text
PRE-SCOPE 7b50a5f96739f500bd52ab5f4e35d8f05ce02e3b
CODE/TEST  1978fe5c77c0e2661239372bf0f9bee238021faa
CI         33879774332 / run #907 PASS
```

## 8. M3-4 Integrated Adaptive Composition — CLOSED / VALIDATED

M3-4 changed normal live World composition from the pre-M3-4 fixed feed to the validated adaptive pipeline:

```text
seven existing M1 runtime readers
-> one bounded adaptive snapshot
-> M3-2 meaningful opportunities
+ the exact accepted M3-3 config owner
+ no invented M4/DANTE ranking signals
-> M3-2 resolver
-> existing Workspace planner
-> finite registry
-> CompositionHost
-> M2 display-safe renderers
```

The same snapshot supplies both opportunity meaning and display-safe rendering data. Apply therefore updates accepted composition metadata and normal composition consumes that owner directly; there is no second config store or second read-on-Apply path.

Proven behavior:

```text
sparse remains sparse
hidden remains hidden
pin protects budget survival without implicit move
promote changes prominence without implicit move
configured order remains user-owned
configured supporting stays supporting unless promoted
stable relative order remains intact
non-user dynamic lead policy remains intact
unresolved pin never fabricates content
unknown future kind degrades locally as unsupported
registered renderer throw degrades locally as error
healthy sibling stays rendered
active scrollable main plane is keyboard focusable
```

Integration surfaced and corrected owner-level defects rather than weakening tests:

```text
planner prominence ordering vs configured order
mixed stable/user/non-user lead reconciliation
scrollable-region keyboard accessibility after multi-module mounting
renderer invocation before error boundary
```

Evidence:

```text
PRE-SCOPE 688e1ab0c7a42f8d83274dedf5a2988a9388bda4
RED        d2af7a47df8562439487fb4ab4298bff4653f098 / CI 33903884239 EXPECTED FAILURE
CODE/TEST  b10dc2bef8bab6ae863ce3c8331da6de96094a66
CI         33904052325 / run #934 PASS
79 / 79 web test files
387 / 387 web unit tests
299 modules / 891 dependencies / 0 violations
Quality / build / diff / mutation / Mobile / Chromium / Firefox / Gate PASS
```

Detailed evidence: `world-focus-m3-4-integrated-adaptive-composition-review.md`.

## 9. M3-4 scope audit

Compare `688e1ab... -> b10dc2b...` is linear (`ahead 8`, `behind 0`). Changed non-doc paths are World Focus application/UI/test/E2E plus directly-falsified planner/workspace corrections.

No Timeline implementation, AppShell, Access/Auth, generated route-tree, backend/API/DB/Alembic/AuthZ/provider/LLM or persistence path changed.

## 10. Next chat / next phase — M3 final hostile closure only

M3 final hostile closure is **NEXT / NOT STARTED**. Do not jump into M4.

First action: fresh read-only preflight against current branch HEAD, then exact bounded gate.

Attack the combined M3 layer with:

```text
conflicting config
stale/partial/empty/unavailable M1 results
sparse and dense worlds
many candidates / budget edges
adopted + hidden + pinned + promoted combinations
mixed user/stable/application-derived ordering
unresolved pins
unknown kinds
renderer failures
responsive / keyboard / a11y pressure
accepted-config revision/base integrity
```

This phase should add no new feature semantics. Only after it passes may M3 become CLOSED and M4 D2–D6 become NEXT.

## 11. Explicit out-of-scope

```text
NO M4 D2–D6 before M3 closure
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO localStorage fake persistence
NO durable server/cross-device persistence
NO Timeline/AppShell/Access/Auth collateral work
NO generated route-tree edits
NO history rewrite / force push
```

## 12. Human visual status

Automated browser coverage is green, including responsive, axe and frozen Timeline regression. Human/manual visual acceptance remains **NOT PERFORMED** and must not be inferred from CI.
