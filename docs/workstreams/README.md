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
Shared Email Platform                            CLOSED / ACCEPTED
Google / Windows Hello / SES real UAT            PASS
Apple registered-domain UAT                      BOUNDED DEFERRED / NON-BLOCKING

integration/access-auth-main-20260904
  main Recovery                                  INCLUDED
  Alembic                                        20260904_17
  topology                                       88/5/16/76/172/89/270
  state                                          COMBINED INTEGRATION QA ACTIVE

feature/platform-observability                   CLOSED / OPERATIONAL PASS / NOT INTEGRATED
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
- `../development/email-platform-acceptance-2026-09-03.md`

M5 is closed. Apple real external UAT is an explicit bounded deferral, not a PASS.

## Documentation lifecycle

Temporary Access/Auth handoffs were removed after knowledge coverage. Durable review/closure evidence may remain, but historical checkpoints never override current executable/current-reference truth.

The old `access-auth-m4-m7-execution-plan.md` is historical planning; current execution order is owned only by `../ROADMAP.md` and `access-auth.md`.

## Current integration order

```text
combined Access/Auth + Recovery + Email QA
→ protected-main PR
→ enriched main into feature/platform-observability
→ observability release rechecks
→ protected-main PR
→ future bounded workstreams
```

## Closed durable records

Backend/database history is retained through current DB authority plus archive/Git chronology. Frontend/engineering/domain/logical historical workstream records remain evidence only unless explicitly marked current.

## Permanent rules

```text
SELECTED != IMPLEMENTED != PASS != REAL UAT != PRODUCTION DEPLOYED
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
CURRENT SPECIFICATION != APPEND-ONLY DIARY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
APPLIED MIGRATION HISTORY IS IMMUTABLE
NO PASS WITHOUT EXECUTED EVIDENCE
```
