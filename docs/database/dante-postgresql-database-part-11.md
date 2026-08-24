<!-- DANTE-CANONICAL-CONTINUATION document="dante-postgresql-database.md" follows="dante-postgresql-database-part-10.md" -->

# DANTE PostgreSQL Database Architecture & Reference — Part 11

**Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / DB-U15 FINAL STRUCTURAL-QUERY INDEX MATRIX CLOSED  
**Scope:** section 42 onward  
**Authority:** this file is one physical part of the single canonical Database Architecture & Reference and MUST be consumed together with Parts 1–10  
**PRE-SCOPE for this DB-U15 closure:** `e53b4adfd38078450c2fa92bc0df9062679c5999`  
**Current PostgreSQL architecture:** PostgreSQL 18 major family / current technical patch 18.6  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  

Part 9 froze the surviving PostgreSQL object inventory. Part 10 closed DB-U08 and froze the exact naming standard. This continuation closes the next required axis: **the complete baseline structural/query index matrix justified by the frozen CP6 database graph**.

Nothing in this section adds or removes semantic objects, tables, columns, constraints, MaterialState facets or recurrence families. It decides only the PostgreSQL indexes justified now by already-accepted integrity, FK, current/history, lookup and concurrency paths.

---

## 42. DB-U15 — Final Structural / Query Index Matrix — CLOSED

### 42.1 Purpose

DB-U15 exists because PostgreSQL indexing is part of the concrete database contract, not an implementation afterthought.

The goal is not maximum index count. The goal is the smallest complete baseline that supports:

```text
primary / unique enforcement
foreign-key parent lifecycle checks
accepted current/history integrity
material-state owner/facet lookup
known owner/context joins
bounded integrity-routine access
accepted Recurrence / Occurrence generation concurrency paths
```

while refusing indexes whose value depends on an application workload that does not yet exist.

The review consumed:

```text
Part 9 frozen 68-table / 5-view object inventory
Part 9 78-index minimum structural floor
Part 9 14 integrity roles / 75 trigger attachments
Part 10 final PostgreSQL naming standard
Part 10 exact 68 FK relationship inventory
CP6-02 IDX-01..IDX-09
accepted Schedule / Actual / Session current-history contracts
accepted Routine/Event Recurrence aggregate contract
accepted Occurrence generation / quota concurrency contract
ON DELETE NO ACTION default lifecycle posture
real current backend state: no materialized business schema or measured product query workload yet
```

### 42.2 Governing index doctrine

The closed CP6-02 Constitution remains authoritative:

```text
IDX-01
index only for a proven access or invariant need

IDX-02
every referencing FK receives an explicit review
PostgreSQL does not create referencing-side FK indexes automatically

IDX-03
composite key order follows real equality/range/sort/filter usage

IDX-04
partial indexes require a stable predicate

IDX-05
INCLUDE is evidence-driven

IDX-06
GiST / SP-GiST / GIN / HNSW / IVFFlat etc. require an actual operator/query/capability need

IDX-07
redundant indexes are forbidden

IDX-08
large live-table index creation may require a migration-safe concurrent/staged method

IDX-09
index/extension maintenance remains part of lifecycle QA
```

Therefore DB-U15 explicitly rejects both extremes:

```text
UNDER-INDEXING
→ relying on application filtering or sequential scans for already-known integrity/FK paths

OVER-INDEXING
→ indexing every FK/column/timestamp/discriminator merely because it exists
```

### 42.3 Index classes and final count

The complete CP6 baseline index set is now:

```text
INHERITED / ALREADY FROZEN IN PART 9 + PART 10
68  PK-backed B-tree indexes
 2  UNIQUE-constraint-backed B-tree indexes
 2  MaterialState owner/facet partial lookup indexes
 5  partial UNIQUE open-current-history indexes
 1  partial UNIQUE open-Session-pause index
---
78  existing structural floor

ADDED BY DB-U15
16  referencing-side FK / structural join indexes
 1  accepted quota-period query/concurrency index
---
17  additional indexes

FINAL CP6 BASELINE
95  DANTE-owned PostgreSQL index objects
```

