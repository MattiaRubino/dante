# ADR-011: Access/Auth Architecture Constitution

- **Status:** ACCEPTED ON `feature/access-auth` FOR M2.1–M2.8 / NOT YET INTEGRATED TO PROTECTED MAIN
- **Date:** 2026-08-27
- **Scope:** reusable Access/Auth architecture and security doctrine for the production vertical
- **Detailed authorities:**
  - `../architecture/access-auth-architecture.md`
  - `../architecture/access-auth-security-contract.md`
  - `../architecture/access-auth-api-contract.md`
- **Active workstream:** `../workstreams/access-auth.md`

## Context

DANTE entered the full Access/Auth vertical after closing its Domain, Logical, Physical, engineering, frontend-foundation and PostgreSQL CP6 foundations. Those foundations deliberately did not invent speculative Account/Principal/Auth persistence.

The accepted Web Access frontend already materializes the product surface/state direction, while the backend/database have no production Auth capability yet. Before the first executable Auth slice, the project needed to settle the cross-cutting decisions that would otherwise force expensive rewrites when adding multi-device sessions, Google/Apple authentication, passkeys, Native Mobile, recovery or future MFA.

The decision was therefore to freeze only the long-lived semantic/security boundaries first, then implement by complete vertical slice rather than pre-building a speculative Auth subsystem.

## Decision

DANTE adopts the Access/Auth architecture defined by the three detailed current contracts listed above.

The durable core is:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session

Account
├── EmailIdentity
├── optional PasswordCredential
├── ExternalIdentity (issuer + subject)
├── 0..N PasskeyCredential
└── 0..N independent AuthSession
```

`Account` is the durable access/security root. It is not the Domain Person, an email/password row, a runtime Principal, a global role or a device.

Authentication mechanisms verify evidence; a common application/security policy decides whether that evidence satisfies sign-in, reauthentication or future step-up requirements. Authenticator-specific code does not own a separate session architecture.

The normal Web browser boundary is same-origin through DANTE edge/ingress, while frontend and FastAPI may remain physically/deployment independent. Web uses a secure host-only HttpOnly opaque server-side session cookie; browser JWT/localStorage is not the default model. Native reuses canonical Account/AuthSession semantics with client-appropriate transport.

PostgreSQL remains canonical persistence authority and Auth inherits ADR-010 transaction/constraint/migration/ACL doctrine rather than creating a separate persistence philosophy.

## Security consequences

Accepted security posture includes:

```text
opaque 256-bit session secret
raw session secret never persisted
SHA-256 server-side session verifier
__Host-* Secure HttpOnly SameSite=Lax Web cookie
session-bound synchronizer CSRF token
Origin + Fetch Metadata checks
normal Web CORS disabled by default
multiple independent sessions per Account
immediate server-side revocation
30-day maximum/default inactive-session policy
recent-auth/security-context aware sensitive operations
```

Password direction includes:

```text
minimum 15 Unicode code points
no mandatory composition rules
NFC normalization
Argon2id explicit policy: 64 MiB / t=3 / p=4
server-side HMAC-SHA-256 pepper before Argon2id
HIBP Pwned Passwords k-anonymity screening
bounded KDF concurrency
rehash-on-auth with authoritative race recheck
```

Recovery reset consumes the proof, replaces the credential and revokes all existing sessions atomically, then requires a normal fresh sign-in.

## Identity consequences

Provider identity uses protocol-stable issuer + subject, never provider email as the canonical identity key.

Email coincidence does not silently merge Accounts. Collision requires proof of the existing DANTE Account, explicit user consent and transactional linking.

DANTE preserves normalized delivery/display email separately from a deterministic case-insensitive comparison representation. The canonical email policy does not remove Gmail dots, strip plus tags or otherwise hardcode provider-specific alias behavior.

## Passkey/MFA consequences

Passkeys are a first-class production roadmap authenticator, including passwordless Accounts and multiple credentials per Account.

DANTE requires WebAuthn user verification for its passkey class, uses a random opaque non-PII user handle, supports synced and device-bound passkeys, avoids mandatory consumer attestation and treats signature-counter anomalies as risk signals rather than automatic lockout proof.

MFA/TOTP/recovery codes remain deferred. The architecture is assurance/evidence-aware and therefore does not use `mfa_enabled` as the complete security model or equate every passkey ceremony with MFA.

## API consequences

The product API uses `/api/v1/*`, models application intents rather than Auth-table CRUD and standardizes failures on RFC 9457 `application/problem+json` with stable DANTE machine codes.

Clients use machine code first, category fallback second and HTTP status fallback third. Human error text is never a machine contract.

OpenAPI operations require explicit stable `operationId` values and material error responses; generated clients must not be accidentally renamed by Python handler refactors.

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
unbounded password-KDF concurrency
provider-specific Gmail normalization as identity policy
passkey == MFA by definition
mfa_enabled Boolean as full security posture
consumer passkey attestation requirement by default
CRUD API over Auth persistence tables
frontend parsing human error strings
```

## Why this is not speculative overengineering

The decision deliberately separates **semantic readiness** from **materialization**.

M2 does not authorize a mega-migration or generic Auth framework. Concrete SQL tables, constraints, indexes, transaction locks, endpoint inventory and generated client are introduced only by slices that require them.

The architecture freezes only boundaries that are expensive to change after production code exists and are already required by accepted roadmap capabilities: Web, Native, password, Google, Apple, passkeys, multi-session, recovery and future-compatible MFA.

## Relationship to existing DANTE decisions

- ADR-007 remains a semantic guardrail: persistence convenience must not redefine Domain/Logical ontology.
- ADR-008/ADR-009 remain frontend stack/architecture authorities; Access integrates through the established application/data-source boundaries.
- ADR-010 remains the persistence constitution and governs Auth database materialization, transactions, constraints, migration evolution and privileges.
- This ADR does not reopen Domain, Logical, Physical or CP6 decisions.

## Current implementation status

This ADR records accepted M2.1–M2.8 architecture only.

```text
M2.9  transaction/concurrency/session-expiry closure  OPEN
M2.10 generated-client integration boundary           OPEN
M2.11 M3 test matrix/full-stack harness                OPEN
M3 production Auth code                               NOT STARTED
```

Before M3 begins, the remaining M2 decisions must close, durable docs must be reconciled and a separate explicit production-code write gate must be approved.

## Reopen rule

Reopen the smallest affected decision only when concrete standards, provider/platform, implementation or operational evidence demonstrates that the accepted boundary cannot preserve DANTE product/security/semantic requirements.

Framework preference, ORM convenience, a desire to reduce table count, another product's undocumented internal architecture or general fashion is not sufficient reopen evidence.