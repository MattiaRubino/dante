# DANTE — Project Status

- **Status:** CURRENT TRUTH FOR `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Protected `main`:** integrated shared-foundation + Recovery authority at `20260830_09`; Access/Auth is not integrated yet
- **Active branch:** `feature/access-auth`
- **Current macro state:** **M5 CLOSED / ACCEPTED; PRE-INTEGRATION AUDIT ACTIVE**
- **Current branch Alembic head:** `20260903_15`
- **Protected-main Alembic head:** `20260830_09`
- **Email Platform:** ENGINEERING + REAL-PROVIDER UAT CLOSED

## 1. Current state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
PostgreSQL                                 18.6

Access M1 Visual / UX Freeze               CLOSED / ACCEPTED
Access M2 Auth Architecture Freeze         CLOSED / ACCEPTED
Access M3 Signin + AuthSession             CLOSED / ACCEPTED
Access M4 Lifecycle / Recovery / Reauth    CLOSED / ACCEPTED
Access M5 Multi-authenticator Account      CLOSED / ACCEPTED

M5 persistence / Google / Apple backend    COMPLETE / ENGINEERING PASS
M5 authenticator lifecycle/passwordless    COMPLETE / ENGINEERING PASS
M5 passkeys / WebAuthn                     COMPLETE / ENGINEERING PASS
M5 FastAPI/OpenAPI/generated client        COMPLETE / ENGINEERING PASS
M5 Web product engineering                 AUTOMATED QA PASS
local password/passkey UAT                 PASS
real Windows Hello UAT                     PASS
real Google UAT                            PASS
real Apple registered-domain UAT           BOUNDED DEFERRED / NON-BLOCKING

Shared Email Platform                      CLOSED / ACCEPTED
real SES signup UAT                        PASS
real SES recovery UAT                      PASS
real reset-notification UAT                PASS

M6 Native Mobile                           FUTURE / OPTIONAL / RE-GATE
M7 later Access/security maturity          FUTURE / NOT STARTED HERE
```

Apple is not reported as PASS. Real Apple Web UAT remains a future release/enablement prerequisite when a usable Apple account and registered HTTPS domain exist. The user explicitly accepted that bounded deferral; it does not keep M5 open.

## 2. Current branch database truth — before main convergence

`feature/access-auth` currently materializes:

```text
PostgreSQL          18.6
Alembic             20260903_15
tables              87
views                5
routines             15
triggers             75
physical indexes     170
foreign keys         88
CHECK constraints    267
```

Access/Auth + Email migration line:

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

Protected `main` has independently advanced from the same CP6 head through Recovery:

```text
20260826_08
→ 20260830_09  recovery_material_state_retirement
```

Protected-main current topology is separately documented in `database/README.md` on `main` as `69/5/15/76/97/69/123`.

These two lines are intentionally **divergent before integration**. No document may pretend Recovery is already present on `feature/access-auth`, or that Access/Auth is already present on protected `main`.

## 3. Access/Auth constitution

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
frontend/provider/browser completion != backend-authoritative success
```

These remain closed architecture rules and are not reopened by branch integration.

## 4. Shared Email Platform closure

The Email Platform is shared DANTE infrastructure; Access/Auth is its first consumer, not its owner.

Accepted platform truth:

```text
PostgreSQL transactional EmailIntent
feature mutation + EmailIntent atomicity
provider I/O after commit
claim / lease / FOR UPDATE SKIP LOCKED
operation-scoped idempotency + fingerprint
explicit ambiguous outcome
no blind retry after ambiguity
AES-256-GCM protected short-lived payload
terminal/unsafe-state secret wipe
Amazon SES API v2 primary external adapter
SMTP local/CI compatibility adapter
provider-event + suppression persistence
privacy-minimized observability
```

Final real SES UAT directly proved signup verification, password recovery, password-reset notification, no auto-login after reset and revocation of a previously authenticated session. Runtime produced three `provider_accepted` attempts, all attempt 1; direct PostgreSQL inspection observed provider MessageId and terminal secret wipe for all three.

Exact evidence: `development/email-platform-acceptance-2026-09-03.md`.

One explicit non-claim remains: the exact same consumed recovery URL was not manually reopened a second time in the final live run.

## 5. Production email boundary

Engineering closure does not claim production sender deployment. Future deployment still owns, as applicable:

```text
DANTE-controlled sender domain/subdomain
SPF / DKIM / DMARC
production workload identity
SES production account/quota/reputation posture
live cloud provider-event ingress
production alerting/SLOs
traffic/reputation segmentation
Apple Private Email Relay sender-domain compatibility
```

These are deployment gates, not an invitation to create another mail subsystem.

## 6. Current work — pre-integration audit

No new M7/M6 feature work is authorized on this branch before integration.

The active sequence is:

```text
A. close documentation lifecycle debt
B. reconcile current DB reference / Dictionary / mappings / Alembic / tests
C. prove feature/access-auth internally coherent at 20260903_15
D. merge protected main into feature/access-auth without rewriting history
E. resolve the two Alembic heads with a forward merge revision
F. prove the combined Recovery + Access/Auth + Email database/application
G. PR feature/access-auth → protected main
H. only then integrate the already-closed platform-observability branch
```

The objective is to return shared foundations to protected `main` so other workstreams can start from canonical common infrastructure instead of depending on long-lived feature branches.

## 7. Integration safety

Permanent rules:

```text
no rebase/history rewrite
no force push
no direct protected-main write
applied migrations immutable
no blind Alembic branch flattening
no schema fact accepted without Dictionary/mapping/migration/PG/test parity
no PASS without executed evidence
```

The future Alembic integration must preserve both already-applied histories and use a normal forward merge revision after the main line is merged into this branch.

## 8. Documentation authority

Current operational routing:

1. `PROJECT-STATUS.md`
2. `ROADMAP.md`
3. `workstreams/access-auth.md`
4. `database/README.md`
5. `database/access-auth.md`
6. `database/dictionary/`
7. `architecture/access-auth-*.md`
8. `architecture/email-platform.md`
9. `development/email-platform-acceptance-2026-09-03.md`
10. executable code / migrations / tests / real PostgreSQL

Historical reviews remain evidence only. Temporary branch handoffs must be removed before protected-main integration under `development/documentation-lifecycle-policy.md`.