All new DB-U15 indexes use ordinary PostgreSQL B-tree. No new extension or non-B-tree access method is required.

### 42.4 The 78 inherited structural indexes remain unchanged

DB-U15 does not rename, replace or duplicate the Part-10 section 40.12 floor.

It remains exactly:

```text
68 PK-backed indexes

2 UNIQUE-constraint-backed indexes
  uq_native_current_material_state_material_state_ref
  uq_scoped_current_material_state_material_state_ref

2 MaterialState partial owner/facet indexes
  ix_material_state_address_native_owner_ref_facet_code
  ix_material_state_address_scoped_owner_ref_facet_code

5 partial UNIQUE current-history indexes
  ux_schedule_placement_current_history_open
  ux_actual_realization_current_history_open
  ux_session_timing_current_history_open
  ux_routine_recurrence_current_history_open
  ux_event_recurrence_current_history_open

1 partial UNIQUE open-pause index
  ux_session_timing_pause_open
```

The 68 exact `pk_*` names remain those frozen in Part 10 section 40.8.

### 42.5 Complete 68-FK referencing-side review

PostgreSQL automatically indexes the referenced PK/UNIQUE side where those constraints require it, but it does not automatically create an index on every referencing FK column.

DANTE therefore replayed all 68 FK relationships one by one against:

```text
existing PK leading columns
existing UNIQUE indexes
existing partial indexes
parent ON DELETE / UPDATE checks
integrity-routine lookups
ordinary owner/context joins
known concurrency paths
```

Final result:

```text
TOTAL FKs REVIEWED                         68
already adequately covered                 52
requiring DB-U15 referencing-side index     16
unreviewed                                  0
```

A FK is considered covered only where an already-existing index can support the exact referencing-column lookup as a leading/equality-access path. Merely containing the FK column later in an unrelated composite key does not count.

### 42.6 Why 52 FKs need no additional index

The 52 covered relationships fall into four exact classes.

#### A. Referencing FK is the whole PK

Many typed material payloads use:

```text
material_state_ref PRIMARY KEY
→ FK parent_state(material_state_ref)
```

or Occurrence generation coordinate children use:

```text
occurrence_ref PRIMARY KEY
→ FK occurrence_generation(occurrence_ref)
```

The PK B-tree already provides the exact FK lookup. A second index would be redundant and is forbidden by IDX-07.

#### B. Referencing FK is the leading PK column

Examples:

```text
schedule_placement_current_history.schedule_ref
→ PK(schedule_ref, current_from_at)

actual_realization_session_basis.actual_material_state_ref
→ PK(actual_material_state_ref, session_ref)

session_timing_pause.material_state_ref
→ PK(material_state_ref, paused_at)

routine/event recurrence selector children.material_state_ref
→ composite PK begins with material_state_ref
```

The existing PK already supports the parent-check/join path.

#### C. Referencing FK has a dedicated UNIQUE index

Both current-binding tables have:

```text
UNIQUE(material_state_ref)
```

which already provides the required B-tree lookup.

#### D. Referencing FK is covered by the accepted MaterialState partial owner index

`material_state_address` has exactly-one owner space. The accepted partial indexes are:

```text
(native_owner_ref, facet_code)
WHERE native_owner_ref IS NOT NULL

(scoped_owner_ref, facet_code)
WHERE scoped_owner_ref IS NOT NULL
```

A parent FK check for a non-null owner reference implies the partial predicate, so those indexes already provide the referencing lookup. Separate single-column indexes would be redundant.

### 42.7 Sixteen new referencing-side indexes — exact manifest

The following 16 FK paths are not adequately covered by an existing leading PK/UQ/partial index and are structurally justified now.

#### Schedule

