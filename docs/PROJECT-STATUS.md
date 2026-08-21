# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**
- Branch-local current work: `feature/backend-scaffold`
- Protected-main truth reconciled from: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- Active backend integration PR: `#24`

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED
Whole-Domain PASS WITH HARDENING
POST-WRITE QA PASS

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WL-H01..WL-H12 ACTIVE

PRE-PHYSICAL COHERENCE
DEFINITIVE CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED / FINAL REVIEW PASS

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / FINAL REVIEW PASS
INTEGRATED VIA PR #22

FRONTEND MATERIALIZATION
ACTIVE ON feature/frontend-materialization
DIRECT FRONTEND VALIDATION NOT YET EARNED

PRODUCTION BACKEND SCAFFOLD
CLOSED ON feature/backend-scaffold / DIRECT QA PASS
CP1 CLOSED / DIRECT QA PASS
CP2 CLOSED / DIRECT QA PASS
CP3 CLOSED / DIRECT QA PASS
CP4 CLOSED / DIRECT REMOTE QA PASS
CP5 CLOSED / DIRECT INTEGRATED QA PASS
PR #24 OPEN / MERGE NOT YET AUTHORIZED

PROTECTED-MAIN CI ENFORCEMENT
Backend CI Gate REQUIRED
Dependency Review REQUIRED
branch up-to-date REQUIRED
source GitHub Actions

CONCRETE LOGICAL → POSTGRESQL IMPLEMENTATION
NOT STARTED / NEXT AFTER VERIFIED SCAFFOLD INTEGRATION

