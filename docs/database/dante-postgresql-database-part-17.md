<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-16.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 17

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / DB-U25 SECOND TOMBSTONE REPAIR CLOSED  
**Scope:** section 55 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–16  
**PRE-SCOPE for this repair:** `f2bdab00faee84c3be6e951b848417fae9330446`  
**Current PostgreSQL architecture:** PostgreSQL 18 major family / current technical patch 18.6  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Part 16 closed pre-Gate03 implementation determinism and froze the direct PostgreSQL proof plan. The mandatory second tombstone audit then restarted independently from Domain and found five implementation/integrity defects that must be repaired before the final replay can earn Gate 03.

This continuation repairs only those findings. It does not reopen Domain, Logical, Physical, CP6-01 or CP6-02; it does not create business DDL; and it does not change the surviving baseline object inventory.

---

## 55. DB-U25 — Second Tombstone Repair — CLOSED

### 55.1 Purpose and audit disposition

The second full tombstone audit did not find a new semantic owner, a generic-root regression or an object-inventory defect. It did find five cases where the accepted database could still admit or fail to reject a semantically false state.

Exact repair register:

```text
TOMB-B01  recurrence selector / phase / range determinism
TOMB-B02  duplicate non-quota generated Occurrence coordinate
TOMB-B03  five NULL-unsafe CHECK expressions
TOMB-B04  generated coordinate not fully proven as a member of governing Recurrence
TOMB-B05  current-history INSERT/closure lifecycle too broad
```

Classification:

```text
Domain reopen                              0
Logical reopen                             0
Physical reopen                            0
new Domain owner                           0
new table                                  0
new view                                   0
new routine                                0
new trigger attachment                     0
new physical index                         0
new FK                                     0
new CHECK identifier                       0
```

Frozen global counts therefore remain:

```text
DANTE tables                               68
DANTE current views                         5
integrity routines                         14
trigger attachments                        75
physical indexes                           95
foreign keys                               68
named CHECK constraints                   120
custom DANTE enum/domain types              0
DANTE sequences                             0
RLS policies                                0
```

Part 17 narrows only exact expressions, cross-table invariant contracts, ACL granularity and proof requirements.

### 55.2 Tombstone supersession rule

Where this Part 17 is more exact, it narrowly supersedes the applicable provisional or under-specified statement in Parts 1–16. Earlier rationale/history remains canonical evidence.

In particular:

```text
"pattern anchor when phase cannot otherwise be determined"
→ exact pattern/interval/phase matrix in this part

family-only occurrence-generation validation
→ exact governing-rule membership validation in this part

current-history table INSERT YES
→ exact column-scoped INSERT in this part

five Part-16 CHECK expressions vulnerable to SQL NULL truth
→ NULL-safe exact expressions in this part
```

Nothing else is silently superseded.

---

## 55.3 TOMB-B01 — exact calendar selector matrix

For each owner `X ∈ {routine,event}`, `X_recurrence_calendar_state.pattern_code` has the following exact aggregate contract.

`calendar_wall_time` children are orthogonal to the selector-family column below and remain zero-or-more according to section 30.6. The selector-family rules below concern only weekday/month-day/ordinal/year-month-day children.

| `pattern_code` | required selector rows | forbidden selector rows | `pattern_anchor` |
|---|---|---|---|
| `daily` | none | weekday, month-day, ordinal-weekday, year-month-day | required iff `interval_count > 1`; otherwise absent |
| `weekly_weekdays` | at least 1 weekday | month-day, ordinal-weekday, year-month-day | required iff `interval_count > 1`; otherwise absent |
| `monthly_month_days` | at least 1 month-day | weekday, ordinal-weekday, year-month-day | required iff `interval_count > 1`; otherwise absent |
| `monthly_ordinal_weekdays` | at least 1 ordinal-weekday pair | weekday, month-day, year-month-day | required iff `interval_count > 1`; otherwise absent |
| `yearly_month_days` | at least 1 year-month-day pair | weekday, month-day, ordinal-weekday | required iff `interval_count > 1`; otherwise absent |
| `anchor_step` | none | weekday, month-day, ordinal-weekday, year-month-day | exactly 1, always |

For all required calendar pattern anchors:

```text
boundary_role = 'pattern_anchor'
boundary_kind = 'date'
inclusive IS NULL
```

No floating-local, named-zone-local or absolute-instant boundary is admitted as the baseline calendar phase anchor. A phase anchor is a date-position basis; clock semantics remain in `clock_basis_code`, `zone_id` and wall-time children.

