# DANTE — Access/Auth M5 Persistence + API Contract

- **Status:** CURRENT / BRANCH-LOCAL M5.2 AUTHORITY / DESIGN FREEZE COMPLETE / M5-A PERSISTENCE ACCEPTED / M5-B RUNTIME INFRASTRUCTURE ACCEPTED / M5-C GOOGLE BACKEND ACCEPTED / M5-D APPLE BACKEND ACCEPTED
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Prerequisite:** M1–M4 CLOSED; M5.1 architecture/external-authority freeze COMPLETE
- **M5.2:** exact persistence/API/state/race design COMPLETE
- **M5-A persistence materialization:** COMPLETE / REAL POSTGRESQL 18.6 PROVEN
- **M5-B provider/JWK/JOSE/AEAD/WebAuthn policy infrastructure:** COMPLETE / ENGINEERING PASS
- **M5-C Google authentication + Account creation/collision:** COMPLETE / ENGINEERING PASS
- **M5-D Apple authentication + grant/notification lifecycle:** COMPLETE / ENGINEERING PASS
- **Accepted PostgreSQL head:** `20260830_12`
- **Prior accepted persistence baseline:** `20260829_11`
- **M5-D accepted implementation checkpoint:** `7d13b712f032e8d41d7cf03d406555fd9f3c0160`
- **M5-C accepted implementation checkpoint:** `e6f738a1ea3f5152caa7d99f1d6ccd108747c806`
- **M5-B accepted implementation checkpoint:** `e2d40a7666e3c0130afecd8113b8063390b86b9d`
- **M5-A accepted implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
- **Next implementation step:** M5-E — Explicit linking + authenticator lifecycle
- **Companion authority:** `access-auth-m5-contract.md`
- **Binding foundations:** Access/Auth architecture/security/API/testing contracts, ADR-011, Database System of Record, CP6 persistence constitution

This document remains the **exact M5 persistence and public-API design authority**. M5-A materialized and proved the persistence subset. M5-B materialized and proved the shared provider/JWK/JOSE/AEAD/WebAuthn-policy runtime foundation. M5-C materialized and proved the Google backend application/persistence slice. M5-D materialized and proved the Apple protocol/application/persistence/grant-lifecycle slice. Public M5 API, generated client, Web integration, complete authenticator management and real provider/browser acceptance remain future M5 slices.

---

# 0. M5-A implementation reconciliation

M5-A materialized the frozen nine-table design plus the EmailIdentity recovery-reachability delta at Alembic `20260830_12`.

Accepted catalog:

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

Accepted proof:

```text
uv lock                                      PASS
Ruff format / lint                           PASS
mypy strict                                  PASS
backend fast                                 87 / 87 PASS
real PostgreSQL 18.6                         95 / 95 PASS
M5 persistence tests                          8 / 8 PASS
migration previous-head → head                PASS
fresh DB → head                               PASS
migration head/base/head                      PASS
single Alembic head                           PASS
Alembic autogenerate drift                    PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PG       PASS
runtime ACL / negative constraints            PASS
CP6/M3/M4 persistence regressions             PASS
backend build                                 PASS
```

Physical materialization strengthened the design in these bounded ways:

```text
ExternalIdentity
→ composite UQ(external_identity_ref, issuer, subject)
→ exact Apple grant identity target

AppleAuthGrant
→ exact ExternalIdentity issuer+subject binding

ExternalLinkChallenge / ExternalSignupChallenge
→ exact Apple grant issuer+subject binding

AuthSession
→ composite UQ(auth_session_ref, account_ref)

WebAuthnAccount
→ composite UQ(account_ref, user_handle)

WebAuthnChallenge
→ exact Account+AuthSession ownership
→ exact Account+userHandle ownership

PasskeyCredential
→ account_ref targets WebAuthnAccount ownership
→ explicit cose_algorithm persisted
→ logical active/revoked lifecycle
→ lifetime credential-id uniqueness retained
→ backup_state=true requires backup_eligible=true

cleanup indexes
→ account_profile_bootstrap(expires_at)
→ apple_auth_grant(pending_expires_at)

EmailIdentity ACL
→ INSERT remains column-scoped and includes the two new nullable recovery fields
→ UPDATE remains limited to those two recovery fields
```

PostgreSQL's 63-byte identifier ceiling required and accepted these shortened exact FK names:

```text
fk_external_link_challenge_apple_grant
fk_external_signup_challenge_apple_grant
```

After M5-A, the exact **physical** source of truth for names/columns/constraints/indexes/ACL is the reconciled set:

```text
this contract
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic 20260830_12
≈ real PostgreSQL 18.6 catalog
≈ direct tests
```

Any mismatch is a defect.

## 0.1 M5-B runtime reconciliation

M5-B materialized the shared provider/crypto/WebAuthn policy infrastructure without changing persistence, Alembic or Dictionary truth.

Accepted implementation checkpoint:

```text
e2d40a7666e3c0130afecd8113b8063390b86b9d
chore(auth): finalize M5-B lock and formatting
```

Accepted dependency/runtime baseline:

```text
fido2         2.2.1
joserfc       1.7.4
cryptography  50.0.1
existing httpx2
Python        3.14
uv            0.12.5
```

Accepted infrastructure:

```text
typed Google/Apple/WebAuthn/provider settings with safe disabled defaults
bounded provider/JWK HTTP runtime
configured provider JWKS endpoints are the only JWK trust sources
coordinated JWK cache, conditional revalidation, rotation and unknown-kid cooldown
JWKS response/key-count/duplicate/private-material bounds
strict JOSE compact/header admission and exact RS256 allowlist
canonical unpadded Base64URL compact segments
Apple AES-256-GCM grant key ring, random 12-byte nonce and stable AAD
purpose-separated 256-bit provider/link/enrollment/WebAuthn flow proofs
FIDO2 WebAuthn exact RP/origin policy baseline
single process-scoped ProviderRuntime inside existing AuthRuntime lifecycle
no provider network I/O at process startup
```