DIRECT HG-01..HG-12
NOT RUN / PASS 0
```

Architecture/design closure does not imply implementation PASS. Branch-local implementation evidence outranks older `main` status text only for this still-unmerged backend workstream.

## 2. Product and semantic invariants

DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

Compass: **Understand life. Shape what comes next.**

Persistent invariants include:

- life central, not task/calendar centric;
- planned vs actual preserved;
- user authority and authorship;
- historical/material truth;
- privacy and provenance;
- honest uncertainty;
- progressive complexity;
- personal-first, not personal-only;
- AI is not product authority;
- possibility != action/decision/preference;
- Effort != Execution != Outcome != Goal Progress;
- Person != Account != Principal != Actor;
- provider state != canonical DANTE state;
- derived projection != canonical truth;
- absence/unknown != false;
- idempotency != semantic identity;
- client local state != canonical accepted effect.

WL-H01..WL-H12 remain active and constrain implementation.

## 3. Logical / Physical authority

The Logical Model remains closed. 57/57 owners are classified and implementation must not mechanically translate owners into one-table/one-service assumptions.

Canonical persistence remains:

```text
PostgreSQL 18.4
sole canonical persistence + material-history authority
```

Selected PostgreSQL capabilities:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native full-text search;
- `pg_trgm`;
- `unaccent`;
- `pg_stat_statements`;
- PgBouncer 1.25.2 selected, activation bounded.

Other selected targets remain bounded and noncanonical where applicable: PowerSync + encrypted SQLite, PostgreSQL transactional outbox, Restate, R2, pgBackRest + AWS S3 `eu-south-1`, OR-Tools CP-SAT and OpenTelemetry/Grafana.

No specialist target is implicitly active merely because it is selected.

## 4. Engineering Foundation and repository

Repository identity governance is complete:

```text
historical repository   MattiaRubino/lifeos
current repository      MattiaRubino/dante
```

Accepted monorepo ownership includes:

```text
apps/backend
apps/web
apps/mobile
packages
infra
tooling
tests/system
docs
prototypes
.github
```

Paths are created only for real content.

Backend architecture remains a capability-first modular monolith with Domain/application/adapters separated, explicit transaction ownership and no universal generic Repository/BaseService/service locator/global DB session.

## 5. Frontend Engineering Foundation

The Frontend Engineering Foundation is integrated into protected `main` via PR #22 and remains closed in design/architecture.

Accepted baseline includes Node 24 LTS, TypeScript 6.0.x strict, pnpm 11, Turborepo 2.x, React 19.2/Vite 8/TanStack Router, React Native 0.86/Expo SDK 57/Expo Router, PowerSync + encrypted SQLite, TanStack Query/Form, Zod 4 and Orval 8.

The separate `feature/frontend-materialization` workstream is active. Its existence is not direct frontend validation PASS.

## 6. Backend CP1 — CLOSED / DIRECT QA PASS

Implementation/closure HEAD:

```text
02d113d772cdb247faebb3cef4d857d125266da3
```

Direct evidence:

```text
Python 3.14.7 project interpreter      PASS
uv locked bootstrap                    PASS
Ruff format/lint                       PASS
mypy strict                            PASS
pytest                                 25/25 PASS
uv build                               PASS
real Uvicorn factory startup           PASS
/health/live                           200 PASS
/health/ready                          200 PASS
```

## 7. Backend CP2 — CLOSED / DIRECT QA PASS

Direct LOCAL PostgreSQL evidence:

```text
PostgreSQL                             18.4 PASS
PostGIS                                3.6.4 PASS
pgvector                               0.8.6 PASS
pg_trgm                                PASS
unaccent                               PASS
pg_stat_statements preload/query       PASS
fresh init                             PASS
named-volume persistence               PASS
destructive reset                      PASS
Windows DBeaver host connection        PASS
```

Accepted image: `dante-postgres-local:18.4`.

## 8. Backend CP3 — CLOSED / DIRECT QA PASS

Implementation/direct-QA HEAD:

```text
35cf6440bc121a38342f6bbee72e210435a788a4
```

Materialized boundaries include SQLAlchemy async runtime, psycopg 3, Alembic technical baseline, typed database settings, FastAPI DB lifespan/readiness, `dante` schema metadata authority, owner/migrator/runtime provisioning and the real PostgreSQL acceptance harness.

Direct closure:

```text
uv lock --check                         PASS
uv sync --locked                        PASS
Ruff                                    PASS
mypy                                    PASS
fast pytest                             32/32 PASS
PostgreSQL pytest                       18/18 PASS
full pytest                             50/50 PASS
full-run coverage                       97.42% evidence only
uv build / sdist / wheel                PASS
Alembic acceptance                      PASS
privilege matrix                        PASS
stale-connection recovery               PASS
DB outage recovery                      PASS
transaction semantics                   PASS
```

The frozen/blackholed-peer readiness behavior remains an explicit hardening finding, not a claimed CP3 PASS.

## 9. Backend CP4 — CLOSED / DIRECT REMOTE QA PASS

Detailed authority:

`docs/development/backend-cp4-ci-contract.md`

### M1–M4

```text
uv authority                      0.12.5
Python authority                  3.14.7
workflow/config materialization   PASS
local fast suite                  32/32 PASS
local PostgreSQL suite            18/18 PASS
protected-main reconciliation     PASS
post-merge regression             PASS
main behind_by                    0 after reconciliation
```

### M5 — real PR green

PR #24 green-calibration HEAD:

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

Remote logs proved uv 0.12.5, Python 3.14.7, checksum-backed uv setup, locked dependency bootstrap, Ruff, mypy, 32/32 fast tests, package build, canonical PostgreSQL image build and 18/18 PostgreSQL acceptance.

Dependency Review directly enumerated the real `apps/backend/uv.lock` delta.

### M6 — deliberate red

HEAD:

```text
739680d11fe5c33a4974f069c2fdcce9e71a4fe0
```

Observed:

```text
Backend Quality       FAILURE — intentional calibration step
Backend PostgreSQL    SUCCESS
Backend CI Gate       FAILURE
Dependency Review     FAILURE — intentional deny-packages policy
```

Gate log observed `QUALITY_RESULT=failure`, `POSTGRES_RESULT=success` and exited red. Dependency Review rejected `fastapi@0.141.1` through `pkg:pypi/fastapi`. No vulnerable package was added.

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

### M8 — protected-main promotion

Existing ruleset `lifeos-main-safety` requires:

```text
Backend CI Gate
Dependency Review
```

Both were selected in the GitHub UI with source **GitHub Actions**. Branch up-to-date, PR-before-merge, zero approvals for the current single-maintainer state, review-thread resolution, deletion protection and force-push protection remain active.

Repository owner enabled the Actions setting requiring full-length commit SHA pins. The connected GitHub integration cannot directly read that setting; it is recorded as owner-applied / connector-unverifiable.

The canonical ruleset definition is `docs/development/github-main-ruleset.json`.

### CP4 closure decision

```text
CP4
CLOSED / DIRECT REMOTE QA PASS
```

## 10. Backend CP5 — CLOSED / DIRECT INTEGRATED QA PASS

CP5 PRE-SCOPE:

```text
35eca3a6b1fc9bbc691672e29ac975e640a49bf4
```

Before QA, the remote branch was identical to that PRE-SCOPE, current `main` was an ancestor with `behind_by = 0`, PR #24 was open/unmerged/mergeable, no review threads were present and both CP4 workflows on PRE-SCOPE were green.

Canonical WSL2/Linux workstation evidence:

```text
branch synchronized to PRE-SCOPE             PASS
uv 0.12.5                                    PASS
Python 3.14.7                                 PASS
uv lock --check                              PASS
uv sync --locked                             PASS
uv tree --locked                             PASS
Ruff format --check                          PASS
Ruff lint                                    PASS
mypy strict                                  PASS
fast pytest                                  32/32 PASS
uv build wheel + sdist                       PASS
canonical PostgreSQL image rebuild           PASS
PostgreSQL acceptance                        18/18 PASS
full backend pytest                          50/50 PASS
full-run coverage                            97.42% evidence only
LOCAL Compose PostgreSQL                     HEALTHY
explicit owner/migrator/runtime provisioning PASS
real Uvicorn factory startup                 PASS
GET /health/live                             200 {"status":"ok"}
GET /health/ready                            200 {"status":"ready"}
```

The local `.env.local` initially predated CP3 database variables; it was brought up to the repository-controlled `.env.example` contract using workstation-local ignored credentials. No secret was committed and no repository source change was required.

One full-suite invocation immediately after a dedicated PostgreSQL run hit Docker Desktop/WSL forwarding state rather than test logic:

```text
docker run exit 125
/forwards/expose returned unexpected status: 500
container state: Created
requested loopback port: no Linux listener
```

The diagnostic container was removed. A clean subsequent `uv run --locked pytest` completed **50/50 PASS**, so the event is classified as a transient Docker Desktop/WSL port-forwarding failure rather than an application, PostgreSQL or test-harness regression.

CP5 added no business schema, backend source, tests, dependency, migration or CI changes.

Closure decision:

```text
CP5
CLOSED / DIRECT INTEGRATED QA PASS

