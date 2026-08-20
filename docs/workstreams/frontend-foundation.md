# Workstream — Frontend Engineering Foundation

- Status: **DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS / PENDING MAIN INTEGRATION**
- Branch: `feature/frontend-foundation`
- Opening base: `7a1600c2167f68c9281d3ed77b32a3d954fbd061`
- Passo-1 checkpoint: `dd23b86ba330f6296806297ef5c68acebbee65e6`
- Passo-2 initial checkpoint: `0269672b6f1cd085fa935d400b774b098feb4c69`
- Final-reviewed pre-closure HEAD: `28630c8d8a1133b785850de804d3a37495e0b3c8`
- PR: **NONE**
- Product/Domain/Logical/Physical/Engineering Foundation: **CONSUMED / NOT REOPENED**
- Production frontend code/scaffold: **NOT STARTED**
- Dependencies installed/configured: **NO**
- Direct frontend validation: **NOT RUN**

## 1. Workstream contract and result

Three substantial passes only:

```text
PASSO 1  technology selection                        PASS
PASSO 2  application/package/data architecture       PASS
PASSO 3  clean review / closure                      FINAL REVIEW PASS
```

Frontend Foundation is closed at **design/architecture level**. It remains unmerged until protected-main integration.

```text
DESIGN CLOSED
!= IMPLEMENTED
!= INSTALLED
!= CONFIGURED
!= DIRECTLY VALIDATED
```

## 2. Durable authorities

- `../architecture/frontend-engineering-foundation.md` — Passo 1;
- `../architecture/frontend-engineering-foundation-part-2.md` — Passo 2;
- `../architecture/frontend-engineering-foundation-final-review.md` — Passo 3 closure evidence;
- `../decisions/ADR-008-frontend-engineering-stack.md` — technology ADR;
- `../decisions/ADR-009-frontend-architecture-boundaries.md` — architecture ADR;
- closed Engineering Foundation/repository layout;
- accepted Physical target/register;
- closed Product/Domain/Logical authorities.

`main` remains integrated truth. These frontend sources are pending-integration branch authority until merge.

## 3. Accepted technology baseline

```text
Node 24 LTS
TypeScript 6.0.x strict
pnpm 11
Turborepo 2.x

Web
React 19.2 + React DOM
Vite 8
TanStack Router

Mobile
React Native 0.86
Expo SDK 57
Expo Router

Data/state
PowerSync + encrypted SQLite
@powersync/react
TanStack Query 5
Zustand specialist/dormant
TanStack Form
Zod 4

API
FastAPI OpenAPI → Orval 8
```

Complete UI/testing/release selection remains in Passo 1.

## 4. Accepted architecture baseline

### Root/application ownership

Frontend inherits accepted repository ownership:

```text
apps/
packages/
infra/
tooling/
tests/system/
docs/
prototypes/
.github/
```

No empty ceremonial directories.

### Feature/dependency architecture

- Web/Mobile feature-first;
- thin route/navigation adapters;
- bootstrap composition only;
- app-local UI/platform boundaries;
- public-API-only cross-boundary imports;
- feature dependency cycles forbidden;
- no generic dumping grounds;
- no production prototype imports.

### Shared packages

Initial real shared candidates:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

API client only with real OpenAPI; shared feature packages only after real Web+Mobile reuse. Shared cores framework-free by default and never own canonical backend/domain authority.

### Workspace/tooling

- private workspace-only packages;
- `workspace:*`;
- controlled package `exports`;
- source-first TS default;
- workspace/feature cycles forbidden;
- pnpm isolated preferred/direct-validation-required;
- evidence-driven hoisted fallback allowed.

### Data Authority Matrix

```text
canonical accepted effect   backend/PostgreSQL
synced local projection     PowerSync/SQLite noncanonical
offline pending mutation    local staging only
offline acceptance          backend governance/conflict checks
remote request state        TanStack Query + typed API
online governed command     FastAPI/backend
route state                 router
form draft                  TanStack Form
component transient         React
cross-tree transient        Zustand only when justified
```

