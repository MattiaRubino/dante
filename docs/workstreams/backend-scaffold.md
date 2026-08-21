# Workstream — Production Backend Scaffold

- Status: **CLOSED / CP1 CLOSED / CP2 CLOSED / CP3 CLOSED / CP4 CLOSED / CP5 CLOSED / DIRECT QA PASS / PENDING MAIN INTEGRATION**
- Branch: `feature/backend-scaffold`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Engineering Foundation v0: **CLOSED / CONSUMED / NOT REOPENED**
- Concrete Logical → PostgreSQL schema: **NEXT ONLY AFTER VERIFIED SCAFFOLD INTEGRATION**
- Active integration PR: `#24` — **OPEN / UNMERGED**
- CP1 authority: `docs/development/backend-cp1-contract.md`
- CP2 authority: `docs/development/backend-cp2-postgres-contract.md`
- CP3 authority: `docs/development/backend-cp3-persistence-contract.md`
- CP4 authority: `docs/development/backend-cp4-ci-contract.md`

## 1. Purpose and final state

This workstream turned the closed Engineering Foundation into the first production backend scaffold, one directly verifiable checkpoint at a time.

```text
ENGINEERING FOUNDATION v0
        CLOSED
          ↓
CP1 Python/backend process + typed config
        CLOSED / DIRECT QA PASS
          ↓
CP2 reproducible LOCAL PostgreSQL
        CLOSED / DIRECT QA PASS
          ↓
CP3 persistence + migrations + real PostgreSQL harness
        CLOSED / DIRECT QA PASS
          ↓
CP4 quality / CI enforcement
        CLOSED / DIRECT REMOTE QA PASS
          ↓
CP5 full scaffold QA / closure
        CLOSED / DIRECT INTEGRATED QA PASS
          ↓
PROTECTED-MAIN INTEGRATION OF PR #24
        NEXT / EXPLICIT MERGE GATE REQUIRED
          ↓
CONCRETE LOGICAL → POSTGRESQL
        NEXT IMPLEMENTATION BOUNDARY AFTER VERIFIED MERGE
```

The scaffold is infrastructure/application bootstrap. CP1–CP5 do not authorize concrete business tables, repositories, use cases or product API slices.

## 2. Quality bar

DANTE targets production-grade engineering without unnecessary complexity.

Required qualities:

- reproducible Linux/WSL bootstrap;
- exact reviewed runtime/toolchain state;
- strong typing and deterministic validation;
- migration-first schema evolution;
- real PostgreSQL semantics where PostgreSQL behavior matters;
- explicit transaction/session ownership;
- secure configuration and least-privilege runtime identities;
- CI checks that are directly proven before becoming mandatory;
- no fake reviewers, placeholder architecture, arbitrary coverage gates or unused infrastructure.

## 3. CP1 — CLOSED / DIRECT QA PASS

Implementation/closure HEAD:

```text
02d113d772cdb247faebb3cef4d857d125266da3
```

Direct evidence:

```text
Python 3.14.7
uv locked bootstrap
FastAPI application factory
immutable typed settings
Ruff PASS
mypy strict PASS
pytest 25/25 PASS
uv build PASS
real Uvicorn startup PASS
/health/live 200
/health/ready 200
```

CP1 statement/branch coverage 100% is historical evidence for that small surface only, not a permanent project threshold.

## 4. CP2 — CLOSED / DIRECT QA PASS

Materialized LOCAL infrastructure:

```text
infra/local/postgres/Dockerfile
infra/local/postgres/initdb/010-extensions.sql
infra/compose/local.yaml
infra/compose/README.md
```

Accepted envelope:

```text
PostgreSQL 18.4
PostGIS 3.6.4
pgvector 0.8.6
pg_trgm
unaccent
pg_stat_statements
native PostgreSQL FTS
```

Direct evidence includes exact-image build, clean/fresh init, capability probes, `pg_stat_statements` collection, named-volume persistence/reset and Windows DBeaver connectivity.

## 5. CP3 — CLOSED / DIRECT QA PASS

Implementation/direct-QA HEAD:

```text
35cf6440bc121a38342f6bbee72e210435a788a4
```

Accepted runtime architecture:

```text
Settings / DatabaseSettings
        ↓
one AsyncEngine per process
        ↓
one async_sessionmaker per process
        ↓
one AsyncSession per application operation/task
        ↓
explicit transaction boundary
        ↓
PostgreSQL 18.4
```

Key frozen rules:

- SQLAlchemy 2 async + psycopg 3;
- `pool_pre_ping=True`;
- `autobegin=False`, `expire_on_commit=False`, `autoflush=True`;
- outer application operation owns commit/rollback;
- adapters may flush but do not commit;
- no generic Repository/UoW abstraction;
- Alembic owns deployed schema evolution;
- application schema `dante`;
- version table `dante.alembic_version`;
- technical baseline `20260820_01`;
- `dante_owner` NOLOGIN owner;
- `dante_migrator` LOGIN/NOINHERIT with bounded owner role escalation;
- `dante_runtime` LOGIN/NOINHERIT with DML-only posture.

Direct closure:

```text
fast pytest             32/32 PASS
PostgreSQL pytest       18/18 PASS
full pytest             50/50 PASS
full-run coverage       97.42% evidence only
uv build                PASS
Alembic acceptance      PASS
privilege matrix        PASS
transaction semantics   PASS
outage/recovery          PASS
```

The frozen/blackholed-peer readiness scenario remains a separate hardening finding and was not falsely claimed solved.

## 6. CP4 — CLOSED / DIRECT REMOTE QA PASS

CP4 materialized:

```text
apps/backend/pyproject.toml
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
```

Exact toolchain authority:

```text
uv                  0.12.5
Python              3.14.7
runner              ubuntu-24.04
```

Immutable Action pins and uv checksum are recorded in `backend-cp4-ci-contract.md`.

### M1–M4

```text
M1 tool/action/checksum freeze                  COMPLETE
M2 workflow/config materialization              COMPLETE
M3 local locked QA                              PASS
M4 protected-main reconciliation                PASS
M4 post-merge full backend regression           PASS
```

M4 consumed protected `main`:

```text
ff46eb16b971b1fde96eef9047b09faa02e1a5db
```

Two-parent reconciliation:

```text
6a8122249f13f9b8553f511c47b4185c6e3e6540
```

Tested reconciled HEAD:

```text
ba0d994e983cf3e5add6ad640c238999f418e236
```

After reconciliation `main` was an ancestor of the backend branch and `behind_by = 0`.

### M5 — real PR green

Calibration PR:

```text
#24
feature/backend-scaffold → main
```

M5 HEAD:

```text
bf9d364c59f02857125e228c6b223c13650ab78f
```

Runs:

```text
Backend CI          32477974221   SUCCESS
Dependency Review   32477974220   SUCCESS
```

Observed:

```text
Backend Quality       SUCCESS
Backend PostgreSQL    SUCCESS
Backend CI Gate       SUCCESS
Dependency Review     SUCCESS
```

Remote logs directly proved uv 0.12.5, Python 3.14.7, checksum-backed uv install, locked sync, Ruff, mypy, 32/32 fast tests, package build, canonical PostgreSQL image build and 18/18 PostgreSQL acceptance.

Dependency Review directly enumerated the real `apps/backend/uv.lock` delta.

### M6 — deliberate red

M6 HEAD:

```text
739680d11fe5c33a4974f069c2fdcce9e71a4fe0
```

Expected and observed:

```text
Backend Quality       FAILURE — explicit temporary calibration step
Backend PostgreSQL    SUCCESS
Backend CI Gate       FAILURE
Dependency Review     FAILURE — intentional deny-packages policy
```

Gate log proved `QUALITY_RESULT=failure`, `POSTGRES_RESULT=success` and exited red. Dependency Review rejected `fastapi@0.141.1` through the supported `pkg:pypi/fastapi` deny rule. No vulnerable dependency was added.

### M7 — recovery green

Recovery HEAD:

```text
df0a7c4fd3c7fe844fe56052fe7999732f186ee5
```

Runs:

```text
Backend CI          32478852443   SUCCESS
Dependency Review   32478852454   SUCCESS
```

All four intended checks/jobs returned green.

### M8 — required-check promotion

Existing ruleset:

```text
lifeos-main-safety
```

Required checks promoted only after green → deliberate red → recovery green:

```text
Backend CI Gate
Dependency Review
```

Both are selected from source **GitHub Actions**. The ruleset also requires the PR branch to be up to date before merging. PR required, zero approvals for the single-maintainer state, review-thread resolution, deletion protection and force-push protection remain preserved.

Repository owner also enabled the GitHub Actions setting requiring full-length Action SHAs. The connector cannot directly read this setting; the limitation is explicitly documented rather than reported as API PASS.

Canonical ruleset definition:

```text
docs/development/github-main-ruleset.json
```

### CP4 final result

```text
CP4
CLOSED / DIRECT REMOTE QA PASS
```

Detailed acceptance evidence and non-claims live in `docs/development/backend-cp4-ci-contract.md`.

## 7. CP5 — CLOSED / DIRECT INTEGRATED QA PASS

CP5 was deliberately a full-scaffold acceptance/closure checkpoint, not an implementation phase.

