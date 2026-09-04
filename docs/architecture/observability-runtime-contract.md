# DANTE Observability Runtime Contract

- **Status:** BRANCH-LOCAL CURRENT / SOURCE CLOSURE COMPLETE / OPERATIONAL ACCEPTANCE PASS / NOT YET INTEGRATED
- **Branch:** `feature/platform-observability`
- **Pinned source baseline:** `dc5ee595c6291d980dc15f582dd094a399631557`
- **Target:** OpenTelemetry + Grafana Alloy + Grafana Cloud Free EU
- **Scope:** backend, Web, PostgreSQL operational telemetry, collector, dashboards, alerts, privacy and failure behavior
- **Non-scope:** canonical Domain history, security audit ledger, product analytics, Access semantics, Home/Today product UI, cloud compute/IaC

## 1. Decision

DANTE owns one vendor-neutral application instrumentation boundary and one
replaceable collector boundary:

```text
FastAPI metrics/traces ──OTLP/HTTP──┐
backend structured logs ──file──────┤
Web errors/vitals/traces ──Faro─────┼─> Grafana Alloy ─> Grafana Cloud EU
PostgreSQL statistics ──observer────┤      metrics/logs/traces
backend readiness ──black box───────┘
```

Production browser telemetry may use the Grafana Cloud Frontend Observability
collector directly. The browser never receives the Alloy/Grafana Cloud API
token. LOCAL/UAT may use Alloy's loopback-published Faro receiver.

This does not change the permanent semantic boundary:

```text
telemetry != canonical DANTE state
telemetry != Domain history / Evidence / Provenance
telemetry != security audit automatically
telemetry failure != permission to fail or alter product truth
```

## 2. Ownership

| Surface | Owner | Contract |
|---|---|---|
| Backend telemetry runtime | `dante.platform.observability` | providers, instruments, JSON logging, correlation and lifecycle |
| Backend configuration | `dante.platform.config.observability` | immutable bounds and safe defaults |
| Web telemetry adapter | `apps/web/src/platform/observability` | Faro initialization, sanitization, route events and error boundary |
| PostgreSQL collector identity | provisioning + Database System of Record | exact `dante_observer` posture |
| Collector | `infra/observability/alloy/config.alloy` | bounded intake, transformation and delivery |
| Operational views | `infra/observability/grafana` | source-controlled dashboards and alert contract |
| Operations | observability runbook | setup, verification, response, rotation and rollback |

No feature may import telemetry vendor internals to report business data.
Dependency rules prevent Web observability from importing features, Auth
transport or API data contracts.

## 3. Runtime identity

Every signal carries stable technical identity where the protocol supports it:

```text
service.name
service.namespace = dante
service.version = exact source/release SHA
deployment.environment.name = local | dev | uat | prod
dante.build.id = exact build identity
```

Deployment identity is low-cardinality and immutable for a running artifact.
`local` placeholders are rejected outside LOCAL by the existing Settings
contract.

## 4. Signal contract

### 4.1 Backend HTTP

The ASGI boundary records RED signals:

```text
http.server.request.count
http.server.request.duration
http.server.active_requests
```

Allowed dimensions are bounded method, resolved route template, response status
and outcome. Raw path, query string, request/response body, headers, client IP
and business identity are never attached.

Distributed parent context accepts only a single ASCII `traceparent` and
`tracestate`. Duplicate or malformed context is ignored rather than trusted.
Health requests retain metrics but are not traced by default.

### 4.2 Auth operational pressure

Auth reports only bounded outcomes and dependency health:

```text
dante.auth.signin.attempts
dante.auth.signin.duration
dante.auth.kdf.duration
dante.auth.kdf.inflight
dante.auth.kdf.active
dante.auth.kdf.rejections
dante.auth.dependency.requests
dante.auth.dependency.duration
```

No email, Account reference, credential reference, cookie, session secret,
rate-limit key or HIBP password material is a metric/span/log dimension.
Publicly equivalent credential failures remain operationally classifiable only
through bounded server outcomes; telemetry must not weaken the public API
equivalence contract.

### 4.3 PostgreSQL client

Application instrumentation records:

```text
db.client.operation.count
db.client.operation.duration
db.client.connections.usage
dante.database.readiness.checks
dante.database.readiness.duration
```

Database operation is classified into a closed verb set. SQL statement text,
comments, relation names and bind parameters are not exported. Client spans are
manually owned so an automatic driver instrumentor cannot silently add SQL.

### 4.4 Structured logs

Backend logs are one-line JSON with:

```text
timestamp
severity
logger
event
request_id when bound
trace_id/span_id when sampled
deny-listed/allow-listed bounded operational fields
exception type only
```