For the five non-`anchor_step` patterns:

```text
interval_count = 1
→ no pattern_anchor row

interval_count > 1
→ exactly one date pattern_anchor row
```

This removes unused/meaningless anchor data when no phase is needed and removes every hidden phase default when an interval skips natural periods.

### 55.4 Calendar weekday and interval phase semantics

`weekday_number` remains ISO weekday numbering:

```text
1 Monday
2 Tuesday
3 Wednesday
4 Thursday
5 Friday
6 Saturday
7 Sunday
```

The phase lattice is exact:

```text
daily
→ candidate date difference from anchor date is an integer multiple of interval_count days

weekly_weekdays
→ anchor date identifies its ISO Monday-based week
→ candidate ISO-week offset from the anchor ISO week is an integer multiple of interval_count
→ candidate ISO weekday must exist in the exact weekday child set

monthly_month_days
monthly_ordinal_weekdays
→ candidate Gregorian month offset from the anchor month is an integer multiple of interval_count

yearly_month_days
→ candidate Gregorian year offset from the anchor year is an integer multiple of interval_count
```

For `interval_count = 1`, every natural day/week/month/year period is active and no phase anchor is required.

Phase arithmetic is valid in both directions around the anchor. `pattern_anchor` is a phase basis, not an implicit effective lower bound. The explicit effective range remains a separate contract.

### 55.5 Exact monthly/yearly selector meaning

`monthly_month_days` membership:

```text
candidate day matches at least one stored month_day
positive 1..31  → exact day-of-month when it exists
negative -1..-31 → exact backward position from month end
invalid positive position → no candidate; never clamp/fallback
```

`monthly_ordinal_weekdays` membership:

```text
candidate weekday == stored weekday_number
AND
candidate occurrence-number of that weekday in the month == stored ordinal

ordinal > 0
→ count from month start

ordinal < 0
→ count backward from month end
```

A fifth/negative-fifth weekday that does not exist in the concrete month produces no candidate. There is no fallback.

`yearly_month_days` membership:

```text
(candidate month_number, exact/negative month_day)
→ must equal one stored pair
```

A non-existent date such as 29 February in a non-leap year produces no candidate; it is not moved.

### 55.6 `anchor_step` exact lattice

`anchor_step` always has exactly one date pattern anchor and no selector rows.

`step_unit_code` remains one of:

```text
day
week
month
year
```

Membership is exact:

```text
day
→ candidate_date - anchor_date is divisible by interval_count days

week
→ candidate_date - anchor_date is divisible by (7 * interval_count) days

month
→ Gregorian month offset is divisible by interval_count
→ candidate day-of-month equals anchor day-of-month
→ a target month lacking that exact day produces no candidate

year
→ Gregorian year offset is divisible by interval_count
→ candidate month/day equals anchor month/day
→ invalid target date produces no candidate
```

There is no end-of-month clamp and no source-created-at fallback.

### 55.7 Exact wall-time membership

For every calendar recurrence state:

```text
zero wall-time children
→ generated calendar coordinate MUST have generated_wall_time IS NULL

one or more wall-time children
→ generated_wall_time MUST be non-NULL
→ generated_wall_time MUST equal exactly one child wall_time
```

The generation coordinate must also copy the exact recurrence clock basis:

```text
generation.clock_basis_code = recurrence.clock_basis_code
```

and zone semantics:

```text
named_zone
→ generation.zone_id = recurrence.zone_id

floating_local / absolute_utc
→ generation.zone_id IS NULL
```

For a materialized named-zone coordinate with a wall time, `resolved_at` is required because the materialized Occurrence is now persistently distinguishable and must preserve its accepted instant basis. The instant must round-trip to the exact stored generated date + wall time + zone under the Part-16 DST contract.

A named-zone date-only expectation remains date-only and therefore has no fabricated `resolved_at`.

---

## 55.8 Exact Recurrence boundary-role matrix

Boundary roles remain stored only in the owner-specific recurrence boundary table.

Cardinality by state:

```text
pattern_anchor
→ exactly as required/forbidden by family rules in this part

effective_from
→ zero or one generally
→ exactly one when range_kind='expected_count' for an admitted expected-count family

effective_until
→ exactly one iff range_kind='until_boundary'
→ absent for range_kind IN ('open','expected_count')
```

`range_kind='expected_count'` is admitted in the CP6 baseline only for:

```text
calendar_wall_clock
elapsed_interval
cyclic_positional
```

