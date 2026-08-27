# ADR-011: Access/Auth Architecture Constitution

- **Status:** ACCEPTED ON `feature/access-auth` / M2 CLOSED / NOT YET INTEGRATED TO PROTECTED MAIN
- **Date:** 2026-08-27
- **Scope:** reusable Access/Auth architecture/security/API/testing doctrine for the production vertical
- **Detailed authorities:**
  - `../architecture/access-auth-architecture.md`
  - `../architecture/access-auth-security-contract.md`
  - `../architecture/access-auth-api-contract.md`
  - `../architecture/access-auth-testing-contract.md`
- **Active workstream:** `../workstreams/access-auth.md`

## Context

DANTE entered the full Access/Auth vertical after closing its Domain, Logical, Physical, Engineering Foundation, Frontend Foundation/Materialization and PostgreSQL CP6 foundations.

Those foundations deliberately did not invent speculative Account/Principal/Auth persistence. The accepted Web Access frontend already materializes the product surface/state direction while backend/database production Auth capability does not yet exist.

Before the first executable Auth slice, DANTE needed to settle only the cross-cutting decisions that would otherwise create expensive security/semantic rewrites when adding:

```text
multiple Web/Native sessions
password authentication/recovery
Google/Apple authentication
passkeys
Native Mobile
reauthentication/step-up
future MFA compatibility
first-party generated clients
full-stack security proof
```

The decision is therefore:

```text
freeze expensive long-lived boundaries once
→ implement by complete vertical slice
→ materialize no speculative Auth subsystem
```

M2 completes that constitution. M3 remains the first executable production slice.

---

## Decision

DANTE adopts the Access/Auth architecture defined by the four detailed current contracts above.

Durable core:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
method != factor != assurance

