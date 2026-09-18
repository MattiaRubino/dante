# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03 ✅ CLOSED / PROVEN + pre-B04 governance ✅ FROZEN → B04 🟡 IN PROGRESS / B04-A A4 PROOF FRONTIER
- **Reconciled:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A implementation freeze:** `docs/workstreams/timeline-temporal-operational-b04-a-implementation-freeze.md`
- **Pre-B04 governance closure:** `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`
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
├─ B04-A Temporal Constraint canonical core      🟡 IN PROGRESS
├─ B04-B Boundary / Deadline                     ⬜
├─ B04-C Windows / Preferences / Evaluation      ⬜
├─ B04-D Movement Policy                         ⬜
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
Alembic     20260918_32
Topology    107|5|33|85|212|129|309|0|0|0
```

## 2. Closed foundation

B03 remains fully CLOSED / PROVEN. Event is distinct from Activity and reuses one shared Schedule authority. Agenda remains Event-internal value truth. Postponed/TBD Event rediscovery remains explicitly transferred to B05 rather than collapsed into Planning Tray Activity semantics.

The pre-B04 governance closure remains binding:

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

The 13 pre-B04 Temporal operationIds remain frozen compatibility baseline.

## 3. B04-A semantic freeze

Temporal Constraint is a stable `ScopedRecordRef` LR-05 dependent, not a NativeRef and not Schedule placement.

Current B04-A complete rule:

```text
subject             self-owned Activity | Event
facet               temporal_constraint.rule
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary             finite timestamptz
```

Binding non-collapse:

```text
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
Temporal Constraint != Availability / Capacity
constraint revision != Schedule revision
hard planning violation != impossible reality
proposal != accepted effect
current accepted state != newest row
idempotency receipt != Domain identity
```

No generic `Rule(type,payload)` / JSON semantic escape hatch is accepted.

## 4. B04-A persistence now materialized

Candidate chain:

```text
20260917_29 B03 closure
    ↓
20260918_30 B04-A Temporal Constraint core
    ↓
20260918_31 MaterialState totality hardening
    ↓
20260918_32 current-history dispatcher hardening
```

Canonical/control surface:

```text
temporal_constraint
temporal_constraint_state
temporal_constraint_boundary_state
temporal_constraint_boundary_absolute_state
temporal_constraint_current_history
temporal_constraint_mutation_operation

enforce_temporal_constraint_rule_totality()
mutate_self_absolute_earliest_start_constraint(...)
```

Shared bounded controls now admit:

```text
scoped_address                     temporal_constraint
material_state_address             temporal_constraint.rule
scoped_current_material_state      temporal_constraint.rule
```

## 5. Proven B04-A behavior

### A1 — DDL / SQLAlchemy ✅

Fresh migration reaches `_32`; the six Temporal Constraint tables have matching registered SQLAlchemy mappings. The historical migrations remain forward-only and accepted revisions were not rewritten to hide defects.

### A2 — PostgreSQL / integrity / catalog / ACL ✅

Observed proof:

```text
B04-A focused core                         4 PASS
shared history dispatcher                 4 PASS
Temporal + CP6 final regression           32 PASS / 2 deselected
B04-A structural catalog / owner / ACL    3 PASS
```

Direct live topology from the `_32` structural proof:

```text
107 tables
5 views
33 routines
85 triggers
212 indexes
129 FK
309 CHECK
0 enums/domains
0 sequence/materialized/partitioned
0 RLS
```

The `_32` dispatcher is proven on Temporal Constraint plus the legacy Schedule, Actual, Session, Routine recurrence and Event recurrence current-history families.

### A3 — CAS / idempotency ✅

```text
create                 ✅
exact replay           ✅
same key / new intent  ✅ conflict
revise expected CAS    ✅
stale CAS              ✅ conflict
append-only rule state ✅
retire expected CAS    ✅
retained history       ✅
```

## 6. Current active frontier — A4 🟡

The repository now contains the A4 reconciliation candidate:

```text
6 new Temporal Constraint table Dictionary entries
2 new Temporal Constraint routine Dictionary entries
3 shared control-table Dictionary updates
5 shared dispatcher Dictionary updates
scope counts → 107 / 5 / 33 / 85 / 212 / 129 / 309
current-catalog Alembic expectation → 20260918_32
DB SoR → _32
Timeline DB overlay → _32
live map / roadmap / this handoff → B04-A active
```

A4 is deliberately **not yet marked CLOSED**. The immediate next action is local whole-DB reconciliation proof against PostgreSQL `_32`.

## 7. A5 remains unopened

No public Temporal Constraint API endpoint exists yet. Do not start A5 until A4 turns green.

When A5 opens, inspect current Temporal application/API contracts first, then add only the minimum canonical application/API surface justified by B04-A. Every new public operation requires an explicit stable `temporal_*` operationId and same-change OpenAPI/client reconciliation.

No frontend is automatically required merely because A5 begins; frontend scope follows the accepted capability/read-model need, not ceremony.

## 8. Remaining B04 before B05

```text
B04-A canonical core                    current
B04-B Boundary / Deadline constraints   later
B04-C Windows / Preferences             later
B04-D Movement Policy                   later
B04-E advanced-family applicability     later
B04-F whole-B04 closure                 later
```

B05 Product Organization starts only after B04-F closes.

## 9. Current gate

```text
B04-A
├─ A1 ✅
├─ A2 ✅
├─ A3 ✅
├─ A4 🟡 reconciliation candidate materialized
└─ A5 ⬜
```

**Immediate action:** run A4 Dictionary/current-catalog PostgreSQL reconciliation locally. If green, update the ledger from A4 🟡 to A4 ✅ and then open the separate A5 application/API scope.

CI remains separately authorized.
