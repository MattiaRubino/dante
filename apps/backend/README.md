# DANTE Backend

Production backend application for DANTE.

CP1 established the Python/process/configuration foundation. CP2 established the reproducible LOCAL PostgreSQL 18.4 image/envelope and direct phase-time evidence. CP3 activated application persistence, Alembic authority, PostgreSQL role separation and the real PostgreSQL acceptance harness. CP4 established calibrated CI and protected-main enforcement. CP5 re-proved the integrated scaffold end to end on the canonical WSL2/Linux workstation. PR #24 merged the closed scaffold into protected `main`.

CP6 then consumed that foundation and is **CLOSED / CONCRETE POSTGRESQL DATABASE PASS / INTEGRATED VIA PR #42**. Its protected-main integration baseline was revision `20260826_08`.

The PostgreSQL Recovery workstream added forward revision `20260830_09`, retirement/anti-resurrection integrity and a complete LOCAL pgBackRest restore/PITR operator rehearsal. PR #47 integrated that accepted Recovery evolution into protected `main`.

Access/Auth M1–M5 and the shared Email Platform evolved forward from the same CP6 baseline through `20260904_16`. Protected-main Recovery and Access/Auth/Email histories were preserved and joined with no-DDL Alembic merge revision `20260904_17`; PR #52 then integrated the accepted combined foundation into protected `main` at `5f76ec54ad78542f137e8730e904f805d9e59e56`. Post-merge Backend and Frontend CI passed on that exact merge commit.

## Current status

```text
CP1   CLOSED / DIRECT QA PASS
CP2   CLOSED / DIRECT QA PASS — ORIGINAL POSTGRESQL 18.4 EVIDENCE
CP3   CLOSED / DIRECT QA PASS — ORIGINAL POSTGRESQL 18.4 EVIDENCE
CP4   CLOSED / DIRECT REMOTE QA PASS
CP5   CLOSED / DIRECT INTEGRATED QA PASS
PR #24 MERGED / POST-MERGE BACKEND CI PASS

CP6-00 COMPLETE
CP6-01 CLOSED / GATE 01 PASS
CP6-02 CLOSED / GATE 02 PASS
CP6-03 CLOSED / GATE 03 PASS
CP6-04 CLOSED / MATERIALIZATION PASS
CP6-05 CLOSED / DIRECT QA PASS
CP6 CLOSED / CONCRETE POSTGRESQL DATABASE PASS
PR #42 MERGED INTO PROTECTED main

POSTGRESQL 18.6
HISTORICAL PRE-RECOVERY ALEMBIC 20260826_08
HISTORICAL PRE-RECOVERY TOPOLOGY 68 / 5 / 14 / 75 / 95 / 68 / 120

HISTORICAL RECOVERY-ONLY MAIN BEFORE PR #52
Alembic                     20260830_09
Topology                    69 / 5 / 15 / 76 / 97 / 69 / 123
Recovery PR                 #47

CURRENT PROTECTED MAIN
Access integration merge    5f76ec54ad78542f137e8730e904f805d9e59e56
Alembic                     20260904_17
Topology                    88 / 5 / 16 / 76 / 172 / 89 / 270
Access/Auth M1–M5           CLOSED / INTEGRATED
Shared Email Platform       CLOSED / INTEGRATED / OWNERSHIP VERIFIED
Recovery                    CLOSED / INTEGRATED
CP07 LOCAL Recovery         PASS
post-merge Backend CI       PASS
post-merge Frontend CI      PASS
```

The CP07 proof on implementation HEAD `81639c61478b476c995652d0060dde8f53aef089` earned `DATABASE LOCAL REOPEN = PASS` against `20260904_17 / 88|5|16|76|172|89|270|0|0|0`, proved old protected-payload physical resurrection followed by suppression-ledger reconciliation, and rejected protected-payload reinsertion. Remote backup provider activation and production/cloud recovery remain **NOT CLAIMED**.

Protected-main integration milestones:

```text
CP6 final feature HEAD       9297b64c7c912c2cc8e344a6617beb5c91457bbb
CP6 PR                       #42
CP6 merge commit             117360b9333fd1a8a62d0dfeb0398a4d5811e393

Recovery final head          e46ae3d9d5918b27ebf86f4e291b51312f1e7c4d
Recovery PR                  #47
Recovery merge commit        bdd2b2370d41423dbaecd00fde86bb2bf2466f2b

Access implementation proof 81639c61478b476c995652d0060dde8f53aef089
Access final candidate       6cee5506d404d0684b0679aca54c03f0ca433c72
Access integration PR        #52
Access merge commit          5f76ec54ad78542f137e8730e904f805d9e59e56
```

Current backend transition boundary:

