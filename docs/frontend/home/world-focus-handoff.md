# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M0 / M1 / POST-M1 SAFETY / M2 / M3 CLOSED — M4 ACTIVE / D2 PREFLIGHT ACTIVE  
**Date:** 2026-09-05  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This handoff lets a new chat/agent continue without reconstructing the workstream from conversation history. Read repository live before every write; this file defines current sequence and durable constraints, not a substitute for code inspection.

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-frontend-roadmap.md
3. world-focus-handoff.md
4. world-focus-evidence-index.md
5. current-checkpoint.md
6. world-focus-m3-final-hostile-closure-review.md
7. world-focus-m3-adaptive-composition.md
8. world-focus-m3-4-integrated-adaptive-composition-review.md
9. world-focus-dante-spatial-presence-review.md
10. world-focus-d1-dante-entry-review.md
11. product/platform/structure/geometry contracts as needed
```

Older phase-time `NEXT` prose is evidence only unless adopted by current checkpoint authority.

## 1. Current sequence

```text
WF0 / WF-G3                                FROZEN / LOCKED
B0 / WR0–WR2 / B1 / B2                    CLOSED / VALIDATED AS RECORDED
Workspace Platform                         ENGINEERING CLOSED
D0                                         ACCEPTED
D1                                         CLOSED FOR SEQUENCING
WS0–WS8                                    CLOSED
M0                                         CLOSED
M1                                         CLOSED / VALIDATED
POST-M1 SAFETY                             CLOSED / PASS
M2                                         CLOSED / VALIDATED
M3                                         CLOSED / VALIDATED
M3-1                                       CLOSED / VALIDATED
M3-2                                       CLOSED / VALIDATED
PRE-M3-3                                   CLOSED / PASS
M3-3                                       CLOSED / VALIDATED
M3-4                                       CLOSED / VALIDATED
M3 final hostile closure                   CLOSED / PASS
M4 D2–D6                                   ACTIVE
D2 adaptive conversation surface           READ-ONLY PREFLIGHT ACTIVE
D3–D6                                      BLOCKED BY D2 SEQUENCE
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
presentation geometry != conversation identity
context/selection != authorization
```

## 4. Closed M3 substrate

M1 owns non-visual production semantics/application seams. M2 owns bounded display-safe binding, presentation grammar, finite renderers and truthfulness qualifiers. Workspace Platform remains the only planning/packing/placement authority.

M3 owns revisioned client composition metadata, canonical draft transaction, meaningful opportunity extraction, candidate resolution, explicit manual Customize UX and live normal adaptive composition.

Canonical config:

```text
schemaVersion / revision / worldId / ordered entries
entry: instanceId / kind / visibility / pinned / prominenceOverride
```

Finite commands:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

One governed path:

```text
manual UI [M3-3] ----\
                       -> commands -> isolated DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

No hidden DANTE mutation route. `adopt` materializes composition metadata only. `restore` is base-relative. Apply requires World match, revision match and exact base snapshot. No implicit merge/rebase.

Normal live composition:

```text
seven existing M1 readers
-> one bounded adaptive snapshot
-> meaningful opportunities
+ exact accepted config owner
+ no invented M4/DANTE signals
-> M3-2 resolver
-> existing Workspace planner
-> finite registry
-> CompositionHost
-> M2 display-safe renderers
```

## 5. M3 final closure evidence

```text
PRE-SCOPE 2e69b1dd0bda25beaecbc5e5baa26f8720a76ff1
HOSTILE   d9c30a3c6148469b347754eab07dc2ade9be4c52
CI        33951509083 / run #944 PASS
80 / 80 web test files
391 / 391 web unit tests
300 modules / 899 dependencies / 0 architecture violations
Quality / build / diff / mutation / Mobile / Chromium / frozen Firefox / Gate PASS
```

The final hostile phase added exactly one test file and **no production change**. Scope compare is linear (`ahead 2`, `behind 0`). It combines projection truthfulness, guarded customization transaction, resolver precedence, planner budgets/order and 200 seeded hostile configurations. Existing 500-composition and 500-workspace-allocation random pressure remains green.

Detailed evidence:

```text
world-focus-m3-final-hostile-closure-review.md
world-focus-m3-4-integrated-adaptive-composition-review.md
```

## 6. M4 accepted direction

D0 spatial contract remains authoritative:

```text
P0 quiet invoke                        D1 CLOSED
P1 compact composer                    D1 CLOSED
ongoing wide conversation              D2 -> workspace sidecar
ongoing constrained/mobile             D2 -> route-owned focus overlay
wide explicit deep-work maximize       D2 -> sidecar -> route focus overlay
restore                                D2 -> same conversation identity
```

Important:

```text
AI availability is persistent; AI footprint is not
sidecar is non-modal
actual allocated workspace geometry decides split viability
route focus overlay sits below Global Topbar and does not re-own AppShell
presentation geometry != conversation identity
D2 must not fake D3 messages/model/backend
```

## 7. D2 read-only preflight findings already established

Live code confirms:

```text
WorldFocusWorkspaceHost
-> one reducer-owned transient workspace state/surface stack
-> open / replace / promote / close / Escape APIs
-> keyed by worldId so another World cannot inherit transient state

Workspace allocation
-> sidecar splits only when actual workspace >= viable threshold
-> sidecar otherwise becomes workspace-local overlay
-> presentation='route' is represented as slot='external'

WorldFocusSurfaceLayer
-> renders workspace-local sidecar/overlay/focus only
-> deliberately skips external placements

AppShell
-> owns GlobalTopbar
-> then #app-route-content / Outlet

World route
-> renders WorldFocusPage under AppShell route content
```

Therefore D2 cannot simply rely on sidecar's compact workspace-overlay fallback for long conversation: D0 already proved the World workspace can be ~238 px at 390 viewport width. D2 needs a **route-owned presenter for the existing external surface state** below GlobalTopbar.

It must not create:

```text
second surface state engine
second Workspace host
independent chat route/product
new URL solely to represent presentation geometry
AppShell/Topbar ownership rewrite
```

## 8. D2 next exact methodological step

Before writes:

```text
fresh branch/HEAD
inspect AppShell route geometry CSS
inspect D1 tests/focus lifecycle
inspect Workspace surface reducer promote/replace/escape laws
inspect finite surface registry and external placement semantics
inspect responsive browser pressure tests
choose exact owner for route-owned external presenter
state PRE-SCOPE / CREATE / UPDATE / DELETE / RED-FIRST / OUT-OF-SCOPE
```

RED-first must prove at least:

```text
wide conversation -> sidecar
constrained conversation -> route-owned focus overlay, not ~238px workspace overlay
explicit maximize/restore preserves same logical conversation identity
presentation switch does not create a second conversation state
sidecar remains non-modal
route focus owns appropriate interaction/focus/Escape without re-owning Topbar
World switch/generation cannot attach stale transient DANTE surface to the next World
D2 contains no fake assistant message/backend behavior
```

## 9. M4 remaining sequence

```text
D2 adaptive conversation surface
-> D3 deterministic pre-backend conversation adapter
-> D4 contextual/deictic invocation with bounded references
-> D5 Insight presentation integration
-> D6 Proposal / confirmation / receipt presentation
```

DANTE proposals later reuse canonical app paths; they do not bypass manual capability or mutation governance.

## 10. Visual strategy agreed with user

```text
After M4: structural visual check only
M5: build contrasting complete Worlds
After M5: serious product/visual review
M6: visual polish + responsive + motion + a11y + performance
M7: frontend/backend seam freeze
```

Do not spend D2–D6 on unrelated cosmetic redesign.

## 11. Explicit out-of-scope

```text
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO localStorage fake persistence
NO durable server/cross-device persistence
NO Timeline/Access/Auth collateral work
NO GlobalTopbar ownership rewrite
NO WF0/WF-G3 macro geometry rewrite
NO D3–D6 hidden inside D2
NO generated route-tree edits unless a later explicitly-authorized route design proves unavoidable
NO history rewrite / force push
```

## 12. Human visual status

Automated browser coverage is green. Human/manual visual acceptance remains **NOT PERFORMED** and must not be inferred from CI.
