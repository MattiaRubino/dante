<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-9.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 10

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / DB-U08 FINAL POSTGRESQL OBJECT NAMING CLOSED  
**Scope:** section 40 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–9  
**PRE-SCOPE for this DB-U08 closure:** `f90092d5e79036a01c51be0e3e56675e9fdbfc33`  
**Current PostgreSQL architecture:** PostgreSQL 18 major family / current technical patch 18.6  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Part 9 froze which PostgreSQL objects survive. This continuation closes the next required axis: **their repository-wide PostgreSQL naming contract**.

Nothing in this section adds or removes a business object. Part 9 object membership remains frozen. DB-U15 and DB-U21 remain open.

---

## 40. DB-U08 — Final PostgreSQL Object Naming — CLOSED

### 40.1 Purpose and authority

DB-U08 exists so CP6-04 cannot invent SQL identifiers while implementing the already-frozen object graph.

Naming is treated as an operational database contract because names appear in:

```text
Alembic revisions
SQLAlchemy MetaData
PostgreSQL catalogs
constraint/index diagnostics
pg_stat views
incident/debugging output
query plans
schema-drift tooling
Database Dictionary
support/runbook SQL
future online migrations
```

The naming standard therefore optimizes for:

```text
semantic readability
mechanical determinism
PostgreSQL safety
stable diagnostics
migration stability
collision resistance
minimal abbreviation
zero quoting dependency
```

Inputs consumed:

```text
CP3 SQLAlchemy MetaData naming convention
CP6-02 CON-10 deterministic constraint-name rule
Part 9 frozen 68-table / 5-view object inventory
Part 9 78-index structural floor
Part 9 14 integrity-routine roles
Part 9 75 trigger attachments
PostgreSQL 18 identifier rules
SQLAlchemy 2.0 naming-convention behavior
large-system constraint/index naming practice used as benchmark only
```

Relevant platform facts:

```text
PostgreSQL default max_identifier_length = 63 bytes
ASCII lower_snake_case therefore gives byte length == character length
SQLAlchemy naming conventions are deterministic
SQLAlchemy can deterministically truncate generated names, but DANTE does not rely on PostgreSQL silent truncation
```

### 40.2 Core lexical standard

All DANTE-owned SQL identifiers MUST be:

```text
ASCII
lowercase
lower_snake_case
unquoted
semantically meaningful
stable across environments
```

Allowed identifier alphabet for DANTE-authored objects:

```text
[a-z][a-z0-9_]*
```

Identifiers MUST NOT:

```text
require double quotes
contain uppercase letters
contain whitespace
contain punctuation other than underscore
encode environment names
encode developer initials
encode ticket numbers
encode provider names unless the object is genuinely provider-owned
encode UUID/time/random suffixes merely to avoid thinking about collisions
```

Reserved-word conflict rule:

```text
current manifest
→ must use an ordinary unquoted non-keyword identifier

future candidate conflicts with PostgreSQL/SQL keyword
→ rename semantically
→ do NOT rescue it with quoted identifiers
```

Handwritten SQL may uppercase SQL keywords for readability, but database object identifiers remain lowercase.

### 40.3 Identifier-length policy

PostgreSQL 18 reports the default identifier ceiling through `max_identifier_length`; the standard build uses 63 bytes.

DANTE rule:

```text
all explicitly authored DANTE identifiers
MUST fit within 63 bytes before DDL reaches PostgreSQL
```

No migration may intentionally submit an overlength explicit DANTE name and rely on PostgreSQL to truncate it.

For SQLAlchemy convention-generated names:

```text
normal convention result <= 63 bytes
→ use it directly

normal convention result > 63 bytes
→ use a DB-U08-approved explicit semantic alias
→ do not depend on server truncation
```

SQLAlchemy's deterministic truncation remains a safety property for external/generated behavior, not the chosen naming design for the CP6 baseline.

The materialization QA must query the live server's `max_identifier_length` and fail if it is unexpectedly below the declared manifest requirement.

### 40.4 Namespace and collision discipline

Naming QA must understand PostgreSQL namespaces rather than performing only a global string scan.

DANTE nevertheless deliberately uses stronger uniqueness where practical.

```text
schema relation namespace
→ tables / views / indexes / sequences / materialized views must not collide

constraint names
→ PostgreSQL scope rules apply, but DANTE includes table identity so names remain diagnostic

routine names
→ PostgreSQL permits overloading by signature
→ DANTE integrity routines MUST NOT rely on overload ambiguity
→ one exact integrity routine name per role

trigger names
→ PostgreSQL uniqueness is table-local
→ DANTE baseline trigger identifiers are globally distinct anyway

columns
→ unique within their owning relation

Alembic revision IDs
→ globally unique within the one canonical migration DAG
```

