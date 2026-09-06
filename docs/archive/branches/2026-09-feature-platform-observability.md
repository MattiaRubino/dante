# Branch history — Platform Observability

> Historical branch/integration record. **NON-AUTHORITATIVE / HISTORICAL / EVIDENCE ONLY.**
> Current truth lives in executable repository state, `docs/architecture/observability-runtime-contract.md`, `docs/development/observability-runbook.md`, `infra/observability/README.md`, the current database references, `docs/PROJECT-STATUS.md` and `docs/ROADMAP.md`.

## Identity

- Repository: `MattiaRubino/dante`
- Source workstream branch: `feature/platform-observability`
- Source merge base: `dc5ee595c6291d980dc15f582dd094a399631557`
- Source implementation HEAD: `428bb47cb9a77483bab444a657f2edcc3023ca62`
- Source closure HEAD: `828cfd231debb1326933052fefd74e81c653a6c3`
- Integration baseline: `318ae452556e8bada3aaeee09688a89acc548a32`
- Integration branch: `integration/platform-observability-v2`
- True integration merge: `14faecfb11bded15aa929b0eaac91427031072ed`
- Historical source→integration conflict-discovery PR: `#57`
- PostgreSQL: 18.6
- Application Alembic head during integration: `20260904_17`

At the checkpoint represented by this history record, the integration candidate had been accepted on the integration branch. Protected-main integration remained a later Git/PR reachability event and is not fabricated retroactively here.

## Purpose

The workstream introduced a bounded, privacy-safe Platform Observability foundation around the existing DANTE application rather than creating a second product-data system or an observability-owned business layer.

Delivered surfaces:

```text
backend OpenTelemetry metrics/traces
backend structured deny-by-default JSON logs
request correlation / route-template RED metrics
Auth signin/KDF/dependency operational telemetry
SQL-free database operation/readiness/pool telemetry
Web Faro adapter, Web Vitals, errors and sampled same-origin traces
PostgreSQL aggregate operational statistics via dante_observer
Grafana Alloy collector runtime
Grafana Cloud metrics/logs/traces delivery
black-box backend readiness
source-controlled dashboards and alert rules
bounded queues/retries/WAL/rate limits
privacy/cardinality/failure contracts and operator runbook
```

Permanent semantic boundary carried into current authority:

```text
telemetry != canonical DANTE state
telemetry != Domain history / Evidence / Provenance
telemetry failure != permission to alter product truth
no identity/session/secret/raw URL/raw SQL telemetry dimensions
observability remains removable/replaceable infrastructure
```

## Source workstream closure

The source branch closed before integration with:

```text
source implementation verification      13/13 PASS
backend format/lint/strict typing        PASS
Web format/lint/test/typecheck/build     PASS
backend non-PostgreSQL regression        PASS
backend package build                    PASS
remote backend CI                        PASS
real PostgreSQL acceptance               PASS
```

Remote backend CI evidence included run `33417015520`, with PostgreSQL acceptance passing.

The real Grafana Cloud activation proved the complete external signal path rather than only source configuration:

```text
Alloy exact-image validation             PASS
PostgreSQL + Alloy health                PASS
backend readiness                        HTTP 200
Prometheus remote write                  PASS
PostgreSQL aggregate statistics          PRESENT
black-box readiness 0 → 1                PASS
backend OTel metrics                     PRESENT
backend structured logs in Loki          PRESENT
HTTP + PostgreSQL traces in Tempo        PRESENT
Web Faro / Web Vitals                    PRESENT
Web privacy boundary                     PASS
Grafana dashboards                       2 MATERIALIZED
production alert rules                   8 MATERIALIZED
real notification receipt                PASS
synthetic cleanup                        PASS
dashboard visual smoke                   PASS
collector outage / product isolation     PASS
```

A real notification receipt was observed on 2026-08-31 at 17:41:00 UTC.

At source closure the remote service-account-token revocation was still unconfirmed. During pre-PR integration closure on 2026-09-05, the temporary `dante-observability-acceptance` service account was deleted in Grafana Cloud, revoking its remaining token. The Alloy ingestion token was deliberately left untouched.

## PostgreSQL observer contract

The source workstream introduced the provisioning-owned `dante_observer` technical role. Its accepted posture was:

```text
LOGIN / NOINHERIT
NOSUPERUSER / NOCREATEDB / NOCREATEROLE / NOREPLICATION / NOBYPASSRLS
CONNECT dante
NO database CREATE / TEMP
search_path = pg_catalog
pg_read_all_stats membership with INHERIT TRUE / SET FALSE / ADMIN FALSE
NO dante/public business-object access
NO DANTE application-role membership
```

No DANTE business DDL, Alembic revision or SQLAlchemy business model was added for observability. Current authority for this role is the Database System of Record, Section 46 of the detailed database reference, provisioning and live PostgreSQL tests.

## Integration history

