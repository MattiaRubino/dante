# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M0 / M1 / POST-M1 SAFETY / M2 CLOSED — M3 ACTIVE / M3-1 + M3-2 VALIDATED / PRE-M3-3 SAFETY CLOSED / PASS / M3-3 CLOSED / VALIDATED / M3-4 NEXT  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This handoff is written so a new chat/agent can continue without reconstructing the project from conversation history. Read the repository live before every write; this file defines current sequence and durable constraints, not a substitute for fresh code inspection.

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-frontend-roadmap.md
4. world-focus-handoff.md
5. world-focus-evidence-index.md
6. current-checkpoint.md
7. world-focus-m2-shared-visual-primitives.md
8. world-focus-m0-materialization-mapping.md
9. product/platform/structure/geometry contracts as needed
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
PRE-M3-3 customization reachability safety CLOSED / PASS
M3-3 Manual Customize UX                   CLOSED / VALIDATED
M3-4 integrated adaptive composition       NEXT / NOT STARTED
M3 final hostile closure                   BLOCKED BY M3-4
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
adopt != semantic truth/AuthZ/persistence
```

## 4. Closed substrate

M1 owns non-visual production semantics/application seams. M2 owns bounded display-safe binding, presentation grammar, finite renderers and truthfulness qualifiers. Workspace Platform remains the only planning/packing/placement authority.

M3-1/M3-2/PRE-M3-3 own the revisioned client composition metadata, canonical draft transaction, bounded meaningful opportunity extraction and candidate resolution. No frontend layer becomes canonical Domain truth, AuthZ or durable persistence authority.

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

`adopt` receives an already-known meaningful opportunity and materializes only composition metadata: visible, unpinned, null prominence override. It cannot retain projection payload, references, reason codes, disclosure/AuthZ state, provider/runtime state, confidence/score/AI relevance or renderer code.

`restore` is base-relative. Existing base entries return to exact base state/order; adopted-only entries disappear from the draft.

Apply semantics:

```text
World mismatch -> fail closed
revision mismatch -> revision-conflict
same revision + different base snapshot -> fail closed
same revision + exact base snapshot -> revision N+1
```

No implicit merge/rebase.

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

## 7. M3-3 closure — what is now live

M3-3 is no longer next. It is **CLOSED / VALIDATED**.

Production additions:

```text
application/world-focus-composition-customization-read.ts
ui/world-focus-composition-customization-context.tsx
ui/world-focus-composition-customization-surface.tsx
ui/world-focus-composition-customization.css
```

Bounded integrations:

```text
ui/world-focus-page.tsx
ui/world-focus-core-surfaces.tsx
packages/i18n/src/resources/en/world-focus.ts
packages/i18n/src/resources/it/world-focus.ts
```

The experience provides:

```text
explicit View -> Customize transition
one isolated route-scoped draft
lazy read of existing M1 projection seams
bounded opportunity reduction before UI state
explicit adopt for unconfigured meaningful opportunities
pin/unpin/hide/show/move/promote/restore through canonical commands
keyboard reorder independent of drag
moved-item focus preservation + screen-reader position announcement
explicit dirty/review state
Apply / Cancel terminals
revision conflict and invalid-state treatment
exact invoker focus return on Cancel/Escape/successful Apply
wide sidecar through existing surface platform
compact overlay through existing Workspace allocator
```

There is no drag dependency, localStorage, server persistence, fake durable state or M3-4 live candidate mounting.

Normal World composition remains the existing core composition until M3-4.

## 8. M3-3 evidence

Authorized PRE-SCOPE:

```text
7b50a5f96739f500bd52ab5f4e35d8f05ce02e3b
```

Valid RED:

```text
f1b08fc1766f801d4573f81194a6e66a147c9433
fd1d503268608df89724e216f3a5fc59f697dbef
CI 33875210161 EXPECTED FAILURE
362 / 362 pre-existing web tests PASS
5 / 5 new M3-3 tests FAIL because Customize was absent
```

Production correction path:

```text
a1e6709e375cdeab984e9625a326ae5fcdc4e919  initial shell
c2f2f3e875c73a3ec54938c206f2fad873f5bc21  cancellation typing/semantics correction
168d3c9565914c8fcc47a578c0750b030d42223f  focus restoration correction / baseline FULL PASS
```

Hostile test-only hardening:

```text
0dd816fe03fc45c5fe1799a5cd41e75c59c726ee
93effa1278b4a3d33c289f6467ee35551d0324b0
1978fe5c77c0e2661239372bf0f9bee238021faa
```

Final M3-3 code/test closure:

```text
HEAD 1978fe5c77c0e2661239372bf0f9bee238021faa
CI   33879774332 / run #907 PASS
77 / 77 web test files
376 / 376 web unit tests
294 modules / 851 dependencies / 0 violations
Quality / build / diff / mutation / Mobile / Chromium / frozen Timeline Firefox / Gate PASS
```

Hostile browser coverage includes all World pressure widths `1856 / 1600 / 1366 / 1200 / 1024 / 901 / 900 / 760 / 721 / 720 / 719 / 390`, no horizontal overflow, sidecar/overlay behavior, axe and forced-colors operability.

The test contract was not weakened. Intermediate red CI results were fixed at their root cause.

Human visual acceptance remains **NOT PERFORMED**.

## 9. M3-3 final scope audit

PRE-SCOPE -> code/test hardening HEAD is linear, no behind. Changed non-doc paths are only the authorized M3-3 application/UI/test/i18n/CSS files. No Timeline, AppShell, Access/Auth, route-tree, backend/API/DB/Alembic/AuthZ/provider/LLM or M3-4 integration work entered the scope.

## 10. Next chat / next phase — M3-4 only

M3-4 is **NEXT / NOT STARTED**. The next agent must not jump straight into writes.

First action: fresh read-only preflight against current branch HEAD.

Inspect live:

```text
world-focus current checkpoint and M3 authority
WorldFocusPage / current normal composition owner
M1 runtime projection readers
M3-2 opportunity collector and candidate resolver
M3 accepted config/customization owner
existing planner / module registry / CompositionHost
Workspace/surface allocation
renderer failure isolation
current tests, CSS and i18n as affected by the proposed path
```

Then propose a new exact bounded gate:

```text
branch
PRE-SCOPE exact SHA
CREATE
UPDATE
DELETE
purpose
red-first tests
explicit out-of-scope
```

M3-4 target path:

```text
validated M1 application results
-> meaningful opportunities
+ accepted M3 config
+ finite value signals
-> M3-2 candidate resolver
-> existing planner
-> finite registry
-> CompositionHost
```

Must prove:

```text
sparse remains sparse
hidden remains hidden
pinned intent survives adaptive budget
configured order remains user-owned
configured supporting remains supporting unless promoted
unresolved pin never fabricates content
unknown future kinds remain safe
renderer failure remains local
no fake persistence
no frontend canonical-truth/AuthZ invention
```

## 11. Explicit out-of-scope until a later gate

```text
NO M3 final hostile closure before M3-4
NO M4 D2–D6
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO localStorage fake persistence
NO durable server/cross-device persistence
NO Timeline/AppShell/Access/Auth collateral work
NO generated route-tree edits
NO history rewrite / force push
```

## 12. After M3-4

```text
M3 final hostile closure
-> M4 D2–D6 contextual DANTE
-> M5 contrasting complete Worlds
-> M6 integrated product/visual/a11y/perf review
-> M7 pre-backend freeze
-> backend vertical integration
```
