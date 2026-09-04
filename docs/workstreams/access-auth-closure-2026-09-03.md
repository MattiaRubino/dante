# DANTE — Access/Auth Branch Closure Record — 2026-09-03

- **Class:** BRANCH HISTORY / CLOSURE RECORD
- **Authority:** HISTORICAL/EVIDENCE ONLY — current truth lives in status/roadmap/subsystem references
- **Branch:** `feature/access-auth`
- **Original protected-main anchor:** `f011e252b6a294a12c38927ef2d528244ea1fee6`
- **Feature-work closure checkpoint before pre-integration cleanup:** `deba7781ffd3567440232f4d72cbcd138231399a`
- **Current branch state:** feature work CLOSED; pre-integration audit/integration still pending
- **Do not infer:** protected-main integration from this record

## 1. Purpose

This is the single retained human-readable branch history for the Access/Auth workstream. It replaces temporary live/session handoffs that were useful while the branch was active.

It is not current execution authority. Use:

```text
../PROJECT-STATUS.md
../ROADMAP.md
access-auth.md
../database/README.md
../architecture/access-auth-*.md
../architecture/email-platform.md
```

for current truth.

## 2. Scope delivered

The branch turned the accepted Access UX and Auth architecture into a real full-stack Account capability:

```text
M1  Visual / UX freeze
M2  Auth architecture/security/API/testing freeze
M3  email/password signin + canonical AuthSession
M4  signup / email verification / recovery / reset / reauth
M5  Google + Apple backend + passkeys + explicit authenticator lifecycle
    + passwordless Accounts
    + public FastAPI/OpenAPI/generated-client materialization
    + Access Web security management
    + shared durable Email Platform
```