Accepted closeout proof:

```text
uv lock --check                              PASS
Ruff autofix / format / lint                 PASS
mypy strict                                  PASS / 73 source files
backend fast                                 127 / 127 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
```

PostgreSQL was intentionally not rerun for M5-B because this slice changes no DB/schema/Alembic/Dictionary contract and no regression evidence justified reopening the accepted M5-A persistence gate.

## 0.2 M5-C Google backend reconciliation

M5-C materialized the Google authentication application/persistence slice without changing schema, Alembic or Dictionary truth.

Accepted implementation checkpoint:

```text
e6f738a1ea3f5152caa7d99f1d6ccd108747c806
chore(auth): finalize M5-C formatting
```

Accepted implementation:

```text
Google OIDC trust boundary over accepted M5-B JOSE/JWK runtime
canonical Google issuer + issuer/subject identity authority
issuer/audience/azp/nonce/exp/iat/nbf/subject validation
Gmail / Workspace / third-party mailbox authority classification
verifier-only ExternalAuthTransaction state/nonce persistence
single transaction claim / replay rejection
known ExternalIdentity signin → canonical DANTE AuthSession
provider-authoritative mailbox → passwordless Account + verified EmailIdentity + ExternalIdentity
third-party mailbox → DANTE provider-enrollment OTP before Account creation
existing EmailIdentity collision → explicit link_required, never silent merge
Google link/reauth exact AuthSession binding and bearer rotation
one-shot account_profile_bootstrap staging
purpose-separated provider-enrollment OTP verifier
bounded provider ingress rate limits
ambiguous commit reconciliation and uniqueness-race convergence
no Google bearer/ID-token persistence or logging
provider network work outside DB transactions
```

Accepted closeout proof:

```text
uv lock --check                              PASS
Ruff format / format-check / lint            PASS
mypy strict                                  PASS / 79 source files
backend fast                                 148 / 148 PASS
focused real PostgreSQL M5-C                  7 / 7 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
```

The focused PostgreSQL suite proves transaction verifier-only persistence/replay rejection, passwordless Account creation and identity reuse, email collision without silent merge, third-party mailbox enrollment, enrollment collision→link transition, concurrent same Google identity convergence and link/reauth session behavior.

M5-C does not claim public M5 routes/OpenAPI/client, Access Web Google UI or real Google browser/provider acceptance.

## 0.3 M5-D Apple backend reconciliation

M5-D materialized the Apple authentication, refresh-grant and server-notification lifecycle without changing schema, Alembic or Dictionary truth.

Accepted implementation checkpoint:

```text
7d13b712f032e8d41d7cf03d406555fd9f3c0160
chore(auth): finalize M5-D formatting
```

Accepted implementation:

```text
Apple Web begin + form_post-compatible authorization topology
ExternalAuthTransaction claim before the single-use code exchange
front-channel ID-token and server-side exchanged ID-token identity convergence
issuer/audience/nonce/exp/iat/subject/c_hash verification
ES256 Apple client-secret issuance from governed provider settings
single-attempt authorization-code exchange; ambiguous result never blindly retried
one-shot Apple name/profile bootstrap preservation
Hide My Email classification for retained privaterelay.appleid.com and new private.icloud.com addresses
known identity signin / new passwordless Account / collision / provider enrollment
Apple link/reauth exact AuthSession binding and bearer rotation
AES-256-GCM refresh-grant envelope with grant+issuer+subject+client AAD
pending → active → revocation_pending → revoked AppleAuthGrant lifecycle
local-first identity/grant revoke before remote Apple mutation
bounded idempotent revocation_pending reconciliation and final secret-envelope wipe
signed Apple server-notification verification
email-disabled/email-enabled event-time ordering into EmailIdentity reachability state
consent-revoked/account-deleted ExternalIdentity/grant reconciliation
ambiguous PostgreSQL commit reconciliation before provider continuation and after terminal writes
concurrent same issuer+subject convergence without active-grant regression
provider network work outside DB transactions
```

Accepted closeout proof:

```text
uv lock --check                              PASS
Ruff autofix / format / format-check / lint PASS
mypy src                                     PASS / 49 source files
backend fast                                 171 / 171 PASS
focused real PostgreSQL M5-D                  9 / 9 PASS
full real PostgreSQL regression              111 / 111 PASS
backend build                                PASS / sdist + wheel
git diff --check                             PASS
```

The focused PostgreSQL proof covers transaction claim/replay, passwordless Account creation, grant binding/lifecycle, collision/enrollment/link/reauth, signed notification effects, concurrent same-sub convergence and durable revocation reconciliation. The full PostgreSQL regression simultaneously retains M4, Google, M5 persistence and CP6 catalog/constraint/ACL/migration/runtime/transaction proof.

M5-D does not claim public M5 routes/OpenAPI/client, Access Web Apple UI, Apple production registration/configuration, Private Email Relay sender setup or real Apple browser/provider acceptance.

---

# 1. Design result

M5 persistence delta:

```text
ALTER
  dante.email_identity

CREATE
  dante.external_identity
  dante.external_auth_transaction
  dante.external_link_challenge
  dante.external_signup_challenge
  dante.account_profile_bootstrap
  dante.apple_auth_grant
  dante.webauthn_account
  dante.passkey_credential
  dante.webauthn_challenge
```

Exactly **9 new tables**.

