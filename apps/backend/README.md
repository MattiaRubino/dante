# DANTE Backend

Production backend application for DANTE.

The backend runs on the accepted CP1–CP6 PostgreSQL foundation and the integrated Access/Auth, Shared Email, Recovery, Observability, AI low-level platform and pre-vertical foundation layers. Historical phase-by-phase evidence lives in dedicated development/workstream/archive records and Git/PR history; this README describes current runtime/engineering truth.

## Current status

```text
PostgreSQL                                18.6
Protected-main Alembic                    20260906_18
Protected-main topology                   89|5|18|77|173|91|272|0|0|0

Access/Auth M1–M5                         CLOSED / INTEGRATED
Shared Email Platform                     CLOSED / INTEGRATED
PostgreSQL Recovery                       CLOSED / INTEGRATED
Platform Observability                    CLOSED / INTEGRATED VIA PR #58
AI deterministic low-level foundation     CLOSED / INTEGRATED VIA PR #63
Home / World Focus reconciliation         CLOSED / INTEGRATED VIA PR #65
Pre-vertical foundation                   CLOSED / INTEGRATED VIA PR #66

PV-01 Identity / Clock / Time             CLOSED / PASS
PV-02 User Context / Dogfood / Personas   CLOSED / PASS
PV-03 A Scale Harness                     CLOSED / PASS
PV-03 B Whole-Branch QA                   CLOSED / PASS
PV-03 C protected-main integration        CLOSED / PASS
```

Pre-vertical integration anchor:

```text
final candidate   21353469464f1371f9913dc78933f4ee42698f33
PR                #66
merge commit      1ecd58145860aebfaaa3dc1bd356b90f7a8eb19b
```

There is no PV-04.

Current closure record:

`docs/workstreams/pre-vertical-foundation-closure-2026-09-06.md`

Current database authority:

`docs/database/README.md`

Current Recovery operator authority:

`docs/operations/postgres-recovery-runbook.md`

## Pre-vertical backend foundation

The integrated foundation adds only bounded cross-cutting seams needed before a real product vertical:

```text
AuthSession
→ admitted Principal
→ Account
→ AccountApplicationContext
→ self Person
→ user/default timezone policy
→ effective request timezone
```

Permanent distinctions remain:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
```

`20260906_18` adds the Account application-context mapping and bounded first-use capability. Generic runtime `INSERT Person` remains denied. Application-issued UUIDv7 remains identity construction detail and is never chronology/currentness authority.

LOCAL/DEV dogfood and persona tooling lives under:

`apps/backend/tooling/pre_vertical_foundation/`

Operational instructions:

`docs/development/pre-vertical-dogfood-personas.md`

Deterministic scale/readiness reference:

`docs/development/pre-vertical-scale-harness.md`

## Runtime contract

```text
Python supported line      3.14.x
initial exact pin          3.14.7
package manager            uv
import namespace           dante
project distribution      dante-backend
server semantics           Linux / WSL2
canonical DB architecture PostgreSQL 18
current technical patch    PostgreSQL 18.6
```

The repository-controlled environment lives at `apps/backend/.venv` after `uv sync`. Do not share one virtual environment between Windows and WSL.

## Dependency bootstrap

From `apps/backend`:

```bash
uv sync --locked
uv lock --check
uv tree --locked --depth 1
```

`pyproject.toml` records compatibility policy; `uv.lock` records the exact resolved graph. Never hand-edit `uv.lock`.

Current persistence resolution includes:

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

## Runtime configuration

`.env.example` is a safe runtime-only template. Copy it to `.env.local` and replace placeholders with LOCAL credentials kept outside Git.

The application does not discover `.env.local` automatically; inject it explicitly through `uv`.

Runtime database settings:

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

## LOCAL database security provisioning

Canonical application identities:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
dante_observer   LOGIN statistics-only collector identity
```

Provisioning is intentionally separate from FastAPI startup and Alembic. Supply admin, migrator, runtime and observer credentials only to the provisioning command/process.

Conceptual invocation from `apps/backend`:

```bash
DANTE_DATABASE__HOST=127.0.0.1 \
DANTE_DATABASE__PORT=5432 \
DANTE_DATABASE__NAME=dante \
DANTE_ADMIN__USER=postgres \
DANTE_ADMIN__PASSWORD='<local admin secret>' \
DANTE_MIGRATOR__PASSWORD='<local migrator secret>' \
DANTE_RUNTIME__PASSWORD='<local runtime secret>' \
DANTE_OBSERVER__PASSWORD='<independent local observer secret>' \
uv run python -m dante.platform.database.provisioning
```

Do not commit these secrets or reuse LOCAL credentials in DEV/UAT/PROD.

