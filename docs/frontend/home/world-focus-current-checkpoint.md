# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / M3-3 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Historical `NEXT`/`ACTIVE` prose is phase-time evidence unless adopted here.

# 1. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m3-adaptive-composition.md
3. world-focus-m2-shared-visual-primitives.md
4. world-focus-post-m1-safety-falsification-review.md
5. world-focus-m1-core-nonvisual-materialization-review.md
6. world-focus-m1-next-subblock.md
7. world-focus-m0-materialization-mapping.md
8. world-focus-contract-sequencing-supersession.md
9. world-focus-frontend-roadmap.md
10. world-focus-handoff.md
11. world-focus-evidence-index.md
12. product/platform/structure/geometry contracts as needed
```

# 2. Live sequence

```text
WF0                                   FROZEN / USER AUTHORIZED
WF-G3                                 LOCKED / USER AUTHORIZED
WF-V4                                 CANDIDATE
B0                                    ENGINEERING CLOSED
WR0–WR2                               CLOSED
B1                                    CLOSED FOR SEQUENCING
B2                                    IMPLEMENTED / AUTOMATED PASS
Workspace Platform                    ENGINEERING CLOSED
D0                                    ACCEPTED
D1                                    CLOSED FOR SEQUENCING
WS0–WS8                               CLOSED
POST-WS8 HYGIENE                      CLOSED / APPLIED
PRE-M0 FALSIFICATION                  CLOSED / PASS
M0                                    CLOSED
M1                                    CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION          CLOSED / PASS
M2                                    CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION        CLOSED / PASS
M3 Adaptive World Composition         ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver      CLOSED / VALIDATED
M3-3 manual Customize UX              NEXT
M3-4 integrated adaptive composition  BLOCKED BY M3-3
M3 final falsification                BLOCKED BY M3-4
M4–M7                                 BLOCKED BY SEQUENCE
D2–D6                                 DEFERRED TO M4
BACKEND                               BLOCKED UNTIL M7
assistant manual visual review        NOT PERFORMED
```

# 3. Current evidence anchors

```text
M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS

M2 final hostile closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
70 / 70 web test files; 332 / 332 web unit tests
279 modules / 770 dependencies / 0 violations

M3-1 red
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE

M3-1 validation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
72 / 72 web test files; 344 / 344 web unit tests
283 modules / 777 dependencies / 0 violations

M3-2 red
HEAD c2688c46bcbdaf06f2c5da9470bae967550b456d
CI   33854105057 EXPECTED FAILURE

M3-2 validated code
HEAD b7892642dd66104ec04ea4b08ca11aa123789fa4
CI   33854543037 PASS
74 / 74 web test files; 356 / 356 web unit tests
287 modules / 797 dependencies / 0 violations
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS
```

Operational M3-2 PRE-SCOPE is `c5fb717754792c2ad757444533302fbe0e0d5710`. Its tree is identical to the authorized M3-1 closure tree at `4f18f89e35d217c05ca0c2153e82573957e8f42d`; intervening commits only created/deleted empty connector side-effect files and changed no project content.

# 4. Closed substrate retained

M1 owns validated non-visual semantics and application seams. M2 owns bounded display/presentation and finite renderer vocabulary. M3 must consume these layers, not reinterpret them.

Permanent non-collapses include:

```text
World != Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend authorization
timeout != semantic negative
offline != source absent
Comparison != Decision
missing trajectory position != zero
AI output != fact
```

# 5. Existing composition substrate

The Workspace Platform remains the only composition planner owner:

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

M3-2 feeds this planner; it does not replace it. `WorldFocusCompositionHost` still owns placement/failure isolation only.

# 6. M3-1 result

M3-1 owns revisioned client composition configuration plus isolated Draft/Apply/Cancel semantics.

```text
config: schemaVersion / revision / worldId / ordered entries
entry: instanceId / kind / visibility / pinned / prominenceOverride
commands: pin / unpin / hide / show / move / promote / restore
```

Apply creates revision `N+1` only from the current base revision. Stale apply returns `revision-conflict`; no implicit merge. Manual UI and future DANTE proposals share this command language and cannot bypass Apply.

# 7. M3-2 result

M3-2 owns the candidate-resolution boundary:

```text
validated meaningful M1 results
  -> bounded opportunities
  + M3-1 user config
  + finite explicit value signals
  -> WorldFocusCompositionCandidate[]
  -> existing planner
```

Meaningfulness is explicit. Empty/unavailable results do not create modules. Stale/partial Continuity with real content remains meaningful and is qualified later by existing M2 presentation.

Opportunity instances:

```text
situation
continuity
attention:<primitiveId>
next
comparison:<primitiveId>
trajectory:<primitiveId>
evidence-history
```

Opportunity metadata contains no source projection/reference/reason code, Domain payload, AuthZ/disclosure state or executable renderer.

Finite ranking signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

No universal confidence, AI relevance or weighted score.

User precedence:

```text
hidden > signals
pinned > adaptive budget
configured relative order > adaptive ranking
promote -> presentation lead only
```

Pinned visible intent without a currently meaningful projection becomes `unresolvedPinned`; content is not fabricated.

World/kind/signal mismatches and stale signal targets fail closed. Unknown future Worlds/module kinds remain representable.

# 8. M0 M3 disposition state

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVE
M0-37 production candidate resolver                      M3-2 CLOSED / VALIDATED
M0-38 Customize Draft/Apply/Cancel + commands           MODEL M3-1 CLOSED; UI M3-3 NEXT
M0-39 client revision/conflict/migration representation M3-1 CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

# 9. Current gate — M3-3 only

M3-3 Manual Customize UX is next but unstarted.

It must expose an explicit, accessible draft-editing surface over the M3-1 commands:

```text
Customize entry
pin/unpin
hide/show
reorder
promote/restore
review changes
Apply/Cancel
revision-conflict UX
keyboard/touch paths
responsive behavior
```

Drag/drop cannot be the only reorder path. M3-3 must not mount adaptive candidates into the live World; that remains M3-4.

# 10. Stop lines

```text
NO M3-4 live integration
NO fake local persistence
NO durable server persistence/cross-device sync
NO DANTE D2–D6
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral work
```

A fresh explicit write gate is required before M3-3.
