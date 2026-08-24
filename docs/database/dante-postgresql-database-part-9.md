<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-8.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 9

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / FINAL ACTUAL POSTGRESQL OBJECT INVENTORY FROZEN  
**Scope:** section 38 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–8  
**PRE-SCOPE for this inventory freeze:** `5db80a57d3ef7b99d3e78603519e4f99c9263dbb`  
**Current PostgreSQL architecture:** PostgreSQL 18 major family / current technical patch 18.6  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

This continuation freezes the **actual surviving PostgreSQL object inventory** that CP6-04 is eventually expected to materialize after Gate 03 and a separate explicit materialization authorization. It does not create any database object, migration or SQLAlchemy business mapping.

Parts 1–8 remain canonical in full. This section resolves the pre-inventory object-membership question by mechanically replaying their explicit supersessions and final survivor audits. Where an earlier provisional object is absent below because a later checkpoint explicitly withdrew baseline materialization, that absence is intentional and authoritative for the CP6 baseline.

---

## 38. Final Actual PostgreSQL Object Inventory — FROZEN

### 38.1 Purpose and authority

Checkpoint J closed the final 57-concept materialization-disposition gap but deliberately left the exact PostgreSQL object inventory unfrozen. This section performs that next required design step.

The derivation consumed together:

```text
closed Domain 57/57
closed Whole-Logical model
accepted PostgreSQL Physical mapping
CP6-01 persistence coverage Parts 1–2
CP6-02 PostgreSQL Persistence Constitution / ADR-010
Database Architecture & Reference Parts 1–8
all explicit later supersessions
real CP3 PostgreSQL/Alembic/SQLAlchemy foundation
real current backend/migration tree
```

Inventory rule:

```text
include
→ every PostgreSQL object whose existence/topology is already determinable

exclude
→ every historical candidate explicitly withdrawn by a later no-DDL disposition

classify separately
→ DANTE-owned objects
→ technical foundation objects
→ PostgreSQL-extension-owned objects
```

The result is an object-membership and topology freeze. It does **not** close:

```text
DB-U08 exact final SQL identifier naming
DB-U15 final complete structural/query index matrix
DB-U21 exact object-by-object runtime privilege matrix
```

Those three items remain open in that order after this section.

### 38.2 Ownership classes — foundation, DANTE-owned, extension-owned

The final database must not confuse objects merely because PostgreSQL exposes them in the same database.

Three ownership classes are therefore explicit.

#### A. Technical foundation

Already present or owned by the CP3/database-platform foundation:

```text
PostgreSQL database                       dante deployment database
schema                                    dante
Alembic technical version table           dante.alembic_version
PostgreSQL roles                          dante_owner
                                          dante_migrator
                                          dante_runtime
```

The technical Alembic table is not a DANTE semantic/business table and is excluded from the 68-table DANTE-owned count.

After eventual CP6 materialization, assuming the same Alembic topology:

```text
DANTE-owned baseline tables               68
Alembic technical table                    1
---------------------------------------------
TABLES IN schema dante                     69
```

That `69` is a physical schema-count statement, not a semantic owner count.

#### B. DANTE-owned CP6 baseline

Objects whose schema contract belongs to DANTE and is governed by this reference:

```text
DANTE-owned tables                         68
DANTE-owned ordinary views                  5
DANTE custom enum/domain types              0
DANTE sequences                             0
DANTE materialized views                    0
DANTE RLS policies                          0
```

The table and view sets are enumerated exactly below.

#### C. PostgreSQL extension-owned capability surface

The current technical database image/init contract creates these extensions:

```text
postgis             3.6.4
vector              0.8.6
pg_trgm
unaccent
pg_stat_statements
```

Objects created internally by those extensions are **extension-owned**. They are not individually promoted into the DANTE Database Dictionary merely because PostgreSQL introspection exposes them.

Examples include extension-owned types, functions, operators, catalogs, views or support tables. They are governed as extension/capability dependencies unless a later DANTE object explicitly consumes one of their types/operators/index methods.

Hard rule:

```text
extension object visible in PostgreSQL
!= DANTE-owned persistence object
```

No CP6 baseline business object currently requires a PostGIS geometry/geography column, pgvector column/index, trigram index or persisted FTS/search structure.

### 38.3 Final count freeze

The exact DANTE-owned row-shaped inventory is:

```text
LR-01 native identity shells             15
shared address/current controls           5
Schedule family                           7
Actual family                             5
Session timing/history family             5
Routine/Event Recurrence family          26
Occurrence generation family              5
--------------------------------------------
DANTE TABLES                              68

facet-specific current views              5
--------------------------------------------
DANTE TABLES + ORDINARY VIEWS            73
```

No table is counted twice. No independently scoped `Recurrence` table exists.

### 38.4 Fifteen native identity-shell tables

The exact LR-01 native-owner table set remains:

```text
dante.person
  person_ref uuid PRIMARY KEY

dante.living_referent
  living_referent_ref uuid PRIMARY KEY

dante.asset
  asset_ref uuid PRIMARY KEY

dante.place
  place_ref uuid PRIMARY KEY

dante.content_artifact
  content_artifact_ref uuid PRIMARY KEY

dante.collective
  collective_ref uuid PRIMARY KEY

dante.possibility
  possibility_ref uuid PRIMARY KEY

dante.goal
  goal_ref uuid PRIMARY KEY

dante.plan
  plan_ref uuid PRIMARY KEY

dante.activity
  activity_ref uuid PRIMARY KEY

dante.event
  event_ref uuid PRIMARY KEY

dante.routine
  routine_ref uuid PRIMARY KEY

dante.occurrence
  occurrence_ref uuid PRIMARY KEY

dante.session
  session_ref uuid PRIMARY KEY

dante.observation
  observation_ref uuid PRIMARY KEY
```

