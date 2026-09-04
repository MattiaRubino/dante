# DANTE Roadmap

- **Status:** CURRENT PROTECTED-MAIN ROADMAP
- **Last reconciled:** 2026-09-04
- **Current macro state:** **ACCESS/AUTH M1–M5 + SHARED EMAIL + RECOVERY CLOSED / INTEGRATED**
- **Protected-main Alembic head:** `20260904_17`
- **Immediate red remediation:** Email post-restore quarantine/reopen whole-flow proof
- **Next bounded integration after remediation:** `feature/platform-observability`

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
PR #52 → protected main
        MERGED
              ↓
POST-MERGE MAIN BACKEND + FRONTEND CI
        PASS
              ↓
DATABASE-LOCAL CP07
        PASS FOR EXECUTED SCOPE
              ↓
POST-MERGE RED AUDIT
        EMAIL REOPEN ORDERING GAP FOUND
              ↓
EMAIL POST-RESTORE QUARANTINE + WHOLE-FLOW REHEARSAL
        REQUIRED BEFORE APPLICATION/EMAIL REOPEN CLAIM
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

The Access workstream is no longer an active continuation authority. Current truth is routed through protected-main subsystem references; one historical branch record lives at `archive/branches/2026-09-feature-access-auth.md` and is non-authoritative.

## 3. Email Platform

The Email Platform is shared DANTE infrastructure, not an Access-owned mailer. Current persistence is the four bounded delivery/attempt/provider-event/suppression structures. No second mail subsystem or generic event-bus abstraction is authorized.

The shared-ownership refactor and vocabulary hardening are integrated on protected `main`. The 2026-09-03 real SES UAT remains accepted historical real-provider evidence; production sender/domain deployment remains separate.

Post-restore quarantine is already implemented and directly tested in PostgreSQL. The outstanding item is **recovery orchestration and whole-flow proof**:

```text
restore remains traffic-isolated
→ Email workers stopped
→ MaterialState reconciliation accepted
→ quarantine_after_restore()
→ restored pending/claimed/retryable EmailIntent becomes recovery_quarantined
→ sensitive delivery material wiped
→ commit + read-back
→ workers/application traffic may resume
```

The whole CP07 harness must exercise this ordering before DANTE claims Email/application reopen after PITR.

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

The migration merge itself is accepted: `20260904_17` is no-DDL and preserves both histories. Real PostgreSQL acceptance proved convergence from the prior Recovery and Access heads to the single current head and reconciled Dictionary / SQLAlchemy / Alembic / live catalog.

A representative **existing-row preservation regression** for the `20260830_09 → 20260904_17` upgrade remains worth adding as explicit evidence. This is an evidence hardening item, not current evidence of data loss.

## 5. Recovery acceptance boundary

The historical CP07 rehearsal on implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` directly re-proved the current database head/topology during restore acceptance and earned `DATABASE LOCAL REOPEN = PASS` for its executed PostgreSQL/MaterialState scope.

It did not directly exercise Email `quarantine_after_restore()` before Email workers resume. Therefore:

```text
DATABASE LOCAL REOPEN                    PROVEN BY HISTORICAL CP07
APPLICATION / EMAIL REOPEN AFTER PITR    NOT YET PROVEN BY WHOLE CP07
remote backup provider                   TBD / NOT ACTIVATED
production/cloud recovery                NOT CLAIMED
```

Do not widen an old PASS beyond the steps actually executed.

## 6. Protected-main integration closure

PR #52 merged the accepted candidate into protected `main` at:

```text
merge commit   5f76ec54ad78542f137e8730e904f805d9e59e56
old main       fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282
candidate      6cee5506d404d0684b0679aca54c03f0ca433c72
merge tree     b610ece4fbfa0049749bb8454345a96a0385e6e5
```

The merge tree is identical to the accepted final candidate tree. Push CI on the exact merge commit passed Backend Quality, real PostgreSQL acceptance, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate.

Access/Auth + Email + Recovery therefore requires no further feature-branch merge step. The remaining recovery/Email work is a **forward post-merge remediation**, not a branch-history rewrite or PR #52 re-merge.

## 7. Platform Observability — next integration

`feature/platform-observability` is source-closed and operationally accepted but not yet integrated. Do not feed a known red recovery/reopen gap into its integration baseline first.

Required sequence:

```text
close Email post-restore recovery/reopen remediation on protected main
→ whole-flow recovery proof
→ enriched protected main
→ merge forward into feature/platform-observability
→ resolve bounded integration deltas
→ release identity / redaction / correlation / CI rechecks
→ PR observability → main
→ verify resulting protected main
```

Do not recreate accepted OTel/Alloy/Grafana/Faro/PostgreSQL-observer work.

## 8. Later Access maturity / M7

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

## 9. M6 Native Mobile

**FUTURE / OPTIONAL / RE-GATE.** It does not block the current red remediation.

## 10. Permanent rules

```text
protected main is integration authority
applied Alembic revisions are immutable
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PostgreSQL ≈ current DB reference
no network I/O in authoritative DB transactions
no blind retry after ambiguous external effects
restored external-effect work != permission to replay
no generic EAV/JSONB semantic escape hatch
no fake PASS
LOCAL DATABASE RECOVERY PASS != APPLICATION TRAFFIC REOPEN PASS
LOCAL recovery PASS != production/cloud recovery PASS
```
