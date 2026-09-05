# DANTE Observability Runbook

- **Status:** CURRENT / OPERATOR PROCEDURE
- **Target:** Grafana Cloud Free EU + Grafana Alloy
- **Architecture:** `../architecture/observability-runtime-contract.md`
- **Collector source:** `../../infra/observability/`

## 1. What this runbook operates

This procedure operates DANTE technical telemetry only:

```text
backend metrics/traces
backend redacted structured logs
Web errors/Web Vitals/sampled traces
PostgreSQL operational statistics
black-box readiness
collector health/budget
```

It is not a product analytics system, canonical history store or security audit
ledger.

## 2. One-time Grafana Cloud Free setup

Create/select one Free stack in an EU region. Record the exact values shown in
the stack connection pages:

```text
OTLP gateway URL + instance ID
Prometheus remote-write URL + instance ID
Loki push URL + instance ID
Grafana stack URL
```

Create one ingestion access-policy token restricted to the exact stack and only:

```text
metrics write
logs write
traces write
```

Do not grant stack administration to Alloy. Do not reuse a personal/admin token
and do not put this token in the browser build.

For production browser telemetry, create one Frontend Observability application
per environment and copy its Web SDK collector URL. That URL is public Web
configuration; it is not the private ingestion token above.

Configure at least one real alert contact point before declaring PROD alerting
active. Contact-point ownership and escalation destination are deployment
decisions; the repository does not invent a recipient.

## 3. LOCAL files

From repository root:

```bash
mkdir -p infra/compose/secrets .dante/observability/logs
chmod 750 .dante/observability/logs
umask 077
python3 -c "import secrets,sys; sys.stdout.write(secrets.token_urlsafe(32))" \
  > infra/compose/secrets/dante_observer_password.local
python3 -c "import getpass,sys; sys.stdout.write(getpass.getpass('Grafana Cloud token: '))" \
  > infra/compose/secrets/grafana_cloud_api_key.local
cp infra/observability/.env.example infra/observability/.env.local
```

Replace every `REPLACE_*` value in `.env.local` with the exact EU stack values.
Never add tokens there.

Alloy runs as UID/GID `473:473` plus the host log directory's group. Set the
non-secret Compose interpolation before starting the profile:

```bash
export DANTE_OBSERVABILITY_LOG_GID="$(id -g)"
```

## 4. Provision the observer

Use the same generated observer password in the explicit database provisioning
command. From `apps/backend`, alongside the existing admin/migrator/runtime
values:

```bash
export DANTE_OBSERVER__PASSWORD="$(cat ../../infra/compose/secrets/dante_observer_password.local)"
uv run python -m dante.platform.database.provisioning
unset DANTE_OBSERVER__PASSWORD
```

Then write Alloy's private DSN without putting the password in argv or output:

```bash
cd ../..
python3 tooling/observability/write-observer-dsn.py
python3 tooling/observability/write-grafana-otlp-authorization.py
```

Keep `dante_observer_password.local` mode `0600` and without a trailing newline.
The derived observer DSN, Grafana ingestion token and derived OTLP authorization
are the only files projected into the non-root Alloy container. LOCAL Docker
Compose implements file-backed secrets as bind mounts, so make those files mode
`0640` after creation/rotation; Alloy is added only to the workstation user's
primary group:

```bash
chmod 640 infra/compose/secrets/grafana_cloud_api_key.local infra/compose/secrets/dante_observer_dsn.local infra/compose/secrets/grafana_cloud_otlp_authorization.local
```

Never make a secret world-readable. Remote environments use their
platform-native secret manager rather than this LOCAL bind-mount arrangement.
The OTLP header is derived from the ingestion token and stack instance ID; it is
not another token and must be regenerated whenever the ingestion token rotates.

## 5. Validate before start

```bash
python3 tooling/observability/validate.py
docker compose -f infra/compose/local.yaml config --quiet
```

CI also runs the exact pinned Alloy image's native `validate` command. A local
static PASS does not replace that native binary validation.

## 6. Start/stop

