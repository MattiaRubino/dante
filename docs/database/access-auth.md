# DANTE Access/Auth Database Reference

- **Status:** CURRENT / BRANCH-LOCAL / M4 PERSISTENCE CLOSED + REAL POSTGRESQL PROVEN / M5.1 SEMANTICS FROZEN / M5 PERSISTENCE NOT YET MATERIALIZED
- **Branch:** `feature/access-auth`
- **Current accepted Alembic head:** `20260829_11`
- **Accepted M3 Alembic baseline:** `20260827_10`
- **Protected-main CP6 baseline:** `20260826_08`
- **M4 final accepted implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **Database System of Record:** `README.md`
- **M4 architecture authority:** `../architecture/access-auth-m4-contract.md`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **Security authority:** `../architecture/access-auth-security-contract.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **M5 handoff:** `../workstreams/access-auth-m5-live-handoff-2026-08-29.md`

## 1. Purpose / evidence status

This file owns current Access/Auth persistence meaning on `feature/access-auth`.

Authority relationship:

```text
Database System of Record
+ Access/Auth architecture/security/M4/M5 contracts
↓
this subject reference
↓
Dictionary + SQLAlchemy + Alembic
↓
real PostgreSQL catalog + direct tests
```

Current evidence state:

```text
M3 persistence
→ MATERIALIZED + REAL POSTGRESQL PROVEN + CLOSED

M4 persistence
→ MATERIALIZED IN DICTIONARY / SQLALCHEMY / ALEMBIC
→ REAL POSTGRESQL/CURRENT-CATALOG PROVEN
→ CLOSED / ACCEPTED

M5.1
→ SEMANTIC/ARCHITECTURE PERSISTENCE REQUIREMENTS FROZEN
→ NO M5 TABLE/COLUMN/MIGRATION ACCEPTED YET

M5.2
→ NEXT / EXACT PERSISTENCE + API DESIGN
```

`TEST CODE EXISTS != TEST EXECUTION PASS` remains permanent. M5 will claim PostgreSQL capability only after execution on the real PostgreSQL boundary.

---

## 2. Current materialized topology through M4

```text
Account
├── 1..N verified recovery/contact EmailIdentity over lifecycle
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

Accepted M3 historical baseline:

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

No M5 persistence count exists yet.

---

## 3. Canonical materialized Auth objects

### `dante.account`

Durable Access/security root.

```text
account_ref   uuid / UUIDv7 PK
status_code   active | disabled
created_at    finite timestamptz
disabled_at   nullable finite timestamptz
```

It does not store email/password/provider/passkey/profile/device/global-role payload.

Runtime ACL through M4:

```text
SELECT                                         yes
INSERT account_ref,status_code,created_at,
       disabled_at                             yes
broad UPDATE                                   no
DELETE                                         no
```

Account security serialization continues through `dante.acquire_account_security_lock(uuid)`, not broad Account UPDATE or ad-hoc advisory locks.

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

Comparison remains application-owned NFC/casefold + canonical IDNA ASCII lower domain; PostgreSQL uniqueness is final race arbiter.

M4 composite owner target:

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

M5 may need provider/relay reachability semantics, but M5.1 does **not** authorize adding status columns to EmailIdentity by assumption. M5.2 must decide whether current EmailIdentity, a provider lifecycle object or another explicit owner carries that state.

### `dante.password_credential`

Optional current password credential:

```text
password_credential_ref
account_ref UNIQUE
verifier
pepper_key_id
created_at
updated_at
```

Raw password/normalized bytes/pepper/HIBP material are never persisted.

M4 runtime ACL:

```text
SELECT                                      yes
INSERT exact establishment columns          yes
UPDATE verifier,pepper_key_id,updated_at    yes
broad UPDATE / DELETE                       no
```

M5 freezes passwordless Accounts and therefore requires a future **create-or-replace** recovery path and authenticated first-password establishment without changing the 0..1 credential cardinality.

### `dante.auth_session`

Independent opaque server-authoritative session:

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

Raw bearer remains transient only.

M4 update capability:

```text
SELECT                                                   yes
INSERT                                                   yes
UPDATE last_user_activity_at,revoked_at,
       revocation_reason_code                            yes
UPDATE secret_verifier,recent_auth_at,expires_at        yes
broad UPDATE / DELETE                                    no
```

Google/Apple/passkey success in M5 must still create/rotate this canonical AuthSession model, never a provider session substitute.

---

## 4. M4 challenge state

### `dante.password_signup_challenge`

Purpose: ephemeral anonymous/pre-Account password signup.

Key fields:

```text
signup_ref                      UUIDv7 PK
email_address
email_comparison_key
password_verifier
password_pepper_key_id
otp_verifier                    32-byte HMAC verifier
otp_key_id
created_at / updated_at
signup_expires_at
verification_issued_at
verification_expires_at
failed_verification_attempts
```