All fifteen use native PostgreSQL `uuid` and application-issued UUIDv7 identity under the existing ID doctrine.

The shell rows do not receive generic:

```text
name
title
status
created_at
updated_at
deleted_at
is_deleted
metadata jsonb
```

merely for CRUD convenience.

Schema existence does not authorize semantic identity-only creation. In particular:

```text
Routine
→ must establish complete current routine.recurrence semantics by COMMIT

Session
→ must establish complete current session.timing semantics by COMMIT

Occurrence
→ individually materialized identity must retain truthful origin/generation basis

Observation
→ identity shell exists, but semantic creation remains unavailable until a concrete typed assertion profile exists
```

### 38.5 Shared bounded address and current-state control tables

The exact five shared technical control tables are:

```text
dante.native_address
  native_ref      uuid PRIMARY KEY
  owner_family    text NOT NULL

dante.scoped_address
  scoped_ref      uuid PRIMARY KEY
  scoped_family   text NOT NULL

dante.material_state_address
  material_state_ref   uuid PRIMARY KEY
  native_owner_ref     uuid NULL
  scoped_owner_ref     uuid NULL
  facet_code           text NOT NULL

dante.native_current_material_state
  native_owner_ref    uuid NOT NULL
  facet_code          text NOT NULL
  material_state_ref  uuid NOT NULL
  PRIMARY KEY(native_owner_ref, facet_code)
  UNIQUE(material_state_ref)

dante.scoped_current_material_state
  scoped_owner_ref    uuid NOT NULL
  facet_code          text NOT NULL
  material_state_ref  uuid NOT NULL
  PRIMARY KEY(scoped_owner_ref, facet_code)
  UNIQUE(material_state_ref)
```

`material_state_address` requires exactly one owner address space:

```text
num_nonnulls(native_owner_ref, scoped_owner_ref) = 1
```

Foreign-key directions remain:

```text
material_state_address.native_owner_ref
→ native_address(native_ref)
→ ON DELETE NO ACTION

material_state_address.scoped_owner_ref
→ scoped_address(scoped_ref)
→ ON DELETE NO ACTION

native_current_material_state.native_owner_ref
→ native_address(native_ref)
→ ON DELETE NO ACTION

scoped_current_material_state.scoped_owner_ref
→ scoped_address(scoped_ref)
→ ON DELETE NO ACTION

both current tables.material_state_ref
→ material_state_address(material_state_ref)
→ ON DELETE NO ACTION
```

These tables are technical address/control infrastructure, not semantic superclasses.

### 38.6 Final bounded dispatcher vocabularies

#### Native owner families

`native_address.owner_family` is bounded to exactly the 15 LR-01 owners:

```text
person
living_referent
asset
place
content_artifact
collective
possibility
goal
plan
activity
event
routine
occurrence
session
observation
```

#### Scoped families

The final baseline scoped-family survivor set is exactly:

```text
schedule
actual
```

No baseline registration survives for:

```text
agreement
milestone
temporal_constraint
recurrence
outcome
criterion
evaluation
```

#### MaterialState facets

The final baseline facet set is exactly:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

Mechanically replayed historical candidates that do not survive include:

```text
agreement.shared_assent
milestone.context
temporal_constraint.definition
recurrence.definition
criterion.definition
evaluation.result
outcome.result
```

No sixth baseline facet was found during the final mechanical replay of Parts 1–8.

### 38.7 Schedule family — seven tables

The complete Schedule baseline is:

```text
dante.schedule
  schedule_ref         uuid PRIMARY KEY
  subject_native_ref   uuid NOT NULL

dante.schedule_placement_state
  material_state_ref   uuid PRIMARY KEY
  schedule_ref         uuid NOT NULL
  temporal_form_code   text NOT NULL

dante.schedule_placement_date_state
  material_state_ref   uuid PRIMARY KEY
  date_span            daterange NOT NULL

dante.schedule_placement_floating_local_state
  material_state_ref   uuid PRIMARY KEY
  extent_code          text NOT NULL
  starts_local_at      timestamp without time zone NOT NULL
  ends_local_at        timestamp without time zone NULL

dante.schedule_placement_named_zone_state
  material_state_ref   uuid PRIMARY KEY
  extent_code          text NOT NULL
  starts_local_at      timestamp without time zone NOT NULL
  ends_local_at        timestamp without time zone NULL
  zone_id              text NOT NULL
  resolved_start_at    timestamptz NULL
  resolved_end_at      timestamptz NULL

dante.schedule_placement_absolute_state
  material_state_ref   uuid PRIMARY KEY
  extent_code          text NOT NULL
  starts_at            timestamptz NOT NULL
  ends_at              timestamptz NULL

dante.schedule_placement_current_history
  schedule_ref         uuid NOT NULL
  material_state_ref   uuid NOT NULL
  current_from_at      timestamptz NOT NULL
  current_until_at     timestamptz NULL
  PRIMARY KEY(schedule_ref, current_from_at)
```

`subject_native_ref` is a bounded heterogeneous NativeRef admitting only:

```text
activity
event
occurrence
```

`temporal_form_code` baseline values are exactly:

```text
date_span
floating_local
named_zone_local
absolute
```

Exactly one matching typed placement payload must exist for every live `schedule.placement` MaterialStateRef by COMMIT.

No baseline qualitative day-part payload exists. `Tuesday afternoon` remains semantically valid upstream but cannot be stored canonically until a bounded accepted day-part vocabulary exists.

Schedule current-history must preserve non-overlapping currentness episodes and current-binding equivalence. Schedule may later have no current placement after governed unscheduling while history remains.

