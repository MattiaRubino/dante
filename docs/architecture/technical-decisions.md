# DANTE Technical Decisions

- Status: **CURRENT DECISION REGISTER**

Detailed rationale/constraints live in accepted Domain/Logical/Physical/Engineering/Frontend Foundation sources and ADRs.

## TD-01 — Canonical persistence
**ACCEPTED** — PostgreSQL 18.4 is sole canonical persistence/material-history authority. No separate graph/vector/search/event-store database is canonical by default.

## TD-02 — PostgreSQL capability envelope
**ACCEPTED** — PostGIS, pgvector, native FTS, pg_trgm, unaccent, pg_stat_statements and PgBouncer target posture. Full selected extension envelope is present from first LOCAL PostgreSQL baseline when materialized.

## TD-03 — Offline/sync
**ACCEPTED TARGET / NOT IMPLEMENTED** — PowerSync + encrypted SQLite bounded local state. SQLite/local pending state is noncanonical; offline capability is operation-specific; consequential offline mutation returns through backend governance/revalidation before PostgreSQL acceptance.

## TD-04 — Async/durable work
**ACCEPTED** — Class A PostgreSQL transactional outbox + bounded worker. Restate selected/dormant for Class B until a real durable workflow.

## TD-05 — Object bytes
**ACCEPTED TARGET / NOT IMPLEMENTED** — private EU Cloudflare R2 raw bytes when activated; PostgreSQL owns ContentArtifact authority/metadata/provenance/visibility/retention/hash/locator semantics.

## TD-06 — Recovery
**ACCEPTED TARGET / INITIALLY DORMANT** — pgBackRest + AWS S3 eu-south-1 + accepted Versioning/Object Lock GOVERNANCE posture + WAL/PITR. Recovery copies noncanonical; anti-resurrection active.

## TD-07 — Solver
**ACCEPTED TARGET / NOT IMPLEMENTED** — OR-Tools CP-SAT; `UNKNOWN != INFEASIBLE`; solver output candidate until governed acceptance.

## TD-08 — Observability
**ACCEPTED TARGET** — backend OpenTelemetry + Grafana Alloy + Grafana Cloud EU + pg_stat_statements; frontend Sentry behind bounded adapters when activated. Telemetry privacy-minimized/noncanonical.

## TD-09 — Repository strategy/root ownership
**ACCEPTED** — one DANTE monorepo in current repository. Root ownership reserves `apps`, `packages`, `infra`, `tooling`, `tests/system`, `docs`, `prototypes`, `.github`; paths appear only with real content. `infra` never owns business logic; production never imports prototypes.

## TD-10 — Backend architecture
**ACCEPTED** — capability-first modular monolith; no mechanical 57-owner module mapping; no universal CRUD repository/BaseService/service locator/global DB session; Domain/application independent of transport/ORM/provider; explicit composition; truthful cross-capability ACID when required.

## TD-11 — Frontend application architecture
**ACCEPTED / FRONTEND FOUNDATION FINAL REVIEW PASS / PENDING MAIN INTEGRATION** — Web React DOM/Vite/TanStack Router; Mobile RN/Expo/Expo Router; feature-first; route/navigation adapters thin; public-API-only and acyclic dependencies; app-local UI/platform; no prototype imports; executable architecture rules during materialization.

Shared packages require real multi-consumer semantics. Shared frontend cores are framework-free by default and never canonical Domain/AuthZ/conflict/persistence/accepted-effect authority.

## TD-12 — Frontend language/toolchain
**ACCEPTED / PENDING MAIN INTEGRATION** — Node 24 LTS, TypeScript 6.0.x strict, pnpm 11, Turborepo 2.x. Isolated pnpm layout preferred/direct-validation-required; evidence-driven hoisted fallback allowed. Turbo JS/frontend graph only; GitHub Actions remains repo CI/CD authority.

## TD-13 — Frontend data/state authority
**ACCEPTED / PENDING MAIN INTEGRATION** — canonical accepted state/effect backend+PostgreSQL; PowerSync/SQLite noncanonical projection/pending local state; TanStack Query request/response remote state; TanStack Form drafts; React transient; Zustand bounded cross-tree transient only. Feature UI uses data/model firewall; no universal frontend `Repository<T>`.

