# Physical Model

- Status: **CLOSED AT TARGET-ARCHITECTURE LEVEL — SELECTED / ACCEPTED / INTEGRATED INTO MAIN VIA PR #15**
- Product: **DANTE** (`LifeOS` remains historical working-name evidence where present)
- Former workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Physical integration commit: `e6f191bad947388a44defe2c15f4939345084f58` via PR #15
- Physical phase-time PostgreSQL patch: **18.4 / HISTORICAL EXACT SELECTION EVIDENCE**
- PostgreSQL architecture family: **18 / SOLE CANONICAL PERSISTENCE + MATERIAL-HISTORY AUTHORITY**
- Current downstream PostgreSQL patch: **18.6 / CP6 DIRECT REMOTE FOUNDATION REGRESSION PASS**
- Current backend progression: **CP1–CP5 CLOSED; CP6-01 CLOSED / GATE 01 PASS; CP6-02 CLOSED / GATE 02 PASS; CP6-03 ACTIVE / CHECKPOINT J + DB-U23 CLOSED / FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT**
- Physical semantic benchmark/direct HG corpus: **DIRECT HG PASS 0 unless an exact qualifying scenario was executed elsewhere**

## 1. Purpose and historical boundary

This directory preserves the evidence, selection and accepted Physical architecture that translates the closed DANTE Domain + Logical model into implementation mechanisms.

The Physical Model itself is closed. CP6 consumes it; CP6 does not redesign it merely because concrete PostgreSQL schema work has begun.

PM-00..PM-14 preserve their phase-time facts exactly. Later backend implementation does not rewrite historical statements such as:

```text
PostgreSQL 18.4 selected
DATABASE DEPLOYMENT NOT STARTED
DIRECT HG PASS 0
```

when those statements accurately described the Physical checkpoint at the time.

For **current downstream implementation status**, use:

```text
../PROJECT-STATUS.md
../ROADMAP.md
../workstreams/logical-postgresql.md
```

## 2. PostgreSQL version truth

```text
ARCHITECTURE FAMILY
PostgreSQL 18
sole canonical persistence / material-history authority

PHYSICAL PHASE-TIME EXACT PATCH
PostgreSQL 18.4
historical selection evidence

CP2 / CP3 ORIGINAL DIRECT EVIDENCE
PostgreSQL 18.4
historical exact direct PASS

CURRENT CP6 TECHNICAL PATCH
PostgreSQL 18.6
configuration refresh APPLIED
direct remote foundation regression PASS
Backend CI run 32568664940
HEAD ec3dc795b5e044daa3a77723c94a1b4b5b92865c
```

A compatible maintenance patch inside PostgreSQL 18 is lifecycle maintenance and does not reopen the accepted Physical architecture. A future PostgreSQL major-version change is a separate review boundary.

## 3. Historical Physical checkpoint results

```text
PM-00   QA PASS
PM-01   PASS-CONDITIONAL
PM-02   COMPLETE
PM-03   STATIC COMPLETE / 0 REJECTS
PM-04A  COMPLETE / 0 EXECUTION-WORTHY GAPS
PM-04B  NOT ADMITTED
PM-05   COMPLETE
PM-06   EVIDENCE QUALIFICATION COMPLETE / DIRECT PERFORMANCE NOT RUN
PM-07   EVIDENCE QUALIFICATION COMPLETE / DIRECT DESTRUCTIVE RUNS NOT RUN
PM-08   SECONDARY/SPECIALIST QUALIFICATION COMPLETE
PM-09   EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE
PM-10   FINAL STACK RECOMMENDATION COMPLETE
PM-11   EXPLICIT TARGET STACK SELECTION COMPLETE
PM-12   ACCEPTED PHYSICAL MODEL COMPLETE
PM-13   CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS
PM-14   BRANCH / WORKSTREAM CLOSURE COMPLETE
PR #15  PROTECTED-MAIN INTEGRATION COMPLETE
```

## 4. Current Physical authority order

Read the closed Physical target from:

1. [`pm-11-explicit-selection-v1.md`](pm-11-explicit-selection-v1.md) — explicit selected target stack at phase time;
2. [`pm-12-accepted-physical-model-v1.md`](pm-12-accepted-physical-model-v1.md) — accepted Physical ownership/topology contract;
3. [`pm-13-clean-room-qa-v1.md`](pm-13-clean-room-qa-v1.md) — architecture/documentation clean-room QA;
4. [`pm-14-closure-v1.md`](pm-14-closure-v1.md) — Physical workstream closure evidence;
5. [`recommendation/post-selection-validation-register-v1.md`](recommendation/post-selection-validation-register-v1.md) — direct implementation-validation carry-forward;
6. [`result-register-v1.md`](result-register-v1.md) — Physical result ledger;
7. [`../workstreams/physical-model.md`](../workstreams/physical-model.md) — Physical durable handoff.

Current CP6 consumes, additionally:

```text
../development/backend-cp6-01-concrete-persistence-coverage.md
../development/backend-cp6-01-concrete-persistence-coverage-part-2.md
../development/backend-cp6-02-postgresql-persistence-constitution.md
../workstreams/logical-postgresql.md
../database/README.md
../database/dante-postgresql-database.md + Parts 2–8
```

The active Database Architecture & Reference must be consumed as one multi-part authority. Checkpoint J / `DB-U23` is closed; the Final Actual PostgreSQL Object Inventory is the next CP6-03 design block.

## 5. Non-negotiable barriers

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE TOKEN != MaterialStateRef
CANONICAL != PROVIDER / DERIVED / SECURITY STATE
SECONDARY != CANONICAL
LOCAL != CANONICAL
RUNTIME != DOMAIN HISTORY
MISSING != FALSE
EVIDENCE-QUALIFIED != EXECUTED PASS
EVIDENCE-WEIGHTED SCORE != VERIFIED-RUN SCORE
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
POSTGRESQL PATCH REFRESH != PHYSICAL REOPEN
CP3 TECHNICAL QA != BUSINESS-SEMANTIC HG PASS
DATABASE MATERIALIZATION != FIRST PRODUCT VERTICAL APPLICATION IMPLEMENTATION
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut is accepted.

## 6. Accepted target stack

The following preserves the accepted Physical target. Exact phase-time versions remain selection evidence; compatible downstream patch maintenance is separately lifecycle-managed.

```text
CANONICAL PRIMARY
PostgreSQL 18 architecture family
Physical phase-time exact patch 18.4
current CP6 technical patch 18.6

POSTGRESQL CAPABILITIES
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2

OFFLINE / SYNC
PowerSync Open Edition target
encrypted SQLite
PostgreSQL-backed PowerSync bucket storage
explicit client-safe sync projections

BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS-B
Restate runtime
initial DEV posture DORMANT / NOT ACTIVE

OBJECT BYTES
Cloudflare R2 Standard
private

RECOVERY TARGET
pgBackRest
AWS S3 Standard eu-south-1
Versioning
Object Lock GOVERNANCE / finite policy-bound retention

SOLVER
OR-Tools CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy
Grafana Cloud EU
pg_stat_statements
```

## 7. Canonical ownership

```text
PostgreSQL
= canonical DANTE truth + material history

PostGIS
= geospatial capability over PostgreSQL state

FTS / pg_trgm / unaccent / pgvector
= derived/query retrieval

SQLite / PowerSync
= bounded local/sync state

Restate
= durable execution runtime

R2
= raw object bytes

S3
= recovery copies

OR-Tools
= candidate solver state

OTel / Grafana
= operational telemetry
```

Canonical persistence authorities: **1 — PostgreSQL**.

## 8. Accepted PostgreSQL mapping thesis

The Physical selection accepted:

```text
owner-specific canonical tables/families
+
owner-specific material-state/history tables/families
+
specific relation tables/families
+
bounded technical address/control structures only where genuine heterogeneous addressing requires them
+
separate provider / projection / technical concerns
```

Explicitly rejected:

```text
universal Entity / Thing table
universal Relationship table
generic canonical EAV/property bag
universal event-log ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
PostgreSQL inheritance as ontology
```

## 9. Reference / state mapping carried into CP6

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor
```

Material state:

```text
stable semantic owner
+
bounded material-state address/control
+
owner-specific material-state row
+
explicit current accepted-state binding where required
+
retained owner-specific history
+
typed correction/replacement/reconciliation lineage
```

`MaterialStateRef` remains distinct from `xmin/xid`, timestamps, row hashes, ETags and provider revisions.

Simple binary relations use specific association tables/families. Qualified/material/n-ary relations preserve their actual contextual semantics rather than collapsing into generic edges.

## 10. Offline / specialist activation posture

Selected does not mean active.

```text
PowerSync / logical replication
→ activate on real offline/sync implementation

