# DANTE Platform Observability Workstream

- **Status:** ACTIVE / IMPLEMENTATION COMPLETE IN WORKTREE / ACCEPTANCE IN PROGRESS
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
- error, Web Vitals, session, view, navigation, performance, CSP, React and
  sampled tracing instrumentation;
- same-origin `/api/` trace propagation only;
- recursive transport sanitizer;
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
- static validator, private observer-DSN writer and operator runbook;
- CI native Alloy validation gate.

## Evidence ledger

| Evidence | State |
|---|---|
| Backend targeted observability tests | PASS locally |
| Existing backend fast regression | PASS before final additions; rerun required |
| Web typecheck/lint/tests | PASS before final infrastructure/docs; rerun required |
| Static observability artifact validator | pending final rerun |
| Exact Alloy native validation | CI REQUIRED; local Docker/binary unavailable |
| Disposable PostgreSQL role/ACL proof | CI REQUIRED; local Docker unavailable |
| Compose config | Docker environment required |
| Real Grafana Cloud Free EU ingestion | USER STACK CREDENTIALS/SETUP REQUIRED |
| Dashboard visual/data-source smoke | REAL STACK REQUIRED |
| Alert notification delivery | REAL STACK + CONTACT POINT REQUIRED |

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
