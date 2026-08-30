# DANTE Access/Auth Database Reference

- **Status:** CURRENT / BRANCH-LOCAL / M4 PERSISTENCE CLOSED / M5-A PERSISTENCE MATERIALIZED + REAL POSTGRESQL PROVEN / M5-B NEXT
- **Branch:** `feature/access-auth`
- **Current accepted Alembic head:** `20260830_12`
- **Accepted M5-A implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
- **Accepted M4 Alembic baseline:** `20260829_11`
- **Accepted M3 Alembic baseline:** `20260827_10`
- **Protected-main CP6 baseline:** `20260826_08`
- **Database System of Record:** `README.md`
- **M4 architecture authority:** `../architecture/access-auth-m4-contract.md`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5 persistence/API authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
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
→ MATERIALIZED + REAL POSTGRESQL/CURRENT-CATALOG PROVEN
→ CLOSED / ACCEPTED

M5.1
→ SEMANTIC / ARCHITECTURE FREEZE COMPLETE

M5.2
→ EXACT PERSISTENCE + API DESIGN COMPLETE

M5-A
→ DICTIONARY / SQLALCHEMY / ALEMBIC MATERIALIZED
→ REAL POSTGRESQL 18.6 PROVEN
→ COMPLETE

M5-B
→ NEXT / PROVIDER + JOSE/JWK/AEAD INFRASTRUCTURE
```

`TEST CODE EXISTS != TEST EXECUTION PASS` remains permanent. M5-A claims only what actually executed on the real persistence boundary.

---

## 2. Current materialized topology through M5-A

```text
Account
├── 1..N EmailIdentity over lifecycle
├── 0..1 PasswordCredential
├── 0..N AuthSession
├── 0..N ExternalIdentity
├── 0..1 WebAuthnAccount
│   └── 0..N PasskeyCredential
└── 0..1 current PasswordRecoveryChallenge

PasswordSignupChallenge
└── anonymous/pre-Account password signup state

ExternalAuthTransaction
└── bounded provider sign-in/link/reauth transaction

ExternalLinkChallenge
└── bounded explicit provider collision/link continuation

ExternalSignupChallenge
└── bounded provider enrollment + mailbox proof

AccountProfileBootstrap
└── non-canonical one-shot provider bootstrap staging

AppleAuthGrant
└── encrypted pending/active/revocation lifecycle

WebAuthnChallenge
└── bounded registration/authentication/reauthentication ceremony state

bounded DB capability
└── acquire_account_security_lock(uuid)
```

Accepted current M5-A catalog:

```text
PostgreSQL          18.6
Alembic             20260830_12
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

Accepted M4 historical baseline:

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

---

## 3. Canonical core Auth objects

### `dante.account`

Durable Access/security root.

```text
account_ref   uuid / UUIDv7 PK
status_code   active | disabled
created_at    finite timestamptz
disabled_at   nullable finite timestamptz
```

It does not store email/password/provider/passkey/profile/device/global-role payload.

Runtime posture remains narrow. Account-wide security mutation serializes through `dante.acquire_account_security_lock(uuid)`, not broad Account UPDATE or ad-hoc advisory locks.

### `dante.email_identity`

Canonical login/contact/recovery email identity.

```text
email_identity_ref
account_ref
address
comparison_key UNIQUE
created_at
verified_at
recovery_restriction_code NULL
recovery_restriction_observed_at NULL
```

`verified_at` remains historical mailbox-control evidence.

M5 recovery reachability:

```text
recovery_restriction_code
→ current known policy restriction preventing recovery use

initial vocabulary:
provider_delivery_disabled

recovery_restriction_observed_at
→ newest provider reachability evidence timestamp
```

Apple ordering rule:

```text
apply email-disabled/email-enabled only when event time is newer
older/equal events cannot reverse newer reachability truth
verified_at is not cleared merely because relay delivery is disabled
```

Composite owner target remains:

```text
uq_email_identity_email_identity_ref_account_ref
(email_identity_ref, account_ref)
```

Runtime ACL after M5-A:

```text
SELECT                                      yes
INSERT exact establishment columns          yes
INSERT recovery_restriction_code,
       recovery_restriction_observed_at      yes / column-scoped
UPDATE recovery_restriction_code,
       recovery_restriction_observed_at      yes / column-scoped
broad INSERT / UPDATE / DELETE               no
```

The two new INSERT columns are required because SQLAlchemy names the nullable M5 columns in establishment INSERT statements; PostgreSQL still requires privileges on named columns even when values are NULL.

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

M5 keeps passwordless Accounts valid. Password add/remove/recovery adaptation occurs in later M5 slices; no second password system is introduced.

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

M5-A adds the composite uniqueness target:

```text
uq_auth_session_auth_session_ref_account_ref
(auth_session_ref, account_ref)
```

This exists to let WebAuthn challenge state bind an exact session to the exact Account declaratively.

Provider/passkey success in later M5 slices must still create/rotate this canonical DANTE AuthSession model; provider tokens/assertions never become DANTE sessions.

---

## 4. M4 challenge state retained

### `dante.password_signup_challenge`

Purpose: ephemeral anonymous/pre-Account password signup.

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

Current physical FK:

```text
fk_password_recovery_challenge_email_account_email_identity
```

M5 passwordless recovery reuses this strong proof posture. Later M5-G changes reset from replace-only to create-or-replace PasswordCredential without weakening single-use/all-session-revoke/no-auto-login behavior.

---

## 5. `dante.external_identity`

Durable lifetime binding between one DANTE Account and one verified external provider identity.

Identity authority:

```text
issuer + subject
```

Email is metadata only and never the Account link key.

Current shape:

```text
external_identity_ref       UUIDv7 PK
account_ref                 FK Account
email_identity_ref          nullable exact same-Account binding
provider_code               google | apple
issuer
subject
provider_email_address      nullable hint
provider_email_private      nullable, paired with email hint
status_code                 active | revoked
created_at
status_changed_at
last_authenticated_at
revoked_at                  nullable
revocation_reason_code      nullable
```

Hard uniqueness:

```text
UNIQUE(issuer, subject)
```

M5-A adds the exact composite target:

```text
UNIQUE(external_identity_ref, issuer, subject)
```

This lets Apple grant persistence prove that a bound grant's issuer+subject exactly matches the referenced ExternalIdentity.

No `UNIQUE(account_ref, provider_code)` exists.

Normal unlink is logical:

```text
active → revoked
```

No runtime DELETE. Lifetime provider identity cannot silently be recycled onto another Account.

---

## 6. `dante.external_auth_transaction`

Short-lived server-authoritative Google/Apple transaction state.

```text
external_auth_transaction_ref
provider_code
expected_issuer
purpose_code       sign_in | link | reauthenticate
state_verifier     32 bytes UNIQUE
nonce_verifier     32 bytes UNIQUE
auth_session_ref   nullable
auth_session_secret_verifier nullable
return_target_code access | security
created_at
expires_at         <= 15 min
claimed_at         nullable
```

`sign_in` is anonymous.

`link` and `reauthenticate` bind the exact `auth_session_ref` plus begin-time bearer-verifier snapshot.

Claim is single-use and conditional. Apple transaction claim must occur before one-use authorization-code exchange. Ambiguous Apple code-exchange outcomes are not blindly retried.

Raw state/nonce/session secrets are not persisted.

---

## 7. Provider collision / enrollment state

### `dante.external_link_challenge`

Bounded explicit link/collision state.

Key semantics:

```text
no silent provider-email merge
flow capability stored as verifier only
exact target Account / EmailIdentity
optional exact pending Apple grant binding
15-minute class lifetime
final Account lock + issuer/subject uniqueness decides race
```

M5-A exact Apple binding uses the shortened PostgreSQL-safe FK name:

```text
fk_external_link_challenge_apple_grant
```

### `dante.external_signup_challenge`

Provider proof that still requires DANTE mailbox recovery proof.

```text
provider identity evidence
optional mailbox input
purpose-separated OTP verifier
challenge <= 30 min
OTP <= 15 min
failed verification <= 5
optional exact Apple pending grant binding
```

