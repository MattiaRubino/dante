<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-13.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 14

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / SQLALCHEMY MAPPING PLAN FROZEN  
**Scope:** section 48 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–13  
**PRE-SCOPE for this mapping-plan freeze:** `243175a99052acc6533cc376bef842dceeb13f8a`  
**Current PostgreSQL architecture:** PostgreSQL 18 major family / current technical patch 18.6  
**Current SQLAlchemy line:** 2.0.x / repository resolution 2.0.52 at this checkpoint  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Part 9 froze the surviving PostgreSQL object inventory, Part 10 froze SQL naming, Part 11 froze the complete 95-index matrix, Part 12 froze exact privileges and Part 13 froze the migration/materialization DAG. This continuation freezes the SQLAlchemy representation plan that CP6-04 must consume.

No Python business mapping, Alembic revision, PostgreSQL object, runtime adapter or application use case is created by this checkpoint.

---

## 48. SQLAlchemy Mapping Plan — FROZEN

### 48.1 Purpose

The SQLAlchemy layer represents the accepted PostgreSQL contract to backend code without becoming a second semantic authority.

The mapping plan must preserve all of the following simultaneously:

```text
PostgreSQL remains canonical persistence/material-history authority
one canonical SQLAlchemy Base / MetaData for DANTE tables
Alembic target_metadata remains the same table metadata authority
68 DANTE tables are represented completely
five bounded current views remain capability surfaces, not invented ORM entities
NativeRef / ScopedRecordRef / MaterialStateRef remain distinguishable in Python typing
PostgreSQL types remain explicit where semantic type matters
text + CHECK vocabularies remain text + CHECK
no accidental PostgreSQL ENUM/domain creation
95 physical index contract remains exact
triggers/functions/views remain migration-owned DDL
no ORM event layer duplicates PostgreSQL integrity
no implicit commit or hidden transaction ownership
no generic Repository / UnitOfWork / BaseService abstraction
no ORM cascade exceeds database lifecycle semantics
no relationship/lazy-load graph becomes a second domain model
Base.metadata never advances ahead of the accepted Alembic materialization stage
```

The mapping is implementation infrastructure. `PersonRow`, `RoutineRow`, `ScheduleRow` and similar names MUST NOT be interpreted as Domain model classes.

### 48.2 Existing foundation is retained

The existing canonical foundation remains:

```text
apps/backend/src/dante/platform/database/metadata.py

DANTE_SCHEMA = "dante"
Base(DeclarativeBase)
Base.metadata = MetaData(schema="dante", naming_convention=...)
```

The existing CP3 naming convention remains the common metadata convention:

```text
pk_<table>
fk_<table>_<columns>_<referred_table>
uq_<table>_<columns>
ix_<table>_<columns>
ck_<table>_<semantic_constraint_name>
```

DB-U08 explicit names/aliases remain authoritative whenever an automatically expanded convention name would exceed the PostgreSQL identifier limit or otherwise differs from the frozen explicit name.

No second DeclarativeBase is introduced for DANTE tables.

### 48.3 Planned central database package topology

CP6-04 materializes the technical mapping package under the platform database boundary:

```text
apps/backend/src/dante/platform/database/
├── __init__.py
├── metadata.py
├── references.py
├── locking.py
└── mappings/
    ├── __init__.py
    ├── identity.py
    ├── addressing.py
    ├── schedule.py
    ├── actual.py
    ├── session.py
    ├── recurrence.py
    ├── occurrence.py
    └── views.py
```

This package is not a product-capability module.

Future behavior/cohesion modules remain under the accepted application topology:

```text
dante/modules/<capability>/
  domain/
  application/
  ports/
  adapters/outbound/persistence/
```

Capability-specific persistence adapters may consume these table/view handles. They MUST NOT leak SQLAlchemy row instances into Domain/Application contracts merely because the mapping is centrally available.

### 48.4 Mapping-family allocation

Exactly 68 DANTE tables receive Declarative row mappings.

Allocation:

```text
identity.py      15
addressing.py     5
schedule.py       7
actual.py         5
session.py        5
recurrence.py    26
occurrence.py     5
-------------------
TOTAL            68
```

Migration batching and Python module boundaries are deliberately different concerns. M1..M7 describe dependency-safe materialization order; the modules above describe stable database-family cohesion.