### 38.8 Actual family — five tables

The complete Actual baseline is:

```text
dante.actual
  actual_ref           uuid PRIMARY KEY
  subject_native_ref   uuid NOT NULL

dante.actual_realization_state
  material_state_ref      uuid PRIMARY KEY
  actual_ref              uuid NOT NULL
  realization_occurred    boolean NOT NULL

dante.actual_realization_timing
  material_state_ref   uuid PRIMARY KEY
  extent_code          text NOT NULL
  started_at           timestamptz NOT NULL
  ended_at             timestamptz NULL

dante.actual_realization_session_basis
  actual_material_state_ref          uuid NOT NULL
  session_ref                        uuid NOT NULL
  session_timing_material_state_ref  uuid NOT NULL
  PRIMARY KEY(actual_material_state_ref, session_ref)

dante.actual_realization_current_history
  actual_ref           uuid NOT NULL
  material_state_ref   uuid NOT NULL
  current_from_at      timestamptz NOT NULL
  current_until_at     timestamptz NULL
  PRIMARY KEY(actual_ref, current_from_at)
```

`actual.subject_native_ref` admits only:

```text
activity
event
occurrence
```

There is deliberately no global `UNIQUE(actual.subject_native_ref)`.

`actual_realization_timing` is optional and valid only when the parent realization state is `realization_occurred=true`.

`actual_realization_session_basis` binds both stable Session identity and the exact `session.timing` MaterialStateRef used by that historical Actual state.

No generic Actual result/status or Outcome field exists.

### 38.9 Session timing/history family — five tables in addition to native `session`

The Session companion baseline is:

```text
dante.session_timing_state
  material_state_ref   uuid PRIMARY KEY
  session_ref          uuid NOT NULL
  timing_form_code     text NOT NULL

dante.session_timing_absolute
  material_state_ref      uuid PRIMARY KEY
  started_at              timestamptz NOT NULL
  start_precision_code    text NOT NULL
  ended_at                timestamptz NULL
  end_precision_code      text NULL

dante.session_timing_elapsed
  material_state_ref       uuid PRIMARY KEY
  elapsed_seconds          numeric NOT NULL
  elapsed_precision_code   text NOT NULL

dante.session_timing_pause
  material_state_ref      uuid NOT NULL
  paused_at               timestamptz NOT NULL
  pause_precision_code    text NOT NULL
  resumed_at              timestamptz NULL
  resume_precision_code   text NULL
  PRIMARY KEY(material_state_ref, paused_at)

dante.session_timing_current_history
  session_ref          uuid NOT NULL
  material_state_ref   uuid NOT NULL
  current_from_at      timestamptz NOT NULL
  current_until_at     timestamptz NULL
  PRIMARY KEY(session_ref, current_from_at)
```

`timing_form_code` is exactly:

```text
absolute
elapsed_only
```

Session-local precision vocabulary is exactly:

```text
exact
approximate
rounded
```

`elapsed_seconds` must be finite and greater than zero.

For one accepted absolute timing state:

```text
pause boundaries lie within representative Session boundaries
pause intervals do not overlap
ended Session cannot contain an open pause
at most one open pause exists per timing state
```

The last rule is declaratively enforceable by a partial unique index and is therefore not delegated to trigger-only enforcement.

A canonical Session must have one complete current `session.timing` state by COMMIT. “Current timing” means current accepted interpretation of the execution episode, not “currently running”.

### 38.10 Routine/Event Recurrence family — twenty-six tables

Recurrence remains owner-bound. There is no independently scoped `dante.recurrence` root.

#### State envelopes — two

```text
dante.routine_recurrence_state
  material_state_ref          uuid PRIMARY KEY
  routine_ref                 uuid NOT NULL
  family_code                 text NOT NULL
  range_kind                  text NOT NULL
  expected_occurrence_count   integer NULL

dante.event_recurrence_state
  material_state_ref          uuid PRIMARY KEY
  event_ref                   uuid NOT NULL
  family_code                 text NOT NULL
  range_kind                  text NOT NULL
  expected_occurrence_count   integer NULL
```

Physical `family_code` values are exactly:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

The accepted semantic families `completion_relative` and `anchor_stream_relative` remain no-baseline-DDL until their exact qualifying-anchor contracts exist.

`range_kind` values are exactly:

```text
open
until_boundary
expected_count
```

#### Boundary states — two

```text
dante.routine_recurrence_boundary_state
dante.event_recurrence_boundary_state

  material_state_ref   uuid NOT NULL
  boundary_role        text NOT NULL
  boundary_kind        text NOT NULL
  inclusive            boolean NULL
  date_value           date NULL
  local_value          timestamp without time zone NULL
  zone_id              text NULL
  instant_value        timestamptz NULL
  resolved_at          timestamptz NULL
  PRIMARY KEY(material_state_ref, boundary_role)
```

`boundary_role`:

```text
pattern_anchor
effective_from
effective_until
```

`boundary_kind`:

```text
date
floating_local
named_zone_local
absolute_instant
```

#### Calendar family — twelve tables

```text
dante.routine_recurrence_calendar_state
dante.event_recurrence_calendar_state

  material_state_ref   uuid PRIMARY KEY
  pattern_code         text NOT NULL
  interval_count       integer NOT NULL
  clock_basis_code     text NOT NULL
  zone_id              text NULL
  step_unit_code       text NULL
```

`pattern_code`:

```text
daily
weekly_weekdays
monthly_month_days
monthly_ordinal_weekdays
yearly_month_days
anchor_step
```

`clock_basis_code`:

```text
floating_local
named_zone
absolute_utc
```