`dante_observer` is a technical statistics reader only. Its exact least-privilege contract is in `docs/database/dante-postgresql-database-part-12.md` and live provisioning/ACL tests.

## Alembic

Alembic owns application-schema deployment history.

```text
schema               dante
version table        dante.alembic_version
migration login      dante_migrator
DDL owner role       dante_owner via explicit SET ROLE
```

Normal application startup never runs migrations.

Current graph:

```text
20260826_08
├── 20260830_09 Recovery
└── 20260827_09 → ... → 20260904_16 Access/Auth + Email

20260830_09 + 20260904_16
            ↓
        20260904_17
            ↓
        20260906_18            current protected-main head
```

Applied migration history is immutable. Later corrections use new forward revisions. A future product vertical that genuinely needs a schema change must evolve the database through a reviewed forward migration and keep SQLAlchemy, Dictionary, human reference and direct tests aligned in the same change.

## Run locally

After roles/schema are provisioned and `.env.local` contains the matching runtime/Auth configuration:

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

Probe responses expose no credentials, DSN, database host/name, SQL or stack details. Neither probe appears in the product OpenAPI surface.

The normal Web LOCAL development server owns `http://localhost:5173` and proxies `/api/v1` to the canonical local backend `http://127.0.0.1:8000`. The Auth LOCAL origin example is aligned to that topology.

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

The outer application-operation boundary owns commit/rollback. Persistence adapters never commit implicitly. There is no generic `Repository[T]` or generic Unit of Work in the accepted foundation.

Provider/network I/O remains forbidden inside authoritative PostgreSQL transactions. For Email delivery, canonical feature mutation + durable EmailIntent may share one transaction; provider I/O occurs only after commit and ambiguity is never blindly retried.

## API documentation behavior

```text
LOCAL / DEV / UAT   /docs ON    /openapi.json ON    /redoc OFF
PROD                /docs OFF   /openapi.json OFF   /redoc OFF
```

## Quality and acceptance commands

From `apps/backend`:

```bash
# Local formatting — modifies files
uv run --locked ruff format .

# Non-mutating quality gates
uv run --locked ruff format --check .
uv run --locked ruff check .
uv run --locked mypy

# Fast tests
uv run --locked pytest -m "not postgres"

# Real PostgreSQL 18.6 acceptance
uv run --locked pytest -m postgres

# Full suite
uv run --locked pytest

# Build
uv build
```

PostgreSQL-marked tests require the canonical `dante-postgres-local:18.6` image. They use a disposable acceptance cluster and fresh databases rather than destructive mutation of the ordinary LOCAL `dante` database.

## Accepted pre-vertical evidence

The final pre-vertical implementation had direct evidence for:

```text
Ruff format/lint                              PASS
strict mypy                                   PASS
non-PostgreSQL pytest                         457 PASS
AI eval deterministic pytest                  22 PASS
backend build                                 PASS
real PostgreSQL 18.6 acceptance               165 PASS
exact-head LOCAL Recovery                     PASS
Backend CI Gate                               PASS
Dependency Review                             PASS
Frontend CI Gate                              PASS
protected-main merge/readback                 PASS
```

The final exact-head Recovery proof is bound to candidate `21353469464f1371f9913dc78933f4ee42698f33`. It proves the current database-local Recovery contract; it does not relabel historical CP08 application/Email reopen evidence as newly executed.

## Durable engineering references

Current references:

- `docs/database/README.md` — database system of record
- `docs/architecture/authenticated-dante-context.md` — Account → DANTE context contract
- `docs/development/pre-vertical-dogfood-personas.md` — LOCAL/DEV seed/persona tooling
- `docs/development/pre-vertical-scale-harness.md` — deterministic scale fixtures
- `docs/operations/postgres-recovery-runbook.md` — Recovery/reopen operator contract
- `docs/workstreams/pre-vertical-foundation-closure-2026-09-06.md` — final pre-vertical closure record

Historical CP1–CP6, Recovery, Access/Auth and integration measurements remain in dedicated development/workstream/archive records and Git/PR history rather than being duplicated here as an append-only diary.

## Permanent boundaries

Database/schema existence alone does **not** authorize or prove:

- arbitrary product API routes merely because database objects exist;
- frontend behavior outside accepted feature scope;
- direct AI database access;
- PowerSync, Restate or PgBouncer activation merely because selected;
- remote/cloud backup-provider activation from LOCAL pgBackRest evidence;
- automatic deadlock/serialization retries without operation-specific safety/idempotency design;
- production deployment or blanket Physical HG/PSV PASS;
- Apple registered-domain acceptance without real external prerequisites/UAT;
- production Email sender-domain/DNS/reputation/workload-identity acceptance from development UAT.

Future product work starts from then-current protected `main` under a new explicit bounded scope. Do not continue development on the retired `feature/pre-vertical-foundation` branch.