```text
1. ix_schedule_subject_native_ref
   ON dante.schedule USING btree (subject_native_ref)

   supports:
   - native_address parent delete/update checks
   - subject → Schedule lookup
   - bounded NativeRef integrity path

2. ix_schedule_placement_state_schedule_ref
   ON dante.schedule_placement_state USING btree (schedule_ref)

   supports:
   - Schedule parent lifecycle checks
   - owner → historical placement-state lookup
   - owner-completeness / material-state integrity

3. ix_schedule_placement_current_history_material_state_ref
   ON dante.schedule_placement_current_history USING btree (material_state_ref)

   supports:
   - placement-state parent lifecycle checks
   - exact state → currentness-history lookup
   - current/history equivalence verification
```

#### Actual

```text
4. ix_actual_subject_native_ref
   ON dante.actual USING btree (subject_native_ref)

5. ix_actual_realization_state_actual_ref
   ON dante.actual_realization_state USING btree (actual_ref)

6. ix_actual_realization_session_basis_session_ref
   ON dante.actual_realization_session_basis USING btree (session_ref)

7. ix_actual_realization_session_basis_timing_state
   ON dante.actual_realization_session_basis USING btree (session_timing_material_state_ref)

8. ix_actual_realization_current_history_material_state_ref
   ON dante.actual_realization_current_history USING btree (material_state_ref)
```

Justification:

```text
subject_native_ref
→ parent checks + subject → Actual lookup

actual_ref
→ Actual → realization-state lookup + owner completeness

session_ref
→ Session parent checks + Session → dependent Actual-basis rows

session_timing_material_state_ref
→ exact Session timing-state parent checks and historical basis lookup

history.material_state_ref
→ exact realization state → currentness episodes
```

The long timing-state index name follows the DB-U08 explicit semantic-alias rule; the stored key remains the full column `session_timing_material_state_ref`.

#### Session

```text
9. ix_session_timing_state_session_ref
   ON dante.session_timing_state USING btree (session_ref)

10. ix_session_timing_current_history_material_state_ref
    ON dante.session_timing_current_history USING btree (material_state_ref)
```

These support Session parent lifecycle/completeness and exact timing-state history lookup respectively.

#### Routine / Event Recurrence

```text
11. ix_routine_recurrence_state_routine_ref
    ON dante.routine_recurrence_state USING btree (routine_ref)

12. ix_event_recurrence_state_event_ref
    ON dante.event_recurrence_state USING btree (event_ref)

13. ix_routine_recurrence_current_history_material_state_ref
    ON dante.routine_recurrence_current_history USING btree (material_state_ref)

14. ix_event_recurrence_current_history_material_state_ref
    ON dante.event_recurrence_current_history USING btree (material_state_ref)
```

The first pair supports owner completeness, owner → recurrence-state lookup and parent checks. The second pair supports exact recurrence-state → currentness-history lookup and current/history equivalence.

#### Occurrence generation

```text
15. ix_occurrence_generation_source_governing_state
    ON dante.occurrence_generation USING btree (
      source_native_ref,
      governing_recurrence_state_ref,
      occurrence_ref
    )

16. ix_occurrence_generation_governing_recurrence_state_ref
    ON dante.occurrence_generation USING btree (
      governing_recurrence_state_ref
    )
```

Index 15 deliberately does more than a single-column FK index while still satisfying the `source_native_ref` FK because `source_native_ref` is the leading key.

Its key order follows the already-accepted generation operation:

```text
same source
+
same governing recurrence state
→ enumerate materialized Occurrences deterministically
```

`occurrence_ref` is included as the third **key column**, not an INCLUDE payload, because it is the join identity into the exact generation-coordinate child and gives deterministic narrow key traversal without requiring an evidence-free covering-index policy.

Index 16 remains necessary because `governing_recurrence_state_ref` is not the leading column of index 15 and PostgreSQL parent checks / direct state-based lookup must not depend on scanning every source prefix.

### 42.8 Seventeen-th index — quota-period concurrency/query path

The one accepted non-FK query index added by DB-U15 is:

```text
17. ix_occurrence_generation_quota_period
    ON dante.occurrence_generation_quota USING btree (
      period_start_date,
      period_end_date_exclusive,
      occurrence_ref
    )
```

This is not speculative product optimization.

The closed Recurrence/Occurrence generation contract already requires the quota materialization transaction to:

```text
lock the exact Routine/Event source deterministically
→ verify the governing recurrence MaterialStateRef
→ derive the exact quota period
→ count already materialized recurrence_generated Occurrences
   for the same source
   + same governing recurrence state
   + same exact quota period
→ reject when count >= quota_count
```

The final access path is therefore intentionally supported from both sides:

```text
occurrence_generation
ix_occurrence_generation_source_governing_state
→ source + governing state + occurrence identity

occurrence_generation_quota
ix_occurrence_generation_quota_period
→ exact period + occurrence identity
```

The operation joins on `occurrence_ref` and remains protected by the accepted deterministic source-row lock discipline. No fake quota slot/ordinal is introduced merely for indexing.

### 42.9 Final DB-U15 index manifest added to the 78-floor

The exact 17 names introduced by DB-U15 are:

```text
ix_schedule_subject_native_ref
ix_schedule_placement_state_schedule_ref
ix_schedule_placement_current_history_material_state_ref

ix_actual_subject_native_ref
ix_actual_realization_state_actual_ref
ix_actual_realization_session_basis_session_ref
ix_actual_realization_session_basis_timing_state
ix_actual_realization_current_history_material_state_ref

ix_session_timing_state_session_ref
ix_session_timing_current_history_material_state_ref

ix_routine_recurrence_state_routine_ref
ix_event_recurrence_state_event_ref
ix_routine_recurrence_current_history_material_state_ref
ix_event_recurrence_current_history_material_state_ref

ix_occurrence_generation_source_governing_state
ix_occurrence_generation_governing_recurrence_state_ref
ix_occurrence_generation_quota_period
```

Naming audit:

```text
new identifiers                     17
unique identifiers                  17
collisions                           0
identifiers > 63 bytes               0
longest new identifier              56 bytes
quoted identifiers                   0
silent PostgreSQL truncation         0
```

### 42.10 Access method and sort semantics

All 95 baseline indexes are ordinary B-tree except where PostgreSQL internally represents the already-frozen constraint/index class under the same ordinary B-tree semantics.

DB-U15 introduces no:

```text
GiST
SP-GiST
GIN
BRIN
HASH
HNSW
IVFFlat
```

because the frozen baseline currently has no query/invariant requiring those methods.

Default ascending key order is sufficient. No baseline query requires a physically declared descending index.

### 42.11 Current/history path review — PASS

Each current-history table has two distinct access needs and both are now covered:

```text
owner → history ordered by current_from_at
→ existing PK(owner_ref, current_from_at)

owner → open episode
→ existing partial UNIQUE(owner_ref)
  WHERE current_until_at IS NULL

MaterialStateRef → history episode(s)
→ DB-U15 material_state_ref index
```

This applies to:

```text
schedule_placement_current_history
actual_realization_current_history
session_timing_current_history
routine_recurrence_current_history
event_recurrence_current_history
```

No index on `current_until_at` alone is justified.

### 42.12 MaterialState control lookup review — PASS

`material_state_address` already has:

```text
PRIMARY KEY(material_state_ref)

(native_owner_ref, facet_code)
WHERE native_owner_ref IS NOT NULL

(scoped_owner_ref, facet_code)
WHERE scoped_owner_ref IS NOT NULL
```

This supports:

```text
MaterialStateRef → exact address
native owner + facet → state-address candidates
scoped owner + facet → state-address candidates
parent FK checks for non-null native/scoped owner references
```

No standalone index is added on:

```text
facet_code
native_owner_ref
scoped_owner_ref
```

because the accepted paths are owner-addressed rather than global facet scans.

### 42.13 Native/scoped address discriminator review — NO INDEX

