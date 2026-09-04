# DANTE Roadmap

- **Status:** CURRENT PROTECTED-MAIN ROADMAP
- **Last reconciled:** 2026-09-04
- **Current macro state:** **ACCESS/AUTH M1–M5 + SHARED EMAIL + RECOVERY CLOSED / INTEGRATED**
- **Protected-main Alembic head:** `20260904_17`
- **Next bounded integration:** `feature/platform-observability`

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
Recovery + Access/Auth + Email convergence
        20260904_17
              ↓
COMBINED QA + CP07
        PASS
              ↓
PR #52 → protected main
        MERGED
              ↓
POST-MERGE MAIN BACKEND + FRONTEND CI
        PASS
              ↓
ACCESS FOUNDATION
        CLOSED / INTEGRATED
              ↓
enriched main → feature/platform-observability
              ↓
OBSERVABILITY INTEGRATION RECHECK
              ↓
PR observability → protected main
              ↓
SHARED FOUNDATION UNBLOCKED
```

## 2. Access/Auth closure

M1–M5 are closed and integrated for their accepted scope. Password/session, signup/recovery/reset/reauth, Google, passkeys/Windows Hello, authenticator lifecycle, generated client, Web security surface and shared durable Email Platform are implemented and accepted at their documented evidence levels.

Apple real registered-domain UAT is **BOUNDED DEFERRED / NON-BLOCKING**. It is not a real-provider PASS and must be re-opened before future Apple production enablement.

## 3. Email Platform

The Email Platform is shared DANTE infrastructure, not an Access-owned mailer. Current persistence is the four bounded delivery/attempt/provider-event/suppression structures. No second mail subsystem or generic event-bus abstraction is authorized.

The shared-ownership refactor and vocabulary hardening are integrated on protected `main`. The 2026-09-03 real SES UAT remains accepted historical real-provider evidence; production sender/domain deployment remains separate.

## 4. Database convergence

```text
20260826_08
├── 20260830_09 Recovery
└── Access/Auth → Email → 20260904_16

20260830_09 + 20260904_16 → 20260904_17
```

Current protected-main topology:

```text
88 tables / 5 views / 16 routines
76 triggers / 172 indexes / 89 FKs / 270 CHECKs
```

The CP07 rehearsal on implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` independently re-proved this head/topology during restore acceptance and earned `DATABASE LOCAL REOPEN = PASS`. Remote backup provider and production/cloud recovery remain not activated/not claimed.

## 5. Protected-main integration closure

PR #52 merged the accepted candidate into protected `main` at:

```text
merge commit   5f76ec54ad78542f137e8730e904f805d9e59e56
old main       fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282
candidate      6cee5506d404d0684b0679aca54c03f0ca433c72
merge tree     b610ece4fbfa0049749bb8454345a96a0385e6e5
```

The merge tree is identical to the accepted final candidate tree. Push CI on the exact merge commit passed Backend Quality, real PostgreSQL acceptance, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate.

Access/Auth + Email + Recovery integration therefore requires no further feature-branch merge step.

## 6. Platform Observability — next integration

`feature/platform-observability` is source-closed and operationally accepted but not yet integrated. The next bounded sequence is:

```text
enriched protected main
→ merge forward into feature/platform-observability
→ resolve bounded integration deltas
→ release identity / redaction / correlation / CI rechecks
→ PR observability → main
→ verify resulting protected main
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

Start this later from then-current enriched protected main on a new bounded branch.

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
