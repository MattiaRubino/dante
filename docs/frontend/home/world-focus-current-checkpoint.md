# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M3 CLOSED / VALIDATED — M4 CONTEXTUAL DANTE ACTIVE / D2 READ-ONLY PREFLIGHT ACTIVE  
**Date:** 2026-09-05  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Historical `NEXT`/`ACTIVE` prose is evidence only unless adopted here. Fresh live code inspection is required before every write scope.

# 1. Read order

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
11. world-focus-m2-shared-visual-primitives.md
12. world-focus-m1-core-nonvisual-materialization-review.md
13. world-focus-m0-materialization-mapping.md
14. product/platform/structure/geometry contracts as needed
```

# 2. Live sequence

```text
WF0                                      FROZEN / USER AUTHORIZED
WF-G3                                    LOCKED / USER AUTHORIZED
WF-V4                                    CANDIDATE
B0 / WR0–WR2 / B1 / B2                  CLOSED AS RECORDED
Workspace Platform                       ENGINEERING CLOSED
D0                                       ACCEPTED
D1                                       CLOSED FOR SEQUENCING
WS0–WS8                                  CLOSED
POST-WS8 HYGIENE                         CLOSED / APPLIED
PRE-M0 FALSIFICATION                     CLOSED / PASS
M0                                       CLOSED
M1                                       CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION             CLOSED / PASS
M2                                       CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION           CLOSED / PASS
M3 Adaptive World Composition            CLOSED / VALIDATED
M3-1 composition configuration           CLOSED / VALIDATED
M3-2 adaptive candidate resolver         CLOSED / VALIDATED
PRE-M3-3 customization safety            CLOSED / PASS
M3-3 Manual Customize UX                 CLOSED / VALIDATED
M3-4 integrated adaptive composition     CLOSED / VALIDATED
M3 final hostile closure                 CLOSED / PASS
M4 Contextual DANTE / D2–D6             ACTIVE
D2 adaptive conversation surface         READ-ONLY PREFLIGHT ACTIVE / NOT MATERIALIZED
D3 deterministic conversation adapter    BLOCKED BY D2
D4 contextual/deictic invocation         BLOCKED BY D3
D5 Insight presentation integration      BLOCKED BY D4
D6 Proposal/confirmation/receipt          BLOCKED BY D5
M5 complete contrasting Worlds           BLOCKED BY M4
M6 integrated product/visual/a11y/perf   BLOCKED BY M5
M7 pre-backend frontend freeze           BLOCKED BY M6
BACKEND                                  BLOCKED UNTIL M7
human/manual visual review               NOT PERFORMED
```

# 3. Permanent product / semantic law

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

A World is a shared coordinate system between user and DANTE, not a shared source of truth.

Permanent non-collapses:

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend authorization
AI output != accepted fact
Possibility != Goal != Proposal != Decision
planned != actual
Actual != Observation != Outcome
Proposal != Decision != effect
provider ACK != canonical completion
cancel != reverse != compensation
Comparison != Decision
missing trajectory position != zero
client composition config != canonical Domain state
client revision != backend persistence revision
adopt != semantic truth != authorization != persistence
renderer availability != mandatory mounting
presentation geometry != conversation identity
selected UI/context != authorization
```

# 4. Closed M3 result

M3 now closes the full adaptive composition path:

```text
seven existing M1 runtime readers
-> one bounded adaptive snapshot
-> meaningful M3-2 opportunities
+ exact accepted M3-3 config owner
+ no invented DANTE/M4 ranking signals
-> M3-2 resolver
-> existing Workspace planner
-> finite registry
-> CompositionHost
-> M2 display-safe renderers
```

Customization remains one canonical client transaction:

```text
CURRENT CONFIG
-> begin customization
-> isolated DRAFT
-> adopt / pin / unpin / hide / show / move / promote / restore
-> REVIEW
-> Apply | Cancel
```

Configuration is composition metadata only. Apply is exact-base/revision guarded and never implicitly merges/rebases.

M3 final hostile closure:

```text
PRE-SCOPE  2e69b1dd0bda25beaecbc5e5baa26f8720a76ff1
HOSTILE    d9c30a3c6148469b347754eab07dc2ade9be4c52
CI         33951509083 / run #944 PASS
80 / 80 web test files
391 / 391 web unit tests
300 modules / 899 dependencies / 0 architecture violations
Quality / build / diff / mutation / Mobile / Chromium / Firefox / Gate PASS
```

Scope compare is linear (`ahead 2`, `behind 0`) and the only net changed path is `world-focus-m3-final-hostile.test.ts`. No production code changed.

Detailed evidence: `world-focus-m3-final-hostile-closure-review.md`.

# 5. M4 / D2 accepted starting point

D0 already fixes the spatial direction:

```text
P0 quiet DANTE invoke
P1 compact transient composer
ongoing conversation + wide viable workspace
-> workspace sidecar

ongoing conversation + constrained/mobile workspace
-> route-owned focus overlay below Global Topbar

wide deep work
-> explicit maximize sidecar -> focus overlay
-> restore same conversation
```

Important D2 laws:

```text
AI availability is persistent; AI footprint is not
sidecar is non-modal
route focus overlay does not re-own Global Topbar
actual allocated workspace geometry decides split viability
presentation geometry != conversation identity
World switch/generation guards prevent late result attachment to another World
no fake D3 messages/backend in D2
```

Live architecture facts already confirmed in D2 preflight:

```text
Workspace allocator classifies presentation='route' as slot='external'
WorldFocusSurfaceLayer deliberately does not render external placements
workspace-local sidecar fallback becomes overlay when split is impossible
that workspace overlay is NOT sufficient for long conversation at ~238 px mobile workspace
WorldFocusWorkspaceHost already owns the one transient surface stack/state
AppShell owns GlobalTopbar then #app-route-content / Outlet
WorldFocus route renders WorldFocusPage inside that route content
```

Therefore D2 needs a route-owned presenter for the existing external surface state; it must not invent a second surface/conversation state engine or a disconnected chatbot route.

# 6. D2 preflight still required before writes

Before D2 write scope is fixed, inspect/falsify at least:

```text
WorldFocusWorkspaceHost state and promote/replace/escape semantics
route-owned placement/external activation semantics
WorldFocusPage ownership below AppShell Topbar
AppShell route geometry/CSS
D1 invoke/composer focus lifecycle
surface registry and finite-kind ownership
existing browser tests and pressure widths
sidecar -> route focus maximize/restore continuity
compact/mobile automatic presentation policy without duplicating viewport JS state
```

Then state exact PRE-SCOPE / CREATE / UPDATE / DELETE / RED-FIRST / OUT-OF-SCOPE.

# 7. Visual strategy agreed with user

```text
M4: implement the real DANTE interaction grammar; only structural visual check after M4
M5: prove contrasting complete Worlds over the same engine
After M5: serious product/visual review
M6: implement/refine visual polish + responsive + a11y + performance
M7: pre-backend frontend freeze
```

Do not spend M4 on cosmetic redesign unrelated to its interaction geometry.

# 8. Stop lines

```text
NO D3 fake conversation adapter inside D2
NO D4 contextual reference widening inside D2
NO D5/D6 early materialization
NO second surface/workspace/conversation state engine
NO AppShell/GlobalTopbar ownership rewrite
NO WF0/WF-G3 macro geometry rewrite
NO localStorage fake persistence
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO claim of human visual acceptance from CI
```

Automated browser green is not human visual acceptance. Human/manual visual review remains **NOT PERFORMED**.