No standalone indexes are created on:

```text
native_address.owner_family
scoped_address.scoped_family
```

Reasons:

```text
canonical lookup is by *_ref PK
bounded dispatch validators use one addressed row, not global family scans
no baseline operational/reporting query requires family enumeration
family values are low-cardinality discriminators
```

If a future operational maintenance workload proves a family scan material, that future database evolution may add an index with evidence. CP6 does not anticipate it.

### 42.14 Schedule temporal index review — NO GiST / date-time scan index

Schedule contains:

```text
daterange
timestamp without time zone
timestamptz
```

but existence of temporal columns is not itself an index requirement.

No baseline index is introduced on:

```text
schedule_placement_date_state.date_span
starts_local_at
ends_local_at
starts_at
ends_at
resolved_start_at
resolved_end_at
```

and no GiST/EXCLUDE structure is created merely because `daterange` supports it.

Reason:

```text
Schedule accepted placement
!= Capacity reservation
!= universal conflict calendar
```

No accepted invariant says two Schedule placements may not overlap. A future actual scheduling/calendar vertical may prove concrete range-query indexes, but CP6 cannot invent that workload now.

### 42.15 Session chronology index review — no speculative timestamp indexes

No baseline standalone indexes are added on:

```text
session_timing_absolute.started_at
session_timing_absolute.ended_at
session_timing_pause.paused_at
session_timing_pause.resumed_at
```

The pause table PK already begins with `material_state_ref` and orders within a state by `paused_at`.

The one-open-pause invariant remains the existing partial unique index:

```text
ux_session_timing_pause_open
UNIQUE(material_state_ref)
WHERE resumed_at IS NULL
```

Global timeline/report queries are product-level workload evidence not yet present.

### 42.16 Recurrence selector/index review — PK coverage sufficient

The Routine/Event selector children use composite PKs such as:

```text
(material_state_ref, wall_time)
(material_state_ref, weekday_number)
(material_state_ref, month_day)
(material_state_ref, weekday_number, ordinal)
(material_state_ref, month_number, month_day)
(material_state_ref, position_index)
```

The accepted integrity/generation algorithms load selectors for one governing recurrence state. Their leading `material_state_ref` PK access is therefore already optimal for the known path.

No reverse/global indexes are added on selector values such as:

```text
weekday_number
month_day
wall_time
position_index
```

because no baseline query asks “find every recurrence using Tuesday/09:00/day 15”.

### 42.17 IANA timezone lookup review — no persisted zone index

`zone_id` appears in bounded temporal/recurrence payloads, but timezone validation is a narrow value-validation routine against PostgreSQL/tzdb vocabulary.

No DANTE baseline query scans business rows by timezone, so DB-U15 adds no index on any `zone_id` column.

### 42.18 No INCLUDE baseline

No new index uses PostgreSQL `INCLUDE`.

Reason:

```text
no materialized application workload yet
no measured index-only-scan benefit
no proven hot read projection
```

The quota-period index keeps `occurrence_ref` as an actual key because it participates in exact join traversal and deterministic key ordering. This is not an INCLUDE workaround.

### 42.19 No BRIN baseline

BRIN is valuable for sufficiently large naturally correlated append-like tables. CP6 currently has neither:

```text
materialized business table size evidence
nor accepted large time-range scan workload
```

Therefore adding BRIN on history/timestamp columns now would be technology enthusiasm rather than a closed requirement.

### 42.20 No GIN/trigram/vector/search indexes

Part 9 already determined that the CP6 baseline materializes no persisted search/vector capability.

Therefore:

```text
pg_trgm extension selected/present       != trigram index required
vector extension selected/present        != vector column/index required
PostGIS selected/present                 != spatial index required
PostgreSQL FTS capability                != GIN search index required
```

DB-U15 adds zero:

```text
GIN
trigram
HNSW
IVFFlat
spatial GiST
persisted FTS index
```

The capability-triggered future dispositions from Checkpoint I remain intact.