PRODUCTION BACKEND SCAFFOLD
CLOSED ON FEATURE BRANCH / PENDING PROTECTED-MAIN INTEGRATION
```

## 11. Current direct-validation non-claims

Do not extrapolate scaffold evidence into blanket Physical or production validation:

```text
CODEQL POST-MAIN ACTIVATION            NOT RUN
DIRECT HG-01..HG-12                    NOT RUN
DIRECT HG PASS                         0
RESTORE/PITR REHEARSAL                 NOT RUN
POWERSYNC DIRECT TEST                  NOT RUN
RESTATE DIRECT TEST                    NOT RUN
OBJECT RECOVERY TEST                   NOT RUN
SOLVER DIRECT TEST                     NOT RUN
PRODUCTION DEPLOYMENT                  NOT STARTED
FRONTEND DIRECT MATERIALIZATION PASS   NOT YET EARNED
CONCRETE BUSINESS DB SCHEMA            NOT STARTED
```

## 12. Active branches / workstreams

```text
feature/backend-scaffold
→ CP1–CP5 CLOSED / DIRECT QA PASS
→ PR #24 active; merge not authorized yet
→ next action: separate explicit merge gate

feature/frontend-materialization
→ frontend production materialization
→ separate worktree/workstream
```

The workstreams may proceed in parallel. Shared global documentation must be reconciled semantically at integration time; one workstream must not overwrite newer protected-main truth from the other.

## 13. Exact next backend action

```text
1. Treat CP1–CP5 as closed accepted backend scaffold checkpoints.
2. Do not add more implementation to CP5.
3. Open a fresh exact merge gate for PR #24.
4. Revalidate branch HEAD, current main, required checks, up-to-date state, review threads and exact PR delta on the actual merge candidate.
5. Merge only with explicit authorization and the accepted merge-commit method.
6. Perform post-merge readback and push-to-main CI verification before declaring scaffold integration complete.
7. Keep CodeQL a separate post-main boundary.
8. Start concrete Logical → PostgreSQL mapping only after verified scaffold integration.
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Frontend Foundation/CP1/CP2/CP3/CP4/CP5 decisions without concrete contradictory evidence.