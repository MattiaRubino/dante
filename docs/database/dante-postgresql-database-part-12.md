<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-11.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 12

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / DB-U21 EXACT OBJECT-LEVEL POSTGRESQL PRIVILEGE MATRIX CLOSED  
**Scope:** section 44 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–11  
**PRE-SCOPE for this DB-U21 closure:** `7306c1e3ece0b0f91e71138132c7bd1cd8b34e9f`  
**Current PostgreSQL architecture:** PostgreSQL 18 major family / current technical patch 18.6  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Part 9 froze the final baseline object inventory, Part 10 froze naming and Part 11 froze the 95-index matrix. This continuation closes the last global DB-U axis: exact PostgreSQL ownership and runtime privilege posture for every surviving baseline object class.

No GRANT/REVOKE is executed here. No provisioning code, Alembic migration, SQLAlchemy mapping, table, view, function, trigger or index is created or changed by this document.

---

## 44. DB-U21 — Exact Object-Level PostgreSQL Privilege Matrix — CLOSED

### 44.1 Purpose

The privilege contract is part of the database design.

The baseline must satisfy all of the following simultaneously:

```text
dante_owner owns DANTE schema objects but cannot LOGIN
dante_migrator logs in with NOINHERIT and uses bounded SET ROLE dante_owner
dante_runtime is the application database identity and never receives owner/DDL authority
PUBLIC receives no accidental DANTE capability
migration history remains unavailable to runtime
material/history payloads are append-retained rather than ordinary mutable CRUD
current binding mutation is exposed only through bounded facet views
schema existence does not imply semantic create permission
```

The controlling rule from Checkpoint J remains:

```text
SCHEMA OBJECT EXISTS
!=
SEMANTIC CREATE OPERATION AUTHORIZED
```

DB-U21 therefore does not grant `INSERT` merely because a table exists and does not grant `UPDATE` merely because a row may need to participate in a locking protocol.

### 44.2 PostgreSQL role boundary

The frozen CP3 roles remain:

```text
dante_owner
  NOLOGIN
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
  owns schema dante and all DANTE-owned objects

dante_migrator
  LOGIN
  NOINHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
  membership in dante_owner:
    INHERIT FALSE
    SET TRUE
    ADMIN FALSE

dante_runtime
  LOGIN
  NOINHERIT
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS
  no dante_owner membership
```

No application `Account`, `Principal`, `Actor`, `Authority` or `Visibility` semantics are inferred from these database roles.

### 44.3 Database-level privileges

For the DANTE database:

| Grantee | CONNECT | TEMPORARY | CREATE |
|---|:---:|:---:|:---:|
| `PUBLIC` | NO | NO | NO |
| `dante_runtime` | YES | NO | NO |
| `dante_migrator` | YES | NO | NO |
| `dante_owner` | owner-context only | NO baseline requirement | NO separate database-authority expansion |

`PUBLIC CONNECT` and `PUBLIC TEMPORARY` remain revoked.

Runtime cannot create temporary tables. Migration execution receives database connectivity through `dante_migrator`, then switches to `dante_owner` only for the bounded migration operation.

### 44.4 Schema privileges

#### `dante`

| Grantee | USAGE | CREATE |
|---|:---:|:---:|
| `PUBLIC` | NO | NO |
| `dante_runtime` | YES | NO |
| `dante_migrator` direct | NO | NO |
| `dante_owner` | owner | owner |

`dante_migrator` does not need direct schema authority because migrations execute DDL only after explicit `SET ROLE dante_owner`.

#### `public`

Baseline DANTE posture:

| Grantee | USAGE | CREATE |
|---|:---:|:---:|
| `PUBLIC` | NO | NO |
| `dante_runtime` | NO | NO |
| `dante_migrator` direct | NO | NO |
| `dante_owner` | YES | NO baseline creation need |

The runtime `search_path` MAY remain `dante,public` for compatibility, but lack of `USAGE` means `public` does not become an implicit runtime capability surface.