and is **rejected for `quota_per_period`**.

Reason: quota expectations inside a period deliberately have no arbitrary first/second/third semantic slot. A global expected-count cutoff could otherwise invent an arbitrary partial-period ordering. A future quota expected-count profile requires an explicit accepted partial-period/ordering contract before materialization.

For every admitted expected-count state:

```text
exactly one effective_from boundary
no effective_until boundary
expected_occurrence_count > 0
```

The first N generated coordinates are counted from that explicit effective lower boundary; current-state acceptance time, insertion time and source creation time are never substituted.

### 55.9 Effective-boundary kind compatibility

Pattern anchors are handled separately above. Effective boundaries use the following exact baseline matrix:

```text
calendar + floating_local
→ date OR floating_local

calendar + named_zone
→ date OR named_zone_local OR absolute_instant

calendar + absolute_utc
→ date OR absolute_instant

elapsed_interval
→ absolute_instant only

quota_per_period
→ date only

cyclic_positional
→ date only
```

For one recurrence state, if both `effective_from` and `effective_until` exist, they MUST use the same `boundary_kind`. For `named_zone_local`, both must also use the exact recurrence `zone_id`.

A calendar rule with no wall-time children may use only date effective boundaries. A local/instant boundary requires an exact candidate coordinate at that granularity; DANTE does not fabricate midnight or another clock position.

For named-zone effective boundaries, invalid/non-existent/ambiguous civil coordinates follow the Part-16 DST contract. A consequential boundary that cannot be resolved without an arbitrary gap/fold choice is rejected rather than normalized silently.

When both effective boundaries exist, the interval must be non-empty under their exact values/inclusive flags:

```text
lower < upper
OR
lower = upper AND effective_from.inclusive AND effective_until.inclusive
```

No mixed-kind comparison or hidden timezone conversion is allowed.

### 55.10 Effective membership semantics

For a generated coordinate to be valid, it must satisfy every present effective boundary in its admitted semantic frame.

```text
effective_from inclusive=true   → coordinate >= lower
effective_from inclusive=false  → coordinate >  lower

effective_until inclusive=true  → coordinate <= upper
effective_until inclusive=false → coordinate <  upper
```

Date boundaries compare the generated semantic date, not a fabricated midnight instant.

Floating-local boundaries compare exact generated local date+wall-time and therefore require a calendar wall-time coordinate.

Named-zone-local boundaries compare exact generated local date+wall-time in the same stored zone and the accepted resolved basis where required.

Absolute-instant boundaries compare an exact accepted instant:

```text
elapsed
→ expected_at

calendar named-zone
→ resolved_at

calendar absolute_utc with wall time
→ exact UTC instant derived from generated date + generated_wall_time
```

If the coordinate cannot supply the exact comparison basis required by the stored effective-boundary kind, the recurrence state/materialization is invalid; server timezone or a default clock value is never substituted.

### 55.11 Expected-count ordering

For the three admitted expected-count families, generated coordinates have an intrinsic deterministic sequence order independent of Occurrence UUIDs:

```text
calendar
→ generated_date ASC
→ when wall-time children exist: generated_wall_time ASC

elapsed
→ expected_at ASC

cyclic
→ generated_date ASC
```

`expected_occurrence_count = N` admits exactly the first N coordinates satisfying the recurrence pattern and effective-from boundary.

The database validator MUST determine membership/rank from the accepted rule and coordinate. It MUST NOT use:

```text
number of rows already materialized
UUID order
insertion order
current time
```

as a substitute for sequence position.

CP6-04 may implement the exact family arithmetic efficiently, but it may not replace the invariant with iterative unbounded global expansion. If the implementation cannot prove the rank with bounded family-specific arithmetic, it must stop and re-gate rather than weaken expected-count semantics.

---

## 55.12 Quota phase and exact period coordinate

Quota phase is now exact.

```text
period_span = 1
→ no pattern_anchor row

period_span > 1
→ exactly one date pattern_anchor row
```

When present, the quota pattern anchor is the start of one exact period block:

```text
period_unit_code='day'
→ any finite anchor date

period_unit_code='week'
→ anchor ISO weekday = week_start

period_unit_code='month'
→ anchor day-of-month = 1

period_unit_code='year'
→ anchor month/day = 1 January
```

For `period_span = 1`, natural calendar period boundaries plus `week_start` fully determine membership; no redundant phase anchor is stored.

A quota generation coordinate must match the governing state exactly:

```text
frame_code = quota_state.frame_code
zone_id    = quota_state.zone_id under the exact zone-basis rule
```

and:

```text
period_start_date
period_end_date_exclusive
```

must be the exact half-open period `[start,end)` derived from `period_unit_code`, `period_span`, `week_start` and optional pattern anchor.

No arbitrary date span is accepted as a quota generation coordinate.

Quota effective boundaries are date-only and align to quota period boundaries:

```text
effective_from
→ inclusive = true
→ exact period start

effective_until
→ inclusive = false
→ exact period end boundary
```

A partial-period quota is not invented by CP6 baseline.

Quota still permits multiple differentiated Occurrences in one exact period up to `quota_count`; there is deliberately no slot ordinal.

---

## 55.13 Elapsed recurrence exact coordinate

Elapsed recurrence has no `pattern_anchor` boundary row because `anchor_at` is already its exact seed.

Any `pattern_anchor` boundary on an `elapsed_interval` state is rejected.

The two existing recurrence elapsed-positive CHECKs are tightened, without adding CHECK identifiers, to require microsecond-representable exact seconds:

```text
elapsed_seconds NOT IN ('NaN'::numeric,'Infinity'::numeric,'-Infinity'::numeric)
AND elapsed_seconds > 0
AND elapsed_seconds = trunc(elapsed_seconds, 6)
```

This aligns exact persisted duration with PostgreSQL/Python timestamp microsecond resolution and prevents a state whose exact interval can never map to an exact `timestamptz` lattice.

For both `fixed_anchor` and `previous_expected` baseline modes:

```text
expected_at = anchor_at + k * elapsed_seconds
for an integer k >= 1
```

`previous_expected` remains semantically chained to the previous expected coordinate rather than Actual completion, but because the interval is fixed the valid coordinate lattice is the same exact seed-plus-k-interval set.

An `expected_at` not lying on that lattice is rejected.

---

## 55.14 Cyclic recurrence exact coordinate

Cyclic state continues to require exactly one date pattern anchor.

For `position_unit_code='day'`:

```text
step_index = generated_date - anchor_date   -- integer days
position_index = positive_mod(step_index, cycle_length)
```

For `position_unit_code='week'`:

```text
generated_date MUST equal anchor_date + (step_index * 7 days)
position_index = positive_mod(step_index, cycle_length)
```

Thus a week-based cyclic coordinate stores the exact cycle-week start date, not an arbitrary day inside the week.

In both modes:

```text
corresponding cycle-position child MUST exist
cycle-position.generates_expected MUST be true
```

A coordinate with a valid numeric `position_index` but the wrong date/phase is rejected.

---

## 55.15 TOMB-B02 — duplicate non-quota generation identity

A `recurrence_generated` Occurrence represents one specific expected coordinate under one exact source and governing recurrence MaterialState.

For Calendar, Elapsed and Cyclic baseline families, two different OccurrenceRefs MUST NOT represent the same generation identity.

Exact duplicate keys:

```text
CALENDAR
source_native_ref
+ governing_recurrence_state_ref
+ generated_date
+ generated_wall_time with SQL NULL treated as the date-only coordinate
+ clock_basis_code
+ zone_id with SQL NULL treated as the non-named-zone coordinate

ELAPSED
source_native_ref
+ governing_recurrence_state_ref
+ expected_at

CYCLIC
source_native_ref
+ governing_recurrence_state_ref
+ generated_date
+ position_index
```

`resolved_at` is not part of Calendar identity. A named-zone DST overlap may not create two Occurrences for one civil generation coordinate merely by choosing different offsets.

Quota is deliberately excluded from this uniqueness rule:

```text
same source + governing state + exact quota period
→ multiple distinct Occurrences permitted
→ bounded only by quota_count
```

`explicit_extra` is also outside recurrence-coordinate uniqueness because it has no governing recurrence coordinate.

Role 13 (`enforce_occurrence_generation_integrity`) must reject a second non-quota Occurrence with a duplicate exact generation identity.

### 55.16 Duplicate-generation concurrency

Correctness under concurrency uses the already-frozen application/database lock registry rather than a speculative new index/table.

For `recurrence_generated` materialization, the accepted operation acquires both:

```text
source current-recurrence lock
+
source occurrence-generation lock
```

under the Part-14 namespace registry and sorted acquisition rule before reading current state or inserting.

Role 13 is additionally required to acquire/reuse the exact source occurrence-generation transaction lock before its final duplicate/cardinality validation. Because the integrity routine is `VOLATILE`, the duplicate query is executed after the lock acquisition and must observe the then-committed state under the transaction's accepted READ COMMITTED behavior.