## TD-14 — Frontend offline posture
**ACCEPTED / PENDING MAIN INTEGRATION** — Mobile PowerSync+encrypted SQLite at materialization; Web online-first with PowerSync Web dormant; browser PWA/SW dormant. Local data identity scoped; cross-account leakage forbidden.

## TD-15 — Frontend API/codegen
**ACCEPTED / PENDING MAIN INTEGRATION** — FastAPI OpenAPI → Orval 8 → React-free/auth-storage-agnostic `@dante/api-client` when real OpenAPI exists. Generated runtime source deterministic/drift checked; Query ownership not forced on PowerSync-backed reads.

## TD-16 — Frontend UI/tokens/i18n/time
**ACCEPTED / PENDING MAIN INTEGRATION** — separate DANTE Web and Native UI layers; DTCG-compatible semantic tokens with platform outputs; `@dante/i18n` framework-free; `@dante/time` Temporal semantics.

## TD-17 — Frontend Web runtime config/delivery
**ACCEPTED / PENDING MAIN INTEGRATION** — versioned Zod-validated public runtime config; one immutable SPA artifact where platform permits; Cloudflare Workers Static Assets target; app-coupled config Worker not BFF/business backend.

## TD-18 — Mobile build/release
**ACCEPTED / PENDING MAIN INTEGRATION** — EAS Build/Submit/Update; EAS Workflows optional/dormant; Android/iOS supported targets with release gates applied when each target is activated.

## TD-19 — Backend language/runtime
**ACCEPTED** — Python 3.14.x (initial 3.14.7), uv, `apps/backend/src/dante`, Ruff, mypy strict, pytest, Hypothesis.

## TD-20 — Developer OS/workflow
**ACCEPTED / FRONTEND QUALIFIED** — backend Linux semantics; one authoritative WSL-backed checkout on Windows; JetBrains/PyCharm supported; frontend same checkout; WSL↔Windows Metro/ADB direct-validation adapter; no divergent cross-OS source clones/node_modules.

## TD-21 — LOCAL container/persistence toolkit
**ACCEPTED** — backend direct WSL/Linux inner loop, Docker Compose stateful LOCAL infra, future OCI server; SQLAlchemy 2.0 stable + psycopg 3 + Alembic; application boundary owns transaction.

## TD-22 — Migration/copy/recovery governance
**ACCEPTED** — Alembic authority, immutable applied revisions, drift/risk review, staged PostgreSQL changes, expand→migrate→contract, bounded backfills, separated privilege classes, logical copy distinct from recovery; raw PROD→DEV forbidden by default.

## TD-23 — Environment/config/secrets
**ACCEPTED** — exactly LOCAL/DEV/UAT/PROD; environment != Git branch; backend typed fail-fast config/workload identity/secret manager/OIDC posture; frontend profiles map to same contexts and client config is public.

## TD-24 — Testing/CI/supply chain
**ACCEPTED** — GitHub Actions primary; backend risk-layered real-PostgreSQL testing; frontend co-located unit/component + app E2E + strict boundary/cycle checks; required checks only after real stable contexts; least privilege/SHA pinning/supply-chain controls at real artifact boundaries.

## TD-25 — Cloud/IaC and current next boundary
**PARTLY DEFERRED / CURRENT HANDOFF** — backend compute/IaC/registry/sizing remain deferred until first remote infrastructure.

Frontend Foundation design/architecture is **CLOSED / ACCEPTED / FINAL REVIEW PASS / PENDING MAIN INTEGRATION**.

```text
prepare protected-main integration
→ PR only with explicit authorization
→ merge only with expected-head safety and explicit authorization
→ post-merge readback
→ new bounded frontend materialization/direct-validation scope
```

Backend production scaffold remains separate and NOT STARTED.

## Selected defaults not to reintroduce casually

Do not casually reintroduce previously excluded/nonselected canonical databases/service zoo, universal event sourcing/CRDT authority, Next.js for authenticated DANTE Web, Flutter/RN-Web universal renderer, Nx baseline, Redux default authority, alpha PowerSync Query adapter, or generic browser PWA/service-worker offline baseline without materially changed evidence and explicit architecture scope.
