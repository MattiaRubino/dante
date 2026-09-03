# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — WORLD FOCUS M1 CLOSED / M2 NEXT  
**Date:** 2026-09-03  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This is the branch-level live entry point. Do not reconstruct current state from older phase labels or chat summaries.

## 1. Branch workstreams

```text
APP SHELL / HOME
TEMPORAL / TIMELINE
WORLD FOCUS
```

Permanent distinctions:

```text
Home AI != World contextual DANTE
Home Timeline != full temporal workspace
World Focus != Home overlay
Mondi Overview != World Focus
```

## 2. Live World Focus state

```text
WF0 route/shell                         FROZEN / USER AUTHORIZED
WF-G3 geometry                         LOCKED / USER AUTHORIZED
WF-V4 visual treatment                 CANDIDATE
B0 foundation                          ENGINEERING CLOSED
WR0–WR2                                CLOSED
B1 Orientation                         CLOSED FOR SEQUENCING
B2 Continuity / Resume                 IMPLEMENTED / AUTOMATED PASS
Workspace Platform                     ENGINEERING CLOSED
D0 contextual DANTE spatial contract   ACCEPTED
D1 quiet invoke + compact composer      CLOSED FOR SEQUENCING
WS0–WS8                                CLOSED
POST-WS8 HYGIENE                       CLOSED / APPLIED
PRE-M0 FALSIFICATION                   CLOSED / PASS
M0 Materialization Mapping             CLOSED
M1 Core Non-Visual Materialization     CLOSED / VALIDATED
M1-1 identity/reference ownership      CLOSED / VALIDATED
M1-2 facets + WP/O2/O5/O8 seams        CLOSED / VALIDATED
M2 Shared Visual Primitive Layer       NEXT
M3–M7                                  BLOCKED BY SEQUENCE
D2–D6                                  DEFERRED TO M4
BACKEND                                BLOCKED UNTIL M7
assistant manual visual review         NOT PERFORMED
```

## 3. Current validated evidence

```text
M0 docs closure
HEAD 6ea74f630cb35af65d58e7ae873882d6d975411e
CI   33668744509 PASS

M1-1 production identity/reference
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 non-visual production materialization
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final production falsification — red discovery
HEAD 67bd06d63d84273ba2077761919d714c8d442254
CI   33740212989 EXPECTED FAILURE
1 failed / 288 passed — hidden cursor contextReferences representation only

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS
```

## 4. M1 closed result

M1 now has production-grade non-visual ownership for:

```text
open-ended World identity + explicit descriptor
neutral bounded context-reference sets
canonical workspace/cursor context
reference resolution: usable / unresolved / retired
freshness/as-of
validity: current / superseded / retracted / unresolved
coverage: complete / incomplete / conflicted / unknown
material payload: present / retired with exact material-state reference
evidence / provenance / integrity-attestation as distinct bounded roles
sanitized disclosure: available / restricted / unavailable
effect presentation + execution revalidation
connectivity / replay / provider delivery / request timing
O2 Situation
O5 Next
O8 Evidence / History
WP-01 Continuity
WP-02 Attention
WP-03 Comparison
WP-04 Trajectory
World-scoped validated/cancellable read mechanics
deterministic pre-backend adapters
unknown-future World compatibility
basic useful path without DANTE
```

The final M1 falsification proved the only remaining compatibility debt was the non-enumerable `cursor.contextReferences`. It is now a normal enumerable frozen property. `selection` remains only a compatibility projection of `contextReferences.primary`, not the semantic owner.

No universal `ProjectionEnvelope`, generic `Thing/Entity/Fact/PropertyBag`, frontend ACL/AuthZ, World canonical ownership or backend authority was introduced.

## 5. Read order

```text
1. world-focus-current-checkpoint.md
2. world-focus-m1-core-nonvisual-materialization-review.md
3. world-focus-m1-next-subblock.md
4. world-focus-m0-materialization-mapping.md
5. world-focus-contract-sequencing-supersession.md
6. world-focus-frontend-roadmap.md
7. world-focus-handoff.md
8. world-focus-evidence-index.md
9. world-focus-substrate-closure-plan.md
10. product/platform/structure/geometry contracts as needed
```

## 6. Next gate — M2 only

M2 materializes the **shared visual primitive layer** for semantics already earned by M1.

Rules:

```text
primitive != card
question/output family != mandatory visible module
no page-per-World architecture
no renderer may become canonical semantic owner
no visual treatment may collapse freshness/validity/disclosure/effect/sync axes
unknown future Worlds must safe-degrade through finite registries
sparse Worlds remain sparse
```

M3 adaptive customization, M4 contextual DANTE D2–D6, M5 complete Worlds, M6 integrated visual/a11y/performance review, M7 frontend freeze and backend all remain blocked by sequence.

## 7. Permanent barriers

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
derived output != disclosure permission
AI output != accepted fact
Proposal != Decision != effect
provider ACK != canonical completion
absence/unknown != false
Evidence != Provenance
Provenance != integrity attestation
Authority != Visibility
timeout != semantic negative
offline != source absent
retired reference != replacement reference
```

## 8. Backend stop line

```text
frontend view model != backend DTO != Domain model != persistence row
NO World DB/Alembic
NO real business API merely for frontend completeness
NO real AuthZ/provider runtime
NO real LLM routing/streaming
NO durable DANTE Run backend
NO real tool/effect execution
NO fake success
```

## 9. Operational rules

- stay on `feature/home-react` unless explicitly authorized otherwise;
- fresh live HEAD before every write scope;
- no merge/rebase/force/history rewrite/main mutation without explicit authorization;
- do not modify Access/Auth, frozen Timeline or AppShell as collateral work;
- generated route tree is never manually edited;
- fix CI root causes rather than weaken tests;
- human visual review is recorded only when actually performed.