This provides defense in depth for accepted DML paths without adding a second identity column or generic generation-key hash.

The existing DB-U15 index:

```text
ix_occurrence_generation_source_governing_state
```

remains the bounded parent lookup path for duplicate validation; coordinate children are joined by their PK `occurrence_ref`.

No new baseline index is added by this repair. CP6-05 must include a representative long-lived-state stress check; measured evidence may later justify an additive lookup index, but correctness is not allowed to depend on such a future optimization.

---

## 55.17 TOMB-B03 — exact NULL-safe CHECK repair

PostgreSQL accepts a CHECK result of TRUE **or NULL**. Therefore five Part-16 expressions are tightened so missing companion values cannot pass through SQL three-valued logic.

The CHECK identifiers and total count remain unchanged.

### Session — one replacement

```text
ck_session_timing_absolute_end_precision

(ended_at IS NULL AND end_precision_code IS NULL)
OR
(ended_at IS NOT NULL
 AND end_precision_code IS NOT NULL
 AND isfinite(ended_at)
 AND end_precision_code IN ('exact','approximate','rounded'))
```

This supersedes the Part-16 expression only by adding the explicit `end_precision_code IS NOT NULL` requirement.

### Routine/Event calendar — two replacements

For `X ∈ {routine,event}`:

```text
ck_<x>_recurrence_calendar_state_step_unit

(pattern_code='anchor_step'
 AND step_unit_code IS NOT NULL
 AND step_unit_code IN ('day','week','month','year'))
OR
(pattern_code<>'anchor_step' AND step_unit_code IS NULL)
```

### Routine/Event quota — two replacements

For `X ∈ {routine,event}`:

```text
ck_<x>_recurrence_quota_state_week_start

(period_unit_code='week'
 AND week_start IS NOT NULL
 AND week_start BETWEEN 1 AND 7)
OR
(period_unit_code<>'week' AND week_start IS NULL)
```

Reconciliation:

```text
CHECK identifiers changed                  0
CHECK count                              120
NULL-unsafe known expressions after repair 0
```

---

## 55.18 TOMB-B04 — governing Recurrence membership is database-validated

A row being the correct **family type** is not sufficient evidence that it was generated by the governing Recurrence.

For every `origin_code='recurrence_generated'`, Role 13 must prove by COMMIT all of the following:

```text
1. source_native_ref resolves to Routine/Event and matches the governing state owner
2. governing_recurrence_state_ref resolves to the exact owner/facet/family state
3. governing recurrence state equals the accepted current recurrence binding at materialization time
4. exactly one matching family coordinate exists and all non-matching coordinate families are absent
5. coordinate fields match the exact governing family payload
6. coordinate satisfies exact selector/phase/anchor rules
7. coordinate lies inside the exact effective range
8. expected_count, when admitted, includes the coordinate in its first-N sequence
9. Calendar/Elapsed/Cyclic coordinate is not a duplicate generation identity
10. Quota exact period/cardinality remains within quota_count
```

A MaterialStateRef that is historically valid but no longer current remains permanently valid for reconstruction of an **existing** Occurrence. It is not a baseline authority for minting a **new** recurrence-generated Occurrence after a different recurrence state has become current.

No automatic historical rebasing occurs: once a valid Occurrence has been created, later recurrence-current changes never rewrite its stored governing state.

### 55.19 Calendar membership validation

For Calendar Role-13 validation:

```text
generated date
→ must satisfy exact pattern_code selector
→ must satisfy interval phase when interval_count > 1

generated wall time
→ must satisfy exact wall-time child set rule

clock basis / zone
→ must equal governing calendar state

named-zone resolution
→ must satisfy Part-16 IANA/DST round-trip contract

effective boundaries
→ must admit the exact coordinate under section 55.9/55.10
```

A weekly-Monday recurrence with a Tuesday generated date is rejected even though both rows are structurally valid Calendar objects.

### 55.20 Elapsed membership validation

For Elapsed:

```text
expected_at
→ finite
→ exact positive integer lattice step from anchor_at
→ admitted by effective boundaries
→ admitted by expected_count when range_kind='expected_count'
```

An arbitrary finite `expected_at` is not sufficient.

### 55.21 Quota membership validation

For Quota:

```text
coordinate frame / zone
→ exact governing-state equality

coordinate [period_start_date, period_end_date_exclusive)
→ exact derived period block

range_kind='expected_count'
→ REJECT baseline

effective date boundaries
→ exact period-boundary alignment

materialized count for same source + governing state + exact period
→ before insert < quota_count
```

A skipped/cancelled generated Occurrence continues to count as an expected generated slot.

### 55.22 Cyclic membership validation

For Cyclic:

```text
generated_date
→ exact phase lattice from pattern_anchor

position_index
→ exact modulo-derived index for that date/week

position child
→ exists and generates_expected=true

effective boundaries / expected_count
→ admit the coordinate
```

A correct position number paired with the wrong date is rejected.

---

## 55.23 TOMB-B05 — current-history lifecycle is one-way

The five current-history families retain the existing shape:

```text
owner_ref
material_state_ref
current_from_at
current_until_at
```

but their lifecycle is now explicitly database-enforced, not only documented.

For each of:

```text
schedule_placement_current_history
actual_realization_current_history
session_timing_current_history
routine_recurrence_current_history
event_recurrence_current_history
```

Role 6 (`enforce_current_history_equivalence`) must enforce:

```text
INSERT
→ current_until_at MUST be NULL

owner_ref
material_state_ref
current_from_at
→ immutable after INSERT

substantive UPDATE
→ only OLD.current_until_at IS NULL
   → NEW.current_until_at IS finite and > current_from_at

OLD.current_until_at IS NOT NULL
→ changing it to NULL REJECT
→ changing it to another timestamp REJECT

same-value no-op UPDATE
→ may be accepted but has no semantic effect
```

The already-frozen non-overlap/open-row/current-binding equivalence rules remain in force.

Thus a currentness episode always begins open and may close exactly once. It cannot be inserted already closed, reopened, or moved after closure.

### 55.24 Exact DB-U21 INSERT supersession for history

Part 12's coarse table-level `INSERT YES` entries for the five history tables are narrowed.

Runtime INSERT capability remains present on 54 of the 68 tables, but it decomposes exactly as:

```text
49 tables
→ table-level INSERT as previously frozen

5 current-history tables
→ column-scoped INSERT only

14 tables
→ no INSERT
```

Exact history grants:

```text
schedule_placement_current_history
INSERT(schedule_ref, material_state_ref, current_from_at)

actual_realization_current_history
INSERT(actual_ref, material_state_ref, current_from_at)

session_timing_current_history
INSERT(session_ref, material_state_ref, current_from_at)

routine_recurrence_current_history
INSERT(routine_ref, material_state_ref, current_from_at)

event_recurrence_current_history
INSERT(event_ref, material_state_ref, current_from_at)
```

`current_until_at` is intentionally absent from the INSERT grant and therefore begins NULL.

The existing five column-level closure grants remain unchanged:

```text
UPDATE(current_until_at)
```

There is still:

```text
0 table-level runtime UPDATE
0 runtime base-table DELETE
0 TRUNCATE
0 REFERENCES
0 TRIGGER
0 MAINTAIN
0 grant option
```

M7 materializes this more exact ACL matrix. P0/provisioning still must never broaden it on rerun.

---

## 55.25 Trigger/routine topology consequence

The 14 routine names and 75 trigger attachments remain unchanged.

No generic recurrence engine, new trigger family or extra helper routine is introduced.

Role refinements:

```text
Role 6 — current/history equivalence
+ INSERT-open-only rule
+ immutable episode key/start fields
+ one-way current_until_at closure

Role 12 — recurrence aggregate integrity
+ exact selector-family matrix
+ exact phase-anchor presence/type
+ exact boundary-kind/range compatibility
+ quota phase/period-boundary compatibility
+ expected-count family compatibility

Role 13 — occurrence-generation aggregate integrity
+ governing state current-at-materialization
+ exact rule-coordinate membership
+ non-quota duplicate generation identity
+ effective-range / expected-count membership
+ exact quota-period/cardinality validation
+ occurrence-generation transaction lock defense in depth
```

The physical trigger split therefore remains:

```text
18 ordinary immediate
57 deferred constraint triggers
75 total
```

No trigger depends on alphabetical firing order.

---

## 55.26 DB-U15 consequence — 95 indexes remain justified

The second tombstone repair adds a real duplicate/membership lookup path, but it does not automatically add an index by habit.

Existing relevant paths remain:

```text
occurrence_generation PK by occurrence_ref
ix_occurrence_generation_source_governing_state
ix_occurrence_generation_governing_recurrence_state_ref
family coordinate PKs by occurrence_ref
ix_occurrence_generation_quota_period
```

