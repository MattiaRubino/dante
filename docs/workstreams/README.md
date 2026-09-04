# DANTE Workstream Records

- **Status:** CURRENT INDEX
- **Last reconciled:** 2026-09-04
- **Rule:** protected `main` stores durable current records/evidence, not active chat/session handoffs

## Current project state

```text
Product / Domain / Logical / Physical            CLOSED / CURRENT
Engineering / Frontend / Backend CP1–CP6        CLOSED / ACCEPTED
PostgreSQL                                       18.6
Protected-main Recovery                          CLOSED / INTEGRATED

Access/Auth M1–M5                                CLOSED / ACCEPTED
Shared Email Platform                            CLOSED / ACCEPTED / OWNERSHIP VERIFIED
Google / Windows Hello / SES real UAT            PASS
Apple registered-domain UAT                      BOUNDED DEFERRED / NON-BLOCKING

integration/access-auth-main-20260904
  proof HEAD                                     81639c61478b476c995652d0060dde8f53aef089
  main Recovery                                  INCLUDED
  Alembic                                        20260904_17
  topology                                       88/5/16/76/172/89/270
  combined CI                                    PASS
  CP07 whole LOCAL recovery                      PASS
  state                                          READY FOR PROTECTED-MAIN MERGE

feature/platform-observability                   CLOSED / OPERATIONAL PASS / NOT INTEGRATED
M6 Native Mobile                                 FUTURE / OPTIONAL
later M7 Access/security maturity                FUTURE
```

## Current Access/Auth authority

- `access-auth.md`
- `access-auth-integration-acceptance-2026-09-04.md`
- `../PROJECT-STATUS.md`
- `../ROADMAP.md`
- `../database/README.md`
- `../database/access-auth.md`
- `../architecture/access-auth-*.md`
- `../architecture/email-platform.md`
- `../operations/postgres-recovery-runbook.md`
- `../development/email-platform-acceptance-2026-09-03.md`

M5 is closed. Apple real external UAT is an explicit bounded deferral, not a PASS. CP07 is a LOCAL operator-recovery PASS, not production/cloud recovery acceptance.

## Documentation lifecycle

Temporary Access/Auth handoffs were removed after knowledge coverage. Durable review/closure/integration evidence may remain, but historical checkpoints never override current executable/current-reference truth.

The old `access-auth-m4-m7-execution-plan.md` is historical planning; current execution order is owned only by `../ROADMAP.md` and `access-auth.md`.

## Current integration order

```text
accepted Access/Auth + Recovery + Email candidate
→ protected-main PR #52
→ post-merge main verification + current-document reconciliation
→ enriched main into feature/platform-observability
→ observability release rechecks
→ protected-main PR
→ future bounded workstreams
```

## Closed durable records

Backend/database history is retained through current DB authority plus archive/Git chronology. Frontend/engineering/domain/logical historical workstream records remain evidence only unless explicitly marked current.

`access-auth-closure-2026-09-03.md` remains historical feature-branch closure evidence and must continue to say integration was pending at that historical checkpoint. `access-auth-integration-acceptance-2026-09-04.md` is the durable record for the accepted combined candidate immediately before protected-main integration.

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
