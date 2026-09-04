# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Older `D2 NEXT`, `M0 NEXT`, `M1 ACTIVE`, `M2 ACTIVE`, `M3 NEXT` or similar prose is phase-time history only unless adopted here.

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
9. world-focus-pre-m0-falsification-review.md
10. world-focus-post-ws8-hygiene-audit.md
11. world-focus-substrate-closure-plan.md
12. world-focus-frontend-roadmap.md
13. world-focus-handoff.md
14. world-focus-evidence-index.md
15. WS7/WS8/WS6 evidence as needed
16. product/platform/structure/geometry contracts as needed
```

# 2. Live sequence

```text
WF0                                      FROZEN / USER AUTHORIZED
WF-G3                                    LOCKED / USER AUTHORIZED
WF-V4                                    CANDIDATE
B0                                       ENGINEERING CLOSED
WR0–WR2                                  CLOSED
B1                                       CLOSED FOR SEQUENCING
B2                                       IMPLEMENTED / AUTOMATED PASS
Workspace Platform                       ENGINEERING CLOSED
D0                                       ACCEPTED
D1                                       CLOSED FOR SEQUENCING
WS0–WS8                                  CLOSED
POST-WS8 HYGIENE                         CLOSED / APPLIED
PRE-M0 FALSIFICATION                     CLOSED / PASS
M0                                       CLOSED
M1                                       CLOSED / VALIDATED
M1-1 identity/reference ownership        CLOSED / VALIDATED
M1-2 non-visual facets + seams           CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION             CLOSED / PASS
M2 shared visual primitive layer         CLOSED / VALIDATED
M2-1 shared presentation/L1 renderers    CLOSED / VALIDATED
M2-2 truthfulness/direct output          CLOSED / VALIDATED
M2 FINAL CLOSURE FALSIFICATION           CLOSED / PASS
M3 Adaptive World Composition            ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver         NEXT
M4–M7                                    BLOCKED BY SEQUENCE
D2–D6                                    DEFERRED TO M4
BACKEND                                  BLOCKED UNTIL M7
assistant manual visual review           NOT PERFORMED
```

# 3. Evidence anchors

```text
WS8 semantic proof/runtime
HEAD 88db899391a3a41e23e76177d4896a657232b5eb
CI   33639741630 PASS

M0 closure docs
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1-1 production identity/reference
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 production non-visual semantics
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS

M2-1 shared visual primitive validation
HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI   33781753823 PASS
61 / 61 web test files; 312 / 312 web unit tests
262 modules / 684 dependencies / 0 violations
Continuity pressure at 720 / 719 / 390 PASS

M2-2 final integration validation
HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5
CI   33788370490 PASS

M2 final hostile closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
hostile 5 / 5 PASS
web test files 70 / 70; web unit tests 332 / 332
architecture 279 modules / 770 dependencies / 0 violations
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS

M3-1 red-first owner proof
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE
pre-production contracts PASS; Quality failed because M3-1 owner modules were unresolved

M3-1 production validation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
web test files 72 / 72; web unit tests 344 / 344
architecture 283 modules / 777 dependencies / 0 violations
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS
```

# 4. Closed substrate retained

M1 remains the non-visual semantic/application substrate. M2 remains the bounded presentation layer. Neither is reopened by M3.

Permanent non-collapses remain:

```text
World != Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend authorization
offline != source absent
timeout != semantic negative
partial-real effect != generic failure != success
Comparison != Decision
missing trajectory position != zero
AI output != fact
```

# 5. Existing composition substrate reused by M3

The Workspace Platform already owns a deterministic bounded composition planner and finite module registry.

Current planner semantics retained:

```text
stability: stable / adaptive / ephemeral
origin: system-default / user / dante-proposed / application-derived
prominence: lead / primary / supporting
footprint: wide / standard / compact
12-unit grid packing
bounded adaptive/ephemeral budgets
stable relative order preserved
```

`WorldFocusCompositionHost` continues to own placement/failure isolation for an already-resolved plan. It does not become ranking, truth or AuthZ authority.

The current live core candidate input still mounts only Continuity. M3-1 does not modify that composition.

# 6. M3-1 validated production result

M3-1 establishes client composition configuration ownership:

```text
WorldFocusCompositionConfig
  schemaVersion = 1
  revision
  worldId
  ordered entries

