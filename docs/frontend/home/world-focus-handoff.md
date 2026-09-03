# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — WS0–WS8 / M0 / M1 / POST-M1 SAFETY CLOSED — M2 NEXT  
**Date:** 2026-09-03  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

Read in order:

```text
1. world-focus-current-checkpoint.md
2. world-focus-post-m1-safety-falsification-review.md
3. world-focus-m1-core-nonvisual-materialization-review.md
4. world-focus-m1-next-subblock.md
5. world-focus-m0-materialization-mapping.md
6. world-focus-contract-sequencing-supersession.md
7. world-focus-pre-m0-falsification-review.md
8. world-focus-post-ws8-hygiene-audit.md
9. world-focus-substrate-closure-plan.md
10. world-focus-ws8-final-falsification-review.md
11. world-focus-ws7-executable-harness-review.md
12. world-focus-ws6-universal-work-primitives.md
13. world-focus-ws6-primitive-pressure-matrix.md
14. world-focus-substrate-final-convergence-proof.md
15. world-focus-substrate-combinatorial-evidence.md
16. world-focus-frontend-roadmap.md
17. world-focus-evidence-index.md
18. product/platform/structure/geometry contracts as needed
```

Older `NEXT` or `ACTIVE` prose is phase-time evidence only unless adopted by a newer live authority.

---

# 1. Current status

```text
WF0 route/shell                         FROZEN / USER AUTHORIZED
WF-G3 geometry                         LOCKED / USER AUTHORIZED
WF-V4 visual treatment                 CANDIDATE
B0 foundation                          ENGINEERING CLOSED
WR0–WR2                                CLOSED
B1 Orientation                         CLOSED FOR SEQUENCING
B2 Continuity / Resume                 IMPLEMENTED / AUTOMATED PASS
Workspace Platform                     ENGINEERING CLOSED
D0 DANTE spatial/presence              ACCEPTED
D1 quiet invoke/composer               CLOSED FOR SEQUENCING
WS0–WS8                                CLOSED
POST-WS8 HYGIENE                       CLOSED / APPLIED
PRE-M0 FALSIFICATION                   CLOSED / PASS
M0 Materialization Mapping             CLOSED
M1 Core Non-Visual Materialization     CLOSED / VALIDATED
M1-1 identity/reference ownership      CLOSED / VALIDATED
M1-2 non-visual facets + seams         CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION           CLOSED / PASS
M2 shared visual primitive layer       NEXT
M3–M7                                  BLOCKED BY SEQUENCE
BACKEND                                BLOCKED UNTIL M7
D2–D6                                  PRESERVED / DEFERRED TO M4
```

Key executable evidence:

```text
WS8
HEAD 88db899391a3a41e23e76177d4896a657232b5eb
CI   33639741630 PASS

PRE-M0 fix
HEAD 7c9feab50c6e2a04a9a3b1e36c92958362dba704
CI   33664655614 PASS

M0 closure
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1-1 code
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 code
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final red
HEAD 67bd06d63d84273ba2077761919d714c8d442254
CI   33740212989 EXPECTED FAILURE

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety red
HEAD 0b674effa292881303288dd90c88db2c14e61872
CI   33747167897 FAIL
7 / 9 hostile tests PASS

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS
9 / 9 hostile tests; 56 / 56 web test files; 301 / 301 web unit tests
```

Later documentation synchronization is a separate evidence point and does not replace validated code heads above.

---

# 2. Product compass

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

A World is a user-recognizable continuity context for a significant part of reality.

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

Closed layers:

```text
L0 Higher Authorities
L1 Work-Semantic Projections
L2 Evidence / Basis
L3 Coordination / Disclosure
L4 Interaction / Reference
L5 Composition Configuration
L6 Operation / Effect Presentation
L7 Renderer / Specialist Extension
L8 Platform / User Policies
```

Finite L1:

```text
WP-01 Continuity
WP-02 Attention
WP-03 Comparison
WP-04 Trajectory
```

L1 is optional; direct Domain/application projection may be correct.

---

# 4. Permanent non-collapses

```text
Person != Account != Principal != Actor
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Provenance != integrity attestation
Authority != Visibility
Agreement != Consent
Proposal != Decision != effect
provider state != canonical state
absence/unknown != false
idempotency != semantic identity
reference exists != payload available != current != disclosable != fresh
stale != superseded != retracted
timeout != semantic negative
offline != source absent
```