Pre-materialization generated-manifest QA must check collision-free names before the migration is reviewed.

### 40.5 Semantic object names from Part 9 are now exact

The following Part-9 design handles are accepted unchanged as final PostgreSQL identifiers:

```text
schema
  dante

technical table
  dante.alembic_version

68 DANTE-owned table names
  exactly as enumerated in Part 9 sections 38.4–38.11

5 current-facet view names
  dante.schedule_current_placement
  dante.actual_current_realization
  dante.session_current_timing
  dante.routine_current_recurrence
  dante.event_current_recurrence

all Part-9 column names
  exact / unchanged
```

No pluralization migration is performed merely for fashion.

DANTE convention is:

```text
one semantic owner/object family
→ singular relation name unless the accepted object itself is naturally a collection/history structure

child/state/history relation
→ semantic owner/facet/purpose encoded in the relation name
```

Examples retained:

```text
person
schedule
actual
session_timing_state
schedule_placement_current_history
routine_recurrence_calendar_ordinal_weekday
occurrence_generation_quota
```

Forbidden cosmetic prefixes:

```text
tbl_
table_
vw_
view_
entity_
obj_
```

Object type is available from PostgreSQL catalogs; semantic relation names remain cleaner without decorative type prefixes.

### 40.6 Column naming contract

Part 9 column identifiers are final.

Core suffix meanings remain stable:

```text
*_ref
→ stable DANTE/reference identity slot

*_at
→ absolute timestamp/timestamptz instant or boundary

*_local_at
→ local timestamp without time zone

*_date
→ civil date

*_code
→ bounded semantic discriminator stored as text + CHECK

*_count
→ cardinality/count, not semantic identity

*_seconds
→ exact elapsed-seconds quantity under the owning contract

*_from_at / *_until_at
→ applicability/current-history interval boundaries
```

Do not introduce:

```text
id
uuid
fk_id
value1/value2
payload
data
meta
flag
kind
status
```

when the exact semantic role is known.

A technical `id` may exist in a later bounded technical object only when `id` is truly its whole technical meaning; it is not the DANTE semantic-identity default.

### 40.7 CP3 constraint/index convention — retained

The existing canonical SQLAlchemy `MetaData` convention remains valid and authoritative:

```text
pk_<table>
fk_<table>_<column(s)>_<referred_table>
uq_<table>_<column(s)>
ix_<table>_<column(s)>
ck_<table>_<semantic_constraint_name>
```

This preserves the current CP3 implementation contract rather than introducing a second convention.

DB-U08 adds only the missing explicit conventions needed by the frozen Part-9 inventory:

```text
ux_<table>_<semantic_key_or_predicate>
→ explicit UNIQUE INDEX that is not a UNIQUE constraint

trg_<table>_<role>
→ ordinary/immediate trigger

ctrg_<table>_<role>
→ deferred PostgreSQL CONSTRAINT TRIGGER
```

No `fn_` prefix is used for routines. Integrity functions use an action verb because the function's semantic behavior is more useful than repeating its catalog type.

### 40.8 Primary-key names — exact

The 68 primary-key constraints, and therefore their backing index names, are exactly:

```text
pk_person
pk_living_referent
pk_asset
pk_place
pk_content_artifact
pk_collective
pk_possibility
pk_goal
pk_plan
pk_activity
pk_event
pk_routine
pk_occurrence
pk_session
pk_observation
pk_native_address
pk_scoped_address
pk_material_state_address
pk_native_current_material_state
pk_scoped_current_material_state
pk_schedule
pk_schedule_placement_state
pk_schedule_placement_date_state
pk_schedule_placement_floating_local_state
pk_schedule_placement_named_zone_state
pk_schedule_placement_absolute_state
pk_schedule_placement_current_history
pk_actual
pk_actual_realization_state
pk_actual_realization_timing
pk_actual_realization_session_basis
pk_actual_realization_current_history
pk_session_timing_state
pk_session_timing_absolute
pk_session_timing_elapsed
pk_session_timing_pause
pk_session_timing_current_history
pk_routine_recurrence_state
pk_event_recurrence_state
pk_routine_recurrence_boundary_state
pk_event_recurrence_boundary_state
pk_routine_recurrence_calendar_state
pk_event_recurrence_calendar_state
pk_routine_recurrence_calendar_wall_time
pk_event_recurrence_calendar_wall_time
pk_routine_recurrence_calendar_weekday
pk_event_recurrence_calendar_weekday
pk_routine_recurrence_calendar_month_day
pk_event_recurrence_calendar_month_day
pk_routine_recurrence_calendar_ordinal_weekday
pk_event_recurrence_calendar_ordinal_weekday
pk_routine_recurrence_calendar_year_month_day
pk_event_recurrence_calendar_year_month_day
pk_routine_recurrence_elapsed_state
pk_event_recurrence_elapsed_state
pk_routine_recurrence_quota_state
pk_event_recurrence_quota_state
pk_routine_recurrence_cyclic_state
pk_event_recurrence_cyclic_state
pk_routine_recurrence_cycle_position
pk_event_recurrence_cycle_position
pk_routine_recurrence_current_history
pk_event_recurrence_current_history
pk_occurrence_generation
pk_occurrence_generation_calendar
pk_occurrence_generation_elapsed
pk_occurrence_generation_quota
pk_occurrence_generation_cyclic
```