### 48.5 Row-class naming rule

Every mapped DANTE table follows:

```text
SQL table snake_case
→ PascalCase + Row
```

Examples:

```text
person
→ PersonRow

living_referent
→ LivingReferentRow

material_state_address
→ MaterialStateAddressRow

schedule_placement_named_zone_state
→ SchedulePlacementNamedZoneStateRow

routine_recurrence_calendar_ordinal_weekday
→ RoutineRecurrenceCalendarOrdinalWeekdayRow
```

`Row` is mandatory for these technical mappings to avoid accidental equivalence with future Domain concepts/classes.

Baseline mapped attribute names match SQL column names exactly. No broad Python aliasing layer is introduced merely to make ORM names look different from the database.

### 48.6 Exact identity.py manifest — 15 mappings

```text
PersonRow                          → dante.person
LivingReferentRow                  → dante.living_referent
AssetRow                           → dante.asset
PlaceRow                           → dante.place
ContentArtifactRow                 → dante.content_artifact
CollectiveRow                      → dante.collective
PossibilityRow                     → dante.possibility
GoalRow                            → dante.goal
PlanRow                            → dante.plan
ActivityRow                        → dante.activity
EventRow                           → dante.event
RoutineRow                         → dante.routine
OccurrenceRow                      → dante.occurrence
SessionRow                         → dante.session
ObservationRow                     → dante.observation
```

These are identity-shell row mappings only. Class existence MUST NOT be interpreted as generic semantic create authorization. DB-U21 remains authoritative for actual runtime INSERT capability.

### 48.7 Exact addressing.py manifest — five mappings

```text
NativeAddressRow                   → dante.native_address
ScopedAddressRow                   → dante.scoped_address
MaterialStateAddressRow            → dante.material_state_address
NativeCurrentMaterialStateRow       → dante.native_current_material_state
ScopedCurrentMaterialStateRow       → dante.scoped_current_material_state
```

The current-control row classes exist because the tables are part of Base.metadata and the DB contract. Direct runtime DML remains denied; the five bounded views are the mutation surfaces frozen by DB-U21.

### 48.8 Exact schedule.py manifest — seven mappings

```text
ScheduleRow                         → dante.schedule
SchedulePlacementStateRow           → dante.schedule_placement_state
SchedulePlacementDateStateRow       → dante.schedule_placement_date_state
SchedulePlacementFloatingLocalStateRow
                                    → dante.schedule_placement_floating_local_state
SchedulePlacementNamedZoneStateRow  → dante.schedule_placement_named_zone_state
SchedulePlacementAbsoluteStateRow   → dante.schedule_placement_absolute_state
SchedulePlacementCurrentHistoryRow  → dante.schedule_placement_current_history
```

### 48.9 Exact actual.py manifest — five mappings

```text
ActualRow                           → dante.actual
ActualRealizationStateRow           → dante.actual_realization_state
ActualRealizationTimingRow          → dante.actual_realization_timing
ActualRealizationSessionBasisRow    → dante.actual_realization_session_basis
ActualRealizationCurrentHistoryRow  → dante.actual_realization_current_history
```

### 48.10 Exact session.py manifest — five mappings

```text
SessionTimingStateRow               → dante.session_timing_state
SessionTimingAbsoluteRow            → dante.session_timing_absolute
SessionTimingElapsedRow             → dante.session_timing_elapsed
SessionTimingPauseRow               → dante.session_timing_pause
SessionTimingCurrentHistoryRow      → dante.session_timing_current_history
```

`SessionRow` itself remains in `identity.py` because it is one of the 15 LR-01 native identities.

### 48.11 Exact recurrence.py manifest — twenty-six mappings

Routine recurrence:

