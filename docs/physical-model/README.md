# DANTE Physical Model

- **Status:** CLOSED / SELECTED / ACCEPTED / INTEGRATED VIA PR #15
- **Product:** DANTE (`LifeOS` remains historical working-name evidence where present)
- **Former branch:** `feature/physical-model` — merged / deleted
- **Integration commit:** `e6f191bad947388a44defe2c15f4939345084f58`
- **Architecture family:** PostgreSQL 18
- **Physical phase-time exact patch:** PostgreSQL 18.4 / historical selection evidence
- **Current downstream repository patch:** PostgreSQL 18.6
- **Current downstream status authority:** `../PROJECT-STATUS.md`, `../ROADMAP.md`, `../database/README.md`

## 1. Purpose and lifecycle

This directory preserves the accepted Physical architecture that translates the closed DANTE Product / Domain / Logical model into implementation mechanisms.

The Physical phase is closed. Its PM-00..PM-14 artifacts preserve exact phase-time selection, rationale and QA evidence. Later backend/database implementation does not rewrite that historical evidence, but this README is a current navigation surface and therefore must not report old CP6 progress as present state.

Use:

```text
../PROJECT-STATUS.md
../ROADMAP.md
../database/README.md
```

for current implementation, Alembic, catalog and integration status.

## 2. Authority order

Primary accepted Physical artifacts:

1. `pm-11-explicit-selection-v1.md` — selected target stack;
2. `pm-12-accepted-physical-model-v1.md` — accepted Physical ownership/topology contract;
3. `pm-13-clean-room-qa-v1.md` — architecture/documentation QA;
4. `pm-14-closure-v1.md` — Physical closure evidence;
5. `recommendation/post-selection-validation-register-v1.md` — implementation-validation carry-forward;
6. `result-register-v1.md` — Physical result ledger.

Current PostgreSQL implementation/reference authority lives downstream in:

```text
../development/backend-cp6-02-postgresql-persistence-constitution.md
../decisions/ADR-010-postgresql-persistence-constitution.md
../database/README.md
../database/dictionary/
Alembic + SQLAlchemy + real PostgreSQL + direct tests
```

Phase-time PM evidence remains valid evidence; it does not override later executable/current-reference truth.

## 3. Permanent non-collapse barriers

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
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
POSTGRESQL PATCH REFRESH != PHYSICAL REOPEN
DATABASE MATERIALIZATION != PRODUCT SEMANTIC COLLAPSE
```

Rejected as global shortcuts:

```text
universal Entity / Thing table
universal Relationship / generic edge
canonical EAV / property bag
universal event-log ontology
universal Fact / Version semantic payload root
JSONB required-semantic escape hatch
PostgreSQL inheritance as ontology
```

## 4. Accepted target stack

The selected architecture remains:

```text
CANONICAL PRIMARY
PostgreSQL 18 architecture family

POSTGRESQL CAPABILITIES
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer when concretely justified/activated

OFFLINE / SYNC TARGET
PowerSync
bounded encrypted SQLite local state
PostgreSQL remains canonical

BOUNDED CLASS-A ASYNC
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS-B TARGET
Restate when a real Class-B workflow requires it

OBJECT BYTES TARGET
Cloudflare R2 Standard / private

RECOVERY TARGET
pgBackRest
AWS S3 Standard eu-south-1
Versioning / Object Lock GOVERNANCE posture

SOLVER
OR-Tools CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy
Grafana Cloud EU
pg_stat_statements
```

Selection does not mean every capability is active in every environment. Activation remains trigger-based and governed by the current workstream responsible for that capability.

## 5. Canonical ownership

```text
PostgreSQL
= sole canonical DANTE persistence + material-history authority

PostGIS / FTS / pg_trgm / unaccent / pgvector
= PostgreSQL capabilities / derived retrieval machinery

SQLite / PowerSync
= bounded local/sync state, never canonical authority

Restate
= durable execution runtime when activated, not Domain history

R2
= raw object bytes

S3 / pgBackRest
= recovery copies / PITR infrastructure

OR-Tools
= candidate solver output

OpenTelemetry / Grafana
= operational telemetry
```

Canonical persistence authority count remains one: PostgreSQL.

## 6. Accepted PostgreSQL mapping thesis

```text
owner-specific canonical tables/families
+
owner-specific material-state/history tables/families
+
specific typed relation tables/families
+
bounded technical address/control structures only where required
+
separate provider / projection / runtime / technical concerns
```

A mechanism is not promoted into a semantic supertype merely because it is shared technically.

## 7. Reference and material-state mapping

```text
homogeneous NativeRef
→ direct concrete FK

genuinely heterogeneous NativeRef
→ bounded native-address control

ScopedRecordRef / MaterialStateRef
→ bounded address/control topology
→ owner-specific relational persistence
```

Material state preserves:

```text
stable semantic owner
+
explicit material-state address
+
owner-specific state payload
+
current accepted-state binding where required
+
history / lineage / correction semantics
```

`MaterialStateRef` is not `xmin/xid`, timestamp, row hash, ETag or provider revision.

## 8. Transaction / evolution posture carried downstream

The accepted Physical direction is compatible with the later PostgreSQL Constitution:

```text
short authoritative transactions
READ COMMITTED baseline
application operation owns commit/rollback
constraints are final race arbiters
no network wait inside authoritative DB write transaction
operation-specific idempotency/reconciliation
forward Alembic evolution
applied migrations immutable
owner / migrator / runtime privilege separation
```

Exact current implementation details are owned by ADR-010, the Database System of Record and executable code rather than duplicated here.

## 9. Current implementation relationship

The Physical target has already been consumed by later completed backend/database work. In particular, old README statements such as:

```text
CP6-03 ACTIVE
Gate 03 not earned
DANTE business database not materialized
first product capability not started
```

are historical phase-progress statements only and are not current repository status.

Current status is intentionally not restated here because it evolves independently from the closed Physical selection. Follow `../PROJECT-STATUS.md` and `../database/README.md` instead.

## 10. Reopen boundary

Do not reopen the Physical model merely because:

```text
a PostgreSQL 18 maintenance patch changes
a new feature needs another ordinary relational table
a provider integration is added
a selected dormant capability is activated
a later workstream needs operational tuning
```

Reopen only for material evidence that changes the accepted Physical architecture itself — for example a canonical-database change, a contradiction in the accepted persistence thesis, or a requirement that cannot be represented without violating the closed semantic/physical barriers.

Repository/executable current truth and accepted narrower downstream authorities beat obsolete phase-progress prose.
