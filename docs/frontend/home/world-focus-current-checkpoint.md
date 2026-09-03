# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M2 ACTIVE / M2-1 + M2-2 CLOSED / VALIDATED  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Older `D2 NEXT`, `M0 NEXT`, `M1 ACTIVE`, `M1-2 NEXT`, `POST-M1 SAFETY ACTIVE`, `M2 NEXT`, `M2-1 NEXT` or similar prose is phase-time history only.

# 1. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m2-shared-visual-primitives.md
3. world-focus-post-m1-safety-falsification-review.md
4. world-focus-m1-core-nonvisual-materialization-review.md
5. world-focus-m1-next-subblock.md
6. world-focus-m0-materialization-mapping.md
7. world-focus-contract-sequencing-supersession.md
8. world-focus-pre-m0-falsification-review.md
9. world-focus-post-ws8-hygiene-audit.md
10. world-focus-substrate-closure-plan.md
11. world-focus-frontend-roadmap.md
12. world-focus-handoff.md
13. world-focus-evidence-index.md
14. WS7/WS8/WS6 evidence as needed
15. product/platform/structure/geometry contracts as needed
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
M1-1 identity/reference ownership     CLOSED / VALIDATED
M1-2 non-visual facets + seams        CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION          CLOSED / PASS
M2 shared visual primitive layer      ACTIVE
M2-1 shared presentation/L1 renderers CLOSED / VALIDATED
M2-2 truthfulness/direct output       CLOSED / VALIDATED
M2 FINAL CLOSURE AUDIT                NEXT
M3–M7                                 BLOCKED BY SEQUENCE
D2–D6                                 DEFERRED TO M4
BACKEND                               BLOCKED UNTIL M7
assistant manual visual review         NOT PERFORMED
```

# 3. Evidence anchors

```text
WS8 semantic proof/runtime
HEAD 88db899391a3a41e23e76177d4896a657232b5eb
CI   33639741630 PASS

PRE-M0 adversarial fix
HEAD 7c9feab50c6e2a04a9a3b1e36c92958362dba704
CI   33664655614 PASS

M0 closure docs
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1-1 production identity/reference
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 production non-visual semantics
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final red-first falsification
HEAD 67bd06d63d84273ba2077761919d714c8d442254
CI   33740212989 EXPECTED FAILURE

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety red-first falsification
HEAD 0b674effa292881303288dd90c88db2c14e61872
CI   33747167897 FAIL

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS

M2-1 shared visual primitive validation
HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI   33781753823 PASS
61 / 61 web test files; 312 / 312 web unit tests
262 modules / 684 dependencies / 0 violations
Continuity pressure at 720 / 719 / 390 PASS in Chromium
frozen Timeline Firefox PASS

M2-2 red-first owner proof
HEAD 5374f77d7cf7b52ef87ce64315a606bc1d96cf0b
CI   33787162755 EXPECTED FAILURE
exactly 8 unresolved M2-2 presentation owners at Typecheck

M2-2 production baseline
HEAD b9856d497273d22face94fcd14f0deda853bbdb8
CI   33787905171 PASS

M2-2 final integration validation
HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5
CI   33788370490 PASS
Quality / Chromium / frozen Timeline Firefox / Mobile / Frontend CI Gate PASS
```

# 4. Closed non-visual production result

Production identity remains open-ended and descriptor-driven while routability remains explicit. The deterministic fixture catalog is not a permanent World taxonomy.

Canonical transient interaction context is:

```text
WorldFocusContextReferenceSet
  primary
  ordered bounded supporting[]
```

Workspace and interaction cursor expose this canonical set normally. `selection` remains a compatibility projection of primary only. Surfaces inherit primary only by default so supporting context is never silently widened.

M1 materialized narrow, orthogonal production semantics:

```text
reference resolution
  usable / unresolved / retired

L2
  freshness current/stale/unknown + as-of where known
  validity current/superseded/retracted/unresolved
  coverage complete/incomplete/conflicted/unknown
  exact material-state payload present/retired
  evidence / provenance / integrity-attestation roles kept distinct

L3
  sanitized disclosure available/restricted/unavailable

L6
  pending / ambiguous / partial-real / reconciliation-required / reversed / compensated
  execution revalidation not-required / required-before-execution

L8
  online/offline
  replay idle/pending
  provider nominal/lagging/unknown
  request within-window/timed-out/unknown

Output Grammar seams
  O2 Situation
  O5 Next
  O8 Evidence / History

L1 application seams
  WP-01 Continuity
  WP-02 Attention
  WP-03 Comparison
  WP-04 Trajectory
```

The shared read foundation owns only cancellation/latest-read/boundary-validation mechanics. It is not a universal semantic envelope or backend authority.

# 5. Post-M1 safety result

The bounded safety gate preserved the hostile test and found two real production defects:

```text
A. cancelled non-cooperative World read
   late adapter completion could still reach validation

B. O8 evidence snapshot ownership
   caller-provided evidence facet could remain aliased