```text
RoutineRecurrenceStateRow
→ dante.routine_recurrence_state

RoutineRecurrenceCurrentHistoryRow
→ dante.routine_recurrence_current_history

RoutineRecurrenceBoundaryStateRow
→ dante.routine_recurrence_boundary_state

RoutineRecurrenceCalendarStateRow
→ dante.routine_recurrence_calendar_state

RoutineRecurrenceCalendarWallTimeRow
→ dante.routine_recurrence_calendar_wall_time

RoutineRecurrenceCalendarWeekdayRow
→ dante.routine_recurrence_calendar_weekday

RoutineRecurrenceCalendarMonthDayRow
→ dante.routine_recurrence_calendar_month_day

RoutineRecurrenceCalendarOrdinalWeekdayRow
→ dante.routine_recurrence_calendar_ordinal_weekday

RoutineRecurrenceCalendarYearMonthDayRow
→ dante.routine_recurrence_calendar_year_month_day

RoutineRecurrenceElapsedStateRow
→ dante.routine_recurrence_elapsed_state

RoutineRecurrenceQuotaStateRow
→ dante.routine_recurrence_quota_state

RoutineRecurrenceCyclicStateRow
→ dante.routine_recurrence_cyclic_state

RoutineRecurrenceCyclePositionRow
→ dante.routine_recurrence_cycle_position
```

Event recurrence mirrors the same owner-specific shape:

```text
EventRecurrenceStateRow
→ dante.event_recurrence_state

EventRecurrenceCurrentHistoryRow
→ dante.event_recurrence_current_history

EventRecurrenceBoundaryStateRow
→ dante.event_recurrence_boundary_state

EventRecurrenceCalendarStateRow
→ dante.event_recurrence_calendar_state

EventRecurrenceCalendarWallTimeRow
→ dante.event_recurrence_calendar_wall_time

EventRecurrenceCalendarWeekdayRow
→ dante.event_recurrence_calendar_weekday

EventRecurrenceCalendarMonthDayRow
→ dante.event_recurrence_calendar_month_day

EventRecurrenceCalendarOrdinalWeekdayRow
→ dante.event_recurrence_calendar_ordinal_weekday

EventRecurrenceCalendarYearMonthDayRow
→ dante.event_recurrence_calendar_year_month_day

EventRecurrenceElapsedStateRow
→ dante.event_recurrence_elapsed_state

EventRecurrenceQuotaStateRow
→ dante.event_recurrence_quota_state

EventRecurrenceCyclicStateRow
→ dante.event_recurrence_cyclic_state

EventRecurrenceCyclePositionRow
→ dante.event_recurrence_cycle_position
```

No independent `RecurrenceRow` exists because no independent `dante.recurrence` root exists.

### 48.12 Exact occurrence.py manifest — five mappings

```text
OccurrenceGenerationRow             → dante.occurrence_generation
OccurrenceGenerationCalendarRow     → dante.occurrence_generation_calendar
OccurrenceGenerationElapsedRow      → dante.occurrence_generation_elapsed
OccurrenceGenerationQuotaRow        → dante.occurrence_generation_quota
OccurrenceGenerationCyclicRow       → dante.occurrence_generation_cyclic
```

`OccurrenceRow` remains in `identity.py`.

### 48.13 Baseline ORM relationship posture

Baseline declarations:

```text
relationship()                       0
backref/back_populates               0
ORM cascade                           0
delete-orphan                         0
implicit lazy relationship loading    0
```

This is deliberate.

The database already owns referential integrity and lifecycle truth through PK/FK/NO ACTION/constraint/trigger rules. The initial mapping does not create a parallel object graph that can:

```text
issue implicit SELECTs
hide join/filter shape
imply parent/child lifecycle that the DB did not authorize
cascade deletes beyond accepted semantics
turn 68 tables into one giant session-managed object graph
```

Capability adapters query/join by explicit references.

A later bounded `relationship()` may be introduced when a concrete capability demonstrates real value and the relationship configuration remains consistent with the accepted DB lifecycle. That later mapping-only convenience does not change database semantics automatically.

### 48.14 Python reference-family typing

