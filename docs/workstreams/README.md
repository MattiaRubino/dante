# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-04
- **Rule:** current subsystem/workstream files describe present truth; Git/PR/archive preserve chronology

## Current project state

```text
Product / Domain / Logical / Physical            CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6        CLOSED / ACCEPTED
PostgreSQL                                       18.6
Recovery                                         CLOSED / INTEGRATED

Access/Auth M1–M5                                CLOSED / INTEGRATED
Shared Email Platform                            CLOSED / INTEGRATED / OWNERSHIP VERIFIED
Google / Windows Hello / SES real UAT            PASS
Apple registered-domain UAT                      BOUNDED DEFERRED / NON-BLOCKING

protected main
  Access integration merge                       5f76ec54ad78542f137e8730e904f805d9e59e56
  Recovery↔Email hardening merge                 c67a18c24a6cf22b003ffd2c14243af53fec5077
  Alembic                                        20260904_17
  topology                                       88/5/16/76/172/89/270
  database-local CP07                            PASS
  application / Email reopen CP08                PASS
  post-merge Backend CI                          PASS
  post-merge Frontend CI                         PASS

feature/platform-observability                   CLOSED / OPERATIONAL PASS / NEXT INTEGRATION
M6 Native Mobile                                 FUTURE / OPTIONAL
later M7 Access/security maturity                FUTURE
```

The historical CP07 execution remains a valid **LOCAL PostgreSQL/database-local + MaterialState recovery proof** and is intentionally not widened beyond what it executed. PR #55 and CP08 closed the separate Email/application reopen gap forward: restored sendable Email work was physically resurrected by PITR, quarantined while workers remained stopped, sensitive material was wiped, the second reconciliation was idempotent, claimable work became `0`, and application/Email reopen passed.

Remote-provider and production/cloud recovery remain unclaimed separate gates.

## Current authority

Protected-main project truth is owned by:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

Access/Auth M1–M5 is integrated and therefore has **no active workstream authority file**. Current subsystem authority lives in:

- `../database/access-auth.md`
- `../architecture/access-auth-architecture.md`
- `../architecture/access-auth-security-contract.md`
- `../architecture/access-auth-api-contract.md`
- `../architecture/access-auth-testing-contract.md`
- `../architecture/access-auth-m5-contract.md`
- `../architecture/access-auth-m5-persistence-api-contract.md`
- `../frontend/access.md`
- `../architecture/email-platform.md`
- `../architecture/access-auth-email-delivery.md`
- `../operations/postgres-recovery-runbook.md`

## Access/Auth closure disposition

The completed Access/Auth workstream now follows the same lifecycle shape as the integrated Recovery workstream:

```text
active branch/workstream authority       RETIRED
obsolete execution-plan overlay          RETIRED
old pre-integration closure duplicate     CONSOLIDATED
live/session handoffs                     ABSENT
one branch-history record                 ARCHIVED / NON-AUTHORITATIVE
dated validation evidence                 RETAINED WHERE USEFUL
current subsystem references              CURRENT / EVOLVING
```

Historical branch record:

- `../archive/branches/2026-09-feature-access-auth.md` — **NON-AUTHORITATIVE**

Retained dated evidence:

- `access-auth-m5-review-2026-09-02.md` — historical validation/UAT evidence
- `access-auth-integration-acceptance-2026-09-04.md` — historical integration/CP07/CI evidence

Those evidence files never override current executable or current-reference truth.

## PostgreSQL Recovery

The PostgreSQL Recovery workstream is closed/integrated and has no active Recovery workstream overlay.

Current durable operational authority:

```text
database contract   ../database/README.md
operator runbook    ../operations/postgres-recovery-runbook.md
bootstrap           ../../infra/local/postgres/recovery/bootstrap-local-recovery.sh
whole rehearsal     ../../infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

Historical branch record:

- `../archive/branches/2026-08-feature-postgres-recovery.md` — **NON-AUTHORITATIVE**

## Current integration order

```text
enriched protected main
→ feature/platform-observability
→ observability release/integration rechecks
→ protected-main Observability PR
→ future bounded workstreams
```

## Operational continuation rule

Before continuing an active workstream:

1. verify exact branch/worktree/remote relation;
2. read current global/subsystem authority;
3. read an active branch-local workstream record only when one legitimately exists;
4. prefer repository/code/tests over conversation memory;
5. do not write to protected `main` outside the repository integration path;
6. do not treat selected/unimplemented capability as PASS;
7. keep current docs aligned with materialized repository truth;
8. remove live/session/resume handoffs before integration;
9. after merge, reconcile candidate/branch-local wording to protected-main truth and repair links to intentionally removed overlays;
10. keep at most one justified branch-history/closure narrative and classify retained dated audits as evidence rather than current authority.

## Permanent rules

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
APPLIED MIGRATION HISTORY IS IMMUTABLE
NO PASS WITHOUT EXECUTED EVIDENCE
LOCAL DATABASE RECOVERY PASS != APPLICATION TRAFFIC REOPEN PASS
LOCAL RECOVERY PASS != PRODUCTION/CLOUD RECOVERY PASS
```
