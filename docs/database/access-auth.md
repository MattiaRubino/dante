# DANTE Access/Auth Database Reference

- **Status:** CURRENT / BRANCH-LOCAL / M3 CLOSED / M4 PERSISTENCE CLOSED + REAL POSTGRESQL PROVEN
- **Branch:** `feature/access-auth`
- **Current accepted Alembic head:** `20260829_11`
- **Accepted M3 Alembic baseline:** `20260827_10`
- **Protected-main CP6 baseline:** `20260826_08`
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **Database System of Record:** `README.md`
- **M4 architecture authority:** `../architecture/access-auth-m4-contract.md`
- **Security authority:** `../architecture/access-auth-security-contract.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **M4 closure handoff:** `../workstreams/access-auth-m4-live-handoff-2026-08-29.md`

## 1. Purpose / evidence status

This file owns the current Access/Auth persistence meaning on `feature/access-auth`.

Authority relationship:

```text
Database System of Record
+ Access/Auth architecture/security contract
↓
this subject reference
↓
Dictionary + SQLAlchemy + Alembic
↓
real PostgreSQL catalog + direct tests
```

Current accepted evidence state:

```text
M3 persistence
→ MATERIALIZED + REAL POSTGRESQL PROVEN + CLOSED

M4 persistence
→ MATERIALIZED IN DICTIONARY / SQLALCHEMY / ALEMBIC
→ REAL POSTGRESQL/CURRENT-CATALOG PROVEN
→ CLOSED / ACCEPTED
```

`TEST CODE EXISTS != TEST EXECUTION PASS` remains a permanent rule; M4 now has accepted execution evidence.

---

## 2. Current topology

```text
Account
├── 1..N verified recovery/contact EmailIdentity over product lifetime semantics
├── 0..1 PasswordCredential
├── 0..N AuthSession
└── 0..1 current PasswordRecoveryChallenge

PasswordSignupChallenge
└── anonymous/pre-Account pending signup state, isolated by signup_ref

bounded DB capability
└── acquire_account_security_lock(uuid)
```

Accepted M4 catalog:

```text
PostgreSQL          18.6
Alembic             20260829_11
74 tables
5 views
15 routines
75 triggers
113 physical indexes
72 foreign keys
149 CHECK constraints
94 standalone Dictionary entries
```

Accepted M3 baseline remains historical comparison:

```text
Alembic             20260827_10
72 tables
5 views
15 routines
75 triggers
104 physical indexes
71 foreign keys
137 CHECK constraints
92 standalone Dictionary entries
```

---

## 3. Canonical Account/Auth objects

### `dante.account`

Durable Access/security root.

```text
account_ref   uuid / UUIDv7 PK
status_code   active | disabled
created_at    finite timestamptz
disabled_at   nullable finite timestamptz
```

It does not store email/password/provider/passkey/profile/device/global-role payload.

M4 runtime ACL remains deliberately narrow:

```text
SELECT                                         yes
INSERT account_ref,status_code,created_at,
       disabled_at                             yes
broad UPDATE                                   no
DELETE                                         no
```

Account security serialization continues through `dante.acquire_account_security_lock(uuid)`, not broad Account UPDATE or ad-hoc advisory-lock replacement.

### `dante.email_identity`

Canonical login/contact/recovery email identity.

```text
email_identity_ref
account_ref
address
comparison_key UNIQUE
created_at
verified_at
```

Canonical comparison remains application-owned NFC/casefold + canonical IDNA ASCII lower domain; PostgreSQL uniqueness remains the final race arbiter.

M4 adds the composite uniqueness needed for exact recovery binding:

```text
uq_email_identity_email_identity_ref_account_ref
(email_identity_ref, account_ref)
```

Runtime ACL:

```text
SELECT                                      yes
INSERT exact establishment columns          yes
broad UPDATE / DELETE                       no
```

### `dante.password_credential`

Optional current password credential per Account.

```text
password_credential_ref
account_ref UNIQUE
verifier
pepper_key_id
created_at
updated_at
```

Raw password, normalized bytes, pepper secret and HIBP material are never persisted.

M4 runtime ACL:

```text
SELECT                                      yes
INSERT exact establishment columns          yes
UPDATE verifier,pepper_key_id,updated_at    yes
broad UPDATE / DELETE                       no
```

### `dante.auth_session`

Independent opaque server-authoritative session.

```text
auth_session_ref
account_ref
secret_verifier UNIQUE
created_at
authenticated_at
recent_auth_at
last_user_activity_at
expires_at
revoked_at
revocation_reason_code
```

Raw bearer secret remains transient only.

M4 reauthentication capability is column-bounded:

```text
SELECT                                                   yes
INSERT                                                   yes
UPDATE last_user_activity_at,revoked_at,
       revocation_reason_code                            yes
