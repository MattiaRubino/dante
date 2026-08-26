<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-15.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 16

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / DB-U24 IMPLEMENTATION-DETERMINISM HARDENING CLOSED / DIRECT POSTGRESQL PROOF PLAN FROZEN  
**Scope:** section 52 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–15  
**PRE-SCOPE:** `0c67b2877393e68a235448510e6a725718117b05`  
**PostgreSQL target:** PostgreSQL 18 major family / current repository patch 18.6  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Part 15 froze Database Dictionary readiness. A subsequent independent pre-Gate-03 implementation review found that the semantic/object model remained sound but several PostgreSQL facts were not yet implementation-deterministic enough to let Alembic invent nothing while coding. This continuation closes those gaps before the mandatory Second Full Tombstone Audit.

No business migration, SQLAlchemy mapping, PostgreSQL object, runtime adapter or product behavior is created here.

---

## 52. DB-U24 — Final Gate-03 implementation-determinism hardening — CLOSED

### 52.1 Purpose

`DB-U24` is the single bounded hardening item created by the pre-Gate-03 review. Repository search found no prior use of this identifier.

It closes only physical/implementation facts already implied by Parts 9–15 and PostgreSQL 18 behavior. It does **not** reopen Domain, Logical, Physical, CP6-01 or CP6-02 semantics and does not change the frozen object counts:

```text
DANTE tables                         68
ordinary current views                5
integrity routines                   14
trigger attachments                  75
physical indexes                     95
foreign keys                         68
custom DANTE enum/domain/sequence     0
materialized views                    0
RLS policies                          0
```

The hardened axes are:

```text
exact declarative constraint manifest
exact five-view DDL contract
exact trigger physical attachment contract
exact integrity-routine physical contract
stable database error diagnostics
P0 fail-closed enforcement before M1
PostgreSQL 18 UUIDv7 / non-finite value enforcement
Dictionary structural + semantic-validator contract
runtime/migrator technical session envelope
final direct PostgreSQL proof contract
```

### 52.2 PostgreSQL 18 constraint posture

Every baseline PK/FK/UQ/CHECK is enforced. CP6-04 MUST NOT use PostgreSQL 18 `NOT ENFORCED` for a DANTE baseline constraint.

Frozen physical properties:

```text
68 PRIMARY KEY constraints
→ NOT DEFERRABLE
→ ENFORCED

2 UNIQUE constraints
→ NOT DEFERRABLE
→ ENFORCED

68 FOREIGN KEY constraints
→ exact names/columns/targets already frozen in Part 10
→ MATCH SIMPLE
→ ON UPDATE NO ACTION
→ ON DELETE NO ACTION
→ NOT DEFERRABLE
→ ENFORCED
→ VALID

120 CHECK constraints
→ exact manifest in 52.4–52.10
→ ENFORCED
→ VALID
→ NO INHERIT = false

EXCLUDE constraints
→ 0
```

The 57 deferred invariants remain PostgreSQL constraint triggers rather than DEFERRABLE FK/UQ substitutions.

### 52.3 UUIDv7 root enforcement — exact 18 CHECKs

UUIDv7 issuance remains application-boundary-first, but PostgreSQL 18 additionally rejects a non-v7 identifier at the semantic identity roots.

Exact expression form:

```sql
uuid_extract_version(<root_ref>) IS NOT DISTINCT FROM 7
```

`IS NOT DISTINCT FROM` is deliberate: non-RFC UUID versions that yield NULL must also reject rather than pass PostgreSQL CHECK three-valued logic.

Exact constraints:

```text
ck_person_uuidv7
ck_living_referent_uuidv7
ck_asset_uuidv7
ck_place_uuidv7
ck_content_artifact_uuidv7
ck_collective_uuidv7
ck_possibility_uuidv7
ck_goal_uuidv7
ck_plan_uuidv7
ck_activity_uuidv7
ck_event_uuidv7
ck_routine_uuidv7
ck_occurrence_uuidv7
ck_session_uuidv7
ck_observation_uuidv7
ck_schedule_uuidv7
ck_actual_uuidv7
ck_material_state_address_uuidv7
```

They apply respectively to each table's native/scoped/material identity PK column. Projection/reference rows (`native_address`, `scoped_address`, current/history/payload rows) do not repeat UUID-version CHECKs because their identity already binds through the exact authoritative owner/address FK/dispatcher contract.

### 52.4 Shared control CHECK manifest — exact 6

```text
ck_native_address_owner_family
owner_family IN (
  'person','living_referent','asset','place','content_artifact',
  'collective','possibility','goal','plan','activity','event',
  'routine','occurrence','session','observation'
)

ck_scoped_address_scoped_family
scoped_family IN ('schedule','actual')

ck_material_state_address_one_owner
num_nonnulls(native_owner_ref, scoped_owner_ref) = 1

ck_material_state_address_facet_code
facet_code IN (
  'schedule.placement','actual.realization','session.timing',
  'routine.recurrence','event.recurrence'
)

ck_native_current_material_state_facet_code
facet_code IN ('session.timing','routine.recurrence','event.recurrence')

ck_scoped_current_material_state_facet_code
facet_code IN ('schedule.placement','actual.realization')
```

Together with the 18 UUIDv7 checks the cumulative CHECK count is 24.

### 52.5 Schedule CHECK manifest — exact 10

```text
ck_schedule_placement_state_temporal_form
  temporal_form_code IN ('date_span','floating_local','named_zone_local','absolute')

ck_schedule_placement_date_state_date_span
  NOT isempty(date_span)
  AND NOT lower_inf(date_span)
  AND NOT upper_inf(date_span)
  AND lower_inc(date_span)
  AND NOT upper_inc(date_span)
  AND isfinite(lower(date_span))
  AND isfinite(upper(date_span))

ck_schedule_placement_floating_local_state_extent
ck_schedule_placement_named_zone_state_extent
ck_schedule_placement_absolute_state_extent
  each: extent_code IN ('point','start_only','interval')

ck_schedule_placement_floating_local_state_interval_order
  isfinite(starts_local_at)
  AND (
    (extent_code IN ('point','start_only') AND ends_local_at IS NULL)
    OR
    (extent_code='interval' AND ends_local_at IS NOT NULL
     AND isfinite(ends_local_at) AND ends_local_at > starts_local_at)
  )

ck_schedule_placement_named_zone_state_interval_order
  same exact extent/order expression over starts_local_at / ends_local_at

ck_schedule_placement_named_zone_state_resolved_pair
  (resolved_start_at IS NULL OR isfinite(resolved_start_at))
  AND (
    resolved_end_at IS NULL
    OR (resolved_start_at IS NOT NULL AND extent_code='interval'
        AND isfinite(resolved_end_at) AND resolved_end_at > resolved_start_at)
  )

ck_schedule_placement_absolute_state_interval_order
  isfinite(starts_at)
  AND (
    (extent_code IN ('point','start_only') AND ends_at IS NULL)
    OR
    (extent_code='interval' AND ends_at IS NOT NULL
     AND isfinite(ends_at) AND ends_at > starts_at)
  )

ck_schedule_placement_current_history_current_interval
  isfinite(current_from_at)
  AND (current_until_at IS NULL
       OR (isfinite(current_until_at) AND current_until_at > current_from_at))
```

