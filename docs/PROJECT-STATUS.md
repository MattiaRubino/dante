# DANTE — Project Status

- **Status:** CURRENT TRUTH
- **Last reconciled:** 2026-08-26
- **Protected `main`:** `117360b9333fd1a8a62d0dfeb0398a4d5811e393`
- **Backend CP6 integration:** PR #42 MERGED
- **Current active product implementation:** Access frontend on `feature/access-frontend` — UNMERGED

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED / SEMANTICALLY COMPLETE FOR CURRENT SCOPE

LOGICAL MODEL
CLOSED
57 / 57 CLASSIFIED
WL-H01..WL-H12 ACTIVE AS BINDING HARDENINGS

PRE-PHYSICAL COHERENCE
CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED
PostgreSQL 18 major family
sole canonical persistence / material-history authority
Physical phase-time exact patch 18.4 / HISTORICAL

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
CLOSED / PASS / INTEGRATED VIA PR #28

PRODUCTION BACKEND SCAFFOLD
CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24
CP1 CLOSED / DIRECT QA PASS
CP2 CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
CP3 CLOSED / DIRECT QA PASS — PostgreSQL 18.4 historical exact evidence
CP4 CLOSED / DIRECT REMOTE QA PASS
CP5 CLOSED / DIRECT INTEGRATED QA PASS

CP6 — CONCRETE POSTGRESQL DATABASE
CLOSED / CONCRETE POSTGRESQL DATABASE PASS
INTEGRATED IN PROTECTED main VIA PR #42
CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 CLOSED / GATE 03 PASS
CP6-04 CLOSED / MATERIALIZATION PASS
CP6-05 CLOSED / DIRECT QA PASS

CURRENT POSTGRESQL TECHNICAL PATCH
18.6

CURRENT DANTE BUSINESS DATABASE
MATERIALIZED / MAPPED / DICTIONARY-RECONCILED / DIRECTLY TESTED
ALEMBIC 20260826_08
68 tables / 5 views / 14 routines / 75 triggers /
95 indexes / 68 FKs / 120 CHECKs

ACCESS FRONTEND
ACTIVE / UNMERGED ON feature/access-frontend
AF-01D PASS
AF-02A PASS
AF-02B PASS
ACCESS VERTICAL NOT CLOSED
REAL BACKEND AUTH / FULL-STACK / RELEASE BOUNDARY STILL REQUIRED

FIRST POST-CP6 BACKEND PRODUCT VERTICAL
NOT STARTED ON A DEDICATED BACKEND BRANCH
```

Architecture/design closure is not the same as runtime/product completion. Historical PostgreSQL 18.4 evidence remains exact for the phases that executed on 18.4; current repository-owned PostgreSQL is 18.6.

## 2. Current protected-main backend/database truth

PR #42 integrated the completed CP6 branch into protected `main` through the required merge-commit path.

Final accepted CP6 implementation candidate:

```text
22bbc078391d52c43665474bf465593d6225106e
```

Final feature head before merge:

```text
9297b64c7c912c2cc8e344a6617beb5c91457bbb
```

Protected-main merge commit:

```text
117360b9333fd1a8a62d0dfeb0398a4d5811e393
```

Final database baseline:

```text
PostgreSQL          18.6
Alembic head        20260826_08

tables              68
views                5
routines            14
triggers             75
physical indexes    95
foreign keys         68
CHECK constraints   120

custom enum/domain    0
sequences             0
materialized views    0
RLS policies          0
```

Final direct acceptance included:

```text
Ruff format/check                    PASS
mypy strict                          PASS
non-PostgreSQL tests                 37 / 37 PASS
real PostgreSQL tests                76 / 76 PASS
build                                PASS
Dictionary JSON-Schema               PASS
Dictionary ↔ SQLAlchemy              PASS
Dictionary ↔ Alembic                 PASS
Dictionary ↔ live PostgreSQL         PASS
persistent LOCAL upgrade/restart     PASS
security / ACL posture               PASS
GET /health/live                     200
GET /health/ready                    200
```

Durable evidence:

- `development/backend-cp6-05-whole-database-qa.md`
- `database/README.md`
- `database/dictionary/`
- `archive/branches/2026-08-feature-logical-postgresql.md` — non-authoritative branch history

## 3. Persistence authority

Current persistence authority is layered rather than chosen ad hoc:

```text
Domain / Logical / Physical
→ semantic and architectural source

CP6-02 Constitution + ADR-010
→ durable PostgreSQL doctrine

Database System of Record
→ current human-readable database meaning + machine Dictionary

Alembic
→ deployed application-schema evolution authority

SQLAlchemy metadata / mappings
→ application representation of deployed database contract

real PostgreSQL introspection
→ observed materialized database

direct tests
→ executable proof
```

Permanent reconciliation invariant:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

A later structural DB change is incomplete if these representations are left inconsistent.

## 4. Logical / Physical invariants that remain binding

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Subject != Resource != native identity
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Agreement != Consent
Ownership != Possession
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
client local state != canonical accepted effect
```

Accepted persistence thesis:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific typed relation families
+ bounded technical address/control structures only where genuinely heterogeneous addressing requires them
+ separate provider/derived/runtime concerns
```

Forbidden shortcuts remain:

```text
universal Entity / Thing
universal Relationship / generic edge
canonical EAV/property bag
universal event ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
```

## 5. Reference / material-state baseline

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Current physical direction:

```text
homogeneous NativeRef
→ direct FK