No traceback or exception message is emitted by the governed `log_event`
boundary. Common email, authorization, secret assignment, JWT, UUID/reference,
IPv4, DSN user-info, URL query/fragment and control-character forms are
redacted defensively. Arbitrary extra fields are discarded. Messages and files
are bounded; local files use rotation and mode `0640`.

Redaction is defense in depth, not permission to log sensitive input.

### 4.5 Web

The Web adapter records sampled, ephemeral-session diagnostics:

```text
uncaught errors and React boundary errors
Web Vitals
bounded navigation/view signals
CSP violations
sampled same-origin API traces
bounded resolved route identifiers
```

The Faro vendor runtime is a lazy production chunk. Disabled observability and
an honored browser Global Privacy Control signal do not download or initialize
the SDK. Initialization is idempotent under React development concurrency,
does not expose Faro on the browser global object and buffers at most the latest
bounded route template while the chunk loads.

It deliberately disables geolocation, resource collection, persistent session
tracking, attribution sources, console capture and generic user-action capture.
Generic resource-performance instrumentation is also disabled. After Faro
initializes its instrumentation hooks, DANTE removes the complete vendor
default metadata-producer set and installs its sanitizer as the terminal
outbound hook; initialization order is therefore part of the tested privacy
contract.
The transport sanitizer recursively bounds depth/keys/arrays/strings and
redacts identity-like keys, email, UUID/reference, authorization and URL
query/fragment content. It also enforces a total node budget, handles circular
references without recursion failure, never evaluates accessor properties and
uses null-prototype output objects. URL credentials, identifier-like path
segments and non-HTTP(S) URLs are removed before export.

Receiver translation may derive the coarse boolean `browser_mobile` dimension.
It contains no browser name/version, operating system, user agent, URL, session
or identity value. Any other exported `browser_*`, `page_*`, `session_*`,
`user_*`, `context_*` or resource-performance field violates this contract.

The deployment CSP must allow `connect-src` only to the DANTE API origin and
the exact configured Faro collector origin. Wildcard telemetry origins are
forbidden. The selected same-origin `/api/` deployment boundary remains the
only browser-to-backend trace-propagation surface.

The fallback screen is a functional product boundary, not a decorative mock:

- semantic DANTE design tokens only;
- localized IT/EN copy;
- keyboard-visible focus;
- retry and full reload actions;
- responsive system layout;
- no embedded brand background or raster asset that blocks theme/brand change.

Color, radii and surfaces remain centrally changeable through design tokens.

## 5. PostgreSQL observer

`dante_observer` is provisioning-owned technical foundation, not an Account,
Principal, Actor, application runtime or SQLAlchemy model.

Exact posture:

```text
LOGIN / INHERIT
NOSUPERUSER / NOCREATEDB / NOCREATEROLE / NOREPLICATION / NOBYPASSRLS
CONNECT dante
NO TEMP / CREATE
search_path = pg_catalog
pg_read_all_stats membership only
NO dante/public schema usage
NO DANTE object privileges
NO DANTE role membership
```

Alloy uses the exporter safe defaults plus a bounded optional collector list,
disables settings metrics and does not enable `pg_stat_statements`. A
fail-closed metric-family allowlist forwards only aggregate database, lock,
WAL, replication, checkpoint, wraparound, long-transaction and exporter/scrape
health. Per-table, role, slot, vacuum-relation and future unreviewed families
are dropped before remote-write. The credential is still classified as a
secret because `pg_read_all_stats` exposes operational cluster statistics if
compromised.

The general Database Blueprint, Dictionary technical-role registry/schema,
provisioning and live PostgreSQL tests are updated together. Alembic and
SQLAlchemy are N/A because no schema/application object is added.

## 6. Collector reliability and security

The reviewed Alloy image is version-and-multi-platform-digest pinned. The
container is non-root, read-only, capability-free, `no-new-privileges`,
PID/CPU/memory bounded and publishes all ingress/UI ports on loopback only.

Delivery behavior is finite:

| Signal | Buffer/retry behavior | Exhaustion behavior |
|---|---|---|
| OTLP metrics/traces | memory limiter, batch, 128-request queue, 2-minute retry horizon | reject/drop telemetry; never block product indefinitely |
| Logs | rotating source file + finite Loki batching/retries | source stays bounded; final delivery drops visible in self-metrics |
| Prometheus metrics | WAL max one hour, bounded shards/capacity, ten-minute sample age | stale samples discarded; product unaffected |
| Faro | 512 KiB request limit and per-app token bucket | HTTP 429/drop browser telemetry |

Alloy self-metrics, black-box readiness and pipeline dashboards make collector
failure observable. Application startup and request handling do not depend on
Grafana Cloud availability.

## 7. Cardinality and cost contract

Allowed application dimensions are closed or deployment-bounded:

```text
environment / release / build
service
HTTP method / route template / status / outcome
Auth outcome / dependency / queue state
DB operation / connection state
```