No generic `auth_token`, `oauth_token`, `provider_challenge`, `credential`, `security_blob` or cross-purpose god-table is permitted.

Permanent identity direction:

```text
Account
├── EmailIdentity 1..N over lifecycle
├── PasswordCredential 0..1
├── ExternalIdentity 0..N
├── WebAuthnAccount 0..1
│   └── PasskeyCredential 0..N
└── AuthSession 0..N
```

---

# 2. Cross-cutting physical rules

All M5 persistence follows CP6:

```text
UUIDv7 for DANTE durable row refs
READ COMMITTED
short explicit transactions
Account security row lock for Account-wide auth mutations
NO ACTION foreign keys unless separately justified
no blanket SERIALIZABLE
no blind mutation retries
no provider/network I/O inside DB transactions
no raw bearer/token/challenge secret persistence
no server-side SQL defaults merely for application convenience
runtime role = least privilege / default deny
```

All timestamps are `timestamp with time zone`, finite, application-supplied UTC instants.

All external strings are bounded before persistence. Application validation remains stricter where protocol syntax cannot be expressed safely as a small PostgreSQL CHECK.

Raw high-entropy flow capabilities are never stored. PostgreSQL stores only 32-byte purpose-specific verifiers. Raw values never enter logs.

---

# 3. `email_identity` M5 evolution

M5 adds:

```text
recovery_restriction_code         text        NULL
recovery_restriction_observed_at  timestamptz NULL
```

Semantics:

```text
verified_at
= historical evidence that control of this exact mailbox was proven

recovery_restriction_code
= current known policy restriction that prevents this EmailIdentity being treated as a viable recovery channel

recovery_restriction_observed_at
= latest provider reachability evidence timestamp relevant to that restriction, retained even when restriction is cleared
```

Initial vocabulary:

```text
provider_delivery_disabled
```

Checks:

```text
recovery_restriction_code IS NULL
OR recovery_restriction_code = 'provider_delivery_disabled'

recovery_restriction_code IS NULL
OR recovery_restriction_observed_at IS NOT NULL

recovery_restriction_observed_at IS NULL
OR (
  isfinite(recovery_restriction_observed_at)
  AND recovery_restriction_observed_at >= created_at
)
```

Apple ordering:

```text
email-disabled at T
→ apply only when T is newer than current observed_at
→ code=provider_delivery_disabled
→ observed_at=T

email-enabled at T
→ apply only when T is newer
→ code=NULL
→ observed_at=T retained
```

Never clear `verified_at` merely because provider delivery is disabled.

M5-A runtime ACL reconciliation:

```text
existing SELECT remains

INSERT remains column-scoped across exact EmailIdentity establishment columns,
including:
  recovery_restriction_code
  recovery_restriction_observed_at

UPDATE only:
  recovery_restriction_code
  recovery_restriction_observed_at
```

The INSERT extension is necessary because SQLAlchemy names these nullable columns in establishment INSERT statements; it is not permission for broad EmailIdentity writes.

---

# 4. `external_identity`

## Purpose

Durable lifetime binding between one DANTE Account and one verified external provider identity.

Authority:

```text
issuer + subject
```

Email is not the identity key.

## Columns

```text
external_identity_ref       uuid        NOT NULL
account_ref                 uuid        NOT NULL
email_identity_ref          uuid        NULL
provider_code               text        NOT NULL
issuer                      text        NOT NULL
subject                     text        NOT NULL
provider_email_address      text        NULL
provider_email_private      boolean     NULL
status_code                 text        NOT NULL
created_at                  timestamptz NOT NULL
status_changed_at           timestamptz NOT NULL
last_authenticated_at       timestamptz NOT NULL
revoked_at                  timestamptz NULL
revocation_reason_code      text        NULL
```

## Keys / constraints

```text
PK  pk_external_identity
    (external_identity_ref)

FK  fk_external_identity_account_ref_account
    (account_ref)
    → dante.account(account_ref)

FK  fk_external_identity_email_account_email_identity
    (email_identity_ref, account_ref)
    → dante.email_identity(email_identity_ref, account_ref)
    MATCH SIMPLE

UQ  uq_external_identity_issuer_subject
    (issuer, subject)

UQ  uq_external_identity_external_identity_ref_issuer_subject
    (external_identity_ref, issuer, subject)
```

No `UNIQUE(account_ref, provider_code)`.

Checks include:

```text
UUIDv7 ref
provider_code IN ('google','apple')
provider/issuer canonical pair
subject trimmed/nonempty <=255
provider email/private flag all-or-none
status_code IN ('active','revoked')
finite/ordered timestamps
active ↔ revoked fields exact
```

Indexes:

```text
ix_external_identity_account_ref
ix_external_identity_email_identity_ref
```

Lifecycle:

```text
active → revoked
```

Normal unlink is logical, not SQL DELETE. Lifetime `(issuer, subject)` cannot silently move to another Account.

Runtime:

```text
SELECT
INSERT exact immutable/current columns
UPDATE provider email/private + status/timestamps/revocation metadata
NO DELETE
```

---

# 5. `external_auth_transaction`

Short-lived server-authoritative Google/Apple transaction.

Columns:

```text
external_auth_transaction_ref  uuid        NOT NULL
provider_code                  text        NOT NULL
expected_issuer                text        NOT NULL
purpose_code                   text        NOT NULL
state_verifier                 bytea       NOT NULL
nonce_verifier                 bytea       NOT NULL
auth_session_ref               uuid        NULL
auth_session_secret_verifier   bytea       NULL
return_target_code             text        NOT NULL
created_at                     timestamptz NOT NULL
expires_at                     timestamptz NOT NULL
claimed_at                     timestamptz NULL
```

