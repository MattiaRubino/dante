# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current repository state

Protected `main` remains the integration authority. The accepted integration candidate is `integration/access-auth-main-20260904`, which contains protected-main Recovery plus Access/Auth M1–M5 and the shared Email Platform.

```text
PRODUCT / DOMAIN / LOGICAL / PHYSICAL      CLOSED / CURRENT
ENGINEERING / FRONTEND / BACKEND CP1–CP6  CLOSED / ACCEPTED
POSTGRESQL                                 18.6

PROTECTED MAIN
  Recovery                                 CLOSED / INTEGRATED
  Alembic                                  20260830_09

INTEGRATION CANDIDATE
  branch                                   integration/access-auth-main-20260904
  accepted proof HEAD                      81639c61478b476c995652d0060dde8f53aef089
  Access/Auth M1–M5                        CLOSED / ACCEPTED
  Shared Email Platform                    CLOSED / ACCEPTED
  Windows Hello / Google / SES real UAT    PASS
  Apple registered-domain UAT              BOUNDED DEFERRED / NON-BLOCKING
  Recovery from main                       INCLUDED
  Alembic                                  20260904_17
  DB topology                              88 tables / 5 views / 16 routines /
                                           76 triggers / 172 indexes / 89 FKs /
                                           270 CHECKs
  combined CI                              PASS
  CP07 whole LOCAL recovery rehearsal      PASS
  current work                             READY FOR PROTECTED-MAIN MERGE

M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

`20260904_17` is a no-DDL forward Alembic merge revision with parents `20260830_09` and `20260904_16`. Neither accepted migration history was rewritten.

The accepted CP07 rehearsal on exact proof HEAD `81639c61478b476c995652d0060dde8f53aef089` proved the integrated `20260904_17` database contract, deterministic PITR, anti-resurrection reconciliation, rejected protected-payload reinsertion and `DATABASE LOCAL REOPEN = PASS`. Remote backup provider activation and production/cloud recovery remain **NOT CLAIMED**.

Durable integration evidence lives in `docs/workstreams/access-auth-integration-acceptance-2026-09-04.md`.

## Permanent architecture rules

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
provider identity = issuer + subject
provider email != Account/link authority
passwordless Account valid
PasskeyCredential != Account
PostgreSQL is canonical persistence
no provider/network I/O inside authoritative DB transactions
no blind retry after ambiguous external effects
applied migrations are immutable
```

The Email Platform is shared DANTE infrastructure; Access/Auth is its first consumer, not its owner.

## Current integration order

```text
accepted Recovery + Access/Auth + Email candidate
→ PR #52 to protected main
→ post-merge main verification and current-authority reconciliation
→ enriched main into feature/platform-observability
→ observability integration/release rechecks
→ PR observability to protected main
→ future bounded workstreams from enriched main
```

No rebase, history rewrite, force push or direct protected-main write.

## Documentation entry points

- `docs/PROJECT-STATUS.md`
- `docs/ROADMAP.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- `docs/workstreams/access-auth.md`
- `docs/workstreams/access-auth-integration-acceptance-2026-09-04.md`
- `docs/architecture/email-platform.md`
- `docs/operations/postgres-recovery-runbook.md`
- `apps/backend/README.md`

Executable repository truth and accepted current documentation outrank conversation memory and historical handoffs.