The currently installed PostGIS, pgvector, pg_trgm, unaccent and pg_stat_statements objects remain extension-owned. Their existence does not imply runtime usage permission. A later DANTE object that genuinely requires an extension must add the exact required schema/object privilege as part of that reviewed capability activation.

### 44.5 Default privileges — deny by default

The current CP3 broad defaults must not survive CP6-04 business materialization.

For objects subsequently created by `dante_owner`, the baseline is:

```text
TABLES
PUBLIC                 none
dante_runtime default  none

SEQUENCES
PUBLIC                 none
dante_runtime default  none

DANTE TYPES / DOMAINS
PUBLIC USAGE           revoked
dante_runtime default  none

DANTE ROUTINES
PUBLIC EXECUTE         revoked
dante_runtime default  none
```

The current CP3 mechanisms equivalent to:

```text
ALTER DEFAULT PRIVILEGES ... GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dante_runtime
ALTER DEFAULT PRIVILEGES ... GRANT USAGE ON SEQUENCES TO dante_runtime
ALTER DEFAULT PRIVILEGES ... GRANT USAGE ON TYPES TO dante_runtime

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA dante TO dante_runtime
GRANT USAGE ON ALL SEQUENCES IN SCHEMA dante TO dante_runtime
```

are implementation debt to be removed in CP6-04.

Provisioning owns role/schema/database hardening. Alembic migrations own exact object ACLs in the same reviewed change that creates or alters each DANTE object.

A provisioning rerun MUST NOT broaden migration-owned business ACLs.

### 44.6 Runtime table privilege doctrine

For all 68 DANTE-owned baseline tables:

```text
SELECT
YES on all 68

INSERT
YES only where the frozen baseline has an accepted insert-bearing persistence operation
NO on 14 exact objects listed below

UPDATE
NO table-level UPDATE anywhere
column-level UPDATE(current_until_at) only on five current-history tables

DELETE
NO on all 68 base tables

TRUNCATE
NO

REFERENCES
NO

TRIGGER
NO

MAINTAIN
NO

GRANT OPTION
NO
```

`SELECT` on all DANTE tables is a database-runtime capability and is not product-level disclosure authorization. Product AuthZ/Visibility remains outside CP6. It is also required by the `SECURITY INVOKER` integrity layer for bounded cross-table validation.

### 44.7 Exact 68-table runtime matrix

