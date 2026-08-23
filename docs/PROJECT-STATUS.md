# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**
- Protected-main backend integration: PR `#24` — **MERGED / VERIFIED**
- Frontend Foundation integration: PR `#22` — **MERGED / VERIFIED**
- Frontend materialization: `feature/frontend-materialization` — **CLOSED / PASS**
- Current pending integration: `chore/frontend-materialization-integration` — PR `#28` **ACTIVE / DRAFT**

## 1. Executive state

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL
CLOSED

LOGICAL MODEL
CLOSED
WL-H01..WL-H12 ACTIVE

PRE-PHYSICAL COHERENCE
CLOSED / FINAL QA PASS

PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED

ENGINEERING FOUNDATION v0
CLOSED / ACCEPTED

FRONTEND ENGINEERING FOUNDATION
CLOSED / ACCEPTED / FINAL REVIEW PASS
INTEGRATED VIA PR #22

PRODUCTION BACKEND SCAFFOLD
CLOSED / DIRECT QA PASS
INTEGRATED VIA PR #24
CP1..CP5 CLOSED AT THEIR STATED SCOPES

FRONTEND MATERIALIZATION
CLOSED / PASS
FM-00..FM-07 COMPLETE AT THEIR STATED SCOPES

FRONTEND INTEGRATION HARDENING
ACTIVE / PR #28
CURRENT candidate CI GREEN before this documentation-reconciliation commit

CONCRETE LOGICAL -> POSTGRESQL
NOT STARTED

PRODUCT VERTICAL IMPLEMENTATION
NOT STARTED

PRODUCTION DEPLOYMENT
NOT STARTED
```

Architecture/design closure does not imply implementation PASS. Direct evidence is scoped to the artifact/scenario that actually ran.

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

## 3. Canonical architecture truth

```text
PostgreSQL 18.4
SOLE CANONICAL PERSISTENCE + MATERIAL-HISTORY AUTHORITY
```

Selected PostgreSQL capabilities include PostGIS 3.6.4, pgvector 0.8.6, native FTS, `pg_trgm`, `unaccent`, `pg_stat_statements` and bounded PgBouncer activation.

Selected specialist targets such as PowerSync + encrypted SQLite, Restate, R2, pgBackRest/S3, OR-Tools and remote observability remain noncanonical and activate only when their real boundary exists.

## 4. Repository / application ownership

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

One product monorepo remains authoritative. Paths exist only for real content. Production code does not import from `prototypes/`.

Backend remains a capability-first modular monolith. Web and Mobile are sibling platform-specific clients with selective semantic sharing.

## 5. Backend scaffold — CLOSED / integrated

Detailed authority: `docs/workstreams/backend-scaffold.md`.

Integrated evidence includes:

```text
Python 3.14.7 / uv 0.12.5                 PASS
Ruff / mypy strict                        PASS
fast pytest                               32/32 PASS
PostgreSQL acceptance                     18/18 PASS
full backend pytest                       50/50 PASS
wheel + sdist                             PASS
PostgreSQL 18.4 LOCAL image               PASS
least-privilege DB provisioning           PASS
real Uvicorn startup                      PASS
/health/live                              200 PASS
/health/ready                             200 PASS
Backend CI green/red/recovery calibration PASS
protected-main merge PR #24               PASS
post-merge Backend CI                     PASS
```

Current protected-main required checks remain `Backend CI Gate` and `Dependency Review` with branch-up-to-date required.

Concrete business schema remains NOT STARTED.

## 6. Frontend materialization — CLOSED / PASS

Detailed authority: `docs/workstreams/frontend-materialization.md`.

Directly qualified implemented baseline:

```text
Node                     24.19.0
pnpm                     11.22.0
TypeScript               6.0.3 strict
Turborepo                2.10.11
React Web / React DOM    19.2.8 / 19.2.8
Vite                     8.2.1
TanStack Router          1.170.31
Expo SDK                 57.x / clean resolve 57.0.15
React Native             0.86.2
Mobile React             19.2.3
Gesture Handler          2.32.0
Reanimated               4.5.1
Vitest                   4.1.11
Playwright               1.62.1
temporal-polyfill        1.0.4
```

Direct evidence includes:

```text
fresh frozen install                          PASS
strict TS                                    PASS
architecture graph 36 modules / 45 deps      0 violations
generated-source drift                       PASS
@dante/time                                  5 PASS
@dante/i18n                                  5 PASS
Web production build                         PASS
Web Chromium E2E                             PASS
Android Hermes bundle smoke                  PASS
Android emulator/Metro/Hermes runtime        PASS
Expo install --check                         PASS
fresh browser bootstrap                      PASS
tracked/untracked residue                    0
GitHub-hosted Frontend CI                    PASS
```

Known peer diagnostic:

```text
Web react-dom@19.2.8 wants React ^19.2.8
workspace also contains Mobile React 19.2.3
Expo compatibility for Mobile React 19.2.3 PASS
classification: known / reproducible / non-blocking
```

No React version change, peer suppression, packageExtensions, hoisting or nodeLinker change is authorized merely to silence this diagnostic.

## 7. Materialization qualification of design-time selections

The Frontend Foundation remains the architecture/design authority. Later direct materialization evidence qualifies version-specific implementation details.

Current reconciled implementation authority:

```text
Temporal implementation      temporal-polyfill 1.0.4
Gesture Handler              2.32.0 under Expo SDK 57
Web E2E path                 apps/web/e2e/
Mobile React                 19.2.3 under Expo SDK 57
Web React / React DOM        19.2.8 / 19.2.8
```

This is a qualification of implementation evidence, not a reopening of the entire frontend architecture.

## 8. PR #28 integration-hardening state

Integration branch:

```text
chore/frontend-materialization-integration
```

The branch was created from current `main` and preserves the closed frontend materialization history through a real two-parent merge commit.

Hardening already materialized:

- Mobile TypeScript explicitly includes `src/**/*.ts(x)`;
- reusable `mobile:compat:check` / Expo compatibility gate;
- tracked + untracked CI repository-mutation check;
- stable aggregate `Frontend CI Gate`;
- workflow-level least privilege;
- pnpm `minimumReleaseAge = 1440` minutes;
- npm/pnpm Dependabot scope;
- narrow documented Dependency Review accepted-risk exceptions.

Real PR evidence on candidate `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06`:

```text
Dependency Review   PASS
Backend CI          PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