The named-zone trigger additionally proves actual IANA/local-resolution semantics; the CHECKs above own only row-local shape.

Cumulative CHECK count: 34.

### 52.6 Actual CHECK manifest — exact 3

```text
ck_actual_realization_timing_extent
  extent_code IN ('instant','start_only','interval')

ck_actual_realization_timing_interval_order
  isfinite(started_at)
  AND (
    (extent_code IN ('instant','start_only') AND ended_at IS NULL)
    OR
    (extent_code='interval' AND ended_at IS NOT NULL
     AND isfinite(ended_at) AND ended_at > started_at)
  )

ck_actual_realization_current_history_current_interval
  isfinite(current_from_at)
  AND (current_until_at IS NULL
       OR (isfinite(current_until_at) AND current_until_at > current_from_at))
```

`actual_realization_state` and `actual_realization_session_basis` intentionally have no row-local CHECK beyond native PostgreSQL NOT NULL/PK/FK semantics; their cross-table basis/realization rules belong to the frozen trigger layer.

Cumulative CHECK count: 37.

### 52.7 Session CHECK manifest — exact 10

The exact Session precision set is:

```text
'exact','approximate','rounded'
```

Manifest:

```text
ck_session_timing_state_timing_form
  timing_form_code IN ('absolute','elapsed_only')

ck_session_timing_absolute_start_precision
  start_precision_code IN ('exact','approximate','rounded')
  AND isfinite(started_at)

ck_session_timing_absolute_end_precision
  (ended_at IS NULL AND end_precision_code IS NULL)
  OR
  (ended_at IS NOT NULL AND isfinite(ended_at)
   AND end_precision_code IN ('exact','approximate','rounded'))

ck_session_timing_absolute_interval_order
  ended_at IS NULL OR ended_at > started_at

ck_session_timing_elapsed_elapsed_positive
  elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric)
  AND elapsed_seconds > 0

ck_session_timing_elapsed_elapsed_precision
  elapsed_precision_code IN ('exact','approximate','rounded')

ck_session_timing_pause_pause_precision
  pause_precision_code IN ('exact','approximate','rounded')
  AND isfinite(paused_at)

ck_session_timing_pause_resume_precision
  resume_precision_code IS NULL
  OR resume_precision_code IN ('exact','approximate','rounded')

ck_session_timing_pause_resume_pair
  (resumed_at IS NULL AND resume_precision_code IS NULL)
  OR
  (resumed_at IS NOT NULL AND isfinite(resumed_at)
   AND resume_precision_code IS NOT NULL AND resumed_at > paused_at)

ck_session_timing_current_history_current_interval
  isfinite(current_from_at)
  AND (current_until_at IS NULL
       OR (isfinite(current_until_at) AND current_until_at > current_from_at))
```

The explicit `NaN/±Infinity` rejection is required because PostgreSQL `numeric` supports those special values and a plain `> 0` is not sufficient as the whole finite-value contract.

Cumulative CHECK count: 47.

### 52.8 Routine/Event Recurrence CHECK manifest — exact symmetric 31 + 31 = 62

For each owner prefix `X ∈ {routine,event}`, instantiate the following exact table/name/expression matrix by replacing `<x>` with the lower-case prefix. The expansion is normative and produces 31 checks per owner, not a naming suggestion.

#### State — 3

```text
ck_<x>_recurrence_state_family_code
  family_code IN ('calendar_wall_clock','elapsed_interval','quota_per_period','cyclic_positional')

ck_<x>_recurrence_state_range_kind
  range_kind IN ('open','until_boundary','expected_count')

ck_<x>_recurrence_state_expected_count
  (range_kind='expected_count'
   AND expected_occurrence_count IS NOT NULL
   AND expected_occurrence_count > 0)
  OR
  (range_kind IN ('open','until_boundary')
   AND expected_occurrence_count IS NULL)
```

#### Boundary — 4

```text
ck_<x>_recurrence_boundary_state_boundary_role
  boundary_role IN ('pattern_anchor','effective_from','effective_until')

ck_<x>_recurrence_boundary_state_boundary_kind
  boundary_kind IN ('date','floating_local','named_zone_local','absolute_instant')

ck_<x>_recurrence_boundary_state_boundary_payload
  exact disjunction:
  date
    → date_value IS NOT NULL AND isfinite(date_value)
      AND local_value/zone_id/instant_value/resolved_at ARE NULL
  floating_local
    → local_value IS NOT NULL AND isfinite(local_value)
      AND date_value/zone_id/instant_value/resolved_at ARE NULL
  named_zone_local
    → local_value IS NOT NULL AND isfinite(local_value)
      AND zone_id IS NOT NULL
      AND date_value/instant_value ARE NULL
      AND (resolved_at IS NULL OR isfinite(resolved_at))
  absolute_instant
    → instant_value IS NOT NULL AND isfinite(instant_value)
      AND date_value/local_value/zone_id/resolved_at ARE NULL

ck_<x>_recurrence_boundary_state_inclusive_role
  (boundary_role='pattern_anchor' AND inclusive IS NULL)
  OR
  (boundary_role IN ('effective_from','effective_until') AND inclusive IS NOT NULL)
```

The implementation expression for `boundary_payload` MUST be the direct SQL OR-of-four predicates above; no helper JSON or generic dynamic rule engine is permitted.

#### Calendar envelope — 5

