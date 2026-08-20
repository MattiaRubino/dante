# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED
integrated via protected-main workflow
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
PM-11 COMPLETE
PM-12 COMPLETE
PM-13 QA PASS
PM-14 CLOSURE COMPLETE

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED / FINAL REVIEW PASS

FRONTEND ENGINEERING FOUNDATION
DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS
PASSO 1 PASS
PASSO 2 PASS
PASSO 3 PASS
INTEGRATED VIA PR #22
MERGE COMMIT 9116cd508d372cd56cf00403aa59633589b2d365
PRODUCTION FRONTEND CODE NOT STARTED
DIRECT FRONTEND VALIDATION NOT RUN

PRODUCTION BACKEND SCAFFOLD
NOT STARTED

CONCRETE LOGICAL → POSTGRESQL IMPLEMENTATION
NOT STARTED

DIRECT SELECTED-STACK IMPLEMENTATION VALIDATION
NOT STARTED
DIRECT HG PASS 0
VERIFIED-RUN SCORE NOT AVAILABLE
```

## 2. Product/North Star

DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

Compass: **Understand life. Shape what comes next.**

Important product invariants include:

- life central, not task/calendar centric;
- planned vs actual preserved;
- user authority and authorship;
- historical/material truth;
- privacy and provenance;
- honest uncertainty;
- progressive complexity;
- personal-first, not personal-only;
- AI is not the product authority;
- possibility != action/decision/preference;
- Effort != Execution != Outcome != Goal Progress.

## 3. Core identity/governance invariants

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
HTTP/UI/tool/AuthZ string != canonical governed effect
client local state != canonical accepted effect
```

WL-H01..WL-H12 remain active and constrain implementation.

## 4. Logical model

57/57 owners are classified.

Native identity owners include Person, Living Referent, Asset, Place, Content Artifact, Collective, Possibility, Goal, Plan, Activity, Event, Routine, Occurrence, Session and Observation.

Reference families:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

No implementation scope may mechanically translate 57 Logical owners into 57 services/modules/tables by assumption.

## 5. Accepted Physical target

### Canonical persistence

```text
PostgreSQL 18.4
sole canonical persistence + material history authority
```

Selected PostgreSQL capabilities:

- PostGIS 3.6.4;
- pgvector 0.8.6;
- native full-text search;
- pg_trgm;
- unaccent;
- pg_stat_statements;
- PgBouncer 1.25.2.

### Offline/sync

- PowerSync Service 1.25.0 Open Edition target from the accepted Physical Model;
- encrypted SQLite local state;
- PostgreSQL-backed PowerSync bucket storage;
- explicit client-safe sync projections.

Frontend implementation must preserve:

```text
SQLite local copy != canonical truth
PowerSync arrival order != conflict resolution
offline capability = operation-specific
local pending mutation != canonical effect
consequential offline mutation → DANTE backend revalidation → PostgreSQL
```

PowerSync JavaScript client packaging/version is selected by the closed Frontend Foundation and does not rewrite accepted Physical ownership semantics.

### Async/durable

Class A:

- PostgreSQL transactional outbox + bounded worker.

Class B:

- Restate selected;
- Restate Python SDK 1.0.3 / Server 1.7.2 target posture;
- **dormant / not active** until first real Class-B durable workflow;
- self-hosted vs Cloud EU deferred until activation.

### Objects

- Cloudflare R2 Standard;
- EU jurisdiction;
- private;
- raw bytes only;
- PostgreSQL owns ContentArtifact identity/metadata/provenance/visibility/retention/hash/locator semantics.

### Recovery

- pgBackRest 2.59.0;
- AWS S3 Standard `eu-south-1`;
- Versioning + accepted Object Lock GOVERNANCE posture;
- recovery copies noncanonical;
- anti-resurrection required;
- **dormant** until recovery/production boundary or real rehearsal.

### Solver

- OR-Tools 9.15 CP-SAT candidate mechanism;
- UNKNOWN != INFEASIBLE.

### Observability

- OpenTelemetry;
- Grafana Alloy 1.18.0;
- Grafana Cloud EU;
- privacy-minimized operational telemetry.

## 6. Engineering Foundation v0 — closed

### Repository

