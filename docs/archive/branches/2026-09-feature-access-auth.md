# Branch history — feature/access-auth

> Historical branch record. **NON-AUTHORITATIVE for current project state.**
> Current truth lives in protected-main/live Git, current Access/Auth and Email architecture/database references, executable code/migrations/tests, `docs/PROJECT-STATUS.md`, and the PostgreSQL Recovery operator runbook.

## Identity

- Repository: `MattiaRubino/dante`
- Original feature branch: `feature/access-auth`
- Original protected-main anchor: `f011e252b6a294a12c38927ef2d528244ea1fee6`
- Feature-work closure checkpoint before integration cleanup: `deba7781ffd3567440232f4d72cbcd138231399a`
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

## Database evolution and integration

The feature branch evolved from the common CP6 head through:

```text
20260826_08
→ 20260827_09  Account / EmailIdentity / PasswordCredential / AuthSession
→ 20260827_10  Account security-lock capability
→ 20260829_11  signup/recovery challenge persistence
→ 20260830_12  multi-authenticator / Apple / WebAuthn persistence
→ 20260831_13  authenticator-lifecycle ACL follow-up
→ 20260903_14  shared Email Platform persistence
→ 20260903_15  Email Platform exact runtime ACL hardening
→ 20260904_16  Email Platform forward vocabulary/current contract
```

Protected-main Recovery independently evolved from the same CP6 parent at `20260830_09`. The two accepted histories were preserved as siblings and joined without rewriting either history:

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

## Important real-UAT defects and repairs retained from branch closure

Manual UAT exposed issues that automated tests had not initially caught and that remain useful engineering history:

1. **AuthSession rotation/read race** — an in-flight session read could overwrite freshly rotated authoritative session state. The application boundary was hardened to cancel the exact stale read before committing the new session state.
2. **Cross-chunk remote-error identity** — lazy/chunk boundaries could break remote-error classification; the boundary handling was hardened.
3. **WebAuthn response-envelope mismatch** — frontend code consumed flattened ceremony options while the backend correctly returned `ceremony.options.publicKey`; the adapter/tests were corrected and real Windows Hello then passed.

Real Google UAT used a third-party mailbox. DANTE correctly required direct DANTE mailbox proof rather than treating provider authentication or provider email as sufficient Account/link authority. Direct database inspection proved a passwordless Google-created Account with verified EmailIdentity, active Google ExternalIdentity and active AuthSession.

The first real SES attempt exposed a Botocore temporary browser-login credential-refresh region defect. DANTE classified the uncertain operation as `ambiguous` and did not blind retry. The SES adapter was repaired to construct a region-bound `boto3.Session`; focused unit coverage protects that path. Final SES UAT then proved signup verification, recovery/reset, prior-session revocation and reset notification delivery, with provider message IDs recorded and sensitive delivery material wiped after acceptance.

Apple registered-domain real UAT was not executable because the required external account/domain prerequisites were unavailable. Engineering acceptance is historical fact; real Apple PASS is **not** claimed.

## Shared Email Platform carry-forward rules

The workstream evolved the original process-memory delivery slice into shared DANTE infrastructure:

```text
feature/application state
+ durable EmailIntent
→ PostgreSQL COMMIT
→ claim / lease / bounded worker
→ protected payload + versioned template
→ provider-neutral adapter
→ provider evidence / suppression
```

Persistence added:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Permanent rules retained by current subsystem authority:

```text
provider accepted != delivered
no provider I/O in caller transaction
operation-scoped idempotency + immutable fingerprint
no blind retry after ambiguous provider outcome
short-lived AES-256-GCM protected sensitive payload
terminal/unsafe-state secret wipe
provider feedback != canonical Account truth
Email Platform is shared infrastructure; Access/Auth is its first consumer only
```

## Recovery evidence boundary discovered after integration

The integration candidate ran the existing CP07 whole LOCAL PostgreSQL recovery rehearsal against the enriched `20260904_17` topology and directly proved database/PITR, structural/security acceptance and MaterialState anti-resurrection behavior.

A post-merge red-team audit identified a narrower cross-subsystem acceptance gap: the CP07 harness did **not** directly exercise the shared Email Platform's `quarantine_after_restore()` path before Email workers resume. The Email quarantine implementation and its direct PostgreSQL test exist, but the whole recovery/reopen rehearsal did not prove their ordering as one end-to-end restore scenario.

Therefore the historical CP07 result remains valid for the PostgreSQL/database-local and MaterialState scope it actually executed, but this archive must not be used to claim that application Email traffic reopen after PITR was already end-to-end proven. That remediation is a separate forward protected-main change; history is not rewritten to pretend it was part of PR #52.

## Production items deliberately not claimed

Feature closure/integration did not equal deployment acceptance for:

```text
Apple real registered-domain UAT
DANTE production sender domain
SPF / DKIM / DMARC
SES production quota/reputation posture
production workload identity
live cloud provider-event ingress
production observability release integration
Native Mobile
later session/device/security-event maturity
remote/cloud backup provider activation
production recovery acceptance / production RPO-RTO
```

Those remain future bounded gates where applicable.

## Documentation lifecycle disposition

Temporary live/session Access handoffs were removed before integration after knowledge coverage. During final post-merge reconciliation:

```text
current truth        → protected-main status/roadmap/subsystem references
normative rules      → Access/Auth + Email architecture/database references
validation evidence  → retained dated M5/integration acceptance records
branch chronology    → this single NON-AUTHORITATIVE archive record
future requirements  → roadmap/current subsystem owners
pure planning history→ Git history
```

The former active `docs/workstreams/access-auth.md`, the obsolete M4–M7 execution-plan overlay and the superseded pre-integration branch-closure record were removed after this coverage transfer. The detailed `access-auth-m5-review-2026-09-02.md` and `access-auth-integration-acceptance-2026-09-04.md` remain as historical **EVIDENCE / VALIDATION**, not branch-operational or current-authority documents.

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
