# DANTE — Project Status

- Status: **CURRENT TRUTH**
- Product: **DANTE**
- Frontend Foundation integration: PR `#22` — **MERGED / VERIFIED**
- Backend scaffold integration: PR `#24` — **MERGED / VERIFIED**
- Frontend materialization: `feature/frontend-materialization` — **CLOSED / PASS**
- Current pending integration: `chore/frontend-materialization-integration` — PR `#28` **ACTIVE / READY / FINAL MERGE GATE**

## 1. Executive state

```text
PRODUCT / NORTH STAR                  CURRENT
DOMAIN MODEL                          CLOSED
LOGICAL MODEL                         CLOSED / WL-H01..WL-H12 ACTIVE
PRE-PHYSICAL COHERENCE                CLOSED / FINAL QA PASS
PHYSICAL TARGET                       CLOSED / SELECTED / ACCEPTED
ENGINEERING FOUNDATION v0             CLOSED / ACCEPTED
FRONTEND ENGINEERING FOUNDATION       CLOSED / ACCEPTED / INTEGRATED VIA PR #22
PRODUCTION BACKEND SCAFFOLD           CLOSED / DIRECT QA PASS / INTEGRATED VIA PR #24
FRONTEND MATERIALIZATION              CLOSED / PASS — FM-00..FM-07
FRONTEND INTEGRATION HARDENING        ACTIVE — PR #28 / READY / FINAL MERGE GATE
FRONTEND CI GATE CALIBRATION          COMPLETE
FRONTEND CI GATE PROMOTION            OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE
CONCRETE LOGICAL -> POSTGRESQL         NOT STARTED
PRODUCT VERTICAL IMPLEMENTATION       NOT STARTED
PRODUCTION DEPLOYMENT                 NOT STARTED
```

Architecture/design closure does not imply implementation PASS. Direct evidence is scoped to the artifact/scenario that actually ran.

## 2. Product and semantic invariants

DANTE is a personal operating system designed to help people understand, organize and improve real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

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

WL-H01..WL-H12 remain active.

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

One product monorepo remains authoritative. Backend is a capability-first modular monolith. Web and Mobile are sibling platform-specific clients with selective semantic sharing. Production code never imports from `prototypes/`.

## 5. Backend scaffold — CLOSED / integrated

Detailed authority: `docs/workstreams/backend-scaffold.md`.

Direct integrated evidence includes:

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

Concrete business schema remains NOT STARTED.

## 6. Frontend materialization — CLOSED / PASS

Detailed authority: `docs/workstreams/frontend-materialization.md`.

Qualified baseline:

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
strict TypeScript                            PASS
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

Known workspace peer diagnostic remains reproducible/non-blocking: Web `react-dom@19.2.8` observes workspace Mobile React `19.2.3`, while Expo compatibility directly passes for Mobile React 19.2.3. No React forcing, peer suppression, packageExtensions, hoisting or nodeLinker workaround is authorized merely to silence it.

## 7. Materialization qualification of design-time selections

Current reconciled implementation authority:

```text
Temporal implementation      temporal-polyfill 1.0.4
Gesture Handler              2.32.0 under Expo SDK 57
Web E2E path                 apps/web/e2e/
Mobile React                 19.2.3 under Expo SDK 57
Web React / React DOM        19.2.8 / 19.2.8
```

This qualifies version-specific implementation evidence without reopening the full frontend architecture.

## 8. PR #28 integration-hardening state

Integration branch:

```text
chore/frontend-materialization-integration
```

The branch starts from current `main` and preserves closed frontend history through a real two-parent merge.

Hardening materialized:

- Mobile TypeScript explicitly includes `src/**/*.ts(x)`;
- reusable Expo compatibility CI gate;
- tracked + untracked repository-mutation check;
- aggregate `Frontend CI Gate`;
- workflow least privilege;
- pnpm `minimumReleaseAge = 1440` minutes;
- npm/pnpm Dependabot scope;
- exact/time-bounded Dependency Review exceptions;
- CURRENT documentation reconciliation;
- version-specific Foundation/materialization reconciliation.