Semantics:

```text
multiple pending challenges per email allowed
no Account before proof
OTP raw value never persisted
OTP bound to signup_ref
successful verification removes sibling pending challenges
expired state operational/ephemeral
```

Runtime ACL:

```text
SELECT, INSERT, DELETE
UPDATE only bounded OTP/attempt/time columns
```

### `dante.password_recovery_challenge`

Purpose: one current high-entropy recovery proof per Account.

```text
password_recovery_ref
account_ref
email_identity_ref
secret_verifier
issued_at
expires_at
```

Exact declarative binding:

```text
FK(email_identity_ref, account_ref)
→ email_identity(email_identity_ref, account_ref)
```

Current physical FK name:

```text
fk_password_recovery_challenge_email_account_email_identity
```

Constraints:

```text
PK(password_recovery_ref)
UNIQUE(account_ref)
UNIQUE(secret_verifier)
index(email_identity_ref)
index(expires_at)
```

Runtime ACL:

```text
SELECT, INSERT, DELETE yes
UPDATE                 no
```

M5 passwordless recovery reuses this strong proof posture unless M5.2 evidence shows an exact required extension. Do not create a weaker parallel recovery proof.

---

## 5. Current transaction/race posture through M4

### Signup verification

```text
BEGIN
→ lock PasswordSignupChallenge
→ validate expiry/attempt/OTP
→ canonical EmailIdentity collision check
→ existing email: consume pending state + return existing_account
→ new email: Account + verified EmailIdentity + PasswordCredential + AuthSession
→ delete pending siblings
→ COMMIT/reconcile
→ issue raw session only after durable/reconciled success
```

### Recovery/reset

```text
HIBP + Argon2 outside transaction
→ BEGIN
→ Account security lock
→ exact Account/EmailIdentity/PasswordCredential re-read
→ conditional DELETE ... RETURNING recovery proof
→ replace credential
→ revoke ALL AuthSessions
→ COMMIT/reconcile
→ no auto-login
```

### Reauthentication

```text
password verification outside transaction
→ BEGIN
→ Account security lock
→ re-read credential + exact AuthSession
→ require presented bearer verifier still current
→ rotate secret verifier + recent-auth/window state
→ COMMIT/reconcile
```

M5 inherits:

```text
READ COMMITTED
short authoritative transactions
Account lock for Account-wide security mutation
external/provider/WebAuthn ceremony I/O outside DB transaction
no blanket SERIALIZABLE
no blind mutation retry
```

---

## 6. Performance doctrine

```text
indexed equality on hot Auth lookups
no network wait under DB lock
no provider/JWK/token exchange in DB transaction
no browser ceremony wait in DB transaction
bounded challenge cleanup
bounded provider lifecycle workers if introduced
ambiguous commit handled by operation-specific reconciliation, not replay
```

Provider key caches are process/runtime adapter state, not a reason to add Redis/JWT/session authority.

---

## 7. Mapping / Dictionary / migration traceability through M4

Migrations:

```text
20260827_09
→ Account / EmailIdentity / PasswordCredential / AuthSession

20260827_10
→ acquire_account_security_lock(uuid)

20260829_11
→ PasswordSignupChallenge
→ PasswordRecoveryChallenge
→ exact EmailIdentity↔Account recovery binding
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

Dictionary current Auth entries include:

```text
dictionary/tables/account.json
dictionary/tables/email_identity.json
dictionary/tables/password_credential.json
dictionary/tables/auth_session.json
dictionary/tables/password_signup_challenge.json
dictionary/tables/password_recovery_challenge.json
dictionary/routines/acquire_account_security_lock.json
```

Applied revisions remain immutable evidence under normal migration discipline.

---

## 8. Accepted M4 persistence evidence

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

Therefore M4 database closure remains CLOSED.

---

# 9. M5.1 persistence semantics — FROZEN, NOT MATERIALIZED

M5 architecture authority:

```text
docs/architecture/access-auth-m5-contract.md
```

M5.1 establishes semantic needs, not exact SQL names.

### 9.1 Durable ExternalIdentity

Need:

```text
Account → 0..N ExternalIdentity
identity = issuer + subject
global provider-identity uniqueness
```

Expected invariant direction:

```text
UNIQUE(issuer, subject)
```

Do not add provider email/name/avatar/locale as identity merely for convenience.

Do not automatically impose one provider identity per Account unless M5.2 proves that product rule.

### 9.2 Provider transaction/link state

Need bounded server-authoritative state for:

```text
Google/Apple signin transaction
provider new-account enrollment
explicit Account linking
state/nonce/purpose/account-session binding
single-use/expiry/replay protection
```

Exact table sharing/splitting must follow semantic/lifecycle/ACL equivalence, not table-count preference.

### 9.3 Pending provider account enrollment

A provider may prove identity but not provide sufficient current DANTE recovery-email proof.

Need a safe pending state capable of preserving:

```text
verified provider identity evidence
mailbox-verification requirement
provider transaction expiry
no canonical Account before accepted proof set
```

Do not force an Account row into existence early.

### 9.4 Apple grant secret state

Apple production Auth may require retained token/grant material for validation/revocation/lifecycle.

Any materialized secret state must use:

```text
minimum required token material only
application-layer authenticated encryption
key/version identifier
nonce/ciphertext/integrity representation as required by selected AEAD
key material outside PostgreSQL/Git
rotation/revocation path
no plaintext logging/exposure
```

Exact object/columns are M5.2.

### 9.5 Apple notification idempotency

M5.2 decides whether durable notification identifier/effect state is required for replay/idempotency. Do not add a generic provider-event history table unless the exact provider semantics and retention require it.

### 9.6 WebAuthn user handle

Need one stable opaque random WebAuthn user handle per Account.

```text
target direction: 256 random bits
NOT account_ref
NOT email
NOT PersonRef
```

Exact owner/table/constraint is M5.2.

### 9.7 PasskeyCredential

Need `Account → 0..N PasskeyCredential` with exact database uniqueness and security metadata sufficient for real WebAuthn verification/management.

Expected semantic data classes:

```text
credential identifier
public credential key/algorithm representation
Account/userHandle binding
created/last-used times where justified
signature counter
backup eligibility/state when available
transport hints if useful
optional user-facing label
```

Exact columns are not frozen yet.

### 9.8 WebAuthn challenge state

Need registration/authentication challenge state with:

```text
>=32-byte CSPRNG direction
short TTL
purpose binding
single use
origin/RP/session/account binding as appropriate
replay rejection
bounded cleanup
```

One vs separate challenge tables is an M5.2 decision based on actual semantics.

### 9.9 Provider profile-bootstrap staging

Apple one-shot profile data must not be lost.

M5.2 first checks for an existing canonical Domain/Logical/Physical owner for profile/setup. If none is ready, design bounded durable bootstrap staging with provenance.

Do not add name/avatar/locale columns to Account or ExternalIdentity as a shortcut.

---

## 10. M5.2 exact persistence gate

Before any Alembic revision, produce an object-by-object specification:

```text
semantic owner
canonicality/control status
exact table/routine name
columns + types + nullability
UUIDv7/technical identity choice
PK/FK/UNIQUE/CHECK
index/query matrix
retention/cleanup
secret/verifier/encryption handling
runtime ACL
migration lock/risk review
Dictionary entry
SQLAlchemy mapping
PostgreSQL test obligations
```

Also design required races:

```text
concurrent first provider account creation
same provider identity linked to two Accounts
provider link vs revoke/unlink
provider signin vs Account disable
passkey register duplicate
passkey remove vs auth
password add vs recovery/reset
Apple notification vs signin/link
```

No sleep-based race synchronization as primary proof.

---

## 11. Passwordless recovery DB implication

M5 freezes:

```text
recovery proof valid
+ PasswordCredential absent
→ establish first PasswordCredential

recovery proof valid
+ PasswordCredential present
→ replace PasswordCredential
```

Both paths:

```text
same M4 strong recovery proof
HIBP + Argon2 outside DB transaction
Account security lock/recheck
single-use conditional proof consume
revoke ALL AuthSessions
no auto-login
```

M5.2 decides whether existing runtime ACL already permits the insert/update combination safely or requires a new narrow column/table grant. Never broaden privileges by convenience.

---

## 12. M5 migration/testing constraints

When M5 persistence is eventually materialized, prove:

```text
previous head 20260829_11 → new head
fresh DB → new head
single Alembic head
Dictionary/SQLAlchemy/Alembic parity
real PostgreSQL catalog parity
constraints/indexes
least-privilege allowed/denied runtime actions
race/transaction behavior
rollback/reconciliation behavior where relevant
```

M5.1 documentation itself does not change accepted DB counts/head.

---

## 13. Forward persistence boundary

Current truth:

```text
M4 persistence CLOSED / PROVEN
M5.1 semantics FROZEN
M5.2 exact DB/API design NEXT
M5 schema NOT STARTED
```

Still outside current M5 persistence unless separately authorized:

```text
TOTP / generic MFA / recovery-code tables
Principal table
Account ↔ Person convenience relation
provider-data integration tokens for Gmail/Calendar/iCloud
complete long-term security-event/observability store owned by M7
```

Permanent process:

```text
real Auth need
→ exact semantic/security contract
→ minimal forward migration
→ Dictionary + SQLAlchemy + Alembic
→ current human reference
→ real PostgreSQL proof
```