Non-quota duplicate validation starts from exact source + governing state and joins bounded coordinate rows through their PK.

Current baseline therefore remains:

```text
physical indexes = 95
```

CP6-05 must measure representative long-lived recurrence-state materialization. A future added coordinate lookup index requires measured evidence and a reviewed additive schema change; it is not required to establish current correctness.

---

## 55.27 Migration/materialization DAG consequence

The seven-node DAG remains unchanged.

```text
M4
→ creates recurrence tables + exact row-local CHECKs
→ includes the five NULL-safe replacements and two elapsed microsecond refinements

M5
→ creates Role-6 / Role-12 integrity implementations using this Part-17 contract

M6
→ creates occurrence-generation tables + Role-13 implementation using this Part-17 contract

M7
→ applies narrowed five-history INSERT column grants
```

Object allocations remain:

```text
68 tables
5 views
14 routines
75 triggers
95 indexes
```

No new Alembic planning node is required.

### 55.28 SQLAlchemy consequence

The Part-14 mapping topology remains unchanged.

CP6-04 mappings must carry the repaired CHECK expression contracts under the already-frozen DB-U08 naming convention. The mapping must not add ORM events for any Part-17 invariant.

No new Row class, relationship, Core view handle or advisory-lock namespace is introduced.

### 55.29 Database Dictionary consequence

Dictionary schema v1 already has sufficient fields to represent all Part-17 repairs.

No Dictionary-schema change is required.

When object entries materialize, they must contain the Part-17 current truth for:

```text
repaired CHECK expressions
current-history column-scoped INSERT grants
Role-6 / Role-12 / Role-13 trigger reasons/contracts
Recurrence phase/range semantics
Occurrence-generation membership/duplicate semantics
```

A Dictionary entry that merely repeats older Part-16 text is stale.

---

## 55.30 Direct PostgreSQL proof delta

Part 16 DBP-01..DBP-20 remains the frozen proof framework. The following cases are added to the applicable lanes and are mandatory before CP6-05 closure.

### Recurrence aggregate / B01

For Routine and Event:

```text
daily interval=1 + no anchor                                      PASS
daily interval=1 + redundant pattern anchor                       REJECT
daily interval>1 + missing anchor                                 REJECT
weekly interval>1 + wrong phase week                              REJECT generated coordinate
monthly_month_days with ordinal selector row                      REJECT by COMMIT
monthly_ordinal_weekdays with no ordinal selector                  REJECT by COMMIT
monthly_ordinal_weekdays with month_day/weekday/year pair extras   REJECT by COMMIT
yearly_month_days with wrong selector family                       REJECT by COMMIT
anchor_step with selector rows                                     REJECT by COMMIT
anchor_step with non-date/missing pattern anchor                    REJECT
calendar expected_count without effective_from                     REJECT
quota expected_count                                               REJECT
elapsed with pattern_anchor boundary                               REJECT
```

### NULL-safety / B03

```text
Session ended_at non-NULL + end_precision_code NULL   REJECT
Routine anchor_step + step_unit_code NULL             REJECT
Event anchor_step + step_unit_code NULL               REJECT
Routine weekly quota + week_start NULL                REJECT
Event weekly quota + week_start NULL                  REJECT
```

### Calendar membership / B04

```text
weekly Monday rule + Tuesday generated_date                  REJECT
monthly 31st + 30th generated_date                           REJECT
monthly ordinal second-Tuesday + third-Tuesday coordinate    REJECT
yearly Feb-29 rule + Feb-28 coordinate                       REJECT
interval>1 off-phase coordinate                              REJECT
wall-time set {08:00,20:00} + 09:00 coordinate               REJECT
date-only recurrence + fabricated wall time                  REJECT
named-zone coordinate with wrong zone                        REJECT
named-zone timed materialization without accepted resolved_at REJECT
generated coordinate outside effective range                 REJECT
historical non-current governing state used for new Occurrence REJECT
```

### Elapsed membership / B04

```text
elapsed_seconds with >6 fractional decimal places            REJECT state
off-lattice expected_at                                      REJECT
first lattice point                                          PASS
expected_count N + coordinate N                              PASS
expected_count N + coordinate N+1                            REJECT
```

### Quota membership / B04

```text
period_span>1 without anchor                                 REJECT
weekly multi-period anchor not on week_start                 REJECT
monthly multi-period anchor not day 1                        REJECT
yearly multi-period anchor not Jan 1                         REJECT
wrong period_start/end                                       REJECT
wrong frame/zone                                             REJECT
partial-period effective boundary                            REJECT
concurrent quota_count+1 materialization                     REJECT
```

