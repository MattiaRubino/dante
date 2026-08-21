# Workstream — Production Backend Scaffold

- Status: **ACTIVE / CP1 CLOSED / CP2 CLOSED / CP3 CLOSED / CP4 CLOSED / DIRECT QA PASS / CP5 NEXT**
- Branch: `feature/backend-scaffold`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Engineering Foundation v0: **CLOSED / CONSUMED / NOT REOPENED**
- Concrete Logical → PostgreSQL schema: **OUT OF SCOPE UNTIL CP5 CLOSURE**
- CP1 authority: `docs/development/backend-cp1-contract.md`
- CP2 authority: `docs/development/backend-cp2-postgres-contract.md`
- CP3 authority: `docs/development/backend-cp3-persistence-contract.md`
- CP4 authority: `docs/development/backend-cp4-ci-contract.md`

## 1. Purpose

This workstream turns the closed Engineering Foundation into the first production backend scaffold, one directly verifiable checkpoint at a time.

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
        NEXT
          ↓
CONCRETE LOGICAL → POSTGRESQL
        NEXT WORKSTREAM BOUNDARY
```

The scaffold remains infrastructure/application bootstrap. CP1–CP4 do not authorize concrete business tables, repositories, use cases or product API slices.

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

## 3. Durable checkpoint evidence

### CP1 — CLOSED / DIRECT QA PASS

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

### CP2 — CLOSED / DIRECT QA PASS

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

### CP3 — CLOSED / DIRECT QA PASS

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

## 4. CP4 — CLOSED / DIRECT REMOTE QA PASS

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

Two-parent merge:

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

Runs:

```text
Backend CI          32478656632
Dependency Review   32478656892
```

Gate log proved:

```text
QUALITY_RESULT=failure
POSTGRES_RESULT=success
```

and exited red. Dependency Review rejected `fastapi@0.141.1` through the supported `pkg:pypi/fastapi` deny rule. No vulnerable dependency was added.

### M7 — recovery green

Temporary calibration edits were restored byte-for-byte to the M5 workflow blobs:

```text
backend-ci.yml
20056674477dd0fc2778d7f4d217a7158f0cd2c0

dependency-review.yml
c311f1e0df157b518a7b9883eeaa1a3f96833874
```

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

Both are selected from source **GitHub Actions**.

Also enabled:

```text
Require branches to be up to date before merging
```

Not enabled:

```text
Do not require status checks on creation
```

Preserved:

```text
PR required
0 approvals while one regular maintainer exists
review-thread resolution required
merge commits allowed/required method
main deletion blocked
force pushes/non-fast-forward blocked
no bypass
no merge queue
```

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

## 5. What CP4 does not authorize

CP4 closure does not authorize:

```text
frontend CI
CodeQL activation
production deployment
cloud identity/IaC
business/domain schema
business repositories/use cases/API
PowerSync activation
Restate activation
R2 activation
OR-Tools activation
pgBackRest recovery activation
Physical HG/PSV blanket PASS
```

## 6. CP5 — full scaffold QA / closure — NEXT

CP5 is the final scaffold boundary before concrete Logical → PostgreSQL implementation.

At minimum CP5 must verify the integrated scaffold truth still holds, including:

```text
exact branch/current-main relation
clean locked backend dependency bootstrap
Python 3.14.7
backend process startup
health/live + readiness behavior
Ruff/mypy/pytest
canonical PostgreSQL image
PostgreSQL 18.4 + extension envelope
SQLAlchemy/psycopg async connection
Alembic base → head
real PostgreSQL acceptance harness
CP4 required CI contexts still emitted and green
repository ruleset current truth
```

CP5 must not become a disguised business-schema implementation phase.

## 7. Persistent non-goals until scaffold closure

Do not add by convenience:

- concrete 57-owner table mapping;
- business capability modules merely to reserve names;
- business API routes;
- AuthN/AuthZ product implementation;
- cloud/IaC provider resources;
- production deployment pipeline;
- PowerSync/Restate/R2/OR-Tools activation without a real capability trigger;
- Kafka/Redis/event-sourcing infrastructure not justified by measured need.

## 8. Exact resume point

A new conversation must resume here:

```text
1. Read current main/current branch truth, this handoff and CP4 contract.
2. Treat CP1, CP2, CP3 and CP4 as CLOSED / DIRECT QA PASS.
3. Treat PR #24 as the active backend integration PR; do not merge it without an explicit merge gate.
4. Treat Backend CI Gate and Dependency Review as protected-main required checks.
5. Treat full-SHA repository enforcement as owner-applied but connector-readback-limited.
6. Start CP5 with a fresh exact gate.
7. CP5 is full scaffold QA/closure only.
8. Concrete Logical → PostgreSQL mapping remains deferred until CP5 closes.
9. Frontend materialization continues independently on its separate worktree/branch and shared docs must be semantically reconciled at integration time.
```

### Immediate next action

**CP5 is NEXT. Do not merge PR #24, activate CodeQL or start concrete business-schema mapping without a fresh exact gate.**
