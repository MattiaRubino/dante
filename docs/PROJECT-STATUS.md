# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED
Whole-Domain PASS WITH HARDENING

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING
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
PENDING MAIN INTEGRATION
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

Important invariants include life central rather than task/calendar centric; planned vs actual preserved; user authority/authorship; material history/provenance; privacy; honest uncertainty; progressive complexity; personal-first not personal-only; AI not product authority; possibility != decision/action/preference; Effort != Execution != Outcome != Goal Progress.

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

## 4. Accepted Physical target

PostgreSQL 18.4 remains sole canonical persistence/material-history authority.

Selected database capability envelope remains PostGIS, pgvector, native FTS, pg_trgm, unaccent, pg_stat_statements and PgBouncer target posture.

Offline/sync remains PowerSync + encrypted SQLite bounded local/noncanonical state:

```text
SQLite local copy != canonical truth
PowerSync arrival order != conflict resolution
offline capability = operation-specific
local pending mutation != canonical effect
consequential offline mutation → backend governance/revalidation → PostgreSQL
```

Class-A async, Restate Class-B target, object, recovery, solver and observability decisions remain unchanged and activate only at accepted boundaries.

## 5. Closed Engineering Foundation v0

Repository root ownership reserves one monorepo with:

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

Paths are materialized only when real content exists.

Backend baseline remains Python 3.14.x/uv/Ruff/mypy/pytest/Hypothesis, WSL2/Linux, Docker Compose, PostgreSQL 18.4, SQLAlchemy/psycopg/Alembic, typed config, real-PostgreSQL testing and GitHub Actions/protected-main supply-chain posture.

## 6. Frontend Engineering Foundation — closed design pending integration

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

### Architecture baseline

- Web/Mobile feature-first;
- thin router/navigation adapters;
- public-API-only and acyclic dependency direction;
- app-local UI/platform boundaries;
- only real-consumer shared packages;
- framework-free shared client cores by default;
- formal Data Authority Matrix;
- backend/PostgreSQL canonical accepted-effect authority;
- feature data firewall;
- Mobile PowerSync app-owned initially;
- Web online-first / PowerSync Web dormant;
- browser PWA/service worker dormant;
- identity-scoped local data;
- React-free shared i18n core;
- Temporal time boundary;
- versioned/fail-fast Web runtime public config;
- LOCAL/DEV/UAT/PROD only;
- GitHub Actions primary CI/CD;
- WSL single-checkout developer posture with native bridge direct-validation obligation.

### Passo-3 review

Final review repaired root-topology inheritance, feature-cycle policy and stale current documentation/governance before closure.

Result:

```text
BLOCKING ARCHITECTURE DEFECTS        0
DOMAIN/LOGICAL/PHYSICAL REOPENS      0
CANONICAL AUTHORITY CONFLICTS        0
REPOSITORY-LAYOUT CONFLICTS          0 after repair
FALSE DIRECT PASS CLAIMS             0
CURRENT-TRUTH CLOSURE BLOCKERS       0 after repair
```

Final review authority: `docs/architecture/frontend-engineering-foundation-final-review.md`.

## 7. Direct-validation truth

```text
DATABASE DEPLOYMENT      NOT STARTED
BACKEND SCAFFOLD         NOT STARTED
FRONTEND SCAFFOLD        NOT STARTED
DIRECT HG                NOT RUN
FRONTEND DIRECT TEST     NOT RUN
POWERSYNC DIRECT TEST    NOT RUN
RESTORE REHEARSAL        NOT RUN
PRODUCTION DEPLOYMENT    NOT STARTED
```

Frontend direct validations move to post-integration materialization. A failure first reopens the affected technology/adapter/boundary unless evidence proves wider inconsistency.

## 8. Current repository workstreams

- `feature/frontend-foundation` — design/architecture **CLOSED / ACCEPTED / FINAL REVIEW PASS / PENDING MAIN INTEGRATION**;
- prototype/UX work remains separate evidence and does not authorize production implementation;
- backend production scaffold remains separate and not started.

## 9. Exact next action

```text
FRONTEND
prepare PR / protected-main integration
only with explicit authorization
↓
after integration create a fresh materialization/scaffold scope
↓
execute direct validations progressively

BACKEND
separate production scaffold scope remains NOT STARTED
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Frontend Foundation decisions without concrete contradictory evidence or a materially changed requirement.