Forbidden dimensions include raw URL/path/query, SQL, error message, stack,
email, user/account/person/actor/identity/session reference, token, arbitrary
provider ID and payload-derived text.

Free-plan protection is architectural:

- ten-percent default backend trace ratio;
- ten-percent default Web session ratio;
- health spans off;
- 30-second metric/scrape interval;
- no console/resource/user-action capture;
- no SQL/query text;
- finite log rotation and collector buffers;
- pipeline/budget dashboard with scrape-series and ingestion-rate views.

Budget changes require measured evidence from the target stack, not a blind
increase in sampling or retention assumptions.

## 8. Environment and transport

| Environment | Backend OTLP | Web Faro | Secrets |
|---|---|---|---|
| LOCAL | loopback HTTP to Alloy | loopback Alloy receiver | ignored mode-0600 files |
| DEV/UAT | loopback or HTTPS collector | environment collector URL | environment-isolated secret manager/projection |
| PROD | loopback sidecar/host agent or HTTPS | Grafana Frontend Observability HTTPS collector | PROD-only secret identity |

Non-local plaintext OTLP is rejected unless the collector address is loopback.
Browser collector URLs are public ingestion identifiers; administration/write
tokens are never build-time Web configuration.

## 9. Failure contract

| Failure | Product behavior | Operator signal |
|---|---|---|
| exporter construction fails | application starts with local providers/logging | redacted initialization event |
| Alloy absent | requests continue | `dante-alloy-missing`, local logs, failed exports |
| Grafana Cloud unreachable/429 | bounded retry then telemetry loss | queue/retry/drop self-metrics |
| PostgreSQL observer unavailable | application DB is unaffected | exporter target error |
| malformed Web telemetry config | Web renders with telemetry disabled | bounded console warning |
| Web render crash | localized recovery UI | Faro error when transport works |
| telemetry shutdown stalls | bounded timeout then process exits | shutdown-timeout event |

Observability never catches and converts product errors, fabricates success,
changes database transactions or broadens Auth behavior.

## 10. Source-controlled operational assets

The repository owns:

```text
DANTE · Service overview
DANTE · Telemetry pipeline & budget
exact PromQL alert catalog
setup/verification/incident runbook
static artifact validator
pinned Alloy binary validation in Backend CI
```

The dashboards have distinct, non-overlapping operating purposes:

| Dashboard | Primary question | First-row signals | Do not infer |
|---|---|---|---|
| `DANTE · Service overview` | Is the product runtime available or degraded? | black-box readiness, traffic, 5xx ratio, p95 latency, database readiness errors, KDF rejections | a quiet LOCAL service is unavailable merely because request rate is zero |
| `DANTE · Telemetry pipeline & budget` | Can operators trust telemetry delivery within the Free-plan envelope? | Alloy presence, collector RSS, metric delivery failures, log drops, Faro exporter errors | product failure merely because browser telemetry is intentionally disabled or a Faro series is absent |

The default dashboard refresh is one minute. The operator may select a
30-second refresh during an active incident; this affects dashboard queries
only, not the governed 30-second metric/scrape export cadence. Source dashboards
are descriptive operational views, not canonical history, alert-rule
substitutes or an authority to change product/database behavior.
Never-emitted event-only metric families may appear as `NO SIGNAL` or Grafana's
native `No data`. Both are neutral absence and must never be interpreted as a
healthy zero. Required liveness signals remain explicit and must be present when
the corresponding runtime component is expected to be available.

The alert catalog is source truth for expressions/severity/no-data behavior.
It is materialized in a real Grafana Cloud stack only after the first target
ingestion proves the exact provider-side metric label translation. A dashboard
or alert that has merely been committed is not claimed as remotely active.

## 11. Required proof

Closure requires:

```text
backend format + lint + strict typing + fast tests + build
frontend format + lint + architecture + typecheck + tests + build
Dictionary/Blueprint/provisioning static reconciliation
real PostgreSQL role/membership/ACL/operational-statistics proof
pinned Alloy validate command
Grafana dashboard/alert JSON validation
Compose configuration validation
fresh target-stack smoke: metrics + logs + traces + Faro + dashboard + alert path
redaction negative probes
collector-unavailable failure probe
```

Local absence of Docker or external credentials is recorded as missing evidence,
never converted into a PASS.

## 12. Reopen triggers

Reopen the smallest boundary if evidence shows:

- Free-plan quota pressure at accepted traffic;
- material sampling bias or missing incident evidence;
- label/cardinality drift;
- redaction leakage;
- target metric-name translation differs from dashboards/alerts;
- Alloy/provider API incompatibility;
- production topology cannot preserve loopback/TLS and secret separation;
- a real security audit ledger or product analytics capability is required.

Do not turn observability into canonical history or add a paid/local telemetry
stack merely because a future quota or provider constraint might exist.