```text
ck_<x>_recurrence_calendar_state_pattern_code
  pattern_code IN ('daily','weekly_weekdays','monthly_month_days',
                   'monthly_ordinal_weekdays','yearly_month_days','anchor_step')

ck_<x>_recurrence_calendar_state_interval_positive
  interval_count > 0

ck_<x>_recurrence_calendar_state_clock_basis
  clock_basis_code IN ('floating_local','named_zone','absolute_utc')

ck_<x>_recurrence_calendar_state_zone_basis
  (clock_basis_code='named_zone' AND zone_id IS NOT NULL)
  OR
  (clock_basis_code IN ('floating_local','absolute_utc') AND zone_id IS NULL)

ck_<x>_recurrence_calendar_state_step_unit
  (pattern_code='anchor_step' AND step_unit_code IN ('day','week','month','year'))
  OR
  (pattern_code<>'anchor_step' AND step_unit_code IS NULL)
```

#### Selector scalar checks — 6

```text
ck_<x>_recurrence_calendar_weekday_weekday_range
  weekday_number BETWEEN 1 AND 7

ck_<x>_recurrence_calendar_month_day_month_day_range
  month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1

ck_<x>_recurrence_calendar_ordinal_weekday_weekday_range
  weekday_number BETWEEN 1 AND 7

ck_<x>_recurrence_calendar_ordinal_weekday_ordinal_range
  ordinal BETWEEN -5 AND 5 AND ordinal <> 0

ck_<x>_recurrence_calendar_year_month_day_month_range
  month_number BETWEEN 1 AND 12

ck_<x>_recurrence_calendar_year_month_day_month_day_range
  month_day BETWEEN 1 AND 31 OR month_day BETWEEN -31 AND -1
```

The two calendar-wall-time tables intentionally need no row-local CHECK: `time without time zone` plus PK/FK/NOT NULL already gives the complete scalar row shape; aggregate selector/family requirements remain deferred.

#### Elapsed — 3

```text
ck_<x>_recurrence_elapsed_state_elapsed_positive
  elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric)
  AND elapsed_seconds > 0

ck_<x>_recurrence_elapsed_state_anchor_mode
  anchor_mode_code IN ('fixed_anchor','previous_expected')

ck_<x>_recurrence_elapsed_state_anchor_at
  isfinite(anchor_at)
```

#### Quota — 6

```text
ck_<x>_recurrence_quota_state_quota_positive
  quota_count > 0

ck_<x>_recurrence_quota_state_period_span_positive
  period_span > 0

ck_<x>_recurrence_quota_state_period_unit
  period_unit_code IN ('day','week','month','year')

ck_<x>_recurrence_quota_state_frame
  frame_code IN ('floating_local','named_zone','absolute_utc')

ck_<x>_recurrence_quota_state_zone_basis
  (frame_code='named_zone' AND zone_id IS NOT NULL)
  OR
  (frame_code IN ('floating_local','absolute_utc') AND zone_id IS NULL)

ck_<x>_recurrence_quota_state_week_start
  (period_unit_code='week' AND week_start BETWEEN 1 AND 7)
  OR
  (period_unit_code<>'week' AND week_start IS NULL)
```

#### Cyclic — 3

```text
ck_<x>_recurrence_cyclic_state_cycle_length_positive
  cycle_length > 0

ck_<x>_recurrence_cyclic_state_position_unit
  position_unit_code IN ('day','week')

ck_<x>_recurrence_cycle_position_position_nonnegative
  position_index >= 0
```

#### Current history — 1

```text
ck_<x>_recurrence_current_history_current_interval
  isfinite(current_from_at)
  AND (current_until_at IS NULL
       OR (isfinite(current_until_at) AND current_until_at > current_from_at))
```

Per-owner reconciliation:

```text
state 3 + boundary 4 + calendar 5 + selectors 6 + elapsed 3
+ quota 6 + cyclic 3 + history 1
= 31

Routine + Event
= 62
```

Cumulative CHECK count: 109.

### 52.9 Occurrence-generation CHECK manifest — exact 11

```text
ck_occurrence_generation_origin_code
  origin_code IN ('recurrence_generated','explicit_extra')

ck_occurrence_generation_governing_state_pair
  (origin_code='recurrence_generated' AND governing_recurrence_state_ref IS NOT NULL)
  OR
  (origin_code='explicit_extra' AND governing_recurrence_state_ref IS NULL)

ck_occurrence_generation_calendar_clock_basis
  clock_basis_code IN ('floating_local','named_zone','absolute_utc')

ck_occurrence_generation_calendar_zone_basis
  (clock_basis_code='named_zone' AND zone_id IS NOT NULL)
  OR
  (clock_basis_code IN ('floating_local','absolute_utc') AND zone_id IS NULL)

ck_occurrence_generation_calendar_resolved_pair
  isfinite(generated_date)
  AND (resolved_at IS NULL
       OR (clock_basis_code='named_zone' AND isfinite(resolved_at)))

ck_occurrence_generation_elapsed_expected_at
  isfinite(expected_at)

ck_occurrence_generation_quota_period_order
  isfinite(period_start_date)
  AND isfinite(period_end_date_exclusive)
  AND period_end_date_exclusive > period_start_date

ck_occurrence_generation_quota_frame
  frame_code IN ('floating_local','named_zone','absolute_utc')

ck_occurrence_generation_quota_zone_basis
  (frame_code='named_zone' AND zone_id IS NOT NULL)
  OR
  (frame_code IN ('floating_local','absolute_utc') AND zone_id IS NULL)

ck_occurrence_generation_cyclic_generated_date
  isfinite(generated_date)

ck_occurrence_generation_cyclic_position_nonnegative
  position_index >= 0
```

Final CHECK reconciliation:

```text
UUIDv7 roots                 18
shared controls               6
Schedule                     10
Actual                        3
Session                      10
Routine recurrence           31
Event recurrence             31
Occurrence generation        11
-------------------------------
TOTAL                       120
```

Exactly four of the 68 tables have no row-local CHECK:

```text
actual_realization_state
actual_realization_session_basis
routine_recurrence_calendar_wall_time
event_recurrence_calendar_wall_time
```

Their required invariants remain fully covered by NOT NULL/PK/FK and/or the bounded trigger layer.

No CHECK identifier in this manifest exceeds PostgreSQL's 63-byte baseline identifier ceiling; the longest is 61 bytes.

### 52.10 Non-finite date/time doctrine

DANTE baseline semantic time does not use PostgreSQL special `infinity` / `-infinity` values as alternate open-ended semantics.

```text
open-ended semantic interval
→ NULL / extent/range-kind semantics already frozen

PostgreSQL date/timestamp infinity
→ REJECT on canonical baseline date/timestamp boundaries where a finite fact is required
```