### 42.21 No duplicate UUID indexes

Every stable native/scoped/material identity already indexed through a PK/UQ is left alone.

UUIDv7 time ordering does not justify another index and must not be used as semantic chronology.

### 42.22 Parent DELETE / UPDATE integrity posture

The baseline uses `ON DELETE NO ACTION` and stable identity/reference semantics.

The 16 added referencing indexes ensure that parent checks do not require unnecessary full scans on the known uncovered FK paths.

This index support does **not** authorize semantic parent deletion. It only makes the database mechanism supporting the accepted lifecycle contract structurally sound.

### 42.23 Trigger/integrity-routine query review

The 14 frozen integrity roles were replayed against the final indexes.

Result:

```text
NativeAddress / ScopedAddress owner binding
→ direct concrete owner PK lookup

NativeRef eligibility
→ native_address PK lookup

MaterialState totality
→ material_state_ref PK + owner/facet partial indexes

current binding
→ current PK/UQ + material_state address PK

current-history equivalence
→ owner history PK + open partial UNIQUE + new material_state_ref indexes

owner creation completeness
→ new owner→state indexes where state owner FK was uncovered

Schedule payload totality
→ child PK material_state_ref

Actual basis
→ Actual-state PK + new Session/timing reverse indexes

Session timing totality/pause consistency
→ state/payload PKs + pause PK/open partial unique

Recurrence aggregate integrity
→ recurrence state owner indexes + child PK-leading material_state_ref

Occurrence generation integrity
→ occurrence generation source/governing indexes + coordinate PKs

IANA timezone validation
→ no business-table timezone scan required
```

No missing structural index remains for a currently frozen integrity routine.

### 42.24 Quota concurrency path — explicit index + lock boundary

Indexing does not replace transaction correctness.

The quota path remains:

```text
lock concrete Routine/Event source row
→ verify expected governing recurrence MaterialStateRef
→ derive exact quota period
→ query/count materialized rows through the two accepted indexes
→ require count < quota_count
→ insert Occurrence + generation coordinate
→ COMMIT
```

The source-row lock serializes competing quota materializations for one concrete source. The indexes bound the lookup cost. No index is treated as a concurrency primitive by itself.

### 42.25 Migration-time index construction posture

CP6-04 begins from a database that has no DANTE business tables today.

For the first whole-database materialization, these baseline indexes can be created transactionally together with their bounded migration batches unless the later migration DAG identifies a concrete reason not to.

`CREATE INDEX CONCURRENTLY` is therefore **not automatically required** for the initial empty-schema materialization.

Future live-table evolution remains governed by IDX-08 / MIG-19:

```text
large live table + lock-risk evidence
→ consider CREATE INDEX CONCURRENTLY / staged rollout
→ isolate non-transactional boundary
→ define invalid-index cleanup/retry
```

DB-U15 does not pre-authorize concurrent DDL where it is unnecessary.

### 42.26 Index naming compliance — PASS

All 17 new identifiers comply with Part 10 DB-U08:

```text
ASCII lower_snake_case
unquoted
ix_ prefix
semantic purpose traceable
<= 63 bytes
collision-free
```

No Part-10 index name is changed.

### 42.27 Final negative-index ledger

DB-U15 explicitly rejects the following CP6 baseline additions:

```text
standalone native_address.owner_family index
standalone scoped_address.scoped_family index
standalone material_state_address.facet_code index
standalone current-history current_until_at indexes
standalone every-timestamp indexes
Schedule daterange GiST merely because daterange exists
Schedule overlap EXCLUDE constraint/index
Session global chronology indexes without workload
Recurrence selector reverse indexes
zone_id indexes
BRIN history/timestamp indexes without scale workload
GIN text/JSON/search indexes
pg_trgm indexes
pgvector HNSW/IVFFlat indexes
PostGIS spatial indexes
INCLUDE covering indexes without measured need
one redundant index per PK/UQ-backed FK
one automatic index per FK regardless of existing prefix coverage
```