```text
CP6 CLOSED + INTEGRATED
        ↓
RECOVERY EVOLUTION 20260830_09 + LOCAL RECOVERY SYSTEM
CLOSED + INTEGRATED
        ↓
ACCESS/AUTH M1–M5 + SHARED EMAIL PLATFORM
CLOSED + INTEGRATED
        ↓
NO-DDL ALEMBIC CONVERGENCE 20260904_17
        ↓
COMBINED CI + REAL POSTGRESQL + CP07
PASS
        ↓
PR #52 + POST-MERGE MAIN CI
PASS / INTEGRATED
        ↓
OBSERVABILITY INTEGRATION
NEXT
```

There is no remaining CP6, Recovery or Access/Auth integration step. Final CP6 closure evidence lives in `docs/development/backend-cp6-05-whole-database-qa.md`; current Recovery operation lives in `docs/operations/postgres-recovery-runbook.md`; durable combined integration evidence lives in `docs/workstreams/access-auth-integration-acceptance-2026-09-04.md`; historical branch records remain non-authoritative for current state.

## Runtime contract

```text
Python supported line      3.14.x
initial exact pin          3.14.7
package manager            uv
import namespace           dante
project distribution       dante-backend
server semantics           Linux / WSL2
canonical DB architecture  PostgreSQL 18
current technical patch    PostgreSQL 18.6
Physical/CP2/CP3 evidence  PostgreSQL 18.4 historical exact evidence
```

The repository-controlled environment lives at `apps/backend/.venv` after `uv sync`. Do not share a single virtual environment between Windows and WSL.

## Dependency bootstrap

From `apps/backend`:

```bash
uv sync --locked
uv lock --check
uv tree --locked --depth 1
```

`pyproject.toml` records bounded compatibility policy; `uv.lock` records the exact resolved graph. Never hand-edit `uv.lock`.

Current persistence resolution is:

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

## Runtime configuration

`.env.example` is a safe runtime-only template. Copy it to `.env.local` and replace the LOCAL runtime password with the credential provisioned for `dante_runtime`.

The application does not discover `.env.local` automatically; inject it explicitly through `uv`.

Runtime database variables:

| Variable | Required | Default | Secret | Meaning |
|---|---:|---|---:|---|
| `DANTE_DATABASE__HOST` | yes | none | no | PostgreSQL host |
| `DANTE_DATABASE__PORT` | no | `5432` | no | PostgreSQL port |
| `DANTE_DATABASE__NAME` | yes | none | no | database name |
| `DANTE_DATABASE__USER` | yes | none | no | runtime login; LOCAL uses `dante_runtime` |
| `DANTE_DATABASE__PASSWORD` | yes | none | yes | runtime credential |
| `DANTE_DATABASE__CONNECT_TIMEOUT_SECONDS` | no | `5` | no | connect timeout |
| `DANTE_DATABASE__POOL_SIZE` | no | `5` | no | persistent pool size |
| `DANTE_DATABASE__MAX_OVERFLOW` | no | `10` | no | bounded pool overflow |
| `DANTE_DATABASE__POOL_TIMEOUT_SECONDS` | no | `30` | no | pool checkout timeout |
| `DANTE_DATABASE__READINESS_TIMEOUT_SECONDS` | no | `2` | no | readiness deadline |

Admin and migrator secrets do **not** belong in the normal backend runtime environment.

The complete CP3 database contract lives in:

`docs/development/backend-cp3-persistence-contract.md`

The closed CP6-02 database constitution lives in:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

Formal Gate 02 closure evidence lives in:

`docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`

The current Database System of Record lives in:

`docs/database/README.md`

Final CP6 direct closure evidence lives in:

`docs/development/backend-cp6-05-whole-database-qa.md`

Historical CP6 branch chronology lives in:

`docs/archive/branches/2026-08-feature-logical-postgresql.md`

Historical Recovery branch chronology lives in:

`docs/archive/branches/2026-08-feature-postgres-recovery.md`

No live/session CP6, Recovery or Access/Auth handoff is current authority after integration.

## LOCAL database security provisioning

The PostgreSQL container starts with the platform/bootstrap administrator `postgres`. CP3 adds the application security boundary through the explicit provisioning command:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Provisioning is intentionally separate from FastAPI startup and Alembic. Supply admin, migrator and runtime credentials only to the provisioning command/process.

Conceptual invocation from `apps/backend`:

```bash
DANTE_DATABASE__HOST=127.0.0.1 \
DANTE_DATABASE__PORT=5432 \
DANTE_DATABASE__NAME=dante \
DANTE_ADMIN__USER=postgres \
DANTE_ADMIN__PASSWORD='<local admin secret>' \
DANTE_MIGRATOR__PASSWORD='<local migrator secret>' \
DANTE_RUNTIME__PASSWORD='<local runtime secret>' \
uv run python -m dante.platform.database.provisioning
```