All are within the PostgreSQL identifier limit.

### 40.9 Foreign-key naming — deterministic convention + exact long-name aliases

There are 68 frozen baseline FK relationships in the current Part-9 topology.

#### 40.9.1 Short convention-generated FK names

When the canonical CP3 formula fits within 63 bytes, it is the exact final name.

The 17 currently qualifying FK identifiers are:

```text
fk_material_state_address_native_owner_ref_native_address
fk_material_state_address_scoped_owner_ref_scoped_address
fk_schedule_subject_native_ref_native_address
fk_schedule_placement_state_schedule_ref_schedule
fk_schedule_placement_current_history_schedule_ref_schedule
fk_actual_subject_native_ref_native_address
fk_actual_realization_state_actual_ref_actual
fk_actual_realization_session_basis_session_ref_session
fk_actual_realization_current_history_actual_ref_actual
fk_session_timing_state_session_ref_session
fk_session_timing_current_history_session_ref_session
fk_routine_recurrence_state_routine_ref_routine
fk_routine_recurrence_current_history_routine_ref_routine
fk_event_recurrence_state_event_ref_event
fk_event_recurrence_current_history_event_ref_event
fk_occurrence_generation_occurrence_ref_occurrence
fk_occurrence_generation_source_native_ref_native_address
```

#### 40.9.2 Exact semantic aliases for overlength FK names

The remaining 51 relationships would exceed 63 bytes under the full CP3 formula. They therefore receive explicit stable semantic aliases.

These aliases are not arbitrary abbreviations: the owning table already identifies most context, while the suffix identifies the exact target role.

