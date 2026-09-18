# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03 ✅ CLOSED / PROVEN + pre-B04 governance ✅ FROZEN + B04-A ✅ CLOSED / PROVEN → B04-B NEXT
- **Reconciled:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B04 execution authority:** `docs/workstreams/timeline-temporal-operational-b04-execution-plan.md`
- **B04-A implementation freeze:** `docs/workstreams/timeline-temporal-operational-b04-a-implementation-freeze.md`
- **B04-A closure:** `docs/workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md`
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
├─ B04-A Temporal Constraint canonical core      ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline                     ⬜ NEXT
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
Alembic     20260918_33
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

## 3. B04-A semantic closure

Temporal Constraint is a stable `ScopedRecordRef` LR-05 dependent, not a NativeRef and not Schedule placement.

Closed B04-A complete rule:

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

Binding non-collapse remains:

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

No generic `Rule(type,payload)` / JSON semantic escape hatch was introduced.

## 4. B04-A persistence authority at closure

Candidate chain:

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

Shared bounded controls admit:

```text
scoped_address                     temporal_constraint
material_state_address             temporal_constraint.rule
scoped_current_material_state      temporal_constraint.rule
```

`_33` does not change structural topology. It makes mutation replay compatible with server-generated replacement UUIDs while returning the originally accepted canonical refs, and grants only the narrow runtime read surface needed by Get/List. History and mutation receipt internals remain non-public and generic direct writes remain governed.

## 5. B04-A proven behavior

### A1 — DDL / SQLAlchemy ✅

Fresh migration reaches `_33`; the six Temporal Constraint tables have matching registered SQLAlchemy mappings. Historical migrations remain forward-only.

### A2 — PostgreSQL / integrity / catalog / ACL ✅

Observed proof includes:

```text
B04-A focused core                         4 PASS
shared history dispatcher                 4 PASS
Temporal + CP6 final regression           32 PASS / 2 deselected
B04-A structural catalog / owner / ACL    3 PASS
```

Accepted topology:

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

### A4 — DB / Dictionary / docs ✅

Whole-DB Dictionary/current-catalog reconciliation passed, then `_33` current-catalog/ACL expectations were reconciled. Final DB/current-catalog/API-activation gate: `13 PASS`.

### A5 — application / API / generated contract ✅

Accepted public capability:

```text
Get Temporal Constraint
List Temporal Constraints by subject
Create absolute earliest-start constraint
Revise absolute earliest-start rule
Retire Temporal Constraint
```

Every new operation uses an explicit stable semantic `temporal_*` operationId. Existing 13 pre-B04 operationIds remain unchanged.

Observed A5 evidence:

```text
focused API + Temporal inventory             10 PASS
B04-A PostgreSQL/application activation       12 PASS
OpenAPI export/inventory/API parity           18 PASS
@dante/api-client typecheck                   PASS
@dante/api-client Vitest                      11 PASS
pnpm generated:check                          PASS / 159 deterministic files
```

No frontend product surface was required by the accepted B04-A scope, so no manual frontend userTest is claimed.

## 6. B04-A closure decision

```text
A1 ✅ CLOSED / PROVEN
A2 ✅ CLOSED / PROVEN
A3 ✅ CLOSED / PROVEN
A4 ✅ CLOSED / PROVEN
A5 ✅ CLOSED / PROVEN

B04-A Temporal Constraint canonical core ✅ CLOSED / PROVEN
```

Closure authority: `timeline-temporal-operational-b04-a-closure-2026-09-18.md`.

## 7. Next slice — B04-B Boundary / Deadline

B04-B is the next implementation slice. It must begin with semantic inspection/freeze before any DDL/API write.

Candidate semantic territory:

```text
earliest-start
latest-start
latest-completion / deadline
hard | soft boundary semantics
lossless date/floating/named-zone/absolute representation where actually justified
```

Do not collapse:

```text
earliest_start != latest_start
deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
constraint != placement
coarse/date precision != invented exact instant
```

The first B04-B implementation slice should be deliberately narrow and complete rather than activating every candidate family at once.

## 8. Remaining B04 before B05

```text
B04-A canonical core                    ✅ CLOSED / PROVEN
B04-B Boundary / Deadline constraints   NEXT
B04-C Windows / Preferences             later
B04-D Movement Policy                   later
B04-E advanced-family applicability     later
B04-F whole-B04 closure                 later
```

B05 Product Organization starts only after B04-F closes.

## 9. Current gate

```text
B04
├─ B04-A ✅ CLOSED / PROVEN
└─ B04-B ⬜ NEXT
```

**Immediate action:** re-open the Domain / Logical / Physical / B04 execution authority for Boundary / Deadline semantics, freeze the exact B04-B first slice, then approve its implementation scope.

CI remains separately authorized.