`step_unit_code`, only for `anchor_step`:

```text
day
week
month
year
```

Typed selector children exist owner-specifically:

```text
dante.routine_recurrence_calendar_wall_time
dante.event_recurrence_calendar_wall_time
  material_state_ref uuid NOT NULL
  wall_time          time without time zone NOT NULL
  PRIMARY KEY(material_state_ref, wall_time)

dante.routine_recurrence_calendar_weekday
dante.event_recurrence_calendar_weekday
  material_state_ref uuid NOT NULL
  weekday_number     smallint NOT NULL
  PRIMARY KEY(material_state_ref, weekday_number)

dante.routine_recurrence_calendar_month_day
dante.event_recurrence_calendar_month_day
  material_state_ref uuid NOT NULL
  month_day          smallint NOT NULL
  PRIMARY KEY(material_state_ref, month_day)

dante.routine_recurrence_calendar_ordinal_weekday
dante.event_recurrence_calendar_ordinal_weekday
  material_state_ref uuid NOT NULL
  weekday_number     smallint NOT NULL
  ordinal            smallint NOT NULL
  PRIMARY KEY(material_state_ref, weekday_number, ordinal)

dante.routine_recurrence_calendar_year_month_day
dante.event_recurrence_calendar_year_month_day
  material_state_ref uuid NOT NULL
  month_number       smallint NOT NULL
  month_day          smallint NOT NULL
  PRIMARY KEY(material_state_ref, month_number, month_day)
```

Row-local selector checks remain exact:

```text
weekday_number              1..7
month_number                1..12
month_day                   1..31 OR -31..-1
ordinal                     -5..-1 OR 1..5
```

No invalid-date fallback/clamp field exists.

#### Elapsed family — two tables

```text
dante.routine_recurrence_elapsed_state
dante.event_recurrence_elapsed_state

  material_state_ref   uuid PRIMARY KEY
  elapsed_seconds      numeric NOT NULL
  anchor_mode_code     text NOT NULL
  anchor_at            timestamptz NOT NULL
```

`elapsed_seconds` is finite and greater than zero.

`anchor_mode_code`:

```text
fixed_anchor
previous_expected
```

The explicit seed `anchor_at` is mandatory. Actual completion is not silently substituted.

#### Quota family — two tables

```text
dante.routine_recurrence_quota_state
dante.event_recurrence_quota_state

  material_state_ref   uuid PRIMARY KEY
  quota_count          integer NOT NULL
  period_unit_code     text NOT NULL
  period_span          integer NOT NULL
  frame_code           text NOT NULL
  zone_id              text NULL
  week_start           smallint NULL
```

Rules include:

```text
quota_count > 0
period_span > 0
period_unit_code IN ('day','week','month','year')
frame_code IN ('floating_local','named_zone','absolute_utc')
week_start 1..7 only for weekly period
```

No quota slot ordinal exists.

#### Cyclic family — four tables

```text
dante.routine_recurrence_cyclic_state
dante.event_recurrence_cyclic_state

  material_state_ref   uuid PRIMARY KEY
  cycle_length         integer NOT NULL
  position_unit_code   text NOT NULL

dante.routine_recurrence_cycle_position
dante.event_recurrence_cycle_position

  material_state_ref   uuid NOT NULL
  position_index       integer NOT NULL
  generates_expected  boolean NOT NULL
  PRIMARY KEY(material_state_ref, position_index)
```

Rules:

```text
cycle_length > 0
position_unit_code IN ('day','week')
position_index >= 0
exact date-based pattern_anchor required
complete index set 0..cycle_length-1 required by COMMIT
```

#### Current-history — two tables

```text
dante.routine_recurrence_current_history
  routine_ref         uuid NOT NULL
  material_state_ref  uuid NOT NULL
  current_from_at     timestamptz NOT NULL
  current_until_at    timestamptz NULL
  PRIMARY KEY(routine_ref, current_from_at)

dante.event_recurrence_current_history
  event_ref           uuid NOT NULL
  material_state_ref  uuid NOT NULL
  current_from_at     timestamptz NOT NULL
  current_until_at    timestamptz NULL
  PRIMARY KEY(event_ref, current_from_at)
```

Routine creation requires a complete current recurrence contract by COMMIT. One-off Event remains valid without recurrence; establishing recurring Event semantics requires the complete owner/facet/current contract in the recurrence-bearing operation.

### 38.11 Occurrence generation family — five tables

The exact origin envelope is:

```text
dante.occurrence_generation
  occurrence_ref                   uuid PRIMARY KEY
  source_native_ref                uuid NOT NULL
  governing_recurrence_state_ref   uuid NULL
  origin_code                      text NOT NULL
```

`source_native_ref` admits only:

```text
routine
event
```

`origin_code`:

```text
recurrence_generated
explicit_extra
```

For `recurrence_generated`, the exact owner-bound governing recurrence MaterialStateRef is mandatory. For `explicit_extra`, that field is NULL and no false rule-generated coordinate exists.

Family coordinates:

```text
dante.occurrence_generation_calendar
  occurrence_ref       uuid PRIMARY KEY
  generated_date       date NOT NULL
  generated_wall_time  time without time zone NULL
  clock_basis_code     text NOT NULL
  zone_id              text NULL
  resolved_at          timestamptz NULL

dante.occurrence_generation_elapsed
  occurrence_ref       uuid PRIMARY KEY
  expected_at          timestamptz NOT NULL

dante.occurrence_generation_quota
  occurrence_ref                uuid PRIMARY KEY
  period_start_date             date NOT NULL
  period_end_date_exclusive     date NOT NULL
  frame_code                    text NOT NULL
  zone_id                       text NULL

dante.occurrence_generation_cyclic
  occurrence_ref       uuid PRIMARY KEY
  generated_date       date NOT NULL
  position_index       integer NOT NULL
```

