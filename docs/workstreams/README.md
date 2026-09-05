# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-05
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

Alembic                                          20260904_17
Database topology                                88/5/16/76/172/89/270
Database-local CP07                              PASS
Application / Email reopen CP08                  PASS

Platform Observability source                    CLOSED / OPERATIONAL PASS
Platform Observability protected main            CLOSED / INTEGRATED VIA PR #58

AI deterministic low-level foundation            CLOSED / PASS / BRANCH-LOCAL
AI main reconciliation                           COMPLETE / 4a0a69d9
AI protected-main integration                    PR / REQUIRED GATES PENDING
AI production/private-data qualification         NOT CLAIMED
AI real owner/product seams                      DEFERRED / TRIGGER-GATED

M6 Native Mobile                                 FUTURE / OPTIONAL
later M7 Access/security maturity                FUTURE
```

Protected-main acceptance is commit-reachability scoped. Platform Observability satisfies that condition through merge commit `b74a806deed68b2729dd04678c0a5674cd572e8a` from PR `#58`. AI does not yet: `feature/ai-implementation` is a main-reconciled candidate until its required PR gates and protected-main merge complete.

## Current authority

Project truth is owned by:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`
- executable repository truth
- current subsystem references

Access/Auth M1–M5 and Platform Observability have **no active workstream authority file** after closure and protected-main integration.

AI currently retains active branch-local integration authority at:

- `ai-implementation.md`
- `ai-foundation-closure-2026-09-05.md`
- `ai-runtime-model-target-closure-acceptance-2026-09-05.md`
- `../architecture/dante-ai-implementation-baseline-final.md`
- `../architecture/dante-ai-search-intelligence-boundary-amendment-2026-09.md`

The deterministic AI foundation is closed; the active responsibility of the branch is integration, not expansion into deferred product work.

## AI closure / integration disposition

```text
low-level deterministic foundation            CLOSED / PASS
Search deterministic foundation               CLOSED / PASS / INDEPENDENT FROM INTELLIGENCE
Gemini 3.8 Flash development binding          ACCEPTED FOR DEVELOPMENT FOUNDATION
production/private-data qualification         NOT CLAIMED
real Search owner/data seam                    DEFERRED
real Ask DANTE product integration             DEFERRED
main -> feature true merge                     4a0a69d9 / COMPLETE
required protected-main PR gates              PENDING
protected-main reachability                   NOT YET CLAIMED
```

The current development route keeps `STRUCTURED_INTERPRETATION` and `GENERAL_REASONING` on Gemini 3.8 Flash through DANTE's `ModelAccess` boundary; `DEEP_REASONING` remains dormant with no physical binding. Search remains deterministic and independently usable without Intelligence/model/provider runtime.

The main reconciliation preserves the current Auth/Access, Email, Recovery, Home/Timeline and Observability baseline and adds no database/Alembic revision.

## Access/Auth closure disposition

Current subsystem authority includes:

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

Historical branch record:

- `../archive/branches/2026-09-feature-access-auth.md` — **NON-AUTHORITATIVE**

Retained dated evidence:

- `access-auth-m5-review-2026-09-02.md`
- `access-auth-integration-acceptance-2026-09-04.md`

## Platform Observability closure disposition

Current/evolving authority:

- `../architecture/observability-runtime-contract.md`
- `../development/observability-runbook.md`
- `../../infra/observability/README.md`
- `../database/dante-postgresql-database-part-12.md` — exact `dante_observer` contract
- executable backend/Web/Alloy/Grafana/provisioning/test assets

Historical branch record:

- `../archive/branches/2026-09-feature-platform-observability.md` — **NON-AUTHORITATIVE / HISTORICAL / EVIDENCE ONLY**

Lifecycle disposition:

```text
active source-workstream authority         RETIRED
temporary live/session/resume handoffs     ABSENT
one branch-history record                  ARCHIVED / NON-AUTHORITATIVE
current runtime/ops references             CURRENT / EVOLVING
source and integration validation          RETAINED AS EVIDENCE
protected-main integration                 PR #58 / PASS
full chronology                            GIT / PR HISTORY
```

The former `platform-observability.md` source-workstream record is intentionally removed after knowledge coverage. Its still-useful history is consolidated into the single branch record above; its current rules live in the runtime contract, runbook, infrastructure reference and executable repository.

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
Platform Observability protected-main integration     CLOSED VIA PR #58
→ AI deterministic foundation                        CLOSED / BRANCH-LOCAL PASS
→ main -> feature/ai-implementation                  COMPLETE / 4a0a69d9
→ AI required PR gates                               NEXT
→ protected-main AI merge                            ONLY AFTER GREEN GATES + OWNER AUTHORIZATION
→ post-merge acceptance                              REQUIRED
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
9. reconcile candidate/branch-local wording through reachability-scoped truth;
10. keep at most one justified branch-history/closure narrative and classify retained dated audits as evidence rather than current authority.

## Permanent rules

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
APPLIED MIGRATION HISTORY IS IMMUTABLE
NO PASS WITHOUT EXECUTED EVIDENCE
SEARCH != INTELLIGENCE
LOCAL DATABASE RECOVERY PASS != APPLICATION TRAFFIC REOPEN PASS
LOCAL RECOVERY PASS != PRODUCTION/CLOUD RECOVERY PASS
```
