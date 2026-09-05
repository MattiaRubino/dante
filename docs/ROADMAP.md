# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP
- **Last reconciled:** 2026-09-05
- **Current macro state:** **ACCESS/AUTH M1–M5 + SHARED EMAIL + RECOVERY + PLATFORM OBSERVABILITY CLOSED / INTEGRATED**
- **Protected-main Observability merge:** `b74a806deed68b2729dd04678c0a5674cd572e8a` via PR `#58`
- **Alembic head:** `20260904_17`

## 1. Current sequence

```text
Product / Domain / Logical / Physical
        CLOSED / CURRENT
              ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
              ↓
Access M1–M5 + Shared Email Platform
        CLOSED / INTEGRATED
              ↓
Recovery + Access/Auth + Email convergence
        20260904_17 / ACCEPTED
              ↓
CP07 database-local recovery
        PASS FOR EXECUTED SCOPE
              ↓
CP08 Email/application reopen
        PASS
              ↓
Platform Observability source closure
        OPERATIONAL ACCEPTANCE PASS
              ↓
true merge onto current main baseline
        14faecfb / ACCEPTED
              ↓
source verification + PostgreSQL/ACL + runtime smoke
        PASS
              ↓
documentation lifecycle reconciliation
        PASS
              ↓
PR #58 required CI
        PASS
              ↓
protected-main merge b74a806d
        PASS / INTEGRATED
              ↓
SHARED FOUNDATION UNBLOCKED
```

Platform Observability is now protected-main truth through PR `#58`. The former integration/source branches are historical only; future Observability work starts from then-current protected `main` under a fresh bounded scope.

## 2. Access/Auth + Email + Recovery

M1–M5 remain closed and integrated for their accepted scope. Password/session, signup/recovery/reset/reauth, Google, passkeys/Windows Hello, authenticator lifecycle, generated client, Web security surface and the shared durable Email Platform remain accepted at their documented evidence levels.

Apple real registered-domain UAT remains **BOUNDED DEFERRED / NON-BLOCKING**. It is not a real-provider PASS and must be reopened before future Apple production enablement.

The historical CP07 run proves the LOCAL PostgreSQL/database-local and MaterialState scope it actually executed. CP08 separately proves the forward Email/application reopen sequence after PITR. Neither proof is widened into production/cloud recovery.

## 3. Platform Observability integration

The source workstream is closed and frozen at `828cfd231debb1326933052fefd74e81c653a6c3`. The real integration branch was created from protected-main baseline `318ae452556e8bada3aaeee09688a89acc548a32`, carries the true two-parent merge `14faecfb11bded15aa929b0eaac91427031072ed`, and was integrated into protected `main` via PR `#58` at merge commit `b74a806deed68b2729dd04678c0a5674cd572e8a`.

Accepted integrated gates:

```text
observability source verification           13/13 PASS
PostgreSQL 18.6 / ACL acceptance             155/155 PASS
observer least-privilege posture             PASS
backend observability-enabled bootstrap       PASS
backend readiness                             HTTP 200
Alloy readiness                               PASS
Web/Faro LOCAL production-build smoke         PASS
Grafana Cloud metrics/logs/traces/Faro path   PASS
Tempo privacy boundary                        PASS
collector-outage isolation                    PASS
Grafana acceptance service-account cleanup    PASS
PR #58 Backend CI Gate                        PASS
PR #58 Frontend CI Gate                       PASS
PR #58 Dependency Review                      PASS
```

The accepted architectural boundary is the platform foundation: global HTTP, backend logs/traces, database telemetry, Web/Faro, Auth signin/KDF/dependency telemetry, PostgreSQL observer, Alloy and Grafana assets. Dedicated Google/Apple, passkey, Auth-lifecycle and Email central OTel metrics are optional future enhancements, not prerequisites for the completed integration.

## 4. Current bounded gate

There is no remaining Platform Observability integration gate.

```text
implementation integration      CLOSED
runtime acceptance              CLOSED
Grafana Cloud acceptance        CLOSED
collector isolation             CLOSED
documentation lifecycle         CLOSED
protected-main PR/CI            CLOSED
protected-main reachability     CLOSED
```

Future work must be activated as a new bounded workstream from current protected `main` rather than reopening the closed integration branch.

## 5. Database contract

Current application database contract remains:

```text
PostgreSQL          18.6
Alembic             20260904_17
88 tables / 5 views / 16 routines
76 triggers / 172 indexes / 89 FKs / 270 CHECKs
```

Platform Observability adds no business DDL or Alembic migration. `dante_observer` is a provisioning-owned operational role with `pg_read_all_stats` membership only and no DANTE/public business-object access.

## 6. Later work

Future bounded workstreams may include:

```text
M6 Native Mobile                         OPTIONAL / RE-GATE
session/device inventory                 FUTURE
per-session revoke / revoke all others   FUTURE
security-event history                   FUTURE
new-login/security notifications         FUTURE
Security UI refinement                   FUTURE
vertical observability metrics           FUTURE / NEED-DRIVEN
production observability tuning          FUTURE / MEASURED-EVIDENCE ONLY
production/cloud recovery                FUTURE / SEPARATE ACCEPTANCE
```

Start future work from then-current protected main on fresh bounded branches.

## 7. Permanent rules

```text
protected main is integration authority
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
applied Alembic revisions are immutable
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PostgreSQL ≈ current DB reference
no blind retry after ambiguous external effects
restored external-effect work != permission to replay
telemetry != canonical DANTE state
telemetry failure must not alter product behavior
no fake PASS
LOCAL recovery PASS != production/cloud recovery PASS
CURRENT SPECIFICATION != APPEND-ONLY DIARY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
```