PR #28 is READY. The directly observed pre-reconciliation head `bdd6e08cbca4c19989502235855d52a620d29fb5` was current with `main`, mergeable, review-thread clean and green. Any subsequent documentation-only head must independently satisfy the same exact-head gates before merge authorization.

## 9. Frontend CI Gate calibration — COMPLETE

### Real green

Commit `79b55b3a1986cc910af0ce84df411314e8453e80`:

```text
Dependency Review   PASS
Backend CI Gate     PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

### Deliberate red

Commit `6491b0dfdf4d6d005017b4a1f9a021976a0b9ff8`:

```text
Quality             FAILURE — intentional
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    FAILURE — mandatory failure propagated
Backend CI          PASS
Dependency Review   PASS
```

### Recovery green

Commit `02ee9034f37000819afb2c27b0bd826b128f69b5` restored exact workflow blob `14626e696d91d3f184b58dac111cd88102832e91` and observed:

```text
Dependency Review   PASS
Backend CI          PASS
Backend CI Gate     PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

Therefore `Frontend CI Gate` is directly calibrated.

## 10. Protected-main ruleset promotion state

The branch-local canonical ruleset definition contains:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
source: GitHub Actions
Frontend CI Gate integration_id: 15368
```

It preserves branch-up-to-date enforcement, PR-before-merge, zero required approvals, review-thread resolution, merge-commit policy, deletion protection and force-push protection.

The repository owner confirmed applying the `Frontend CI Gate` promotion in the GitHub ruleset UI. The GitHub connector available to this workstream does not expose direct ruleset readback, therefore the setting is classified:

```text
Frontend CI Gate GitHub ruleset setting   OWNER-CONFIRMED APPLIED
Direct ruleset API readback               UNAVAILABLE
```

This administrative evidence boundary is kept explicit; it does not replace or weaken the direct green/red/recovery calibration evidence of the emitted check.

## 11. Dependency Review accepted-risk register

Dependency Review remains fail-closed at `moderate+` for runtime/development/unknown scopes.

Only these exact transitive tooling advisories are temporarily allowed:

```text
GHSA-5p2g-fcmc-qvqq
GHSA-w3rx-r6r6-pgpr
GHSA-w5hq-g745-h8pq
```

Review deadline: **2026-09-23**.

Detailed paths, exposure and removal triggers: `docs/workstreams/frontend-materialization-integration.md`.

## 12. Current non-claims

```text
CodeQL active                                  NO
PowerSync runtime integrated                   NO
Orval API client materialized                  NO
TanStack Query product usage                   NO
TanStack Form product usage                    NO
Sentry active                                  NO
Cloudflare Web deployment active               NO
EAS release pipeline active                    NO
iOS direct build/device validation             NO
Concrete business DB schema                    NO
Access/Home production vertical                NO
PROD deployment                                NO
```

## 13. Future activation register

The trigger-based future capability register is maintained in `docs/workstreams/frontend-materialization-integration.md`. Consult it at the first real product vertical, UI/design-system surface, form, remote API, offline operation, shared deployment, Mobile release, post-integration security step, pre-PROD maturity step and scale-triggered infrastructure decision.

Do not install placeholder infrastructure merely because larger applications often use it later.

## 14. Exact next actions

```text
FRONTEND INTEGRATION
1. require hosted CI green on the exact current PR #28 head
2. require branch current with main
3. require PR mergeable and review-thread clean
4. confirm accepted-risk register remains valid
5. obtain separate protected-main merge authorization

BACKEND NEXT
Concrete Logical -> PostgreSQL
-> fresh bounded workstream/gate

PRODUCT NEXT AFTER FOUNDATIONAL INTEGRATION
first real vertical slice
-> activate only capability/testing/lint boundaries actually consumed
```

Do not reopen closed Product/Domain/Logical/Physical/Engineering/Foundation or CP1-CP5 decisions without concrete contradictory evidence.
