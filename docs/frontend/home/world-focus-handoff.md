# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M0 / M1 / POST-M1 SAFETY / M2 CLOSED — M3 ACTIVE / M3-1 + M3-2 VALIDATED / M3-3 NEXT  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-m2-shared-visual-primitives.md
4. world-focus-m0-materialization-mapping.md
5. world-focus-frontend-roadmap.md
6. world-focus-evidence-index.md
7. product/platform/structure/geometry contracts as needed
```

Older phase-time `NEXT` prose is evidence only unless adopted by the current checkpoint.

## 1. Current sequence

```text
WF0 / WF-G3                            FROZEN / LOCKED
B0 / WR0–WR2 / B1 / B2                CLOSED / VALIDATED AS RECORDED
Workspace Platform                     ENGINEERING CLOSED
D0 / D1                                ACCEPTED / CLOSED FOR SEQUENCING
WS0–WS8                                CLOSED
M0                                     CLOSED
M1                                     CLOSED / VALIDATED
POST-M1 SAFETY                         CLOSED / PASS
M2                                     CLOSED / VALIDATED
M3                                     ACTIVE
M3-1 composition configuration         CLOSED / VALIDATED
M3-2 adaptive candidate resolver       CLOSED / VALIDATED
M3-3 manual Customize UX               NEXT
M3-4 integrated adaptive composition   BLOCKED BY M3-3
M4 D2–D6                               BLOCKED BY M3
M5–M7                                  BLOCKED BY SEQUENCE
BACKEND                                BLOCKED UNTIL M7
manual visual acceptance               NOT PERFORMED
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
```

## 4. Closed M1/M2 substrate

M1 owns non-visual production semantics/application seams including open-ended World identity, bounded references, truthfulness/disclosure/effect/sync dimensions, O2/O5/O8 and WP-01..04.

M2 owns bounded display-safe binding, presentation grammar, WP renderers, O2/O5/O8 rendering and truthfulness qualifiers. Renderer availability never implies mandatory live mounting.

## 5. Existing composition engine — preserve

Workspace Platform already owns:

```text
stable / adaptive / ephemeral
system-default / user / dante-proposed / application-derived
lead / primary / supporting
wide / standard / compact
12-unit deterministic packing
adaptive / ephemeral budgets
stable relative-order preservation
finite module registry
local renderer failure isolation
```

M3 must feed this engine rather than replace it.

## 6. M3-1 handoff

Production owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Configuration is revisioned client composition metadata only:

```text
schemaVersion / revision / worldId / ordered entries
entry: instanceId / kind / visibility / pinned / prominenceOverride
```

Customization transaction:

```text
CURRENT -> DRAFT -> pin/unpin/hide/show/move/promote/restore -> Apply | Cancel
```

Stale Apply returns `revision-conflict`; no implicit merge. Manual UI and future DANTE proposals use the same command language and Apply barrier.

Evidence:

```text
RED  b68b6e8fa0d70844f6d058c7b77ded676f1e675f / CI 33850177297 EXPECTED FAILURE
PASS 49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
```

## 7. M3-2 handoff

Production owners:

```text
application/world-focus-composition-opportunities.ts
application/world-focus-composition-resolver.ts
```

M3-2 creates no UI. It sits before the existing planner:

```text
validated M1 results
-> meaningful bounded opportunities
+ current M3-1 config
+ finite application-owned value signals
-> WorldFocusCompositionCandidate[]
-> existing planner
```

Meaningful mapping:

```text
Situation ready + content                -> situation
Continuity ready/partial/stale + content -> continuity
Attention ready                          -> attention:<id> per primitive
Next ready + content                     -> next
Comparison ready                         -> comparison:<id> per primitive
Trajectory ready                         -> trajectory:<id> per primitive
Evidence/History any role content        -> evidence-history
empty / unavailable                      -> nothing
```

Opportunity set is bounded to 16. Opportunity metadata carries no projection, context references, `reasonCode`, Domain payload, disclosure/AuthZ authority or renderer code.

Finite value signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No confidence score, `aiRelevance`, weighted ranking number or model authority exists.

Value bands:

```text
foreground -> lead minimum
active     -> primary minimum
ordinary   -> opportunity default
```

User configuration precedence:

```text
hidden > signals
pinned > adaptive budget
configured order > adaptive ranking
promote -> lead override only
```

Pinned visible config with no meaningful projection becomes `unresolvedPinned`, never a fake empty candidate.

Resolver fails closed on World/kind mismatches, stale signal targets and duplicates. Unknown future World/module kinds remain supported.

Evidence:

```text
operational PRE-SCOPE c5fb717754792c2ad757444533302fbe0e0d5710
RED  c2688c46bcbdaf06f2c5da9470bae967550b456d / CI 33854105057 EXPECTED FAILURE
PASS b7892642dd66104ec04ea4b08ca11aa123789fa4 / CI 33854543037 PASS
74 / 74 web test files
356 / 356 web unit tests
287 modules / 797 dependencies / 0 violations
Quality / Mobile / Chromium / frozen Timeline Firefox / Gate PASS
```

## 8. Manual / DANTE capability rule

Permanent rule:

> Canonical app capabilities that DANTE can propose or accelerate must remain usable through a manual/non-AI path where they are meaningful application functions.

For composition:

```text
manual UI [M3-3] ----\
                       -> same commands -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

DANTE has no hidden configuration mutation API.

## 9. M3-3 handoff — next only

M3-3 must build the actual manual Customize surface over M3-1, informed by M3-2 opportunity/config truth.

Required:

```text
explicit Customize mode
draft/current distinction
pin/unpin
hide/show
reorder
promote/restore
change review
Apply/Cancel
revision-conflict UX
keyboard-accessible reorder
usable touch controls
focus and screen-reader semantics
responsive behavior
```

Drag/drop is optional enhancement, not the only reorder path.

M3-3 must not perform M3-4 live candidate integration and must not invent persistence.

## 10. Explicit stop lines

```text
NO live adaptive World composition until M3-4
NO localStorage fake persistence
NO durable server config persistence
NO DANTE D2–D6 until M4
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral changes
```

When frontend sequencing reaches M7, later real vertical integration can connect:

```text
UI -> application -> Access/Auth/AuthZ -> API -> Domain -> PostgreSQL
```

under backend authority.

## 11. Repository discipline

Every new write scope requires fresh branch HEAD, explicit paths/PRE-SCOPE and bounded authorization. No merge/rebase/force/main mutation without explicit authorization. Fix CI root causes rather than weakening tests.

Immediate continuation:

> **M3-3 is NEXT but unstarted. Start only with a fresh bounded write gate.**
