# Timeline / Temporal-Operational — B04-A Temporal Constraint Core Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Accepted code/data anchor before closure reconciliation:** `7490b48927415728167afb701b620d246c2c01d5`
- **Alembic head:** `20260918_33`
- **Candidate topology:** `107|5|33|85|212|129|309|0|0|0`
- **Parent block:** B04 Temporal Constraints + Movement Policy 🟡 IN PROGRESS
- **Next slice:** B04-B Boundary / Deadline constraints
- **CI:** not used; closure evidence was executed locally

## 1. Closure scope

B04-A activates the canonical Temporal Constraint identity and one complete typed rule path without collapsing constraint truth into Schedule placement, Movement Policy, recurrence, execution or solver output.

Accepted first complete rule:

```text
subject             self-owned Activity | Event
identity            ScopedRecordRef, not NativeRef
facet               temporal_constraint.rule
family              boundary
boundary kind       earliest_start
constrained facet   schedule.start
strength            hard | soft
temporal form       absolute
boundary             finite timestamptz
```

Permanent non-collapse remains binding:

```text
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
Temporal Constraint != Availability / Capacity
constraint revision != Schedule revision
proposal != accepted effect
current accepted state != latest row
idempotency receipt != constraint identity != MaterialState identity
hard planning violation != impossible reality
planned/intended != happened
```

No generic `Rule(type,payload)` or JSON semantic escape hatch was introduced.

## 2. Persistence authority at closure

B04-A evolved the Timeline candidate only through forward revisions:

```text
20260917_29 B03 closure
    ↓
20260918_30 b04_temporal_constraint_core
    ↓
20260918_31 b04_temporal_constraint_totality_hardening
    ↓
20260918_32 b04_current_history_dispatch_hardening
    ↓
20260918_33 b04_temporal_constraint_api_activation
```

`_33` does not change structural topology. It closes the API-activation persistence gap by making mutation replay compatible with server-generated UUIDs and granting the runtime the narrow read-only surface required by Get/List while retaining governed writes and keeping receipt/history internals non-public.

Accepted structural authority remains:

```text
PostgreSQL 18.6
107 tables
5 views
33 routines
85 triggers
212 indexes
129 FK
309 CHECK
0 enums/domains
0 sequences/materialized/partitioned
0 RLS
```

Canonical B04-A persistence surface:

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

## 3. A1–A3 persistence and behavioral proof

### A1 — DDL / SQLAlchemy ✅

Fresh migration reaches the B04-A head; the six Temporal Constraint tables have matching registered SQLAlchemy mappings. Shared CP6 controls are extended instead of duplicated.

### A2 — PostgreSQL / integrity / catalog / ACL ✅

Observed evidence includes:

```text
focused B04-A core                         4 PASS
shared current-history legacy-family proof 4 PASS
Temporal + CP6 final regression           32 PASS / 2 deselected
B04-A structural catalog / owner / ACL     3 PASS
```

The shared current-history dispatcher is proven for Temporal Constraint plus Schedule, Actual, Session, Routine recurrence and Event recurrence.

### A3 — CAS / idempotency ✅

Proven behavior:

```text
create                              PASS
exact replay                        PASS
same key + changed material intent  conflict
revise expected-state CAS           PASS
stale CAS                           conflict
append-only rule state              PASS
retire expected-state CAS           PASS
retained stable identity/history    PASS
Activity/Event self ownership       PASS
cross-self rejection                PASS
runtime direct-write bypass         denied
```

## 4. A4 DB / Dictionary / documentation reconciliation ✅

A4 reconciled Alembic, SQLAlchemy, Dictionary object entries/scope, live PostgreSQL catalog, owners/ACL, whole-DB SoR, Timeline candidate overlay and workstream references.

The whole-DB reconciliation gate passed locally:

```text
current catalog + database catalog + B04 catalog
11 PASS
```

After `_33` API activation, current-catalog and ACL expectations were reconciled again. Final DB/current-catalog/API-activation gate:

```text
13 PASS
```

Topology remains unchanged at `_33` because the activation revision alters routine behavior and privileges, not object counts.

## 5. A5 application / API contract ✅

B04-A exposes the minimum canonical public surface:

```text
Get Temporal Constraint by TemporalConstraintRef
List Temporal Constraints by self-owned subject
Create absolute earliest-start constraint
Revise current absolute earliest-start rule
Retire Temporal Constraint
```

Application semantics preserve:

```text
accepted-current read model != mutation replay result
server-generated IDs remain replay-safe
expected-current CAS remains authoritative
operation-id idempotency remains authoritative
retired != deleted
Activity | Event remain the only B04-A subject families
```

Every new public operation uses an explicit stable semantic `temporal_*` operationId. The 13 pre-B04 Temporal operationIds remain unchanged compatibility baseline.

Observed A5 proof:

```text
focused API + Temporal OpenAPI inventory       10 PASS
B04-A PostgreSQL/application activation         12 PASS
OpenAPI export/inventory/API parity             18 PASS
@dante/api-client TypeScript typecheck          PASS
@dante/api-client Vitest                         11 PASS
final DB/current-catalog/API-activation gate    13 PASS
```

The governed OpenAPI snapshot and Orval-generated `@dante/api-client` artifacts are committed on the branch.

Final determinism gate executed on the accepted branch head:

```text
pnpm generated:check
PASS: generated sources are deterministic and current (159 files)
```

No frontend product surface was required by the accepted A5 scope; therefore no manual frontend userTest is claimed for B04-A.

## 6. Closure decision

All B04-A stages are complete:

```text
A1 exact DDL + SQLAlchemy                         ✅ CLOSED / PROVEN
A2 PostgreSQL structural/integrity/catalog/ACL    ✅ CLOSED / PROVEN
A3 create/revise/retire CAS + idempotency         ✅ CLOSED / PROVEN
A4 Dictionary/current-catalog/DB docs             ✅ CLOSED / PROVEN
A5 application/API/OpenAPI/generated client       ✅ CLOSED / PROVEN

B04-A Temporal Constraint canonical core          ✅ CLOSED / PROVEN
```

B04 itself remains open. The next implementation slice is:

```text
B04-B Boundary / Deadline constraints
```

B04-C Windows / Preferences / Evaluation, B04-D Movement Policy, B04-E advanced-family applicability and B04-F whole-B04 closure remain later work. B05 begins only after B04-F closes.

No CI run is implied by this closure.