Start PostgreSQL and optional Alloy:

```bash
docker compose -f infra/compose/local.yaml --profile observability up -d --wait
docker compose -f infra/compose/local.yaml ps
```

Stop while preserving PostgreSQL and Alloy WAL state:

```bash
docker compose -f infra/compose/local.yaml --profile observability down
```

Do not add `--volumes` unless destruction of LOCAL state is explicitly intended.

Loopback endpoints:

| Endpoint | Purpose |
|---|---|
| `http://127.0.0.1:12345/-/ready` | Alloy readiness |
| `http://127.0.0.1:12345` | Alloy component UI |
| `127.0.0.1:4317` | OTLP/gRPC |
| `http://127.0.0.1:4318` | OTLP/HTTP |
| `http://127.0.0.1:12347/collect` | LOCAL Faro |

## 7. Application configuration

Backend `.env.local` uses:

```text
DANTE_OBSERVABILITY__ENABLED=true
DANTE_OBSERVABILITY__OTLP_HTTP_ENDPOINT=http://127.0.0.1:4318
DANTE_OBSERVABILITY__TRACE_SAMPLE_RATIO=0.10
DANTE_OBSERVABILITY__TRACE_HEALTH_CHECKS=false
DANTE_OBSERVABILITY__METRIC_EXPORT_INTERVAL_SECONDS=30
# Run from apps/backend: resolve to the worktree-root path mounted into Alloy.
DANTE_OBSERVABILITY__LOG_FILE=../../.dante/observability/logs/backend.jsonl
```

Web LOCAL uses:

```text
VITE_DANTE_OBSERVABILITY_ENABLED=true
VITE_DANTE_FARO_COLLECTOR_URL=http://127.0.0.1:12347/collect
VITE_DANTE_FARO_SESSION_SAMPLE_RATE=0.10
VITE_DANTE_FARO_RESPECT_GPC=true
```

Remote Web values are build-time and must contain exact release/build identity.
Never embed the Grafana Cloud API token.

Faro is lazy-loaded only when telemetry is enabled and permitted by the privacy
policy above. The production CSP must add the exact Faro collector origin to
`connect-src`; never use `*`. Keep browser API calls behind the same-origin
`/api/` boundary so trace propagation remains narrowly scoped.

LOCAL Alloy `faro.receiver` v1.19 accepts the Faro session header but not the
experimental fetch-v2 `Idempotency-Key` header. DANTE therefore deliberately
uses Faro's stable transport. Do not enable `fetchTransportV2` unless the
collector version and its exact CORS header contract are upgraded and verified
with a real-browser smoke, not only a minimal `OPTIONS` request.

The browser boundary also normalizes event/context attribute maps to the
string-map protocol accepted by this pinned Alloy receiver and removes browser
user metadata, session identifiers, browser fingerprinting and page URLs
entirely. The generic resource-performance instrumentation and Faro's complete
default metadata-producer set are disabled at the source; the recursive
sanitizer is then registered as the terminal outbound hook. This preserves
low-cardinality operational dimensions while keeping the Web SDK and collector
independently upgradeable.

The receiver may derive the coarse boolean `browser_mobile` field during
translation. It is the only permitted `browser_*` output: browser name/version,
OS, user agent, URLs, session identifiers, `context_*` and automatic resource
fields remain forbidden. Treat their appearance as a privacy-contract failure.

The Web build runs a manifest-backed bundle gate. It fails if the Faro runtime
stops being a dynamic chunk, the initial entry exceeds 500 KiB or the governed
Faro chunk exceeds 300 KiB. These are uncompressed transfer-independent upper
bounds; normal gzip/Brotli delivery is still required in deployment.

### 7.1 Source-closure verification

Run the deterministic source gates from the repository root before any runtime
acceptance or dashboard work:

```bash
corepack pnpm observability:verify
```