### Cyclic membership / B04

```text
correct position_index + wrong generated_date                REJECT
week-unit generated_date not exact 7-day lattice             REJECT
position whose generates_expected=false                      REJECT
```

### Duplicate generation / B02

Both serial and two-connection concurrent tests:

```text
same Calendar source/state/coordinate + second OccurrenceRef  REJECT
same Elapsed source/state/expected_at + second OccurrenceRef   REJECT
same Cyclic source/state/date/position + second OccurrenceRef  REJECT
same quota period with remaining capacity                     PASS
same quota period above quota_count                            REJECT
```

Concurrency tests must prove the intended advisory-lock blocking point and final committed state, not rely on sleeps alone.

### Current-history lifecycle / B05

For each of five history families:

```text
runtime INSERT including current_until_at                     privilege DENIED
owner/test insertion with non-NULL current_until_at           invariant REJECT
open insert                                                   PASS
NULL → valid later closure                                    PASS
closed → NULL reopen                                          REJECT
closed → different timestamp                                  REJECT
owner/material_state/current_from mutation                     REJECT
second open row / overlap                                     REJECT
```

---

## 55.31 Cumulative second-audit repair reconciliation

Post-repair design reconciliation:

```text
57 / 57 Domain disposition                     unchanged / PASS
15 / 15 native owners                           unchanged / PASS
scoped families                                 schedule, actual only
MaterialState facets                            five only
new semantic root                               0
new generic fallback                            0
new schema object                               0

TOMB-B01 recurrence determinism                 REPAIRED
TOMB-B02 duplicate generated coordinate         REPAIRED
TOMB-B03 NULL-unsafe CHECKs                     REPAIRED
TOMB-B04 generation membership                  REPAIRED
TOMB-B05 history lifecycle/ACL                  REPAIRED

CHECK identifiers                              120
FKs                                             68
indexes                                         95
routines                                        14
triggers                                        75
views                                            5
tables                                          68
```

The repair does **not** itself constitute the final second tombstone PASS because the blueprint changed in response to the audit. A fresh independent replay is mandatory after this checkpoint.

### 55.32 DB-U25 closure

```text
DB-U25
SECOND TOMBSTONE REPAIR
CLOSED

KNOWN B FINDINGS FROM SECOND AUDIT
REPAIRED IN BLUEPRINT

C FINDINGS
0

GLOBAL DB-U OPEN
0
```

This status means the known audit findings have deterministic dispositions. It does not mean Gate 03 is earned.

---

## 56. Current continuation state

The canonical Database Architecture & Reference is now Parts 1–17 consumed together.

Current CP6-03 state:

```text
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY       FROZEN
DB-U08 FINAL NAMING                            CLOSED
DB-U15 FINAL INDEX MATRIX                      CLOSED
DB-U21 FINAL PRIVILEGE MATRIX                  CLOSED / NARROWLY SUPERSEDED BY PART 17 HISTORY INSERT ACL
MIGRATION / MATERIALIZATION DAG                FROZEN
SQLALCHEMY MAPPING PLAN                        FROZEN
DATABASE DICTIONARY READINESS                  READY / HARDENED
DB-U24 IMPLEMENTATION DETERMINISM              CLOSED
DIRECT POSTGRESQL PROOF / TEST PLAN            FROZEN + PART-17 DELTA
DB-U25 SECOND TOMBSTONE REPAIR                 CLOSED
GLOBAL DB-U OPEN                               0

SECOND FULL TOMBSTONE AUDIT
→ PRIOR RUN FOUND B FINDINGS
→ REPAIR COMPLETE
→ MUST RESTART FROM ZERO AFTER THIS PART

GATE 03                                        NOT YET EARNED
CP6-04                                         NOT STARTED / NOT AUTHORIZED
```

Part 17 supersedes only the exact repaired scopes listed in section 55.2. Parts 1–16 otherwise remain canonical and unchanged.

The exact next operation is a **fresh independent SECOND FULL TOMBSTONE AUDIT FROM ZERO over Parts 1–17**. It must not inherit PASS from either the pre-repair audit or this repair checkpoint.

If and only if that replay returns no unresolved semantic/structural/implementation blocker, Gate 03 may be recorded in a separate closure checkpoint. Entering CP6-04 remains a separate explicit user-approved materialization gate.