| Object | SELECT | INSERT | UPDATE | DELETE |
|---|:---:|:---:|---|:---:|
| `dante.person` | YES | NO | NO | NO |
| `dante.living_referent` | YES | NO | NO | NO |
| `dante.asset` | YES | NO | NO | NO |
| `dante.place` | YES | NO | NO | NO |
| `dante.content_artifact` | YES | NO | NO | NO |
| `dante.collective` | YES | NO | NO | NO |
| `dante.possibility` | YES | NO | NO | NO |
| `dante.goal` | YES | NO | NO | NO |
| `dante.plan` | YES | NO | NO | NO |
| `dante.activity` | YES | NO | NO | NO |
| `dante.event` | YES | NO | NO | NO |
| `dante.routine` | YES | YES | NO | NO |
| `dante.occurrence` | YES | YES | NO | NO |
| `dante.session` | YES | YES | NO | NO |
| `dante.observation` | YES | NO | NO | NO |
| `dante.native_address` | YES | YES | NO | NO |
| `dante.scoped_address` | YES | YES | NO | NO |
| `dante.material_state_address` | YES | YES | NO | NO |
| `dante.native_current_material_state` | YES | NO | NO | NO |
| `dante.scoped_current_material_state` | YES | NO | NO | NO |
| `dante.schedule` | YES | YES | NO | NO |
| `dante.schedule_placement_state` | YES | YES | NO | NO |
| `dante.schedule_placement_date_state` | YES | YES | NO | NO |
| `dante.schedule_placement_floating_local_state` | YES | YES | NO | NO |
| `dante.schedule_placement_named_zone_state` | YES | YES | NO | NO |
| `dante.schedule_placement_absolute_state` | YES | YES | NO | NO |
| `dante.schedule_placement_current_history` | YES | YES | current_until_at only | NO |
| `dante.actual` | YES | YES | NO | NO |
| `dante.actual_realization_state` | YES | YES | NO | NO |
| `dante.actual_realization_timing` | YES | YES | NO | NO |
| `dante.actual_realization_session_basis` | YES | YES | NO | NO |
| `dante.actual_realization_current_history` | YES | YES | current_until_at only | NO |
| `dante.session_timing_state` | YES | YES | NO | NO |
| `dante.session_timing_absolute` | YES | YES | NO | NO |
| `dante.session_timing_elapsed` | YES | YES | NO | NO |
| `dante.session_timing_pause` | YES | YES | NO | NO |
| `dante.session_timing_current_history` | YES | YES | current_until_at only | NO |
| `dante.routine_recurrence_state` | YES | YES | NO | NO |
| `dante.routine_recurrence_boundary_state` | YES | YES | NO | NO |
| `dante.routine_recurrence_calendar_state` | YES | YES | NO | NO |
| `dante.routine_recurrence_calendar_wall_time` | YES | YES | NO | NO |
| `dante.routine_recurrence_calendar_weekday` | YES | YES | NO | NO |
| `dante.routine_recurrence_calendar_month_day` | YES | YES | NO | NO |
| `dante.routine_recurrence_calendar_ordinal_weekday` | YES | YES | NO | NO |
| `dante.routine_recurrence_calendar_year_month_day` | YES | YES | NO | NO |
| `dante.routine_recurrence_elapsed_state` | YES | YES | NO | NO |
| `dante.routine_recurrence_quota_state` | YES | YES | NO | NO |
| `dante.routine_recurrence_cyclic_state` | YES | YES | NO | NO |
| `dante.routine_recurrence_cycle_position` | YES | YES | NO | NO |
| `dante.routine_recurrence_current_history` | YES | YES | current_until_at only | NO |
| `dante.event_recurrence_state` | YES | YES | NO | NO |
| `dante.event_recurrence_boundary_state` | YES | YES | NO | NO |
| `dante.event_recurrence_calendar_state` | YES | YES | NO | NO |
| `dante.event_recurrence_calendar_wall_time` | YES | YES | NO | NO |
| `dante.event_recurrence_calendar_weekday` | YES | YES | NO | NO |
| `dante.event_recurrence_calendar_month_day` | YES | YES | NO | NO |
| `dante.event_recurrence_calendar_ordinal_weekday` | YES | YES | NO | NO |
| `dante.event_recurrence_calendar_year_month_day` | YES | YES | NO | NO |
| `dante.event_recurrence_elapsed_state` | YES | YES | NO | NO |
| `dante.event_recurrence_quota_state` | YES | YES | NO | NO |
| `dante.event_recurrence_cyclic_state` | YES | YES | NO | NO |
| `dante.event_recurrence_cycle_position` | YES | YES | NO | NO |
| `dante.event_recurrence_current_history` | YES | YES | current_until_at only | NO |
| `dante.occurrence_generation` | YES | YES | NO | NO |
| `dante.occurrence_generation_calendar` | YES | YES | NO | NO |
| `dante.occurrence_generation_elapsed` | YES | YES | NO | NO |
| `dante.occurrence_generation_quota` | YES | YES | NO | NO |
| `dante.occurrence_generation_cyclic` | YES | YES | NO | NO |

Count reconciliation:

```text
TABLES                                           68
SELECT YES                                       68
INSERT YES                                       54
INSERT NO                                        14
TABLE-LEVEL UPDATE YES                            0
COLUMN-LEVEL current_until_at UPDATE              5
DELETE YES                                        0
```

