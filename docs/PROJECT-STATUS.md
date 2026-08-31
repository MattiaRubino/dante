# DANTE — Project Status

- **Status:** CURRENT TRUTH
- **Last reconciled:** 2026-08-31
- **Protected `main`:** integrated source authority; read the live Git ref for the current SHA
- **Backend CP6 integration:** PR #42 MERGED
- **Current product boundary:** protected `main` remains integrated authority; Access/Auth, Home React and platform observability have active bounded unmerged workstreams; PostgreSQL recovery CP01–CP07 is locally closed on its integration-candidate branch

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

PRE-RECOVERY PROTECTED-MAIN BUSINESS DATABASE BASELINE
MATERIALIZED / MAPPED / DICTIONARY-RECONCILED / DIRECTLY TESTED
ALEMBIC 20260826_08
68 tables / 5 views / 14 routines / 75 triggers /
95 indexes / 68 FKs / 120 CHECKs

POST-CP6 RECOVERY EVOLUTION IN THIS TREE
ALEMBIC 20260830_09
69 tables / 5 views / 15 routines / 76 triggers /
97 indexes / 69 FKs / 123 CHECKs
CP01–CP07 LOCAL PASS / CLOSED
remote backup provider TBD / NOT ACTIVATED

ACCESS PRE-BACKEND FRONTEND
CLOSED / ACCEPTED / RELEASE-HARDENED
AF-01D PASS
AF-02A PASS
AF-02B PASS
AF-03A PASS

FULL ACCESS/AUTH PRODUCT VERTICAL
ACTIVE UNMERGED WORKSTREAM / NOT CLAIMED CLOSED HERE
feature/access-auth owns branch-local implementation truth

PARALLEL ACTIVE UNMERGED WORKSTREAMS
feature/home-react
feature/platform-observability
```

Architecture/design closure is not the same as runtime/product completion. Closing the Access frontend workstream establishes the accepted frontend baseline; it does not claim real Auth/session/provider behavior.

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
routines             14
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


### 2.1 Post-CP6 recovery evolution in this tree

The recovery workstream adds one forward database evolution and a fully rehearsed LOCAL recovery system without rewriting the integrated CP6 history:

```text
Alembic head                         20260830_09
topology                             69|5|15|76|97|69|123|0|0|0
material_state_retirement            materialized
suppression ledger                   versioned / fail-closed
CP01–CP07                            LOCAL PASS / CLOSED
whole operator rehearsal             PASS
database-local reopen                PASS
remote backup provider               TBD / NOT ACTIVATED
production/cloud recovery            NOT CLAIMED
```

This is the current contract of the recovery tree. Until integration, protected `main` retains its earlier integrated CP6 database baseline. After integration, live Git—not this phase-time sentence—determines the protected-main state.


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

## 4. Binding semantic invariants

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

Accepted persistence thesis remains owner-specific canonical/material-history families plus specific typed relations and bounded technical addressing/control structures. Universal Entity/Thing, universal generic edges, canonical EAV/property bags and JSONB required-semantic escape hatches remain forbidden shortcuts.

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

PRE-RECOVERY PROTECTED-MAIN DANTE DATABASE BASELINE
18.6 / Alembic 20260826_08

POST-CP6 RECOVERY EVOLUTION IN THIS TREE
18.6 / Alembic 20260830_09 / 69|5|15|76|97|69|123|0|0|0
```

Patch maintenance inside major line 18 does not reopen the accepted database architecture or rewrite historical direct evidence.

## 8. Access frontend baseline

The completed `feature/access-frontend` workstream materialized the approved pre-backend Web Access system and release-hardened it without inventing fake Auth success.

Accepted checkpoints:

```text
AF-01D  shell completion / professional polish      PASS
AF-02A  complete pre-backend frontend state graph   PASS
AF-02B  downstream surface hardening                PASS
AF-03A  release-hardening viewport matrix           PASS
```

Current durable authority:

- `frontend/access.md`
- current `apps/web` Access code/tests
- `archive/branches/2026-08-feature-access-frontend.md` for non-authoritative branch history

The accepted pre-backend frontend remains the baseline. A real `feature/access-auth` workstream is now active and unmerged, so this global status document does not freeze a list of still-missing Auth subfeatures; use that branch's durable docs/code/tests for exact progress. The vertical is not claimed closed until its own gates earn closure.

## 9. Current bounded unmerged workstreams

Protected `main` remains integrated authority. Current branch-local work observed at the 2026-08-31 reconciliation includes:

```text
feature/access-auth             active unmerged product vertical
feature/home-react              active unmerged frontend workstream
feature/platform-observability  active unmerged platform workstream
feature/postgres-recovery       LOCAL recovery closed / integration candidate
```

Do not infer one branch's implementation from another branch or from this global summary. Each bounded branch owns its own newer truth until integration.

A legitimate schema evolution continues to use a reviewed forward Alembic migration synchronized with mappings, Dictionary, human-readable database reference and tests. CP6 is not reopened.

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

pgBackRest LOCAL recovery
→ implemented / whole LOCAL operator rehearsal PASS on the recovery workstream

remote backup provider
→ TBD; production activation/proof deferred until deployment requires it
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
FULL-STACK ACCESS/AUTH CLOSURE                     NOT CLAIMED
NATIVE MOBILE ACCESS                             NOT CLAIMED COMPLETE
DIRECT BUSINESS HG-01..HG-12                     NOT BLANKET-PASSED
PRODUCTION/CLOUD RECOVERY                        NOT CLAIMED
REMOTE BACKUP PROVIDER                           TBD / NOT ACTIVATED
REAL V1→V2 BUSINESS-SCHEMA EVOLUTION             NOT RUN
POWERSYNC DIRECT PRODUCT TEST                    NOT RUN
RESTATE DIRECT PRODUCT TEST                      NOT RUN
PRODUCTION DEPLOYMENT                            NOT STARTED
```

The Access frontend branch's historical local/automated evidence must not be inflated: AF-03A full automation was proven before its final one-line width refinement; exact final delta plus visual review were accepted, while the final branch integration still requires hosted PR CI.

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

Frontend Access:

```text
docs/frontend/access.md
apps/web/src/features/access/
apps/web/e2e/access.spec.ts
```

Historical branch narratives under `docs/archive/branches/` are evidence/navigation only and never current authority.