Account
├── EmailIdentity
├── optional PasswordCredential
├── 0..N ExternalIdentity (issuer + subject)
├── 0..N PasskeyCredential
└── 0..N independent AuthSession
```

`Account` is the durable Access/security root. It is not Domain Person, an email/password row, runtime Principal, global role or device.

Authentication mechanisms verify evidence. Common application/security policy decides whether evidence satisfies signin, reauthentication or future step-up. Authenticator-specific code does not own a separate session architecture.

---

## Web/Native topology decision

Normal Web browser security boundary is same-origin through DANTE edge/ingress:

```text
https://<canonical-app-origin>/
https://<canonical-app-origin>/api/v1/*
```

React and FastAPI may remain physically/deployment independent behind that boundary.

Web uses a secure host-only HttpOnly opaque server-side session cookie. Browser JWT/localStorage authentication is not selected.

Native reuses canonical Account/AuthSession semantics with a client-appropriate secure transport/storage adapter. Browser cookie mechanics never become Domain/application semantics.

A future dedicated native/public API hostname remains compatible with the same application contract.

---

## Security consequences

Accepted posture includes:

```text
opaque 256-bit session secret
raw session secret never persisted
SHA-256 server-side session verifier
__Host-* Secure HttpOnly Path=/ SameSite=Lax cookie
session-bound synchronizer CSRF token
exact Origin + Fetch Metadata checks
normal Web CORS disabled by default
multiple independent sessions per Account
server-authoritative revocation/account disable
30-day overall + 30-day inactive default policy
background polling != user activity
recent-auth/assurance-aware sensitive operations
Cache-Control: no-store on sensitive Auth/session responses
```

Revocation/disable COMMIT is the security barrier for new authentication admission; already-admitted requests are not retroactively distributed-cancelled.

---

## Password decision

Password policy/storage direction:

```text
minimum 15 Unicode code points
maximum 1024 code points / 4096 normalized UTF-8 bytes
NFC normalization
no mandatory composition rules
paste/password managers first-class
no silent truncation
Argon2id v19: 64 MiB / t=3 / p=4
HMAC-SHA-256 prehash with separate 256-bit server pepper
HIBP range/k-anonymity screening
bounded KDF concurrency
rehash-on-auth with authoritative current-credential recheck
```

Unknown-account signin performs dummy current-policy Argon2 verification after cheap rate limiting.

New credential establishment fails closed if required breach intelligence is unavailable. Existing valid-password login may fail open only for auxiliary HIBP intelligence, with telemetry.

---

## Identity consequences

Provider identity uses stable protocol key:

```text
issuer + subject
```

Provider email is never canonical federated identity.

Email coincidence does not silently merge/link Accounts. Collision requires proof of the existing DANTE Account, explicit consent and transactional linking.

Email identity separates normalized delivery/display form from deterministic comparison key:

```text
local part → NFC + Unicode casefold
domain     → UTS #46 / IDNA ASCII lowercase
```

DANTE does not remove Gmail dots, strip plus-tags or hardcode provider-specific mailbox alias rules into canonical identity.

The standard consumer Account maintains a verified recovery/contact EmailIdentity, including passwordless/provider/passkey accounts under current product policy.

---

## Credential/session lifecycle consequences

Current logout, specific revoke, revoke-all-others and logout-everywhere are distinct intents.

Authenticated password change:

```text
recent auth
→ replace current PasswordCredential
→ revoke all other sessions
→ preserve initiating session only when continuity is valid
→ rotate initiating session secret
```

Recovery reset:

```text
consume proof
+ replace credential
+ revoke all sessions
→ COMMIT
→ no auto-login
→ fresh normal signin required
```

Account disable revokes all sessions and re-enable never resurrects them.

Authenticator removal may not leave the Account inaccessible and requires proof through a method that remains valid after removal where applicable.

---

## Passkey/MFA consequences

Passkeys are first-class roadmap authenticators, including passwordless Accounts and multiple passkeys per Account.

Accepted WebAuthn boundary includes:

```text
userVerification required
discoverable-credential direction
random opaque 32-byte non-PII userHandle
narrow stable RP-ID principle
synced and device-bound credentials supported
consumer mandatory attestation not selected
signature-counter anomaly = risk signal, not automatic lockout
short-lived single-use cryptographic challenge
```

MFA/TOTP/recovery codes remain deferred. Architecture is evidence/assurance-aware and therefore does not use `mfa_enabled` as the complete security model or equate every passkey ceremony with MFA.

---

## Transaction/concurrency consequences

Auth inherits ADR-010/CP3/CP6:

```text
PostgreSQL canonical authority
READ COMMITTED default
outer application operation owns transaction
no hidden commits
no hidden transaction retries
narrowest truthful concurrency mechanism
no network/human waits inside DB transaction
no blind retry after ambiguous commit
```

Account row is the natural serialization point for account-wide security mutations.

Lock order is deterministic:

```text
Account
→ relevant credential/identity/authenticator
→ relevant session set/session
```

Do not use advisory locks for Account when a canonical row exists. Do not use `SKIP LOCKED` for Auth security invariants. Do not lock Account on every normal session-validation request.

Signin uses:

```text
short DB snapshot
→ Argon2/HIBP outside authoritative DB mutation
→ short Account-locked transaction
→ re-read current Account/Credential
→ create session only if still current
→ COMMIT
→ Set-Cookie
```

Two valid concurrent signins may create two independent sessions.

Signin racing reset/disable is safe because final mutation rechecks canonical state under Account serialization.

Ambiguous AuthSession commit is reconciled through a pre-generated non-secret `auth_session_ref`; it is never blindly retried into a second session effect.

---

## API consequences

Product API uses:

```text
/api/v1/*
```

It models application intents rather than Auth-table CRUD.

Material failures use RFC 9457 `application/problem+json` with stable DANTE extensions:

```text
code
category
request_id
retryable
errors[] when applicable
```

Client behavior uses exact machine code, then category, then HTTP status; human text is never parsed as logic.

Every operation has explicit stable OpenAPI `operationId` and documents material error responses.

---

## OpenAPI/generated-client consequences

ADR-008's selected FastAPI OpenAPI → Orval direction activates in M3.

Canonical chain:

```text
FastAPI/Pydantic API declarations
→ deterministic committed OpenAPI 3.1 snapshot
→ Orval Fetch generation
→ framework-neutral @dante/api-client
→ Web/Native transport adapters
→ application/data-source boundary
→ UI
```

Generated OpenAPI and TypeScript/Zod artifacts are committed/generated and never hand-edited.

`@dante/api-client` does not own React, TanStack Query, routing, cookies, CSRF lifecycle, localStorage or Native secure storage.

Web uses relative same-origin URLs and an injected transport adapter. Native later uses a Native adapter over the same canonical API semantics.

Runtime response validation uses the selected Zod capability. Client-local network/abort/contract failures are not fabricated server machine codes.

TanStack Query activates in M3 for Web remote request/cache state but does not become canonical Auth state or replace the Access product/UI reducer.

---

## Testing/proof consequences

Production Auth completion requires multiple proof layers:

```text
unit/pure application
real PostgreSQL 18.6
real FastAPI HTTP
OpenAPI/Orval/Zod deterministic contract
Web application boundary
real same-origin HTTPS browser full stack
```

The critical M3 browser Auth spine runs on Chromium, Firefox and WebKit.

Mandatory CI external dependencies use protocol-faithful deterministic substitutes; DANTE's own internal Auth path is not faked.

Race tests use real multiple PostgreSQL sessions/connections with deterministic barriers, not arbitrary sleeps.

Critical Auth E2E does not bypass signin with a shared committed Playwright authenticated storage-state file.

M3 adds an Access/Auth cross-stack CI gate while preserving Backend CI Gate and Frontend CI Gate as separate owners.

---

## Rejected alternatives / shortcuts

The accepted architecture rejects as defaults:

```text
Account = Person
Account = email + password
email as Account primary key
provider email as canonical identity
silent merge by matching provider email
one universal Authenticator database table
Principal persistence without concrete need
one session token shared across devices
JWT/localStorage default browser session
browser cross-origin credentialed API by default
wildcard credentialed CORS
SameSite as sole CSRF defense
password composition-rule checklists
periodic password rotation without cause
unbounded KDF concurrency
provider-specific Gmail normalization
passkey == MFA by definition
mfa_enabled Boolean as full posture
mandatory consumer passkey attestation
CRUD API over Auth persistence tables
frontend parsing human error strings
global SERIALIZABLE for Auth
Account row lock on every request
advisory Account lock where row exists
SKIP LOCKED for Auth invariants
Argon2/network work inside long DB transaction
blind ambiguous-commit retry
Redis/JWT session cache in M3
generic signin idempotency table without evidence
handwritten duplicate API client
Axios introduced solely for generated transport
generated React/TanStack hooks as canonical API boundary
remote DEV OpenAPI as generator authority
Auth query cache persisted to browser storage
SQLite/fake DB as PostgreSQL Auth proof
coverage percentage as security proof
```

---

## Why this is not speculative overengineering

M2 freezes only boundaries that are already forced by accepted product scope and expensive to change after production data/client contracts exist.

M2 does **not** authorize:

```text
mega Auth migration
pre-built MFA tables
provider tables without a slice
passkey implementation before M5
generic security-event/SIEM subsystem
global public-developer API platform
```

Concrete SQL tables, indexes, exact endpoints and client package files are materialized only by slices that require them.

DANTE can still ship a serious first-party Web/Play-Store/App-Store product. A separate third-party developer platform (external API keys/OAuth apps, public SDK lifecycle, developer portal, partner webhooks/quotas) remains a future capability only if a real product need appears.

---

## Relationship to existing DANTE decisions

- ADR-007 preserves semantic/persistence boundaries; Auth convenience cannot redefine Domain/Logical ontology.
- ADR-008 owns selected frontend technology including FastAPI OpenAPI → Orval activation trigger.
- ADR-009 owns frontend application/dependency/data-authority boundaries and feature data firewall.
- ADR-010 owns PostgreSQL transaction/constraint/migration/ACL/idempotency doctrine.
- This ADR consumes rather than reopens Domain, Logical, Physical or CP6 decisions.

---

## M2 closure status

```text
M2.1  deployment/origin topology                         CLOSED
M2.2  session/cookie/CSRF/CORS                           CLOSED
M2.3  Account/Identity/Credential/AuthSession/Principal  CLOSED
M2.4  multi-session/credential lifecycle/revocation      CLOSED
M2.5  password hashing/breach policy                     CLOSED
M2.6  passkey-ready/MFA compatibility                    CLOSED
M2.7  email normalization/comparison                     CLOSED
M2.8  API namespace/error/naming                         CLOSED
M2.9  transaction/concurrency/session-expiry             CLOSED
M2.10 OpenAPI/generated-client/Web boundary              CLOSED
M2.11 test matrix/full-stack harness                      CLOSED

M3 production Auth code                                 NOT STARTED
```

M2 closure is a design/documentation/consistency closure. It does not claim runtime Auth proof. M3 implementation requires a separate exact production-code write gate.

---

## Reopen rule

Reopen the smallest affected decision only when concrete standards, provider/platform, implementation, security or operational evidence demonstrates that the accepted boundary cannot preserve DANTE requirements.

Framework preference, ORM convenience, a desire for fewer tables, another product's undocumented internal architecture, generator fashion or test-suite convenience is not sufficient reopen evidence.