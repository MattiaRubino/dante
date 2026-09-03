# DANTE — World Focus Current Checkpoint

**Status:** CURRENT LIVE WORLD FOCUS CHECKPOINT — M1 CLOSED / M2 NEXT  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the first World Focus authority a new chat/agent must read. Older `D2 NEXT`, `M0 NEXT`, `M1 ACTIVE`, `M1-2 NEXT` or similar prose is phase-time history only.

# 1. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m1-core-nonvisual-materialization-review.md
3. world-focus-m1-next-subblock.md
4. world-focus-m0-materialization-mapping.md
5. world-focus-contract-sequencing-supersession.md
6. world-focus-pre-m0-falsification-review.md
7. world-focus-post-ws8-hygiene-audit.md
8. world-focus-substrate-closure-plan.md
9. world-focus-frontend-roadmap.md
10. world-focus-handoff.md
11. world-focus-evidence-index.md
12. WS7/WS8/WS6 evidence as needed
13. product/platform/structure/geometry contracts as needed
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
M2 shared visual primitive layer      NEXT
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
```

# 4. M1 closed production result

Production identity remains open-ended and descriptor-driven while routability remains explicit. The current deterministic fixture catalog is not a permanent World taxonomy.

Canonical transient interaction context is:

```text
WorldFocusContextReferenceSet
  primary
  ordered bounded supporting[]
```

Workspace and interaction cursor now expose this canonical set normally. `selection` remains a compatibility projection of primary only. Surfaces inherit primary only by default so supporting context is never silently widened.

M1-2 also materialized narrow, orthogonal production semantics:

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

# 5. Final M1 falsification result

The final hostile production test deliberately combined unknown-future World handling, bounded context, cross-axis facets, O2/O5/O8, WP-01..04, same-generation wrong-World rejection and a useful non-DANTE path.

The red run found exactly one remaining issue:

```text
cursor type said contextReferences was canonical
runtime hid it as a non-enumerable compatibility property
```

The other hostile cases passed. The fix removed the `Object.defineProperty(... enumerable: false)` representation and returns a normal frozen `contextReferences` property. Exact-shape tests were migrated rather than weakening the canonical cursor.

# 6. Permanent non-collapses retained

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

No universal `ProjectionEnvelope`, generic `Thing/Entity/Fact/PropertyBag`, frontend ACL/AuthZ, World-owned canonical state or backend owner was introduced.

# 7. Next gate — M2

M2 may now build shared visual primitives over M1 semantics.

Constraints:

```text
primitive != card
renderer != semantic owner
Output Grammar family != mandatory module
finite renderer registry
safe degradation for unknown future Worlds
no fabricated urgency or density
no visual collapse of semantic axes
no M3 customization yet
no D2–D6 yet
no backend yet
```

# 8. Stop lines

```text
M2 shared visual renderer layer              NEXT
M3 adaptive composition/customization        BLOCKED BY M2
M4 D2–D6 contextual DANTE                    BLOCKED BY M3
M5 complete contrasting Worlds               BLOCKED BY M4
M6 integrated visual/a11y/performance review BLOCKED BY M5
M7 pre-backend frontend freeze               BLOCKED BY M6
BACKEND                                      BLOCKED UNTIL M7
```

# 9. Contract sequencing

`world-focus-product-contract.md` and `world-focus-platform-contract.md` retain semantic authority. Historical next-gate wording is superseded only for sequencing by the live checkpoint and `world-focus-contract-sequencing-supersession.md`.

# 10. Immediate continuation

> **Begin M2 only: materialize the shared visual primitive layer over the closed M1 semantics. Do not start M3, D2–D6/M4 or backend work.**