### 44.8 Exact no-INSERT set — 14 tables

Runtime `INSERT` is denied on exactly:

```text
dante.person
dante.living_referent
dante.asset
dante.place
dante.content_artifact
dante.collective
dante.possibility
dante.goal
dante.plan
dante.activity
dante.event
dante.observation
dante.native_current_material_state
dante.scoped_current_material_state
```

The first 12 are identity shells whose generic baseline schema does not itself establish a complete semantic creation profile.

This does not mean those concepts can never be created. The first exact product/profile operation that makes creation truthful must introduce its own reviewed runtime capability/ACL change together with the required companion semantics.

`native_current_material_state` and `scoped_current_material_state` are shared control tables and are never direct generic runtime mutation surfaces.

### 44.9 Exact history UPDATE surface — five columns only

Runtime receives no table-level UPDATE on history.

It receives exactly:

```text
UPDATE(current_until_at)
ON dante.schedule_placement_current_history

UPDATE(current_until_at)
ON dante.actual_realization_current_history

UPDATE(current_until_at)
ON dante.session_timing_current_history

UPDATE(current_until_at)
ON dante.routine_recurrence_current_history

UPDATE(current_until_at)
ON dante.event_recurrence_current_history
```

All other columns remain non-updatable by runtime.

The database contract still restricts the semantic transition to:

```text
NULL
→ exact later closure timestamp
```

and integrity machinery rejects invalid chronology/equivalence.

No ordinary runtime DELETE exists for these history tables.

### 44.10 Five bounded current-facet view ACLs

The five views remain owned by `dante_owner`, use the default privilege-checking posture (`security_invoker = false`) and are simple automatically-updatable views over the shared current-control tables.

Each retains its exact fixed facet predicate plus `WITH LOCAL CHECK OPTION`.

This allows the runtime to receive DML on the bounded view while direct mutation of the underlying shared control table remains denied.

#### `dante.schedule_current_placement`

```text
SELECT                                      YES
INSERT(scoped_owner_ref, material_state_ref) YES
UPDATE(material_state_ref)                  YES
DELETE                                      YES
facet_code direct assignment                NO
```

`facet_code` is fixed to `schedule.placement` by the view contract/default + CHECK OPTION.

DELETE means only cessation of the current placement binding. It does not delete the Schedule owner or history.

#### `dante.actual_current_realization`

```text
SELECT                                      YES
INSERT(scoped_owner_ref, material_state_ref) YES
UPDATE(material_state_ref)                  YES
DELETE                                      YES
facet_code direct assignment                NO
```

DELETE represents an accepted no-current Actual gap/retraction where the owner-specific reconciliation contract permits it; history remains retained.

#### `dante.session_current_timing`

```text
SELECT                                      YES
INSERT(native_owner_ref, material_state_ref) YES
UPDATE(material_state_ref)                  YES
DELETE                                      NO
facet_code direct assignment                NO
```

After Session establishment the baseline does not permit an intentional no-current timing gap.

#### `dante.routine_current_recurrence`

```text
SELECT                                      YES
INSERT(native_owner_ref, material_state_ref) YES
UPDATE(material_state_ref)                  YES
DELETE                                      NO
facet_code direct assignment                NO
```

A canonical Routine requires a complete current recurrence contract.

#### `dante.event_current_recurrence`

```text
SELECT                                      YES
INSERT(native_owner_ref, material_state_ref) YES
UPDATE(material_state_ref)                  YES
DELETE                                      NO baseline operation
facet_code direct assignment                NO
```

One-off Event has no recurrence row at all. Once a recurring Event recurrence facet is established, the baseline does not invent a generic recurrence-removal lifecycle through this view.

A future exact Event operation may evolve this DELETE posture if upstream semantics explicitly close such a transition.

### 44.11 View security boundary

The five current views are capability surfaces, not security-invoker mirrors.

Frozen baseline:

```text
view owner                   dante_owner
security_invoker             false
WITH LOCAL CHECK OPTION      yes
runtime base-table DML       no
runtime view DML             exact grants in 44.10
INSTEAD OF triggers          none
```

Therefore PostgreSQL checks the view DML privilege on `dante_runtime` and the underlying relation privilege using the view owner. The runtime does not need direct INSERT/UPDATE/DELETE on the shared current-control tables.

No RLS policy is introduced by this design.

### 44.12 Integrity routine ACLs — exact 14

The frozen integrity routines are:

```text
enforce_native_address_owner
enforce_scoped_address_owner
enforce_native_ref_eligibility
enforce_material_state_totality
enforce_current_material_state_binding
enforce_current_history_equivalence
enforce_owner_creation_completeness
enforce_schedule_placement_totality
enforce_actual_realization_basis
enforce_session_timing_totality
enforce_session_pause_consistency
enforce_recurrence_aggregate_integrity
enforce_occurrence_generation_integrity
validate_iana_timezone
```

Exact baseline:

```text
OWNER                         dante_owner
SECURITY                      INVOKER
PUBLIC EXECUTE                NO
dante_runtime direct EXECUTE  NO
dante_migrator direct EXECUTE NO
dante_owner EXECUTE           owner authority
```

The runtime causes the functions to execute only through their table triggers. They are not callable application APIs.

The trigger creation migration runs after `SET ROLE dante_owner`, so trigger creation has the required function authority without granting direct runtime EXECUTE.

If a future routine genuinely requires privilege elevation, that is a separate `SECURITY DEFINER` security design requiring a fixed safe `search_path`, bounded owner rights and explicit direct tests. No such routine exists in the CP6 baseline.

### 44.13 `dante.alembic_version`

Runtime receives no privileges:

```text
SELECT      NO
INSERT      NO
UPDATE      NO
DELETE      NO
TRUNCATE    NO
REFERENCES  NO
TRIGGER     NO
MAINTAIN    NO
```

The Alembic environment continues to own migration-history access under migrator → owner role transition.

### 44.14 Sequences / custom DANTE types

Part 9 froze:

```text
DANTE sequences               0
DANTE custom enum/domain      0
```

Therefore the baseline runtime object matrix contains no DANTE sequence/type grants.

If a later migration creates a DANTE sequence, type or domain, its runtime privilege is deny-by-default until that migration explicitly proves and grants the required capability.

Extension-owned types are outside the DANTE-owned object count and remain dormant from the baseline runtime privilege surface.

### 44.15 Immutable owner rows and PostgreSQL locking privilege conflict — HARDENED

Earlier blueprint prose used deterministic owner-row locking for some current/history and quota invariants.

PostgreSQL requires `UPDATE` privilege for `SELECT ... FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE` and `FOR KEY SHARE`.

Granting a fake UPDATE privilege on otherwise immutable owner rows solely to obtain a lock would contradict this matrix.

Therefore the baseline is hardened:

```text
immutable owner identity row
→ NO synthetic UPDATE privilege merely for locking
→ NO dummy lock_version column
→ NO lock-only DANTE table
→ NO SECURITY DEFINER lock wrapper solely to bypass ACL
```

Where a transaction requires serialization on an immutable semantic owner and no already-authorized mutable control row can truthfully provide that lock, use a transaction-scoped PostgreSQL advisory lock over a deterministic owner-scoped key.

Required properties:

```text
transaction-level, not session-level
exclusive where the invariant requires single-writer serialization
same semantic owner/invariant always maps to the same key
different owner namespaces cannot collide accidentally
key derivation stable across application processes
lock acquired before read/count/check/write sequence
ordinary transaction rollback/commit releases the lock
no advisory lock becomes semantic identity
```

The exact key derivation/helper placement is a migration/SQLAlchemy/concurrency implementation detail that MUST be frozen before Gate 03 in the mapping/proof-plan blocks.

