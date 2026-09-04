# DANTE Roadmap

- **Status:** CURRENT INTEGRATION-CANDIDATE ROADMAP
- **Last reconciled:** 2026-09-04
- **Current macro state:** **M5 CLOSED / COMBINED INTEGRATION QA PASS / READY FOR PROTECTED-MAIN MERGE**
- **Candidate proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Candidate Alembic head:** `20260904_17`
- **Protected-main Alembic head:** `20260830_09`

## 1. Current sequence

```text
Product / Domain / Logical / Physical
        CLOSED / CURRENT
              ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
              ↓
Access M1–M5 + Shared Email Platform
        CLOSED / ACCEPTED
              ↓
PRE-INTEGRATION AUDIT
        CLOSED / PASS
              ↓
protected main Recovery merged into candidate
        DONE
              ↓
Alembic 20260904_17
        SINGLE FORWARD MERGE HEAD
              ↓
COMBINED RECOVERY + ACCESS + EMAIL QA
        PASS
              ↓
CP07 WHOLE LOCAL OPERATOR RECOVERY
        PASS
              ↓
PR #52 Access/Auth + Email foundation → protected main
        NEXT
              ↓
POST-MERGE MAIN VERIFICATION + DOC RECONCILIATION
              ↓
enriched main → feature/platform-observability
              ↓
OBSERVABILITY INTEGRATION RECHECK
              ↓
PR observability → protected main
              ↓
SHARED FOUNDATION UNBLOCKED
```

## 2. M5 closure

M5 is closed for its accepted scope. Password/session, signup/recovery/reset/reauth, Google, passkeys/Windows Hello, authenticator lifecycle, generated client, Web security surface and shared durable Email Platform are implemented and accepted at their documented evidence level.

Apple real registered-domain UAT is **BOUNDED DEFERRED / NON-BLOCKING**. It is not a real-provider PASS and must be re-opened before future Apple production enablement.

## 3. Email Platform

The Email Platform is shared DANTE infrastructure, not an Access-owned mailer. Current persistence is the four bounded delivery/attempt/provider-event/suppression structures. No second mail subsystem or generic event-bus abstraction is authorized.

The 2026-09-04 shared-ownership refactor and vocabulary hardening are accepted on the current candidate through static/unit/PostgreSQL regression and exact-HEAD CI. The 2026-09-03 real SES UAT remains accepted historical real-provider evidence; production sender/domain deployment remains separate.

## 4. Database convergence

```text
20260826_08
├── 20260830_09 Recovery
└── Access/Auth → Email → 20260904_16

20260830_09 + 20260904_16 → 20260904_17
```

Accepted candidate topology:

```text
88 tables / 5 views / 16 routines
76 triggers / 172 indexes / 89 FKs / 270 CHECKs
```

The enriched-baseline CP07 rehearsal on exact proof HEAD `81639c61478b476c995652d0060dde8f53aef089` independently re-proved this head/topology during restore acceptance and earned `DATABASE LOCAL REOPEN = PASS`. Remote backup provider and production/cloud recovery remain not activated/not claimed.

## 5. Protected-main integration gate

Before PR #52 is merged:

```text
current documentation reconciled to measured candidate truth
candidate HEAD/upstream alignment rechecked
protected main ref rechecked
fresh CI required on the final candidate commit
no migration/code/schema drift introduced by documentation closure
```

If protected `main` advances before merge, stop and integrate that delta into the candidate first. Rerun every affected gate; rerun CP07 whenever the database/recovery contract changes.

After merge, the resulting protected-main tree and CI are verified before the integration branch is retired.

## 6. Platform observability after Access integration

`feature/platform-observability` is already source-closed and operationally accepted but not integrated. After Access/Auth lands on main and post-merge main verification passes:

```text
enriched protected main
→ merge into feature/platform-observability
→ resolve integration deltas
→ release identity / redaction / correlation / CI rechecks
→ PR observability → main
```

Do not recreate accepted OTel/Alloy/Grafana/Faro/PostgreSQL-observer work.

## 7. Later Access maturity / M7

Future only:

```text
session/device inventory
per-session revoke / revoke all others
security-event history
new-login/security notifications
"this wasn't me" response
Security UI refinement/componentization
final authenticated Home handoff
release/accessibility/security polish
```

Start this later from enriched protected main on a new bounded branch.

## 8. M6 Native Mobile

**FUTURE / OPTIONAL / RE-GATE.** It does not block current integration.

## 9. Permanent rules

```text
protected main is integration authority
applied Alembic revisions are immutable
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PostgreSQL ≈ current DB reference
no network I/O in authoritative DB transactions
no blind retry after ambiguous external effects
no generic EAV/JSONB semantic escape hatch
no fake PASS
LOCAL recovery PASS != production/cloud recovery PASS
```
