# DANTE — Project Status

- **Status:** CURRENT REPOSITORY TRUTH / INTEGRATION CANDIDATE ACCEPTED
- **Last reconciled:** 2026-09-05
- **Access/Auth + Email + Recovery protected-main baseline:** `318ae452556e8bada3aaeee09688a89acc548a32`
- **Platform Observability source closure:** `828cfd231debb1326933052fefd74e81c653a6c3`
- **Platform Observability integration merge:** `14faecfb11bded15aa929b0eaac91427031072ed`
- **Current Alembic head:** `20260904_17`

## 1. Current state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
PostgreSQL                                 18.6

Access M1–M5                               CLOSED / INTEGRATED
Shared Email Platform                      CLOSED / INTEGRATED / OWNERSHIP VERIFIED
PostgreSQL Recovery                        CLOSED / INTEGRATED
local password/passkey UAT                 PASS
real Windows Hello UAT                     PASS
real Google UAT                            PASS
real Apple registered-domain UAT           BOUNDED DEFERRED / NON-BLOCKING

Alembic                                    20260904_17
database topology                          88/5/16/76/172/89/270
database-local CP07                        PASS
application / Email reopen CP08            PASS

Platform Observability source workstream   CLOSED / OPERATIONAL ACCEPTANCE PASS
Platform Observability current tree        INTEGRATED / ACCEPTED CANDIDATE
observability source verification          13/13 PASS
PostgreSQL/ACL integration acceptance      155/155 PASS
backend readiness + Alloy                  PASS
Web/Faro integrated production smoke       PASS

M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

Platform Observability is materially present in the current repository tree through a real two-parent Git merge. A protected-main integration claim is valid only once the corresponding integration commit is reachable from protected `main`; branch-local acceptance alone does not create that claim.

Apple is not reported as PASS. Real Apple external acceptance remains a future enablement prerequisite when its external account/domain prerequisites exist.

Remote backup-provider activation and production/cloud recovery remain **NOT CLAIMED**.

## 2. Current database truth

```text
PostgreSQL          18.6
Alembic             20260904_17
tables              88
views                5
routines             16
triggers             76
physical indexes     172
foreign keys         89
CHECK constraints    270
```

The current cross-representation database contract remains aligned across the Dictionary, SQLAlchemy mappings, Alembic and real PostgreSQL. Platform Observability adds no DANTE business DDL, Alembic revision or SQLAlchemy business mapping.

Its PostgreSQL operational reader is the provisioning-owned `dante_observer` role: `LOGIN INHERIT`, `pg_read_all_stats` only, no DANTE/public business-object access, no database `CREATE`/`TEMP`, and `search_path=pg_catalog`. The exact contract remains in `database/dante-postgresql-database-part-12.md` and the live provisioning/acceptance tests.

## 3. Accepted foundation evidence

Access/Auth + Email + Recovery remain closed at their accepted evidence levels. The historical CP07 database-local proof and the later CP08 application/Email reopen proof remain distinct; CP07 is not widened retroactively. Their durable evidence remains in `workstreams/access-auth-integration-acceptance-2026-09-04.md`, `archive/branches/2026-09-feature-access-auth.md` and the Recovery operator references.

Platform Observability acceptance on the integrated tree includes:

```text
true Git three-way merge                         PASS
frozen source history retained                   PASS
observability source verification                13/13 PASS
Web tests                                        23 files / 101 tests PASS
backend non-PostgreSQL regression                286/286 PASS
strict mypy                                      148 source files / zero issues
backend package build                            PASS
PostgreSQL 18.6 marked acceptance                155/155 PASS
observer role / membership / ACL proof           PASS
backend bootstrap with observability enabled     PASS
backend /health/ready                            HTTP 200
Alloy readiness                                  PASS
Web/Faro production-build smoke surface          PASS
```

The source workstream had already proved the real Grafana Cloud path for metrics, logs, traces, PostgreSQL statistics, black-box readiness and Web Faro/Web Vitals, plus dashboard/alert materialization and collector-outage failure isolation. That evidence is retained rather than rerun merely for repetition.

Dedicated Google/Apple, passkey, Auth-lifecycle and Email-to-central-OTel domain metrics are future observability enhancements. They are not blockers for the accepted platform foundation because global HTTP, database, Web, Auth signin/KDF/dependency and collector telemetry already cover the integration boundary without changing product semantics.

## 4. Current integration gate

The implementation integration work is complete on the current tree. The remaining repository gate is bounded:

```text
documentation lifecycle reconciliation
→ integration/platform-observability-v2 → protected-main PR
→ mandatory PR/merge CI
→ protected-main reachability establishes final integration state
```

Do not reopen accepted OTel/Alloy/Grafana/Faro/PostgreSQL-observer implementation merely to repeat evidence.

## 5. Documentation lifecycle state

Platform Observability no longer needs an active workstream authority file. Current truth is routed through:

- `architecture/observability-runtime-contract.md`
- `development/observability-runbook.md`
- `../infra/observability/README.md`
- `database/dante-postgresql-database-part-12.md` for the observer-role contract
- executable code, tests and source-controlled Grafana/Alloy assets

One consolidated historical record is retained at `archive/branches/2026-09-feature-platform-observability.md`. It is **NON-AUTHORITATIVE / HISTORICAL / EVIDENCE ONLY**.

Temporary live/session/resume handoffs are forbidden at the integration gate. Historical source-workstream chronology that is not current authority remains recoverable from the consolidated branch record and Git/PR history.

## 6. Permanent safety rules

```text
protected main is integration authority
no rebase/history rewrite of accepted work
no force push for normal integration
applied migrations are immutable
no schema claim without Dictionary/mapping/migration/PG/test parity
no PASS without executed evidence
telemetry != canonical DANTE state
telemetry failure != permission to alter product truth
LOCAL recovery PASS != production/cloud recovery PASS
```

## 7. Authority order

1. executable code / migrations / tests / real PostgreSQL
2. Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. this status + roadmap
5. durable evidence / Git chronology
6. conversation memory