```text
native_current_material_state.native_owner_ref
→ native_address
→ fk_native_current_material_state_owner_address

native_current_material_state.material_state_ref
→ material_state_address
→ fk_native_current_material_state_state_address

scoped_current_material_state.scoped_owner_ref
→ scoped_address
→ fk_scoped_current_material_state_owner_address

scoped_current_material_state.material_state_ref
→ material_state_address
→ fk_scoped_current_material_state_state_address

schedule_placement_state.material_state_ref
→ material_state_address
→ fk_schedule_placement_state_state_address

schedule_placement_date_state.material_state_ref
→ schedule_placement_state
→ fk_schedule_placement_date_state_placement_state

schedule_placement_floating_local_state.material_state_ref
→ schedule_placement_state
→ fk_schedule_placement_floating_local_state_placement_state

schedule_placement_named_zone_state.material_state_ref
→ schedule_placement_state
→ fk_schedule_placement_named_zone_state_placement_state

schedule_placement_absolute_state.material_state_ref
→ schedule_placement_state
→ fk_schedule_placement_absolute_state_placement_state

schedule_placement_current_history.material_state_ref
→ schedule_placement_state
→ fk_schedule_placement_current_history_placement_state

actual_realization_state.material_state_ref
→ material_state_address
→ fk_actual_realization_state_state_address

actual_realization_timing.material_state_ref
→ actual_realization_state
→ fk_actual_realization_timing_actual_state

actual_realization_session_basis.actual_material_state_ref
→ actual_realization_state
→ fk_actual_realization_session_basis_actual_state

actual_realization_session_basis.session_timing_material_state_ref
→ session_timing_state
→ fk_actual_realization_session_basis_timing_state

actual_realization_current_history.material_state_ref
→ actual_realization_state
→ fk_actual_realization_current_history_actual_state

session_timing_state.material_state_ref
→ material_state_address
→ fk_session_timing_state_state_address

session_timing_absolute.material_state_ref
→ session_timing_state
→ fk_session_timing_absolute_timing_state

session_timing_elapsed.material_state_ref
→ session_timing_state
→ fk_session_timing_elapsed_timing_state

session_timing_pause.material_state_ref
→ session_timing_absolute
→ fk_session_timing_pause_timing_absolute

session_timing_current_history.material_state_ref
→ session_timing_state
→ fk_session_timing_current_history_timing_state

routine_recurrence_state.material_state_ref
→ material_state_address
→ fk_routine_recurrence_state_state_address

routine_recurrence_boundary_state.material_state_ref
→ routine_recurrence_state
→ fk_routine_recurrence_boundary_state_recurrence_state

routine_recurrence_calendar_state.material_state_ref
→ routine_recurrence_state
→ fk_routine_recurrence_calendar_state_recurrence_state

routine_recurrence_calendar_wall_time.material_state_ref
→ routine_recurrence_calendar_state
→ fk_routine_recurrence_calendar_wall_time_calendar_state

routine_recurrence_calendar_weekday.material_state_ref
→ routine_recurrence_calendar_state
→ fk_routine_recurrence_calendar_weekday_calendar_state

routine_recurrence_calendar_month_day.material_state_ref
→ routine_recurrence_calendar_state
→ fk_routine_recurrence_calendar_month_day_calendar_state

routine_recurrence_calendar_ordinal_weekday.material_state_ref
→ routine_recurrence_calendar_state
→ fk_routine_recurrence_calendar_ordinal_weekday_calendar_state

routine_recurrence_calendar_year_month_day.material_state_ref
→ routine_recurrence_calendar_state
→ fk_routine_recurrence_calendar_year_month_day_calendar_state

routine_recurrence_elapsed_state.material_state_ref
→ routine_recurrence_state
→ fk_routine_recurrence_elapsed_state_recurrence_state

routine_recurrence_quota_state.material_state_ref
→ routine_recurrence_state
→ fk_routine_recurrence_quota_state_recurrence_state

routine_recurrence_cyclic_state.material_state_ref
→ routine_recurrence_state
→ fk_routine_recurrence_cyclic_state_recurrence_state

routine_recurrence_cycle_position.material_state_ref
→ routine_recurrence_cyclic_state
→ fk_routine_recurrence_cycle_position_cyclic_state

routine_recurrence_current_history.material_state_ref
→ routine_recurrence_state
→ fk_routine_recurrence_current_history_recurrence_state

event_recurrence_state.material_state_ref
→ material_state_address
→ fk_event_recurrence_state_state_address

event_recurrence_boundary_state.material_state_ref
→ event_recurrence_state
→ fk_event_recurrence_boundary_state_recurrence_state

event_recurrence_calendar_state.material_state_ref
→ event_recurrence_state
→ fk_event_recurrence_calendar_state_recurrence_state

event_recurrence_calendar_wall_time.material_state_ref
→ event_recurrence_calendar_state
→ fk_event_recurrence_calendar_wall_time_calendar_state

event_recurrence_calendar_weekday.material_state_ref
→ event_recurrence_calendar_state
→ fk_event_recurrence_calendar_weekday_calendar_state

event_recurrence_calendar_month_day.material_state_ref
→ event_recurrence_calendar_state
→ fk_event_recurrence_calendar_month_day_calendar_state

event_recurrence_calendar_ordinal_weekday.material_state_ref
→ event_recurrence_calendar_state
→ fk_event_recurrence_calendar_ordinal_weekday_calendar_state

event_recurrence_calendar_year_month_day.material_state_ref
→ event_recurrence_calendar_state
→ fk_event_recurrence_calendar_year_month_day_calendar_state

event_recurrence_elapsed_state.material_state_ref
→ event_recurrence_state
→ fk_event_recurrence_elapsed_state_recurrence_state

event_recurrence_quota_state.material_state_ref
→ event_recurrence_state
→ fk_event_recurrence_quota_state_recurrence_state

event_recurrence_cyclic_state.material_state_ref
→ event_recurrence_state
→ fk_event_recurrence_cyclic_state_recurrence_state

event_recurrence_cycle_position.material_state_ref
→ event_recurrence_cyclic_state
→ fk_event_recurrence_cycle_position_cyclic_state

event_recurrence_current_history.material_state_ref
→ event_recurrence_state
→ fk_event_recurrence_current_history_recurrence_state

occurrence_generation.governing_recurrence_state_ref
→ material_state_address
→ fk_occurrence_generation_state_address

occurrence_generation_calendar.occurrence_ref
→ occurrence_generation
→ fk_occurrence_generation_calendar_generation

occurrence_generation_elapsed.occurrence_ref
→ occurrence_generation
→ fk_occurrence_generation_elapsed_generation

occurrence_generation_quota.occurrence_ref
→ occurrence_generation
→ fk_occurrence_generation_quota_generation

occurrence_generation_cyclic.occurrence_ref
→ occurrence_generation
→ fk_occurrence_generation_cyclic_generation
```