UPDATE secret_verifier,recent_auth_at,expires_at        yes
broad UPDATE / DELETE                                    no
```

Reauthentication preserves `auth_session_ref` while rotating the exact presented bearer verifier and recent-auth/session-window state.

---

## 4. `dante.password_signup_challenge`

Purpose: ephemeral anonymous/pre-Account password signup state.

It deliberately does **not** create canonical Account state before mailbox proof.

Key fields:

```text
signup_ref                      UUIDv7 PK / public non-secret ref
email_address                   normalized delivery/display form
email_comparison_key            canonical comparison key
password_verifier               Argon2id verifier
password_pepper_key_id          non-secret key id
otp_verifier                    32-byte HMAC verifier
otp_key_id                      non-secret OTP key id
created_at
updated_at
signup_expires_at
verification_issued_at
verification_expires_at
failed_verification_attempts    0..5
```

Security semantics:

```text
multiple pending challenges for one email are allowed
signup_ref isolates anonymous attempts
no UNIQUE(email_comparison_key)
OTP raw value never persisted
OTP verifier is cryptographically bound to signup_ref
successful verification deletes sibling pending challenges for canonical email
expired state is operational/ephemeral, not product history
```

Indexes:

```text
PK(signup_ref)
ix_password_signup_challenge_email_comparison_key
ix_password_signup_challenge_signup_expires_at
```

Runtime ACL:

```text
SELECT, INSERT, DELETE                         yes
UPDATE only OTP rotation/attempt/time columns  yes
```

---

## 5. `dante.password_recovery_challenge`

Purpose: one current high-entropy password-recovery proof per Account.

Key fields:

```text
password_recovery_ref  UUIDv7 PK / public non-secret ref
account_ref
email_identity_ref
secret_verifier        32-byte purpose-separated verifier
issued_at
expires_at
```

Declarative exact-owner binding:

```text
FK(email_identity_ref, account_ref)
→ email_identity(email_identity_ref, account_ref)
```

The physical constraint name is deliberately bounded below PostgreSQL's identifier limit:

```text
fk_password_recovery_challenge_email_account_email_identity
```

This avoids implicit server-side name truncation while preserving the semantic identity of the composite relationship.

Current constraints/indexes include:

```text
PK(password_recovery_ref)
UNIQUE(account_ref)              → one current challenge per Account
UNIQUE(secret_verifier)          → verifier collision/alias protection
index(email_identity_ref)
index(expires_at)
```

Lifecycle:

```text
256-bit raw recovery bearer
raw secret never persisted
new issuance supersedes prior challenge
single use
bounded lifetime
consumption is physical DELETE
not retained as canonical product history
```

Runtime ACL:

```text
SELECT, INSERT, DELETE yes
UPDATE                 no
```

---

## 6. Transaction/race posture

### Signup verification

```text
BEGIN
→ lock PasswordSignupChallenge by signup_ref
→ validate expiry/attempt budget/OTP
→ check canonical EmailIdentity collision
→ if existing email:
     delete pending siblings
     COMMIT
     return existing_account
→ else:
     insert Account
     insert verified EmailIdentity
     insert PasswordCredential
     insert AuthSession
     delete pending siblings