```text
one product monorepo
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

Paths are materialized only when real content exists. Production remains in the current repository.

### Backend architecture

- capability-first modular monolith;
- Domain/application/adapters separated;
- FastAPI inbound adapter/process host;
- no universal `Repository[T]`/BaseService/service locator/global DB session;
- cross-module transactions allowed when accepted semantics require atomicity.

### Backend toolchain

```text
Python             3.14.x
initial pin         3.14.7
uv
Ruff
mypy strict
pytest
Hypothesis
SQLAlchemy 2.0 stable line
psycopg 3
Alembic
```

### Developer environment

- Linux canonical server semantics;
- Windows 11 via WSL2/Linux;
- one authoritative WSL-backed repository posture;
- PyCharm WSL supported;
- backend direct WSL inner loop;
- Docker Compose stateful LOCAL infra;
- future backend immutable OCI deployable.

### LOCAL PostgreSQL

First LOCAL DB uses real PostgreSQL 18.4 with full selected extension envelope enabled, including pg_stat_statements preload. DANTE owns reproducible LOCAL PostgreSQL build/configuration.

### Persistence/migration

- async DB I/O technical boundaries; Domain/application sync/pure by default;
- one AsyncSession per concurrent task/use-case;
- application boundary owns transaction;
- Alembic authority/autogenerate candidate only/applied revisions immutable;
- schema drift checked;
- risk classification and staged/online PostgreSQL techniques;
- expand → migrate → contract;
- large backfills resumable/idempotent/bounded;
- separated DB privilege classes;
- logical-copy path distinct from pgBackRest/WAL/PITR recovery;
- raw PROD→DEV forbidden by default; production-derived lower data sanitized/minimized.

### Config/secrets

- pydantic-settings typed/fail-fast immutable bootstrap config;
- safe `.env.example` + ignored LOCAL `.env.local`;
- minimize secrets → workload identity → provider secret manager → least privilege → rotation/revocation/audit;
- GitHub OIDC preferred future cloud identity;
- independent environment/workload credentials.

### Testing/CI

- real PostgreSQL integration, never SQLite as PostgreSQL proof;
- unit/application/property/state-machine/architecture/migration/concurrency/provider/API/privacy layers;
- PR/DEV/nightly/UAT tiers;
- no arbitrary pre-code coverage floor;
- GitHub Actions primary CI/CD;
- real-check-before-required-check;
- least privilege + SHA-pinned protected Actions;
- dependency/CodeQL/secret controls when applicable;
- GitHub-hosted runner initially;
- future build-once/promote + attestation/SBOM release posture.

## 7. Frontend Engineering Foundation — closed design / integrated via PR #22

Durable authorities are now integrated on `main`:

- `docs/architecture/frontend-engineering-foundation.md`;
- `docs/architecture/frontend-engineering-foundation-part-2.md`;
- `docs/architecture/frontend-engineering-foundation-final-review.md`;
- `docs/architecture/frontend-engineering-foundation-post-closure-qa.md`;
- `docs/decisions/ADR-008-frontend-engineering-stack.md`;
- `docs/decisions/ADR-009-frontend-architecture-boundaries.md`;
- `docs/workstreams/frontend-foundation.md`.

Protected-main integration completed through PR #22 at merge commit `9116cd508d372cd56cf00403aa59633589b2d365`. The former `feature/frontend-foundation` branch was merged and auto-deleted.

### Technology baseline

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x
React 19.2 + Vite 8 + TanStack Router
React Native 0.86 + Expo SDK 57 + Expo Router
PowerSync + encrypted SQLite
TanStack Query 5
TanStack Form
Zod 4
Orval 8
```

### Structural posture

- feature-first Web/Mobile;
- route/navigation adapters thin;
- public-API-only and acyclic dependencies;
- small real-consumer shared packages;
- framework-free shared cores by default;
- Data Authority Matrix before ambiguous data implementation;
- canonical accepted effects backend/PostgreSQL only;
- feature data firewall;
- Mobile PowerSync app-owned initially;
- Web online-first / PowerSync Web dormant;
- browser PWA/service worker dormant;
- identity-scoped local data;
- React-free shared i18n;
- versioned validated Web runtime public config;
- exactly LOCAL/DEV/UAT/PROD;
- Android+iOS supported targets with release gates when activated;
- pnpm isolated preferred/direct-validation-required, hoisted evidence fallback;
- WSL single-checkout posture, native bridge direct-validation required.

### Final review

Passo 3 repaired repository-layout inheritance, feature-cycle enforcement and stale CURRENT documentation/governance.

```text
BLOCKING ARCHITECTURE DEFECTS        0
DOMAIN/LOGICAL/PHYSICAL REOPENS      0
CANONICAL AUTHORITY CONFLICTS        0
REPOSITORY-LAYOUT CONFLICTS          0 after repair
FEATURE CYCLES ALLOWED               NO
FALSE DIRECT PASS CLAIMS             0
CURRENT-TRUTH CLOSURE BLOCKERS       0 after repair
```

## 8. Direct-validation truth

Never claim these passed:

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS          NOT STARTED
DIRECT HG-01..HG-12      NOT RUN
DIRECT HG PASS           0
LOW/BASE/HIGH            NOT RUN
RESTORE REHEARSAL        NOT RUN
MIGRATION REHEARSAL      NOT RUN
FAILURE INJECTION        NOT RUN
POWERSYNC DIRECT TEST    NOT RUN
RESTATE DIRECT TEST      NOT RUN
OBJECT RECOVERY TEST     NOT RUN
SOLVER DIRECT TEST       NOT RUN
FRONTEND DIRECT TEST     NOT RUN
VERIFIED-RUN SCORE       NOT AVAILABLE
```

Frontend direct obligations move to the fresh post-integration materialization scope. Failure first reopens affected technology/adapter unless wider contradiction is proven.

## 9. Current repository branches/workstreams

- Frontend Engineering Foundation — **DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**; former `feature/frontend-foundation` branch merged/auto-deleted;
- separate prototype/UX workstreams remain non-production evidence;
- Engineering Foundation v0 closed;
- frontend/backend production scaffolds not started by the Foundation workstreams.

## 10. Exact next action

```text
FRONTEND
open a fresh bounded materialization/scaffold/direct-validation workstream
→ materialize only accepted real workspace/app/package artifacts
→ execute carried validation obligations progressively
→ do not implement product surfaces until relevant foundation/contracts exist
```

Backend production scaffold remains separate/not started and requires its own bounded gate.

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Frontend Foundation decisions without concrete contradictory evidence or a materially changed requirement.