Every recurrence-generated Occurrence has exactly one coordinate family matching the governing recurrence family. `explicit_extra` has zero generated-coordinate rows.

Quota coordinate has no slot ordinal.

Historical materialized Occurrence remains bound to the exact old governing recurrence state after later recurrence revision.

### 38.12 Five bounded current-facet views

The final ordinary-view set is exactly:

```text
dante.schedule_current_placement
→ filtered dante.scoped_current_material_state
→ facet_code = 'schedule.placement'

dante.actual_current_realization
→ filtered dante.scoped_current_material_state
→ facet_code = 'actual.realization'

dante.session_current_timing
→ filtered dante.native_current_material_state
→ facet_code = 'session.timing'

dante.routine_current_recurrence
→ filtered dante.native_current_material_state
→ facet_code = 'routine.recurrence'

dante.event_current_recurrence
→ filtered dante.native_current_material_state
→ facet_code = 'event.recurrence'
```

Each view uses a fixed facet predicate and `WITH LOCAL CHECK OPTION` when exposed as an updatable bounded operation surface.

The design relies on PostgreSQL automatically-updatable simple-view semantics where applicable. CP6 does **not** add `INSTEAD OF` trigger machinery merely for these views.

Exact runtime DML privileges remain DB-U21.

### 38.13 Declarative constraint floor

Every invariant that PostgreSQL can express correctly with ordinary declarative constraints remains declarative before trigger machinery is considered.

The final baseline includes, as applicable per table:

```text
NOT NULL
PRIMARY KEY
FOREIGN KEY
UNIQUE
CHECK
partial UNIQUE index-backed invariants
```

Global rules:

```text
ON DELETE NO ACTION baseline
stable identity not reused
material payload not silently overwritten
current state not inferred by insertion/timestamp/UUID order
unknown/absence not encoded as false by default
```

Representative mandatory row-local checks include:

```text
material_state_address exactly-one owner space
Schedule temporal form/extent compatibility
finite/non-empty Schedule date span
Schedule/Actual interval end > start
Actual direct timing only when realization_occurred=true
Session absolute/elapsed exclusivity
Session positive finite elapsed duration
Session precision vocabulary
Recurrence family/range vocabulary
Recurrence positive interval/quota/cycle quantities
calendar selector numeric bounds
boundary-kind payload exclusivity
quota period validity
Occurrence origin NULL/non-NULL governing-state rule
generation-coordinate frame/zone combinations
cyclic position_index >= 0
```

Cross-table/cross-row invariants that ordinary FK/CHECK/UNIQUE cannot express use only the bounded integrity layer below.

### 38.14 Minimum structural index floor — 78 DANTE indexes before DB-U15

The inventory establishes a **minimum structural index floor**, not the final DB-U15 index matrix.

Already justified physical indexes:

```text
68  indexes backing the 68 DANTE table primary keys
 2  UNIQUE indexes backing UNIQUE(material_state_ref)
    on native_current_material_state and scoped_current_material_state
 2  material_state_address partial owner/facet indexes
 5  partial UNIQUE indexes enforcing one open current-history episode
 1  partial UNIQUE index enforcing one open Session pause per timing state
---
78  MINIMUM STRUCTURAL DANTE INDEXES
```

The two material-state partial indexes are:

```text
(native_owner_ref, facet_code)
WHERE native_owner_ref IS NOT NULL

(scoped_owner_ref, facet_code)
WHERE scoped_owner_ref IS NOT NULL
```

The five open-history uniqueness predicates apply separately to:

```text
schedule_placement_current_history
actual_realization_current_history
session_timing_current_history
routine_recurrence_current_history
event_recurrence_current_history

UNIQUE(owner_ref)
WHERE current_until_at IS NULL
```

The Session pause structural index is conceptually:

```text
UNIQUE(material_state_ref)
WHERE resumed_at IS NULL
```

because the accepted model permits at most one open pause in one timing state and PostgreSQL can express that invariant declaratively.

DB-U15 remains OPEN. It must still review every referencing FK, parent lifecycle path, join/filter/order pattern, current/history access path and concurrency operation and may add only indexes with a proven structural or query reason.

No speculative:

```text
index-every-FK rule
index-every-timestamp rule
GiST solely for style
GIN/trigram/vector/search index without a real consumer
partitioning/sharding
```

is authorized by this floor.

### 38.15 Bounded integrity-routine / trigger attachment topology

A fresh object-level replay was performed specifically to avoid freezing an estimated trigger count.

The frozen design topology is:

```text
BOUNDED INTEGRITY ROUTINE ROLES          14
TRIGGER ATTACHMENTS                      75
  ordinary/immediate                     18
  deferred constraint-trigger            57
VIEW INSTEAD-OF TRIGGERS                  0
```

These are **integrity design roles and table-attachment topology**. Exact SQL routine and trigger identifiers remain DB-U08 work. A bounded validator may be reused across a symmetric owner-specific aggregate when doing so preserves exact static semantics; that reuse does not create a generic Rule/business-workflow engine.

#### Role 1 — NativeAddress concrete-owner dispatcher

```text
attachments: 1 immediate
  native_address
```

Validates bounded `owner_family` and existence in the exact one of 15 concrete native owner tables. Address identity/family is immutable under ordinary runtime authority.

#### Role 2 — ScopedAddress concrete-owner dispatcher

```text
attachments: 1 immediate
  scoped_address
```

Validates only final scoped families `schedule` / `actual` and exact concrete owner existence.

