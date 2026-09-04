# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-04
- **Rule:** protected `main` stores durable current records/evidence, not active chat/session handoffs

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
  Alembic                                        20260904_17
  topology                                       88/5/16/76/172/89/270
  CP07 whole LOCAL recovery                      PASS
  post-merge Backend CI                          PASS
  post-merge Frontend CI                         PASS

feature/platform-observability                   CLOSED / OPERATIONAL PASS / NEXT INTEGRATION
M6 Native Mobile                                 FUTURE / OPTIONAL
later M7 Access/security maturity                FUTURE
```

## Current Access/Auth authority

- `access-auth.md`
- `../PROJECT-STATUS.md`
- `../ROADMAP.md`
- `../database/README.md`
- `../database/access-auth.md`
- `../architecture/access-auth-*.md`
- `../architecture/email-platform.md`
- `../operations/postgres-recovery-runbook.md`
- `../development/email-platform-acceptance-2026-09-03.md`

Durable executed integration evidence remains in `access-auth-integration-acceptance-2026-09-04.md`; it is historical evidence, not an active handoff.

M5 is closed and integrated. Apple real external UAT is an explicit bounded deferral, not a PASS. CP07 is a LOCAL operator-recovery PASS, not production/cloud recovery acceptance.

## Documentation lifecycle

Temporary Access/Auth handoffs were removed after knowledge coverage. Durable review/closure/integration evidence remains, but historical checkpoints never override current executable/current-reference truth.

The old `access-auth-m4-m7-execution-plan.md` is historical planning; current execution order is owned only by `../ROADMAP.md` and current workstream documents.

The former integration branch `integration/access-auth-main-20260904` is no longer current authority after PR #52. Its history remains Git evidence only.

## Current integration order

```text
enriched protected main
→ feature/platform-observability
→ observability release/integration rechecks
→ protected-main Observability PR
→ future bounded workstreams
```

## Closed durable records

Backend/database history is retained through current DB authority plus archive/Git chronology. Frontend/engineering/domain/logical historical workstream records remain evidence only unless explicitly marked current.

`access-auth-closure-2026-09-03.md` remains historical feature-branch closure evidence and truthfully records that integration was pending at that checkpoint. `access-auth-integration-acceptance-2026-09-04.md` records the accepted combined candidate and later post-merge closure evidence without rewriting its original chronology.

## Permanent rules

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
APPLIED MIGRATION HISTORY IS IMMUTABLE
NO PASS WITHOUT EXECUTED EVIDENCE
LOCAL RECOVERY PASS != PRODUCTION/CLOUD RECOVERY PASS
```
