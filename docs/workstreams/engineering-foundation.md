# Workstream — Engineering Foundation v0

- Status: **CLOSED / ACCEPTED / FINAL REVIEW PASS**
- Branch: `chore/engineering-foundation-v0`
- Approved PRE-SCOPE: `ebc3616956faeabd99d90f5f32458b284be218e4`
- Final repair PRE-SCOPE: `0805eae9aa6288f588a8b8181cf94531270bdaa2`
- Product: **DANTE**
- Domain Model: **CLOSED / CONSUMED / NOT REOPENED**
- Logical Model: **CLOSED / CONSUMED / WL-H01..WL-H12 ACTIVE**
- Physical target: **CLOSED / SELECTED / ACCEPTED / CONSUMED**
- Production application code: **NOT STARTED**
- Direct selected-stack validation: **NOT STARTED / DIRECT HG PASS 0**

## 1. Purpose

Engineering Foundation v0 is the final bounded engineering-design workstream before DANTE production implementation.

It defines how the repository, backend development environment, persistence workflow, configuration, testing, CI/CD and release controls are structured. It does not redefine product semantics and it does not replace the closed Domain, Logical or Physical models.

```text
PRODUCT / DOMAIN / LOGICAL / PHYSICAL
                CLOSED
                  ↓
       ENGINEERING FOUNDATION v0
             CLOSED HERE
                  ↓
       PRODUCTION IMPLEMENTATION
                NEXT
```

## 2. Final approved scope

The workstream closes the following decisions.

### Repository and application boundaries

- keep **one DANTE product monorepo**;
- continue on the existing GitHub repository; do **not** create a new repository for production implementation;
- repository rename `lifeos → dante` is a separate governance operation, not part of this workstream;
- top-level deployable application boundaries are `apps/backend`, `apps/web`, `apps/mobile`;
- backend is the only application whose internal engineering structure is fixed here;
- web/mobile internal tooling, package-manager, test stack and release implementation are deferred to the dedicated frontend workstream;
- shared packages exist only for real shared contracts/assets, never as generic dumping grounds;
- backend starts as a capability-first modular monolith.

### Environment model

DANTE uses exactly these lifecycle contexts:

```text
LOCAL
DEV
UAT
PROD
```

- environments are **not Git branches**;
- `main` is the single integrated source truth;
- LOCAL activates with first implementation;
- remote DEV is architecturally defined now but activated only when remote integration is useful;
- UAT activates when real release candidates exist;
- PROD activates at production-readiness;
- DEV/UAT/PROD require independent state, credentials, secrets and provider-native isolation boundaries;
- cloud/compute provider remains intentionally unselected until the first remote environment is implemented.

### Backend development baseline

```text
Python line                 3.14.x
initial interpreter pin     3.14.7
package/environment mgr     uv
backend source root         apps/backend/src/dante
formatter/linter            Ruff
type checker                mypy strict baseline
test runner                 pytest
property testing            Hypothesis where valuable
```

Windows development baseline:

```text
HOST                        Windows 11 supported
CANONICAL BACKEND SEMANTICS Linux
WINDOWS BACKEND ENV         WSL2 / Linux
PRIMARY USER IDE            PyCharm supported with WSL interpreter
REPOSITORY                  stored in WSL filesystem for backend workflow
```

The repository remains IDE-neutral; PyCharm is a supported workflow, not a repository dependency.

### Local infrastructure

- backend process normally runs directly in WSL/Linux for fast reload/debug;
- Docker Compose owns stateful LOCAL dependencies;
- future deployable backend is packaged as an immutable OCI image;
- LOCAL persistence uses real PostgreSQL 18.4;
- the selected PostgreSQL extension envelope is installed **and enabled from the first LOCAL database**, even where application code does not yet use it:
  - PostGIS 3.6.4;
  - pgvector 0.8.6;
  - `pg_trgm`;
  - `unaccent`;
  - `pg_stat_statements` with required preload configuration;
  - native PostgreSQL full-text search availability;
- DANTE owns a reproducible PostgreSQL development image/build/configuration; no unpinned “all extensions” image is accepted as canonical LOCAL infrastructure.

PgBouncer 1.25.2 remains a selected Physical target but activates in the concrete connection/pooling validation boundary rather than being forced into every day-one local connection.

### Persistence and schema evolution