#### Role 3 — heterogeneous NativeRef consumer eligibility

```text
attachments: 3 immediate
  schedule
  actual
  occurrence_generation
```

Enforces the consumer-specific admitted `native_address.owner_family` set rather than application-only `kind+uuid` checks.

#### Role 4 — MaterialState live address↔payload totality

```text
attachments: 6 deferred constraint triggers
  material_state_address
  schedule_placement_state
  actual_realization_state
  session_timing_state
  routine_recurrence_state
  event_recurrence_state
```

Enforces the bidirectional live total 1:1 address/payload contract and exact owner/facet matching by COMMIT.

#### Role 5 — shared current-binding owner/facet validation

```text
attachments: 2 immediate
  native_current_material_state
  scoped_current_material_state
```

Validates same address space, owner and facet as the selected MaterialStateRef.

#### Role 6 — current-history overlap + current-binding equivalence

```text
attachments: 7 deferred constraint triggers
  schedule_placement_current_history
  actual_realization_current_history
  session_timing_current_history
  routine_recurrence_current_history
  event_recurrence_current_history
  native_current_material_state
  scoped_current_material_state
```

Uses bounded deterministic owner-row locking to reject overlapping history episodes and enforce open-history ⇔ current-binding equivalence by COMMIT.

#### Role 7 — semantic owner creation completeness

```text
attachments: 5 deferred constraint triggers
  schedule
  actual
  session
  routine
  occurrence
```

Prevents committed ceremonial shells where current authority already requires companion semantics:

```text
Schedule   → accepted placement/current-history contract
Actual     → established realization/current-history contract
Session    → complete current session.timing contract
Routine    → complete current routine.recurrence contract
Occurrence → truthful origin/generation basis when individually materialized
```

This role does not grant create operations for every shell and does not invent a universal lifecycle.

#### Role 8 — Schedule placement payload totality/exclusivity

```text
attachments: 5 deferred constraint triggers
  schedule_placement_state
  schedule_placement_date_state
  schedule_placement_floating_local_state
  schedule_placement_named_zone_state
  schedule_placement_absolute_state
```

Ensures exactly one payload matching `temporal_form_code` and no wrong-family payload by COMMIT.

#### Role 9 — Actual exact-basis validation

```text
attachments: 2 immediate
  actual_realization_timing
  actual_realization_session_basis
```

Validates realized-state eligibility and exact Session timing-state owner/facet basis.

#### Role 10 — Session timing payload totality

```text
attachments: 3 deferred constraint triggers
  session_timing_state
  session_timing_absolute
  session_timing_elapsed
```

Ensures exactly one payload matching `timing_form_code`.

#### Role 11 — Session pause geometry/consistency

```text
attachments: 2 deferred constraint triggers
  session_timing_pause
  session_timing_absolute
```

Enforces pause containment, no overlap and ended-session/open-pause consistency. One-open-pause cardinality itself remains declarative through the partial unique index.

#### Role 12 — Routine/Event recurrence aggregate integrity

```text
attachments: 24 deferred constraint triggers
```

The attachments cover the symmetric Routine/Event recurrence aggregate across:

```text
recurrence_state
recurrence_boundary_state
recurrence_calendar_state
recurrence_calendar_wall_time
recurrence_calendar_weekday
recurrence_calendar_month_day
recurrence_calendar_ordinal_weekday
recurrence_calendar_year_month_day
recurrence_elapsed_state
recurrence_quota_state
recurrence_cyclic_state
recurrence_cycle_position
```

for both Routine and Event.

This bounded integrity role enforces aggregate rules that cannot be truthfully expressed by row-local CHECK alone, including:

```text
exactly one matching family payload
calendar selector-family totality/exclusivity
required pattern anchors where phase demands them
range/boundary completeness
quota phase requirements
cyclic complete 0..cycle_length-1 position set
owner/facet correctness
```

It is not a generic recurrence DSL and admits only the four baseline physical families.

#### Role 13 — Occurrence generation family integrity

```text
attachments: 5 deferred constraint triggers
  occurrence_generation
  occurrence_generation_calendar
  occurrence_generation_elapsed
  occurrence_generation_quota
  occurrence_generation_cyclic
```

Enforces:

```text
exact governing owner/facet recurrence state
recurrence_generated → exactly one matching coordinate family
recurrence_generated → zero nonmatching coordinate families
explicit_extra → no governing recurrence state
explicit_extra → zero generated-coordinate rows
cyclic position eligibility against governing state
```

Quota materialization cardinality remains additionally protected by the accepted operation-level deterministic source-row lock/count transaction discipline; it is not represented by a fake quota slot identity.

#### Role 14 — accepted IANA timezone validation

```text
attachments: 9 immediate
  schedule_placement_named_zone_state
  routine_recurrence_boundary_state
  event_recurrence_boundary_state
  routine_recurrence_calendar_state
  event_recurrence_calendar_state
  routine_recurrence_quota_state
  event_recurrence_quota_state
  occurrence_generation_calendar
  occurrence_generation_quota
```

Validates named-zone values against the PostgreSQL/tzdb accepted IANA timezone vocabulary without inventing a DANTE timezone taxonomy table.

Count reconciliation:

```text
immediate
1 + 1 + 3 + 2 + 2 + 9 = 18

deferred
6 + 7 + 5 + 5 + 3 + 2 + 24 + 5 = 57

TOTAL = 75
```

Earlier draft estimates produced during read-only derivation are superseded by this mechanically reconciled object-level ledger.

### 38.16 Timezone validation boundary

DANTE stores timezone identifiers only where the accepted temporal form requires a named zone.

The baseline does **not** create:

```text
dante.timezone
dante.time_zone
timezone lookup taxonomy
provider timezone mapping
```