Approved PRE-SCOPE:

```text
35eca3a6b1fc9bbc691672e29ac975e640a49bf4
```

Remote preflight proved:

```text
feature/backend-scaffold == PRE-SCOPE     PASS
main ancestor / behind_by=0               PASS
PR #24 open / unmerged / mergeable        PASS
review threads                             0
Backend CI on PRE-SCOPE                    SUCCESS
Dependency Review on PRE-SCOPE             SUCCESS
```

Canonical WSL2/Linux workstation acceptance proved:

```text
branch synchronization                     PASS
uv 0.12.5                                  PASS
Python 3.14.7                               PASS
uv lock --check                            PASS
uv sync --locked                           PASS
uv tree --locked --depth 1                 PASS
Ruff format --check                        PASS
Ruff lint                                  PASS
mypy strict                                PASS
fast pytest                                32/32 PASS
uv build                                   PASS
canonical dante-postgres-local:18.4 build  PASS
PostgreSQL pytest                          18/18 PASS
full pytest                                50/50 PASS
full-run coverage                          97.42% evidence only
LOCAL Compose PostgreSQL                   HEALTHY
explicit DB role/security provisioning     PASS
real Uvicorn factory startup               PASS
GET /health/live                           200 {"status":"ok"}
GET /health/ready                          200 {"status":"ready"}
```

The workstation `.env.local` initially existed but predated the CP3 database configuration. It was aligned to the repository-controlled `.env.example` using locally generated ignored runtime/migrator credentials and explicit idempotent provisioning. No credential was printed into project documentation or committed.

### Docker Desktop transient observed during CP5

Immediately after one successful dedicated PostgreSQL run, a subsequent full-suite invocation failed before PostgreSQL test execution because Docker Desktop/WSL could not expose a newly selected loopback port:

```text
docker run exit 125
ports are not available
/forwards/expose returned unexpected status: 500
container state: Created
Linux listener on requested port: none
```

The failed diagnostic container was removed. The next clean `uv run --locked pytest` passed all **50/50** tests in 16.13 seconds. Because the PostgreSQL suite had already passed 18/18 and the clean full suite then passed 50/50 without code changes, this is recorded as transient Docker Desktop/WSL forwarding behavior rather than an application, database or test-harness regression.

### CP5 scope integrity

CP5 made no changes to:

```text
backend source
tests
dependencies
uv.lock
migrations
PostgreSQL implementation
CI workflows
ruleset settings
frontend
business schema
Logical → PostgreSQL implementation
main
```

Closure decision:

```text
CP5
CLOSED / DIRECT INTEGRATED QA PASS

PRODUCTION BACKEND SCAFFOLD
CLOSED ON feature/backend-scaffold
PENDING PROTECTED-MAIN INTEGRATION VIA PR #24
```

## 8. Persistent non-goals after scaffold closure

Do not add by convenience:

- concrete 57-owner table mapping before the scaffold is verified on protected `main`;
- business capability modules merely to reserve names;
- business API routes without their real vertical slice;
- AuthN/AuthZ product implementation without its capability boundary;
- cloud/IaC provider resources without a real remote boundary;
- production deployment pipeline without release infrastructure requirements;
- PowerSync/Restate/R2/OR-Tools activation without a real capability trigger;
- Kafka/Redis/event-sourcing infrastructure not justified by measured need.

## 9. Exact resume point

A new conversation must resume here:

```text
1. Read current protected main, current feature/backend-scaffold, this handoff and CP4 contract.
2. Treat CP1, CP2, CP3, CP4 and CP5 as CLOSED / DIRECT QA PASS.
3. Treat the production backend scaffold as CLOSED ON FEATURE BRANCH, not yet integrated into main.
4. Treat PR #24 as the active backend integration PR; do not merge it without a fresh explicit merge gate.
5. Treat Backend CI Gate and Dependency Review as protected-main required checks.
6. Treat full-SHA repository enforcement as owner-applied but connector-readback-limited.
7. Revalidate exact branch/main relation and final required checks on the actual merge candidate.
8. If explicitly authorized, merge PR #24 using the accepted merge-commit method only.
9. After merge, verify protected-main readback and push-to-main CI before calling scaffold integration complete.
10. Keep CodeQL as a separate post-main boundary.
11. Start concrete Logical → PostgreSQL only after verified scaffold integration.
12. Frontend materialization continues independently on feature/frontend-materialization; shared docs must be reconciled semantically at integration time.
```

### Immediate next action

**Open a fresh exact merge gate for PR #24. Do not add more CP5 implementation, activate CodeQL, start concrete business-schema mapping or mutate protected `main` without the appropriate next gate.**