`references.py` defines distinct static types for the three DANTE-owned UUID reference spaces used by this baseline:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
```

They are Python `NewType` wrappers over `uuid.UUID`.

Conceptual contract:

```python
NativeRef = NewType("NativeRef", UUID)
ScopedRecordRef = NewType("ScopedRecordRef", UUID)
MaterialStateRef = NewType("MaterialStateRef", UUID)
```

The canonical Base metadata registers these annotation types explicitly to PostgreSQL `UUID` through SQLAlchemy's type-annotation map.

Physical representation remains:

```text
NativeRef         → PostgreSQL uuid
ScopedRecordRef   → PostgreSQL uuid
MaterialStateRef  → PostgreSQL uuid
```

The distinct Python types exist to prevent accidental reference-family collapse in typed backend code. They do not create PostgreSQL custom domains/types.

Where a UUID column is not one of these semantic reference families, use ordinary `uuid.UUID` rather than forcing every UUID into one of the three aliases.

### 48.15 UUIDv7 issuance

Stable DANTE UUIDv7 identities are application-issued before row construction.

The mapping plan requires explicit factories/helpers, conceptually:

```text
new_native_ref()
new_scoped_record_ref()
new_material_state_ref()
```

They return the corresponding typed UUIDv7 value.

Forbidden baseline shortcuts:

```text
server-side sequence identity
serial/bigserial semantic IDs
hidden database default that mints a DANTE semantic identity
mapped_column(default=...) solely to hide identity issuance until flush
UUID ordering as semantic revision/currentness
```

The operation that establishes a new stable identity therefore has that identity available before constructing the persistence rows and can use the same value across its bounded aggregate inserts.

### 48.16 Exact PostgreSQL type mapping doctrine

Use explicit SQLAlchemy/PostgreSQL types where persisted semantics depend on the SQL type.

Baseline mapping:

```text
PostgreSQL uuid
→ Python uuid.UUID / typed NewType wrappers

text
→ Python str

timestamptz
→ Python datetime with timezone-aware contract
→ DateTime(timezone=True)

timestamp without time zone
→ Python datetime with naive/local-civil contract
→ DateTime(timezone=False)

date
→ Python date
→ Date

time without time zone
→ Python time
→ Time(timezone=False)

boolean
→ Python bool

smallint / integer
→ Python int with exact DB CHECK range where required

numeric
→ Python Decimal
→ Numeric with exact accepted database precision/scale posture from the frozen column contract

daterange
→ PostgreSQL DATERANGE / SQLAlchemy PostgreSQL Range[date]
```

A timezone-aware Python datetime value is required at application boundaries for `timestamptz`; a naive datetime is only valid for columns whose accepted semantics are local/floating civil time.

No conversion of civil date/local time into artificial UTC midnight is introduced by the mapping.

### 48.17 Code/vocabulary fields remain text + CHECK

Fields such as:

```text
owner_family
scoped_family
facet_code
temporal_form_code
extent_code
realization/timing/family/range/pattern/clock/frame codes
precision codes
origin_code
boundary_role / boundary_kind
```

remain mapped as `str` / PostgreSQL `text`.

The accepted vocabularies remain enforced by named DB CHECK constraints.

The baseline MUST NOT let SQLAlchemy automatically convert Python `Enum`/`Literal` annotations into PostgreSQL `ENUM` objects because Part 9 froze:

```text
DANTE custom PostgreSQL enum/domain types = 0
```

A future Python enum used as an application convenience must still bind as text unless a separately reviewed schema evolution intentionally creates a PostgreSQL enum/domain.

### 48.18 Constraint representation

Every table mapping carries the declarative constraints that SQLAlchemy can represent faithfully:

```text
PrimaryKeyConstraint
ForeignKeyConstraint / ForeignKey
UniqueConstraint
CheckConstraint
Index
```

All names must match the DB-U08 frozen names exactly.

When a cross-table or deferred invariant is implemented through the Part-9 integrity layer, the mapping MUST NOT add a fake row-local CheckConstraint that only approximates that invariant.

Database-only trigger/function DDL remains the actual enforcement authority.

### 48.19 Physical index reconciliation in SQLAlchemy metadata

The 95 physical PostgreSQL indexes decompose as:

```text
68 PK-backed indexes
 2 UNIQUE-constraint-backed indexes