Offline operation = staging → upload → backend accept/reject → reconciliation. Local staging never canonical.

### Data/offline/session

- feature data/model firewall;
- no universal frontend Repository;
- Mobile PowerSync app-owned initially;
- Web online-first / PowerSync Web dormant;
- browser PWA/SW dormant;
- identity-scoped local DB;
- app-local session adapters;
- no invented AuthN token/cookie contract.

### UI/shared semantics/config

- separate DANTE Web/Native UI implementations;
- shared semantic tokens with platform-specific representation;
- React-free `@dante/i18n`;
- Temporal `@dante/time`;
- deterministic generated runtime source/drift checks;
- versioned/Zod-validated Web public runtime config;
- exactly LOCAL/DEV/UAT/PROD.

### Release/CI/developer posture

- Android+iOS supported targets; gates apply when activated;
- GitHub Actions primary CI/CD;
- Turbo JS/frontend graph only;
- no guessed required checks;
- one authoritative WSL-backed checkout;
- WSL↔Windows Android/Metro direct-validation adapter;
- EAS Build/Submit/Update selected; Workflows optional/dormant.

## 5. Passo-3 final review

Clean review found and repaired before closure:

1. repository-layout inheritance (`infra/`, `tooling/`, `tests/system`);
2. missing explicit feature-cycle prohibition;
3. stale CURRENT status/roadmap/architecture summaries;
4. stale CURRENT governance continuation.

Final result:

```text
BLOCKING ARCHITECTURE DEFECTS          0
DOMAIN/LOGICAL/PHYSICAL REOPENS        0
CANONICAL AUTHORITY CONFLICTS          0
REPOSITORY LAYOUT CONFLICTS            0 after repair
FEATURE-CYCLE LOOPHOLE                 CLOSED
FALSE DIRECT PASS CLAIMS               0
STALE CURRENT CLOSURE BLOCKERS         0 after repair
```

Full evidence: `../architecture/frontend-engineering-foundation-final-review.md`.

## 6. Direct-validation obligations carried forward

Still **NOT RUN**. Materialization must progressively validate:

- Node/pnpm/Turbo real workspace;
- preferred isolated native dependency graph / hoisted fallback only if evidenced;
- Vite production build;
- Expo/RN active targets;
- strict TS package graph;
- exports/import/cycle enforcement;
- deterministic tokens;
- real OpenAPI→Orval when API exists;
- TanStack Form Web/RN/Zod;
- TanStack Query remote path;
- PowerSync/OP-SQLite/SQLCipher;
- offline accept/reject/conflict reconciliation;
- identity-scoped DB lifecycle;
- WSL↔Windows Android tooling;
- Web runtime config/Cloudflare when activated;
- selected tests;
- Sentry/EAS integrations when activated.

Failure first reopens affected technology/adapter/boundary unless wider contradiction is proven.

## 7. Git/continuation state

```text
OPENING BASE
7a1600c2167f68c9281d3ed77b32a3d954fbd061

PASSO 1
dd23b86ba330f6296806297ef5c68acebbee65e6

PASSO 2 INITIAL
0269672b6f1cd085fa935d400b774b098feb4c69

FINAL-REVIEWED PRE-CLOSURE HEAD
28630c8d8a1133b785850de804d3a37495e0b3c8
```

Final closure commit is the commit containing this handoff plus the Passo-3 final-review document; verify exact remote HEAD during closure QA.

## 8. Exact next action

```text
PENDING MAIN INTEGRATION

PR creation
ONLY with explicit authorization

merge
ONLY with explicit authorization + expected-head protection

post-merge
reread/compare main + verify branch lifecycle

then
new bounded frontend materialization/scaffold/direct-validation scope
```

Do not restart general frontend technology/architecture research without concrete contradictory evidence or a materially changed requirement.