Restate
→ activate on first real Class-B durable workflow

pgBackRest + S3
→ activate at recovery/production boundary or real rehearsal

PgBouncer
→ activate when connection-pressure value exists
```

PostgreSQL transactional outbox is selected for bounded Class-A work but materializes only on a real Class-A requirement.

A PostgreSQL-native database structure required by the concrete DANTE schema may be implemented in CP6 without automatically activating its surrounding product/runtime capability.

## 11. Current CP6 downstream boundary

The current backend workstream has corrected an earlier process misunderstanding.

CP6 is allowed — and expected — to turn the closed model into the concrete DANTE database before the first product vertical.

```text
CP6-03
WHOLE DANTE DATABASE BLUEPRINT
CURRENT: CHECKPOINT J / DB-U23 CLOSED
NEXT: FINAL ACTUAL POSTGRESQL OBJECT INVENTORY
DB-U08 / DB-U15 / DB-U21 OPEN
SECOND FULL TOMBSTONE AUDIT REQUIRED BEFORE GATE 03
        ↓
GATE 03
NOT YET EARNED
        ↓
CP6-04
WHOLE DANTE DATABASE MATERIALIZATION
        ↓
CP6-05
WHOLE DATABASE DIRECT QA + CP6 CLOSURE
        ↓
POST-CP6
FIRST PRODUCT VERTICAL APPLICATION PHASE
```

Therefore CP6 may, after exact gates, create:

```text
DANTE business tables
Alembic business-schema migrations
SQLAlchemy database mappings
reference/material-state/history structures
specific relation tables
constraints / indexes / privileges
database-level direct tests
```

CP6 still does not implement first-product-vertical application use cases, application services, product persistence adapters, API or frontend.

This current execution boundary is owned by `../workstreams/logical-postgresql.md` and does not retroactively alter what PM-00..PM-14 or CP6-01/02 actually did at their checkpoints.

## 12. Current direct execution truth

Later backend work directly established the technical PostgreSQL substrate:

```text
BACKEND CP1–CP5                  CLOSED / INTEGRATED / DIRECT QA PASS
POSTGRESQL 18.4                  ORIGINAL CP2/CP3 HISTORICAL DIRECT PASS
CURRENT POSTGRESQL 18.6          DIRECT REMOTE QA PASS
18.6 CI RUN                      32568664940
18.6 EXECUTED HEAD               ec3dc795b5e044daa3a77723c94a1b4b5b92865c
POSTGIS 3.6.4                    CURRENT ENVELOPE PASS
PGVECTOR 0.8.6                   CURRENT ENVELOPE PASS
SQLALCHEMY / PSYCOPG             MATERIALIZED
ALEMBIC TECHNICAL BASELINE       MATERIALIZED / DIRECT QA PASS
DANTE SCHEMA / ROLE MODEL        MATERIALIZED / DIRECT QA PASS
REAL POSTGRESQL TEST HARNESS     MATERIALIZED / DIRECT QA PASS
DANTE BUSINESS DATABASE          NOT YET MATERIALIZED
SEMANTIC HG BLANKET PASS         NO
```

The PostgreSQL 18.6 run passed Backend Quality, Backend PostgreSQL and Backend CI Gate; 32 fast tests and 18 real-PostgreSQL tests covered the current 50-test corpus across the two mandatory lanes.

PostgreSQL 18.6 release-note impact review found no current post-upgrade action for the materialized technical foundation. Future capability activation must re-evaluate then-applicable maintenance requirements.

## 13. Current boundary summary

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 architecture family
phase-time exact patch 18.4

BACKEND FOUNDATION CP1–CP5
CLOSED / INTEGRATED / DIRECT QA PASS

CURRENT POSTGRESQL TECHNICAL PATCH
18.6 / DIRECT REMOTE FOUNDATION REGRESSION PASS

CP6
ACTIVE ON feature/logical-postgresql
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 ACTIVE / CHECKPOINT J + DB-U23 CLOSED
FINAL ACTUAL POSTGRESQL OBJECT INVENTORY NEXT
DB-U08 / DB-U15 / DB-U21 OPEN
GATE 03 NOT YET EARNED

DANTE BUSINESS DATABASE
NOT YET MATERIALIZED

FIRST PRODUCT VERTICAL APPLICATION
POST-CP6 / NOT STARTED
```