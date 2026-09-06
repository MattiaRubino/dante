# DANTE — World Focus M1 Core Non-Visual Materialization Review

**Status:** M1 CLOSED / VALIDATED — M2 NEXT  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`

This document is the durable M1 execution evidence. M0 remains the scope-freeze/disposition authority; M1 records the production materialization and red-green validation of the non-visual World Focus substrate.

## 1. M0 prerequisite

M0 is CLOSED.

```text
M0 closure docs HEAD  6ea74f630cb35af65d58e7ae873882d6d975411e
Frontend CI           33668744509 PASS
66 decisions assigned
unowned material rows 0
```

Authority: `world-focus-m0-materialization-mapping.md`.

## 2. M1-1 — identity/reference ownership

Validated code:

```text
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS
```

M1-1 materialized:

```text
open-ended WorldFocusId
WorldFocusIdentityDescriptor
fixture IDs separated as WorldFocusFixtureId
explicit fixture/catalog routability
neutral WorldFocusContextReference
bounded ordered WorldFocusContextReferenceSet
workspace canonical contextReferences
selection compatibility projection = primary only
surface default inheritance = primary only
Context/Page explicit descriptor consumption
production World binding in Continuity
proof/oracle imports decoupled from workspace ownership
```

An opaque World id validates identity shape only. It does not establish existence, routability, canonical membership, authorization, disclosure or persistence.

## 3. M1-2 — narrow facets and application seams

Validated production code:

```text
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS
```

This tranche completed the remaining M0-frozen non-visual production work without introducing a universal semantic envelope.

### 3.1 Reference resolution

Finite presentation vocabulary:

```text
usable
unresolved
retired
```

Resolution preserves the exact reference. It never silently chooses a merge/split successor, copies payload, widens disclosure or promotes provider state to canonical identity.

### 3.2 L2 basis / evidence facets

Freshness:

```text
current + asOf
stale + asOf
unknown
```

Validity:

```text
current
superseded + reasonCode
retracted + reasonCode
unresolved + reasonCode
```

Coverage:

```text
complete
incomplete + reasonCode
conflicted + reasonCode
unknown
```

Material payload:

```text
present + exact materialStateReference
retired + exact materialStateReference + reasonCode + retiredAt
```

Evidence metadata remains role-preserving:

```text
evidenceReferences
provenanceReferences
integrityAttestationReferences
```

No confidence score, provider winner, payload copy or generic truth wrapper was added.

### 3.3 L3 sanitized disclosure

Frontend outcome:

```text
available
restricted
unavailable
```

This is only an already-sanitized presentation outcome. The frontend does not decide AuthZ, recipient, purpose or policy. Extra authorization/purpose/recipient fields are not copied through the boundary.

### 3.4 L6 effect presentation

Effect states:

```text
pending
ambiguous
partial-real
reconciliation-required
reversed
compensated
```

Execution revalidation:

```text
not-required
required-before-execution
```

The model does not execute, authorize, cancel, reverse, refund, compensate or infer canonical completion from provider acknowledgements.

### 3.5 L8 sync/platform presentation

Independent axes:

```text
connectivity       online / offline
replay             idle / pending
provider delivery  nominal / lagging / unknown
request timing     within-window / timed-out / unknown
```

Therefore:

```text
offline != source absent
provider lag != canonical stale
timeout != semantic negative
replay pending != replay success/failure
```

### 3.6 Direct Output Grammar seams

Production reference-only seams now exist for:

```text
O2 Situation
O5 Next
O8 Evidence / History
```

They preserve bounded ordered references and do not become Domain owners or generic projection containers.

### 3.7 L1 application seams

Finite work semantics remain exactly:

```text
WP-01 Continuity
WP-02 Attention
WP-03 Comparison
WP-04 Trajectory
```

WP-01 now carries meaningful thread/checkpoint/continuation references.

WP-02 carries material matter/reason/resolution references; notification/unread alone is not Attention.

WP-03 remains bounded comparison, not ranking, recommendation, winner, Decision or causality.

WP-04 preserves ordered points, explicit missing positions and ordering/aggregation basis; missing interval/position is never rewritten as zero.

### 3.8 Shared read mechanics

`world-focus-foundation.ts` owns only reusable mechanics:

```text
World-scoped request
abort relay
runtime boundary validation
latest-read generation
obsolete-read commit rejection
```

Semantic validation remains with intent-specific owners. The shared reader is not a universal `ProjectionEnvelope`, backend DTO or source-of-truth abstraction.

### 3.9 Deterministic adapters

Pre-backend adapters remain deterministic and bounded. Unknown future World IDs can flow through production identity/application seams without extending the fixed visual fixture catalog.

A useful authorized basic path does not require DANTE.

## 4. M1 final red-first falsification

Final adversarial test:

`apps/web/src/features/world-focus/application/world-focus-m1-final-falsification.test.ts`

Red commit:

```text
67bd06d63d84273ba2077761919d714c8d442254
```

CI:

```text
33740212989 — EXPECTED FAILURE
```

Pre-unit gates were green. Web unit result:

```text
55 test files total
1 failed / 54 passed
289 tests total
1 failed / 288 passed
```

The three cross-semantic hostile tests passed:

```text
reference/basis/disclosure/sync/effect axes remained independent
unknown future World supported O2/O5/O8 + WP-01..04 without DANTE
same-generation late surface from wrong World was rejected
```

The only failure was deliberate and precise:

```text
WorldFocusInteractionCursor type declared canonical contextReferences
but runtime Object.keys(cursor) did not expose contextReferences
```

Root cause: the M1-1 compatibility layer still installed `contextReferences` with `Object.defineProperty(... enumerable: false)`.

## 5. Final cursor closure

Fix HEAD:

```text
7369c51e7ba04f8913728a0770f700c728c3b9f9
```

Frontend CI:

```text
33740710290 PASS
```

Validated jobs:

```text
contract drift                PASS
active Home format            PASS
lint                          PASS
typecheck                     PASS
architecture                  PASS
generated-source drift        PASS
unit tests                    PASS
production build              PASS
diff check                    PASS
repository mutation check     PASS
Mobile Bundle                 PASS
Chromium Web E2E              PASS
Firefox frozen Timeline       PASS
Frontend CI Gate              PASS
```

`getWorldFocusInteractionCursor()` now returns `contextReferences` as a normal enumerable frozen property. Historical exact-object tests were migrated to the canonical shape rather than hiding the field.

`selection` remains a compatibility projection of `contextReferences.primary`; it is not the semantic owner.

## 6. M1 permanent barriers preserved

M1 introduced none of the forbidden generic escapes:

```text
NO universal ProjectionEnvelope
NO Thing / Entity / Fact / Relationship / PropertyBag root
NO frontend ACL/AuthZ engine
NO World canonical data ownership
NO page-per-World semantic architecture
NO backend DTO/persistence ownership
NO provider authority
NO durable DANTE Run backend
NO real effect execution
NO AI-required basic path
```

Permanent non-collapses include:

```text
reference exists != payload available != current != disclosable != fresh
stale != superseded != retracted
Evidence != Provenance != integrity attestation
restricted != nonexistent
partial-real != failed != completed
cancel != reversed != compensated
Comparison != Decision
provider state != canonical state
absence/unknown != false
```

## 7. M1 closure disposition

```text
M0                                  CLOSED / VALIDATED
M1                                  CLOSED / VALIDATED
M1-1 identity/reference             CLOSED / VALIDATED
M1-2 non-visual facets + seams      CLOSED / VALIDATED
M2 shared visual primitives         NEXT
M3–M7                               BLOCKED BY SEQUENCE
D2–D6                               DEFERRED TO M4
BACKEND                              BLOCKED UNTIL M7
```

M2 may now render the semantics earned by M1, but renderer components do not become semantic owners and `primitive != card` remains binding.

Immediate continuation:

> **Begin M2 only. Do not start M3 customization, M4 DANTE D2–D6, complete Worlds, integrated visual acceptance or backend work.**