The longest explicit FK alias is 61 bytes. Collision count = 0.

Future schema evolution uses the same rule:

```text
full CP3 FK convention <= 63 bytes
→ use full convention

> 63 bytes
→ choose one explicit semantic role alias
→ document it in the same database change
→ no opaque numeric abbreviation
```

### 40.10 UNIQUE constraint and explicit UNIQUE INDEX naming

The two frozen current-binding UNIQUE constraints remain exact convention-generated names:

```text
uq_native_current_material_state_material_state_ref
uq_scoped_current_material_state_material_state_ref
```

For a unique index that is not represented as a PostgreSQL UNIQUE constraint, DANTE uses `ux_`.

Reason:

```text
uq_
→ UNIQUE constraint semantics

ux_
→ explicit unique physical index, including partial uniqueness
```

This distinction improves schema inspection and migration review.

### 40.11 CHECK constraint semantic naming

CHECK constraints use the retained CP3 form:

```text
ck_<table>_<semantic_rule_slug>
```

The semantic slug MUST describe the invariant rather than repeat SQL syntax.

Allowed baseline rule vocabulary includes, when applicable:

```text
one_owner
owner_family
scoped_family
facet_code
temporal_form
extent
interval_order
date_span
resolved_pair
realization_timing
timing_form
start_precision
end_precision
elapsed_positive
elapsed_precision
pause_precision
resume_precision
resume_pair
current_interval
family_code
range_kind
expected_count
boundary_role
boundary_kind
boundary_payload
inclusive_role
pattern_code
interval_positive
clock_basis
zone_basis
step_unit
weekday_range
month_range
month_day_range
ordinal_range
anchor_mode
quota_positive
period_span_positive
period_unit
frame
week_start
cycle_length_positive
position_unit
position_nonnegative
origin_code
governing_state_pair
period_order
```

A table may use only the slugs corresponding to invariants actually frozen for that table.

Forbidden slugs:

```text
valid
check
constraint
rule1
rule2
misc
values
logic
```

Where two different checks on one table would otherwise receive the same slug, the slug must be refined semantically before implementation rather than adding `_2`.

### 40.12 Final 78-index structural-floor names

Part 9 froze a minimum structural floor of 78 indexes. Their identifiers are now exact.

#### Primary-key-backed indexes — 68

The 68 PK-backed index names are the 68 `pk_*` names in section 40.8.

#### UNIQUE-constraint-backed indexes — 2

```text
uq_native_current_material_state_material_state_ref
uq_scoped_current_material_state_material_state_ref
```

#### MaterialState partial lookup indexes — 2

```text
ix_material_state_address_native_owner_ref_facet_code
ix_material_state_address_scoped_owner_ref_facet_code
```

#### Partial unique open-currentness indexes — 5

```text
ux_schedule_placement_current_history_open
ux_actual_realization_current_history_open
ux_session_timing_current_history_open
ux_routine_recurrence_current_history_open
ux_event_recurrence_current_history_open
```

#### Partial unique open-pause index — 1

```text
ux_session_timing_pause_open
```

Count:

```text
68 + 2 + 2 + 5 + 1 = 78
```

All 78 names are collision-free in the `dante` relation namespace. Longest current index identifier = 53 bytes.

DB-U15 remains responsible for deciding whether any additional FK/query/concurrency/lifecycle indexes are justified. Any index DB-U15 adds must follow this naming standard.

### 40.13 Future DB-U15 index naming rule

DB-U15 must not invent another style.

Normal non-unique index:

```text
ix_<table>_<ordered_key_slug>[_<predicate_or_purpose_slug>]
```

Explicit unique index:

```text
ux_<table>_<semantic_key_or_predicate_slug>
```

Rules:

```text
column order in the name follows key order when the name enumerates columns
INCLUDE columns do not automatically enter the name
operator class/access method enters the name only if needed to distinguish materially different indexes
partial predicate gets a semantic suffix such as open/current when that predicate is the reason the index exists
no index receives a UUID/hash suffix as its normal name
```

If the readable index identifier would exceed 63 bytes, DB-U15 must define an explicit semantic alias in its matrix.

### 40.14 Exact integrity-routine names — 14

The 14 bounded integrity routine roles from Part 9 receive these exact schema-local routine identifiers:

```text
1  dante.enforce_native_address_owner
2  dante.enforce_scoped_address_owner
3  dante.enforce_native_ref_eligibility
4  dante.enforce_material_state_totality
5  dante.enforce_current_material_state_binding
6  dante.enforce_current_history_equivalence
7  dante.enforce_owner_creation_completeness
8  dante.enforce_schedule_placement_totality
9  dante.enforce_actual_realization_basis
10 dante.enforce_session_timing_totality
11 dante.enforce_session_pause_consistency
12 dante.enforce_recurrence_aggregate_integrity
13 dante.enforce_occurrence_generation_integrity
14 dante.validate_iana_timezone
```

Routine naming rules:

```text
enforce_
→ function rejects writes that violate an accepted database invariant

validate_
→ bounded value/reference validation helper
```

No overloading by signature is used for these baseline integrity routines.

No generic names such as:

```text
validate_row
check_data
apply_rules
business_rule
validate_entity
```

are allowed.

Longest routine identifier = 39 bytes.

### 40.15 Exact trigger naming — 75 attachments

Trigger prefixes are semantically distinct:

```text
trg_
→ ordinary/immediate trigger

ctrg_
→ PostgreSQL deferred CONSTRAINT TRIGGER
```

The suffix is a controlled role slug. The exact 75 names are frozen below.

#### Role 1 — NativeAddress owner binding

```text
trg_native_address_owner_binding
```

#### Role 2 — ScopedAddress owner binding

```text
trg_scoped_address_owner_binding
```

#### Role 3 — heterogeneous NativeRef eligibility

```text
trg_schedule_native_ref
trg_actual_native_ref
trg_occurrence_generation_native_ref
```

#### Role 4 — MaterialState totality

```text
ctrg_material_state_address_state_totality
ctrg_schedule_placement_state_state_totality
ctrg_actual_realization_state_state_totality
ctrg_session_timing_state_state_totality
ctrg_routine_recurrence_state_state_totality
ctrg_event_recurrence_state_state_totality
```

#### Role 5 — current binding

```text
trg_native_current_material_state_current_binding
trg_scoped_current_material_state_current_binding
```

#### Role 6 — current history equivalence

```text
ctrg_schedule_placement_current_history_current_history
ctrg_actual_realization_current_history_current_history
ctrg_session_timing_current_history_current_history
ctrg_routine_recurrence_current_history_current_history
ctrg_event_recurrence_current_history_current_history
ctrg_native_current_material_state_current_history
ctrg_scoped_current_material_state_current_history
```

The repeated `current_history` in some identifiers is intentional: the first occurrence belongs to the table name; the final occurrence identifies the integrity role.

#### Role 7 — semantic owner creation completeness

```text
ctrg_schedule_owner_complete
ctrg_actual_owner_complete
ctrg_session_owner_complete
ctrg_routine_owner_complete
ctrg_occurrence_owner_complete
```

#### Role 8 — Schedule placement payload totality

```text
ctrg_schedule_placement_state_placement_payload
ctrg_schedule_placement_date_state_placement_payload
ctrg_schedule_placement_floating_local_state_placement_payload
ctrg_schedule_placement_named_zone_state_placement_payload
ctrg_schedule_placement_absolute_state_placement_payload
```

#### Role 9 — Actual exact basis

```text
trg_actual_realization_timing_actual_basis
trg_actual_realization_session_basis_actual_basis
```

#### Role 10 — Session timing totality

```text
ctrg_session_timing_state_timing_payload
ctrg_session_timing_absolute_timing_payload
ctrg_session_timing_elapsed_timing_payload
```

#### Role 11 — Session pause consistency

```text
ctrg_session_timing_pause_pause_consistency
ctrg_session_timing_absolute_pause_consistency
```

#### Role 12 — Routine/Event Recurrence aggregate

```text
ctrg_routine_recurrence_state_recurrence
ctrg_event_recurrence_state_recurrence
ctrg_routine_recurrence_boundary_state_recurrence
ctrg_event_recurrence_boundary_state_recurrence
ctrg_routine_recurrence_calendar_state_recurrence
ctrg_event_recurrence_calendar_state_recurrence
ctrg_routine_recurrence_calendar_wall_time_recurrence
ctrg_event_recurrence_calendar_wall_time_recurrence
ctrg_routine_recurrence_calendar_weekday_recurrence
ctrg_event_recurrence_calendar_weekday_recurrence
ctrg_routine_recurrence_calendar_month_day_recurrence
ctrg_event_recurrence_calendar_month_day_recurrence
ctrg_routine_recurrence_calendar_ordinal_weekday_recurrence
ctrg_event_recurrence_calendar_ordinal_weekday_recurrence
ctrg_routine_recurrence_calendar_year_month_day_recurrence
ctrg_event_recurrence_calendar_year_month_day_recurrence
ctrg_routine_recurrence_elapsed_state_recurrence
ctrg_event_recurrence_elapsed_state_recurrence
ctrg_routine_recurrence_quota_state_recurrence
ctrg_event_recurrence_quota_state_recurrence
ctrg_routine_recurrence_cyclic_state_recurrence
ctrg_event_recurrence_cyclic_state_recurrence
ctrg_routine_recurrence_cycle_position_recurrence
ctrg_event_recurrence_cycle_position_recurrence
```