```text
ORM / SQL toolkit           SQLAlchemy 2.0 stable line
PostgreSQL driver           psycopg 3
DB I/O                      async at I/O boundaries
Domain/application logic    sync/pure by default
migration authority         Alembic
```

Hard rules:

- ORM rows/mappings are not the Domain Model;
- transport DTOs are not the Domain Model;
- no universal generic `Repository[T]` CRUD semantic model;
- `AsyncSession` is bounded to one use-case/task transaction and never shared concurrently;
- commit/rollback ownership belongs to the application/use-case transaction boundary;
- deployed schema is migration-owned; application startup never manages production schema with `metadata.create_all()`;
- Alembic autogenerate creates a candidate only;
- applied/merged migration revisions are immutable;
- manual unrepresented DDL in DEV/UAT/PROD is forbidden;
- schema drift is detected in CI once mappings/migrations exist;
- breaking evolution uses expand → migrate → contract;
- large backfills/data transformations use bounded, resumable, idempotent jobs rather than giant long-held migration transactions;
- migration risk analysis includes lock/rewrite/data-loss consequences and uses PostgreSQL-safe techniques such as concurrent index creation and staged constraint validation where appropriate;
- database privileges separate owner, migrator, runtime, replication and backup responsibilities when those roles activate.

Copy/recovery paths are deliberately distinct:

```text
pg_dump / pg_restore
logical copy / portability / bounded clone use

pgBackRest + WAL / PITR
recovery-grade physical backup path at the accepted recovery boundary
```

- restore rehearsal is mandatory once recovery is active;
- raw PROD dumps are not normal DEV test data;
- production-derived lower-environment data requires explicit sanitization/minimization;
- PostgreSQL major-version upgrades are a separate platform procedure, not ordinary DANTE schema migrations.

### Configuration and secrets

Backend configuration:

- uses `pydantic-settings` as the typed bootstrap boundary;
- is validated before serving work;
- fails fast on missing/invalid/dangerous combinations;
- is immutable after bootstrap;
- distinguishes non-secret deployment config, secret material, build/release identity and governed domain/business configuration;
- uses `.env.local` only for ignored LOCAL convenience and a safe committed `.env.example` contract.

Remote secret posture:

```text
MINIMIZE SECRETS
        ↓
WORKLOAD / FEDERATED IDENTITY
        ↓
PROVIDER SECRET MANAGER
        ↓
LEAST PRIVILEGE
        ↓
ROTATION / REVOCATION / AUDIT
```

- GitHub OIDC is the preferred CI-to-cloud identity mechanism when supported;
- long-lived deployment keys are fallback only;
- DEV/UAT/PROD credentials are independent;
- runtime and migration database identities are independent;
- secrets are not source code, OCI build arguments, checked-in deployment manifests or client configuration;
- logging/telemetry must redact credentials and sensitive configuration.

### Backend testing

Required risk layers as implementation appears:

- unit/domain tests;
- application/use-case tests;
- property/invariant tests with Hypothesis where state space matters;
- state-machine testing where lifecycle sequencing is material;
- architecture dependency tests;
- real PostgreSQL 18.4 integration tests using the DANTE-owned database image/envelope;
- migration base→head and released-version→head tests;
- schema-drift checks;
- concurrency/expected-state/idempotency/multi-owner/outbox-atomicity tests;
- provider fake + real non-production contract tests when integrations activate;
- HTTP/API contract behavior tests when the API exists;
- explicit privacy/non-interference test families, including WL-H12 leakage classes;
- performance/resilience/recovery/PSV tests only at applicable boundaries.

SQLite is never accepted as proof of PostgreSQL backend behavior.

Coverage is tracked but no arbitrary numeric floor is invented before the first real vertical slice provides a meaningful denominator. Later thresholds are deliberate and ratcheted, not silently lowered to make CI green.

Tests are tiered by cost: PR, accepted-main/DEV, scheduled/nightly and UAT/release.

### CI/CD and supply chain