Vocabulary:

```text
purpose_code:
  sign_in
  link
  reauthenticate

return_target_code:
  access
  security
```

Keys:

```text
PK external_auth_transaction_ref
FK auth_session_ref → auth_session
UQ state_verifier
UQ nonce_verifier
```

Checks:

```text
provider/issuer canonical pair
purpose/return target vocabulary
state/nonce verifier exactly 32 bytes
sign_in → session fields NULL
link/reauth → session ref + 32-byte bearer-verifier snapshot present
expires_at > created_at and <= created_at + 15 minutes
claimed_at NULL or finite within issued lifetime
```

Claim semantics:

```text
UPDATE ...
SET claimed_at=:now
WHERE ref/verifier match
  AND claimed_at IS NULL
  AND expires_at>:now
RETURNING ...
```

Apple claim occurs **before** authorization-code exchange. Ambiguous code exchange is not blindly retried.

Indexes:

```text
ix_external_auth_transaction_expires_at
ix_external_auth_transaction_auth_session_ref
```

Runtime:

```text
SELECT, INSERT, DELETE
UPDATE claimed_at only
```

DELETE is cleanup/terminal retention only.

---

# 6. `apple_auth_grant`

Durable encrypted Apple refresh-grant lifecycle, including the gap between successful Apple code exchange and final DANTE Account/link completion.

Columns:

```text
apple_auth_grant_ref          uuid        NOT NULL
external_identity_ref         uuid        NULL
issuer                        text        NOT NULL
subject                       text        NOT NULL
client_id                     text        NOT NULL
refresh_token_ciphertext      bytea       NULL
refresh_token_nonce           bytea       NULL
encryption_key_id             text        NULL
status_code                   text        NOT NULL
created_at                    timestamptz NOT NULL
updated_at                    timestamptz NOT NULL
status_changed_at             timestamptz NOT NULL
pending_expires_at            timestamptz NULL
revocation_requested_at       timestamptz NULL
revoked_at                    timestamptz NULL
```

Statuses:

```text
pending
active
revocation_pending
revoked
```

Encryption:

```text
application-layer AEAD
baseline AES-256-GCM
12-byte nonce
key id/version
key outside PostgreSQL/Git/logs
stable AAD binds grant ref + issuer + subject + client_id
```

Exact bound identity rule after M5-A:

```text
(external_identity_ref, issuer, subject)
→ external_identity(external_identity_ref, issuer, subject)
```

Grant uniqueness remains one issuer+subject and one bound ExternalIdentity lifecycle.

Lifecycle:

```text
code exchange + identity verification
→ pending grant

successful Account/link finalization
→ bind exact ExternalIdentity
→ active

local unlink/provider revoke
→ ExternalIdentity locally revoked first
→ grant revocation_pending
→ COMMIT
→ remote Apple revoke outside DB tx
→ confirmed → revoked + encrypted token cleared

abandoned pending expiry
→ revocation_pending
→ bounded reconciliation
→ remote revoke
→ revoked + secret cleared
```

Cleanup indexes include:

```text
status_code + updated_at
pending_expires_at
```

Runtime:

```text
SELECT, INSERT
bounded UPDATE of binding/secret/status/timestamp fields
NO DELETE
```

---

# 7. `external_link_challenge`

Purpose: short-lived provider-first collision state after valid provider proof identifies an email already owned by a DANTE Account.

Columns include:

```text
external_link_challenge_ref
target_account_ref
target_email_identity_ref
provider_code
issuer
subject
provider_email_address?
provider_email_private?
apple_auth_grant_ref?
continuation_verifier
created_at
expires_at
```

Raw continuation capability exists only in the Secure HttpOnly host-only provider-link cookie.

Keys/invariants:

```text
exact target Account
exact target EmailIdentity+Account binding
UNIQUE(issuer,subject)
UNIQUE(continuation_verifier)
Google → no Apple grant
Apple → exact Apple grant required
continuation verifier 32 bytes
TTL <= 15 minutes
```

M5-A exact Apple grant binding verifies matching grant issuer+subject, not merely grant-row existence.

PostgreSQL-safe FK name:

```text
fk_external_link_challenge_apple_grant
```

Runtime:

```text
SELECT, INSERT, DELETE
NO UPDATE
```

Successful confirm consumes challenge in the same authoritative transaction as identity creation/reactivation.

---

# 8. `external_signup_challenge`

Purpose: pending provider enrollment when provider proof is valid but DANTE still requires current mailbox proof before canonical Account creation.

Columns:

```text
external_signup_ref
provider_code
issuer
subject
provider_email_address?
provider_email_private?
apple_auth_grant_ref?
continuation_verifier
email_address?
email_comparison_key?
otp_verifier?
otp_key_id?
verification_issued_at?
verification_expires_at?
failed_verification_attempts
bootstrap_display_name?
bootstrap_given_name?
bootstrap_family_name?
bootstrap_picture_url?
bootstrap_locale?
created_at
updated_at
expires_at
```

Keys/invariants:

```text
UNIQUE(issuer,subject)
UNIQUE(continuation_verifier)
continuation verifier 32 bytes
Google → no Apple grant
Apple → exact Apple grant required
email address/key all-or-none
OTP state all-or-none when email present
OTP verifier 32 bytes
OTP <= 15 minutes
challenge <= 30 minutes
failed_verification_attempts 0..5
bootstrap fields bounded
```

M5-A exact Apple grant binding verifies matching grant issuer+subject.

PostgreSQL-safe FK name:

```text
fk_external_signup_challenge_apple_grant
```

Terminal mailbox proof:

```text
email still unowned
→ Account + verified EmailIdentity + ExternalIdentity
→ bind Apple grant if applicable
→ AuthSession
→ profile bootstrap if useful

email now owned due race
→ no duplicate Account
→ convert verified provider evidence into ExternalLinkChallenge
```

Database uniqueness remains final arbiter.

Runtime:

```text
SELECT, INSERT, DELETE
UPDATE only bounded email/OTP/attempt/time fields
provider/bootstrap identity evidence immutable
```

---

# 9. `account_profile_bootstrap`

Bounded non-canonical first-account provider bootstrap staging.

Columns:

```text
account_ref             uuid PK/FK Account
source_provider_code
source_issuer
display_name?
given_name?
family_name?
picture_url?
locale?
created_at
expires_at
```

Rules:

```text
source provider/issuer canonical pair
at least one bootstrap value present
bounded trimmed values
expires_at > created_at and <= created_at + 30 days
NO UPDATE lifecycle
```

Lifecycle:

```text
first provider Account creation → optional INSERT
future canonical profile/setup consumes → DELETE
later provider login → MUST NOT refresh/overwrite
expiry → DELETE
```

M5-A adds `expires_at` cleanup indexing.

Runtime:

```text
SELECT, INSERT, DELETE
```

Remote picture URL is not an unrestricted SSRF fetch primitive.

---

# 10. `webauthn_account`

One stable opaque WebAuthn user handle per DANTE Account.

```text
account_ref   uuid        NOT NULL
user_handle   bytea       NOT NULL
created_at    timestamptz NOT NULL
```

Keys:

```text
PK/FK account_ref → account
UQ user_handle
UQ (account_ref,user_handle)
CHECK octet_length(user_handle)=32
CHECK finite created_at
```

`user_handle` is immutable random 256-bit state. Never use AccountRef/email/PersonRef as WebAuthn `user.id`.

Runtime:

```text
SELECT, INSERT
NO UPDATE/DELETE
```

---

# 11. `passkey_credential`

Durable public WebAuthn credential. Private keys never reach DANTE.

Columns:

```text
passkey_credential_ref   uuid        NOT NULL
account_ref              uuid        NOT NULL
credential_id            bytea       NOT NULL
credential_public_key    bytea       NOT NULL
cose_algorithm           integer     NOT NULL
sign_count               bigint      NOT NULL
backup_eligible          boolean     NOT NULL
backup_state             boolean     NOT NULL
transports               text[]      NOT NULL
label                    text        NOT NULL
status_code              text        NOT NULL
created_at               timestamptz NOT NULL
updated_at               timestamptz NOT NULL
last_used_at             timestamptz NULL
revoked_at               timestamptz NULL
revocation_reason_code   text        NULL
```

Keys:

```text
PK passkey_credential_ref
FK account_ref → webauthn_account(account_ref)
UQ credential_id
```

Checks include:

```text
UUIDv7 ref
1..1023 credential-id bytes
1..8192 public-key bytes
sign_count 0..4294967295
backup_state=true → backup_eligible=true
transports bounded / no NULL element
label trimmed/nonempty <=100
status active|revoked
finite ordered timestamps
active/revoked fields exact
```

Do **not** DB-enumerate transport strings; future valid standardized transports are accepted after bounded application normalization.

Immutable:

```text
credential_public_key
credential_id
cose_algorithm
backup_eligible
Account binding
```

Successful assertion:

```text
larger sign_count → persist larger value
zero/non-increasing valid count → do not lower stored count; bounded risk signal
backup_state may update from verified authenticator data
last_used_at / updated_at advance
```

Removal is logical revoke, not SQL DELETE. Credential-id lifetime uniqueness remains.

Runtime:

```text
SELECT, INSERT
UPDATE sign_count, backup_state, label, status/timestamps/revocation metadata
NO DELETE
```

---

# 12. `webauthn_challenge`

Purpose-specific short-lived WebAuthn ceremony state.

Columns:

```text
webauthn_challenge_ref          uuid        NOT NULL
ceremony_code                   text        NOT NULL
challenge_verifier              bytea       NOT NULL
account_ref                     uuid        NULL
auth_session_ref                uuid        NULL
auth_session_secret_verifier    bytea       NULL
user_handle                     bytea       NULL
rp_id                           text        NOT NULL
expected_origin                 text        NOT NULL
created_at                      timestamptz NOT NULL
expires_at                      timestamptz NOT NULL
claimed_at                      timestamptz NULL
```

Ceremonies:

```text
registration
authentication
reauthentication
```

Keys/invariants after M5-A:

```text
PK challenge ref
UQ challenge_verifier
anonymous authentication → Account/session/userHandle fields NULL
registration/reauth → all binding fields present
exact (auth_session_ref,account_ref) FK
exact (account_ref,user_handle) FK
challenge/session verifiers exactly 32 bytes
rp_id/origin bounded
TTL <= 5 minutes
claimed_at within lifetime
```

Registration requires recent auth at begin and rechecks at complete.

Reauthentication requires current session + CSRF but **does not** require already-fresh recent auth; successful proof refreshes `recent_auth_at` and rotates the same session bearer.

Runtime:

```text
SELECT, INSERT, DELETE
UPDATE claimed_at only
```

---

# 13. Account security / anti-lockout rules

Every authenticator mutation uses Account security serialization and re-reads current truth under lock.

Active direct authenticators:

```text
PasswordCredential present
active ExternalIdentity count
active PasskeyCredential count
```

Normal removal must preserve at least one direct authenticator.

A passwordless Account additionally retains at least one verified, recovery-eligible EmailIdentity.

UI checks are advisory only; backend transaction is authority.

Security-sensitive successful mutations that retain the current session rotate its bearer verifier.