```

Both were fixed under existing owners. No new semantic class, substrate layer, DB authority or M1 reopen was required.

# 6. M2-1 validated result

M2-1 owns only the presentation boundary and shared L1 renderer grammar earned by M1:

```text
WorldFocusDisplayBinding
  exact semantic reference match
  bounded display-safe label/supporting text
  no raw reference-key fallback

shared presentation primitives
  semantic section + heading ownership
  textual state treatment
  existing DANTE tokens
  container-query responsive behavior
  forced-colors support

finite L1 renderers
  WP-02 Attention
  WP-03 Comparison
  WP-04 Trajectory

real vertical integration
  WP-01 Continuity migrated to shared M2 grammar
```

WP-02..WP-04 are production renderer contracts and are tested directly against M1 primitives, but they are not inserted into live World composition simply to demonstrate them.

# 7. M2-2 validated result

M2-2 reuses the M2-1 display/presentation grammar to materialize the remaining mapped shared truthfulness/direct-output rendering:

```text
WorldFocusQualifier / WorldFocusQualifierGroup
WorldFocusPresentationSubsection

L2
  freshness / validity / coverage / material-payload retirement

L3
  disclosure available/restricted/unavailable

L6
  effect lifecycle + execution revalidation

L8
  connectivity / replay / provider delivery / request timing

O2 Situation
O5 Next
O8 Evidence / History
```

The O2/O5/O8 renderers require exact `WorldFocusDisplayBinding` ownership and preserve semantic order. O8 keeps Evidence, Provenance, integrity-attestation and History as separate accessible roles.

Nominal basis/disclosure/sync states remain quiet. Degraded states use visible textual qualifiers and do not rely on color alone.

Continuity integrates the same qualifier grammar only for states it already owns:

```text
partial -> coverage / incomplete
stale   -> freshness / stale
```

No `reasonCode`, protected provider/policy detail or raw reference key becomes display copy.

# 8. Permanent non-collapses retained

```text
reference exists != payload available != current != disclosable != fresh
stale != superseded != retracted
Evidence != Provenance != integrity attestation
restricted != nonexistent
available disclosure != frontend authorization
offline != source absent
provider lag != canonical stale
timeout != semantic negative
partial-real effect != generic failure != success
cancel != reverse != compensate
reversed != compensated
execution revalidation != effect state
Comparison != Decision
missing trajectory position != zero
World relevance != AuthZ
AI output != fact
```

No universal `ProjectionEnvelope`, generic `Thing/Entity/Fact/PropertyBag`, frontend ACL/AuthZ, World-owned canonical state, universal `Card<T>` renderer or backend owner was introduced.

# 9. M0 M2-disposition audit

Known shared visual dispositions assigned to M2 now have concrete production owners:

```text
M0-19 WP-02 shared rendering                  DONE / M2-1
M0-21 WP-03 shared rendering                  DONE / M2-1
M0-23 WP-04 shared rendering                  DONE / M2-1
M0-28 shared Evidence / History affordance    DONE / M2-2
M0-42 shared effect presentation              DONE / M2-2
M0-49 WP shared renderer family               DONE / M2-1

O2 Situation visual presentation              DONE / M2-2
O5 Next visual presentation                   DONE / M2-2
O8 Evidence / History visual presentation     DONE / M2-2
L2/L3/L6/L8 truthfulness presentation         DONE / M2-2
```

This does not itself close M2; it establishes that a final falsification may now test closure instead of materializing another arbitrary renderer family.

# 10. Current gate — M2 final closure audit

M2 remains active. The next bounded gate is a hostile closure audit/falsification over the combined M2-1/M2-2 production layer.

It must pressure at least:

```text
cross-axis visual non-collapse
unknown future World
exact binding/fail-closed behavior
reasonCode/reference-key non-leakage
nominal-state quietness
sparse/no-fake-live composition
long-copy and compact responsive safety
forced-colors/textual-state semantics
finite renderer registry boundaries
no universal card/envelope emergence
no M3 customization pulled forward
```

Only real executable PASS may advance to M3.

# 11. Stop lines

```text
M2 FINAL CLOSURE AUDIT                     NEXT
M3 adaptive composition/customization      BLOCKED BY M2
M4 D2–D6 contextual DANTE                  BLOCKED BY M3
M5 complete contrasting Worlds             BLOCKED BY M4
M6 integrated visual/a11y/performance      BLOCKED BY M5
M7 pre-backend frontend freeze             BLOCKED BY M6
BACKEND                                    BLOCKED UNTIL M7
```

# 12. Contract sequencing

`world-focus-product-contract.md` and `world-focus-platform-contract.md` retain semantic authority. Historical next-gate wording is superseded only for sequencing by this live checkpoint and `world-focus-contract-sequencing-supersession.md`.

# 13. Immediate continuation

> **Run the final M2 closure audit/falsification only. Do not start M3, D2–D6/M4 or backend work unless M2 is actually closed by executable evidence.**
