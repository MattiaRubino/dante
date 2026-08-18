# PM-14 — Physical Model Closure v1

- Status: **BRANCH CLOSURE COMPLETE / PROTECTED-MAIN INTEGRATION PENDING EXTERNAL GIT ACTION**
- Workstream: `feature/physical-model`
- Closure scope: Physical Model PM-00 through PM-14
- Domain: **CLOSED / UNCHANGED**
- Logical: **CLOSED / UNCHANGED / WL-H01..WL-H12 ACTIVE**
- Backend production implementation: **NOT STARTED**
- Development Profile v0: **NOT STARTED / SEPARATE NEXT OPERATIONAL SCOPE**

## 1. Closure result

The Physical Model workstream has completed its target-architecture decision sequence:

```text
PM-00  QA PASS
PM-01  PASS-CONDITIONAL
PM-02  COMPLETE
PM-03  STATIC COMPLETE / 0 REJECTS
PM-04A COMPLETE / 0 EXECUTION-WORTHY GAPS
PM-04B NOT ADMITTED
PM-05  COMPLETE
PM-06  EVIDENCE QUALIFICATION COMPLETE
PM-07  EVIDENCE QUALIFICATION COMPLETE
PM-08  SECONDARY/SPECIALIST QUALIFICATION COMPLETE
PM-09  EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE
PM-10  FINAL STACK RECOMMENDATION COMPLETE
PM-11  EXPLICIT USER-APPROVED TARGET STACK SELECTION COMPLETE
PM-12  ACCEPTED PHYSICAL MODEL COMPLETE
PM-13  CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS
PM-14  BRANCH CLOSURE COMPLETE
```

## 2. Accepted target architecture

```text
CANONICAL PRIMARY
PostgreSQL 18.4

POSTGRESQL CAPABILITIES
PostGIS 3.6.4
pgvector 0.8.6
native FTS
pg_trgm
unaccent
pg_stat_statements
PgBouncer 1.25.2

OFFLINE / SYNC
PowerSync Service 1.25.0 Open Edition
encrypted SQLite local state
PostgreSQL-backed PowerSync bucket storage

ASYNC CLASS A
PostgreSQL transactional outbox + bounded worker

DURABLE CLASS B
Restate runtime
Restate Python SDK 1.0.3
Restate Server 1.7.2 self-hosted/reproducible subject
Restate Cloud EU allowed managed deployment
GLOBAL RESTATE DEPLOYMENT DEFAULT NONE

OBJECT
Cloudflare R2 Standard / EU jurisdiction / private

RECOVERY
pgBackRest 2.59.0
AWS S3 Standard eu-south-1 recovery target
Versioning
Object Lock GOVERNANCE / finite policy-bound retention
separate DB and object backup repositories

SOLVER
OR-Tools 9.15 CP-SAT

OBSERVABILITY
OpenTelemetry
Grafana Alloy 1.18.0
Grafana Cloud EU
pg_stat_statements
```

## 3. Canonical-authority result

```text
CANONICAL PERSISTENCE AUTHORITIES
1

OWNER
PostgreSQL 18.4
```

All companion states remain bounded:

```text
SQLite / PowerSync   local/projection
Restate              runtime
R2                   raw object bytes
S3                   recovery copy
pgvector/search      derived retrieval
OR-Tools             candidate solver output
OTel/Grafana         operational telemetry
```

No companion is a second canonical semantic database.

## 4. Restate closure qualification

The final architecture selects **Restate runtime**, not `Restate Cloud EU` as a universal deployment default.

```text
SELF-HOSTED
FIRST-CLASS SELECTED DEPLOYMENT OPTION

CLOUD EU
ALLOWED MANAGED DEPLOYMENT OPTION

GLOBAL DEFAULT
NONE
```

Reason: Restate can be self-hosted as a self-contained binary/container; Cloud supports an EU region; current client-side journal encryption is documented only in the TypeScript SDK while LifeOS targets Python. Journal minimization and deployment privacy/operability review remain mandatory.

## 5. Direct-execution truth preserved at closure

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG-01..HG-12      NOT RUN
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE REHEARSAL         NOT RUN
MIGRATION REHEARSAL       NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC DIRECT TEST     NOT RUN
RESTATE DIRECT TEST       NOT RUN
OBJECT RECOVERY TEST      NOT RUN
SOLVER DIRECT TEST        NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

PM-14 closure does not relabel these values.

## 6. Mandatory implementation carry-forward

The selected target is accepted, but direct implementation/release obligations remain in:

```text
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

They include primary recovery/evolution/non-interference, search/vector/projection security/freshness/deletion, PowerSync offline/replication/local-encryption, Restate durable-runtime and deployment privacy, R2/S3 recovery, PostGIS/PgBouncer interactions, OR-Tools solver semantics and observability privacy.

A later failed applicable validation may reopen the affected Physical decision; it may not weaken accepted Domain/Logical semantics silently.

## 7. Technology exclusion closure

The accepted target does not depend on the PM-10 excluded set. Reintroduction of an excluded technology requires an explicit later architecture decision based on material new requirements/evidence.

## 8. Development Profile v0 boundary

The next operational design may define a separate `Development Profile v0` covering:

```text
which selected components are active immediately
self-hosted vs managed choices where Physical permits both
free-tier/local development choices
accounts/credentials/environment setup
initial backup and observability activation
upgrade/production triggers
```

This is **not** a reopen of the target Physical Model.

## 9. Protected-main integration contract

Normal integration must use the repository-protected path:

```text
feature/physical-model
→ pull request
→ main
```

Before merge:

- compare the closure branch against current `main`;
- verify no behind/divergence or resolve explicitly;
- verify the full approved closure delta;
- inspect PR changed files;
- verify required repository checks/rules that actually exist;
- resolve blocking review threads if any.

After merge:

- verify remote `main` contains the intended selected/accepted Physical records;
- verify merge commit/PR state remotely;
- verify no direct-main bypass occurred;
- treat GitHub PR/merge history as the authoritative integration evidence.

This evidence document intentionally does not embed a guessed future merge SHA.

## 10. Closure verdict

```text
PHYSICAL MODEL TARGET ARCHITECTURE
CLOSED

PM-13 CLEAN-ROOM QA
PASS

CANONICAL PRIMARY
PostgreSQL 18.4

TARGET COMPANION STACK
SELECTED / ACCEPTED

DIRECT IMPLEMENTATION
NOT STARTED

DEV-v0
SEPARATE NEXT OPERATIONAL SCOPE

PROTECTED-MAIN INTEGRATION
NEXT EXTERNAL GIT ACTION
```