The CHECK manifest above therefore uses `isfinite(...)` on canonical date/timestamp boundaries and finite range bounds.

This does not prohibit PostgreSQL's type capability globally; it prohibits silently introducing a second DANTE missingness/open-ended encoding.

### 52.11 Five current views — exact physical DDL contract

The five views expose exactly the three base columns, in this order:

```text
schedule_current_placement
actual_current_realization
  → scoped_owner_ref, facet_code, material_state_ref

session_current_timing
routine_current_recurrence
event_current_recurrence
  → native_owner_ref, facet_code, material_state_ref
```

Each is an ordinary simple automatically-updatable view over exactly one shared current table with:

```text
security_invoker  = false
security_barrier  = false
CHECK OPTION      = LOCAL
INSTEAD OF trigger = none
owner             = dante_owner
```

Exact predicates and view-local defaults:

```text
schedule_current_placement
WHERE facet_code = 'schedule.placement'
ALTER VIEW ... ALTER COLUMN facet_code SET DEFAULT 'schedule.placement'

actual_current_realization
WHERE facet_code = 'actual.realization'
ALTER VIEW ... ALTER COLUMN facet_code SET DEFAULT 'actual.realization'

session_current_timing
WHERE facet_code = 'session.timing'
ALTER VIEW ... ALTER COLUMN facet_code SET DEFAULT 'session.timing'

routine_current_recurrence
WHERE facet_code = 'routine.recurrence'
ALTER VIEW ... ALTER COLUMN facet_code SET DEFAULT 'routine.recurrence'

event_current_recurrence
WHERE facet_code = 'event.recurrence'
ALTER VIEW ... ALTER COLUMN facet_code SET DEFAULT 'event.recurrence'
```

The default is required because DB-U21 intentionally grants INSERT only on owner ref + material_state_ref and does not grant direct assignment of `facet_code`. `LOCAL CHECK OPTION` prevents any insert/update from escaping the fixed facet.

### 52.12 Exact integrity-routine physical contract — all 14

The existing 14 names from DB-U08 are unchanged:

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

Every baseline routine is exactly:

```text
routine kind       FUNCTION
arguments          none: ()
return type        trigger
language           plpgsql
security           SECURITY INVOKER
volatility         VOLATILE
parallel safety    PARALLEL UNSAFE
leakproof          false
owner              dante_owner
function search_path  pg_catalog, dante
PUBLIC EXECUTE     revoked
dante_runtime EXECUTE revoked
dante_migrator direct EXECUTE revoked
```

No overloaded baseline routine name is permitted.

Dispatcher implementations use static bounded `CASE`/schema-qualified SQL over the exact frozen owner/family set. Generic dynamic SQL over arbitrary table/type names is forbidden.

No routine owns business workflow, transaction begin/commit/rollback, retry or external side effect.

### 52.13 Stable trigger error contract

Trigger-raised invariant errors are machine-diagnostic. Backend/tests MUST NOT parse human message text.

Frozen mapping:

```text
reference/address/family eligibility violations
roles 1 / 2 / 3
→ SQLSTATE 23503 (foreign_key_violation class)

all other trigger-owned invariant violations
roles 4..14
→ SQLSTATE 23514 (check_violation class)

native PK/UQ/FK/CHECK failures
→ PostgreSQL native SQLSTATE, including 23505 / 23503 / 23514 as applicable
```

For explicit trigger `RAISE` diagnostics:

```text
CONSTRAINT = exact TG_NAME
TABLE      = exact TG_TABLE_NAME
SCHEMA     = TG_TABLE_SCHEMA where supported
DETAIL     = bounded non-secret invariant context
MESSAGE    = human diagnostic only; not an API contract
```

Tests assert SQLSTATE and diagnostic object identifiers, not locale/message text.

### 52.14 Exact trigger physical topology

All 75 baseline triggers are:

```text
orientation       ROW
arguments         []
WHEN condition    none baseline
execution enabled ORIGIN
```

No invariant may depend on PostgreSQL's alphabetical trigger firing order. Multiple applicable triggers must be semantically independent/commutative validators over the same accepted transaction state.

#### Ordinary/immediate — exact 18

All ordinary triggers use `BEFORE ROW`, are not constraint triggers, and are not deferrable.

```text
Role 1 — native address owner binding — 1
native_address
  INSERT OR UPDATE OF native_ref, owner_family

Role 2 — scoped address owner binding — 1
scoped_address
  INSERT OR UPDATE OF scoped_ref, scoped_family

Role 3 — heterogeneous NativeRef eligibility — 3
schedule
  INSERT OR UPDATE OF subject_native_ref
actual
  INSERT OR UPDATE OF subject_native_ref
occurrence_generation
  INSERT OR UPDATE OF source_native_ref

Role 5 — shared current binding — 2
native_current_material_state
  INSERT OR UPDATE OF native_owner_ref, facet_code, material_state_ref
scoped_current_material_state
  INSERT OR UPDATE OF scoped_owner_ref, facet_code, material_state_ref

Role 9 — Actual exact basis — 2
actual_realization_timing
  INSERT OR UPDATE
actual_realization_session_basis
  INSERT OR UPDATE

Role 14 — IANA/local-time validation — 9
schedule_placement_named_zone_state
routine_recurrence_boundary_state
event_recurrence_boundary_state
routine_recurrence_calendar_state
event_recurrence_calendar_state
routine_recurrence_quota_state
event_recurrence_quota_state
occurrence_generation_calendar
occurrence_generation_quota
  each: INSERT OR UPDATE OF its relevant zone/frame/local/resolved fields
```

Exact trigger names remain the 18 `trg_*` identifiers in Part 10 section 40.15.

#### Deferred constraint triggers — exact 57

All use:

```text
AFTER ROW
CONSTRAINT TRIGGER
DEFERRABLE
INITIALLY DEFERRED
INSERT OR UPDATE OR DELETE
```

except Role 7 owner-completeness triggers, which fire on INSERT only because ordinary runtime owner UPDATE/DELETE is not an owner-creation event.

Attachment counts remain:

```text
Role 4  MaterialState totality                  6  I/U/D
Role 6  current/history equivalence             7  I/U/D
Role 7  owner creation completeness             5  INSERT
Role 8  Schedule payload totality               5  I/U/D
Role 10 Session payload totality                3  I/U/D
Role 11 Session pause consistency               2  I/U/D
Role 12 Routine/Event recurrence aggregate     24  I/U/D
Role 13 Occurrence-generation aggregate         5  I/U/D
-------------------------------------------------
TOTAL                                           57
```