Do not commit these secrets or reuse LOCAL credentials in DEV/UAT/PROD.

## Alembic

Alembic owns deployment history for the DANTE application schema.

```text
schema               dante
version table        dante.alembic_version
migration login      dante_migrator
DDL owner role       dante_owner via explicit SET ROLE
```

Migration commands must receive the dedicated migrator password separately from runtime config. Normal application startup never runs migrations.

The migration history begins with the technical CP3 baseline `20260820_01`. CP6 materialized the concrete business database through the reviewed M1..M7 linear stages and the CP6-05 hardening revision `20260826_08`. Recovery then added sibling forward revision `20260830_09` for MaterialState retirement/anti-resurrection integrity. Access/Auth and Email evolved independently from `20260826_08` through `20260904_16`. Protected `main` preserves both histories and joins them with forward no-DDL merge revision `20260904_17`.

```text
20260826_08
├── 20260830_09 Recovery
└── 20260827_09 → ... → 20260904_16 Access/Auth + Email

20260830_09 + 20260904_16 → 20260904_17
```

Applied migration history is immutable; later corrections use new forward revisions. PostgreSQL server patch maintenance such as 18.4 → 18.6 is platform/image maintenance and does not rewrite Alembic business/schema history.

A later product vertical that genuinely needs a schema change must evolve the database through normal reviewed forward migration and keep SQLAlchemy, Dictionary, human-readable reference and direct tests aligned in the same change.

## Run locally

After PostgreSQL roles/schema are provisioned and `.env.local` contains the matching runtime credential:

```bash
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Technical probes:

```text
GET /health/live   process liveness only
GET /health/ready  bounded real PostgreSQL readiness
```

Expected dependency behavior:

```text
PostgreSQL available     live 200   ready 200
PostgreSQL unavailable   live 200   ready 503
PostgreSQL recovers      same process can return ready 200
```

Probe responses deliberately expose no credentials, DSN, database host/name, SQL or stack details. Neither endpoint appears in the product OpenAPI surface.

## Session and transaction rules

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation/task
session never global/shared across concurrent tasks
autobegin=False
expire_on_commit=False
autoflush=True
```

The outer application-operation boundary owns commit/rollback. Persistence adapters never commit implicitly. There is no generic `Repository[T]` or generic Unit of Work in the closed scaffold.

Provider/network I/O remains forbidden inside authoritative PostgreSQL transactions. For Email delivery, canonical feature mutation + durable EmailIntent may share one transaction; provider I/O occurs only after commit and ambiguity is never blindly retried.

## API documentation behavior

```text
LOCAL / DEV / UAT   /docs ON    /openapi.json ON    /redoc OFF
PROD                /docs OFF   /openapi.json OFF   /redoc OFF
```

## Quality and acceptance commands

From `apps/backend`:

```bash
# Local formatting (modifies files)
uv run ruff format .

# Non-mutating quality gates
uv run ruff format --check .
uv run ruff check .
uv run mypy

# Fast tests only — no PostgreSQL acceptance container
uv run pytest -m "not postgres"

# Real PostgreSQL 18.6 acceptance tests
uv run pytest -m postgres

# Full backend suite; includes the real PostgreSQL harness
uv run pytest

# Build wheel + source distribution
uv build
```

PostgreSQL-marked tests require the current image `dante-postgres-local:18.6`. They start one disposable, loopback-only acceptance container for the pytest session and create fresh databases inside that isolated cluster. If the required image is absent, the tests fail explicitly rather than skip.

This design protects the ordinary LOCAL `dante` database and its cluster-global application-role credentials from destructive acceptance testing while exercising the exact same DANTE PostgreSQL image/envelope.

## Historical CP5 integrated acceptance evidence

CP5 re-ran the production scaffold on the actual WSL2/Linux workstation against the then-current PostgreSQL 18.4 envelope:

```text
uv 0.12.5                                  PASS
Python 3.14.7                               PASS
uv lock --check / sync --locked            PASS
Ruff format + lint                         PASS
mypy strict                                PASS
fast pytest                                32/32 PASS
canonical PostgreSQL image rebuild         PASS
PostgreSQL pytest                          18/18 PASS
full pytest                                50/50 PASS
full-run coverage                          97.42% evidence only
uv build wheel + sdist                     PASS
LOCAL Compose PostgreSQL healthy           PASS
explicit provisioning                      PASS
real Uvicorn factory startup               PASS
GET /health/live                           200 {"status":"ok"}
GET /health/ready                          200 {"status":"ready"}
```

One immediately repeated full-suite launch hit a Docker Desktop/WSL `/forwards/expose` HTTP 500 while creating a disposable PostgreSQL container on a loopback port that had no Linux listener. After the diagnostic container was removed, a clean full run passed 50/50. The event is treated as transient local Docker port-forwarding behavior, not as an application or PostgreSQL acceptance failure.

