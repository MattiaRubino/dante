# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — WS0–WS8 / M0 / M1 / POST-M1 SAFETY / M2 CLOSED — M3 ACTIVE / M3-1 VALIDATED / M3-2 NEXT  
**Date:** 2026-09-04  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

Read in order:

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
12. world-focus-ws8-final-falsification-review.md
13. world-focus-ws7-executable-harness-review.md
14. world-focus-ws6-universal-work-primitives.md
15. world-focus-ws6-primitive-pressure-matrix.md
16. world-focus-substrate-final-convergence-proof.md
17. world-focus-substrate-combinatorial-evidence.md
18. world-focus-frontend-roadmap.md
19. world-focus-evidence-index.md
20. product/platform/structure/geometry contracts as needed
```

Older `NEXT` or `ACTIVE` prose is phase-time evidence only unless adopted by a newer live authority.

---

# 1. Current status

```text
WF0 route/shell                          FROZEN / USER AUTHORIZED
WF-G3 geometry                          LOCKED / USER AUTHORIZED
WF-V4 visual treatment                  CANDIDATE
B0 foundation                           ENGINEERING CLOSED
WR0–WR2                                 CLOSED
B1 Orientation                          CLOSED FOR SEQUENCING
B2 Continuity / Resume                  IMPLEMENTED / AUTOMATED PASS
Workspace Platform                      ENGINEERING CLOSED
D0 DANTE spatial/presence               ACCEPTED
D1 quiet invoke/composer                CLOSED FOR SEQUENCING
WS0–WS8                                 CLOSED
POST-WS8 HYGIENE                        CLOSED / APPLIED
PRE-M0 FALSIFICATION                    CLOSED / PASS
M0 Materialization Mapping              CLOSED
M1 Core Non-Visual Materialization      CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION            CLOSED / PASS
M2 shared visual primitive layer        CLOSED / VALIDATED
M2 FINAL HOSTILE CLOSURE                CLOSED / PASS
M3 Adaptive World Composition           ACTIVE
M3-1 composition configuration foundation CLOSED / VALIDATED
M3-2 adaptive candidate resolver        NEXT
M4–M7                                   BLOCKED BY SEQUENCE
BACKEND                                 BLOCKED UNTIL M7
D2–D6                                   PRESERVED / DEFERRED TO M4
assistant manual visual review          NOT PERFORMED
```

Key executable evidence:

```text
WS8
HEAD 88db899391a3a41e23e76177d4896a657232b5eb
CI   33639741630 PASS

M0 closure
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS

M2-1 validation
HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI   33781753823 PASS

M2-2 final integration validation
HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5
CI   33788370490 PASS

M2 final hostile closure
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS
70 / 70 web test files; 332 / 332 web unit tests
279 modules / 770 dependencies / 0 architecture violations

M3-1 red
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE
pre-production contracts PASS; unresolved M3-1 owner modules caused the expected Quality failure

M3-1 validation
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
72 / 72 web test files; 344 / 344 web unit tests
283 modules / 777 dependencies / 0 architecture violations
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS
```

---

# 2. Product compass

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

Core thesis:

> **World is a shared coordinate system between user and DANTE, not a shared source of truth.**

World is not a Domain owner, folder, life taxonomy, DB partition, permission boundary, AI memory bucket, chat room, mandatory Goal/time/KPI surface or dashboard ontology.

---

# 3. Output Grammar and substrate

```text
O1 Orientation
O2 Situation
O3 Continuity / Resume
O4 Attention / Resolution
O5 Next
O6 Change
O7 Trajectory / Comparison
O8 Evidence / History
O9 Explore
O10 Act / Decide
O11 Intelligence
```

Output Grammar families are product questions, not automatically primitives/modules/renderers.

Finite L1 remains:

```text
WP-01 Continuity
WP-02 Attention
WP-03 Comparison
WP-04 Trajectory
```

Permanent non-collapses include:

```text
Person != Account != Principal != Actor
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Authority != Visibility
Proposal != Decision != effect
provider state != canonical state
reference exists != payload available != current != disclosable != fresh
stale != superseded != retracted
timeout != semantic negative
offline != source absent
Comparison != Decision
missing trajectory position != zero
```

No generic Entity/Thing/Relationship/Fact/property-bag root.

---

# 4. Closed M1/M2 result retained

M1 owns the non-visual production semantics/application seams. M2 owns bounded presentation and finite renderer vocabulary. M3 consumes both and does not reopen them.

M2 closure still guarantees:

```text
bounded display-safe reference binding
WP-01..04 rendering ownership
O2/O5/O8 presentation
truthfulness/disclosure/effect/sync presentation
nominal-state quietness
no raw reference/reasonCode leakage
no fake live module mounting
```

---

# 5. Existing composition engine retained

Reuse remains:

```text
stable/adaptive/ephemeral composition
finite module/surface registries
12-unit planner
workspace generation
surface stack/allocation
local failure isolation
container-query ownership
```

The planner already preserves stable relative order and bounds adaptive/ephemeral entries. M3 must feed this planner rather than replacing it.

The live core composition still mounts Continuity only. M3-1 does not alter live composition.

---

# 6. M3-1 production foundation

M3-1 introduces two production owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Config snapshot:

```text
schemaVersion
revision
worldId
ordered entries
```

Entry metadata:

```text
instanceId
kind
visibility
pinned
prominenceOverride
```

No canonical Domain payload, AuthZ/disclosure authority, provider/runtime truth, executable renderer code or arbitrary property bag is retained.

Version disposition:

```text
current
migration-required
unsupported
```

No automatic migration and no persistence are fabricated.

---

# 7. Customization command/draft semantics

Finite commands:

```text
pin
unpin
hide
show
move
promote
restore
```

Finite sources:

```text
manual
dante-proposed
```

Transaction:

```text
CURRENT revision N
  ↓