Exact table attachments and `ctrg_*` names remain the Part 9 / Part 10 75-attachment ledger.

### 52.15 Deferred-trigger execution-quality rule

Constraint triggers are row-level PostgreSQL mechanics. CP6-04 implementations MUST therefore obey:

```text
validator lookup begins from exact affected owner/material state
all repeated relation lookups use the already-frozen PK/UQ/index paths
no trigger performs an unbounded global table scan for correctness
no invariant depends on which applicable trigger fires first
aggregate scans are bounded to the exact affected aggregate
```

CP6-05 measures representative/worst-case selector/position collections before accepting an implementation that repeatedly rescans a potentially large aggregate. This requirement does not authorize speculative new indexes or a generic statement-level shadow framework.

### 52.16 Native/scoped dispatcher reverse-continuity boundary

The pre-Gate03 review rechecked the asymmetric dispatcher topology.

```text
address INSERT/UPDATE
→ bounded trigger proves concrete owner exists/family matches

heterogeneous consumer
→ FK address + bounded family eligibility

ordinary runtime owner DELETE
→ denied by DB-U21
```

No additional baseline owner-delete trigger family is added merely to increase trigger count. Trusted migration/owner destructive changes remain governed operations and CP6-05 integrity scans must prove no orphan/mismatched address after migration/restore-style work. Future owner-specific destructive lifecycle evolution must preserve or remove address continuity truthfully.

The frozen 75-trigger topology therefore remains unchanged.

### 52.17 Named-zone and DST resolution contract

`validate_iana_timezone` does more than test non-empty text.

Baseline requirements:

```text
zone identifier
→ exact accepted PostgreSQL/tzdb IANA zone vocabulary
→ invalid zone REJECT

named-zone local coordinate that is nonexistent in a DST gap
→ no hidden shift-forward/backward
→ no canonical resolved instant unless an explicit accepted resolution exists

ambiguous local coordinate in a DST overlap
→ no hidden first/second-offset choice
→ no automatic duplicate Occurrences

when resolved_at / resolved_start_at / resolved_end_at is supplied
→ instant must be finite
→ conversion through the stored zone must round-trip to the exact stored local coordinate
→ accepted historical instant is retained and later tzdb changes do not rewrite it
```

Where the owning contract permits an unresolved named-zone local state, unresolved values remain unresolved rather than fabricating a canonical instant.

No DANTE timezone taxonomy table or policy-code placeholder is introduced.

### 52.18 P0 provisioning hardening is fail-closed

Part 13 P0 remains provisioning-owned and non-Alembic. This checkpoint adds the missing technical guardrail:

```text
CP6-M01 MUST execute a read-only preflight before its first business DDL statement.
```

The preflight must prove from live PostgreSQL catalogs/effective privileges that P0 is in effect, including at least:

```text
dante schema owner = dante_owner
PUBLIC has no DANTE schema authority
dante_runtime has dante USAGE but no CREATE
dante_runtime has no owner membership
PUBLIC database CONNECT/TEMP remain revoked under DB-U21
runtime has no default future-table CRUD from dante_owner
runtime has no default future-sequence USAGE from dante_owner
runtime has no default future-type USAGE from dante_owner
PUBLIC has no default EXECUTE on future dante_owner routines
legacy blanket ALL TABLES / ALL SEQUENCES reconciliation is no longer active
```

If this preflight fails:

```text
M1 aborts before creating the first CP6 business table.
```

Defense-in-depth during materialization:

```text
M1..M6
→ newly created DANTE objects are explicitly reconciled deny-by-default in the same transaction
→ no runtime business capability is activated merely by object creation

M5
→ PUBLIC EXECUTE on each created routine is revoked in the same transaction before commit

M7
→ exact DB-U21 runtime privileges are granted/activated
```

Thus a mistaken direct `alembic upgrade head` against an un-hardened legacy CP3 database fails closed rather than producing a temporarily over-privileged schema.

### 52.19 Legacy CP3 upgrade proof

CP6-05 must own a test-only legacy CP3 posture independent of the newly hardened provisioning implementation.

Required cases:

```text
legacy CP3 defaults + CP3 Alembic base
→ attempt M1 directly
→ FAIL before CP6 business DDL

same legacy CP3 database
→ apply current P0 provisioning hardening
→ M1..M7
→ PASS

post-M7
→ rerun provisioning
→ exact business ACLs remain unchanged / not broadened
```

The legacy fixture reproduces the immutable historical CP3 privilege contract rather than calling the current provisioning function after that function has changed.

### 52.20 Technical PostgreSQL session envelope

CP6-04/05 must keep runtime/migrator diagnostics deterministic without changing civil-time semantics:

```text
server_encoding = UTF8
runtime TimeZone = UTC
migrator TimeZone = UTC
runtime search_path = dante, public with actual schema privileges bounded by DB-U21
migrator uses explicit SET ROLE dante_owner for migration DDL
```

`TimeZone=UTC` affects session rendering/implicit timestamp interpretation only; DANTE named-zone/floating-local semantic fields remain explicitly typed and never inherit session/device zone as their meaning.

TLS, HA, backup topology, PgBouncer and managed-vs-self-hosted production transport remain deployment-environment concerns and are not invented as database-semantic Gate-03 facts.

### 52.21 Deployment schema-compatibility gate

`DatabaseRuntime.is_ready()` remains a reachability/health probe and does not gain access to `dante.alembic_version`.

Production rollout must instead have a migrator/deployment preflight:

```text
repository expected Alembic head
== live dante.alembic_version
→ application rollout may proceed

mismatch
→ rollout blocked
```

Runtime migration-history access remains denied.

### 52.22 Database Dictionary v1 hardening

Because no object-specific Dictionary entries exist yet, the readiness schema may be hardened in-place before first materialization without migrating historical object records.

`scope.json` lifecycle becomes:

```text
readiness_only
materializing
materialized
```

and tracks current materialization counts/stages separately from immutable expected-baseline counts.

The extension-owned registry becomes an exact keyed object:

```text
postgis
vector
pg_trgm
unaccent
pg_stat_statements
```

rather than an array whose semantic key uniqueness cannot be guaranteed by `uniqueItems` alone.

Object-schema additions required by this checkpoint:

```text
TABLE physical properties
  persistence            permanent
  access_method          heap
  partitioned            false
  row_security           false
  force_row_security     false
  replica_identity       default
  reloptions             [] baseline

PK/UQ
  deferrable
  initially
  enforced

FK
  match_type
  deferrable
  initially
  enforced
  validated

CHECK
  enforced
  validated
  no_inherit

INDEX
  valid
  ready
  live

TRIGGER
  orientation
  enabled_mode
  update_columns
  when_condition
  arguments

VIEW
  security_invoker
  security_barrier
  column_defaults

ROUTINE
  argument_types
  return_type
  leakproof
  function_search_path
```

### 52.23 Dictionary validation is two-level

JSON Schema Draft 2020-12 remains structural validation, but it is not sufficient for cross-file semantic integrity.

CP6-04/05 must implement a DANTE semantic Dictionary validator which proves at least:

```text
unique object keys and filenames
object.key == object.type + schema + name
exact extension key set
unique column names within relation
unique PK/UQ/FK/CK/index/trigger identifiers in applicable scope
all referenced columns exist
all FK target objects/columns exist
all index keys/include columns exist
all trigger routine references resolve
routine signature matches trigger use
all grant columns exist
68 table / 5 view / 14 routine / 87 standalone counts
75 trigger attachments
95 physical indexes
120 exact CHECK constraints
68 exact FK relationships
introduction stages reconcile with CP6-M01..M07
SQLAlchemy mode matches object type
Alembic revision/head traceability is coherent
no extension-owned object becomes a false DANTE drift
```

The structural validator and semantic validator are complementary; neither replaces real PostgreSQL introspection.

### 52.24 DB-U24 acceptance

```text
object inventory unchanged                          PASS
95-index matrix unchanged                           PASS
68-FK target/name inventory unchanged               PASS
120 exact CHECK contracts frozen                    PASS
18 root UUIDv7 DB checks frozen                     PASS
non-finite numeric/time rejection frozen            PASS
five view defaults/security/projections frozen      PASS
14 routine physical contracts frozen                PASS
75 trigger physical contracts frozen                PASS
stable SQLSTATE diagnostic contract frozen          PASS
P0 fail-closed M1 guard frozen                       PASS
legacy CP3 upgrade proof frozen                      PASS
Dictionary physical hardening frozen                PASS
Dictionary semantic-validator contract frozen       PASS
runtime/migrator UTC/UTF8 envelope frozen            PASS
deployment head-compatibility gate frozen            PASS
new semantic root                                    0
new table/view/routine/index                         0
new business DDL                                     0
```

`DB-U24` is therefore CLOSED.

---

## 53. Direct PostgreSQL proof / test plan — FROZEN

### 53.1 Proof doctrine

CP6-05 acceptance is evidence coverage, not a vanity pytest count.

Qualifying database behavior uses real PostgreSQL. SQLite/mocks do not prove PostgreSQL FK, range, trigger, view, ACL, isolation, advisory-lock, extension or Alembic semantics.

The existing CP3 real-PostgreSQL suite is retained and extended rather than replaced.

Final acceptance must reconcile at least:

```text
68 / 68 DANTE tables
5 / 5 current views
14 / 14 routines
75 / 75 trigger attachments
95 / 95 physical indexes
68 / 68 foreign keys
120 / 120 CHECK constraints
14 / 14 integrity roles behavior-covered
```

### 53.2 DBP-01 — Exact environment

Every qualifying run records/asserts:

```text
PostgreSQL exact patch
server_encoding = UTF8
runtime/migrator TimeZone = UTC
max_identifier_length supports frozen manifest
PostGIS version
pgvector version
pg_trgm installed
unaccent installed
pg_stat_statements installed
```

### 53.3 DBP-02 — Provisioning / P0

Prove:

```text
roles exact
membership/NOINHERIT/SET topology exact
database/schema/public ACL exact
default ACL deny-by-default exact
provisioning idempotent
post-M7 provisioning rerun non-broadening
legacy CP3 direct M1 fail-closed
legacy CP3 + P0 + M1..M7 succeeds
```

### 53.4 DBP-03 — Alembic DAG and upgrade paths

Prove one canonical head and exact linear dependency:

```text
20260820_01
→ CP6-M01
→ M02
→ M03
→ M04
→ M05
→ M06
→ M07
```

Qualifying paths:

```text
fresh provisioned database → head
legacy supported CP3 state → P0 → head
head → CP3 → head on disposable empty acceptance database
alembic check / no mapping-schema drift
```

A destructive production downgrade is not represented as recovery truth.

### 53.5 DBP-04 — Stage-by-stage materialization

Expected cumulative topology:

```text
M1  16 tables / 16 indexes
M2  22 tables / 28 indexes
M3  37 tables / 55 indexes
M4  63 tables / 87 indexes
M5  +5 views / +13 routines / +66 triggers
M6  68 tables / 95 indexes / 14 routines / 75 triggers
M7  topology unchanged / exact runtime ACL activated
```

Before M7 runtime business DML remains unavailable.

Dictionary current-materialization counts/stages must track the same accepted migration checkpoint.

### 53.6 DBP-05 — Exact object inventory

At head:

```text
DANTE-owned tables            68
ordinary DANTE views            5
DANTE routines                 14
trigger attachments            75
physical indexes               95
CHECK constraints             120
FK constraints                 68
custom DANTE enum/domain        0
DANTE sequences                 0
materialized views              0
RLS policies                    0
partitioned DANTE tables        0
schema dante tables incl Alembic 69
```

Extension-owned objects are classified through `scope.json`, not counted as DANTE drift.

### 53.7 DBP-06 — Structural PostgreSQL catalog proof

Use PostgreSQL catalogs/information schema as appropriate to prove:

```text
columns/types/nullability/defaults
PK/UQ/FK/CHECK exact names/definitions
enforced/validated/deferrability/match/delete/update state
relation owner/persistence/access method/RLS/partitioning/replica identity/reloptions
view definition/options/defaults/check option/updatability
routine signature/language/security/volatility/parallel/leakproof/search_path/owner
trigger event/timing/orientation/enabled/deferrability/routine/args/WHEN
```

Unexpected `UNLOGGED`, TEMP, partitioning, RLS, NOT ENFORCED or invalid constraints are failures.

### 53.8 DBP-07 — 95/95 index proof

Every expected physical index is:

```text
present
exactly named
correct access method
correct key order
correct uniqueness
correct predicate
correct INCLUDE set
valid
ready
live
```

Reconcile:

```text
68 PK-backed + 2 UQ-backed + 25 explicit = 95
```