## PostgreSQL 18.6 foundation regression evidence

Before concrete business-database materialization, CP6 refreshed only the PostgreSQL 18 maintenance patch and executed the then-existing mandatory CI lanes against the exact branch HEAD:

```text
Backend CI run                32568664940
workflow event                workflow_dispatch
HEAD                          ec3dc795b5e044daa3a77723c94a1b4b5b92865c

PostgreSQL base               18.6-trixie
PostGIS                       3.6.4
pgvector                      0.8.6

Backend Quality               SUCCESS
fast pytest                   32 / 32 PASS
Ruff format/lint              PASS
mypy strict                   PASS
wheel + sdist                 PASS

Backend PostgreSQL            SUCCESS
PostgreSQL pytest             18 / 18 PASS
Alembic fresh → head          PASS
Alembic base/head round-trip  PASS
Alembic drift check           PASS
privilege matrix              PASS
runtime identity              PASS
outage/readiness recovery     PASS
transaction semantics         PASS

Backend CI Gate               SUCCESS
current test corpus           50 / 50 covered across the two mandatory CI lanes
```

This remains historical **DIRECT REMOTE QA PASS for the technical PostgreSQL 18.6 foundation regression**. It predates and does not replace the final CP6-05 disposable PostgreSQL acceptance, later Recovery proof or current integrated protected-main acceptance.

## CP6 final direct acceptance evidence

Final accepted implementation HEAD:

```text
22bbc078391d52c43665474bf465593d6225106e
```

Observed final acceptance:

```text
ruff format --check               PASS — 44 files
ruff check                        PASS
mypy strict                       PASS — 40 source files
fast pytest                       37 / 37 PASS
uv build                          PASS
PostgreSQL 18.6 image             PASS
real PostgreSQL pytest            76 / 76 PASS
persistent LOCAL upgrade          20260826_07 → 20260826_08
alembic check                     PASS
final topology                    68|5|14|75|95|68|120
final security posture            PASS
Dictionary JSON-Schema            PASS
restart without volume deletion   PASS
revision/topology persistence     PASS
GET /health/live                  200 {"status":"ok"}
GET /health/ready                 200 {"status":"ready"}
```

See `docs/development/backend-cp6-05-whole-database-qa.md` for the full closure record, including historical failures and repairs.

## Access/Auth + Email + Recovery integration evidence

Exact accepted implementation proof HEAD:

```text
81639c61478b476c995652d0060dde8f53aef089
```

GitHub Actions on that exact HEAD:

```text
Dependency Review              PASS
Frontend CI                    PASS
Backend Quality                PASS
Backend PostgreSQL             PASS
Backend CI Gate                PASS
```

The real PostgreSQL lane includes the current migration/catalog/constraint/ACL acceptance suite against PostgreSQL 18.6. The CP07 whole LOCAL operator rehearsal then independently re-proved the accepted head/topology after restore and semantic reconciliation.

```text
Alembic                        20260904_17
topology                       88|5|16|76|172|89|270|0|0|0
DATABASE LOCAL REOPEN          PASS
old protected X resurrection  PROVEN
ledger reconciliation         PASS
payload reinsertion           REJECTED
```

PR #52 merged the final candidate `6cee5506d404d0684b0679aca54c03f0ca433c72` into protected main at `5f76ec54ad78542f137e8730e904f805d9e59e56`. The merge tree matches the final candidate tree exactly. Post-merge Backend Quality, real PostgreSQL acceptance, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate all passed.

See `docs/workstreams/access-auth-integration-acceptance-2026-09-04.md` for the durable integration record and `docs/operations/postgres-recovery-runbook.md` for the operator contract.

## Post-CP6 boundaries

The concrete PostgreSQL kernel, Recovery evolution, Access/Auth M1–M5 and shared Email Platform are closed and integrated on protected `main` at `20260904_17`.

Database existence alone still does **not** authorize or prove:

- arbitrary product API routes merely because database objects exist;
- frontend behavior outside accepted feature scope;
- direct AI database access;
- PowerSync, Restate or PgBouncer activation merely because selected;
- remote/cloud backup-provider activation merely because LOCAL pgBackRest recovery is implemented;
- automatic deadlock/serialization retries without operation-specific safety/idempotency design;
- production deployment or blanket Physical HG/PSV PASS;
- Apple real registered-domain acceptance without the external prerequisites and real UAT;
- production Email sender-domain/DNS/reputation/workload-identity acceptance from development SES UAT.

Current sequence:

```text
enriched protected main
→ feature/platform-observability
→ observability integration/release rechecks
→ protected-main Observability PR
→ future bounded workstreams
```

Future new verticals start only from the then-current enriched protected `main` under an explicit bounded gate.
