# DANTE System Overview

- Status: **CURRENT ARCHITECTURE OVERVIEW**

## 1. Product

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and the distinction between intention, execution and outcome.

Compass: **Understand life. Shape what comes next.**

## 2. Architectural authority

Implementation consumes the closed Product/Domain/Logical/Physical models and the closed Engineering Foundation.

Core invariants include:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical DANTE state
derived projection != canonical truth
absence/unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI/solver output != accepted canonical effect
```

WL-H01..WL-H12 remain active.

## 3. Repository/application topology

One product monorepo:

```text
DANTE repository
│
├── apps/backend
│   └── capability-first modular monolith
│
├── apps/web
│   └── client boundary; internal engineering deferred
│
├── apps/mobile
│   └── client boundary; internal engineering deferred
│
├── packages
│   └── only genuinely shared contracts/artifacts
│
├── infra
│   └── LOCAL and future remote infrastructure definitions
│
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Production implementation continues in the existing repository. A rename from historical `lifeos` to `dante` is a separate governance step; a new repo is not planned.

## 4. Backend architecture

Target internal shape:

```text
apps/backend/src/dante
├── bootstrap
├── kernel
├── platform
└── modules/<capability>
    ├── domain
    ├── application
    ├── ports
    └── adapters
        ├── inbound/http
        └── outbound/persistence|integrations
```

The shape expresses dependency direction, not mandatory empty folders.

FastAPI is an inbound adapter/process host.

SQLAlchemy/persistence/provider/runtime objects remain outside Domain identity.

Capability boundaries are behavior/cohesion based, not one owner/table/route per module.

## 5. Canonical persistence

```text
PostgreSQL 18.4
SOLE CANONICAL PERSISTENCE AUTHORITY
```

It owns canonical material state/history required by the accepted Logical/Physical model.

Selected DB capabilities:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native FTS;
- pg_trgm;
- unaccent;
- pg_stat_statements;
- PgBouncer 1.25.2 target.

The first LOCAL DB already has the full extension envelope installed/enabled. “Enabled” does not mean every capability is already used by application code.

## 6. Persistence/application boundary

```text
application use case
        ↓
capability-shaped persistence boundary
        ↓
SQLAlchemy 2.0 / psycopg 3
        ↓
PostgreSQL
```

Rules:

- ORM != Domain;
- no universal generic CRUD repository;
- one AsyncSession per concurrent use-case/task scope;
- application/use-case boundary owns transaction;
- implicit/lazy DB I/O does not leak into Domain/application logic;
- cross-capability transaction remains possible inside the modular monolith where accepted semantics require atomicity.

## 7. Schema evolution

```text
Alembic revision history
= deployment schema-change authority
```

Policy:

- autogenerate candidate only;
- applied revisions immutable;
- clean base→head tests;
- metadata/schema drift detection;
- lock/rewrite/data-loss review;
- online/staged PostgreSQL techniques where appropriate;
- expand → migrate → contract for breaking evolution;
- large backfills as bounded resumable/idempotent jobs;
- separate runtime/migrator/owner privileges.

Logical copy and disaster recovery are different mechanisms:

```text
pg_dump / pg_restore
logical copies / bounded clone workflows

pgBackRest + WAL/PITR + AWS S3
recovery-grade path when recovery boundary activates
```

## 8. Offline/sync

Selected target:

- PowerSync Open Edition;
- encrypted SQLite local state;
- PostgreSQL-backed PowerSync bucket storage;
- explicit client-safe sync projections.

Invariants:

```text
SQLite local state != canonical truth
PowerSync arrival order != conflict resolution
consequential offline mutation → backend revalidation → PostgreSQL
```

PowerSync is not implemented merely because the target is selected.

## 9. Async/durable work

### Class A

PostgreSQL transactional outbox + bounded worker.

Where semantics require atomicity:

```text
canonical state transition
+
outbox record
= same PostgreSQL transaction
```

### Class B

Restate is selected but dormant until first real Class-B durable workflow.

Restate runtime state never becomes canonical DANTE history by default.

## 10. Content artifacts / object bytes

When activated:

```text
PostgreSQL
owns ContentArtifact identity/metadata/provenance/visibility/retention/hash/locator

Cloudflare R2
owns private raw object bytes only
```

R2 is private and EU-jurisdiction target under the accepted Physical posture.

## 11. Recovery

Selected target:

- pgBackRest 2.59.0;
- AWS S3 Standard eu-south-1;
- Versioning/Object Lock posture defined by Physical model;
- WAL/PITR;
- anti-resurrection requirement;
- recovery copies noncanonical.

Initial implementation posture remains dormant until recovery/production boundary or real rehearsal.

Once active, backup verification and restore rehearsal are mandatory evidence.

## 12. Solver

OR-Tools CP-SAT is the selected candidate mechanism when solver-backed planning arrives.

```text
UNKNOWN != INFEASIBLE
```

Solver output remains candidate/derived context until accepted through governed application semantics.

## 13. Observability

Selected target:

- OpenTelemetry;
- Grafana Alloy;
- Grafana Cloud EU;
- pg_stat_statements.

Observability is privacy-minimized operational telemetry, not a shadow user-data store or canonical history.

Backend design includes correlation/release identity and secret/payload redaction boundaries from the first service scaffold.

## 14. Configuration/secrets

Backend uses typed `pydantic-settings` configuration with fail-fast validation and immutable runtime state.

Remote target:

```text
workload/federated identity
→ provider secret manager
→ least privilege
→ rotation/revocation/audit
```

GitHub OIDC is preferred for future cloud deployment identity.

DEV/UAT/PROD identities/secrets/state remain isolated.

## 15. Environments

```text
LOCAL → DEV → UAT → PROD
```

These are runtime lifecycle contexts, not Git branches.

- LOCAL activates with first implementation;
- remote DEV when remote integration is useful;
- UAT with real release candidates;
- PROD at production readiness.

Cloud/compute provider and IaC engine are intentionally deferred.

## 16. CI/security

GitHub Actions is the primary CI/CD control plane.

Backend quality target includes:

- Ruff/mypy;
- unit/application/Hypothesis;
- architecture tests;
- real PostgreSQL integration/migration/concurrency;
- privacy/non-interference tests;
- dependency/security analysis;
- real-check-before-required-check branch-protection rule;
- least-privilege workflows and immutable Action SHA pinning;
- no production deployment identity in ordinary PRs;
- future artifact digest/provenance/SBOM release evidence.

## 17. Frontend relationship

`apps/web` and `apps/mobile` consume governed backend contracts.

Their internal package/tool/test/build decisions are deliberately deferred to the frontend workstream. They cannot bypass backend authority for consequential canonical mutations.

## 18. Current direct evidence boundary

Architecture/design closure is not implementation proof.

```text
BACKEND SCAFFOLD          NOT STARTED
DATABASE DEPLOYMENT       NOT STARTED
CONCRETE SCHEMA           NOT STARTED
DIRECT HG                 NOT RUN
PSV                       NOT RUN
RESTORE REHEARSAL         NOT RUN
```

## 19. Next system-building step

Keep the current repository. Resolve the small repository rename decision (`lifeos → dante`) first, then open an exact write gate for the real `apps/backend` scaffold and LOCAL PostgreSQL/migration/test/config/CI baseline.
