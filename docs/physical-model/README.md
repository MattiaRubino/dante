# Physical Model

- **Status:** CLOSED AT TARGET-ARCHITECTURE LEVEL — SELECTED / ACCEPTED / INTEGRATED VIA PR #15
- **Product:** DANTE (`LifeOS` remains historical working-name evidence where present)
- **Former workstream branch:** `feature/physical-model` — MERGED / AUTO-DELETED
- **Physical integration commit:** `e6f191bad947388a44defe2c15f4939345084f58`
- **PostgreSQL architecture family:** 18 / sole canonical persistence + material-history authority
- **Physical phase-time exact patch:** 18.4 / historical selection evidence
- **Current downstream PostgreSQL patch:** 18.6
- **Current downstream database state:** CP1–CP6 CLOSED; CP6 integrated via PR #42; LOCAL PostgreSQL Recovery integrated via PR #47
- **Current protected-main database head:** Alembic `20260830_09` / `69|5|15|76|97|69|123|0|0|0`

## 1. Purpose and historical boundary

This directory preserves the accepted Physical architecture that translates the closed DANTE Domain + Logical model into implementation mechanisms.

The Physical Model is closed. Later implementation consumes it; later implementation does not rewrite phase-time evidence. Historical Physical statements such as:

```text
PostgreSQL 18.4 selected
DATABASE DEPLOYMENT NOT STARTED
DIRECT HG PASS 0
```

remain valid only for the checkpoint at which they were written.

For current downstream implementation status use:

```text
../PROJECT-STATUS.md
../ROADMAP.md
../database/README.md
```

`../workstreams/logical-postgresql.md` and PM checkpoint files are historical/phase-time evidence, not current resume routes.

## 2. PostgreSQL version truth

```text
ARCHITECTURE FAMILY
PostgreSQL 18
sole canonical persistence / material-history authority

PHYSICAL PHASE-TIME EXACT PATCH
18.4 / historical selection evidence

CP2 / CP3 ORIGINAL DIRECT EVIDENCE
18.4 / historical exact direct PASS

CURRENT REPOSITORY / DATABASE PATCH
18.6
```

A compatible maintenance patch inside PostgreSQL 18 is lifecycle maintenance and does not reopen the accepted Physical architecture. A PostgreSQL major-version change is a separate architecture/revalidation boundary.

## 3. Historical Physical checkpoint result

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

## 4. Authority order

Read the closed Physical target from:

1. [`pm-11-explicit-selection-v1.md`](pm-11-explicit-selection-v1.md) — selected target stack at phase time;
2. [`pm-12-accepted-physical-model-v1.md`](pm-12-accepted-physical-model-v1.md) — accepted ownership/topology contract;
3. [`pm-13-clean-room-qa-v1.md`](pm-13-clean-room-qa-v1.md) — clean-room QA;
4. [`pm-14-closure-v1.md`](pm-14-closure-v1.md) — workstream closure evidence;
5. [`recommendation/post-selection-validation-register-v1.md`](recommendation/post-selection-validation-register-v1.md) — implementation-validation carry-forward;
6. [`result-register-v1.md`](result-register-v1.md) — Physical result ledger.

Current concrete persistence is owned downstream by:

```text
../development/backend-cp6-02-postgresql-persistence-constitution.md
../development/backend-cp6-05-whole-database-qa.md
../decisions/ADR-010-postgresql-persistence-constitution.md
../database/README.md
../database/dante-postgresql-database.md + current continuation parts
../operations/postgres-recovery-runbook.md
```

CP6 is CLOSED / integrated via PR #42. The accepted LOCAL Recovery workstream then added normal forward evolution `20260830_09` and was integrated into protected `main` via PR #47. The former Recovery branch is historical; current protected-main database/recovery truth lives in the sources above.

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
DATABASE MATERIALIZATION != PRODUCT-VERTICAL APPLICATION IMPLEMENTATION
LOCAL RECOVERY PASS != REMOTE/CLOUD PRODUCTION RECOVERY PASS
```

No universal Entity/Thing/EAV/generic-edge canonical shortcut is accepted.

## 6. Accepted target stack

The target below preserves the Physical selection. Selection and activation are separate facts.

```text
CANONICAL PRIMARY
PostgreSQL 18

