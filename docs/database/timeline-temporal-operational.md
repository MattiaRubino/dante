# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY
- **Reconciled:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate head:** `20260918_33`
- **Candidate topology:** `107|5|33|85|212|129|309|0|0|0`
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **B03 closure authority:** `../workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`
- **Pre-B04 governance closure:** `../workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`
- **B04-A implementation freeze:** `../workstreams/timeline-temporal-operational-b04-a-implementation-freeze.md`
- **B04-A closure authority:** `../workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md`

## 1. Purpose and authority boundary

This file is the human-readable database overlay for Timeline candidate-only persistence. It exists so feature-branch schema truth is documented without rewriting candidate state as protected-main truth.

```text
protected main
  docs/database/README.md protected-main section
  + current protected-main architecture

Timeline candidate
  protected-main baseline
  + this overlay
  + Dictionary candidate tree/scope
  + candidate Alembic
  + SQLAlchemy
  + real PostgreSQL proof
```

Candidate truth becomes protected-main truth only after the applicable integration gates and protected-main merge/readback.

## 2. Candidate evolution

```text
20260906_18 protected-main baseline
    ↓
20260908_19 B01 Activity core
    ↓
20260909_20 → 20260915_26 B02 shared Schedule core/closure
    ↓
20260916_27 B03-A Event canonical core
    ↓
20260917_28 B03-B shared Event/Schedule activation
    ↓
20260917_29 B03-D Event Agenda / B03 closure
    ↓
20260918_30 B04-A Temporal Constraint canonical core
    ↓
20260918_31 B04-A shared MaterialState totality hardening
    ↓
20260918_32 B04-A shared current-history dispatch hardening
    ↓
20260918_33 B04-A API activation replay / runtime-read hardening
```

B03-C intentionally adds no Event-specific scheduling DDL. Event lifecycle reuses the shared Schedule capability. B04-A likewise extends the bounded CP6 scoped/material-state controls instead of creating a second generic state engine.

`_33` does not add tables, routines, triggers, indexes, FK or CHECK objects. It changes accepted behavior/ACL only, so the measured structural topology remains unchanged from `_32`.

## 3. Candidate objects/capabilities activated by the vertical

### Activity

```text
activity_intention
activity_create_operation
create_self_activity(...)
```

### Shared Schedule

B02 activates governed establishment, revision, current/history, unschedule and guarded Undo across the accepted placement union:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

Schedule remains a shared owner/capability; no Activity- or Event-specific placement engine is introduced.

### Event

```text
event_expectation
event_create_operation
event_agenda_part
event_agenda_current
event_agenda_mutation_operation
create_self_event(...)
create_self_event_with_agenda(...)
replace_self_event_agenda(...)
```

Event Schedule authorization is generalized against the existing shared Schedule owner. Agenda values remain Event-internal ordered content and do not receive NativeRef identity.

### Temporal Constraint — B04-A ✅ CLOSED / PROVEN

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

Temporal Constraint is a stable `ScopedRecordRef` dependent. B04-A supports exactly one complete typed rule path:

```text
Activity | Event subject
+ boundary family
+ earliest_start
+ schedule.start
+ hard | soft
+ absolute
+ finite timestamptz
```

The bounded shared controls are extended with:

```text
scoped_address                temporal_constraint
material_state_address        temporal_constraint.rule
scoped_current_material_state temporal_constraint.rule
```

`_31` closes the MaterialState exclusivity gap so Temporal Constraint payload cannot coexist with Schedule/Actual/Session/recurrence payload in either direction. `_32` hardens the polymorphic current-history trigger dispatcher and is proven across the legacy history families as well as Temporal Constraint.

`_33` closes the application/API activation gap:

```text
same operation_id + same material intent
→ replay returns originally accepted canonical refs
→ caller-generated replacement UUIDs do not break idempotency

runtime SELECT
→ allowed only on the narrow current-rule read surface needed by Get/List
→ history and mutation receipts remain internal
→ generic runtime writes remain denied
```

Create/revise/retire use immutable receipts, expected-state CAS and retained current-history episodes. Revision never rewrites an existing rule MaterialState. Retirement means no current `temporal_constraint.rule` binding while constraint identity and history remain.

## 4. Non-collapse invariants

```text
Activity != Event
Activity != Schedule
Event != Schedule
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
constraint revision != Schedule revision
Schedule != Session != Actual
Actual != Outcome
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
Schedule identity != placement MaterialState
current accepted state != newest row
operation/idempotency identity != Domain identity
provider identity != DANTE identity
```

## 5. Current proof state

```text
B01 ✅ CLOSED / PROVEN
B02 ✅ CLOSED / PROVEN
B03 ✅ CLOSED / PROVEN
B04  🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core  ✅ CLOSED / PROVEN
└─ B04-B Boundary / Deadline                 ⬜ NEXT
```

B04-A closure evidence includes focused persistence/CAS/idempotency proofs, shared current-history regression, whole-DB Dictionary/current-catalog reconciliation, API activation, OpenAPI parity, generated client type/test gates and deterministic generation.

Final candidate structural authority:

```text
Alembic  20260918_33
Topology 107|5|33|85|212|129|309|0|0|0
```

The final current-catalog/DB/B04 activation reconciliation passed locally, and `pnpm generated:check` confirmed deterministic current generated sources across 159 files.

## 6. Binding same-change gate for B04+

Any Timeline change that affects persistence must update, in one reviewed slice, every affected representation:

```text
Domain / Logical / Physical authority when semantics change
→ Alembic forward revision when DDL is required
→ SQLAlchemy mappings / MetaData
→ Dictionary object entries + scope counts
→ current-catalog / owner / ACL proof
→ docs/database/README.md
→ this candidate overlay
→ direct PostgreSQL tests
→ affected map / roadmap / closure evidence
```

No slice can close with a known mismatch. No placeholder table/column/routine is added for future scope. No historical migration is rewritten. No candidate object is promoted to protected-main truth before it exists there.

## 7. Next persistence boundary

B04-A is closed at `_33`. B04-B is the next slice and must begin by freezing the exact Boundary/Deadline semantics before deciding whether any new persistence is required.

B04-B must not assume:

```text
earliest_start == latest_start == deadline
all date/floating/named-zone/absolute representations are interchangeable
passed deadline == Actual failure/outcome
constraint == placement
```

B04-C windows/preferences, B04-D Movement Policy, B04-E advanced-family applicability and B04-F whole-B04 closure remain later work. B05 does not begin until B04-F is closed.