→ COMMIT
→ reconcile ambiguous commit only against exact generated state
→ issue raw session secret only after durable/reconciled success
```

PostgreSQL `EmailIdentity.comparison_key` uniqueness is the final duplicate-email race arbiter.

### Recovery issuance

```text
read eligible verified email/password Account
→ BEGIN
→ Account security lock
→ exact eligibility re-read
→ delete prior recovery challenge for Account
→ insert new challenge bound to exact EmailIdentity + Account
→ COMMIT/reconcile
→ enqueue email outside transaction
```

### Password reset

```text
proof/new-password preflight
→ HIBP + Argon2 outside transaction
→ BEGIN
→ Account security lock
→ exact Account/EmailIdentity/PasswordCredential re-read
→ conditional DELETE ... RETURNING recovery challenge
→ replace PasswordCredential
→ revoke ALL active AuthSessions with password_reset reason
→ COMMIT/reconcile
→ no auto-login
```

The conditional consume prevents cleanup/reset/replay races from producing reuse.

### Reauthentication

```text
verify password outside transaction
→ BEGIN
→ Account security lock
→ re-read credential and exact AuthSession
→ require current secret_verifier == verifier of bearer presented by this request
→ conditional AuthSession UPDATE
→ rotate secret_verifier
→ refresh recent_auth_at / last activity / expiry as contracted
→ COMMIT/reconcile
```

A stale pre-rotation bearer cannot perform another reauth merely because it was admitted earlier.

---

## 7. Performance doctrine

```text
READ COMMITTED default
no blanket SERIALIZABLE
Account security lock only for Account-wide security mutation
Argon2/HIBP/network work outside DB transaction
no email/SMTP wait under DB lock
indexed equality lookups on hot paths
bounded challenge cleanup
no blind mutation retry
ambiguous commit uses explicit reconciliation, never automatic replay
```

---

## 8. Mapping / Dictionary / migration traceability

Migrations:

```text
20260827_09
→ Account / EmailIdentity / PasswordCredential / AuthSession

20260827_10
→ acquire_account_security_lock(uuid)

20260829_11
→ PasswordSignupChallenge
→ PasswordRecoveryChallenge
→ exact EmailIdentity↔Account composite key for recovery binding
→ M4 narrow runtime ACL delta
```

SQLAlchemy module:

```text
dante.platform.database.mappings.auth
├── AccountRow
├── EmailIdentityRow
├── PasswordCredentialRow
├── AuthSessionRow
├── PasswordSignupChallengeRow
└── PasswordRecoveryChallengeRow
```

Dictionary current entries include:

```text
dictionary/tables/account.json
dictionary/tables/email_identity.json
dictionary/tables/password_credential.json
dictionary/tables/auth_session.json
dictionary/tables/password_signup_challenge.json
dictionary/tables/password_recovery_challenge.json
dictionary/routines/acquire_account_security_lock.json
```

The original introducing stage of M3 objects remains M3; their `runtime_acl_stage` evolves truthfully to M4 where M4 adds capabilities.

---

## 9. Accepted M4 persistence evidence

```text
real PostgreSQL marked suite                 87 / 87 PASS
current-catalog / Alembic head parity        PASS
M4 lifecycle PostgreSQL tests                PASS
M3 signin/session PostgreSQL regression      PASS
runtime ACL exactness                        PASS
migration head/base/head round-trip          PASS
real browser DB-backed Auth matrix           33 / 33 PASS
Chromium / Firefox / WebKit                  11 / 11 each
manual signup/recovery/existing-account UAT  PASS
```

The final PostgreSQL acceptance run proved the complete 87-test marked suite against the accepted M4 source/catalog state.

Therefore:

```text
M4 source representation parity              ACCEPTED
M4 real PostgreSQL execution evidence         PASS
M4 full-stack browser DB evidence             PASS
M4 database closure                           CLOSED
```

---

## 10. Forward persistence boundary

M4 does **not** authorize speculative provider/passkey/MFA persistence.

Still deferred until their own contracts:

```text
ExternalIdentity
PasskeyCredential
provider callback/challenge state
TOTP / MFA / recovery codes
Principal table
Account ↔ Person convenience relation
```

Permanent rule:

```text
later Auth need
→ exact semantic/security contract
→ minimal forward migration
→ SQLAlchemy
→ Dictionary
→ human current reference
→ real PostgreSQL proof
```

M5 is next and must freeze provider/passkey/linking semantics before any persistence delta is added.
