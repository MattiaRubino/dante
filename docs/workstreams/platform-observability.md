# DANTE Platform Observability Workstream

- **Status:** ACTIVE / FOUNDATION ACTIVATED / SOURCE CLOSURE IN PROGRESS
- **Branch:** `feature/platform-observability`
- **PRE-SCOPE:** `dc5ee595c6291d980dc15f582dd094a399631557`
- **Authority:** branch-local until protected-main integration
- **Production target:** Grafana Cloud Free EU

## Purpose

Materialize the already selected observability target as an independently
mergeable platform slice, without waiting for or modifying later Access/Auth or
Home product work.

This branch is intentionally pinned before concurrently produced Access/Auth M4
commits. It does not merge/rebase them and does not modify Access product
behavior, Home/Today, migrations or business schema.

## Accepted scope

```text
backend OpenTelemetry metrics/traces + structured logs
Web Faro errors/Web Vitals/traces + recovery boundary
Grafana Alloy collector
Grafana Cloud Free connection contract
PostgreSQL statistics-only observer
black-box readiness
dashboards + alert source contract
redaction/cardinality/budget/failure handling
tests, CI, runbook and current architecture/database docs
```

## Implemented state

### Backend

- immutable bounded observability settings;
- owned OTel providers and bounded shutdown;
- route-template-only HTTP RED metrics/spans;
- Auth/KDF/HIBP operational instruments without identity labels;
- SQL-free database operations, pool and readiness signals;
- correlated deny-by-default JSON logging with rotation/redaction;
- exporter/collector failure isolated from product truth.

### Web

- Faro SDK platform adapter and failure-isolated initialization;
- error, Web Vitals, ephemeral session, view, navigation, CSP, React and sampled
  tracing instrumentation;
- same-origin `/api/` trace propagation only;
- vendor default metadata and generic resource-performance producers disabled;
- terminal recursive transport sanitizer with bounded Faro-v1 normalization;
- localized, responsive, token-driven recovery UI;
- architecture rule forbidding product/Auth/API data dependencies.

### PostgreSQL

- exact `dante_observer` role created/reconciled by provisioning;
- `pg_read_all_stats` membership only;
- no DANTE/public schema or DANTE object access;
- no statement collector and fail-closed remote-write family allowlist;
- Blueprint ↔ Dictionary scope/schema ↔ provisioning ↔ live-PG ↔ Alloy
  collector contract;
- no Alembic/schema/mapping change.

### Infrastructure/operations

- Alloy 1.19.2 pinned to reviewed multi-platform digest;
- hardened optional Compose profile;
- OTLP, Loki, Faro, Prometheus/PostgreSQL, black-box and self pipelines;
- finite queue/retry/WAL/memory/rate limits;
- two source-controlled Grafana dashboards;
- eight-rule source-controlled alert catalog;
- static validator, deterministic source-closure runner, private observer-DSN
  writer and operator runbook;
- CI native Alloy validation gate.

## Verified activation checkpoint — 2026-08-30

The following was proved against the real Grafana Cloud Free EU stack, not
inferred from static configuration. Credentials remain local-only and are not
represented in this repository.

| Evidence | State |
|---|---|
| Alloy native configuration validation, exact pinned image | PASS locally |
| Compose observability profile (PostgreSQL + Alloy) | PASS locally; both services healthy |
| Alloy readiness endpoint | PASS (`200`) |
| Alloy remote-write delivery | PASS; connection failures and enqueue retries observed as `0` |
| PostgreSQL statistics collector | PASS; `pg_stat_database_numbackends` returned the DANTE database series |
| Black-box backend readiness | PASS; `probe_success` changed from `0` to `1` when the backend started |
| Backend OpenTelemetry metrics | PASS; `http_server_request_count_total` received for real requests |
| Structured backend JSON logs → Loki | PASS; `observability.runtime_initialized` received with expected labels |
| HTTP and PostgreSQL spans → Tempo | PASS; `GET /api/v1/auth/session` and `postgresql.select` traces received |
| Web Faro events/measurements → Loki | PASS; real Firefox navigation and Web Vitals received for `dante-web` |
| Web privacy boundary | PASS on activation checkpoint; no URL, UA, browser/OS version, session, DOM context or resource timing fields exported |
| Secrets committed or displayed | PASS; none |

The HTTP request, its database span, the matching backend log pipeline and
backend health were all demonstrated using local runtime traffic. This is the
end-to-end activation checkpoint for the platform foundation.

## Remaining acceptance

| Evidence | State |
|---|---|
| Full backend regression and current-tree quality-gate rerun | pending |
| Full web quality gates | PASS locally; 58 tests, lint, typecheck, production build and bundle budget |
| Faro/browser activation | PASS operationally; final release-identity smoke remains part of integration acceptance |
| Source-controlled dashboard import and visual smoke | pending |
| Alert evaluation and delivery to a configured contact point | pending |
| Explicit redaction/correlation acceptance query | PASS on activation checkpoint; repeat for the integration release |
| Collector-outage proof: application remains available | pending |
| Disposable PostgreSQL role/ACL proof in CI | CI REQUIRED |

Historical or earlier runs are never promoted to PASS for the final tree.

## Closure rule

The workstream may claim source implementation closure only after repository
quality gates pass. It may claim end-to-end operational activation only after a
real Grafana Cloud stack proves metrics, logs, traces, dashboards, alert
evaluation/contact delivery, redaction and collector-outage behavior.

## Durable owners before integration

```text
architecture semantics  → observability-runtime-contract.md
operator procedure      → observability-runbook.md
collector/assets        → infra/observability/
database role truth     → database README/Blueprint/Dictionary + provisioning/tests
branch evidence/state   → this file
```

This workstream record must be consolidated according to the documentation
lifecycle policy before protected-main integration; it must not become the sole
authority for runtime behavior.
