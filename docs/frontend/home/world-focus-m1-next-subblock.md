# DANTE — World Focus M1-2 Execution Scope / Closure Record

**Status:** M1-2 CLOSED / VALIDATED — HISTORICAL EXECUTION SCOPE  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`

This document was the frozen execution scope after M1-1. It is now retained as the M1-2 closure record. It is no longer the live next gate; M2 is next.

## 1. Frozen objective — completed

Materialize the remaining reusable non-visual frontend facets and typed application seams earned by M0 while preserving Domain/backend authority boundaries.

All required model/application work below was completed and validated:

```text
1. reference resolution
   usable / unresolved / retired
   exact reference preserved
   no silent merge/split retarget

2. L2 narrow facets
   freshness / as-of
   validity / superseded / retracted / unresolved
   coverage / incomplete / conflict / unknown
   present/retired exact material-state payload status
   evidence / provenance / integrity-attestation kept distinct

3. L3 sanitized disclosure
   available / restricted / unavailable
   no frontend AuthZ decision
   no recipient/purpose widening

4. L6 effect presentation
   pending / ambiguous / partial-real / reconciliation-required
   reversed / compensated
   execution revalidation state
   no real execution

5. L8 sync/platform presentation
   online/offline
   replay idle/pending
   provider nominal/lagging/unknown
   request within-window/timed-out/unknown
   timeout != semantic negative

6. direct typed Output Grammar seams
   O2 Situation
   O5 Next
   O8 Evidence / History

7. L1 application seams
   WP-01 Continuity strengthened
   WP-02 Attention
   WP-03 Comparison
   WP-04 Trajectory

8. shared mechanics
   World-scoped cancellable validated read boundary
   latest-only read coordination
   deterministic pre-backend adapters
```

## 2. Design constraints — satisfied

M1-2 did **not** create one universal `ProjectionEnvelope` containing every possible field.

It did not create:

```text
generic Thing
Entity root
Fact root
Relationship root
PropertyBag
frontend ACL/AuthZ
World-owned canonical state
backend DTO/persistence owner
provider/LLM/effect runtime
```

Narrow facets compose only where they are semantically needed.

## 3. Production evidence

Primary M1-2 production tranche:

```text
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS
```

This tranche included the non-visual facets, O2/O5/O8 seams, WP-01..04 application alignment, deterministic adapters and shared read mechanics.

## 4. Final hostile closure pressure

Red-first final falsification:

```text
HEAD 67bd06d63d84273ba2077761919d714c8d442254
CI   33740212989 EXPECTED FAILURE
```

Result:

```text
4 final hostile tests
3 PASS
1 FAIL
whole web suite: 1 failed / 288 passed
```

The passing hostile cases demonstrated:

```text
reference/basis/disclosure/sync/effect axes do not collapse
unknown future World supports O2/O5/O8 + WP-01..04 without DANTE
same-generation wrong-World late surface remains rejected
```

The sole failure proved the transitional M1-1 cursor representation was still hidden from normal object shape:

```text
contextReferences type = canonical
contextReferences runtime property = non-enumerable
```

Final fix and validation:

```text
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS
```

The cursor now exposes `contextReferences` as a normal enumerable frozen property. `selection` remains only a compatibility projection of primary.

## 5. Test pressure disposition

Required pressure is closed:

```text
current vs stale                         COVERED
superseded/retracted vs freshness        COVERED
partial/conflicted/missing evidence      COVERED
retired material/reference continuity    COVERED
usable/unresolved/retired reference      COVERED
available/restricted/unavailable         COVERED
offline/replay/provider lag/timeout      COVERED
pending/ambiguous/partial-real effect     COVERED
execution revalidation                   COVERED
unknown future World                     COVERED
useful path without DANTE                COVERED
wrong-World/stale generation guards       COVERED
cursor canonical context shape           COVERED RED→GREEN
```

WS7/WS8 remained proof/falsification references only; the oracle was not promoted to production authority.

## 6. Explicitly still out of scope

```text
M2 renderers/cards/charts
M3 pin/hide/reorder/customization
M4 D2–D6
M5 complete Worlds
M6 integrated visual review
M7 frontend freeze
backend/API/DB/Alembic/AuthZ/provider/LLM/tools/effects
```

## 7. Closure rule — satisfied

```text
implementation                         PASS
focused tests                          PASS
red-first final falsification          PASS as method; expected red discovered
root-cause fix                         PASS
typecheck/lint/architecture/unit/build PASS
Chromium                               PASS
Firefox frozen Timeline                PASS
Mobile                                 PASS
Frontend CI Gate                       PASS
exact validated code HEAD recorded     PASS
live docs synchronized                 THIS CLOSURE COMMIT
```

## 8. Final disposition

```text
M1-2 CLOSED / VALIDATED
M1   CLOSED / VALIDATED
M2   NEXT
```

> **This file is now closure evidence, not an instruction to continue M1-2.**
