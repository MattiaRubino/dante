# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03 ✅ CLOSED / PROVEN + pre-B04 governance ✅ FROZEN + B04-A/B/C ✅ CLOSED / PROVEN → B04-D NEXT
- **Reconciled:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md`
- **B04-B closure:** `docs/workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md`
- **B04-C freeze:** `docs/workstreams/timeline-temporal-operational-b04-c-implementation-freeze.md`
- **B04-C closure:** `docs/workstreams/timeline-temporal-operational-b04-c-closure-2026-09-19.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline                     ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation      ✅ CLOSED / PROVEN
├─ B04-D Movement Policy                         ⬜ NEXT
├─ B04-E Advanced-family applicability           ⬜
└─ B04-F Whole-B04 closure                       ⬜
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260919_36
Topology    109|5|35|87|214|131|312|0|0|0
```

## 2. Binding foundation

B03 remains CLOSED / PROVEN. Event is distinct from Activity and reuses the shared Schedule authority. Agenda remains Event-internal value truth. Postponed/TBD Event rediscovery remains transferred to B05.

Pre-B04 governance remains binding:

```text
DB:
Alembic
≈ SQLAlchemy
≈ Dictionary + scope
≈ live catalog / owner / ACL
≈ current DB SoR
≈ Timeline DB overlay
≈ direct PostgreSQL proof
≈ workstream closure docs

API:
route/model
→ explicit stable semantic operationId for every new Temporal endpoint
→ exact Temporal inventory
→ OpenAPI snapshot
→ Orval / @dante/api-client
→ affected API/frontend tests
→ workstream docs
```

The 13 pre-B04 Temporal operationIds remain the frozen compatibility baseline.

## 3. B04-A carried forward

B04-A established Temporal Constraint as a stable `ScopedRecordRef` dependent with immutable rule MaterialState history, explicit current state, expected-state CAS and idempotent create/revise/retire.

First complete rule:

```text
subject             self-owned Activity | Event
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary             finite timestamptz
```

Closure authority: `timeline-temporal-operational-b04-a-closure-2026-09-18.md`.

## 4. B04-B closure carried forward

Closed absolute boundary matrix:

```text
earliest_start     → schedule.start
latest_start       → schedule.start
latest_completion  → schedule.completion
```

Binding non-collapse:

```text
earliest_start != latest_start
latest_completion/deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
constraint != placement
Temporal Constraint != Movement Policy
```

Persistence authority through B04-B:

```text
20260919_34 b04_absolute_boundary_deadline
107|5|34|85|212|129|309|0|0|0
```

Closure authority: `timeline-temporal-operational-b04-b-closure-2026-09-19.md`.

## 5. B04-C semantic closure

B04-C activates absolute windows and deterministic derived evaluation without collapsing constraint truth into Schedule placement or solver behavior.

Closed window relation matrix:

```text
start_within              → schedule.start
completion_within         → schedule.completion
full_placement_contained  → schedule.placement
placement_overlaps        → schedule.placement
```

All window variants require:

```text
subject        self-owned Activity | Event
family         window
strength       hard | soft
temporal form  absolute
starts_at      finite timestamptz
ends_at        finite timestamptz
ends_at        > starts_at
```

Relation semantics:

```text
start_within / completion_within use inclusive point membership
full_placement_contained requires full interval containment
placement_overlaps requires positive overlap; endpoint-only touching is not overlap
```

Soft is preference, not accepted placement. Hard is a validity constraint, not Actual/Outcome truth.

## 6. B04-C persistence authority

Candidate chain continues:

```text
20260917_29 B03 closure
    ↓
20260918_30 B04-A Temporal Constraint core
    ↓
20260918_31 MaterialState totality hardening
    ↓
20260918_32 current-history dispatcher hardening
    ↓
20260918_33 Temporal Constraint API activation hardening
    ↓
20260919_34 B04-B absolute boundary / deadline
    ↓
20260919_35 B04-C absolute window constraints
    ↓
