# Timeline / Temporal-Operational — Candidate Database Overlay

- **Status:** CURRENT CANDIDATE DATABASE AUTHORITY
- **Reconciled:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main baseline:** `20260906_18` / `89|5|18|77|173|91|272|0|0|0`
- **Candidate head:** `20260919_36`
- **Candidate topology:** `109|5|35|87|214|131|312|0|0|0`
- **Whole-DB SoR:** `README.md`
- **Machine-readable authority:** `dictionary/`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Pre-B04 governance closure:** `../workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`
- **B04-A closure authority:** `../workstreams/timeline-temporal-operational-b04-a-closure-2026-09-18.md`
- **B04-B closure authority:** `../workstreams/timeline-temporal-operational-b04-b-closure-2026-09-19.md`
- **B04-C closure authority:** `../workstreams/timeline-temporal-operational-b04-c-closure-2026-09-19.md`

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

Candidate truth becomes protected-main truth only after applicable integration gates and protected-main merge/readback.

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
    ↓
20260919_34 B04-B absolute boundary / deadline
    ↓
20260919_35 B04-C absolute window constraints
    ↓
20260919_36 B04-C window runtime-read ACL
```

`_35` adds the typed window payload tables, widens family/facet discrimination only to the admitted B04-C algebra and adds `mutate_self_absolute_window_constraint(...)`.

`_36` grants runtime SELECT only on the two current window payload tables required by the canonical read model.

## 3. Candidate objects/capabilities activated by the vertical

### Activity

```text
activity_intention
activity_create_operation
create_self_activity(...)
```

### Shared Schedule

B02 activates governed establishment, revision, current/history, unschedule and guarded Undo across:

```text
date_span
floating_local
named_zone_local
absolute
coarse_local_period
```

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

Event Schedule authorization is generalized against the existing shared Schedule owner. Agenda values remain Event-internal ordered content.

### Temporal Constraint — B04-A/B/C ✅ CLOSED / PROVEN

```text
temporal_constraint
temporal_constraint_state
temporal_constraint_boundary_state
temporal_constraint_boundary_absolute_state
temporal_constraint_window_state
temporal_constraint_window_absolute_state
temporal_constraint_current_history
temporal_constraint_mutation_operation

enforce_temporal_constraint_rule_totality()
mutate_self_absolute_earliest_start_constraint(...)
mutate_self_absolute_boundary_constraint(...)
mutate_self_absolute_window_constraint(...)
```

Temporal Constraint remains a stable `ScopedRecordRef` dependent.

Accepted absolute boundary matrix:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
```

Accepted absolute window matrix:

```text
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Each accepted rule also requires self-owned Activity/Event subject plus hard|soft strength. Boundary/window temporal form remains `absolute` for the activated B04-A/B/C slices.

The bounded shared controls remain:

```text
scoped_address                temporal_constraint
material_state_address        temporal_constraint.rule
scoped_current_material_state temporal_constraint.rule
```

Create/revise/retire continue to use immutable receipts, expected-state CAS and retained current-history episodes. Revision never rewrites an existing rule MaterialState. Retirement means no current `temporal_constraint.rule` binding while identity/history remain.

## 4. B04-C evaluation boundary

B04-C evaluation is derived application/API behavior over current effective Temporal Constraints plus a candidate absolute interval.

```text
per rule  satisfied | violated | not_evaluable
overall   admissible | admissible_with_soft_violations | inadmissible | not_evaluable
hard set  feasible | infeasible | undetermined
```

Evaluation is not persisted as canonical DB state. It performs no solver search, automatic movement, Actual inference or Outcome creation.

## 5. Non-collapse invariants

```text
Activity != Event
Activity != Schedule
Event != Schedule
Schedule != Temporal Constraint
Temporal Constraint != Movement Policy
Temporal Constraint != Recurrence
Temporal Constraint != Session / Actual
constraint revision != Schedule revision
deadline != Schedule end
passed deadline != Actual
passed deadline != Outcome / failure
window != placement
preference != accepted Schedule
evaluation != solver decision
violation != automatic mutation
Schedule != Session != Actual
Actual != Outcome
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
Schedule identity != placement MaterialState
current accepted state != newest row
operation/idempotency identity != Domain identity
provider identity != DANTE identity
```

## 6. Current proof state

```text
B01 ✅ CLOSED / PROVEN
B02 ✅ CLOSED / PROVEN
B03 ✅ CLOSED / PROVEN
B04  🟡 IN PROGRESS
├─ B04-A Temporal Constraint canonical core  ✅ CLOSED / PROVEN
├─ B04-B Boundary / Deadline                 ✅ CLOSED / PROVEN
├─ B04-C Windows / Preferences / Evaluation  ✅ CLOSED / PROVEN
└─ B04-D Movement Policy                     ⬜ NEXT
```

Current candidate structural authority:

```text
Alembic  20260919_36
Topology 109|5|35|87|214|131|312|0|0|0
```

B04-C proof includes:

```text
PostgreSQL / application evaluation             9 PASS / 2 deselected
current catalog / Dictionary / ACL             12 PASS
OpenAPI / Temporal API contract                24 PASS
@dante/api-client typecheck                    PASS
@dante/api-client Vitest                       11 PASS
pnpm generated:check                           PASS / 177 deterministic files
```

## 7. Binding same-change gate for B04+

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

No slice can close with a known mismatch. No placeholder object is added for future scope. No historical migration is rewritten. No candidate object is promoted to protected-main truth before it exists there.

## 8. Next persistence boundary

B04-C is closed at `_36`.

B04-D Movement Policy is next only as a PRE-SCOPE gate. No B04-D persistence, enum, mutation routine, API shape, frontend behavior or solver coupling is authorized by B04-C closure.

B04-E advanced-family applicability and B04-F whole-B04 closure remain later work. B05 does not begin until B04-F is closed.
