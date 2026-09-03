# DANTE — Access/Auth Full-Stack Workstream

- **Status:** **M1–M5 CLOSED / ACCEPTED — PRE-INTEGRATION AUDIT ACTIVE**
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Branch Alembic head:** `20260903_15`
- **Protected-main Alembic head:** `20260830_09`
- **Architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Exact persistence/API authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Shared Email Platform authority:** `../architecture/email-platform.md`
- **Real Email evidence:** `../development/email-platform-acceptance-2026-09-03.md`

> Access/Auth feature development is frozen for integration. Do not add M6/M7 scope here before this branch converges with protected main and is integrated.

## 1. Closure state

```text
M1 Visual / UX                             CLOSED / ACCEPTED
M2 Auth architecture                       CLOSED / ACCEPTED
M3 Signin + AuthSession                    CLOSED / ACCEPTED
M4 Signup/recovery/reset/reauth            CLOSED / ACCEPTED
M5 Multi-authenticator Account             CLOSED / ACCEPTED

M5 persistence                             POSTGRESQL PROVEN
Google                                     ENGINEERING + REAL UAT PASS
Apple backend/grant/notifications          ENGINEERING PASS
Apple real registered-domain UAT           BOUNDED DEFERRED / NON-BLOCKING
Passkeys / WebAuthn                        ENGINEERING + WINDOWS HELLO UAT PASS
Authenticator lifecycle / anti-lockout     PASS
FastAPI / OpenAPI / generated client       PASS
Access Web automated QA                    PASS

Shared Email Platform                      CLOSED / ACCEPTED
Real SES signup/recovery/reset notification PASS
```

Apple is not a real-provider PASS. The required external prerequisites are unavailable, so the user explicitly accepted a bounded deferral for M5 closure. Apple must receive real external acceptance before future production enablement.

## 2. Frozen Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived, never persisted
multiple AuthSessions normal
provider identity = issuer + subject
provider email != Account/link authority
provider auth != provider-data authorization
provider assertion/token != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
method != factor != assurance
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Do not reopen these rules absent direct defect evidence and a new explicit architecture gate.

## 3. Accepted product evidence

Observed automated/live proof includes:

```text
password signin/logout + reload authority
password reauth + session bearer rotation
signup / OTP verification
recovery / reset / no-auto-login
post-reset prior-session revocation
real Windows Hello passkey registration/use/reauth/signin
passkey rename/remove + final-authenticator anti-lockout
password remove/re-establish
real Google passwordless Account flow
issuer + subject ExternalIdentity authority
canonical AuthSession convergence
```

Manual UAT also found and closed three important defects: AuthSession read/rotation race, cross-chunk remote-error classification, and WebAuthn response-envelope mismatch. The detailed checkpoint remains in `access-auth-m5-review-2026-09-02.md` as evidence.

## 4. Shared Email Platform

Email is shared DANTE infrastructure; Access/Auth is its first consumer, not its architectural owner.

```text
feature/Auth mutation
+ durable EmailIntent
→ PostgreSQL COMMIT
→ claim / lease / worker
→ protected payload + versioned template
→ provider-neutral adapter
→ SES API v2 / SMTP local-CI compatibility
→ provider evidence / suppression
```

Permanent rules:

```text
provider I/O outside caller transaction
provider accepted != delivered
no blind retry after ambiguous outcome
operation-scoped idempotency + immutable fingerprint
short-lived AES-256-GCM protected payload
terminal/unsafe-state payload wipe
Auth/security tracking and link rewriting OFF
```

Final 2026-09-03 UAT proved real signup verification, password recovery and reset notification through SES. All three accepted attempts had provider MessageId and terminal sensitive-payload wipe in PostgreSQL.

One explicit manual non-claim remains: the exact consumed recovery URL was not manually reopened a second time.

## 5. Branch-local database truth

Before merging main:

```text
PostgreSQL          18.6
Alembic             20260903_15
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
```

Current branch migration line:

```text
20260826_08
→ 20260827_09
→ 20260827_10
→ 20260829_11
→ 20260830_12
→ 20260831_13
→ 20260903_14
→ 20260903_15
```

Protected main independently contains Recovery:

```text
20260826_08
→ 20260830_09 recovery_material_state_retirement
```

The two histories must remain intact and later converge through a forward Alembic merge revision. Applied migrations are immutable.

## 6. Current work: pre-integration audit only

Authorized work before the merge:

```text
reconcile documentation lifecycle
remove temporary/duplicate branch handoffs after knowledge coverage
mark evidence as evidence, not current status
repair stale current references
verify Blueprint / Physical / Constitution consistency
verify Database Dictionary / scope/schema consistency
verify SQLAlchemy mappings
verify Alembic DAG/head and ACL
verify real PostgreSQL catalog/test parity
verify backend/Web/OpenAPI generated-client regressions
```

No new feature work belongs in this branch during the audit.

## 7. Integration sequence

After branch-internal audit is green:

```text
1. merge protected main into feature/access-auth
2. preserve Recovery and Access/Auth migration histories
3. add one forward Alembic merge revision
4. reconcile combined Dictionary / mappings / database reference
5. run fresh-database + migration + PostgreSQL + backend + Web gates
6. PR feature/access-auth → protected main
7. update protected main
8. merge enriched main into feature/platform-observability
9. run observability integration/release rechecks
10. PR platform-observability → protected main
```

No rebase, history rewrite, force push or direct protected-main write.

## 8. What deliberately waits

Do not block current integration on:

```text
M6 Native Mobile
session/device inventory
remote session management
security event center / "this wasn't me"
future Access polish
future Apple real UAT until prerequisites exist
production email domain/DNS/reputation deployment
```

Those can use fresh bounded branches from the later enriched protected main.

## 9. Documentation authority

Current operational truth:

```text
../PROJECT-STATUS.md
../ROADMAP.md
this file
../database/README.md
../database/access-auth.md
../architecture/access-auth-*.md
../architecture/email-platform.md
../development/email-platform-acceptance-2026-09-03.md
../development/documentation-lifecycle-policy.md
```

Historical reviews/checkpoints never override current executable/current-reference truth.