Database-local validation uses PostgreSQL's accepted timezone/tzdb vocabulary through a narrow schema-qualified validator. The stored `zone_id` remains the accepted original IANA identifier for the semantic state.

The validator must not silently:

```text
substitute server timezone
substitute device timezone
shift DST gaps
choose first/second DST-overlap offset
rewrite a historical resolved instant because tzdb later changes
```

Historical consequential resolution retains the original local coordinate/zone plus accepted resolved instant where the relevant state shape permits it.

### 38.17 No DANTE custom type/domain/sequence baseline

The final inventory contains no DANTE-owned PostgreSQL:

```text
CREATE TYPE ... AS ENUM
CREATE DOMAIN
CREATE SEQUENCE
```

Bounded semantic vocabularies remain `text + CHECK` in this baseline where that was already the selected contract.

UUIDv7 semantic identities are application-issued and stored as PostgreSQL `uuid`; no sequence is needed.

Extension-owned types such as PostGIS/pgvector types are not counted as DANTE custom types.

### 38.18 No materialized view / RLS baseline

The five current surfaces are ordinary filtered views. No materialized view is justified.

No baseline PostgreSQL RLS policy is introduced. RLS remains optional defense-in-depth under CP6-02 and cannot become Domain Authority/Consent/Visibility semantics.

Therefore:

```text
DANTE MATERIALIZED VIEWS = 0
DANTE RLS POLICIES       = 0
```

### 38.19 Negative-object / tombstone exclusion ledger

The final inventory explicitly excludes all of the following baseline objects or object families.

#### Generic semantic roots

```text
Entity / Thing
Relationship / generic edge
Fact / Claim
Version root
Rule(type,payload)
generic event ontology/event store
generic semantic property/EAV store
generic provenance/audit graph
generic workflow root
```

#### Reference/address shortcuts

```text
generic kind + uuid reference
generic ReferenceAddress union table
ActorRef
SubjectRef
ResourceRef
independent QuantityRef
independent MonetaryAmountRef
independent CapacityRef
```

#### Explicitly withdrawn scoped/material candidates

```text
dante.recurrence independent root
agreement tables / agreement.shared_assent facet
milestone tables / milestone.context facet
temporal_constraint tables / temporal_constraint.definition facet
criterion root/facet
evaluation root/facet
outcome root/facet
```

#### Checkpoint-J final no-DDL semantic families

No generic baseline root/table exists for:

```text
Acknowledgement
Authority
Availability
Conditional Policy
Confirmation
Consent
Contribution
Coordination Stewardship
Decision
Dependency
Evidence
Interpersonal Relationship
Membership
Ownership
Participation
Possession
Proposal
Provenance
Reconciliation
Representation
Request
Resource Allocation
Resource Requirement
Responsibility
Visibility
```

plus the already independently closed no-DDL families:

```text
Agreement
Criterion
Evaluation
Milestone
Outcome
Temporal Constraint
```

Their exact future activation triggers remain in Parts 2–8 and are not replaced by this inventory summary.

#### Security/integration/runtime technical objects not triggered

```text
Account tables
Principal registry
credential/login-session product tables
provider registry
ExternalRef registry
provider generic mapping table
idempotency reservation table
transactional outbox
generic integration event table
search cache tables
vector embedding business tables
persisted FTS/trigram search structures
```

#### Recurrence objects not authorized

```text
completion_relative payload tables
anchor_stream_relative payload tables
recurrence_component
recurrence_expression
union/intersection recurrence AST/DSL
recurrence_cutover generic table
future-occurrence reconciliation-status table
quota slot-number table/column
```

#### Session/Observation/Place generic placeholders

```text
generic Session status enum/table
session_split/session_merge generic lifecycle tables
generic SessionContext kind+id/JSON
generic Observation property/value/assertion JSON payload
universal property registry
mandatory Place geometry/address/provider payload
speculative Place spatial index
```

#### Generic lifecycle placeholders

```text
universal deleted_at
universal is_deleted
universal tombstone root
universal status
universal metadata JSONB
```

### 38.20 Object-membership freeze versus remaining DB-U work

This section freezes **what object topology survives**. The remaining DB-U items may refine only their owned axes.

#### DB-U08 — exact naming

May freeze/refine deterministic PostgreSQL identifiers for:

```text
tables/columns where a design handle is not yet final
PK/FK/UQ/CK constraints
indexes
views
functions/routines
triggers
migration identifiers where applicable
```

DB-U08 must use a professional repository-wide deterministic naming standard and PostgreSQL-safe identifier policy. It may not add/remove semantic objects merely to make names convenient.

Already explicitly frozen design names such as the five current views remain strong inputs; any identifier refinement must preserve semantic traceability and be explicitly reconciled.

#### DB-U15 — final index matrix

Starts from the 78-index minimum structural floor and performs the complete FK/query/concurrency/lifecycle review.

It may add a justified index. It may not change semantic cardinality or introduce a new persistence family under the guise of indexing.

#### DB-U21 — exact ACL matrix

Decides privileges for every concrete object and must replace the CP3 broad foundation posture before business object materialization.

It may not infer semantic create/update/delete permission merely because a table exists.

### 38.21 Current foundation ACL caveat carried forward

The current CP3 provisioning historically grants broad runtime table DML/default privileges while no DANTE business objects exist. That posture is foundation evidence, not the final CP6 business-object privilege contract.

Before CP6-04 materialization is authorized, DB-U21 must freeze the exact object-level matrix and the materialization plan must ensure newly created business/control objects receive only the approved privileges.

In particular:

```text
shared control tables
immutable material-state payloads
current-history tables
current-facet views
integrity routines
```