Do not assert that the planner must choose a particular index on an empty/unrepresentative database. The quota concurrency operation must instead prove the real behavior which justified its index.

### 53.9 DBP-08 — SQLAlchemy ↔ PostgreSQL

At final head:

```text
Base.metadata DANTE tables = 68
mapped ...Row classes       = 68
baseline relationship()     = 0
VIEW_METADATA handles       = 5
ORM current-view entities   = 0
```

Metadata may not be ahead of the currently accepted Alembic stage during CP6-04.

### 53.10 DBP-09 — Dictionary structural + semantic validation

Use a maintained test-only Draft 2020-12 validator implementation and the DANTE semantic validator.

Prove:

```text
JSON Schema meta-schema validity
scope.json structural validity
87 object files structural validity at materialized head
cross-file semantic validator clean
Dictionary ↔ PostgreSQL clean
Dictionary ↔ SQLAlchemy clean
Dictionary ↔ Alembic clean
all final scope counts exact
```

No runtime application dependency is introduced merely for Dictionary validation.

### 53.11 DBP-10 — Exact ACL / ownership

Connect using actual roles, not owner-only introspection.

Prove DB-U21 exactly:

```text
68/68 table SELECT
54/68 table INSERT
exact 14 no-INSERT objects
0 table-level runtime UPDATE
5 exact current_until_at column UPDATE grants
0 base-table DELETE
0 TRUNCATE / REFERENCES / TRIGGER / MAINTAIN / grant option
5 bounded current-view DML surfaces
DELETE only Schedule/Actual current views
0 direct runtime routine EXECUTE
runtime cannot read/write dante.alembic_version
runtime cannot CREATE schema objects or TEMP objects
```

### 53.12 DBP-11 — Native/scoped addressing

Positive/negative real PostgreSQL cases:

```text
valid concrete owner + matching native_address             PASS
unknown native owner_family                                REJECT
nonexistent concrete native owner                          REJECT
UUID exists only in wrong native family                    REJECT
valid schedule/actual scoped_address                       PASS
unknown/wrong scoped family                                REJECT
heterogeneous Schedule/Actual subject admitted family      PASS
wrong family                                                REJECT
dangling address/ref                                        REJECT
attempt address ref/family mutation through runtime        DENIED/REJECT
```

Acceptance integrity scan proves no orphan/family-mismatched native/scoped address.

### 53.13 DBP-12 — MaterialState/current/history + trigger ledger

Prove:

```text
missing MaterialState payload                       REJECT by forced deferred validation/commit
orphan payload                                      REJECT
wrong owner/facet/address space                     REJECT
both/no owner spaces                                REJECT
wrong current binding                               REJECT
history overlap                                     REJECT
two open history episodes                           REJECT
open history != current binding                     REJECT by deferred validation
new valid replacement preserves old state/history   PASS
same old state may be reselected later              PASS
```

Deferred trigger method must include both:

```text
temporary invalid intermediate state
→ repair in same transaction
→ SET CONSTRAINTS ALL IMMEDIATE
→ PASS

invalid state left unrepaired
→ SET CONSTRAINTS ALL IMMEDIATE or COMMIT
→ REJECT
```

Trigger attachment introspection ledger:

```text
75 / 75 present
75 / 75 exact routine
75 / 75 exact event/timing/orientation
75 / 75 exact enabled/deferrability
75 / 75 assigned to at least one behavior scenario
```

Tests assert SQLSTATE/diagnostics, not message strings.

### 53.14 DBP-13 — Schedule

Prove all four physical temporal forms plus negatives:

```text
date span [start,end) finite/nonempty                   PASS
empty/infinite/noncanonical bounds                      REJECT
floating point/start-only/interval                      PASS
named-zone point/start-only/interval                    PASS
absolute point/start-only/interval                      PASS
wrong/missing/multiple typed payload                    REJECT
invalid interval ordering / infinity                    REJECT
invalid IANA zone                                       REJECT
DST-gap hidden shift                                    REJECT / no canonical hidden resolution
DST-overlap hidden first/second choice                  REJECT / absent
resolved instant not round-tripping to local+zone       REJECT
blank Schedule at COMMIT                                REJECT
reschedule/current-history integrity                     PASS
unschedule via bounded current view                      PASS
qualitative day-part placeholder                         absent by schema
```

### 53.15 DBP-14 — Actual

Prove the three-state missingness distinction:

```text
no Actual row                         unknown/not established
Actual + false                        known non-realization
Actual + true                         established realization
```

Also prove:

```text
blank Actual at COMMIT                               REJECT
false + direct realized timing                      REJECT
valid direct timing                                 PASS
non-finite/invalid timing                           REJECT
Session basis wrong Session owner/facet/state       REJECT
later Session correction does not rewrite old basis PASS
current-history/current-view reconciliation         PASS
```

### 53.16 DBP-15 — Session

Prove:

```text
creation without current timing                     REJECT
absolute timing                                     PASS
elapsed-only finite positive numeric                PASS
NaN / +Infinity / -Infinity / <=0 elapsed           REJECT
absolute + elapsed payload                          REJECT
precision vocabulary/pairs                          PASS/REJECT as contract
valid pause geometry                                PASS
pause outside Session                               REJECT
overlapping pauses                                  REJECT
two open pauses                                     REJECT
open pause on ended timing                          REJECT
current/history reconciliation                      PASS
```

### 53.17 DBP-16 — Routine/Event Recurrence

For both Routine and Event exercise all four physical families:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

At least eight positive aggregate families plus negative matrix for:

```text
wrong/missing/multiple family payload
wrong owner/facet
range/boundary incompleteness
invalid selector families/combination
invalid scalar selector ranges
invalid/non-finite temporal anchors
invalid zone / DST hidden policy
phase-dependent pattern missing anchor
quota frame/week-start/phase errors
cyclic missing/out-of-range/incomplete positions
```

`completion_relative` and `anchor_stream_relative` remain unavailable as baseline physical family codes/payloads.

### 53.18 DBP-17 — Occurrence generation

Positive cases:

```text
calendar recurrence-generated
elapsed recurrence-generated
quota recurrence-generated
cyclic recurrence-generated
explicit_extra
```

Negative cases:

```text
recurrence_generated without governing state
wrong source owner/facet/governing family
zero/multiple/wrong coordinate family
explicit_extra with governing recurrence state
explicit_extra with generated coordinate
invalid/non-finite coordinate
cyclic non-generating/out-of-range position
```

