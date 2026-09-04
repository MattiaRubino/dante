# DANTE Platform Observability Workstream

- **Status:** CLOSED / SOURCE CLOSURE COMPLETE / OPERATIONAL ACCEPTANCE PASS / NOT YET INTEGRATED
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

## Final source-closure verification — 2026-08-31

The canonical workstation toolchain first completed the repository-owned
closure runner on source baseline `cef64452e2306de5696fe711534b8591aede6b75`.
After Grafana acceptance and collector-outage tooling evolved, the complete
current runner was executed again on final implementation HEAD
`428bb47cb9a77483bab444a657f2edcc3023ca62`:

| Gate | State |
|---|---|
| Static observability contracts | PASS |
| Grafana acceptance tooling tests | PASS |
| Web formatting, lint, typecheck, tests and production bundle budget | PASS |
| Backend locked environment, Ruff format and lint | PASS |
| Backend mypy strict | PASS |
| Backend non-PostgreSQL regression suite | PASS |
| Backend package build | PASS; sdist and wheel produced |

The final runner completed all 13 current gates with
`observability source verification (all): PASS`. This is the final
implementation-tree source-closure evidence. The later closure documentation
commit does not alter runtime, database, dashboard, alert or collector
implementation.

## Dashboard design revision — 2026-08-31

Commit `f818b4bf9cefc0da777071839ee36342786e8cae` promotes the two
source-controlled Grafana dashboards from a useful query collection to the
intended operator console. It changes dashboard JSON only; no application,
database, migration, observer-ACL or telemetry collection contract changed.

| Dashboard | Decision strip | Diagnostic flow |
|---|---|---|
| `DANTE · Service overview` | readiness, request rate, 5xx ratio, p95 latency, DB readiness errors, KDF rejections | route traffic → Auth → PostgreSQL → redacted logs/traces |
| `DANTE · Telemetry pipeline & budget` | Alloy, collector memory, metrics failures, log drops, Faro exporter errors | OTLP queues/exporters → delivery → ingestion budget → backend warnings |

Both dashboards default to a one-minute refresh, expose an explicit environment
selector and retain 30-second refresh as an operator-selected incident option.
A zero-valued quiet-service signal is not an error. Event-only metric families
that have never emitted a sample may legitimately appear as Grafana `No data`;
that is neutral absence and is not evidence of a healthy zero. Required
liveness signals such as backend readiness and Alloy health remain explicit.

Grafana 12 exposes its stored dashboard as an expanded
`dashboard.grafana.app/v2` resource, whereas the repository owns the stable
classic HTTP-API model. These are not line-compatible JSON documents and must
never be pasted over one another.

The repository owns a guarded Grafana acceptance runner that resolves exact
datasource UIDs, updates the stable dashboards through Grafana's conversion API,
backs up existing objects and verifies their stored panel/query signatures. It
materializes exactly eight schema-v2 rules with numeric signals and explicit
evaluators, binds the real `DANTE Operations` contact point at rule level
without rewriting the global notification policy, and manages only the exact
temporary LOCAL receipt probe.

## Operational acceptance closure — 2026-08-31

| Evidence | State |
|---|---|
| Final implementation-tree source verification | PASS on `428bb47cb9a77483bab444a657f2edcc3023ca62`; all 13 current gates |
| Backend remote CI | PASS; GitHub Actions run `33417015520` on `feature/platform-observability` |
| Backend Quality | PASS |
| Disposable PostgreSQL role/ACL acceptance | PASS; `Backend PostgreSQL` completed the real PostgreSQL marked suite |
| Backend CI Gate | PASS |
| Faro/browser activation | PASS on the real activation checkpoint; release-identity smoke remains an integration-release check |
| Two source-controlled dashboards | PASS; apply and stored source-signature verification completed |
| Dashboard visual smoke | PASS; backend `READY`, live traffic/latency/PostgreSQL signals, Alloy `UP`, delivery failures/drops zero |
| Exact eight-rule production catalog | PASS; all eight governed UIDs applied and source-signature verified |
| `DANTE Operations` notification path | PASS; real synthetic notification delivered at `2026-08-31 17:41:00 UTC` |
| Synthetic acceptance cleanup | PASS; exact temporary rule removed; repeated cleanup confirmed it absent |
| Explicit redaction/correlation acceptance query | PASS on activation checkpoint; repeat for the integration release |
| Collector/Grafana-delivery outage isolation | PASS; backend remained ready for all three checks while Alloy was stopped, then Alloy restored healthy |
| Temporary Grafana administration token file | PASS; local file removed after acceptance |

The live visual smoke also resolved the apparent `No data` ambiguity: required
liveness and normal traffic/database signals were simultaneously present while
never-emitted error/event families remained empty. Those empty event-only
series are therefore treated as neutral absence, not as pipeline failure and
not as an implicit successful zero.

Historical or earlier runs are not promoted to final-tree evidence where a
later current-tree proof was required.

## Closure disposition

All branch-local source and operational acceptance requirements are satisfied.
The workstream is therefore **CLOSED / OPERATIONAL ACCEPTANCE PASS** on
`feature/platform-observability`.

This does **not** claim protected-main integration. Integration remains a
separate explicit gate and must preserve the documented release-identity and
redaction rechecks for the integrated release.

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