POSTGRESQL CAPABILITIES
PostGIS
pgvector
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer target

OFFLINE / SYNC
PowerSync Open Edition target
encrypted SQLite
PostgreSQL-backed bucket storage
explicit client-safe sync projections

BOUNDED ASYNC
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS-B
Restate runtime target

OBJECT BYTES
Cloudflare R2 Standard / private

PHYSICAL PHASE-TIME RECOVERY TARGET
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

The historical S3 selection is phase-time Physical target evidence. It is **not** a claim that the current repository has activated a remote recovery provider.

Current recovery activation boundary:

```text
pgBackRest LOCAL recovery   IMPLEMENTED / DIRECTLY REHEARSED / INTEGRATED VIA PR #47
remote backup provider      TBD / NOT ACTIVATED
production/cloud recovery   NOT CLAIMED
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

remote recovery object storage
= recovery copies only, never canonical DANTE state

OR-Tools
= candidate solver state

OTel / Grafana
= operational telemetry
```

Canonical persistence authorities: **1 — PostgreSQL**.

## 8. Accepted PostgreSQL mapping thesis

```text
owner-specific canonical tables/families
+
owner-specific material-state/history tables/families
+
specific relation tables/families
+
bounded technical address/control structures only for genuine heterogeneous addressing
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

Reference/state rules carried into implementation:

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor

MaterialStateRef
→ stable semantic address
→ bounded material-state control
→ owner-specific material-state row
→ explicit current accepted-state binding where required
→ retained history + typed lineage
```

`MaterialStateRef` remains distinct from MVCC/xmin/xid, timestamps, hashes, ETags and provider revisions.

## 9. Capability activation posture

Selected does not mean active.

```text
PowerSync / logical replication
→ real offline/sync implementation

Restate
→ first real Class-B durable workflow

PgBouncer
→ demonstrated connection-pressure need + direct validation

pgBackRest LOCAL
→ activated, directly rehearsed and integrated by the closed LOCAL Recovery workstream

remote backup provider
→ TBD; select/activate only at a real production deployment boundary with provider-specific proof
```

PostgreSQL-native structures required by the concrete DANTE schema may be implemented without automatically activating surrounding product/provider capabilities.

## 10. Current downstream implementation truth

```text
BACKEND CP1–CP5                    CLOSED / INTEGRATED / DIRECT QA PASS
CP6 CONCRETE POSTGRESQL DATABASE   CLOSED / INTEGRATED VIA PR #42
POSTGRESQL                         18.6
HISTORICAL PRE-RECOVERY CP6 HEAD   20260826_08
HISTORICAL PRE-RECOVERY TOPOLOGY   68|5|14|75|95|68|120|0|0|0
CURRENT PROTECTED-MAIN HEAD        20260830_09
CURRENT PROTECTED-MAIN TOPOLOGY    69|5|15|76|97|69|123|0|0|0
DANTE BUSINESS DATABASE            MATERIALIZED
LOCAL POSTGRESQL RECOVERY          CP01–CP07 PASS / CLOSED / INTEGRATED VIA PR #47
REMOTE BACKUP PROVIDER             TBD / NOT ACTIVATED
PRODUCTION/CLOUD RECOVERY          NOT CLAIMED
SEMANTIC HG BLANKET PASS           NO
```

The CP6 closure proof remains in `../development/backend-cp6-05-whole-database-qa.md`. Current database/recovery truth is owned by `../database/README.md`, current migrations/mappings/tests and `../operations/postgres-recovery-runbook.md`.

## 11. Current boundary summary

```text
PHYSICAL MODEL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 architecture family
phase-time exact patch 18.4 / historical

CONCRETE DATABASE
CP6 CLOSED / INTEGRATED VIA PR #42
PostgreSQL 18.6
business database MATERIALIZED

CURRENT PROTECTED-MAIN RECOVERY EVOLUTION
Alembic 20260830_09
69|5|15|76|97|69|123|0|0|0
CP01–CP07 LOCAL PASS / CLOSED / INTEGRATED VIA PR #47
remote provider TBD / NOT ACTIVATED
production/cloud recovery NOT CLAIMED

PRODUCT / PLATFORM WORK
post-CP6 bounded workstreams; exact status comes from live Git + current project/workstream authority
```