25 explicit Index objects
-------------------------------
95 physical indexes
```

Therefore CP6-04 MUST NOT create 95 explicit SQLAlchemy `Index(...)` declarations.

The 25 explicit objects comprise exactly the DB-U15 non-PK/non-UQ indexes, including:

```text
2 material_state_address owner/facet partial indexes
5 one-open-current-history partial unique indexes
1 one-open-session-pause partial unique index
16 additional referencing-side structural/FK indexes
1 occurrence quota-period query/concurrency index
```

PostgreSQL partial predicates are represented with explicit PostgreSQL `postgresql_where` expressions where SQLAlchemy metadata owns the index definition.

Index order/predicate/name must match Part 11 exactly.

### 48.20 Current-view representation — Core only

Exactly five current capability views exist:

```text
dante.schedule_current_placement
dante.actual_current_realization
dante.session_current_timing
dante.routine_current_recurrence
dante.event_current_recurrence
```

They receive **no ORM mapped row classes** in the baseline.

Reason:

```text
view is a bounded current-binding capability surface
!= independent semantic entity
!= independently lifecycle-managed ORM identity
```

Forcing an ORM mapper would require declaring a mapper primary key/identity interpretation for convenience even though PostgreSQL exposes these as automatically-updatable filtered views over the shared current tables.

Instead `views.py` defines five SQLAlchemy Core `Table` handles in a separate metadata collection:

```text
VIEW_METADATA
```

Required properties:

```text
schema = dante
exact exposed columns only
no CREATE TABLE authority
not included in Alembic target_metadata as tables
used explicitly for Core select/insert/update/delete statements
```

The views themselves are created by M5 migration DDL and retain the frozen fixed facet predicates + `WITH LOCAL CHECK OPTION`.

DB-U21 column-scoped DML remains the capability authority.

### 48.21 View DML rule

Capability adapters that mutate current binding use the bounded view handles, not the underlying current-control row mappings.

Examples:

```text
Schedule current placement
→ dante.schedule_current_placement Core handle

Actual current realization
→ dante.actual_current_realization Core handle

Session current timing
→ dante.session_current_timing Core handle
```

Direct SQLAlchemy ORM mutation of `NativeCurrentMaterialStateRow` or `ScopedCurrentMaterialStateRow` by runtime code is forbidden even though those table mappings exist for complete metadata/schema representation.

The database ACL remains the final enforcement layer if application code violates this convention.

### 48.22 PostgreSQL routines/triggers are migration-owned

The 14 frozen integrity routines and 75 trigger attachments are NOT represented as SQLAlchemy ORM events.

Forbidden duplication:

```text
before_insert listener that mirrors PostgreSQL trigger logic
after_insert listener that creates companion state
before_update listener as lifecycle authority
Session event hooks that silently maintain current/history
ORM callback implementation of IANA timezone validation
```

M5/M6 Alembic revisions own exact PostgreSQL function + trigger DDL.

SQLAlchemy row mappings merely expose the tables those database mechanisms protect.

### 48.23 No metadata.create_all deployment authority

`Base.metadata.create_all()` is not a deployment/migration mechanism.

Canonical rule:

```text
Alembic head
→ deployed schema authority

Base.metadata
→ application/schema representation and drift input
```

Tests MAY use metadata construction/introspection for isolated metadata assertions when doing so does not pretend to prove the Alembic deployment path. Fresh-database acceptance remains Alembic-driven.

### 48.24 Explicit mapping registration

Python import side effects must not determine whether Alembic sees all mapped tables.

`mappings/__init__.py` must provide one explicit registration/import boundary, conceptually:

```text
ensure_mappings_loaded()
```

The Alembic environment invokes this boundary before consuming `Base.metadata`.

The backend may also invoke the same loader at an explicit startup/module wiring boundary where complete mapped metadata is needed.

Requirements:

```text
idempotent imports
no database access during import
no engine/session creation during import
no DDL during import
no domain/application side effects
```

### 48.25 Base.metadata MUST NOT advance ahead of Alembic head during CP6-04

CP6-04 materializes migration and mapping in the same bounded implementation batches.

Required progression:

```text
P0
→ provisioning only

M1
→ migration M1 + identity/address mappings introduced together

M2
→ migration M2 + scoped/material-control mappings introduced together

M3
→ migration M3 + Schedule/Actual/Session companion mappings

M4
→ migration M4 + Routine/Event Recurrence mappings

M5
→ migration M5 + Core view handles + mapping registration reconciliation

M6
→ migration M6 + Occurrence-generation mappings

M7
→ migration M7 ACL only; no new row mappings
```

At every reviewed CP6-04 materialization checkpoint:

```text
Base.metadata expected tables
== tables created by Alembic up through that checkpoint
```

The final baseline after M6/M7 is:

```text
Base.metadata DANTE tables       68
VIEW_METADATA handles             5
PostgreSQL DANTE tables          68
PostgreSQL current views          5
```

This rule prevents autogenerate/drift tooling from seeing future tables that the current Alembic head has not yet created.

### 48.26 Mapping state-mutability doctrine

SQLAlchemy row instances are ordinary Python objects; the ORM mapping does not attempt to manufacture semantic immutability through setter interception or ORM events.

Semantic rule remains:

```text
accepted material-state payload
→ append-retained / immutable-by-policy