entry
  instanceId
  kind
  visibility: visible | hidden
  pinned: boolean
  prominenceOverride: lead | null
```

Config constructors normalize and freeze allowed fields only. Duplicate instances, empty structural tokens, invalid revision or invalid finite state fail closed. Unknown future module kinds remain representable.

Schema compatibility is explicit:

```text
current
migration-required
unsupported
```

No automatic migration is fabricated.

# 7. M3-1 customization transaction

Customization is isolated from current state:

```text
CURRENT CONFIG revision N
        ↓
begin customization
        ↓
DRAFT(baseRevision=N)
        ↓
pin / unpin / hide / show / move / promote / restore
        ↓
Apply OR Cancel
```

Finite sources:

```text
manual
dante-proposed
```

Semantics:

```text
hide != delete
pin != canonical truth
promote != semantic truth
restore = draft-start base state + base order for that entry
```

Apply is the only M3-1 operation that creates revision `N+1`.

Stale current revision returns explicit `revision-conflict`; there is no implicit merge. Cross-World Apply fails closed even when numeric revisions match. Cancel returns the base config with no committed side effect.

# 8. Manual path / DANTE path invariant

Permanent product rule:

> Canonical application capabilities that DANTE can propose or accelerate must also remain available through a manual/non-AI product path where they are meaningful app functions.

M3-1 enforces one command language:

```text
manual UI [later M3-3] ----\
                            -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] -------/
```

DANTE has no hidden configuration mutation API and cannot bypass Apply/revision conflict semantics.

# 9. M0 M3 disposition state

```text
M0-35 stability/origin semantics                      EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner               EXISTING / PRESERVE
M0-37 production candidate resolver                   M3-2 NEXT
M0-38 Customize Draft/Apply/Cancel + commands         PARTIAL / M3-1 MODEL CLOSED; UI M3-3
M0-39 client revision/conflict/migration representation M3-1 CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict  BACKEND-DEFERRED
```

M3-1 deliberately does not claim M0-38 UI closure.

# 10. Current gate — M3-2 only

M3 is active. M3-1 is closed/validated. Next bounded gate:

> **M3-2 — Adaptive Candidate Resolver**

Conceptual path:

```text
meaningful available application projections
+ current composition config
+ bounded ranking inputs
        ↓
M3-2 resolver
        ↓
WorldFocusCompositionCandidate[]
        ↓
existing composition planner
```

M3-2 must not:

```text
manufacture missing Output Grammar content
mount a renderer merely because it exists
use AI relevance alone as ranking authority
collapse evidence/freshness/etc into universal confidence
silently override stable/pinned user intent
perform AuthZ
introduce backend persistence
start Customize UI
start DANTE D2–D6
```

M3-2 has not started and requires a fresh write gate.

# 11. Stop lines

```text
M3-2 adaptive candidate resolver             NEXT
M3-3 manual Customize UX                     BLOCKED BY M3-2
M3-4 integrated adaptive composition         BLOCKED BY M3-3
M3 final falsification                       BLOCKED BY M3-4
M4 D2–D6 contextual DANTE                    BLOCKED BY M3
M5 complete contrasting Worlds               BLOCKED BY M4
M6 integrated visual/a11y/performance review BLOCKED BY M5
M7 pre-backend frontend freeze               BLOCKED BY M6
BACKEND                                      BLOCKED UNTIL M7
```

# 12. Backend stop line

```text
NO World DB/Alembic
NO real World API merely for demos
NO real AuthZ/provider runtime
NO localStorage fake durable config
NO server persistence/cross-device sync
NO real model routing/streaming
NO durable DANTE Run backend
NO real tool/effect execution
NO fake success
```

# 13. Immediate continuation

> **Start only M3-2 from a fresh explicit write gate. Do not start M3-3, M4/DANTE or backend work automatically.**