No generic Entity/Thing/Relationship/Fact/property-bag root.

---

# 5. Retained executable proof

WS7:

```text
HEAD ca89e733893959af7dcc40fd0b8c8ba08e056ba4
CI   33633635890 PASS
67 fixed 3-way rows / 4,455 interactions
157 fixed high-risk 4-way rows / 2,835 interactions
```

WS8:

```text
stateful hostile pressure
mutation-kill
independent post-hardening confirmation
0 unresolved substrate gaps after final hardening
```

Pre-M0 discovered and fixed stale route-origin handoff resurrection without a new substrate owner.

M1 final hostile pressure found only the planned transitional cursor representation residue and closed it red-first.

The post-M1 safety gate then found two additional implementation defects at existing boundaries: cancelled non-cooperative reads could reach validation, and O8 could retain caller evidence aliases. Both were fixed without reopening M1 or WS0–WS8.

---

# 6. Platform + M1 production substrate

Reuse remains:

```text
stable/adaptive/ephemeral composition
finite module/surface registries
12-unit planner
workspace generation
expected-workspace stale guard
surface open/replace/promote/close
blocking-tail barrier
full/split allocation
overlay/focus/inert semantics
ResizeObserver/container-query ownership
local failure isolation
latest-read coordination
boundary validation
safe external URL policy
```

M1 production materialization adds:

```text
neutral production World identity / descriptor
fixture identity separated from production identity
neutral bounded context references
canonical enumerable frozen cursor.contextReferences
selection compatibility projection of primary only
surface primary-only inheritance
reference-resolution presentation
freshness/as-of, validity, coverage, material retirement facets
evidence/provenance/integrity role-preserving metadata
sanitized disclosure outcome
effect lifecycle presentation + execution revalidation
sync/offline/replay/provider lag/request timing axes
O2/O5/O8 direct typed seams
WP-01..WP-04 production/application seams
World-scoped cancellable validated read mechanics
deterministic local adapters
unknown future World support at the non-visual seam
```

Post-M1 hardening strengthens existing ownership only:

```text
aborted read results are rejected before semantic validation
O8 evidence/history owns a normalized frozen evidence snapshot
```

Do not turn proof/oracle-only structures into production owners automatically. A proof seam earns a production review, not necessarily a production type with the same shape.

---

# 7. DANTE disposition

D0 accepted:

> **AI availability is persistent; AI footprint is not.**

D1 global invoke remains `contextReference: null`; no implicit selection leakage.

D2–D6 remain deferred to M4.

DANTE is never truth, authorization, mandatory navigation or automatic effect completion.

M1's useful World path remains functional without DANTE.

---

# 8. M2 handoff

M0 remains the production-disposition authority in `world-focus-m0-materialization-mapping.md`.

M1 is CLOSED / VALIDATED and the bounded post-M1 safety gate is CLOSED / PASS. The next bounded engineering block is:

> **M2 — Shared Visual Primitive Layer.**

M2 renders already-earned semantics. It does not redefine them.

Binding M2 constraints:

```text
primitive != card
renderer != semantic owner
no universal card/module grammar
no page-per-World fork
no hidden semantic inference from visual shape
no fabricated urgency/density
unknown future World safe degradation
responsive changes presentation, not meaning
```

Persistent pin/hide/reorder/customization remains M3. Contextual DANTE D2–D6 remains M4.

---

# 9. Backend stop line

```text
NO World DB/Alembic
NO real World API merely for demos
NO real AuthZ/provider runtime
NO real model routing/streaming
NO durable DANTE Run backend
NO real tool/effect execution
NO fake success
```

---

# 10. Strict reopen policy

Do not restart WS0–WS8 or M1 for a new provider, World noun, renderer, viewport, AI model, config store or larger dataset.

Reopen only when later executable evidence shows a concrete semantic/ownership/state/security/privacy/effect contradiction that cannot fit an existing owner, and reopen only the earliest necessary phase.

---

# 11. Repository discipline

Authority order:

```text
protected-main accepted executable/docs
current main authority
active bounded branch record for its scope
other current branch evidence
Git history
conversation
```

Every write needs exact branch/PRE-SCOPE/path gate and live HEAD recheck. No merge/rebase/force/main mutation without explicit authorization.

Immediate continuation:

> **Proceed with M2 only. M3–M7 and backend remain blocked by sequence.**
