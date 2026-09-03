# DANTE System Overview

- **Status:** CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW
- **Last reconciled:** 2026-09-03
- **Backend foundation:** CP1–CP6 CLOSED / integrated / directly validated
- **Current PostgreSQL:** 18.6
- **Current Access/Auth Alembic head:** `20260903_15`
- **Current branch work:** `feature/access-auth` / M5 final closure reconciliation
- **Shared Email Platform:** ENGINEERING + REAL SES UAT ACCEPTED

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

North Star execution loop:

```text
Understand
→ Discover
→ Orchestrate
→ Decide
→ Plan & Coordinate
→ Act
→ Observe
→ Learn & Adapt
```

Permanent semantic constraints include:

```text
reality != plan
inference != fact
Effort != Execution != Outcome != Goal progress
unknown != false
Person != Account != Principal != Actor
provider state != canonical DANTE state
derived projection != canonical truth
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI/solver output != accepted canonical effect
client local state != canonical accepted effect
```

Implementation consumes the closed Product/Domain/Logical/Physical authorities. Framework/storage convenience does not redefine accepted semantics.

## 2. Repository / application topology

One product monorepo:

```text
DANTE repository
│
├── apps/backend
├── apps/web
├── apps/mobile
├── packages
├── infra
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Backend accepted internal posture is a capability-first modular monolith with explicit application transaction ownership and provider/ORM/HTTP details kept outside semantic authority.

## 3. Foundation state

```text
Engineering Foundation                  CLOSED / ACCEPTED
Frontend Foundation                     CLOSED / ACCEPTED
Backend CP1–CP6                         CLOSED / ACCEPTED
PostgreSQL 18.6                         CURRENT
schema dante                            CURRENT
owner/migrator/runtime privilege split  CURRENT
real PostgreSQL acceptance testing      CURRENT
```

Historical PostgreSQL 18.4 CP2/CP3 evidence remains exact for those runs; current repository patch is 18.6.

## 4. Canonical persistence authority

```text
PostgreSQL 18 major family
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY
```

Current `feature/access-auth` database:

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

The accepted relational thesis remains:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific typed relation families
+ bounded technical address/control structures where required
+ separate provider / derived / runtime concerns
```

Rejected globally:

```text
universal Entity / Thing
universal Relationship / generic edge
canonical EAV/property bag
universal event ontology
universal Fact/Version semantic payload root
JSONB required-semantic escape hatch
```

## 5. Reference / material-state architecture

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Provider revisions, MVCC tokens, timestamps and ETags do not become MaterialStateRef.

The shared Email Platform persistence is a bounded technical delivery-control subsystem and is **not** MaterialState.

## 6. CP6 — Concrete PostgreSQL Database

CP6 is closed and integrated. It converted closed semantic/physical authority into concrete PostgreSQL and validated the result directly.

Later product work evolves that database through forward Alembic migrations under ADR-010 without rewriting applied CP6 history.

## 7. Access/Auth current architecture

Access/Auth is now a real full-stack capability, not a future backend vertical.

Permanent model:

```text
Account
├── EmailIdentity 1..N
├── PasswordCredential 0..1
├── AuthSession 0..N
├── ExternalIdentity 0..N
└── PasskeyCredential 0..N through WebAuthnAccount
```

Core rules:

```text
Person != Account
EmailIdentity != Account
PasswordCredential optional
passwordless Account valid
provider identity = issuer + subject
provider email != linking authority
provider token/assertion != DANTE AuthSession
opaque server-authoritative AuthSession
recent-auth required for sensitive mutation
passkeys use WebAuthn/FIDO2, not custom crypto
```

Current evidence includes local password/session UAT, real Windows Hello/passkey UAT and real Google provider UAT.

## 8. Shared Email Platform

The Email Platform is shared DANTE infrastructure. Access/Auth is the first consumer.

```text
feature/Auth transaction
        │
        ├── canonical state mutation
        └── durable EmailIntent
                 │
                 ▼
          PostgreSQL commit
                 │
                 ▼
         claim / lease / worker
                 │
                 ├── protected payload
                 ├── template rendering
                 ├── retry/ambiguity policy
                 └── provider-neutral adapter
                          │
                          ├── Amazon SES API v2
                          └── SMTP local/CI compatibility
                                   │
                                   ▼
                         provider feedback/events
                                   │
                                   ▼
                     DANTE suppression/observability
```

Current persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Permanent rules:

```text
DANTE owns lifecycle/state
provider owns last-mile transport
provider accepted != delivered
no provider I/O in caller DB transaction
no blind retry after ambiguous send
short-lived AES-GCM protected sensitive payload
terminal/unsafe-state wipe
Auth/security tracking OFF
future consumers reuse platform rather than creating a second mail subsystem
```

## 9. Email Platform acceptance

Final 2026-09-03 real-provider UAT proved:

```text
dedicated non-root AWS UAT principal       PASS
SES eu-west-3 preflight                    PASS
DANTE signup → SES → real mailbox          PASS
received OTP → Account creation            PASS
DANTE recovery → SES → real mailbox        PASS
recovery URL → password reset              PASS
no auto-login                              PASS
prior AuthSession revoked                  PASS
reset security notification → mailbox      PASS
```

Three runtime sends were `provider_accepted`, each on attempt 1.

Direct PostgreSQL UAT inspection observed provider MessageId present and sensitive-payload wipe for signup verification, password recovery and reset notification.

The first live attempt also exposed a real Botocore temporary-credential region-refresh defect; DANTE correctly classified the uncertain send as `ambiguous`, did not blind-retry, and the provider was fixed to propagate region through a boto3 Session. Focused unit coverage now protects this path.

Exact evidence: `../development/email-platform-acceptance-2026-09-03.md`.

## 10. Frontend / client data authority

Frontend Data Authority Matrix remains:

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite noncanonical
offline pending mutation          local staging only
offline acceptance                backend governance/conflict checks
remote request state              TanStack Query + typed API
online governed command           FastAPI/backend
form draft                        TanStack Form
component transient               React
cross-tree transient              Zustand only when justified
```

Local arrival/staging never defines canonical truth.

## 11. Offline / specialist capabilities

Selected targets remain activation-triggered:

```text
PowerSync + encrypted SQLite      when real offline/sync consumer exists
PgBouncer                         when connection-pressure value is proven
PostgreSQL outbox                 ACTIVE for Email Platform Class-A work
Restate                           when real Class-B workflow exists
Cloudflare R2                     when real ContentArtifact byte flow exists
pgBackRest + S3                   recovery/production boundary or rehearsal
OR-Tools                          solver-backed capability
```

## 12. Transactions / migrations / privileges

Current durable posture:

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation
autobegin=False
autoflush=True
expire_on_commit=False
outer application operation owns transaction
adapter may flush / never implicit commit
READ COMMITTED default
one Alembic DAG / one canonical branch head
metadata.create_all() not deployment authority

dante_owner      NOLOGIN
dante_migrator   LOGIN NOINHERIT + bounded SET ROLE
dante_runtime    LOGIN NOINHERIT / least-privilege runtime posture
```

External side effects follow operation-specific idempotency/ambiguity policy rather than blanket retry.

## 13. Recovery posture

Physical recovery uses the accepted pgBackRest/WAL/PITR direction when activated.

Email Platform adds an anti-resurrection obligation:

```text
email workers CLOSED
→ restore
→ recovery reconciliation
→ uncertain restored nonterminal email work = recovery_quarantined
→ sensitive payload wiped
→ reopen workers
```

## 14. Testing / CI

GitHub Actions remains repository-wide CI/CD authority.

Proof layers intentionally separate:

```text
unit/application
architecture/static checks
real PostgreSQL
migration/catalog/ACL
HTTP/OpenAPI/generated client
browser full-stack
real provider/authenticator UAT
real external-delivery UAT
```

A simulated provider never becomes a real-provider acceptance claim.

## 15. Environment / developer posture

Exactly:

```text
LOCAL → DEV → UAT → PROD
```

Environment != Git branch.

Canonical backend semantics remain Linux. Windows development uses the authoritative WSL-backed checkout; divergent Windows/WSL source clones are forbidden.

For local SES UAT, repository-owned tooling provides:

```text
AWS CLI bootstrap
named dante-uat profile
non-root preflight
least-privilege IAM policy template
disposable full-stack harness
real SES/mailbox acceptance procedure
```

Production should use workload identity/IAM role rather than a developer IAM user.

## 16. Current non-claims

```text
EMAIL PLATFORM ENGINEERING                   CLOSED
PRODUCTION EMAIL SENDER DEPLOYMENT           NOT IMPLIED
DKIM/SPF/DMARC PRODUCTION PROOF              OPEN
LIVE AWS FEEDBACK CLOUD INGRESS              DEPLOYMENT GATE
REAL APPLE REGISTERED-DOMAIN UAT             DEFERRED / OPEN
WHOLE M5                                     FINAL CLOSURE RECONCILIATION
M6 NATIVE MOBILE                             FUTURE / OPTIONAL
M7 SECURITY MATURITY/HANDOFF                 PLANNED
```

The exact same consumed recovery URL was not manually reopened in the final Email UAT; do not label that one step manually observed.

## 17. Current execution posture

```text
DOMAIN MODEL          CLOSED
LOGICAL MODEL         CLOSED
PHYSICAL MODEL        CLOSED
BACKEND FOUNDATION    CLOSED
CP6 DATABASE          CLOSED / INTEGRATED
FRONTEND FOUNDATION   CLOSED / INTEGRATED
ACCESS/AUTH M1–M4     CLOSED
ACCESS/AUTH M5        FINAL CLOSURE RECONCILIATION
EMAIL PLATFORM        CLOSED / REAL SES UAT PASS
```

Current general status is owned by `docs/PROJECT-STATUS.md`; branch-local work by `docs/workstreams/access-auth.md`; Email Platform by `email-platform.md` and its acceptance evidence.