genuinely heterogeneous NativeRef
→ bounded native-address anchor

MaterialStateRef
→ UUIDv7 stable address
→ bounded material-state address/control
→ exact owner + facet
→ owner-specific material-state row
→ explicit current accepted-state binding where required
```

No application-only `type + uuid` polymorphic integrity.

## 6. Backend technical foundation

Current backend baseline:

```text
Python                              3.14.x / initial exact pin 3.14.7
uv                                  repository package authority
schema                              dante
SQLAlchemy                          async 2.0 stable line
psycopg                             3
Alembic                             one environment / one DAG / one head
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per app operation
autobegin=False
autoflush=True
expire_on_commit=False
outer application operation owns transaction
adapter may flush / never implicit commit
READ COMMITTED default

dante_owner                         NOLOGIN ownership identity
dante_migrator                      LOGIN migration identity
dante_runtime                       LOGIN application runtime identity
```

No generic Repository/UoW/BaseService architecture is introduced merely for uniformity.

## 7. PostgreSQL version truth

```text
POSTGRESQL ARCHITECTURE
major 18

PHYSICAL PHASE-TIME EXACT PATCH
18.4 / historical

CP2 / CP3 ORIGINAL DIRECT EVIDENCE
18.4 / historical exact

CURRENT REPOSITORY PATCH
18.6

CURRENT MATERIALIZED DANTE DATABASE
18.6 / Alembic 20260826_08
```

Patch maintenance inside major line 18 does not reopen the accepted database architecture or rewrite historical direct evidence.

## 8. Current product implementation work

### Access frontend — active

Branch:

```text
feature/access-frontend
```

Branch-local durable workstream record:

```text
docs/workstreams/access-frontend.md
```

Current accepted frontend-owned/pre-backend checkpoints include:

```text
AF-01D  shell completion / professional polish     PASS
AF-02A  complete pre-backend frontend state graph  PASS
AF-02B  downstream surface hardening               PASS
```

Access itself is **not closed**. Backend-authoritative/full-stack work still includes, according to the final contract as applicable:

```text
real account creation and credential authentication
email verification proof validation
recovery proof validation and reset mutation
Google / Apple transaction validation
secure account linking
session establishment/bootstrap/expiry/revocation
reauthentication
server rate-limit/error mapping
stable Auth OpenAPI
generated typed client
real frontend/backend integration
full-stack isolated E2E
final authenticated Home handoff
release/legal/mobile gates where applicable
```

The Access frontend branch is unmerged and currently diverged from protected `main`; it must be reconciled with current `main` before protected-main integration. Its branch-local live handoff may exist while the branch is active, but temporary handoffs must be removed/consolidated before merge under the documentation lifecycle policy.

## 9. Current backend boundary

There is no active CP6 continuation. CP6 is complete.

The next backend implementation is a **post-CP6 product vertical**, created from current protected `main` under its own bounded branch when explicitly started.

The currently active Access frontend creates a concrete need for a real Auth/backend boundary, but a backend branch/implementation must not be invented merely by documenting it. Until such a branch exists, backend product-vertical implementation remains `NOT STARTED`.

A later vertical may expose a legitimate database evolution requirement. That becomes a normal reviewed forward migration synchronized with the Database System of Record; it does not reopen CP6.

## 10. Capability-triggered components

Selected components remain dormant until a real consuming requirement exists:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

PostgreSQL transactional outbox
→ real Class-A async requirement

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first real Class-B durable workflow

pgBackRest + AWS S3
→ recovery/production boundary or real recovery rehearsal
```

Selected architecture does not imply activated runtime capability.

## 11. Repository / documentation truth

Protected `main` is integrated authority. Unmerged branch truth remains bounded to its branch until merge.

Temporary live/session handoffs are branch-operational only and must not merge into `main`. Completed workstreams may retain at most one justified consolidated branch history record; Git/PR history remains the complete backup.

See:

- `development/documentation-lifecycle-policy.md`
- `archive/README.md`
- `development/repository-engineering-safety.md`
- `development/branching-and-environments.md`

## 12. Current direct-validation non-claims

Do not claim work that has not actually run or been implemented:

```text
FIRST POST-CP6 BACKEND PRODUCT VERTICAL       NOT STARTED
ACCESS REAL BACKEND/FULL-STACK CLOSURE        NOT COMPLETE
DIRECT BUSINESS HG-01..HG-12                  NOT BLANKET-PASSED
RESTORE/PITR REHEARSAL                        NOT RUN
REAL V1→V2 BUSINESS-SCHEMA EVOLUTION          NOT RUN
POWERSYNC DIRECT PRODUCT TEST                 NOT RUN
RESTATE DIRECT PRODUCT TEST                   NOT RUN
PRODUCTION DEPLOYMENT                         NOT STARTED
```

## 13. Current navigation

Start from:

```text
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
```

Backend/database:

```text
apps/backend/README.md
docs/database/README.md
docs/database/dictionary/README.md
docs/development/backend-cp6-05-whole-database-qa.md
```

Current active Access frontend work is branch-local on `feature/access-frontend`; its `docs/workstreams/access-frontend.md` is not yet protected-main authority.