The command validates source-controlled infrastructure and privacy contracts,
Web formatting/lint/tests/typecheck/production bundle limits, and the complete
locked backend format/lint/mypy/non-PostgreSQL regression/build chain. It starts
no service and reads no credential. The canonical Node, pnpm, Python and uv
versions remain mandatory; a toolchain mismatch is a failed precondition, not a
reason to weaken a repository pin. For an isolated diagnosis, use
`python3 tooling/observability/verify.py --scope web` or `--scope backend`.

## 8. First smoke verification

1. Start Alloy and the observability-enabled backend. Then run the governed Web
   surface from the repository root:

```bash
corepack pnpm observability:smoke:web
```

   The command performs backend/Alloy preflight checks, generates an ephemeral
   one-day loopback certificate, builds with 100% LOCAL Faro sampling, serves
   HTTPS with the `/api/v1` proxy, and removes the certificate on exit. It never
   reads or exposes a Grafana credential. Accept the LOCAL certificate warning
   at `https://127.0.0.1:4173`; production certificates remain unaffected.
   Global Privacy Control is still honored, so use a LOCAL browser profile
   without GPC only for this explicit synthetic smoke.
2. Call `/health/ready` and exercise one successful and one deliberately invalid
   signin using synthetic LOCAL data.
3. Load Web and perform one navigation; use a synthetic test-only render error
   boundary probe when available.
4. Wait at least two 30-second metric intervals.
5. In Grafana Explore verify:

```promql
up{job="integrations/self",environment="local"}
probe_success{job="integrations/blackbox/dante-backend-ready",environment="local"}
http_server_request_count_total{deployment_environment_name="local"}
pg_stat_database_numbackends{job="integrations/postgres",environment="local"}
```

6. In Loki verify:

```logql
{application="dante",environment="local"} | json
```

7. In Tempo search for service `dante-backend` and confirm a sampled route span
   contains route template, method and status but no raw URL/query/body/identity.
8. Confirm a JSON backend log can correlate through `request_id` and, when
   sampled, `trace_id`.
9. Stop the Web surface with `Ctrl+C`; its child process and ephemeral TLS key
   must be gone before the smoke is considered complete.

If provider-side OTLP translation produces a different metric suffix/label name,
stop dashboard/alert materialization, capture the observed exact name and update
source-controlled queries plus tests in one change.

## 9. Apply dashboards and materialize alerts

The repository owns two classic dashboard HTTP-API models:

```text
infra/observability/grafana/dashboards/dante-service-overview.json
infra/observability/grafana/dashboards/dante-telemetry-pipeline.json
```

Grafana 12 may display/export the same dashboard as a
`dashboard.grafana.app/v2` resource whose expanded `spec.elements` form is much
longer. The formats are two serializations of the same dashboard; line counts
are not comparable and the classic source must never be pasted over the v2 JSON
editor. The governed runner sends the classic model to Grafana's dashboard API,
which performs the conversion and updates the existing stable UID.

Create a short-lived Grafana service account authorized only to write dashboards
and alert rules in the target stack. This is an administrative provisioning
credential, not the Alloy metrics/logs/traces ingestion token. Save it locally
without displaying or committing it:

```bash
umask 077
python3 -c "import getpass,sys; sys.stdout.write(getpass.getpass('Grafana service-account token: '))" \
  > infra/compose/secrets/grafana_service_account_token.local
chmod 600 infra/compose/secrets/grafana_service_account_token.local
```

In Grafana **Alerts & IRM → Alerting → Contact points**, create the owned real
contact point `DANTE Operations` and use its **Test** action. The destination is
entered only in Grafana; it is never passed in argv, chat or repository source.

Set the non-secret stack root and run the read-only plan first. Pass script
arguments directly after the pnpm script name; do not insert a standalone `--`
because pnpm forwards it literally to Python `argparse` in this toolchain:

```bash
export DANTE_GRAFANA_URL="https://YOUR-STACK.grafana.net"
corepack pnpm observability:grafana:plan --receiver "DANTE Operations"
```

The runner auto-selects a datasource only when exactly one datasource of that
type exists. If it reports multiple candidates, rerun with the exact non-secret
UIDs it prints, for example:

