# Branch history — feature/access-auth

> Historical branch record. **NON-AUTHORITATIVE for current project state.**
> Current truth lives in protected-main/live Git, current Access/Auth and Email architecture/database references, executable code/migrations/tests, `docs/PROJECT-STATUS.md`, and the PostgreSQL Recovery operator runbook.

## Identity

- Repository: `MattiaRubino/dante`
- Original feature branch: `feature/access-auth`
- Final feature-branch HEAD before isolated integration: `f2845238091c0c7d445709446a5acac1d14fa9ca`
- Integration branch: `integration/access-auth-main-20260904`
- Accepted implementation proof HEAD: `81639c61478b476c995652d0060dde8f53aef089`
- Final integration candidate HEAD: `6cee5506d404d0684b0679aca54c03f0ca433c72`
- Protected-main base before Access integration: `fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282`
- Integration preparation PR: `#51`
- Protected-main integration PR: `#52`
- Protected-main merge commit: `5f76ec54ad78542f137e8730e904f805d9e59e56`
- PostgreSQL: 18.6
- Integrated Alembic head: `20260904_17`
- Integrated topology: `88|5|16|76|172|89|270|0|0|0`

Branch/worktree names above are historical phase evidence only. They are not continuation authorities after PR #52.

## Protected-main integration result

```text
feature/access-auth final HEAD        f2845238091c0c7d445709446a5acac1d14fa9ca
accepted implementation proof         81639c61478b476c995652d0060dde8f53aef089
final integration candidate            6cee5506d404d0684b0679aca54c03f0ca433c72
integration PR                          #52
merge method                            normal merge commit
protected-main merge                    5f76ec54ad78542f137e8730e904f805d9e59e56
result                                  MERGED INTO PROTECTED main
```

The merge commit has two parents — the prior protected main and the final integration candidate — and its tree is identical to the final candidate tree. Backend and Frontend CI subsequently passed on the exact protected-main merge commit.

## Delivered scope

The workstream delivered and closed Access/Auth M1–M5 plus the shared Email Platform foundation:

```text
M1 Visual / UX                              CLOSED / INTEGRATED
M2 Auth architecture                        CLOSED / INTEGRATED
M3 Signin + AuthSession                     CLOSED / INTEGRATED
M4 Signup/recovery/reset/reauth             CLOSED / INTEGRATED
M5 Multi-authenticator Account              CLOSED / INTEGRATED
Google                                      REAL UAT PASS
Windows Hello / passkeys                    REAL UAT PASS
Apple backend/grant/notifications           ENGINEERING PASS
Apple registered-domain UAT                 BOUNDED DEFERRED / NON-BLOCKING
Shared Email Platform                       CLOSED / INTEGRATED
SES signup/recovery/reset notification      REAL UAT PASS
```

Permanent semantic constitution carried into current authority:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email != Account/link authority
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
method != factor != assurance
reauthentication != signin
```

## Database integration

Access/Auth + Email and Recovery evolved from the same accepted CP6 parent and were preserved as separate forward histories:

```text
20260826_08
├── 20260830_09 Recovery
└── 20260827_09
    → 20260827_10
    → 20260829_11
    → 20260830_12
    → 20260831_13
    → 20260903_14
    → 20260903_15
    → 20260904_16 Access/Auth + Email

20260830_09 + 20260904_16
            ↓
        20260904_17
```

`20260904_17` is a no-DDL merge revision. Neither accepted history was rebased, renumbered, flattened or rewritten.

Integrated protected-main database contract at closure:

```text
PostgreSQL          18.6
Alembic             20260904_17
tables              88
views                5
routines             16
triggers             76
physical indexes     172
foreign keys         89
CHECK constraints    270
```

Real PostgreSQL acceptance proved Dictionary / SQLAlchemy / Alembic / live-catalog reconciliation, Access/Auth persistence and concurrency behavior, Email Platform persistence/ACL behavior, Recovery retirement integrity, and convergence from both the prior Access head and prior Recovery head to the single merge head.

## Recovery evidence boundary discovered after integration

The integration candidate ran the existing CP07 whole LOCAL PostgreSQL recovery rehearsal against the enriched `20260904_17` topology and directly proved database/PITR, structural/security acceptance and MaterialState anti-resurrection behavior.

A post-merge red-team audit identified a narrower cross-subsystem acceptance gap: the CP07 harness did **not** directly exercise the shared Email Platform's `quarantine_after_restore()` path before Email workers resume. The Email quarantine implementation and its direct PostgreSQL test exist, but the whole recovery/reopen rehearsal did not prove their ordering as one end-to-end restore scenario.

Therefore the historical CP07 result remains valid for the PostgreSQL/database-local and MaterialState scope it actually executed, but this archive must not be used to claim that application Email traffic reopen after PITR was already end-to-end proven. That remediation is a separate forward protected-main change; history is not rewritten to pretend it was part of PR #52.

## Documentation lifecycle disposition

Temporary live/session Access handoffs had already been removed before integration. After PR #52, the active `docs/workstreams/access-auth.md` and execution-plan overlay were no longer valid current authorities and were retired during post-merge reconciliation.

Durable dated evidence may remain under `docs/workstreams/` where explicitly historical, including closure/review/integration acceptance records. Those records do not override current executable or current-reference truth.

## Deliberately later

The completed Access workstream did not absorb later maturity work:

```text
M6 Native Mobile
session/device inventory
remote session management
security event center / "this wasn't me"
future Access polish
Apple real registered-domain UAT when prerequisites exist
production Email sender/domain deployment
remote/cloud backup-provider deployment and production recovery acceptance
```

This archive preserves chronology only. Use current protected-main authority for continuation decisions.