Permanent model retained:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email != linking authority
provider assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
```

## 3. Database evolution on this branch

Starting from the common CP6 head:

```text
20260826_08
→ 20260827_09  Account / EmailIdentity / PasswordCredential / AuthSession
→ 20260827_10  Account security-lock capability
→ 20260829_11  signup/recovery challenge persistence
→ 20260830_12  multi-authenticator / Apple / WebAuthn persistence
→ 20260831_13  authenticator-lifecycle ACL follow-up
→ 20260903_14  shared Email Platform persistence
→ 20260903_15  Email Platform exact runtime ACL hardening
```

Feature-work closure topology before protected-main Recovery convergence:

```text
PostgreSQL          18.6
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
```

Applied migrations are immutable. Protected main independently advanced through Recovery at `20260830_09`; convergence is deliberately left to the explicit post-closure integration gate.

## 4. Automated engineering evidence

Across the accepted implementation checkpoints, evidence included:

```text
backend Ruff / mypy / locked dependency checks
non-PostgreSQL application regression
real PostgreSQL migration/catalog/constraint/ACL suites
Alembic fresh-head + round-trip + drift checks
Web formatting / typecheck / ESLint / architecture checks
Web unit/component suites
HTTPS Auth Playwright across Chromium / Firefox / WebKit
production Web build
deterministic OpenAPI + generated-client checks
backend package build
```

Exact historical counts/checkpoints remain in Git and the retained M5 review/evidence documents; this closure record intentionally does not turn every intermediate count into current status.

## 5. Manual password/session/passkey UAT

Observed live behavior included:

```text
password signin / logout
server-authoritative session across navigation/reload
password reauthentication + bearer rotation
real Windows Hello passkey registration
passkey reauthentication
username-less/discoverable passkey signin
passkey rename persistence
password removal while alternate authenticator remains
final-authenticator removal blocked by backend
password re-establishment + fresh signin
```

The retained passkey label in that UAT was `PC Mattia - Windows`.

## 6. Defects found by real UAT

Manual UAT found three important defects that automated proof had not exposed at the time:

1. **AuthSession rotation/read race** — an in-flight session read could overwrite freshly rotated state. The application boundary was hardened to cancel the exact stale read before committing authoritative new session state.
2. **Cross-chunk remote-error identity** — lazy/chunk boundaries could break remote-error classification; boundary handling was hardened.
3. **WebAuthn response-envelope mismatch** — frontend consumed flattened ceremony options while backend correctly returned `ceremony.options.publicKey`; adapter/tests were corrected and real Windows Hello then passed.

These repairs are why live boundary UAT remains part of DANTE acceptance rather than relying only on mocks/browser automation.

## 7. Real Google UAT

Observed real Google Identity Services chain:

```text
DANTE begin + nonce
→ official Google account interaction
→ real Google ID token
→ backend JWK/signature/issuer/audience/nonce verification
→ issuer + subject identity resolution
→ third-party mailbox classification
→ direct DANTE mailbox proof
→ Account creation
→ canonical AuthSession
```

The tested Google Account used a third-party mailbox, so DANTE correctly refused to infer current mailbox control solely from Google authentication.

Direct database inspection proved a genuinely passwordless Google-created Account with verified EmailIdentity, active Google ExternalIdentity and active AuthSession.

An initial `401 invalid_client` was traced to a manually mistyped public OAuth Client ID; exact-copy correction fixed the UAT without a DANTE code change.

## 8. Apple disposition

Apple backend/protocol/grant/notification engineering was implemented and tested, but real registered-domain Apple UAT was not executable because the required real Apple account + registered HTTPS domain were unavailable.

Final disposition accepted by the user:

```text
engineering implementation       ACCEPTED
real Apple external UAT           NOT EXECUTED
M5 closure blocker                NO
future Apple production enablement requires real UAT
```

This record must never be used to claim a real Apple PASS.

## 9. Shared Email Platform

The original process-memory SMTP delivery slice was evolved into a reusable DANTE-owned lifecycle with specialist last-mile delivery:

```text
feature/application state
+ durable EmailIntent
→ PostgreSQL COMMIT
→ claim / lease / bounded worker
→ protected payload + versioned template
→ provider-neutral adapter
→ Amazon SES API v2 / SMTP local-CI compatibility
→ provider evidence / suppression
```

Persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Important accepted rules:

```text
provider accepted != delivered
no provider I/O in caller transaction
operation-scoped idempotency + immutable fingerprint
no blind retry after ambiguous provider outcome
short-lived AES-256-GCM protected sensitive payload
terminal/unsafe-state secret wipe
provider feedback != canonical Account truth
Email Platform is shared infrastructure; Access/Auth is first consumer only
```

## 10. Real SES UAT

Final 2026-09-03 real-provider UAT used a dedicated non-root AWS UAT principal and SES `eu-west-3`.

Observed:

```text
signup verification email      RECEIVED / OTP USED
password recovery email        RECEIVED / LINK USED
password reset                 PASS
no auto-login after reset      PASS
prior AuthSession revocation   PASS
reset security notification    RECEIVED
```

Runtime recorded exactly three final successful SES attempts as `provider_accepted`, all attempt 1.

Direct disposable PostgreSQL inspection observed for all three intents:

```text
provider_message_id present
error_code NULL
sensitive key/nonce/ciphertext wiped
sensitive_wiped_at present
```

One explicit non-claim: the exact same consumed recovery URL was not manually reopened a second time because the message had already been deleted.

### SES UAT defect and repair

The first live SES attempt exposed a Botocore temporary browser-login credential-refresh region defect. DANTE classified the uncertain operation `ambiguous` and did not blind retry. The SES adapter was repaired to create a region-bound `boto3.Session`, and focused unit coverage protects that path.

## 11. Production items deliberately not claimed

Feature closure does not equal deployment acceptance for:

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
```

Those are future bounded gates, not reasons to keep M5 feature work open.

## 12. Documentation cleanup disposition

Temporary dated handoffs are removed after this record and current references cover their meaningful state. Detailed original handoff text remains recoverable in Git.

The dedicated `access-auth-m5-review-2026-09-02.md` remains because it contains useful direct UAT/deprecation/benchmark evidence beyond ordinary operational handoff content.

## 13. Integration still pending at feature-work closure

This closure record does **not** claim integration.

Required next sequence:

```text
pre-integration documentation/database audit
→ merge protected main into feature/access-auth
→ preserve Recovery + Access/Auth/Email Alembic histories
→ add forward Alembic merge revision
→ combined PostgreSQL/backend/Web proof
→ PR to protected main
```

After that, enriched protected main is intended to flow into the already-closed `feature/platform-observability` workstream before observability also returns to main.