A materialized Occurrence remains bound to its old governing recurrence MaterialStateRef after a later recurrence revision.

### 53.19 DBP-18 — Current capability views

For all five views:

```text
SELECT                                  PASS
INSERT using only owner_ref + material_state_ref  PASS where semantic aggregate complete
facet_code populated by exact view default
UPDATE material_state_ref               PASS under accepted operation
attempt wrong facet                      REJECT by LOCAL CHECK OPTION/base integrity
direct base-current-table DML as runtime DENIED
```

DELETE:

```text
Schedule  PASS
Actual    PASS
Session   DENIED
Routine   DENIED
Event     DENIED
```

Introspection additionally proves exact view column order/default/security/check-option properties.

### 53.20 DBP-19 — Real multi-connection concurrency

Use independent real PostgreSQL connections/tasks with deterministic barriers and bounded local timeouts; avoid timing-only `sleep` assertions.

Advisory-lock tests:

```text
same key        → second transaction blocks until first finishes
different owner → no false conflict
different namespace → no false conflict
commit/rollback → transaction lock released
multiple keys input in opposite order → helper dedupe/sort prevents application-order deadlock
```

Golden vectors freeze exact `(namespace, UUID) → bigint` output for the BLAKE2b key derivation.

Current-state race:

```text
two writers same owner/expected MaterialStateRef
→ no silent lost replacement
→ one coherent current binding
→ non-overlapping history
```

Quota race:

```text
same source + governing state + exact period
→ concurrent materializations cannot exceed quota_count
```

Use `SET LOCAL lock_timeout` / `statement_timeout` and, where useful, `pg_locks`/wait-event evidence so a test proves the intended blocking point rather than merely running concurrently.

### 53.21 DBP-20 — Historical reconstruction + truthful staged evidence

Reconstruct past currentness for:

```text
Schedule placement
Actual realization
Session timing
Routine recurrence
Event recurrence
```

Correction creates another MaterialStateRef and never makes old interpretation depend on today's current state.

Items with no authorized baseline object/capability remain staged rather than fake-PASS, including as applicable:

```text
destructive restore/anti-resurrection evidence
real V1→V2 semantic evolution
Agreement/governance material profile
product selective-disclosure/search surfaces
generic idempotency/outbox/provider sync
RLS
PostGIS business geometry
search/vector persistence
```

No table is invented to make a staged proof green.

### 53.22 PostgreSQL test-fixture architecture

The existing real-PostgreSQL CP3 harness is retained, but CP6-05 must avoid rebuilding the full 68-table/5-extension schema for every semantic test.

Recommended bounded fixture roles:

```text
one session PostgreSQL cluster/image

fresh/unprovisioned database
→ provisioning/migration tests

legacy-CP3 database
→ P0 fail-closed/upgrade tests

stage-specific disposable database
→ M1..M7 topology tests

fully materialized template database
→ built once per test session

isolated database clone from template
→ semantic/negative/concurrency tests
```

Isolation remains database-real. This optimization does not authorize sharing transaction state or test data between cases and does not require a new generic test framework.

### 53.23 CI topology

The existing `Backend PostgreSQL` lane remains the default acceptance lane initially.

Do not pre-split CI merely for aesthetics. Measure the real materialized corpus first. If execution time later justifies it, structural and semantic/concurrency PostgreSQL lanes may be split while the top-level required gate still requires all qualifying lanes.

### 53.24 Proof-plan acceptance

```text
real PostgreSQL required                           PASS
existing CP3 suite reused                          PASS
P0/legacy-upgrade proof                            COMPLETE CONTRACT
M1..M7 stage proof                                 COMPLETE CONTRACT
68-table inventory proof                           COMPLETE CONTRACT
5-view proof                                       COMPLETE CONTRACT
14-routine proof                                   COMPLETE CONTRACT
75-trigger proof                                   COMPLETE CONTRACT
95-index proof                                     COMPLETE CONTRACT
68-FK proof                                        COMPLETE CONTRACT
120-CHECK proof                                    COMPLETE CONTRACT
ACL proof                                          COMPLETE CONTRACT
SQLAlchemy/Alembic/Dictionary/PostgreSQL drift     COMPLETE CONTRACT
DST/non-finite/UUIDv7 negative proof               COMPLETE CONTRACT
real concurrency proof                             COMPLETE CONTRACT
history reconstruction proof                       COMPLETE CONTRACT
staged evidence remains truthful                   PASS
```

The Direct PostgreSQL Proof / Test Plan is therefore **FROZEN** for CP6-03.

---

## 54. Current continuation state

The canonical Database Architecture & Reference is now Parts 1–16 consumed together.

Current CP6-03 state:

```text
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY       FROZEN
DB-U08 FINAL NAMING                            CLOSED
DB-U15 FINAL INDEX MATRIX                      CLOSED
DB-U21 FINAL PRIVILEGE MATRIX                  CLOSED
MIGRATION / MATERIALIZATION DAG                FROZEN
SQLALCHEMY MAPPING PLAN                        FROZEN
DATABASE DICTIONARY READINESS                  READY / HARDENED BY PART 16
DB-U24 IMPLEMENTATION DETERMINISM              CLOSED
DIRECT POSTGRESQL PROOF / TEST PLAN            FROZEN
GLOBAL DB-U OPEN                               0

SECOND FULL TOMBSTONE AUDIT FROM ZERO          NEXT / NOT YET RUN
GATE 03                                        NOT YET EARNED
CP6-04                                         NOT STARTED / NOT AUTHORIZED
```

Part 16 supersedes only narrower implementation-provisional statements where it is explicitly more exact, especially:

```text
representative CHECK floor
→ exact 120-CHECK manifest

current-view fixed predicate only
→ exact projection/security/default/CHECK OPTION contract

trigger role/count only
→ exact physical trigger properties

routine role/name only
→ exact physical function signature/properties/error contract

P0 documentation prerequisite only
→ M1 fail-closed preflight + deny-before-M7 defense

Dictionary readiness schema
→ pre-materialization hardened v1 + semantic-validator requirement

proof-plan candidate prose
→ frozen DBP-01..DBP-20 contract
```

Parts 1–15 otherwise remain canonical and unchanged.

The next operation is the mandatory **SECOND FULL TOMBSTONE AUDIT FROM ZERO**. It must independently replay Domain → Logical → Physical → CP6-01 → CP6-02 → complete Parts 1–16 → Dictionary/proof contract and must not inherit PASS from this hardening review.
