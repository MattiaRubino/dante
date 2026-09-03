# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M2 ACTIVE / M2-1 CLOSED / VALIDATED  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Older `D2 NEXT`, `M0 NEXT`, `M1 ACTIVE`, `M1-2 NEXT`, `POST-M1 SAFETY ACTIVE`, `M2 NEXT` or similar prose is phase-time history only.

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
M2-1 shared presentation/renderers    CLOSED / VALIDATED
M2 remaining visual work              NEXT WITHIN M2
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
1 failed / 288 passed — cursor contextReferences hidden representation

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

POST-M1 safety red-first falsification
HEAD 0b674effa292881303288dd90c88db2c14e61872
CI   33747167897 FAIL
7 / 9 hostile tests PASS; 296 PASS / 2 FAIL overall web units

POST-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS
9 / 9 hostile tests PASS; 56 / 56 web test files; 301 / 301 web unit tests

M2-1 shared visual primitive validation
HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI   33781753823 PASS
61 / 61 web test files; 312 / 312 web unit tests
262 modules / 684 dependencies / 0 violations
Continuity pressure at 720 / 719 / 390 PASS in Chromium
frozen Timeline Firefox PASS
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

Both were fixed under existing owners:

```text
shared read boundary
  reject aborted result before validation, including late non-cooperative completion

O8 Evidence/History seam
  rebuild through existing L2 evidence creator
  own normalized frozen evidence snapshot
```

No new semantic class, substrate layer, DB authority or M1 reopen was required.

# 6. M2-1 validated result

M2-1 now owns only the presentation boundary and shared renderer grammar earned by M1:

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

Truthfulness retained:

```text
reasonCode != user-facing explanation
Comparison != winner/ranking/recommendation/Decision
Trajectory missing != zero/false/inferred value
renderer availability != live composition selection
responsive presentation != semantic rewrite
```

WP-02..WP-04 are production renderer contracts and are tested directly against M1 primitives, but they are not inserted into live World composition simply to demonstrate them. Continuity remains the real live vertical proving the M2 grammar.

# 7. Permanent non-collapses retained

```text
reference exists != payload available != current != disclosable != fresh
stale != superseded != retracted
Evidence != Provenance != integrity attestation
restricted != nonexistent
offline != source absent
provider lag != canonical stale
timeout != semantic negative
partial-real effect != generic failure != success
cancel != reverse != compensate
Comparison != Decision
missing trajectory position != zero
World relevance != AuthZ
AI output != fact
```

No universal `ProjectionEnvelope`, generic `Thing/Entity/Fact/PropertyBag`, frontend ACL/AuthZ, World-owned canonical state, universal Card<T> renderer or backend owner was introduced.

# 8. Current gate — continue M2

M2 remains active after M2-1. The next bounded visual slice must reuse the validated display/presentation grammar and materialize only semantics actually justified by M1/product evidence.

Constraints:

```text
primitive != card
renderer != semantic owner
Output Grammar family != mandatory module
finite renderer registry
safe degradation for unknown future Worlds
no fabricated urgency or density
no visual collapse of semantic axes
no fake mounting of WP-02..04 merely because renderers exist
no M3 customization yet
no D2–D6 yet
no backend yet
```

# 9. Stop lines

```text
M2 remaining shared visual work               NEXT WITHIN M2
M3 adaptive composition/customization         BLOCKED BY M2
M4 D2–D6 contextual DANTE                     BLOCKED BY M3
M5 complete contrasting Worlds                BLOCKED BY M4
M6 integrated visual/a11y/performance review  BLOCKED BY M5
M7 pre-backend frontend freeze                BLOCKED BY M6
BACKEND                                       BLOCKED UNTIL M7
```

# 10. Contract sequencing

`world-focus-product-contract.md` and `world-focus-platform-contract.md` retain semantic authority. Historical next-gate wording is superseded only for sequencing by the live checkpoint and `world-focus-contract-sequencing-supersession.md`.

# 11. Immediate continuation

> **Continue M2 only. Reuse the validated M2-1 display/presentation layer and materialize the next bounded visual semantics without starting M3, D2–D6/M4 or backend work.**
