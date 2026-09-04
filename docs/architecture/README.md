# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION FOR `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Current work:** PRE-INTEGRATION AUDIT

## 1. Current architecture state

```text
Product / Domain / Logical / Physical       CLOSED / CURRENT
Engineering Foundation                      CLOSED / ACCEPTED
Frontend Foundation                         CLOSED / ACCEPTED
Backend CP1–CP6                              CLOSED / ACCEPTED
PostgreSQL                                   18.6 / sole canonical persistence

Access/Auth M1–M5                            CLOSED / ACCEPTED
local password/passkey UAT                   PASS
real Windows Hello UAT                       PASS
real Google UAT                              PASS
real Apple registered-domain UAT             BOUNDED DEFERRED / NON-BLOCKING

Email Platform architecture                  ACCEPTED / SHARED DANTE SUBSYSTEM
Email Platform implementation                ACCEPTED
Email Platform automated/PostgreSQL proof    PASS
real DANTE → SES signup/recovery/notification PASS
Email Platform engineering                   CLOSED

Protected-main Alembic                       20260830_09 / Recovery
Feature/access-auth Alembic                  20260903_15 / Auth + Email
Feature/access-auth topology                 87/5/15/75/170/88/267
```

Protected `main` remains integrated authority. Access/Auth + Email are branch-local until explicit convergence and PR integration.

## 2. Entry points

System/current routing:

- `system-overview.md`
- `technical-decisions.md`
- `../PROJECT-STATUS.md`
- `../ROADMAP.md`

Access/Auth:

- `access-auth-architecture.md`
- `access-auth-security-contract.md`
- `access-auth-api-contract.md`
- `access-auth-testing-contract.md`
- `access-auth-m4-contract.md`
- `access-auth-m5-contract.md`
- `access-auth-m5-persistence-api-contract.md`
- `../frontend/access.md`
- `../database/access-auth.md`

Email Platform:

- `email-platform.md`
- `access-auth-email-delivery.md` — Access/Auth consumer integration only
- `../decisions/ADR-012-email-delivery-platform.md`
- `../development/email-platform-local-uat.md`
- `../development/email-platform-acceptance-2026-09-03.md`

Database:

- `../database/README.md`
- `../database/dictionary/README.md`
- `../development/backend-cp6-02-postgresql-persistence-constitution.md`

Important ADRs:

- `../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `../decisions/ADR-008-frontend-engineering-stack.md`
- `../decisions/ADR-009-frontend-architecture-boundaries.md`
- `../decisions/ADR-010-postgresql-persistence-constitution.md`
- `../decisions/ADR-011-access-auth-architecture.md`
- `../decisions/ADR-012-email-delivery-platform.md`

## 3. Permanent Auth architecture

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal request-runtime only
Account → 0..N AuthSessions
Account → 0..N ExternalIdentities
Account → 0..N PasskeyCredentials
provider identity = issuer + subject
provider email != identity/link authority
provider assertion != DANTE AuthSession
passwordless Account valid
method != factor != assurance
```

Authenticator-specific code verifies evidence. Canonical Account/session policy remains shared DANTE application/security authority.

## 4. Browser security posture

```text
opaque high-entropy server-authoritative AuthSession
Secure + HttpOnly + host-only cookie
no JWT/localStorage/sessionStorage Auth authority
session-bound synchronizer CSRF
exact same-origin posture
Origin + Fetch Metadata
recent reauthentication for sensitive mutations
same-session bearer rotation after reauth/security-context change
```

## 5. Provider architecture

Google:

```text
DANTE transaction + nonce first
official Google Identity Services interaction
Google ID token = evidence only
backend signature/JWK/issuer/audience/nonce verification
issuer + subject = canonical provider identity
third-party mailbox → direct DANTE mailbox proof where current control matters
```

Apple:

```text
DANTE begin → Apple authorization → form_post/code exchange
issuer + subject authority
encrypted server grant lifecycle
verified server notifications
Private Email Relay semantics
```

Apple real registered-domain external acceptance remains deferred until prerequisites exist. This does not reopen M5 engineering.

## 6. Passkey architecture

```text
WebAuthn / FIDO2
resident/discoverable credential required
user verification required
attestation none
exact RP/origin policy
opaque random user_handle
multiple passkeys
DANTE stores public credential material only
```

Backend `python-fido2` owns cryptographic/RP verification; frontend owns browser ceremony interaction/conversion only.

## 7. Shared Email Platform

The Email Platform is shared infrastructure, not an Access/Auth-owned implementation detail.

```text
DANTE feature/application mutation
        │
        ├── canonical state
        └── durable EmailIntent
                 ▼
PostgreSQL COMMIT
                 ▼
claim / lease / worker
                 ▼
versioned template + protected payload
                 ▼
provider-neutral adapter
        ├── Amazon SES API v2
        └── SMTP local/CI compatibility
                 ▼
provider evidence
                 ▼
DANTE delivery/suppression state
```

Permanent rules:

```text
DANTE owns lifecycle/state
provider owns last-mile transport
provider accepted != delivered
network timeout != definitely unsent
no blind retry after ambiguous outcome
no provider I/O in caller DB transaction
short-lived encrypted sensitive payload + wipe
OTP/recovery proof excluded from logs/metrics/traces
Auth/security tracking/link rewriting OFF
```

## 8. Database integration boundary

Current branch and protected main deliberately diverge after `20260826_08`:

```text
main   → 20260830_09 Recovery
Access → 20260903_15 Auth + Email
```

Architecture requires a forward merge of both histories. No semantic model or applied migration is rewritten merely to produce a linear-looking graph.

Combined topology becomes authoritative only after real PostgreSQL proof on the merged branch.

## 9. Current integration sequence

```text
pre-integration audit
→ merge main into feature/access-auth
→ forward Alembic merge revision
→ combined Recovery/Auth/Email QA
→ PR to protected main
→ merge enriched main into feature/platform-observability
→ observability integration checks
→ PR observability to protected main
```

Later M6/M7 work starts from the enriched protected main on fresh bounded branches.

## 10. Historical progress metadata

Some large M4/M5 contracts preserve implementation-stage text such as `NEXT`, old Alembic heads or routes not yet materialized. Those statements are historical checkpoint metadata inside durable design contracts; they do not override current status/routing above.

Temporary handoffs must be removed before protected-main integration under `../development/documentation-lifecycle-policy.md`.