- GitHub Actions is the primary CI/CD orchestration layer;
- workflows are separated by responsibility rather than one monolithic workflow;
- protected `main` remains the integration boundary;
- while DANTE has one active developer, fake human-review requirements are not introduced; automated gates remain real;
- a status check becomes required only after its actual emitted context is verified stable and its failure genuinely means merge must stop;
- workflow `GITHUB_TOKEN` permissions are explicit and least-privilege;
- protected workflows pin external Actions to immutable full commit SHAs;
- normal PR execution receives no production/deployment identity;
- dependency review activates with real manifests and an accepted severity policy;
- CodeQL Python activates when real production Python exists;
- secret scanning/push protection is used where repository capability supports it;
- GitHub-hosted runners are the default until a measured need justifies self-hosted runners;
- merge queue remains deferred until real merge concurrency creates a problem;
- deployment uses immutable artifact identity/digest;
- server release posture is build once → promote exact artifact where the platform permits;
- release artifacts gain provenance/attestation and SBOM at the production release boundary.

## 3. Explicitly deferred

The following are not missing decisions; they are intentionally deferred to the boundary that provides the required facts:

```text
frontend web/mobile internal engineering stack
Node / pnpm / Turborepo or alternatives
web/mobile detailed test stack
mobile EAS/release implementation
exact shared frontend package map

cloud/compute provider
IaC engine
container/artifact registry
remote DEV/UAT/PROD sizing

concrete backend capability-module map
concrete PostgreSQL tables/columns/migrations
exact API route/version surface
AuthN/AuthZ implementation

specialist Physical component implementation
PowerSync / R2 / OR-Tools implementation
Restate activation
pgBackRest/AWS S3 activation before its fixed boundary
```

No deferred item may be silently improvised; it opens through its own implementation decision/gate.

## 4. Preserved inherited Physical posture

The closed Physical target is not reopened.

Particularly:

```text
PostgreSQL 18.4
sole canonical persistence authority

PowerSync + encrypted SQLite
bounded local/offline copy; noncanonical

Class A async work
PostgreSQL transactional outbox + bounded worker

Class B durable work
Restate selected but dormant until first real Class-B workflow

ContentArtifact bytes
Cloudflare R2 Standard / private / EU jurisdiction when activated

Recovery
pgBackRest + AWS S3 eu-south-1 selected but dormant until recovery/production boundary or real rehearsal

Solver
OR-Tools CP-SAT candidate mechanism under accepted rules

Observability
OpenTelemetry + Grafana Alloy + Grafana Cloud EU target
```

Dormancy never cancels applicable PSV obligations.

## 5. Direct-validation truth

Engineering Foundation closure is a design/documentation closure only.

```text
DATABASE DEPLOYMENT          NOT STARTED
SCHEMA IMPLEMENTATION        NOT STARTED
MIGRATIONS IMPLEMENTATION    NOT STARTED
BACKEND SCAFFOLD             NOT STARTED
DIRECT HG                    NOT RUN
DIRECT HG PASS               0
PSV                           NOT RUN
RESTORE REHEARSAL            NOT RUN
PRODUCTION DEPLOYMENT         NOT STARTED
```

No PASS statement in this workstream may be interpreted as implementation evidence.

## 6. Final review result

Final review found:

```text
BLOCKING ARCHITECTURE DEFECTS          0
DOMAIN/LOGICAL IMPLICIT REOPENS        0
PHYSICAL TARGET REOPENS                0
CANONICAL AUTHORITY CONFLICTS          0
UNAPPROVED FRONTEND TOOLING DECISIONS  0 after repair
FALSE DIRECT PASS CLAIMS               0
CLOUD PROVIDER PRESELECTION            0
```

The earlier draft overreach was repaired before closure. The closed specification contains only approved backend/foundation decisions and explicit deferrals.

## 7. Exact next handoff

The next conversation must **not** reopen Engineering Foundation by default.

Start with this order:

```text
STEP 0 — repository identity governance
keep the current repository; DO NOT create a new repository.
Decide/execute the recommended rename `lifeos → dante`, or explicitly defer it.

STEP 1 — production repository/backend scaffold
create only real files/directories required for:
- apps/backend
- Python 3.14.x + uv manifest/lock/pin
- Ruff / mypy / pytest/Hypothesis configuration
- WSL2/Linux developer contract
- Docker Compose/local DANTE PostgreSQL 18.4 image with full selected extension envelope enabled
- SQLAlchemy/psycopg/Alembic bootstrap and migration harness
- typed config bootstrap
- initial architecture/test/CI skeleton only where a real emitted check can exist

STEP 2 — concrete Logical → PostgreSQL implementation
only after scaffold QA.
```

Before STEP 1, run the mandatory repository bootstrap and a fresh exact Git write gate. Production schema/business code is not authorized merely by this closure document.
