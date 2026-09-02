# DANTE Architecture Index

- **Status:** CURRENT / AUTHORITATIVE NAVIGATION FOR `feature/access-auth`
- **Last reconciled:** 2026-09-02

## 1. Current architecture state

```text
Domain Model                         CLOSED
Logical Model                        CLOSED / 57 OF 57
Physical target                      CLOSED / ACCEPTED
Engineering Foundation               CLOSED / ACCEPTED
Frontend Foundation                  CLOSED / ACCEPTED
Backend CP1–CP6                      CLOSED / ACCEPTED
PostgreSQL                           18.6 / sole canonical persistence

Access/Auth M1–M4                    CLOSED / ACCEPTED
M5.1 architecture freeze             COMPLETE
M5.2 persistence/API freeze          COMPLETE
M5-A–D                               COMPLETE
Groups 1–3                           COMPLETE / ENGINEERING PASS
Group 4 product engineering          AUTOMATED QA PASS
local password/passkey UAT           PASS
real Google UAT                      PASS
real Internet email delivery         OPEN
real Apple registered-domain UAT     DEFERRED / OPEN
whole M5                             ACTIVE / NOT FORMALLY CLOSED

Access/Auth Alembic head             20260831_13
Access/Auth DB topology              83 tables / 5 views / 15 routines /
                                     75 triggers / 156 indexes / 85 FKs /
                                     233 CHECKs
```

Protected `main` remains integrated authority for closed shared foundations. Newer Access/Auth truth is branch-local until explicit integration.

## 2. Current architecture entry points

- `system-overview.md` — system/component/authority overview
- `technical-decisions.md` — architecture decision register
- `access-auth-architecture.md` — identity/authenticator/session architecture
- `access-auth-security-contract.md` — security/session/password/email/provider/passkey policy
- `access-auth-api-contract.md` — `/api/v1`, RFC 9457, OpenAPI/generated-client contract
- `access-auth-testing-contract.md` — proof layers and real-boundary contract
- `access-auth-m4-contract.md` — closed lifecycle authority
- `access-auth-m5-contract.md` — durable M5 multi-authenticator semantics
- `access-auth-m5-persistence-api-contract.md` — exact M5 persistence/API design and milestone reconciliation
- `../workstreams/access-auth.md` — current operational state
- `../workstreams/access-auth-m5-review-2026-09-02.md` — current review/UAT evidence
- `../database/README.md` and `../database/access-auth.md`
- `../frontend/access.md`

Important ADRs:

- `../decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `../decisions/ADR-008-frontend-engineering-stack.md`
- `../decisions/ADR-009-frontend-architecture-boundaries.md`
- `../decisions/ADR-010-postgresql-persistence-constitution.md`
- `../decisions/ADR-011-access-auth-architecture.md`

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
provider identity key = issuer + subject
provider email != identity/link authority
provider authentication != provider-data authorization
provider assertion != DANTE AuthSession
passwordless Account valid
method != factor != assurance
```

Authenticator-specific code verifies evidence. Canonical DANTE policy/session creation remains a shared application/security boundary.

## 4. Browser security posture

```text
opaque high-entropy server-authoritative session
Secure + HttpOnly + host-only cookie direction
no JWT/localStorage/sessionStorage Auth authority
session-bound synchronizer CSRF
exact same-origin posture
Origin + Fetch Metadata
no broad credentialed CORS
recent reauthentication for sensitive mutations
same-session bearer rotation after reauth/security-context change
```

## 5. Provider architecture

Google:

```text
official Google Identity Services
DANTE transaction + nonce first
Google ID token = evidence only
backend signature/JWK/issuer/audience/nonce verification
issuer + sub canonical external identity
third-party mailbox → additional DANTE mailbox proof where current control matters
```

Apple:

```text
DANTE begin → Apple authorization → form_post/code exchange
issuer + subject authority
encrypted server grant lifecycle
server notifications
Private Email Relay semantics
```

Sign-in authorization remains separate from future Gmail/Calendar/iCloud data-integration grants.

## 6. Passkey architecture

```text
WebAuthn / FIDO2, not custom crypto
resident/discoverable credential required
user verification required
attestation none
exact RP/origin policy
opaque random user_handle
multiple passkeys
synced/device-bound/security-key compatible
DANTE stores credential public material, never biometric/PIN/private key
```

Frontend owns only browser ceremony conversion/interaction; backend `python-fido2` owns cryptographic/RP verification.

## 7. Current standards/deprecation review

Review on 2026-09-02 found no material deprecated primitive in the current Google/WebAuthn path:

- Google uses current GIS `accounts.google.com/gsi/client` and official `renderButton`.
- `use_fedcm_for_button` remains current; DANTE does not use deprecated `use_fedcm_for_prompt`.
- Google identity is keyed by `sub`, not email, matching current OIDC guidance.
- WebAuthn browser APIs and FIDO2 verification remain current.
- Apple M5 semantics already accept the new `private.icloud.com` Sign in with Apple relay domain alongside `privaterelay.appleid.com`.

See `../workstreams/access-auth-m5-review-2026-09-02.md` for sources and benchmark details.

## 8. Progress metadata inside frozen contracts

The M5 contracts contain detailed milestone-time reconciliation sections. Statements such as `M5-F NEXT` or `public routes later` are historical for the slice when written if they conflict with the current status/workstream. Their semantic/security/persistence design remains authoritative; operational progress is owned by `PROJECT-STATUS`, `ROADMAP`, the active workstream and current review.

## 9. Current architecture gaps — deliberate, not hidden

```text
real outbound-email architecture/provider qualification
real Apple registered-domain UAT
M7 session/device management UX
M7 new-login/security-event response
M7 production observability
final authenticated Home handoff
```

No current evidence requires replacing the accepted Account/AuthSession/authenticator architecture to implement these gaps.