---

# 14. Password lifecycle adaptation

## Establish first password

```text
valid AuthSession + CSRF + recent auth
+ password policy + HIBP fail-closed
+ Argon2id/pepper outside DB transaction
→ Account security lock
→ assert PasswordCredential still absent
→ invalidate pending password recovery proof
→ INSERT PasswordCredential
→ rotate current session bearer
```

## Remove password

```text
valid AuthSession + CSRF + recent auth
→ Account security lock
→ anti-lockout recheck
→ invalidate pending recovery proof
→ DELETE PasswordCredential
→ rotate current session bearer
```

## Passwordless recovery

Existing M4 `password_recovery_challenge` remains the proof table.

```text
strong exact EmailIdentity+Account recovery proof
→ Account security lock
→ PasswordCredential exists?
   yes → replace
   no  → insert first credential
→ conditionally consume proof
→ revoke ALL AuthSessions
→ COMMIT/reconcile
→ NO auto-login
→ fresh signin
```

Normal password add/remove/change invalidates older recovery proof under the same Account lock.

---

# 15. Provider state machines

## Known provider identity sign-in

```text
begin
→ transaction + state/nonce capability
→ provider proof
→ claim transaction
→ verify provider/network evidence outside DB write transaction
→ resolve active ExternalIdentity by issuer+subject
→ Account lock
→ re-read Account/ExternalIdentity active
→ reconcile Apple grant if Apple
→ create canonical AuthSession
→ commit/reconcile
→ session cookie only after durable success
```

## New provider identity with accepted mailbox authority

```text
provider proof
→ normalize/classify email
→ no existing EmailIdentity collision
→ Account transaction
→ Account + verified EmailIdentity + ExternalIdentity
→ Apple grant bind if applicable
→ profile bootstrap if useful
→ AuthSession
```

## New provider identity requiring DANTE mailbox proof

```text
provider proof
→ ExternalSignupChallenge
→ mailbox input if necessary
→ DANTE OTP
→ terminal new-account or collision transition
```

No Account before accepted mailbox proof.

## Provider-first collision

```text
valid provider proof
+ provider email matches existing EmailIdentity
→ no Account creation
→ ExternalLinkChallenge targeted to exact Account/EmailIdentity
→ Secure HttpOnly link-flow cookie
→ user authenticates existing Account
→ explicit confirm
→ Account lock + recent-auth recheck
→ issuer+subject uniqueness recheck
→ create/reactivate ExternalIdentity
→ bind Apple grant if applicable
→ consume challenge
→ rotate current session bearer
```

## Authenticated provider link

```text
begin purpose=link
requires session + CSRF + recent auth
→ provider proof
→ Account lock
→ recent-auth recheck
→ issuer+subject uniqueness recheck
→ create/reactivate identity for same Account
→ rotate bearer
```

No ExternalLinkChallenge required because Account control already exists.

## Provider reauthentication

```text
begin purpose=reauthenticate
requires valid session + CSRF
DOES NOT require recent auth
→ provider proof
→ exact session + begin-time bearer verifier must still match
→ Account lock
→ same auth_session_ref
→ recent_auth_at refresh
→ bearer rotation
```

---

# 16. Apple callback and notification topology

Apple callback:

```text
POST /api/v1/auth/apple/callback
Content-Type: application/x-www-form-urlencoded
```

It is the single reviewed external browser-ingress exception to normal same-origin unsafe-API CSRF handling.

Security authority remains:

```text
state verifier
+ nonce
+ expected provider/client audience
+ code exchange
+ signed ID-token verification
+ session snapshot for link/reauth
```

After terminal processing return `303 See Other` to a **fixed DANTE destination** selected from bounded stored `return_target_code`, never arbitrary return URLs.

Apple notifications:

```text
POST /api/v1/auth/apple/notifications
```

Verify signed payload/JWS first.

Relevant classes:

```text
email-disabled
email-enabled
consent-revoked
account-deleted
```

Rules:

```text
email disabled/enabled
→ exact bound EmailIdentity reachability state with event-time ordering

consent revoked/account deleted
→ Account lock where bound
→ local ExternalIdentity revoke
→ AppleAuthGrant reconciliation
→ never delete DANTE Account merely because Apple state changed
```

---

# 17. Exact M5 public API inventory

All routes are under `/api/v1`, use stable operationIds, RFC 9457 problems, request IDs and `Cache-Control: no-store` for sensitive Auth responses.

## Google

```text
POST /api/v1/auth/google/begin
operationId: auth_begin_google_authentication

POST /api/v1/auth/google/complete
operationId: auth_complete_google_authentication
```

Begin purpose:

```text
sign_in        → anonymous allowed
link           → AuthSession + CSRF + recent auth
reauthenticate → AuthSession + CSRF; recent auth NOT required
```

## Apple

```text
POST /api/v1/auth/apple/begin
operationId: auth_begin_apple_authentication

POST /api/v1/auth/apple/callback
operationId: auth_handle_apple_callback

POST /api/v1/auth/apple/notifications
operationId: auth_process_apple_notification
```

## Provider enrollment

```text
GET  /api/v1/auth/provider-enrollment
operationId: auth_get_provider_enrollment

POST /api/v1/auth/provider-enrollment/email
operationId: auth_set_provider_enrollment_email

POST /api/v1/auth/provider-enrollment/verify
operationId: auth_verify_provider_enrollment

POST /api/v1/auth/provider-enrollment/resend
operationId: auth_resend_provider_enrollment_verification
```

## Provider link / methods

