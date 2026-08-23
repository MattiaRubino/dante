# ADR-009: Frontend Application and Dependency Boundaries

- Status: **ACCEPTED / INTEGRATED VIA PR #22 / MATERIALIZED AT FM-00..FM-07 STATED SCOPES**
- Date: 2026-08-20
- Materialization qualification: 2026-08-23
- Technology authority: [`ADR-008-frontend-engineering-stack.md`](ADR-008-frontend-engineering-stack.md)
- Structural design specification: [`../architecture/frontend-engineering-foundation-part-2.md`](../architecture/frontend-engineering-foundation-part-2.md)
- Direct implementation evidence: [`../workstreams/frontend-materialization.md`](../workstreams/frontend-materialization.md)

## Context

ADR-008 selected the technology family. DANTE also needs ownership/dependency rules that survive library upgrades and remain consistent with the accepted monorepo topology.

Without explicit boundaries, the frontend could collapse into a client monolith where routes own feature logic, Web/Mobile leak platform details, shared packages become dumping grounds, state authorities duplicate or local/offline mechanisms silently replace backend authority.

The architecture decision was integrated via PR #22. The later materialization workstream directly proved the executable package/app boundaries that exist today.

## Decision

### 1. Root repository ownership

Frontend does not redefine the Engineering Foundation root topology:

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

Paths exist only for real content. `infra/` owns infrastructure definitions, not business logic.

### 2. Application boundaries

Keep sibling deployables:

```text
apps/backend
apps/web
apps/mobile
```

Web and Mobile are first-class platform-specific clients with selective semantic sharing, not one forced renderer.

### 3. Feature-first architecture

Web and Mobile use vertical `features/<capability>` ownership when product features exist. Routes/navigation are adapters. Platform integrations are app-local `platform/`; DANTE UI implementations are app-local `ui/`; assembly belongs to bootstrap.

Do not create empty architecture directories merely to satisfy the conceptual model.

### 4. Public APIs and acyclic direction

Cross-boundary dependencies use public APIs only. Bootstrap/router are not deep-import backdoors.

Feature/package dependencies must remain acyclic. Cycles require boundary/orchestration repair rather than import exceptions.

### 5. Shared-package extraction

Shared packages exist only for real multi-consumer semantics.

Current genuine shared packages:

```text
@dante/design-tokens
@dante/i18n
@dante/time
```

`@dante/api-client` appears only with real OpenAPI. Shared feature packages require actual Web+Mobile reuse. Shared cores remain framework/platform-free by default and never own canonical Domain/AuthZ/conflict/persistence/accepted-effect authority.

### 6. Data Authority Matrix

```text
canonical accepted state/effects   backend + PostgreSQL
synced local projection            PowerSync/SQLite when activated
offline pending mutation           local staging only
offline acceptance                 backend governance/conflict checks
remote request state               TanStack Query when activated
form state                         TanStack Form when activated
component transient                React
cross-tree transient               Zustand only when justified
```

### 7. Feature data firewall

Feature UI consumes feature-specific data/model boundaries instead of directly owning HTTP, PowerSync, query cache or storage details. No universal frontend `Repository<T>`.

### 8. Web/Mobile offline posture

Mobile may activate PowerSync + encrypted SQLite at the first real offline operation.

Web starts online-first. PowerSync Web and browser PWA/service-worker behavior remain dormant until explicitly justified.

### 9. Package-manager layout

pnpm isolated layout is preferred and has been directly validated with the current Expo/native graph. Hoisting/nodeLinker changes are evidence-driven fallback only, not a default workaround.

### 10. Platform-neutral shared cores

Shared i18n/time/API contracts/pure feature cores remain framework/platform-free by default. React/RN integration belongs to app bootstrap/platform/UI boundaries.

### 11. Runtime configuration

Versioned validated public Web runtime configuration activates when a shared DEV/Web deployment exists. A delivery/bootstrap Worker may serve bounded public config but is not a DANTE BFF/business backend.

### 12. Environment vocabulary

Exactly:

```text
LOCAL
DEV
UAT
PROD
```

### 13. Platform release activation

Android and iOS are architectural targets. Signed build/device/store gates apply only when a platform is an activated release target. Android direct runtime evidence exists today; iOS direct release validation does not.

### 14. Developer topology

One authoritative WSL-backed source checkout remains the supported Windows posture. WSL<->Windows Metro/ADB details are tooling adapters, not product architecture.

## Materialization evidence

Executable architecture enforcement currently rejects:

- unresolved production imports;
- source dependency cycles;
- Web -> Mobile;
- Mobile -> Web;
- shared -> apps;
- production -> prototypes;
- framework/platform imports from shared cores.

Direct graph evidence:

```text
36 modules
45 dependencies
0 violations
```

Generated-source drift, strict TypeScript, Web build/E2E, Android bundle/runtime and shared-package consumers are also directly validated under the closed frontend materialization.

## Materialization qualification of conceptual structure

The Part-2 design remains the structural architecture authority, but materialization resolves concrete filesystem/tooling details where the design was intentionally conceptual.

Current implementation authority includes:

```text
Web E2E directory     apps/web/e2e/
Mobile TypeScript     app/** + src/** explicitly included
shared package root   package public exports; deep imports forbidden
source-first TS       current default for shared packages
```

The earlier example path `apps/web/tests/e2e/` is therefore not the current filesystem authority. `apps/web/e2e/` is the validated convention.

The current dependency rules operate at package/app level. Feature-public-API and app-local `ui/` / `platform/` rules must be extended when the first real product vertical creates enough real code for those boundaries to be meaningfully enforceable; do not build placeholder directories/rules against nonexistent structure.

## Consequences

Positive:

- framework/provider upgrades do not redefine product architecture;
- Web/Mobile stay platform-native;
- shared packages remain purposeful;
- state/data authority is explicit;
- architecture violations can fail locally/CI;
- future feature-level enforcement has a defined activation trigger.

Costs:

- public APIs and cycle rules require discipline;
- data authority must be classified before ambiguous implementation;
- some duplication is tolerated until real reuse justifies extraction;
- native/tooling boundaries retain direct-validation obligations.

## Current non-decisions / dormant capabilities

This ADR does not itself activate AuthN protocol, concrete backend routes, PowerSync runtime, browser PWA, Orval API generation, TanStack Query/Form product usage, Sentry, Cloudflare deployment, EAS release, CodeQL or product features.

Their activation triggers are recorded in `../workstreams/frontend-materialization-integration.md`.

## Validation/reopen rule

A failed native/tooling integration first reopens the affected adapter/layout choice. Core feature/dependency/data-authority architecture reopens only with evidence of a wider contradiction.

## Relationship to ADR-008

ADR-008 owns technology selection and version-qualified materialization. ADR-009 owns application/package/dependency/data-authority architecture. Neither supersedes the other.