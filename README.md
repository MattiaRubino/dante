# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED

LOGICAL MODEL
CLOSED
WL-H01..WL-H12 ACTIVE

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

PRODUCTION BACKEND SCAFFOLD
NOT STARTED

DIRECT SELECTED-STACK VALIDATION / PSV
NOT RUN
```

Engineering Foundation v0 is the final pre-implementation engineering baseline. There is no separate standalone Development Profile phase.

## Production repository direction

DANTE continues in this repository as one product monorepo.

```text
apps/
├── backend/
├── web/
└── mobile/
```

- `apps/backend` is the server-side application boundary;
- `apps/web` and `apps/mobile` are sibling client boundaries;
- backend internal engineering is fixed by Engineering Foundation v0;
- web/mobile internal engineering/tooling remains deferred to the dedicated frontend workstream;
- do **not** create a new repository for production implementation.

The historical repository name `lifeos` may be renamed to `dante` in a separate small governance operation. Rename is recommended before the production scaffold unless explicitly deferred.

## Backend engineering baseline

```text
Python                 3.14.x
initial pin             3.14.7
package manager         uv
source root             apps/backend/src/dante
format/lint             Ruff
type checking           mypy strict
unit/integration runner pytest
property testing        Hypothesis where meaningful

server semantics        Linux
Windows workflow        WSL2/Linux
primary user IDE        PyCharm with WSL interpreter supported
local stateful infra    Docker Compose

canonical persistence   PostgreSQL 18.4
ORM/SQL toolkit         SQLAlchemy 2.0 stable line
driver                  psycopg 3
migrations              Alembic
```

The first LOCAL PostgreSQL baseline includes the full selected extension envelope installed/enabled:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- `pg_trgm`;
- `unaccent`;
- `pg_stat_statements` with preload configuration;
- native PostgreSQL full-text search.

LOCAL uses a DANTE-owned reproducible PostgreSQL image/build/configuration.

## Environment model

```text
LOCAL
DEV
UAT
PROD
```

These are environments, **not Git branches**.

Activation is progressive:

- LOCAL: first implementation;
- DEV: when remote/shared integration becomes useful;
- UAT: when real release candidates exist;
- PROD: production-readiness.

Cloud/compute provider and IaC engine remain intentionally unselected until the first remote-infrastructure boundary.

## Persistence/recovery posture

Schema evolution is migration-governed:

- Alembic revisions are authoritative deployment history;
- autogenerate creates candidates only;
- applied revisions are immutable;
- schema drift is tested;
- risky changes use expand → migrate → contract;
- large backfills are bounded/resumable/idempotent jobs;
- runtime/migrator/owner/replication/backup privileges are separated as they activate;
- `pg_dump`/`pg_restore` provide logical-copy workflows;
- pgBackRest + WAL/PITR + AWS S3 remains the selected recovery target and stays dormant until the accepted recovery/production boundary or real rehearsal need.

## Testing and delivery

Backend validation is risk-layered:

- unit/domain;
- application/use-case;
- Hypothesis property/state-machine;
- architecture boundaries;
- real PostgreSQL integration;
- migration/drift;
- concurrency/idempotency/multi-owner/outbox atomicity;
- provider contract;
- HTTP/API contract;
- privacy/non-interference including WL-H12;
- release/recovery/PSV at applicable boundaries.

GitHub Actions is the primary CI/CD control plane. Protected workflow policy includes least-privilege permissions, immutable Action SHA pinning, no production identity in normal PRs, OIDC for future cloud deployment, real-check-before-required-check discipline, and production artifact provenance/SBOM at the release boundary.

## Selected Physical target remains unchanged

Key target components include:

- PostgreSQL 18.4 canonical persistence;
- PostGIS / pgvector / native FTS / pg_trgm / unaccent / pg_stat_statements;
- PgBouncer 1.25.2;
- PowerSync + encrypted SQLite for bounded offline/local state when activated;
- PostgreSQL transactional outbox for Class-A async work;
- Restate for Class-B durable work, initially dormant;
- Cloudflare R2 for private ContentArtifact bytes when activated;
- pgBackRest + AWS S3 eu-south-1 for recovery, initially dormant;
- OR-Tools CP-SAT for solver capability when activated;
- OpenTelemetry + Grafana Alloy + Grafana Cloud EU observability target.

No specialist component is implicitly active merely because it is selected.

## Direct evidence truth

Do not infer implementation PASS from architecture closure.

```text
DATABASE DEPLOYMENT      NOT STARTED
BACKEND SCAFFOLD         NOT STARTED
CONCRETE DB SCHEMA       NOT STARTED
MIGRATION IMPLEMENTATION NOT STARTED
DIRECT HG                NOT RUN
DIRECT HG PASS           0
PSV                      NOT RUN
RESTORE REHEARSAL        NOT RUN
PRODUCTION DEPLOYMENT    NOT STARTED
```

## Where to continue

Read in this order before the next write:

1. `docs/README.md`
2. `docs/PROJECT-STATUS.md`
3. `docs/development/agent-operating-manual.md`
4. `docs/development/operating-rules.md`
5. `docs/development/documentation-and-handoff.md`
6. `docs/development/branching-and-environments.md`
7. `docs/development/repository-engineering-safety.md`
8. `docs/workstreams/engineering-foundation.md`
9. `docs/development/engineering-foundation-v0.md`
10. PM-11 / PM-12 / post-selection validation register as required by the next scope.

### Exact next boundary

```text
STEP 0
Keep this repository. Decide/execute recommended repository rename
`lifeos → dante`, or explicitly defer the rename.

STEP 1
Open a fresh exact write gate for the real production scaffold under
`apps/backend` and LOCAL PostgreSQL infrastructure.

STEP 2
After scaffold QA, begin concrete Logical → PostgreSQL implementation.
```

Do not reopen Domain/Logical/Physical/Engineering Foundation by default.