20260919_36 B04-C runtime window read ACL
```

B04-C adds:

```text
temporal_constraint_window_state
temporal_constraint_window_absolute_state
mutate_self_absolute_window_constraint(...)
```

The exact family/relation/facet matrix is enforced by deferred DB totality. Runtime receives SELECT only on the current window payload tables required by the canonical read model.

Accepted topology:

```text
109 tables
5 views
35 routines
87 triggers
214 indexes
131 FK
312 CHECK
0 enums/domains
0 sequence/materialized/partitioned
0 RLS
```

## 7. B04-C application / evaluation / API

Current rule reads now cover typed boundary and window variants through one canonical Temporal Constraint application surface.

Create/revise dispatch on the new rule family. Retire dispatches from the expected current rule family so boundary/window identity remains stable and retirement remains idempotent.

Evaluation is derived from current effective constraints plus a candidate absolute interval.

Per-rule:

```text
satisfied | violated | not_evaluable
```

Overall:

```text
admissible
admissible_with_soft_violations
inadmissible
not_evaluable
```

Hard set:

```text
feasible | infeasible | undetermined
```

Evaluation persists no violation state, creates no Actual/Outcome truth and performs no solver search or automatic movement.

Public API adds exactly:

```text
POST /api/v1/temporal/constraints/evaluate
temporal_evaluate_constraints
```

Existing five Temporal Constraint CRUD operationIds remain stable.

Generated OpenAPI/client commit:

```text
5268d9dd239ab344337cadd1dfdf312dd46ffe42
feat(temporal): generate B04-C window evaluation client
```

## 8. B04-C proof

Observed local proof:

```text
PostgreSQL / application evaluation             9 PASS / 2 deselected
current catalog / Dictionary / ACL             12 PASS
OpenAPI / Temporal API contract                24 PASS
@dante/api-client typecheck                    PASS
@dante/api-client Vitest                       11 PASS
pnpm generated:check                           PASS / 177 deterministic files
```

Observed PostgreSQL topology:

```text
B04_C_LIVE_TOPOLOGY=109|5|35|87|214|131|312|0|0|0
B04_LIVE_TOPOLOGY=109|5|35|87|214|131|312|0|0|0
DATABASE_CURRENT_TOPOLOGY=109|5|35|87|214|131|312|0|0|0
```

No full B04 product UX was part of B04-C, so no manual frontend userTest is claimed for this slice.

Closure decision:

```text
B04-C Windows / Preferences / Evaluation ✅ CLOSED / PROVEN
```

Closure authority: `timeline-temporal-operational-b04-c-closure-2026-09-19.md`.

## 9. Unsupported / later-owned semantics

B04-C does not activate:

```text
date-span window constraints
floating-local window constraints
named-zone-local window constraints
coarse-local-period window constraints
persisted evaluation/violation state
Movement Policy
automatic movement
advanced duration / spacing / relative families
solver / optimization / candidate search
Actual / Outcome inference
full constraint-management product UX
```

These remain fail-closed or owned by later blocks.

## 10. Remaining B04 before B05

```text
B04-A canonical core                    ✅ CLOSED / PROVEN
B04-B Boundary / Deadline constraints   ✅ CLOSED / PROVEN
B04-C Windows / Preferences             ✅ CLOSED / PROVEN
B04-D Movement Policy                   NEXT
B04-E advanced-family applicability     later
B04-F whole-B04 closure                 later
```

B05 Product Organization starts only after B04-F closes.

## 11. Current gate

```text
B04
├─ B04-A ✅ CLOSED / PROVEN
├─ B04-B ✅ CLOSED / PROVEN
├─ B04-C ✅ CLOSED / PROVEN
└─ B04-D ⬜ NEXT
```

**Immediate action:** re-open Domain / Logical / Physical / B04 execution authority for Movement Policy and freeze the exact B04-D scope before any B04-D write.

B04-C closure does not pre-authorize B04-D persistence, enums, mutation semantics, API, frontend behavior or solver coupling.

CI remains separately authorized.