correction/replacement
→ mint new MaterialStateRef + new semantic state rows

historical state mutation
→ forbidden by ordinary runtime ACL except exact current-history closure column
```

DB-U21 PostgreSQL privileges and Part-9 constraints/triggers remain enforcement authority.

A mutable Python object in memory does not imply an authorized persisted UPDATE.

### 48.27 Transaction/session ownership remains unchanged

Existing runtime contract is preserved:

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation/task
autobegin=False
autoflush=True
expire_on_commit=False
outer application-operation boundary owns commit/rollback
adapter may flush
adapter never commits implicitly
```

Mapped helpers MUST NOT call commit/rollback implicitly.

No generic UnitOfWork wrapper is introduced around the already-explicit AsyncSession transaction boundary.

### 48.28 Advisory-lock helper placement

DB-U21 hardened immutable-owner serialization to transaction-scoped PostgreSQL advisory locks when no truthful mutable row can provide the lock.

The implementation helper belongs in:

```text
dante/platform/database/locking.py
```

It is technical transaction infrastructure, not a Domain owner and not a persisted object.

### 48.29 Advisory-lock key format — FROZEN

DANTE uses the one-argument PostgreSQL advisory lock key form with a non-negative signed `bigint` value.

Key layout is exactly 63 significant bits:

```text
bits 62..56  = 7-bit namespace code
bits 55..0   = 56-bit deterministic digest of semantic reference UUID bytes
```

Equivalent arithmetic definition:

```text
lock_key = (namespace_code << 56) | digest56
```

Constraints:

```text
namespace_code 1..127
bit 63/sign bit remains zero
result fits signed PostgreSQL bigint
same namespace + same UUID always yields same key
namespace separation is collision-free by bit layout
```

### 48.30 Advisory-lock namespace registry — baseline

Frozen codes:

```text
1  schedule.placement current serialization
2  actual.realization current serialization
3  session.timing current serialization
4  routine.recurrence current serialization
5  event.recurrence current serialization
6  Routine occurrence-generation / quota serialization
7  Event occurrence-generation / quota serialization
```

Namespace codes are a technical concurrency registry only. They are not persisted semantic enums and do not become database identity.

A future namespace is appended through reviewed mapping/proof documentation; existing numeric meanings are not reassigned.

### 48.31 Advisory-lock digest algorithm — baseline

The low 56 bits are derived from the referenced UUID's canonical 16 raw bytes through BLAKE2b with:

```text
digest_size = 7 bytes
person      = b"dante-lock-v1"
```

The resulting 7 bytes are interpreted as an unsigned big-endian integer.

Why this shape:

```text
stable across processes/platforms
no Python hash() process randomization
no dependence on PostgreSQL hash implementation details
explicit versioned personalization
large namespace-local key space
```

A same-namespace 56-bit digest collision can only cause two independent resources to serialize unnecessarily. It does not merge semantic identity or allow a conflicting write through because advisory locks are only a serialization mechanism and all normal DB integrity checks remain active.

### 48.32 Advisory-lock acquisition API

The helper exposes a bounded operation conceptually equivalent to:

```text
acquire_advisory_xact_locks(session, lock_keys)
```

Requirements:

```text
AsyncSession transaction already active
session.in_transaction() must be true
helper does not begin transaction
helper does not commit
helper does not rollback
keys are deduplicated
keys are sorted ascending
locks acquired sequentially in ascending numeric order
SQL uses pg_catalog.pg_advisory_xact_lock(bigint)
transaction completion releases locks automatically
```

Deterministic ordering is mandatory when an operation needs more than one DANTE advisory lock so two operations cannot choose opposite application lock order.

### 48.33 Current/history serialization usage

Where the accepted operation needs serialization on an immutable owner and no already-authorized mutable row can truthfully represent the same invariant, use the appropriate namespace above before reading/checking/writing current/history structures.

This does not mean every read acquires an advisory lock.

Locks are for invariant-changing operation sequences such as:

```text
read expected/current MaterialStateRef
validate stale-write basis
close previous current-history interval where applicable
create/select replacement current binding
insert new open history interval
commit
```