This narrow hardening supersedes earlier `lock owner row` wording only where executing that row lock as `dante_runtime` would require an otherwise-forbidden UPDATE privilege.

When a transaction already has an authorized mutable control row whose row lock truthfully represents the same concurrency resource, ordinary PostgreSQL row locking remains allowed and preferred.

### 44.16 Quota materialization concurrency consequence

The quota materialization sequence remains semantically unchanged:

```text
serialize exact source/invariant
verify expected/current governing recurrence MaterialStateRef
identify exact quota period
count materialized recurrence-generated Occurrences
require count < quota_count
mint Occurrence UUIDv7
insert occurrence_generation + quota coordinate
commit
```

Only the serialization primitive changes when the source owner row is immutable under runtime ACL:

```text
old generic wording
lock concrete owner row

hardened runtime-compatible implementation
transaction-scoped advisory lock on deterministic source/quota namespace
```

The Part-11 quota-period index remains the query support path for the count.

### 44.17 Provisioning implementation delta required in CP6-04

`apps/backend/src/dante/platform/database/provisioning.py` must be changed in the CP6-04 implementation batch to:

```text
retain
role creation/attributes
migrator SET-role membership
database PUBLIC CONNECT/TEMP hardening
explicit runtime/migrator CONNECT
dante schema ownership
runtime dante USAGE
credentials
PUBLIC routine/type hardening defaults

remove
default runtime CRUD on tables
default runtime sequence USAGE
default runtime type USAGE
GRANT CRUD ON ALL TABLES reconciliation
GRANT USAGE ON ALL SEQUENCES reconciliation

add/harden
PUBLIC USAGE/CREATE posture for public schema
migration-owned ACL non-broadening guarantee
deny-by-default future DANTE object defaults
```

Provisioning remains idempotent but ceases to be business ACL authority.

### 44.18 Existing CP3 acceptance-test impact

The existing CP3 tests intentionally prove the old foundation posture and must evolve in CP6-04.

#### Privilege probe

A fresh owner-owned probe object with no explicit migration/fixture grant must prove:

```text
runtime table DML denied
runtime sequence capability denied
runtime type/domain capability denied where applicable
runtime direct routine EXECUTE denied
provisioning rerun does not broaden ACL
runtime DDL denied
runtime migration-history access denied
```

#### Transaction probe

The transaction fixture still needs a writable technical table.

The fixture therefore explicitly grants only the DML needed by that disposable probe after creating it.

```text
fixture-local probe ACL
!= production default privilege
```

This preserves transaction commit/rollback/savepoint evidence without reintroducing blanket business privileges.

### 44.19 CP6-04 direct PostgreSQL ACL proof obligations

At minimum direct PostgreSQL tests must prove:

```text
ROLE / DATABASE
exact role attributes
migrator membership options
runtime cannot SET ROLE owner
PUBLIC CONNECT denied
PUBLIC TEMP denied
runtime CONNECT yes
runtime TEMP no

SCHEMA
PUBLIC dante USAGE/CREATE denied
runtime dante USAGE yes / CREATE no
PUBLIC public USAGE/CREATE denied
runtime public USAGE/CREATE denied baseline

OWNER / MIGRATOR
every DANTE-owned business/control object owner = dante_owner
migrator direct DDL denied before SET ROLE
migrator SET ROLE owner succeeds
migration-created object ACL exactly matches matrix

TABLES
68/68 runtime SELECT
54/68 exact INSERT allowed
14/68 exact INSERT denied
0 table-level runtime UPDATE
5 exact current_until_at column updates allowed
same history tables: other-column UPDATE denied
68/68 DELETE denied
TRUNCATE/REFERENCES/TRIGGER/MAINTAIN denied

CURRENT VIEWS
all five SELECT allowed
column-scoped INSERT allowed
material_state_ref UPDATE allowed
facet escape rejected by CHECK OPTION
Schedule DELETE allowed
Actual DELETE allowed
Session DELETE denied
Routine DELETE denied
Event DELETE denied
direct base current-table mutation denied

ROUTINES
14/14 owner = dante_owner
14/14 SECURITY INVOKER
14/14 PUBLIC EXECUTE denied
14/14 runtime direct EXECUTE denied
trigger-driven validation still executes successfully

MIGRATION HISTORY
runtime all privileges denied on dante.alembic_version

PROVISIONING
rerun is idempotent
rerun does not broaden any migration-owned object ACL

CONCURRENCY
runtime can execute required accepted current/history/quota operations
immutable owners remain UPDATE-denied
advisory serialization prevents same-owner write races
different owners do not serialize accidentally
rollback releases transaction advisory locks
```