```bash
corepack pnpm observability:grafana:plan \
  --receiver "DANTE Operations" \
  --prometheus-uid METRICS_UID \
  --loki-uid LOKI_UID \
  --tempo-uid TEMPO_UID
```

Review the plan, then use the same datasource arguments for the single apply:

```bash
corepack pnpm observability:grafana:apply \
  --receiver "DANTE Operations" \
  --prometheus-uid METRICS_UID \
  --loki-uid LOKI_UID \
  --tempo-uid TEMPO_UID
```

The apply operation creates or validates the stable `DANTE` folder; updates
only the two DANTE dashboard UIDs; verifies every stored panel/query signature;
creates or updates exactly eight governed production alert UIDs; and creates
one labelled temporary LOCAL notification rule. Before replacing an existing
object it writes a private backup under the ignored
`.dante/observability/grafana-backups/` directory. It never deletes unrelated
objects, rewrites the global notification-policy tree, touches application data
or uses the ingestion credential.

The datasource mapping remains:

| Import field | Required datasource type |
|---|---|
| `DS_PROMETHEUS` | Grafana Cloud Metrics / Prometheus |
| `DS_LOKI` | Grafana Cloud Logs / Loki |
| `DS_TEMPO` | Grafana Cloud Traces / Tempo |

`DANTE · Telemetry pipeline & budget` uses only Prometheus and Loki. Do not
record a stack-specific datasource display name in source: Grafana Cloud names
vary by stack, whereas plugin type and datasource UID are the deployment
binding.

Both dashboards open on `local`, last six hours, with a one-minute refresh.
Select another environment only when that environment's runtime identity and
datasources have actually been activated. Use 30 seconds only while actively
investigating; it is not the normal refresh interval.

### 9.1 Dashboard triage and visual acceptance

Read `DANTE · Service overview` top-to-bottom:

1. `Backend readiness` must be `READY`; a quiet request-rate card is normal in
   LOCAL and is not a readiness failure.
2. When a server-error series exists, `Backend 5xx ratio` is green below 2%,
   yellow from 2% to below 10%, red at 10% or higher. A quiet environment that
   has never emitted that event-only series may show Grafana `No data`; treat
   that as neutral absence, not a healthy zero. `Backend latency p95` is green
   below 0.5 seconds, yellow from 0.5 to below 1 second, red at 1 second or
   higher.
3. Database readiness errors and KDF rejections must be zero when those series
   are present. If an event-only series has never been emitted, `No data` is
   acceptable as neutral absence but is not independent evidence of health. If
   non-zero, use the Auth/Database panels below before opening the redacted
   log/trace panels.
4. Empty warning/error logs and error traces are healthy when the upper signals
   are green; they are investigation surfaces, not required activity.

Read `DANTE · Telemetry pipeline & budget` separately from product health:

1. `Alloy` must be `UP`; collector RSS must remain below its configured warning
   threshold.
2. Metrics delivery failures and log drops must remain zero when present. Faro
   exporter errors are also expected to remain zero when browser telemetry is
   active. An absent Faro or other never-emitted event-only series may appear as
   `NO SIGNAL` or Grafana's native `No data`; both are neutral absence and are
   not implicit delivery success.
3. Use exporter failures, queue depth and the three delivery charts to diagnose
   a telemetry problem. Use the budget row for quota/cost review, not as a
   reason to blindly reduce availability/error instrumentation.

Visual acceptance requires both dashboards to load without datasource errors,
the environment selector to filter live data, and the applicable live signals
to match Explore. Capture that evidence in the current PR/acceptance record; a
closed workstream file is not current authority.

The alert source contract is:

```text
infra/observability/grafana/alerts/dante-alerts.json
```

Schema v2 separates each numeric PromQL signal from its explicit `gt`/`lt`
evaluator. This prevents a healthy false comparison from becoming an empty
vector that Grafana could misclassify as NoData. Production rules remain pinned
to `environment="prod"`; the synthetic receipt probe alone is labelled LOCAL.

