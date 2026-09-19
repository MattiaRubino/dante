# Timeline / Temporal-Operational — B04-E Advanced-family Applicability Freeze

- **Status:** ✅ GATE PASSED / IMPLEMENTATION FROZEN
- **Date:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Previous slice:** B04-D Movement Policy ✅ CLOSED / PROVEN
- **Candidate DB entering B04-E:** PostgreSQL 18.6 / Alembic `20260919_39`
- **Candidate topology entering B04-E:** `115|5|42|89|232|152|329|0|0|0`
- **Execution authority:** `timeline-temporal-operational-b04-execution-plan.md`
- **Domain authority:** `docs/domain/concepts/temporal-constraint.md` + canonical continuation
- **Logical authority:** `docs/logical-model/slices/time-reality-v1.md` + `identity-reference-v1.md`
- **CI:** not used; local gates only

---

# 1. Gate decision

B04-D -> B04-E gate is accepted.

```text
B04-D ✅ CLOSED / PROVEN
B04-E 🟡 ACTIVE
```

B04-E is an applicability/integration slice, not permission to pull Session, Actual, Occurrence generation, solver, Dependency, or generic heterogeneous relationship infrastructure forward.

---

# 2. Frozen advanced-family disposition

## TC-008 — minimum / maximum planned Schedule duration

**Disposition: ACTIVATE IN B04-E.**

Canonical scope is only the duration of a proposed/accepted `Schedule` placement where duration is exactly evaluable from the placement itself.

```text
subject              self-owned Activity | Event
family               duration
constrained facet    schedule.placement
rule kind            minimum | maximum
strength             hard | soft
value                positive exact elapsed duration
first evaluable form absolute interval
```

Permanent non-collapse:

```text
planned Schedule duration
!= Activity estimated effort
!= Session elapsed duration
!= Session active duration
!= Actual duration
```

The first physical representation must be typed relational state; no JSON rule payload or generic Rule root.

The activated evaluator is bounded to exact absolute interval placement. Unsupported/coarse placement forms remain fail-closed rather than receiving fabricated duration precision.

## TC-009 — minimum contiguous Session duration

**Disposition: applicability gate satisfied / runtime deferred to B08 Session Runtime.**

The Domain semantic is accepted, but B04-E must not simulate Session truth through Schedule placement. Reopen when Session ownership/runtime is active.

## TC-010 — spacing / recovery

**Disposition: runtime deferred to B06/B08/B10 according to anchor.**

Rules such as recovery after a previous Session, dose after a previous Actual, or spacing between generated Occurrences require a canonical source-selection anchor that is not active in the current B04 Activity/Event constraint surface.

Forbidden shortcut:

```text
fake last_time timestamp on Activity/Event
```

Reopening trigger: the required previous Session / Actual / Occurrence anchor becomes canonical and queryable under its owning block.

## TC-011 — relative before / after

**Disposition: runtime persistence deferred.**

Relative temporal semantics remain canonical Temporal Constraint semantics. Current Logical identity/reference authority supplies typed `NativeRef` and Reference Contracts, but the current physical B04 surface does not yet supply the reviewed heterogeneous relation/reference persistence needed to activate arbitrary relative targets without inventing `related_id + type`, opaque JSON, or a generic semantic Relationship root.

Reopening trigger: a reviewed bounded reference/relation contract exists for the exact target union and temporal fact being referenced.

---

# 3. B04-E implementation scope

Implement only TC-008 plus integration hardening:

```text
1. typed duration Temporal Constraint persistence
2. immutable MaterialState/current/history through existing Temporal Constraint core
3. expected-state CAS + operation-id idempotency through governed mutation
4. hard|soft duration semantics
5. exact evaluation against absolute interval Schedule placement
6. B04-D automatic-move hard-admissibility extended to current hard duration rules
7. PostgreSQL / SQLAlchemy / Dictionary / catalog reconciliation
8. explicit closure dispositions for TC-009/010/011
```

No new public endpoint is required by this freeze. If the existing public Temporal Constraint contract is later widened to author/read duration in B04-E, OpenAPI/client same-change governance becomes mandatory before closure.

---

# 4. Explicit exclusions

B04-E does not implement:

```text
Session runtime or contiguous Session enforcement          B08
Occurrence generation / previous-occurrence selection      B06
Actual/Outcome-derived spacing anchors                     B10
solver/replanning/search                                   B12
generic Dependency                                         neighboring domain
fallback/replanning prototype policy                       B12
arbitrary heterogeneous relative relation persistence      later reviewed relation owner
fabricated duration for date/coarse placement forms        forbidden
```

---

# 5. Closure proof required

B04-E cannot close until applicable proof is green:

```text
TC-008 create/revise/retire/current/history
hard minimum duration rejection
hard maximum duration rejection
soft duration violation remains admissible with explanation
simultaneous boundary/window/duration composition
hard-set infeasibility where duration conflicts with available placement geometry
automatic Schedule movement cannot bypass hard duration rule
CAS + idempotent replay/collision
Activity/Event self-scope isolation
Dictionary / SQLAlchemy / Alembic / live PostgreSQL parity
explicit TC-009/010/011 defer/reopen ownership recorded
```

B04-F remains the whole-B04 product/regression closure after B04-E.