DRAFT(baseRevision=N)
  ↓
commands
  ↓
Apply | Cancel
```

Apply is the only operation that creates revision `N+1`. Stale revision returns `revision-conflict`; cross-World Apply fails closed; no implicit merge occurs. Cancel returns the base snapshot.

`hide != delete`, `pin != canonical truth`, and `promote != semantic truth`.

---

# 8. Permanent manual / DANTE capability rule

DANTE is an intelligence/acceleration layer over the product, not the only control surface.

Permanent rule:

> Canonical app capabilities that DANTE can propose or accelerate must remain usable through a manual/non-AI path where they are meaningful application functions.

M3-1 makes this executable for composition customization:

```text
manual UI [M3-3] ----\
                       -> same finite commands -> DRAFT -> REVIEW/APPLY
DANTE proposal [M4] --/
```

A DANTE proposal cannot bypass Apply/revision guards or mutate configuration through a hidden side channel.

---

# 9. Current M3 handoff

M0 remains the production-disposition authority.

Current L5 disposition:

```text
M0-35 stability/origin                         existing / preserve
M0-36 prominence/footprint/grid planner        existing / preserve
M0-37 candidate resolver                       M3-2 NEXT
M0-38 Draft/Apply/Cancel + commands            M3-1 foundation CLOSED; manual UX M3-3
M0-39 revision/conflict/migration representation M3-1 CLOSED / VALIDATED
M0-40 durable persistence/sync/conflict        backend-deferred
```

M3-2 must resolve meaningful bounded candidates from already-authorized application projections plus current composition config and feed the existing planner.

Hard rejects:

```text
AI relevance score alone decides layout
universal confidence score
renderer availability forces mounting
missing content is fabricated to fill the World
adaptive logic silently overrides stable/pinned user intent
candidate resolver becomes AuthZ
```

Sparse Worlds remain sparse.

---

# 10. M3-1 explicit non-work

```text
NO candidate resolver/ranking
NO Customize UI / drag/drop
NO localStorage fake persistence
NO server persistence/cross-device sync
NO new live renderer mounting
NO DANTE D2–D6 runtime work
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral changes
```

---

# 11. Backend / future vertical stop line

Backend remains blocked until M7.

When frontend sequencing is closed, the future real vertical can integrate through proper authority:

```text
UI
→ application
→ Access/Auth/AuthZ
→ API
→ Domain
→ PostgreSQL
```

Client composition config must never be promoted directly into Domain or persistence truth.

---

# 12. Strict reopen policy

Do not restart WS0–WS8, M1 or M2 for a new provider, World noun, renderer, viewport, AI model, config store or larger dataset.

Reopen only when later executable evidence shows a concrete contradiction that cannot fit an existing owner, and reopen only the earliest necessary phase.

---

# 13. Repository discipline

Authority order:

```text
protected-main accepted executable/docs
current main authority
active bounded branch record for its scope
other current branch evidence
Git history
conversation
```

Every new write scope needs exact branch/PRE-SCOPE/path gate and live HEAD recheck. No merge/rebase/force/main mutation without explicit authorization.

Immediate continuation:

> **M3-2 is NEXT but unstarted. Start only with a fresh bounded M3-2 gate. M3-3, M4–M7 and backend remain blocked by sequence.**