The source branch had diverged substantially from the later protected-main baseline, which already contained modern Access/Auth M1–M5, Google/Apple/passkeys, shared Email Platform, Recovery hardening, current configuration safety and PostgreSQL 18.6/Alembic `20260904_17`.

An initial branch named `integration/platform-observability` was manually reconstructed through selected-file copying. It was deliberately abandoned and must never be merged because that method could not prove source completeness: it omitted source content including the observer database section, lost executable file modes and accumulated accidental connector commits.

The replacement integration branch, `integration/platform-observability-v2`, was created from the exact current-main anchor `318ae452556e8bada3aaeee09688a89acc548a32` and used a real Git three-way merge of the frozen source closure HEAD.

The resulting merge commit `14faecfb11bded15aa929b0eaac91427031072ed` has two parents:

```text
parent 1  318ae452556e8bada3aaeee09688a89acc548a32
parent 2  828cfd231debb1326933052fefd74e81c653a6c3
```

This made the complete frozen source history reachable from the integration branch and preserved the observability tooling executable modes.

The genuine merge surfaced 15 conflicts. Runtime/configuration conflicts were semantically composed so current Access/Auth/Email/Recovery behavior and observability ownership both survived. A stale source CP6 metadata workaround was rejected in favor of the evolved current-main PostgreSQL test truth. Documentation/index conflicts were intentionally deferred until the code/runtime acceptance gate was complete, then reconciled under the documentation lifecycle policy.

## Integrated acceptance

On the real v2 merge tree:

```text
observability source verification                13/13 PASS
supply-chain lockfile policies                   PASS
Grafana tooling                                  7/7 PASS
Web observability formatting/lint                PASS
Web tests                                        23 files / 101 tests PASS
Web typecheck                                    PASS
Web production build/budget                      PASS
backend locked environment                       PASS
Ruff format/lint                                 PASS
mypy strict                                      148 source files / zero issues
backend non-PostgreSQL regression                286/286 PASS
backend source/wheel build                       PASS
```

Real PostgreSQL 18.6 integration acceptance on the same integrated code passed:

```text
155 selected / 155 passed
Access/Auth M4/M5 integration                    PASS
Google / Apple / passkeys                        PASS
Email lifecycle/platform                         PASS
CP6/current catalog reconciliation               PASS
migrations fresh/head/base/head                  PASS
Alembic check / no drift                         PASS
exact privileges / role posture                  PASS
dante_observer statistics/no-business-state      PASS
runtime DB identity/readiness/outage recovery    PASS
Recovery reconciliation/material retirement      PASS
```

Targeted integrated runtime smoke then proved:

```text
backend bootstrap with Observability enabled     PASS
application startup                              PASS
/health/ready                                    HTTP 200
request-id response boundary                     PRESENT
Alloy readiness                                  PASS
Web production build                             PASS
Access page render                               PASS
invalid synthetic signin handled normally        PASS
Faro smoke surface                               READY
Grafana Cloud metrics/logs/traces/Faro path      PASS
Tempo route-attribute privacy boundary           PASS
collector-outage/product-isolation proof         PASS
```

The historical source cloud acceptance was retained as valid evidence and was not rerun merely to repeat already-earned proof.

## Scope deliberately not expanded during integration

The foundation was accepted without turning integration into a new feature phase. Current global coverage includes HTTP, backend errors/log correlation, database operations/readiness, Auth signin/KDF/dependency pressure, Web/Faro, PostgreSQL infrastructure and Alloy/Grafana.

The following remain future need-driven enhancements, not blockers for the foundation merge:

```text
dedicated Google/Apple domain metrics
passkey-specific domain metrics
Auth lifecycle-specific domain metrics
Email Platform central OTel metrics
```

The Email Platform already has its own privacy-minimized observability probe; exporting additional central OTel metrics is a later bounded choice.

## Knowledge disposition at lifecycle closure

Still-current rules and operator procedures were routed to:

- `../../architecture/observability-runtime-contract.md`
- `../../development/observability-runbook.md`
- `../../../infra/observability/README.md`
- `../../database/README.md`
- `../../database/dante-postgresql-database-part-12.md` — Section 46 observer contract
- `../../PROJECT-STATUS.md`
- `../../ROADMAP.md`

The former `docs/workstreams/platform-observability.md` operational source-workstream record was retired after this coverage review. Temporary live/session/resume handoffs were not retained. This file is the single consolidated Platform Observability branch-history narrative; detailed chronology omitted here remains recoverable through Git and PR history.

## Lifecycle classification

```text
current architecture / runtime contract      CURRENT / EVOLVING
runbook / infrastructure reference           CURRENT / OPERATIONAL
Database observer contract                   CURRENT / EVOLVING
this branch history                          NON-AUTHORITATIVE / HISTORICAL / EVIDENCE ONLY
old active/source workstream overlay         RETIRED
Git / PR chronology                          COMPLETE RECOVERABLE HISTORY
```
