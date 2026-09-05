# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current repository state

Protected `main` is the single integrated authority. Access/Auth M1–M5, the shared Email Platform and PostgreSQL Recovery are integrated through PR #52; post-restore Email replay hardening and the whole-flow CP08 recovery gate are integrated through PR #55.

```text
PRODUCT / DOMAIN / LOGICAL / PHYSICAL      CLOSED / CURRENT
ENGINEERING / FRONTEND / BACKEND CP1–CP6  CLOSED / ACCEPTED
POSTGRESQL                                 18.6

PROTECTED MAIN
  Access/Auth M1–M5                        CLOSED / INTEGRATED
  Shared Email Platform                    CLOSED / INTEGRATED
  Recovery                                 CLOSED / INTEGRATED
  Windows Hello / Google / SES real UAT    PASS
  Apple registered-domain UAT              BOUNDED DEFERRED / NON-BLOCKING
  Alembic                                  20260904_17
  DB topology                              88 tables / 5 views / 16 routines /
                                           76 triggers / 172 indexes / 89 FKs /
                                           270 CHECKs
  post-merge Backend CI                    PASS
  post-merge Frontend CI                   PASS
  database-local CP07                      PASS
  Email/application reopen CP08            PASS

feature/platform-observability             CLOSED / OPERATIONAL PASS / NEXT INTEGRATION
M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

`20260904_17` is a no-DDL forward Alembic merge revision with parents `20260830_09` and `20260904_16`. Neither accepted migration history was rewritten.

PR #52 merged the accepted Access/Auth + shared Email Platform candidate with protected-main Recovery at merge commit `5f76ec54ad78542f137e8730e904f805d9e59e56`. The merge tree is identical to the accepted final candidate tree, and protected-main Backend/Frontend CI passed after the merge.

The historical CP07 rehearsal on implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` proved the integrated `20260904_17` database contract, deterministic PITR, MaterialState anti-resurrection reconciliation, rejected protected-payload reinsertion and `DATABASE LOCAL REOPEN = PASS` for the scope it executed. It did not directly exercise Email post-restore quarantine before worker resume; that historical evidence boundary is retained rather than rewritten.

PR #55 then integrated the forward Recovery↔Email hardening at merge commit `c67a18c24a6cf22b003ffd2c14243af53fec5077`. CP08 ran on proof head `1a5a7f1fbbdc1e5723d58fa90721a8693cce49e9` and directly proved PITR into resurrected sendable Email state, fail-closed quarantine of `pending` / `claimed` / `retryable_failure`, `in_progress` attempt conversion to `ambiguous`, sensitive-material wipe, idempotent second reconciliation, `0` claimable Email work after reconciliation and `APPLICATION / EMAIL REOPEN = PASS`. Remote backup-provider activation and production/cloud recovery remain **NOT CLAIMED**.

Durable historical integration evidence lives in `docs/workstreams/access-auth-integration-acceptance-2026-09-04.md`. Consolidated Access branch chronology lives in `docs/archive/branches/2026-09-feature-access-auth.md` and is **NON-AUTHORITATIVE**.

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
restored external-effect work is not automatically safe to replay
applied migrations are immutable
```

The Email Platform is shared DANTE infrastructure; Access/Auth is its first consumer, not its owner.

## Current integration order

```text
enriched protected main
→ merge into feature/platform-observability
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
- `docs/architecture/access-auth-architecture.md`
- `docs/database/access-auth.md`
- `docs/architecture/email-platform.md`
- `docs/operations/postgres-recovery-runbook.md`
- `docs/workstreams/access-auth-integration-acceptance-2026-09-04.md` — historical evidence
- `docs/archive/branches/2026-09-feature-access-auth.md` — historical branch record
- `apps/backend/README.md`

Executable repository truth and accepted current documentation outrank conversation memory and historical handoffs.