The documentation-reconciliation commit containing this file must earn its own PR CI before being treated as the final combined candidate.

## 9. Dependency Review accepted-risk register

Dependency Review remains fail-closed at:

```text
fail-on-severity: moderate
fail-on-scopes: runtime, development, unknown
```

Only these exact transitive tooling advisories are temporarily allowed:

```text
GHSA-5p2g-fcmc-qvqq
GHSA-w3rx-r6r6-pgpr
GHSA-w5hq-g745-h8pq
```

Review deadline: **2026-09-23**.

Detailed dependency paths, exposure classification and removal triggers live in `docs/workstreams/frontend-materialization-integration.md`. No global vulnerability suppression or severity reduction is authorized.

## 10. Current non-claims

```text
Frontend CI Gate required on main        NO
CodeQL active                             NO
PowerSync runtime integrated              NO
Orval API client materialized             NO
TanStack Query product usage              NO
TanStack Form product usage               NO
Sentry active                              NO
Cloudflare Web deployment active          NO
EAS release pipeline active               NO
iOS direct build/device validation        NO
Concrete business DB schema               NO
Access/Home production vertical           NO
PROD deployment                            NO
```

## 11. Future activation register

The trigger-based future capability register is maintained in `docs/workstreams/frontend-materialization-integration.md`. It must be consulted at the first real product vertical, UI/design-system surface, form, remote API, offline operation, shared deployment, Mobile release, post-integration security step, pre-PROD maturity step and scale-triggered infrastructure decision.

Do not install placeholder infrastructure simply because large applications often use it later.

## 12. Active workstreams / exact next actions

```text
CURRENT FRONTEND INTEGRATION
PR #28
-> current-truth reconciliation
-> PR CI green on reconciled candidate
-> deliberate-red Frontend CI Gate calibration
-> recovery green
-> separate required-check promotion decision
-> final review / merge authorization

BACKEND NEXT
Concrete Logical -> PostgreSQL
-> fresh bounded workstream/gate

PRODUCT NEXT AFTER FOUNDATIONAL INTEGRATION
first real vertical slice
-> activate only the capability/testing/lint boundaries actually consumed
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Foundation or CP1-CP5 decisions without concrete contradictory evidence.