These are negative baseline decisions, not claims that such indexes can never exist. A later real workload may trigger a normal evidence-backed schema evolution.

### 42.28 Final matrix summary

```text
DANTE TABLES                                  68
DANTE VIEWS                                    5

TOTAL FKs                                     68
FKs REVIEWED                                  68
FKs ALREADY COVERED                           52
NEW FK/STRUCTURAL INDEXES                     16

PRE-DB-U15 INDEX FLOOR                        78
NEW FK/STRUCTURAL INDEXES                     16
NEW NON-FK QUERY/CONCURRENCY INDEX             1
-----------------------------------------------
FINAL CP6 BASELINE INDEXES                    95

B-TREE BASELINE                              95
NEW GiST/SP-GiST/GIN/BRIN/HASH                 0
NEW HNSW/IVFFlat                               0
NEW INCLUDE                                    0
NEW speculative search/spatial/vector index    0

UNREVIEWED FK                                  0
UNJUSTIFIED BASELINE INDEX                     0
KNOWN REQUIRED INDEX GAP                       0
```

### 42.29 DB-U15 closure

DB-U15 is now closed.

```text
DB-U15
FINAL STRUCTURAL / QUERY INDEX MATRIX
CLOSED / PASS

78-INDEX STRUCTURAL FLOOR
RETAINED

68-FK REFERENCING REVIEW
COMPLETE

16 NEW FK/STRUCTURAL INDEXES
FROZEN

1 QUOTA QUERY/CONCURRENCY INDEX
FROZEN

FINAL BASELINE INDEX COUNT
95

REDUNDANCY REVIEW
PASS

ACCESS-METHOD REVIEW
PASS

SPECULATIVE INDEXES
0
```

No Domain, Logical, Physical, object-inventory or naming reopening is required.

The surviving global DB-U register is now exactly:

```text
DB-U21  exact object-level PostgreSQL privilege matrix
```

### 42.30 Exact next CP6-03 block

The next design block is:

```text
DB-U21 — EXACT OBJECT-LEVEL POSTGRESQL PRIVILEGE MATRIX
```

Required remaining sequence:

```text
DB-U21 exact object-level privilege matrix
→ migration/materialization DAG
→ SQLAlchemy mapping plan
→ Database Dictionary readiness
→ direct PostgreSQL proof/test plan
→ SECOND FULL TOMBSTONE AUDIT FROM ZERO
→ Gate 03 only if clean
```

### 42.31 CP6-04 boundary remains closed

DB-U15 closure is documentation/design only.

```text
CREATE INDEX                          NOT AUTHORIZED
Alembic business migration creation  NOT AUTHORIZED
SQLAlchemy business mapping creation NOT AUTHORIZED
CREATE TABLE / VIEW                   NOT AUTHORIZED
CREATE FUNCTION / TRIGGER             NOT AUTHORIZED
business ACL materialization          NOT AUTHORIZED
```

CP6-04 remains NOT STARTED / NOT AUTHORIZED.

---

## 43. Current continuation state

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
```

Current checkpoint state:

```text
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY
FROZEN

DB-U08 FINAL POSTGRESQL OBJECT NAMING
CLOSED

DB-U15 FINAL STRUCTURAL / QUERY INDEX MATRIX
CLOSED

FINAL CP6 BASELINE INDEX COUNT
95

GLOBAL DB-U OPEN
DB-U21 ONLY

NEXT
DB-U21 EXACT OBJECT-LEVEL POSTGRESQL PRIVILEGE MATRIX

SECOND FULL TOMBSTONE AUDIT
NOT YET RUN

GATE 03
NOT YET EARNED

CP6-04
NOT STARTED / NOT AUTHORIZED
```

Part 11 supersedes older CURRENT/resume statements only where those statements still say DB-U15 is open/next or the 78-index floor is the final index count. Historical evidence and the Part-9 statement that 78 was a pre-DB-U15 minimum floor remain true in their original phase context.