must not inherit inappropriate blanket runtime authority.

### 38.22 Migration and SQLAlchemy consequences — inventory only

The inventory creates deterministic future mapping pressure but does not yet close the migration DAG or ORM plan.

General consequences already fixed:

```text
one shared SQLAlchemy Base / MetaData
schema = dante
one mapped row class where ORM mapping is useful
no polymorphic semantic root
no generic Repository[T]
no metadata.create_all deployment authority
Alembic remains deployed-schema authority
views need no ORM mapping merely for symmetry
```

The exact migration grouping/order and SQLAlchemy class/module plan remain the explicit later CP6-03 steps after DB-U08/15/21.

### 38.23 Database Dictionary consequence

The inventory is now sufficiently frozen to become the object-membership input to the later Database Dictionary readiness step.

The Dictionary must distinguish at least:

```text
DANTE-owned
Alembic technical
extension-owned/external capability dependency
```

It must not generate false missing-entry failures for every internal PostGIS/pgvector/pg_trgm/unaccent/pg_stat_statements object.

Conversely, every one of the 68 DANTE-owned tables, five DANTE-owned views and later-frozen DANTE integrity/index objects must be accounted for by the Dictionary/reference rules applicable to that object class.

### 38.24 Cumulative whole-database inventory audit

The completed candidate inventory was replayed against the whole accumulated database, not only the new count ledger.

Results:

```text
57 / 57 final concept dispositions                 PASS
15 / 15 native owners                              PASS
new native owner                                   0
unclassified concept/family                        0

DANTE tables                                       68 / EXACT
DANTE ordinary views                                5 / EXACT
independent scoped baseline families                2 / EXACT
MaterialState facets                                5 / EXACT

independent Recurrence root                         0
completion-relative baseline payload                0
anchor-stream baseline payload                      0
custom DANTE enum/domain types                      0
DANTE sequences                                     0
DANTE materialized views                            0
DANTE RLS policies                                  0

foundation vs DANTE ownership                       PASS
extension-owned quarantine                          PASS
Alembic technical table separation                  PASS

scoped survivor replay                              PASS
MaterialState facet replay                          PASS
historical superseded candidates excluded           PASS
Checkpoints D–J negative dispositions preserved     PASS

Schedule object graph                               PASS
Actual object graph                                 PASS
Session object graph                                PASS
Routine/Event Recurrence object graph               PASS
Occurrence generation object graph                  PASS

minimum structural index floor                      78 / RECONCILED
integrity routine roles                             14 / RECONCILED
trigger attachments                                 75 / RECONCILED
view INSTEAD-OF triggers                             0

semantic JSON fallback required                     0
generic kind+uuid fallback required                 0
universal semantic root introduced                  0
hidden business ORM implementation                  0
hidden business Alembic DDL                         0

DB-U08                                              OPEN / CORRECT
DB-U15                                              OPEN / CORRECT
DB-U21                                              OPEN / CORRECT
SECOND FULL TOMBSTONE AUDIT                         NOT YET RUN
GATE 03                                             NOT YET EARNED
CP6-04                                              NOT AUTHORIZED
```

No Domain, Logical, Physical, CP6-01 or CP6-02 reopening is required by this inventory.

### 38.25 Inventory freeze status and exact next step

The Final Actual PostgreSQL Object Inventory is now:

```text
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY
FROZEN

DANTE TABLE MEMBERSHIP
68

DANTE CURRENT VIEW MEMBERSHIP
5

SCOPED FAMILY SET
schedule
actual

MATERIALSTATE FACET SET
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence

MINIMUM STRUCTURAL INDEX FLOOR
78

BOUNDED INTEGRITY ROUTINE ROLES
14

TRIGGER ATTACHMENTS
75

GLOBAL DB-U OPEN
DB-U08
DB-U15
DB-U21
```

Exact next CP6-03 block:

```text
DB-U08 — FINAL POSTGRESQL OBJECT NAMING
```

Required following order remains:

```text
DB-U08 exact naming
→ DB-U15 final structural/query index matrix
→ DB-U21 exact object-level privilege matrix
→ migration/materialization DAG
→ SQLAlchemy mapping plan
→ Database Dictionary readiness
→ direct PostgreSQL proof/test plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03 only if clean
```

### 38.26 CP6-04 boundary remains closed

Nothing in this inventory freeze authorizes real database materialization.

```text
ALEMBIC BUSINESS MIGRATIONS      NOT AUTHORIZED
SQLALCHEMY BUSINESS MAPPINGS     NOT AUTHORIZED
CREATE TABLE                     NOT AUTHORIZED
CREATE VIEW                      NOT AUTHORIZED
CREATE FUNCTION/TRIGGER          NOT AUTHORIZED
BUSINESS INDEX/ACL MATERIALIZE   NOT AUTHORIZED

CP6-03
ACTIVE

GATE 03
NOT YET EARNED

CP6-04
NOT STARTED / NOT AUTHORIZED
```

At Gate 03 the assistant must STOP. Entering CP6-04 requires a separate explicit user-approved materialization gate.

---

## 39. Current continuation state

Part 9 adds no new Domain concept, Logical representation family or Physical technology selection. It freezes the PostgreSQL object membership mechanically derived from the already accepted model.

The single canonical human-readable database authority is now:

```text
Part 1  sections 1–30
Part 2  section 31
Part 3  section 32
Part 4  section 33
Part 5  section 34
Part 6  section 35
Part 7  section 36
Part 8  section 37
Part 9  sections 38–39
```

The next substantive canonical continuation must begin from this inventory freeze and must not restore any tombstoned object merely because an earlier provisional section contained a candidate shape.