If an already-authorized mutable control row can provide the exact same resource lock truthfully, ordinary row locking remains allowed/preferred under DB-U21.

### 48.34 Occurrence-generation concurrency coupling

A recurrence-generated Occurrence operation must serialize both relevant resources before checking/minting/inserting:

For Routine source:

```text
namespace 4 key for RoutineRef
+
namespace 6 key for RoutineRef
```

For Event source:

```text
namespace 5 key for EventRef
+
namespace 7 key for EventRef
```

The keys are deduplicated/sorted numerically and acquired in that order.

Then the transaction performs:

```text
read current governing recurrence binding
verify expected/governing MaterialStateRef
identify exact generation family/coordinate
for quota family: identify exact quota period and count materialized rows using DB-U15 index
require quota capacity remains
mint OccurrenceRef
insert Occurrence + occurrence_generation + exact coordinate row
commit
```

This prevents a concurrent recurrence-current change from being accepted between the governing-state verification and materialization, while the occurrence-generation namespace serializes competing generation/quota writers for that source.

### 48.35 No persistence abstraction inflation

The mapping plan explicitly rejects introducing merely for uniformity:

```text
Repository[T]
generic CRUD repository
generic UnitOfWork wrapper
generic BaseService
generic Entity ORM superclass with semantic fields
one persistence adapter per table mechanically
one capability/module per table mechanically
generic polymorphic reference object that collapses ref families
```

Future adapters are created around actual application behavior/query cohesion after CP6.

### 48.36 SQLAlchemy mapping QA obligations for CP6-04/05

At minimum implementation/direct QA must prove:

```text
MAPPING DISCOVERY
68 / 68 DANTE table mappings registered at final mapping head
exact table/schema names
no unexpected mapped business table
no duplicate table registration
zero baseline relationship() declarations unless separately re-gated

TYPE ALIGNMENT
uuid / typed reference mappings match PostgreSQL uuid
aware/naive temporal mappings match timestamptz/timestamp semantics
date/time/daterange/numeric mappings match exact schema
text+CHECK vocabularies did not create PostgreSQL ENUM/domain objects

CONSTRAINT / INDEX ALIGNMENT
PK/FK/UQ/CHECK names reconcile with frozen inventory/naming
25 explicit Index objects reconcile with DB-U15
68 PK-backed + 2 UQ-backed + 25 explicit = 95 real indexes
no redundant Index object for PK/UQ backing structures

ALEMBIC ALIGNMENT
explicit mapping loader populates target_metadata
Base.metadata is not ahead of active Alembic checkpoint
fresh DB → Alembic head matches final metadata
no metadata.create_all deployment path

VIEW BOUNDARY
five VIEW_METADATA handles
zero current-view ORM row mappings
Core view DML reaches the exact bounded view names
no runtime adapter uses base current-control table as normal current mutation surface

INTEGRITY OWNERSHIP
zero ORM event duplication of the 14 routine / 75 trigger integrity layer
PostgreSQL remains rejection authority

CONCURRENCY HELPER
stable advisory key test vectors
namespace separation test
same UUID/same namespace deterministic key
key range within signed bigint positive range
multiple-key sort/deduplicate behavior
requires active transaction
SQL uses transaction-scoped advisory lock
occurrence operation acquires both recurrence-current and generation namespace locks

TRANSACTION CONTRACT
mapping/helper does not commit implicitly
rollback removes uncommitted writes
session remains operation-scoped
```

Real concurrency behavior against PostgreSQL belongs to the direct proof plan and CP6-05, not a pure unit test alone.

### 48.37 Exact mapping-to-DAG allocation

The planned CP6-04 implementation batches are:

```text
P0
provisioning hardening
mapped table delta: 0

M1
identity.py + NativeAddressRow portion of addressing.py
mapped table delta: 16
cumulative: 16

M2
remaining addressing.py scoped/material/current rows
+ ScheduleRow / ActualRow table owners as required by M2
mapped table delta: 6
cumulative: 22

M3
Schedule/Actual companion mappings + Session timing companion mappings
mapped table delta: 15
cumulative: 37

M4
recurrence.py
mapped table delta: 26
cumulative: 63

M5
views.py five Core handles
mapped table delta: 0
cumulative: 63

M6
occurrence.py generation mappings
mapped table delta: 5
cumulative: 68

M7
ACL only
mapped table delta: 0
cumulative: 68
```

