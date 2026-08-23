# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current state

```text
PRODUCT / NORTH STAR                 CURRENT
DOMAIN MODEL                         CLOSED
LOGICAL MODEL                        CLOSED / WL-H01..WL-H12 ACTIVE
PHYSICAL TARGET                      CLOSED / SELECTED / ACCEPTED
ENGINEERING FOUNDATION v0            CLOSED / ACCEPTED
FRONTEND ENGINEERING FOUNDATION      CLOSED / ACCEPTED / INTEGRATED VIA PR #22
PRODUCTION BACKEND SCAFFOLD          CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24
FRONTEND MATERIALIZATION             CLOSED / PASS — FM-00..FM-07
FRONTEND INTEGRATION HARDENING       ACTIVE — PR #28
CONCRETE LOGICAL -> POSTGRESQL        NOT STARTED
PRODUCT VERTICALS                    NOT STARTED
PRODUCTION DEPLOYMENT                NOT STARTED
```

Architecture/design closure never implies implementation PASS. Direct PASS is recorded only for the exact artifact/scenario that actually ran.

## Repository direction

DANTE remains one product monorepo:

```text
apps/
├── backend/
├── web/
└── mobile/
packages/
infra/
tooling/
tests/system/
docs/
prototypes/
.github/
```

These are ownership boundaries, not instructions to create empty directories. Production code never imports from `prototypes/`. `main` is the only integrated source truth; normal work uses bounded branches and PR integration.

## Backend engineering baseline

```text
Python                 3.14.x
current scaffold pin   3.14.7
package manager        uv 0.12.5 exact project requirement
format/lint            Ruff
type checking          mypy strict
tests                  pytest + Hypothesis where meaningful
persistence            PostgreSQL 18.4
ORM/SQL toolkit        SQLAlchemy 2.0 stable
PostgreSQL driver      psycopg 3
migrations             Alembic
```

The integrated LOCAL PostgreSQL scaffold directly proved PostgreSQL 18.4, PostGIS 3.6.4, pgvector 0.8.6, `pg_trgm`, `unaccent`, `pg_stat_statements`, least-privilege role provisioning, migrations, real readiness and real PostgreSQL acceptance. Detailed CP1-CP5 evidence lives in `docs/workstreams/backend-scaffold.md` and the backend development contracts.

## Frontend engineering baseline — materialized

The closed frontend materialization directly qualified the following baseline at its stated scopes:

```text
Node                    24.19.0
pnpm                    11.22.0
TypeScript              6.0.3 strict
Turborepo               2.10.11
ESLint                  10.8.1
Prettier                3.9.0

Web
React / React DOM       19.2.8 / 19.2.8
Vite                    8.2.1
TanStack Router         1.170.31
Playwright              1.62.1

Mobile
Expo SDK                57.x (clean resolution 57.0.15)
React Native            0.86.2
React                   19.2.3
Expo Router             57.x (clean resolution 57.0.15)
Gesture Handler         2.32.0
Reanimated              4.5.1

Shared
@dante/design-tokens    DTCG/Terrazzo-backed
@dante/i18n             i18next 26.3.6; IT primary/fallback, EN secondary
@dante/time             temporal-polyfill 1.0.4
```

`selected != installed != configured != directly validated` remains the governing rule. The design-time Frontend Foundation remains architecture authority; where version-specific design text differs from later direct materialization evidence, the qualified materialization evidence and later ADR/current-decision reconciliation are authoritative for the implemented baseline.

The only known workspace peer diagnostic is Web `react-dom@19.2.8` observing Mobile React `19.2.3`. Expo `install --check` passes with Mobile React 19.2.3, so the diagnostic is reproducible/non-blocking and is not a reason for React, hoisting or peer-suppression changes.

## Frontend direct evidence

The closed materialization proved, among other things:

```text
fresh frozen pnpm install                     PASS
strict TypeScript                             PASS
architecture graph                            36 modules / 45 deps / 0 violations
generated-source drift                        PASS
unit tests                                    10 PASS
Web production build                          PASS
Web Chromium production-preview E2E           PASS
Android Hermes bundle smoke                   PASS
Android emulator / Metro / Hermes runtime     PASS (FM-04)
Expo dependency compatibility                 PASS
fresh Playwright browser bootstrap            PASS
tracked + untracked repository cleanliness    PASS
GitHub-hosted Frontend CI                     PASS
```

The detailed evidence authority is `docs/workstreams/frontend-materialization.md`.

## Combined integration candidate — PR #28

`chore/frontend-materialization-integration` was created from current `main` and preserves the closed frontend history through a real merge parent. The integration hardening adds Mobile `src/**` TypeScript coverage, Expo compatibility CI, untracked-residue CI checks, a stable `Frontend CI Gate`, least-privilege workflow permissions, pnpm minimum-release-age policy and npm/pnpm Dependabot coverage.

On candidate `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06`, the real PR observed:

```text
Dependency Review    PASS
Backend CI           PASS
Frontend CI          PASS
Quality              PASS
Web E2E              PASS
Mobile Bundle        PASS
Frontend CI Gate     PASS
```

Dependency Review remains fail-closed at `moderate+`. Three exact transitive tooling advisories are temporarily accepted and documented with a review deadline of **2026-09-23**; this is not a global vulnerability suppression.

## Protected-main enforcement

Current `main` protection requires:

```text
Backend CI Gate
Dependency Review
branch up to date before merge
PR-before-merge
review-thread resolution
no force push / no deletion
```

`Frontend CI Gate` now exists and has real green PR evidence, but is **not required on main yet**. Promotion requires deliberate-red failure-propagation proof and recovery-green proof first, followed by a separate explicit ruleset mutation.

## Selected but not yet activated

The following remain selected/deferred rather than silently implemented: PowerSync + encrypted SQLite, TanStack Query/Form, Orval-generated API client, Web runtime config/Cloudflare delivery, Sentry, EAS release services, CodeQL, browser PWA/offline, production recovery/remote deployment and specialist scale infrastructure.

Activation triggers are recorded in `docs/workstreams/frontend-materialization-integration.md`.

## Environment model

```text
LOCAL -> DEV -> UAT -> PROD
```

Environments are runtime contexts, never Git branches.

## Where to continue

Read in order:

1. `docs/README.md`
2. `docs/PROJECT-STATUS.md`
3. `docs/development/repository-engineering-safety.md`
4. the active workstream handoff
5. the applicable closed architecture/ADR/model authorities.

Current integration boundary:

```text
PR #28 integration hardening
-> reconcile CURRENT documentation
-> deliberate-red / recovery-green Frontend CI Gate calibration
-> optional separate required-check promotion
-> final PR review / protected-main merge authorization
```

Backend next remains a separate bounded workstream for Concrete Logical -> PostgreSQL. Product vertical work begins only after its required data/API/UI boundaries are deliberately activated; do not reopen closed foundations by default.