No Account exists before the accepted proof set.

If the email becomes owned during the race, the later lifecycle converts verified provider evidence into an explicit link path rather than creating a duplicate Account.

M5-A exact Apple binding uses:

```text
fk_external_signup_challenge_apple_grant
```

---

## 8. `dante.account_profile_bootstrap`

Non-canonical one-shot provider bootstrap staging.

```text
account_ref PK/FK
source provider/issuer
display_name?
given_name?
family_name?
picture_url?
locale?
created_at
expires_at <= 30 days
```

Semantics:

```text
first provider Account creation → optional INSERT
future canonical profile/setup consumes → DELETE
later provider login → never refresh/overwrite
expiry → DELETE
```

M5-A adds an explicit cleanup index on `expires_at`.

Provider data initializes DANTE where useful but does not permanently own later user-edited DANTE values.

---

## 9. `dante.apple_auth_grant`

Durable encrypted Apple server-side grant lifecycle.

```text
apple_auth_grant_ref
external_identity_ref nullable
issuer
subject
client_id
refresh_token_ciphertext nullable
refresh_token_nonce nullable / 12 bytes when present
encryption_key_id nullable
status_code pending | active | revocation_pending | revoked
created_at
updated_at
status_changed_at
pending_expires_at nullable
revocation_requested_at nullable
revoked_at nullable
```

Pending grants may be temporarily unbound to ExternalIdentity so DANTE can still revoke abandoned Apple authorization after successful code exchange but before Account/link completion.

Secrets are application-layer AEAD encrypted; key material remains outside PostgreSQL/Git/logs.

Exact binding when `external_identity_ref` is present:

```text
(external_identity_ref, issuer, subject)
→ external_identity(external_identity_ref, issuer, subject)
```

Lifecycle:

```text
pending
→ active
→ revocation_pending
→ revoked
```

Local ExternalIdentity revoke precedes remote Apple network revoke. Remote provider outage never keeps Apple Auth locally active.

M5-A adds cleanup indexing on `pending_expires_at`.

---

## 10. WebAuthn / passkey persistence

### `dante.webauthn_account`

One stable WebAuthn account binding per DANTE Account:

```text
account_ref PK/FK Account
user_handle bytea(32) UNIQUE
```

Exact composite target:

```text
UNIQUE(account_ref, user_handle)
```

The user handle is opaque random 256-bit state. It is not AccountRef, email or PersonRef.

### `dante.passkey_credential`

```text
passkey_credential_ref  UUIDv7
account_ref             FK WebAuthnAccount
credential_id           bytea UNIQUE
credential_public_key   bytea
cose_algorithm          integer
sign_count              uint32 semantics
backup_eligible         bool
backup_state            bool
transports              text[]
label
status_code             active | revoked
created_at
updated_at
last_used_at             nullable
revoked_at               nullable
revocation_reason_code   nullable
```

Database invariant:

```text
backup_state=true → backup_eligible=true
```

Passkey removal is logical revoke. Credential-id lifetime uniqueness is retained; a removed credential cannot be silently recycled.

Transport values are not constrained to a closed DB enum because future standards may introduce new valid values.

No AAGUID/device fingerprint is persisted in M5 without a concrete product/security consumer.

### `dante.webauthn_challenge`

Bounded WebAuthn ceremony state:

```text
ceremony_code registration | authentication | reauthentication
challenge_verifier 32-byte UNIQUE
account_ref nullable
auth_session_ref nullable
auth_session_secret_verifier nullable
user_handle nullable
rp_id
expected_origin
created_at
expires_at <= 5 min
claimed_at nullable
```

Registration/reauthentication bind exact Account + AuthSession + WebAuthn user handle through composite FKs. Anonymous authentication remains unbound until credential proof identifies the Account.

Raw browser challenge is never persisted.

---

## 11. Current transaction/race posture

Inherited from M3/M4:

```text
READ COMMITTED
short authoritative transactions
Account security lock for Account-wide security mutation
external/provider/WebAuthn ceremony I/O outside DB transaction
no blanket SERIALIZABLE
no blind mutation retry
```

M5-A proves the database arbiters required by later flows:

```text
ExternalIdentity issuer+subject uniqueness
exact Apple identity/grant ownership
WebAuthn exact Account/session/userHandle ownership
Passkey credential-id uniqueness
challenge/verifier uniqueness
status/chronology/secret-shape invariants
least-privilege runtime ACL
```

Later M5 lifecycle code must still re-read/recheck under the correct transaction/Account lock; DB constraints are final arbiters, not a substitute for lifecycle logic.

---

## 12. Performance doctrine

```text
indexed equality on hot Auth lookups
no network wait under DB lock
no provider/JWK/token exchange in DB transaction
no browser ceremony wait in DB transaction
bounded challenge cleanup
bounded provider lifecycle reconciliation
ambiguous commit handled by operation-specific reconciliation, not replay
```

Provider key caches are process/runtime adapter state, not a reason to add Redis/JWT/session authority.

---

## 13. Mapping / Dictionary / migration traceability

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

20260830_12
→ EmailIdentity recovery reachability delta
→ 9 M5 multi-authenticator tables
→ exact Apple/WebAuthn physical bindings
→ M5 least-privilege runtime ACL
```

SQLAlchemy module:

```text
dante.platform.database.mappings.auth
```

Current Auth mappings include M3/M4 rows plus:

```text
ExternalIdentityRow
ExternalAuthTransactionRow
ExternalLinkChallengeRow
ExternalSignupChallengeRow
AccountProfileBootstrapRow
AppleAuthGrantRow
WebAuthnAccountRow
PasskeyCredentialRow
WebAuthnChallengeRow
```

Dictionary current entries mirror the same materialized objects and current constraints/ACLs.

Applied revisions remain immutable evidence under normal migration discipline.

---

## 14. Accepted M5-A persistence evidence

```text
uv lock                                      PASS
Ruff format / lint                           PASS
mypy strict                                  PASS
backend fast                                 87 / 87 PASS
real PostgreSQL 18.6                         95 / 95 PASS
M5 persistence tests                          8 / 8 PASS
current-catalog parity                        PASS
M4 lifecycle PostgreSQL regression            PASS
M3 signin/session PostgreSQL regression       PASS
runtime ACL exactness                         PASS
migration head/base/head round-trip           PASS
Alembic autogenerate drift                    PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PG       PASS
backend build                                 PASS
```

Therefore:

```text
M5-A persistence COMPLETE / REAL POSTGRESQL PROVEN
```

This does not imply provider runtime/public API/Web/browser/provider UAT closure.

---

## 15. Passwordless recovery DB implication

M5 remains committed to:

```text
recovery proof valid
+ PasswordCredential absent
→ establish first PasswordCredential

recovery proof valid
+ PasswordCredential present
→ replace PasswordCredential
```

Both paths retain:

```text
same M4 strong recovery proof
HIBP + Argon2 outside DB transaction
Account security lock/recheck
single-use conditional proof consume
revoke ALL AuthSessions
no auto-login
```

The runtime ACL/lifecycle implementation for add/remove/create-or-replace password belongs to M5-G and must stay narrow.

---

## 16. Forward persistence boundary

Current truth:

```text
M4 persistence CLOSED / PROVEN
M5.1 semantics FROZEN
M5.2 exact DB/API design COMPLETE
M5-A persistence COMPLETE / POSTGRESQL PROVEN
M5-B provider/JWK/JOSE/AEAD infrastructure NEXT
```

Still outside current M5 persistence unless separately authorized:

```text
TOTP / generic MFA / recovery-code tables
Principal table
Account ↔ Person convenience relation
provider-data integration tokens/grants for Gmail/Calendar/iCloud
complete long-term security-event/observability store owned by M7
```

Permanent process:

```text
real Auth need
→ exact semantic/security contract
→ minimal migration/runtime delta
→ Dictionary + SQLAlchemy + Alembic where structural
→ current human reference
→ real boundary proof
```
