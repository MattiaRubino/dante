# DANTE observability infrastructure

This directory owns the collector-side production baseline for DANTE. It is intentionally separate from Access/Auth business behavior and can be merged, deployed and disabled independently.

The runtime topology is:

- backend OTLP metrics/traces -> loopback-published Alloy OTLP receiver;
- backend newline-delimited JSON logs -> bounded local file -> Alloy file tail -> Loki;
- Web Faro errors, Web Vitals and sampled traces -> local Alloy Faro receiver in LOCAL/UAT, or the Grafana Cloud Frontend Observability collector directly in production;
- PostgreSQL operational metrics -> dedicated `dante_observer` role -> embedded PostgreSQL exporter;
- backend readiness -> black-box probe;
- Alloy self-metrics -> Grafana Cloud Prometheus;
- metrics/logs/traces -> the existing Grafana Cloud Free EU stack endpoints.

No SQL statement text, bind values, request/response bodies, URL query strings, credentials, email addresses or DANTE business references are intended to cross this boundary.

PostgreSQL remote-write is fail-closed through a source-controlled metric-family
allowlist. Per-table, per-role, per-replication-slot, per-vacuum-relation and any
future unreviewed exporter families are dropped inside Alloy before they can
consume Grafana Cloud Free quota or expose object names.

## Immutable collector image

Compose uses `grafana/alloy:v1.19.2` pinned to the verified multi-platform index digest `sha256:b8ec653c44235fbe910879145dac3597d66b0aaecf60bcbbe82580767771a839`.

## Local secret files

Create both files without a trailing newline and keep them workstation-local:

```bash
mkdir -p infra/compose/secrets .dante/observability/logs
umask 077
python3 -c "import secrets,sys; sys.stdout.write(secrets.token_urlsafe(32))" \
  > infra/compose/secrets/dante_observer_password.local
python3 -c "import getpass,sys; sys.stdout.write(getpass.getpass('Grafana Cloud token: '))" \
  > infra/compose/secrets/grafana_cloud_api_key.local
```

Provision PostgreSQL with the exact observer password, then construct the credential file without exposing it in shell history:

```bash
python3 tooling/observability/write-observer-dsn.py
python3 tooling/observability/write-grafana-otlp-authorization.py
```

The generated `infra/compose/secrets/dante_observer_dsn.local` is ignored by Git. It contains only the least-privilege observer identity; it is never a backend runtime or database administrator credential. `grafana_cloud_otlp_authorization.local` is a derived RFC 7617 header for the OTLP gateway; it is not a second Grafana token and must also remain ignored.

For LOCAL Compose, Alloy runs as non-root UID `473` and is added only to your
primary WSL group. Docker Compose implements file-backed secrets as bind mounts,
so make the three projected files read-only for that private group (not
world-readable):

```bash
chmod 640 infra/compose/secrets/grafana_cloud_api_key.local infra/compose/secrets/dante_observer_dsn.local infra/compose/secrets/grafana_cloud_otlp_authorization.local
```

The observer password source remains `0600`: only the derived DSN, Grafana
ingestion token and derived OTLP authorization are projected to Alloy. Re-run
the generator and `chmod` after rotating the token. Remote deployments use
their platform-native secret manager instead.

## Grafana Cloud Free connection

1. Create or select one Grafana Cloud Free stack in an EU region.
2. Create one access-policy token limited to metrics write, logs write and traces write. Do not grant stack administration to Alloy.
3. Copy `infra/observability/.env.example` to `.env.local` and replace every endpoint/instance ID from the stack connection pages.
4. Put only the token in `infra/compose/secrets/grafana_cloud_api_key.local`.
5. For production browser telemetry, create a Frontend Observability application and set its collector URL as `VITE_DANTE_FARO_COLLECTOR_URL` during the Web build. Browser collector URLs are ingestion identifiers, never Grafana administration tokens.

The Web runtime lazy-loads Faro only when enabled and, by default, when Global
Privacy Control is not active. The production CSP must allow `connect-src` to
the exact collector origin and the same-origin DANTE API boundary only; do not
introduce wildcard telemetry destinations.

No paid Grafana feature is required by this baseline. Quotas and retention remain controlled by the selected Cloud Free plan, so the budget dashboard and runbook define the operating guardrails instead of assuming unlimited ingestion.

## Run and verify

```bash
python3 tooling/observability/validate.py
docker compose -f infra/compose/local.yaml config --quiet
docker compose -f infra/compose/local.yaml --profile observability up -d --wait
```

Alloy endpoints are published only on loopback:

- UI/health: `http://127.0.0.1:12345`;
- OTLP gRPC: `127.0.0.1:4317`;
- OTLP HTTP: `http://127.0.0.1:4318`;
- LOCAL Faro: `http://127.0.0.1:12347/collect`.

The application stays available if Alloy or Grafana Cloud is unavailable. Telemetry queues and retries are bounded; exhaustion drops observability data and is itself visible in Alloy self-metrics.
