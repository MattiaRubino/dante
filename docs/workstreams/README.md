# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-06
- **Rule:** current subsystem/workstream files describe present truth; Git/PR/archive preserve chronology

## 1. Current project state

```text
Product / Domain / Logical / Physical            CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6        CLOSED / ACCEPTED
PostgreSQL                                       18.6

Access/Auth M1–M5 + Shared Email                 CLOSED / INTEGRATED
PostgreSQL Recovery                              CLOSED / INTEGRATED
Platform Observability                           CLOSED / INTEGRATED VIA PR #58
AI deterministic low-level foundation            CLOSED / INTEGRATED VIA PR #63
Home / World Focus reconciliation                CLOSED / INTEGRATED VIA PR #65

Protected-main HEAD                              5258452d7bd4e7a2797922b00035a9068ba41167
Protected-main Alembic                           20260904_17
Protected-main topology                          88|5|16|76|172|89|270|0|0|0

Pre-vertical candidate Alembic                   20260906_18
Pre-vertical candidate topology                  89|5|18|77|173|91|272|0|0|0
PV-01                                            CLOSED / PASS
PV-02                                            CLOSED / PASS
PV-03 A Scale Harness                            CLOSED / PASS
PV-03 B Whole-Branch QA                          CLOSED / LOCAL PASS
PV-03 C protected-main integration               IN PROGRESS
```

There is no PV-04.

AI production/private-data qualification, remote backup-provider recovery and production/cloud recovery remain explicitly unclaimed.

## 2. Current authority

Global current truth is owned by:

- `../PROJECT-STATUS.md`
- `../ROADMAP.md`
- executable repository truth
- current subsystem references

### Pre-vertical candidate

The active append-only roadmap `pre-vertical-foundation.md` is retired at closure. The single retained branch closure/integration record is:

- `pre-vertical-foundation-closure-2026-09-06.md`

Durable pre-vertical foundation references are:

- `../architecture/authenticated-dante-context.md`
- `../database/README.md`
- `../development/pre-vertical-dogfood-personas.md`
- `../development/pre-vertical-scale-harness.md`
- `../operations/postgres-recovery-runbook.md`
- executable source/migrations/tests/tooling

The closure record remains integration-candidate evidence until protected-main merge/readback. After merge it becomes historical closure evidence; it does not remain an active development roadmap.

### AI

The deterministic AI foundation is already protected-main truth through PR #63 / merge `431fb34029baeacc9ef9f721e9626b39ca10dd39`.

AI implementation/qualification records may remain as retained design/evidence references, but they are no longer an active protected-main integration workstream. Future real Search/Ask/memory/solver/provider-production work requires a new explicit scope from then-current `main`.

### Home / World Focus

The Home/World Focus reconciliation is already protected-main truth through PR #65 / merge `5258452d7bd4e7a2797922b00035a9068ba41167`. Its closed branch history must not be treated as an active continuing workstream.

## 3. Access/Auth and Email disposition

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

## 4. Platform Observability disposition

Current/evolving authority:

- `../architecture/observability-runtime-contract.md`
- `../development/observability-runbook.md`
- `../../infra/observability/README.md`
- `../database/dante-postgresql-database-part-12.md`
- executable backend/Web/Alloy/Grafana/provisioning/test assets

Historical branch record:

- `../archive/branches/2026-09-feature-platform-observability.md` — **NON-AUTHORITATIVE / HISTORICAL / EVIDENCE ONLY**

Protected-main integration is complete via PR #58.

## 5. PostgreSQL Recovery disposition

PostgreSQL Recovery is integrated and has no active source workstream overlay.

Current durable operational authority:

```text
database contract   ../database/README.md
operator runbook    ../operations/postgres-recovery-runbook.md
bootstrap           ../../infra/local/postgres/recovery/bootstrap-local-recovery.sh
whole rehearsal     ../../infra/local/postgres/recovery/cp07-whole-recovery-rehearsal.sh
```

Historical branch record:

- `../archive/branches/2026-08-feature-postgres-recovery.md` — **NON-AUTHORITATIVE**

Historical CP07/CP08 proof remains exact-head scoped. The pre-vertical `20260906_18` candidate requires its own final exact-head rehearsal before merge.

## 6. Pre-vertical integration order

```text
PV-01 / PV-02 / PV-03 A implementation          CLOSED / PASS
→ PV-03 B local whole-branch QA                 CLOSED / PASS
→ documentation lifecycle cleanup               FINAL CANDIDATE
→ exact-head Recovery rehearsal                 REQUIRED
→ fetch/re-read protected main                  REQUIRED
→ reconcile only if main moved                  CONDITIONAL
→ bounded PR                                    REQUIRED
→ Backend CI Gate                               REQUIRED
→ Dependency Review                             REQUIRED
→ Frontend CI Gate                              REQUIRED
→ merge commit only                             OWNER-AUTHORIZED
→ protected-main readback                       REQUIRED
→ retire feature/pre-vertical-foundation        AFTER ACCEPTANCE
```

No further foundation expansion is implied by this sequence.

## 7. Documentation lifecycle rule

Before continuing any active workstream:

1. verify exact branch/worktree/remote relation;
2. read current global/subsystem authority;
3. read a branch-local workstream record only when one legitimately remains active;
4. prefer repository/code/tests over conversation memory;
5. do not write to protected `main` outside the repository integration path;
6. do not treat selected/unimplemented capability as PASS;
7. keep current docs aligned with materialized repository truth;
8. remove live/session/resume handoffs before integration;
9. retire active workstream authority after protected-main acceptance;
10. retain only justified closure/evidence records; chronology otherwise belongs to Git/PR history.

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

## 9. Next-work rule

After pre-vertical protected-main acceptance, the next workstream must start from then-current protected `main` under a new bounded real product-vertical scope. Do not continue development on a retired feature branch.