Repository presence is not proof that dashboard import, rule evaluation or
notification delivery is active. PROD activation requires a synthetic alert
that reaches the chosen contact point and is then removed/paused.

### 9.2 Integrated operational-acceptance procedure

Run this one bounded procedure only after the source-closure gate and the
runtime smoke both pass. It completes the remaining dashboard, alert,
notification, collector-isolation and CI evidence without changing a migration,
business table, product role, secret or Grafana ingestion credential.

1. **Apply two dashboards and eight rules.** Run the plan/apply sequence above.
   Verify that both dashboards load with their exact datasources, fifteen
   service panels and the complete pipeline console. Treat `NO SIGNAL` and
   Grafana's native `No data` as neutral absence for never-emitted event-only
   series; neither is evidence of a healthy zero. Required liveness panels must
   still show their explicit live state. The eight production rules must appear
   under `DANTE production` with exact source UIDs.
2. **Prove the notification path honestly.** The apply command creates
   `DANTE acceptance · synthetic notification` in the temporary LOCAL group and
   binds it directly to the already-tested real receiver. Wait for the received
   notification and record its timestamp/title. A configured or pending rule is
   not receipt evidence. Immediately after receipt run:

   ```bash
   corepack pnpm observability:grafana:cleanup-synthetic
   ```

   Cleanup first verifies the exact UID, title, group and LOCAL synthetic labels;
   it refuses to delete anything else and confirms the rule is absent afterward.
3. **Prove collector/Grafana-delivery isolation.** With the application and
   Alloy already healthy, run from the repository root:

   ```bash
   corepack pnpm observability:prove:collector-outage --allow-alloy-outage
   ```

   The guarded command stops only the exact optional `alloy` Compose service,
   checks backend readiness three times while the collector path is absent and
   restores/rechecks Alloy in a `finally` block. It does not stop PostgreSQL,
   delete a volume or alter application data. This safely proves loss of the
   collector/Grafana delivery boundary, not an invented provider outage.
4. **Record the CI ACL proof, do not rerun it against a shared database.**
   `.github/workflows/backend-ci.yml` runs the disposable PostgreSQL acceptance
   suite. Its
   `test_current_catalog.py::test_m3_account_security_lock_is_narrow_and_transaction_scoped`
   test proves direct runtime `SELECT … FOR UPDATE` is denied, the narrow
   security-definer lock function is allowed and a second real connection sees
   the row lock. `test_privileges.py` proves exact role posture and that
   `dante_observer` reads statistics but no DANTE business state. The suite
   creates its own disposable database; do not run ACL experiments against a
   persistent development dataset merely to duplicate CI evidence.

The dashboard update, exact eight-rule catalog, real receipt, reversible
collector proof and named PostgreSQL CI checks form one acceptance record. Any
missing item remains `IN PROGRESS`; no dashboard image or local metric alone
upgrades it to PROD activation.

After the two live operations, revoke the short-lived service-account token and
remove only its local file. The Alloy ingestion token remains untouched.

## 10. Normal triage order

Use this order to avoid chasing symptoms:

```text
1. product availability/readiness
2. release/build/environment identity
3. error ratio and latency
4. affected route template / bounded outcome
5. correlated structured log by request_id/trace_id
6. sampled trace dependency timing
7. PostgreSQL/KDF/dependency pressure
8. collector delivery health and Free-plan budget
```

Do not search by email, Account reference or secret. Those values must not exist
in telemetry.

## 11. Alert procedures

### Backend unavailable

1. Confirm black-box failure and Alloy self-signal independently.
2. Check backend process/liveness, then `/health/ready` directly on loopback.
3. If live but not ready, continue with Database readiness.
4. Verify exact release/build and recent deployment/migration evidence.
5. Roll back only through the deployment procedure; do not alter data or bypass
   readiness to silence the alert.

### Backend error ratio

1. Confirm traffic floor and route-template distribution.
2. Correlate bounded 500 events via request/trace ID.
3. Identify application vs dependency vs database outcome.
4. Never enable raw bodies/SQL/emails as a diagnostic shortcut.

### Backend latency