```text
GET /api/v1/auth/provider-link
operationId: auth_get_provider_link

POST /api/v1/auth/provider-link/confirm
operationId: auth_confirm_provider_link

GET /api/v1/auth/methods
operationId: auth_get_authentication_methods

DELETE /api/v1/auth/providers/{external_identity_ref}
operationId: auth_unlink_provider
```

## Password management

```text
POST /api/v1/auth/password/establish
operationId: auth_establish_password

DELETE /api/v1/auth/password
operationId: auth_remove_password
```

Existing M4 `/auth/reset-password` remains stable and adapts internally to create-or-replace credential.

## Passkeys

```text
POST /api/v1/auth/passkeys/registration/begin
operationId: auth_begin_passkey_registration

POST /api/v1/auth/passkeys/registration/complete
operationId: auth_complete_passkey_registration

POST /api/v1/auth/passkeys/authentication/begin
operationId: auth_begin_passkey_authentication

POST /api/v1/auth/passkeys/authentication/complete
operationId: auth_complete_passkey_authentication

POST /api/v1/auth/passkeys/reauthentication/begin
operationId: auth_begin_passkey_reauthentication

POST /api/v1/auth/passkeys/reauthentication/complete
operationId: auth_complete_passkey_reauthentication

PATCH /api/v1/auth/passkeys/{passkey_credential_ref}
operationId: auth_update_passkey

DELETE /api/v1/auth/passkeys/{passkey_credential_ref}
operationId: auth_remove_passkey
```

Registration:

```text
AuthSession + CSRF + recent auth
residentKey required
userVerification required
attestation none
```

Anonymous authentication is discoverable/username-less and creates a fresh canonical AuthSession.

Passkey reauth refreshes recent auth and rotates same session bearer.

PATCH changes label only in M5.

---

# 18. Provider authentication success union

Google complete and Apple callback resolve to:

```text
authenticated
link_required
enrollment_required
```

Email collision is a typed `link_required` state, not an error.

Frontend never infers DANTE success from provider SDK callback alone.

---

# 19. Machine problem codes

M5 stable additions:

```text
auth.provider_transaction_invalid_or_expired
auth.provider_proof_invalid
auth.provider_link_invalid_or_expired
auth.provider_link_account_mismatch
auth.provider_identity_conflict
auth.provider_reconciliation_pending
auth.provider_enrollment_invalid_or_expired
auth.provider_enrollment_verification_invalid_or_expired
auth.passkey_challenge_invalid_or_expired
auth.passkey_verification_failed
auth.passkey_already_registered
auth.passkey_not_found
auth.password_already_established
auth.authenticator_removal_blocked
dependency.provider_unavailable
auth.provider_rate_limited
auth.passkey_rate_limited
```

Existing codes remain authoritative where applicable:

```text
auth.authentication_required
auth.reauthentication_required
auth.session_expired
auth.account_unavailable
security.csrf_failed
conflict.state_changed
request.validation_failed
rate_limit.exceeded
service.unavailable
internal.unexpected
```

No client parses provider/backend English text.

---

# 20. Browser flow-cookie contract

M5 bounded Secure HttpOnly host-only flow cookies:

```text
__Host-dante-provider-link
__Host-dante-provider-enrollment
```

Properties:

```text
Secure
HttpOnly
Path=/
SameSite=Lax
Max-Age <= backing challenge TTL
raw high-entropy continuation capability only
never localStorage/sessionStorage
```

Ordinary `__Host-dante-session` policy is unchanged.

Google begin/complete transaction capability remains browser-memory only; Apple transports transaction capability as provider `state`.

---

# 21. WebAuthn RP/origin contract

Production:

```text
RP ID = exact configured DANTE registrable application domain
allowed origins = explicit canonical HTTPS origins
```

No suffix/substring origin acceptance.

Local browser proof:

```text
origin = https://localhost:<ephemeral-port>
RP ID  = localhost
```

`https://127.0.0.1` is not M5 WebAuthn RP authority.

Each issued challenge persists exact `rp_id` and `expected_origin`; configuration changes cannot reinterpret an already-issued ceremony.

---

# 22. Dependency direction / M5-B accepted admission

Accepted M5-B baseline as of 2026-08-30:

```text
fido2         2.2.1
joserfc       1.7.4
cryptography  50.0.1
existing httpx2
Python        3.14
uv            0.12.5
```

This is accepted lock/runtime truth for M5-B, not a candidate list.

M5-B admission proved:

```text
Python 3.14 compatibility in the project runtime
explicit JOSE RS256 allowlist
strict JWK parsing/rotation bounds
WebAuthn policy construction through fido2
Apple grant AEAD through cryptography AESGCM
no credential/token logging behavior introduced
Ruff/mypy/test/build compatibility
uv lock determinism / uv lock --check
```

The permanent rule remains: do not hand-roll JWT/JWS/JWK, CBOR/COSE/WebAuthn or AES-GCM.

Future dependency upgrades require their own current compatibility/advisory review; later M5 slices do not silently widen the algorithms or trust sources admitted by M5-B.

---

# 23. Rate/resource controls

Bound before expensive work where possible:

```text
provider begin issuance
provider complete failures
JWK refresh
provider enrollment email/OTP issuance
provider link attempts
passkey challenge issuance
passkey verification failures
Apple notification verification
Apple pending/revocation reconciliation
```

Unknown `kid` may cause one bounded coordinated JWK refresh, not one refresh per concurrent request.

Provider requests use bounded connect/read/total timeouts.

No per-request unbounded background task creation.

---

# 24. Logging/privacy

Never log/persist in telemetry:

```text
Google/Apple ID token
authorization code
Apple refresh/access token
Apple client private key/client-secret JWT
raw provider transaction/state capability
raw OIDC nonce
raw passkey challenge
raw WebAuthn assertion/signature beyond protected bounded diagnostics
session/CSRF secret
OTP/recovery secret
password
```

