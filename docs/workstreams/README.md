# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-03
- **Rule:** protected `main` stores durable current records/evidence, not active chat/session handoffs

## 1. Purpose

This directory contains durable workstream references and selected evidence. Temporary branch save-games are allowed only while useful and must be removed before protected-main integration under `../development/documentation-lifecycle-policy.md`.

```text
temporary handoff
→ knowledge coverage
→ current truth in current docs
→ durable rationale/evidence retained where needed
→ Git keeps chronology
→ handoff removed before main
```

## 2. Current project state

```text
Product / Domain / Logical / Physical            CLOSED / CURRENT
Engineering / Frontend Foundation                CLOSED / ACCEPTED
Backend CP1–CP6                                  CLOSED / ACCEPTED
PostgreSQL                                       18.6
Protected-main Recovery                          CLOSED / INTEGRATED

Access/Auth M1–M5                                CLOSED / ACCEPTED
local password/passkey UAT                       PASS
real Windows Hello UAT                           PASS
real Google UAT                                  PASS
real Apple registered-domain UAT                 BOUNDED DEFERRED / NON-BLOCKING

Shared Email Platform                            CLOSED / ACCEPTED
real SES signup/recovery/reset notification       PASS

feature/access-auth                              PRE-INTEGRATION AUDIT
feature/platform-observability                   CLOSED / OPERATIONAL PASS / NOT INTEGRATED
M6 Native Mobile                                 FUTURE / OPTIONAL
later M7 Access/security maturity                FUTURE
```

## 3. Active Access/Auth record

Current branch-local operational authority:

- `access-auth.md`

Current project routing:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

Durable implementation/evidence authorities:

- `../architecture/access-auth-architecture.md`
- `../architecture/access-auth-security-contract.md`
- `../architecture/access-auth-api-contract.md`
- `../architecture/access-auth-testing-contract.md`
- `../architecture/access-auth-m4-contract.md`
- `../architecture/access-auth-m5-contract.md`
- `../architecture/access-auth-m5-persistence-api-contract.md`
- `access-auth-m5-review-2026-09-02.md` — historical engineering/UAT evidence checkpoint
- `../frontend/access.md`
- `../database/access-auth.md`

Shared Email Platform:

- `../architecture/email-platform.md`
- `../architecture/access-auth-email-delivery.md`
- `../decisions/ADR-012-email-delivery-platform.md`
- `../development/email-platform-local-uat.md`
- `../development/email-platform-acceptance-2026-09-03.md`

## 4. Access/Auth closure disposition

M5 is closed. Apple real external UAT was explicitly accepted as a bounded deferral because its external prerequisites are unavailable; it is not represented as a PASS.

The current branch is feature-frozen for integration. No session/device/M7/mobile feature work should be added before Access/Auth and Email Platform are returned to protected main.

Current branch database before convergence:

```text
Alembic             20260903_15
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
```

Protected main independently owns Recovery at `20260830_09`. The histories will be converged later through merge + a forward Alembic merge revision, never by rewriting applied migrations.

## 5. Pre-integration documentation lifecycle

The dated Access/Auth live handoffs are temporary/superseded artifacts, not durable current authority. Before the PR to protected main they must pass knowledge coverage and leave the working tree.

The durable M5 review is retained because it contains useful evidence about real Windows Hello, Google UAT and defects discovered by manual full-stack testing. It must remain clearly evidentiary, not current-status authority.

The old `access-auth-m4-m7-execution-plan.md` path is historical planning. Current execution order is owned only by `../ROADMAP.md` and `access-auth.md`.

## 6. Current integration order

```text
feature/access-auth pre-integration audit
→ merge protected main into feature/access-auth
→ Alembic merge + combined QA
→ PR Access/Auth + Email Platform to protected main
→ merge enriched main into feature/platform-observability
→ observability integration/release rechecks
→ PR observability to protected main
→ new bounded workstreams from enriched main
```

This order returns shared foundations to main and removes long-lived feature-branch dependencies for other product work.

## 7. Closed/integrated durable records

### Backend / database

- `backend-scaffold.md` — CP1–CP5 closure/integration evidence.
- `../archive/branches/2026-08-feature-logical-postgresql.md` — consolidated historical CP6 branch record.
- `../database/README.md` — current database System of Record.
- `../development/backend-cp6-05-whole-database-qa.md` — retained CP6 acceptance evidence.

### Frontend

- `frontend-foundation.md`
- `frontend-materialization.md`
- `frontend-materialization-integration.md`
- `../frontend/access.md`
- `../archive/branches/2026-08-feature-access-frontend.md`

### Engineering / architecture

- `engineering-foundation.md`
- `physical-model.md`
- `pre-physical-coherence.md`

Domain/Logical current semantics live in `../domain/README.md` and `../logical-model/README.md`; old chronological workstream records do not override them.

## 8. Platform observability

`feature/platform-observability` is a separate already-closed branch-local workstream. It owns the accepted OTel/Alloy/Grafana/Faro/PostgreSQL-observer platform and its operational evidence. It is deliberately integrated only after Access/Auth + Email have first returned to main.

Its branch-local workstream file is not copied into Access/Auth as current authority.

## 9. `today-home.md`

`today-home.md` remains a separate Home/Today product/UX workstream record. It does not override current backend/database/Auth authority.

The remaining authenticated Home integration work should eventually start from the enriched main rather than extending this pre-integration Access branch.

## 10. Continuation rule

Before work:

1. read `../PROJECT-STATUS.md` and `../ROADMAP.md`;
2. verify exact branch, remote HEAD and protected-main relationship;
3. read `../development/documentation-lifecycle-policy.md`;
4. read the current workstream record for the active branch;
5. consume subsystem architecture/database authority relevant to the task;
6. use historical reviews only as evidence;
7. never let a dated handoff override current executable/current-reference truth.

## 11. Permanent rules

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED BRANCH TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
APPLIED MIGRATION HISTORY IS IMMUTABLE
NO PASS WITHOUT EXECUTED EVIDENCE
DO NOT REOPEN ACCEPTED WORK WITHOUT DIRECT DEFECT EVIDENCE
```
