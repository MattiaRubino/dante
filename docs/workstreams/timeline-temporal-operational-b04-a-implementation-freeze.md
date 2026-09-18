# Timeline / Temporal-Operational — B04-A Implementation Freeze

- **Status:** IMPLEMENTATION FREEZE — B04-A IN PROGRESS
- **Date:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Entering DB head:** `20260917_29`
- **Entering topology:** `101|5|31|78|198|119|297|0|0|0`
- **Authority:** Domain Temporal Constraint v0 + Time/Reality logical model + accepted PostgreSQL physical mapping + B04 execution plan
- **CI:** not implicitly authorized

## 1. Purpose

Freeze the exact first physical/runtime shape of B04-A before forward DDL. This document narrows implementation detail only; it does not reopen the accepted Domain definition.

B04-A establishes the canonical Temporal Constraint identity/material-state/current/history/concurrency/idempotency machinery for the currently active schedulable native owners:

```text
Activity | Event
```

It does not activate broad deadline/window/solver UI semantics.

## 2. No incomplete canonical rule state

A `TemporalConstraint` owner with a current `MaterialStateRef` is not allowed to point at an incomplete generic envelope.

Forbidden implementation shortcuts:

```text
TemporalConstraint(type, json_payload)
TemporalConstraint(family='boundary') with no boundary value
one generic due_at
one generic min_at/max_at sparse row
placeholder/no-op constraint created only to prove persistence
```

The first accepted creation path therefore establishes the canonical core together with one complete typed rule payload. This prevents B04-A from materializing semantically invalid half-rules merely to exercise identity/history machinery.

## 3. Reference and ownership model

A material Temporal Constraint is an LR-05 dependent/rule record with stable scoped addressability:

```text
constraint_ref : ScopedRecordRef
subject_native_ref : NativeRef
```

It is **not** a new LR-01 NativeRef root.

Initial subject eligibility is exactly:

```text
activity | event
```

No generic Entity/owner family shortcut is introduced. Plan, Routine and Occurrence become eligible only through later explicit activation.

`scoped_address` gains the bounded family:

```text
temporal_constraint
```

## 4. Material-state model

The independently revisable rule facet is:

```text
temporal_constraint.rule
```

It is owned in scoped MaterialState space:

```text
material_state_address.scoped_owner_ref = constraint_ref
material_state_address.facet_code = 'temporal_constraint.rule'
```

Current truth is selected by `scoped_current_material_state`; currentness chronology is retained in an owner-specific `temporal_constraint_current_history` relation.

Rules:

```text
current != newest row
revision appends a new MaterialStateRef
prior material states remain reconstructible
retire/remove closes currentness; it does not delete historical states
constraint revision != Schedule revision
```

## 5. First complete typed rule used to prove the core

The first B04-A canonical creation/revision proof uses the narrowest lossless boundary rule:

```text
family                  boundary
boundary kind           earliest-start
constrained facet       schedule.start
strength                 hard | soft
temporal form            absolute
boundary value           exact timestamptz instant
```

This is a real Temporal Constraint, not a placeholder.

It deliberately does **not** claim that B04-B is complete. B04-B remains responsible for the accepted boundary matrix, including latest-start, latest-completion/delivery Deadline and the additional lossless temporal forms selected there.

Unsupported boundary forms fail closed until their typed representation is activated. No local/date-only/named-zone value is silently converted to an absolute instant.

## 6. First physical owner/state family

The `_30` implementation is expected to materialize an owner-specific structured relational family equivalent to:

```text
temporal_constraint
  constraint_ref
  subject_native_ref

temporal_constraint_state
  material_state_ref
  constraint_ref
  family_code
  strength_code
  constrained_facet_code

temporal_constraint_boundary_state
  material_state_ref
  boundary_kind_code
  temporal_form_code

temporal_constraint_boundary_absolute_state
  material_state_ref
  boundary_at

temporal_constraint_current_history
  constraint_ref
  material_state_ref
  current_from_at
  current_until_at

temporal_constraint_mutation_operation
  self_person_ref
  operation_id
  intent_fingerprint
  mutation_kind
  constraint_ref
  subject_native_ref
  expected_material_state_ref
  resulting_material_state_ref
  created_at
```

Exact DDL names may change only if migration proof reveals a concrete collision or existing canonical pattern that requires it. The semantic ownership above is frozen.

No JSON/JSONB column is part of canonical Temporal Constraint state.

## 7. Mutation semantics

B04-A must prove three governed effects:

```text
create
revise
retire/remove-current
```

### Create

Atomically establishes:

```text
Temporal Constraint owner
+ scoped address
+ immutable MaterialState address
+ typed state/payload
+ current binding
+ open current-history episode
+ idempotency receipt
```

### Revise

Requires the caller's expected current `MaterialStateRef`.

```text
expected != current -> conflict
expected == current -> append new state + close old current episode + select new current
```

No in-place rewrite of a prior rule state is accepted.

### Retire/remove current

Requires the expected current `MaterialStateRef`, closes the open current-history episode, removes only the current binding and records the governed operation receipt.

The stable `constraint_ref` and historical states remain.

## 8. Idempotency contract

Mutation operation identity remains technical and separate from semantic constraint identity.

```text
same self Person + operation_id + materially same intent
-> replay prior accepted result

same self Person + operation_id + materially different intent
-> conflict
```

A receipt never becomes a TemporalConstraintRef or MaterialStateRef.

## 9. Integrity changes required in `_30`

The migration must extend the existing bounded shared controls rather than create a second engine:

```text
scoped_address family check
material_state_address facet check
scoped_current_material_state facet check
enforce_scoped_address_owner
enforce_native_ref_eligibility
enforce_material_state_totality
enforce_current_history_equivalence
```

The Temporal Constraint family receives owner-specific payload-totality enforcement for its typed boundary payload.

Existing Activity/Event/Schedule/Actual/Recurrence/Session semantics must remain unchanged.

## 10. Runtime/API boundary

B04-A first proves the database/domain capability before public HTTP exposure.

```text
DDL + mappings + direct PostgreSQL proof
FIRST

public FastAPI endpoint / frontend wiring
ONLY AFTER canonical proof
```

When B04-A later exposes public Temporal endpoints, every new route must follow the pre-B04 governance gate:

```text
explicit operation_id='temporal_*'
+ exact Temporal API inventory
+ OpenAPI snapshot
+ pnpm api:generate
+ generated client + contract tests
```

## 11. Same-change proof gate

The B04-A persistence slice is not `CLOSED / PROVEN` until the accepted implementation is reconciled across:

```text
Alembic
SQLAlchemy
Dictionary object tree + scope counts
real PostgreSQL catalog / owners / ACL
current DB README
Timeline candidate DB overlay
direct PostgreSQL tests
B04 map / roadmap / closure evidence
```

No B04-A green check is authorized by this freeze alone.

## 12. Immediate implementation order

```text
A1 exact `_30` forward DDL + SQLAlchemy mapping
A2 direct PostgreSQL structural/integrity proof
A3 create/revise/retire CAS + idempotency proof
A4 Dictionary/current-catalog/DB-doc reconciliation
A5 application/API exposure only after A1-A4 are green
```

B04-A remains **IN PROGRESS** until those gates are satisfied.