Safe logs use DANTE refs, provider class, request ID and bounded machine failure category.

Provider email/name/avatar/locale are personal data.

Provider subject is security identity data; do not expose it to normal UI/logs for convenience.

---

# 25. Concurrency/race contract

Deterministic proof is required where DB state is arbiter:

```text
two first provider signins for same issuer+subject
same provider identity linked to two Accounts concurrently
provider signin vs Account disable
provider signin vs ExternalIdentity revoke
provider link vs provider revoke
Apple notification vs signin/link
pending Apple grant expiry vs link completion
provider enrollment verify vs competing Account/email creation
passkey duplicate registration
passkey authentication vs passkey removal
add password vs recovery reset
remove password vs pending recovery proof
authenticator removal vs concurrent authenticator removal
reauth vs concurrent bearer rotation
```

Rules:

```text
Account-wide mutation → Account security lock
provider identity uniqueness → DB UNIQUE(issuer,subject)
passkey identity uniqueness → DB UNIQUE(credential_id)
flow replay → conditional claim/consume
network outside DB transaction
commit ambiguity → operation-specific reconciliation only
no blind mutation retry
```

---

# 26. Proof matrix

## Pure/unit

```text
provider claim normalization
issuer/audience/nonce rules
Google mailbox-authority classification
Apple event ordering decision
AEAD AAD/key-ring behavior
flow verifier hashing
anti-lockout decision
WebAuthn option policy
signCount risk policy
problem mapping
```

## Real PostgreSQL

M5-A proves the persistence foundation. Later lifecycle slices add focused PG proof only where they add DB/race behavior.

```text
PK/FK/UQ/CHECK/index/ACL
EmailIdentity reachability ordering
ExternalIdentity uniqueness/revocation
flow TTL/claim/consume
pending Apple grant lifecycle
Account-lock races
provider collision/account creation races
passkey duplicate/removal/auth races
password/recovery races
```

M5-C focused PostgreSQL proof is accepted for the Google application/persistence behavior added by that slice.

M5-D focused PostgreSQL proof is accepted for Apple transaction/grant/collision/enrollment/link/reauth/notification/revocation behavior, and the M5-D closeout additionally passed the full 111-test PostgreSQL regression suite.

## FastAPI HTTP

```text
exact paths/status/media/cache-control/request-id
CSRF/session requirements by purpose
Apple form_post boundary
Apple notification boundary
RFC9457 problems
no unsafe field exposure
```

## OpenAPI/generated client

```text
deterministic OpenAPI without live providers/secrets
operationIds exactly frozen
success-union schemas
RFC9457 typed problems
governed client only
```

## Web/browser

```text
Google/Apple controls + cancel/error states
provider-enrollment OTP
provider collision → Account proof → explicit link
smart bootstrap without redundant questions
passkey registration
username-less passkey authentication
passkey reauth
flow-cookie/URL scrubbing
hard refresh authoritative
Chromium/Firefox/WebKit truthful capability matrix
```

## Real providers

Before M5 production-ready closure:

```text
real Google configured-client smoke/UAT
real Apple registered HTTPS Services ID/domain smoke/UAT
Apple Private Email Relay delivery configuration proof
real provider revoke/account-change path where safely testable
real WebAuthn/passkey UAT
```

CI remains deterministic and does not depend on public providers.

---

# 27. Current implementation order

```text
M5-A   persistence foundations                              COMPLETE / PROVEN
M5-B   provider/JWK/JOSE/AEAD infrastructure               COMPLETE / ENGINEERING PASS
M5-C   Google                                              COMPLETE / ENGINEERING PASS
M5-D   Apple grant/callback/notifications                   COMPLETE / ENGINEERING PASS
M5-E   linking + authenticator management/anti-lockout      NEXT
M5-F   WebAuthn/passkeys                                    PLANNED
M5-G   add/remove password + passwordless recovery          PLANNED
M5-H   FastAPI public materialization                       PLANNED
M5-I   deterministic OpenAPI + governed client              PLANNED
M5-J   Access Web/smart onboarding                          PLANNED
M5-K+  focused proof → provider/browser UAT → acceptance    PLANNED
```

Do not combine the entire M5 implementation into one uncontrolled patch.

---

# 28. Current closure state

```text
M5.1 architecture/external-authority freeze   COMPLETE
M5.2 exact persistence/API design             COMPLETE
M5-A persistence materialization              COMPLETE
M5-A real PostgreSQL acceptance               95 / 95 PASS
M5-A current catalog parity                   PASS
M5-A static/type/fast/build                    PASS
M5-B provider/JWK/JOSE/AEAD infrastructure    COMPLETE / ENGINEERING PASS
M5-B fast                                      127 / 127 PASS
M5-B Ruff/mypy/build                           PASS
M5-C Google backend                            COMPLETE / ENGINEERING PASS
M5-C fast                                      148 / 148 PASS
M5-C focused real PostgreSQL                    7 / 7 PASS
M5-C Ruff/mypy/build                           PASS
M5-D Apple backend                             COMPLETE / ENGINEERING PASS
M5-D fast                                      171 / 171 PASS
M5-D focused real PostgreSQL                    9 / 9 PASS
M5-D full real PostgreSQL                     111 / 111 PASS
M5-D Ruff/mypy/build                           PASS
M5-E                                           NEXT
```

M5 as a whole remains ACTIVE. Accepted M5-A persistence, M5-B runtime infrastructure, M5-C Google backend behavior and M5-D Apple backend behavior do not imply provider-management completion, public API/Web materialization, browser/provider UAT or whole-M5 completion.