Because `ScheduleRow`, `ActualRow`, `SessionRow`, `RoutineRow`, `EventRow` and `OccurrenceRow` live in stable family modules rather than migration-named modules, implementation commits may touch more than one family file per migration node. The object allocation, not filename exclusivity, is authoritative.

### 48.38 Mapping completeness audit

```text
DANTE TABLES IN FINAL INVENTORY                   68
PLANNED DECLARATIVE ROW MAPPINGS                  68
UNMAPPED DANTE TABLES                              0
EXTRA MAPPED BUSINESS TABLES                       0

CURRENT VIEWS                                      5
PLANNED ORM VIEW MAPPINGS                          0
PLANNED CORE VIEW HANDLES                          5

BASELINE ORM relationship()                        0
BASELINE ORM CASCADE                               0

PHYSICAL POSTGRESQL INDEXES                       95
PK-BACKED                                          68
UQ-BACKED                                           2
EXPLICIT INDEX OBJECTS                             25
INDEX COUNT DRIFT                                   0

POSTGRESQL INTEGRITY ROUTINES                     14
ORM EVENT REIMPLEMENTATIONS                        0
POSTGRESQL TRIGGER ATTACHMENTS                    75
ORM EVENT REIMPLEMENTATIONS                        0

NATIVE / SCOPED / MATERIAL REF TYPE COLLAPSE       0
POSTGRESQL CUSTOM ENUM/DOMAIN INTRODUCED            0
GENERIC REPOSITORY/UOW/BASESERVICE                  0
NEW DOMAIN OWNER                                    0
NEW SEMANTIC DATABASE OBJECT                        0
GLOBAL DB-U OPEN                                    0
```

No Domain/Logical/Physical, inventory, naming, index, ACL or migration-DAG reopen is required.

### 48.39 SQLAlchemy Mapping Plan freeze result

```text
SQLALCHEMY MAPPING PLAN
FROZEN / PASS
```

This freeze gives CP6-04 an exact Python mapping strategy.

It does NOT authorize Python mapping implementation or database materialization.

### 48.40 Exact next CP6-03 block

```text
DATABASE DICTIONARY READINESS
```

Required remaining sequence:

```text
Database Dictionary readiness
→ direct PostgreSQL proof/test plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03 only if clean
```

### 48.41 CP6-04 boundary remains closed

```text
metadata.py implementation change             NOT AUTHORIZED
references.py / locking.py creation            NOT AUTHORIZED
mappings package creation                      NOT AUTHORIZED
Alembic env implementation change              NOT AUTHORIZED
provisioning.py modification                    NOT AUTHORIZED
business migration creation                    NOT AUTHORIZED
CREATE TABLE / VIEW / INDEX                    NOT AUTHORIZED
CREATE FUNCTION / TRIGGER                      NOT AUTHORIZED
GRANT / REVOKE execution                       NOT AUTHORIZED
real PostgreSQL business schema                NOT MATERIALIZED
CP6-04                                         NOT STARTED / NOT AUTHORIZED
```

---

## 49. Current continuation state

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
Part 11  sections 42–43
Part 12  sections 44–45
Part 13  sections 46–47
Part 14  sections 48–49
```

Current checkpoint state:

```text
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY
FROZEN

DB-U08 FINAL POSTGRESQL OBJECT NAMING
CLOSED

DB-U15 FINAL STRUCTURAL / QUERY INDEX MATRIX
CLOSED

DB-U21 EXACT OBJECT-LEVEL PRIVILEGE MATRIX
CLOSED

GLOBAL DB-U OPEN
0

MIGRATION / MATERIALIZATION DAG
FROZEN

SQLALCHEMY MAPPING PLAN
FROZEN

NEXT
DATABASE DICTIONARY READINESS

DIRECT POSTGRESQL PROOF / TEST PLAN
PENDING

SECOND FULL TOMBSTONE AUDIT
NOT YET RUN

GATE 03
NOT YET EARNED

CP6-04
NOT STARTED / NOT AUTHORIZED
```

Part 14 supersedes older CURRENT/resume statements only where they still say SQLAlchemy mapping planning is pending/next or imply that ORM convenience may redefine the accepted PostgreSQL contract.

Historical evidence remains preserved.