### 44.20 DB-U21 cumulative audit

```text
FINAL OBJECT INVENTORY                       68 tables / 5 views
TABLES CLASSIFIED                            68 / 68
VIEWS CLASSIFIED                              5 / 5
INTEGRITY ROUTINES CLASSIFIED                14 / 14
MIGRATION HISTORY CLASSIFIED                  1 / 1
RUNTIME TABLE SELECT                         68
RUNTIME TABLE INSERT                         54
RUNTIME TABLE NO-INSERT                      14
RUNTIME TABLE-LEVEL UPDATE                    0
RUNTIME HISTORY COLUMN UPDATE                 5
RUNTIME TABLE DELETE                          0
RUNTIME VIEW DELETE                           2
PUBLIC DANTE CAPABILITY                       0
BLANKET DEFAULT BUSINESS GRANTS               0 target
ALL-TABLE/ALL-SEQUENCE RECONCILIATION         0 target
RUNTIME DDL                                   0
RUNTIME DIRECT INTEGRITY EXECUTE              0
FAKE OWNER UPDATE FOR LOCKING                 0
NEW SEMANTIC OBJECT                           0
NEW DOMAIN OWNER                              0
RLS POLICY                                    0
SECURITY DEFINER BASELINE ROUTINE             0
UNCLASSIFIED ACL OBJECT                       0
```

No Domain/Logical/Physical, object inventory, naming or index reopening is required.

### 44.21 DB-U21 closure

```text
DB-U21
CLOSED / PASS

GLOBAL DB-U OPEN
0
```

This is the first CP6-03 point at which every global DB-U item is closed.

It does NOT mean Gate 03 is earned.

Remaining blueprint work is still mandatory.

### 44.22 Exact next CP6-03 block

```text
MIGRATION / MATERIALIZATION DAG
```

Required order:

```text
migration/materialization DAG
→ SQLAlchemy mapping plan
→ Database Dictionary readiness
→ direct PostgreSQL proof/test plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03 only if clean
```

### 44.23 CP6-04 boundary remains closed

This checkpoint is documentation/design only.

```text
provisioning.py modification              NOT AUTHORIZED
test modification                         NOT AUTHORIZED
GRANT / REVOKE execution                 NOT AUTHORIZED
Alembic business migration creation      NOT AUTHORIZED
CREATE TABLE / VIEW / INDEX              NOT AUTHORIZED
CREATE FUNCTION / TRIGGER                NOT AUTHORIZED
SQLAlchemy business mapping creation     NOT AUTHORIZED
CP6-04                                   NOT STARTED / NOT AUTHORIZED
```

---

## 45. Current continuation state

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

NEXT
MIGRATION / MATERIALIZATION DAG

SECOND FULL TOMBSTONE AUDIT
NOT YET RUN

GATE 03
NOT YET EARNED

CP6-04
NOT STARTED / NOT AUTHORIZED
```

Part 12 supersedes older CURRENT/resume statements only where those statements still say DB-U21 is open/next, blanket owner-row locking is required despite runtime ACL conflict, or CP3 blanket business grants may survive business materialization.

Historical evidence remains preserved.