1. Compare route p95, DB operation p95, KDF duration/inflight and HIBP duration.
2. Check collector health to exclude telemetry backlog distortion.
3. Reproduce against synthetic data before changing timeout/concurrency bounds.

### Database readiness

1. Check PostgreSQL container/service health and connection exhaustion.
2. Confirm runtime credential/config, not observer credential.
3. Use `dante_observer` only for statistics; never fall back to admin/migrator.
4. Preserve transaction and ACL boundaries during repair.

### Auth KDF saturation

1. Inspect inflight/active/rejection state and request pressure.
2. Distinguish queue-full from queue-timeout.
3. Check CPU and abuse/rate-limit outcomes.
4. Change Argon2 concurrency/queue only after benchmark evidence; never weaken
   password parameters merely to clear the alert.

### Alloy missing

1. Verify container state, health and 512 MiB/PID ceilings.
2. Inspect bounded local container logs.
3. Validate secret files exist/modes and non-secret endpoints are current.
4. Restart Alloy independently; backend availability must remain unchanged.
5. Expect bounded telemetry gaps; do not replay stale data indefinitely.

### Telemetry delivery

1. Check Grafana Cloud status, endpoint identity, token expiry/revocation and
   Free-plan quota/429 response.
2. Inspect OTLP queue, Loki retries/drops and Prometheus pending/failed samples.
3. Do not increase queues, retry horizons or sampling blindly: that converts a
   provider outage into memory/disk pressure.
4. Rotate only the ingestion token if compromise/expiry is confirmed.

## 12. Redaction incident

If any secret, email, business reference, raw URL query/body or SQL text appears:

1. treat it as a privacy/security incident;
2. stop the offending telemetry producer or disable its signal, without stopping
   the product unless product safety requires it;
3. revoke/rotate any exposed credential;
4. restrict access and follow provider deletion/support procedures;
5. identify source, time range, destination and viewers;
6. add a negative regression test before re-enabling;
7. do not paste the leaked value into tickets, commits or chat.

## 13. Rotation

Grafana ingestion token:

1. create a new least-privilege token;
2. update secret manager/file atomically;
3. restart Alloy;
4. verify all three signals;
5. revoke the old token;
6. verify no delivery errors.

Observer password:

1. generate a new independent password;
2. rerun explicit provisioning with the new observer secret;
3. atomically regenerate the DSN secret;
4. restart Alloy and verify PostgreSQL target;
5. remove superseded local secret material.

Never rotate runtime/migrator/admin credentials as a side effect of an observer
rotation unless their own policy requires it.

## 14. Free-plan budget review

Review the pipeline dashboard after first real traffic and at each substantial
feature/sampling change:

```text
scraped series by job
PostgreSQL allowlisted-versus-processed series
OTLP metric volume/queue
log bytes per second
trace sampling rate
Faro intake/errors
provider quota/retention page
```

Preferred reduction order:

```text
remove accidental/high-cardinality telemetry
keep PostgreSQL metric-family additions deny-by-default until reviewed
remove low-value instruments
reduce browser/backend sampling
increase non-critical scrape interval within SLO needs
shorten unnecessary retention/provider use where configurable
```

Never drop availability/error/budget self-signals first.

## 15. Reusable release / acceptance checklist

```text
[ ] exact Alloy native validation PASS
[ ] Compose config PASS
[ ] disposable PostgreSQL observer ACL PASS
[ ] backend/Web full CI PASS
[ ] real stack metrics/logs/traces PASS
[ ] dashboards imported and visually checked
[ ] alerts evaluate with exact labels
[ ] test notification reaches real contact point
[ ] redaction negative probes PASS
[ ] Alloy/Grafana outage leaves product available
[ ] disposable PostgreSQL role/ACL CI job passes
[ ] Free-plan usage measured and within budget
```

This is a reusable operator template for a future activation/release check.
Unchecked boxes do **not** retroactively erase acceptance already recorded in
current project status, archived evidence or CI. For any new execution, an
unchecked item remains missing evidence for that execution.
