# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-16
- **Rule:** current subsystem/workstream files describe present truth; Git/PR/archive preserve chronology

## 1. Current project state

```text
Product / Domain / Logical / Physical            CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6        CLOSED / ACCEPTED
PostgreSQL                                       18.6

Access/Auth + Shared Email                       CLOSED / INTEGRATED
PostgreSQL Recovery                              CLOSED / INTEGRATED
Platform Observability                           CLOSED / INTEGRATED VIA PR #58
AI deterministic low-level foundation            CLOSED / INTEGRATED VIA PR #63
Home / World Focus reconciliation                CLOSED / INTEGRATED VIA PR #65
Pre-vertical foundation                          CLOSED / INTEGRATED VIA PR #66

Protected-main baseline at temporal selection    Alembic 20260906_18
Active candidate workstream                      feature/timeline-temporal-operational
Candidate temporal DB authority                  Alembic 20260915_26

Timeline / Temporal-Operational:
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ⬜ NEXT
B07 UI/UX Consolidation v1                       ⬜ planned after B06
B15 Whole Vertical Closure                       ⬜ future
```

Candidate branch truth is not protected-main truth until integration. The branch-local roadmap/map are the current authority for temporal sequencing and progress.

## 2. Current Timeline / Temporal-Operational authority

Use these files for the active vertical:

- `timeline-temporal-operational-roadmap.md` — current ordered roadmap B00–B15;
- `timeline-temporal-operational-map.md` — current semantic map + live green-check ledger;
- `timeline-temporal-operational-handoff.md` — current handoff/boundary;
- `timeline-temporal-operational-b02-closure-2026-09-16.md` — B02 closure evidence;
- `timeline-temporal-operational-b02-execution-plan.md` — closed B02 plan pointer, no longer active execution authority;
- `timeline-temporal-operational-b02-e-usertest.md` — explicit record that the redundant B02-E manual protocol was not executed and is not an open gate.

Historical snapshots moved under `archive/` preserve the old wording/numbering without competing with current authority:

- `archive/timeline-temporal-operational-roadmap-freeze-2026-09-07.md`;
- `archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`;
- `archive/timeline-temporal-operational-b02-execution-plan-pre-closure.md`;
- `archive/timeline-temporal-operational-b02-e-usertest-protocol-unexecuted.md`.

### Current temporal numbering

```text
B00 Real Data Spine
B01 Activity Core
B02 Schedule Core
B03 Event Core
B04 Temporal Constraints + Movement Policy
B05 Product Organization
B06 Routine / Recurrence / Occurrence Baseline
B07 UI/UX Consolidation v1
B08 Session Runtime
B09 Responsibility / Participation
B10 Actual / Outcome / Confirmation / Resolution
B11 Advanced Recurrence / Conditional / Reminder
B12 Replanning / Conflict / Solver
B13 Provider / Offline / Multi-device
B14 Analytics / Statistics / Signals
B15 Whole Vertical Closure
```

The 2026-09-16 B07 insertion shifted the former B07–B14 blocks by +1. Current canonical docs use only the new numbering; old numbering exists only in explicit historical snapshots.

## 3. Global authority

Global current truth is owned by:

- `../PROJECT-STATUS.md`;
- `../ROADMAP.md`;
- executable repository truth;
- current subsystem references;
- the active bounded workstream authority above while the branch remains unmerged.

Protected-main integration records remain distinct from branch candidate truth.

## 4. Pre-vertical foundation disposition

The pre-vertical foundation is closed and integrated. Its retained closure/evidence record is:

- `pre-vertical-foundation-closure-2026-09-06.md`.

Durable references include authenticated DanteContext, Database README, dogfood personas/scale harness and PostgreSQL recovery runbook.

There is no PV-04.

## 5. Access/Auth and Email disposition

Current subsystem authority includes:

- `../database/access-auth.md`;
- `../architecture/access-auth-architecture.md`;
- `../architecture/access-auth-security-contract.md`;
- `../architecture/access-auth-api-contract.md`;
- `../architecture/access-auth-testing-contract.md`;
- `../frontend/access.md`;
- `../architecture/email-platform.md`;
- `../architecture/access-auth-email-delivery.md`;
- `../operations/postgres-recovery-runbook.md`.

Retained evidence:

- `access-auth-m5-review-2026-09-02.md`;
- `access-auth-integration-acceptance-2026-09-04.md`.

## 6. Platform / Recovery / AI disposition

Platform Observability is integrated via PR #58. PostgreSQL Recovery is integrated. The deterministic AI foundation is integrated through PR #63.

AI production/private-data qualification, remote backup-provider recovery and production/cloud recovery remain explicitly unclaimed.

Future real Search/Ask/memory/solver/provider-production work requires a new explicit scope from then-current authority and must not be inferred from the low-level AI foundation.

## 7. Documentation lifecycle rule

Before continuing any active workstream:

1. verify exact branch/worktree/remote relation;
2. read current global/subsystem authority;
3. read the active workstream roadmap/map/handoff;
4. prefer repository/code/tests over conversation memory;
5. keep protected-main and unmerged candidate truth distinct;
6. do not mark selected/unimplemented capability as PASS;
7. update the live ledger in the same closure/reconciliation slice;
8. move superseded detailed planning snapshots to explicit archive paths rather than leaving them as competing current authority;
9. do not falsify unexecuted manual/CI evidence;
10. retain only justified closure/evidence records as current references.

## 8. Permanent rules

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

For the active temporal vertical specifically:

```text
planned != happened
Schedule != Session != Actual
Routine != Recurrence != Occurrence
projection != canonical truth
current != latest row
Undo != history rewind
```