#### Role 13 — Occurrence generation aggregate

```text
ctrg_occurrence_generation_generation
ctrg_occurrence_generation_calendar_generation
ctrg_occurrence_generation_elapsed_generation
ctrg_occurrence_generation_quota_generation
ctrg_occurrence_generation_cyclic_generation
```

#### Role 14 — IANA timezone validation

```text
trg_schedule_placement_named_zone_state_iana_timezone
trg_routine_recurrence_boundary_state_iana_timezone
trg_event_recurrence_boundary_state_iana_timezone
trg_routine_recurrence_calendar_state_iana_timezone
trg_event_recurrence_calendar_state_iana_timezone
trg_routine_recurrence_quota_state_iana_timezone
trg_event_recurrence_quota_state_iana_timezone
trg_occurrence_generation_calendar_iana_timezone
trg_occurrence_generation_quota_iana_timezone
```

Count reconciliation remains:

```text
ordinary/immediate trigger identifiers   18
constraint-trigger identifiers           57
-------------------------------------------
TOTAL                                     75
```

All 75 trigger names are distinct. Longest trigger identifier = 62 bytes:

```text
ctrg_schedule_placement_floating_local_state_placement_payload
```

No trigger requires PostgreSQL truncation.

### 40.16 Trigger role-slug vocabulary

The exact baseline trigger role slugs are:

```text
owner_binding
native_ref
state_totality
current_binding
current_history
owner_complete
placement_payload
actual_basis
timing_payload
pause_consistency
recurrence
generation
iana_timezone
```

A future trigger must use a similarly bounded semantic role. Generic sequence labels such as `_01` or `_trigger2` are forbidden.

### 40.17 Migration revision/file naming policy

DB-U08 does not allocate future CP6-04 revision IDs because the migration/materialization DAG is a later CP6-03 step.

It freezes the naming policy already established by CP3:

```text
revision ID
YYYYMMDD_NN

file
YYYYMMDD_NN_<bounded_scope_slug>.py
```

Example historical baseline:

```text
revision
20260820_01

file
20260820_01_cp3_persistence_baseline.py
```

Rules:

```text
YYYYMMDD
→ migration-authoring date, not semantic business chronology

NN
→ two-digit collision-free sequence for that date in the canonical DAG

scope_slug
→ short descriptive migration purpose
```

Forbidden:

```text
final.py
fix2.py
new_schema.py
migration_latest.py
random UUID filename
opaque hash-only revision IDs as project convention
```

If concurrent branch work creates an ID collision before integration, one unpublished candidate receives a new revision ID before merge. Applied/merged revision history is never edited merely to improve naming.

### 40.18 SQLAlchemy/Alembic implementation consequence

The future SQLAlchemy mapping plan must consume this standard.

Current CP3 `NAMING_CONVENTION` remains the foundation:

```text
pk
fk
uq
ix
ck
```

Materialization must explicitly name:

```text
all 51 overlength-FK aliases from section 40.9.2
all partial unique `ux_` indexes
all 14 integrity routines
all 75 triggers
```

CHECK constraints must supply the stable semantic `constraint_name` token required by the existing `ck_%(table_name)s_%(constraint_name)s` convention.

Alembic autogenerate remains candidate output only. Generated migration names must be reviewed against this manifest before approval.

This section does **not** choose Python ORM class names or backend module layout. That remains the later SQLAlchemy mapping-plan step.

### 40.19 No hidden semantic meaning in abbreviations

The only compact technical prefixes added/frozen by DB-U08 are:

```text
pk
fk
uq
ck
ix
ux
trg
ctrg
```

Existing semantic suffixes such as `ref`, `at` and `code` retain their already-accepted meanings.

Do not create a private abbreviation dictionary such as:

```text
rcr
msta
schpl
actrlz
ssntm
```

merely to fit 63 bytes.

When a long name needs shortening, remove redundant context through an explicit semantic role alias, as done for the 51 FK exceptions, rather than compressing words into opaque initials.

### 40.20 Reserved-word and quoting preflight

Before CP6-04 emits DDL, automated/static naming QA must check the complete manifest for:

```text
identifier regex compliance
ASCII only
lowercase only
max byte length <= live max_identifier_length
reserved/keyword conflicts
schema-relation namespace collisions
constraint-name collisions in owning scope
routine ambiguity/overload collisions
trigger collisions
Alembic revision collision
```

The current DB-U08 manifest has:

```text
quoted identifiers                         0
uppercase DANTE SQL identifiers            0
known reserved-word conflicts              0
explicit DANTE identifiers > 63 bytes      0
```

### 40.21 Whole-manifest naming QA

Candidate DB-U08 was mechanically checked against the Part-9 inventory.

Results:

```text
DANTE tables                               68 / unchanged
DANTE views                                 5 / unchanged
Part-9 column names                         unchanged

PK identifiers                             68 / unique
frozen FK relationships                    68
  full CP3 convention                      17
  explicit long-name aliases               51
FK identifier collisions                    0
FK identifiers > 63 bytes                   0
longest FK identifier                      61 bytes

frozen structural indexes                  78 / unique
longest current index identifier           53 bytes

integrity routines                         14 / unique
routine overload dependence                 0
longest routine identifier                 39 bytes

trigger attachments                        75 / exact
trigger identifier collisions               0
trigger identifiers > 63 bytes              0
longest trigger identifier                 62 bytes

relation/index namespace collisions         0
quoted-identifier dependency                0
opaque generated naming                     0
semantic object membership change           0
```

Current relation/index manifest checked together:

```text
68 tables
+ 5 views
+ 78 frozen index names
= 151 relation/index identifiers

unique
= 151
```

This is intentionally stronger than relying only on PostgreSQL's narrower per-object namespace rules.

### 40.22 DB-U08 closure

DB-U08 is now closed.

```text
DB-U08
FINAL POSTGRESQL OBJECT NAMING
CLOSED / PASS

TABLE NAMES
FROZEN

COLUMN NAMES
FROZEN

VIEW NAMES
FROZEN

PK NAMES
FROZEN

FK NAMING + LONG-NAME ALIAS MANIFEST
FROZEN

UQ / IX / UX STANDARD
FROZEN

CURRENT 78-INDEX FLOOR NAMES
FROZEN

14 INTEGRITY ROUTINE NAMES
FROZEN

75 TRIGGER NAMES
FROZEN

MIGRATION NAMING POLICY
FROZEN

63-BYTE / QUOTING / COLLISION POLICY
FROZEN
```

No upstream model reopening is required.

The surviving global DB-U register is now exactly:

```text
DB-U15  final structural/query index matrix
DB-U21  exact object-level PostgreSQL privilege matrix
```

### 40.23 Exact next CP6-03 block

The next design block is:

```text
DB-U15 — FINAL STRUCTURAL / QUERY INDEX MATRIX
```

Required sequence remains:

```text
DB-U15 final structural/query index matrix
→ DB-U21 exact object-level privilege matrix
→ migration/materialization DAG
→ SQLAlchemy mapping plan
→ Database Dictionary readiness
→ direct PostgreSQL proof/test plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03 only if clean
```

### 40.24 CP6-04 boundary remains closed

Naming closure is documentation/design only.

```text
Alembic business migration creation      NOT AUTHORIZED
SQLAlchemy business mapping creation     NOT AUTHORIZED
CREATE TABLE / VIEW                      NOT AUTHORIZED
CREATE FUNCTION / TRIGGER                NOT AUTHORIZED
CREATE business indexes                  NOT AUTHORIZED
business ACL materialization             NOT AUTHORIZED
```

CP6-04 remains NOT STARTED / NOT AUTHORIZED.

---

## 41. Current continuation state

The canonical Database Architecture & Reference is now:

```text
Part 1   sections 1–30
Part 2   section 31
Part 3   section 32
Part 4   section 33
Part 5   section 34
Part 6   section 35
Part 7   section 36
Part 8   section 37
Part 9   sections 38–39
Part 10  sections 40–41
```

Current checkpoint state:

```text
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY
FROZEN

DB-U08 FINAL POSTGRESQL OBJECT NAMING
CLOSED

GLOBAL DB-U OPEN
DB-U15
DB-U21

NEXT
DB-U15 FINAL STRUCTURAL / QUERY INDEX MATRIX

SECOND FULL TOMBSTONE AUDIT
NOT YET RUN

GATE 03
NOT YET EARNED

CP6-04
NOT STARTED / NOT AUTHORIZED
```

Part 10 supersedes older CURRENT/resume statements only where those statements still say DB-U08 is open/next. It does not rewrite historical evidence or reopen the Part-9 object inventory.
