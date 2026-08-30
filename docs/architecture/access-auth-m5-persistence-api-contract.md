# DANTE — Access/Auth M5 Persistence + API Contract

- **Status:** CURRENT / BRANCH-LOCAL AUTHORITATIVE FOR M5.2 / DESIGN FREEZE COMPLETE
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Prerequisite:** M1–M4 CLOSED; M5.1 architecture/external-authority freeze COMPLETE
- **Runtime materialization:** NOT STARTED at this checkpoint
- **Accepted PostgreSQL head before M5 implementation:** `20260829_11`
- **Next implementation step:** M5-A — persistence foundations (Dictionary → SQLAlchemy → Alembic → PostgreSQL proof)
- **Companion authority:** `access-auth-m5-contract.md`
- **Binding foundations:** Access/Auth architecture/security/API/testing contracts, ADR-011, Database System of Record, CP6 persistence constitution

This document freezes the **exact M5 persistence and public-API design** required before implementation of Google authentication, Sign in with Apple, passkeys/WebAuthn, explicit provider linking, passwordless Accounts and authenticator management.

It is an implementation contract, not evidence that the schema/API exists yet.

---

## 1. Design result

M5 materializes the following physical delta:

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

Exactly **9 new tables** are frozen by M5.2.

No generic `auth_token`, `oauth_token`, `provider_challenge`, `credential`, `security_blob` or other cross-purpose god-table is permitted.

M5.2 deliberately does **not** add speculative session-method/security-event columns. Current M5 methods must satisfy the accepted policy for the operation they authorize. Durable whole-vertical security-event/session-management history remains an M7 concern unless implementation proves an earlier correctness dependency.

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

Identifiers are named below. If PostgreSQL's 63-byte identifier ceiling requires shortening during Alembic materialization, the shorter name must be frozen consistently across Dictionary, migration, mappings and catalog tests before acceptance.

All timestamps are `timestamp with time zone`, finite, application-supplied UTC instants.

All external strings are bounded before persistence. Application validation remains stricter where protocol syntax cannot be expressed safely as a small PostgreSQL CHECK.

Raw capabilities are never stored. When a flow uses a high-entropy raw secret, PostgreSQL stores only a 32-byte verifier derived with the purpose-specific M5 verifier primitive frozen by implementation. The implementation may use SHA-256 for uniformly random 256-bit flow secrets where no password-hardening property is needed; raw values never enter logs.

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
= latest provider reachability evidence timestamp relevant to that restriction, retained even when the restriction is cleared
```

M5 initial code vocabulary:

```text
provider_delivery_disabled
```

The vocabulary may be extended only by an explicit later contract; do not overload the field with SMTP bounce heuristics.

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

Important Apple ordering rule:

```text
email-disabled event at T
→ update only if T > current recovery_restriction_observed_at (or current is NULL)
→ set code = provider_delivery_disabled
→ set observed_at = T

email-enabled event at T
→ update only if T > current recovery_restriction_observed_at (or current is NULL)
→ set code = NULL
→ retain observed_at = T
```

Therefore a replayed/out-of-order old Apple event cannot reverse newer reachability truth.

M5 runtime ACL delta:

```text
GRANT UPDATE (
  recovery_restriction_code,
  recovery_restriction_observed_at
) ON dante.email_identity TO dante_runtime
```

Existing SELECT/INSERT posture remains.

---

# 4. `external_identity`

## 4.1 Purpose

Durable lifetime binding between one DANTE Account and one verified external provider identity.

Provider identity authority:

```text
issuer + subject
```

Email is not the identity key.

## 4.2 Columns

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

`provider_email_address` is a display/support hint only. It never participates in Account lookup/link authority.

`provider_email_private` is present iff a provider email hint is present. In M5 it is always false for Google and may reflect Apple's private-relay claim for Apple.

## 4.3 Keys / constraints

```text
PK  pk_external_identity
    (external_identity_ref)

FK  fk_external_identity_account_ref_account
    (account_ref)
    → dante.account(account_ref)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION

FK  fk_external_identity_email_account_email_identity
    (email_identity_ref, account_ref)
    → dante.email_identity(email_identity_ref, account_ref)
    MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION

UQ  uq_external_identity_issuer_subject
    (issuer, subject)
```

No `UNIQUE(account_ref, provider_code)` is created.

Checks:

```text
uuid_extract_version(external_identity_ref) IS NOT DISTINCT FROM 7
provider_code IN ('google','apple')

(
  provider_code='google'
  AND issuer='https://accounts.google.com'
)
OR (
  provider_code='apple'
  AND issuer='https://appleid.apple.com'
)

subject = btrim(subject)
AND subject <> ''
AND char_length(subject) <= 255

(provider_email_address IS NULL AND provider_email_private IS NULL)
OR (
  provider_email_address IS NOT NULL
  AND provider_email_address = btrim(provider_email_address)
  AND provider_email_address <> ''
  AND char_length(provider_email_address) <= 320
  AND provider_email_private IS NOT NULL
)

status_code IN ('active','revoked')

isfinite(created_at)
AND isfinite(status_changed_at)
AND isfinite(last_authenticated_at)
AND status_changed_at >= created_at
AND last_authenticated_at >= created_at

(status_code='active'
 AND revoked_at IS NULL
 AND revocation_reason_code IS NULL)
OR
(status_code='revoked'
 AND revoked_at IS NOT NULL
 AND isfinite(revoked_at)
 AND revoked_at >= created_at
 AND revocation_reason_code IN (
   'user_unlinked',
   'provider_revoked',
   'provider_account_deleted'
 ))
```

## 4.4 Indexes

```text
PK / UQ backing indexes
ix_external_identity_account_ref          (account_ref)
ix_external_identity_email_identity_ref    (email_identity_ref)
```

## 4.5 Lifecycle

Normal unlink is **logical revocation**, not SQL DELETE.

```text
active → revoked
```

The `(issuer, subject)` row is retained so the external identity cannot silently be recycled onto another Account after unlink.

A fresh explicit proof may reactivate the same row only for the same owning Account. Moving a lifetime provider identity to another Account is outside normal M5 linking and requires a future explicit account-transfer/deletion policy.

Provider email/profile changes never change `account_ref` or `(issuer, subject)`.

## 4.6 Runtime ACL

```text
SELECT
INSERT (
  external_identity_ref, account_ref, email_identity_ref,
  provider_code, issuer, subject,
  provider_email_address, provider_email_private,
  status_code, created_at, status_changed_at,
  last_authenticated_at, revoked_at, revocation_reason_code
)
UPDATE (
  provider_email_address, provider_email_private,
  status_code, status_changed_at,
  last_authenticated_at, revoked_at, revocation_reason_code
)
```

No runtime DELETE.

---

# 5. `external_auth_transaction`

## 5.1 Purpose

Short-lived server-authoritative transaction for Google/Apple authentication before final provider evidence is applied to DANTE state.

One table is valid because Google and Apple transactions share the same lifecycle/security semantics; provider-specific network details remain adapters.

## 5.2 Columns

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

Semantics:

```text
purpose_code:
  sign_in
  link
  reauthenticate

return_target_code:
  access
  security
```

`state_verifier` is the verifier for the high-entropy transaction capability:

- Apple: raw capability is the provider `state` value.
- Google: raw capability is an in-memory client flow secret returned by begin and supplied to complete; it is never browser-persisted.

`nonce_verifier` binds the server-issued OIDC nonce.

`auth_session_secret_verifier` is a snapshot of the exact DANTE AuthSession bearer verifier at begin. It is **not** a raw session secret and is intentionally not a foreign key, because AuthSession bearer rotation must remain possible.

## 5.3 Keys / constraints

```text
PK  pk_external_auth_transaction
    (external_auth_transaction_ref)

FK  fk_external_auth_transaction_auth_session_ref_auth_session
    (auth_session_ref)
    → dante.auth_session(auth_session_ref)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION

UQ  uq_external_auth_transaction_state_verifier
    (state_verifier)

UQ  uq_external_auth_transaction_nonce_verifier
    (nonce_verifier)
```

Checks:

```text
UUIDv7 ref
provider_code IN ('google','apple')
provider/expected_issuer canonical pair
purpose_code IN ('sign_in','link','reauthenticate')
return_target_code IN ('access','security')
octet_length(state_verifier)=32
octet_length(nonce_verifier)=32

purpose_code='sign_in'
→ auth_session_ref IS NULL
  AND auth_session_secret_verifier IS NULL

purpose_code IN ('link','reauthenticate')
→ auth_session_ref IS NOT NULL
  AND auth_session_secret_verifier IS NOT NULL
  AND octet_length(auth_session_secret_verifier)=32

isfinite(created_at)
AND isfinite(expires_at)
AND expires_at > created_at
AND expires_at <= created_at + interval '15 minutes'

claimed_at IS NULL
OR (
  isfinite(claimed_at)
  AND claimed_at >= created_at
  AND claimed_at <= expires_at
)
```

## 5.4 Claim semantics

Completion begins with a single conditional claim:

```text
UPDATE ...
SET claimed_at = :now
WHERE ref + verifier match
  AND claimed_at IS NULL
  AND expires_at > :now
RETURNING ...
```

Apple claim happens **before** authorization-code exchange. Two callbacks cannot exchange the same single-use Apple code twice.

If an Apple exchange has an ambiguous network outcome after claim, do not replay the code. The transaction stays claimed and the user restarts.

## 5.5 Indexes / ACL

```text
ix_external_auth_transaction_expires_at       (expires_at)
ix_external_auth_transaction_auth_session_ref (auth_session_ref)
```

Runtime:

```text
SELECT, INSERT, DELETE
UPDATE (claimed_at)
```

DELETE is cleanup/terminal retention only.

---

# 6. `apple_auth_grant`

## 6.1 Purpose

Durable encrypted Apple server-side refresh-grant lifecycle, including the period between successful Apple code exchange and final DANTE Account link/create.

This table intentionally supports **pending unbound grants** so DANTE never loses the token required to revoke an abandoned/expired Apple authorization.

## 6.2 Columns

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

## 6.3 Encryption

For `pending`, `active` and `revocation_pending`:

```text
refresh_token_ciphertext != NULL
refresh_token_nonce      = 12 bytes
key id                   != NULL
```

Use application-layer AEAD, baseline AES-256-GCM through `cryptography`.

Key material is outside PostgreSQL, Git and logs.

Stable AAD direction:

```text
dante:apple-auth-grant:v1:
<apple_auth_grant_ref>:
<issuer>:
<subject>:
<client_id>
```

Never reuse a nonce under the same encryption key.

After confirmed provider revocation, secret material is nulled.

## 6.4 Keys / constraints

```text
PK  pk_apple_auth_grant
    (apple_auth_grant_ref)

FK  fk_apple_auth_grant_external_identity_ref_external_identity
    (external_identity_ref)
    → dante.external_identity(external_identity_ref)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION

UQ  uq_apple_auth_grant_issuer_subject
    (issuer, subject)

UQ  uq_apple_auth_grant_external_identity_ref
    (external_identity_ref)
```

Checks include:

```text
UUIDv7 ref
issuer='https://appleid.apple.com'
subject trimmed/nonempty <=255
client_id trimmed/nonempty <=255
status_code IN ('pending','active','revocation_pending','revoked')
finite/ordered timestamps

pending:
  external_identity_ref MAY be NULL
  pending_expires_at NOT NULL
  pending_expires_at <= created_at + interval '30 minutes'
  token fields all NOT NULL

active:
  external_identity_ref NOT NULL
  pending_expires_at IS NULL
  token fields all NOT NULL

revocation_pending:
  token fields all NOT NULL
  revocation_requested_at NOT NULL

revoked:
  revoked_at NOT NULL
  token fields all NULL

refresh_token_ciphertext when present:
  octet_length > 16
  octet_length <= 16384
refresh_token_nonce when present:
  octet_length = 12
encryption_key_id when present:
  trimmed/nonempty <=128
```

## 6.5 Lifecycle

New unbound Apple proof:

```text
code exchange + identity verification
→ create/reconcile pending AppleAuthGrant
→ then enter direct Account create OR link challenge OR enrollment challenge
```

Successful bind:

```text
pending
→ external_identity_ref set
→ active
→ pending_expires_at cleared
```

User unlink/provider revoke:

```text
local ExternalIdentity disabled first
→ AppleAuthGrant revocation_pending
→ COMMIT
→ provider revoke outside DB transaction
→ on confirmed success: revoked + encrypted token material cleared
```

Provider outage never keeps the external identity locally usable.

Expired abandoned pending grant:

```text
pending expiry
→ revocation_pending
→ bounded reconciliation worker
→ revoke
→ revoked / secret cleared
```

## 6.6 Index / ACL

```text
ix_apple_auth_grant_status_updated_at (status_code, updated_at)
```

Runtime:

```text
SELECT, INSERT
UPDATE (
  external_identity_ref,
  refresh_token_ciphertext,
  refresh_token_nonce,
  encryption_key_id,
  status_code,
  updated_at,
  status_changed_at,
  pending_expires_at,
  revocation_requested_at,
  revoked_at
)
```

No runtime DELETE.

---

# 7. `external_link_challenge`

## 7.1 Purpose

Short-lived provider-first collision state after valid provider proof identifies an email already owned by a DANTE Account. It carries sufficient verified provider identity evidence for explicit linking **without** creating a duplicate Account or silently merging by email.

## 7.2 Columns

```text
external_link_challenge_ref  uuid        NOT NULL
target_account_ref           uuid        NOT NULL
target_email_identity_ref    uuid        NOT NULL
provider_code                text        NOT NULL
issuer                       text        NOT NULL
subject                      text        NOT NULL
provider_email_address       text        NULL
provider_email_private       boolean     NULL
apple_auth_grant_ref         uuid        NULL
continuation_verifier        bytea       NOT NULL
created_at                   timestamptz NOT NULL
expires_at                   timestamptz NOT NULL
```

The raw continuation capability is held only in the Secure HttpOnly host-only provider-link flow cookie.

## 7.3 Keys / constraints

```text
PK  pk_external_link_challenge

FK  (target_account_ref) → account
FK  (target_email_identity_ref,target_account_ref)
    → email_identity(email_identity_ref,account_ref)
FK  (apple_auth_grant_ref) → apple_auth_grant

UQ  uq_external_link_challenge_issuer_subject
    (issuer,subject)
UQ  uq_external_link_challenge_continuation_verifier
    (continuation_verifier)
```

Checks:

```text
UUIDv7 ref
canonical provider/issuer pair
subject trimmed <=255
provider email all-or-none with private flag
octet_length(continuation_verifier)=32

provider_code='google' → apple_auth_grant_ref IS NULL
provider_code='apple'  → apple_auth_grant_ref IS NOT NULL

expires_at > created_at
AND expires_at <= created_at + interval '15 minutes'
```

## 7.4 Index / ACL

```text
ix_external_link_challenge_target_account_ref        (target_account_ref)
ix_external_link_challenge_target_email_identity_ref (target_email_identity_ref)
ix_external_link_challenge_apple_auth_grant_ref      (apple_auth_grant_ref)
ix_external_link_challenge_expires_at                 (expires_at)
```

Runtime:

```text
SELECT, INSERT, DELETE
```

No UPDATE. Successful confirm consumes via same transaction that creates/reactivates ExternalIdentity.

Expired Apple-linked challenges transition the pending grant toward revocation before the challenge is finally purged.

---

# 8. `external_signup_challenge`

## 8.1 Purpose

Pending provider enrollment when provider proof is valid but DANTE still requires current mailbox proof before a canonical Account can exist.

Typical M5 case: Google Account backed by a third-party mailbox where Google `email_verified` is not sufficient as durable DANTE mailbox authority.

## 8.2 Columns

```text
external_signup_ref             uuid        NOT NULL
provider_code                  text        NOT NULL
issuer                         text        NOT NULL
subject                        text        NOT NULL
provider_email_address         text        NULL
provider_email_private         boolean     NULL
apple_auth_grant_ref           uuid        NULL
continuation_verifier          bytea       NOT NULL
email_address                  text        NULL
email_comparison_key           text        NULL
otp_verifier                   bytea       NULL
otp_key_id                     text        NULL
verification_issued_at         timestamptz NULL
verification_expires_at        timestamptz NULL
failed_verification_attempts   integer     NOT NULL
bootstrap_display_name         text        NULL
bootstrap_given_name           text        NULL
bootstrap_family_name          text        NULL
bootstrap_picture_url          text        NULL
bootstrap_locale               text        NULL
created_at                     timestamptz NOT NULL
updated_at                     timestamptz NOT NULL
expires_at                     timestamptz NOT NULL
```

## 8.3 Keys / constraints

```text
PK  pk_external_signup_challenge
FK  (apple_auth_grant_ref) → apple_auth_grant
UQ  uq_external_signup_challenge_issuer_subject
    (issuer,subject)
UQ  uq_external_signup_challenge_continuation_verifier
    (continuation_verifier)
```

Important checks:

```text
UUIDv7 ref
provider/issuer canonical pair
subject trimmed <=255
octet_length(continuation_verifier)=32

provider_code='google' → apple_auth_grant_ref IS NULL
provider_code='apple'  → apple_auth_grant_ref IS NOT NULL

email_address and email_comparison_key are both NULL or both non-NULL

when email is NULL:
  otp_verifier IS NULL
  otp_key_id IS NULL
  verification_issued_at IS NULL
  verification_expires_at IS NULL
  failed_verification_attempts = 0

when email is present:
  normalized/bounded email fields nonempty
  otp_verifier NOT NULL and octet_length=32
  otp_key_id trimmed/nonempty <=128
  verification times NOT NULL
  verification_expires_at > verification_issued_at
  verification_expires_at <= verification_issued_at + interval '15 minutes'
  verification_expires_at <= expires_at

failed_verification_attempts BETWEEN 0 AND 5

finite chronology
expires_at > created_at
expires_at <= created_at + interval '30 minutes'
updated_at >= created_at

bootstrap fields bounded:
 display <=256
 given/family <=128
 picture URL <=2048
 locale <=64
```

At least one bootstrap field is not required; no row in `account_profile_bootstrap` is created when all are absent.

## 8.4 OTP purpose separation

Provider-enrollment OTP uses the existing cryptographic key-management discipline but a distinct purpose/domain-separation string from password signup OTP. A verifier from one challenge family cannot validate in the other.

## 8.5 Verification terminal behavior

Valid mailbox proof re-checks canonical state transactionally:

```text
email belongs to no Account
→ create Account
→ verified EmailIdentity
→ ExternalIdentity
→ bind AppleAuthGrant if applicable
→ AuthSession
→ AccountProfileBootstrap if useful
→ delete challenge

email now belongs to existing Account
→ DO NOT create duplicate Account
→ transition verified provider evidence into ExternalLinkChallenge
→ disclose only safe link-required outcome
→ delete signup challenge
```

Database uniqueness remains the race arbiter.

## 8.6 Index / ACL

```text
ix_external_signup_challenge_email_comparison_key (email_comparison_key)
ix_external_signup_challenge_apple_auth_grant_ref (apple_auth_grant_ref)
ix_external_signup_challenge_expires_at           (expires_at)
```

Runtime:

```text
SELECT, INSERT, DELETE
UPDATE (
  email_address,
  email_comparison_key,
  otp_verifier,
  otp_key_id,
  verification_issued_at,
  verification_expires_at,
  failed_verification_attempts,
  updated_at
)
```

Provider/bootstrap identity evidence is immutable after challenge creation.

---

# 9. `account_profile_bootstrap`

## 9.1 Purpose

Bounded non-canonical staging for useful **first-account** provider profile data until the canonical authenticated profile/settings owner consumes it.

This exists because Apple name data may be one-shot.

It is not a Person/Profile table.

## 9.2 Columns

```text
account_ref             uuid        NOT NULL
source_provider_code    text        NOT NULL
source_issuer           text        NOT NULL
display_name            text        NULL
given_name              text        NULL
family_name             text        NULL
picture_url              text        NULL
locale                   text        NULL
created_at               timestamptz NOT NULL
expires_at               timestamptz NOT NULL
```

## 9.3 Keys / constraints

```text
PK/FK account_ref → dante.account(account_ref)
```

Checks:

```text
source provider/issuer canonical pair
at least one bootstrap value IS NOT NULL
bounded trimmed text
picture_url <=2048
locale <=64
finite chronology
expires_at > created_at
expires_at <= created_at + interval '30 days'
```

No UPDATE lifecycle.

```text
provider proof → INSERT once
future profile/setup owner consumes values → DELETE
provider login later → MUST NOT refresh/overwrite row
expiry → DELETE
```

Runtime:

```text
SELECT, INSERT, DELETE
```

Remote `picture_url` is never a free SSRF fetch primitive. Future avatar import goes through the governed Asset/media boundary.

---

# 10. `webauthn_account`

## 10.1 Purpose

One stable opaque WebAuthn user handle per DANTE Account.

## 10.2 Columns

```text
account_ref   uuid        NOT NULL
user_handle   bytea       NOT NULL
created_at    timestamptz NOT NULL
```

## 10.3 Keys / constraints

```text
PK/FK account_ref → account(account_ref)
UQ uq_webauthn_account_user_handle (user_handle)
CHECK octet_length(user_handle)=32
CHECK isfinite(created_at)
```

`user_handle` is 256 random bits, created once and never changed. `account_ref` is not exposed as WebAuthn `user.id`.

Runtime:

```text
SELECT, INSERT
```

No runtime UPDATE/DELETE in M5.

---

# 11. `passkey_credential`

## 11.1 Purpose

Durable public WebAuthn credential owned by one Account. Private keys never reach DANTE.

## 11.2 Columns

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

No AAGUID/device fingerprint is persisted in M5 because no correctness/product consumer justifies that privacy cost.

## 11.3 Keys / constraints

```text
PK  pk_passkey_credential
FK  account_ref → account
UQ  uq_passkey_credential_credential_id (credential_id)
```

Checks:

```text
UUIDv7 ref
1 <= octet_length(credential_id) <= 1023
1 <= octet_length(credential_public_key) <= 8192
sign_count BETWEEN 0 AND 4294967295
cardinality(transports) <= 8
array_position(transports,NULL) IS NULL
label=btrim(label) AND label<>'' AND char_length(label)<=100
status_code IN ('active','revoked')
finite ordered timestamps
last_used_at IS NULL OR last_used_at >= created_at

active:
  revoked_at/reason NULL

revoked:
  revoked_at finite >= created_at
  revocation_reason_code='user_removed'
```

Do **not** DB-enumerate WebAuthn transport strings. Unknown/future standardized transport values are preserved after bounded application normalization.

`credential_public_key`, `credential_id`, `cose_algorithm`, `backup_eligible` and Account binding are immutable.

## 11.4 Counter / backup updates

On successful assertion:

```text
sign_count increases
→ persist larger count

zero/non-increasing count where credential verifies
→ do not lower stored count
→ treat as bounded risk signal
→ do not auto-lock Account merely from this signal

backup_state may be updated from verified authenticator data
last_used_at / updated_at advance
```

## 11.5 Removal

Passkey DELETE API performs logical revoke, not SQL DELETE. `credential_id` remains lifetime-unique so an old removed credential cannot silently reappear as the same DANTE credential row.

## 11.6 Index / ACL

```text
ix_passkey_credential_account_status (account_ref,status_code)
```

Runtime:

```text
SELECT, INSERT
UPDATE (
  sign_count,
  backup_state,
  label,
  status_code,
  updated_at,
  last_used_at,
  revoked_at,
  revocation_reason_code
)
```

No runtime DELETE.

---

# 12. `webauthn_challenge`

## 12.1 Purpose

One purpose-specific short-lived WebAuthn ceremony state table because registration, anonymous authentication and session reauthentication share the same challenge lifecycle and verifier model.

## 12.2 Columns

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

## 12.3 Keys / constraints

```text
PK  pk_webauthn_challenge
FK  account_ref → account
FK  auth_session_ref → auth_session
UQ  uq_webauthn_challenge_challenge_verifier
    (challenge_verifier)
```

Checks:

```text
UUIDv7 ref
octet_length(challenge_verifier)=32
rp_id trimmed/nonempty <=253
expected_origin trimmed/nonempty <=2048

ceremony_code='authentication'
→ account_ref/auth_session_ref/auth_session_secret_verifier/user_handle all NULL

ceremony_code IN ('registration','reauthentication')
→ account_ref/auth_session_ref/auth_session_secret_verifier/user_handle all NOT NULL
→ octet_length(auth_session_secret_verifier)=32
→ octet_length(user_handle)=32

expires_at > created_at
AND expires_at <= created_at + interval '5 minutes'

claimed_at NULL
OR finite, >=created_at and <=expires_at
```

Registration requires recent auth at begin **and rechecks freshness at complete**.

Reauthentication requires a valid current session but deliberately does **not** require recent auth before the ceremony; successful passkey proof refreshes `recent_auth_at` and rotates that same AuthSession bearer.

## 12.4 Claim / index / ACL

Complete uses a single conditional claim before accepting a response. A failed or replayed ceremony requires a new challenge.

Indexes:

```text
ix_webauthn_challenge_expires_at       (expires_at)
ix_webauthn_challenge_account_ref      (account_ref)
ix_webauthn_challenge_auth_session_ref (auth_session_ref)
```

Runtime:

```text
SELECT, INSERT, DELETE
UPDATE (claimed_at)
```

---

# 13. Account security / anti-lockout rules

Every authenticator mutation uses the accepted Account security serialization function and re-reads current truth under that lock.

M5 active direct authenticators are:

```text
PasswordCredential present
active ExternalIdentity count
active PasskeyCredential count
```

Normal removal must preserve at least one direct authenticator after the mutation.

Additionally, a passwordless Account must retain at least one verified, recovery-eligible EmailIdentity so loss of all external/passkey authenticators is recoverable.

A current password means temporary absence of a usable recovery mailbox does not automatically forbid removal of some *other* authenticator; policy must not manufacture lock-in beyond the accepted recovery invariant.

UI checks are advisory only. The backend transaction is the authority.

Security-sensitive successful mutations retain the same `auth_session_ref` only after rotating its bearer verifier.

---

# 14. Password lifecycle adaptation

## 14.1 Establish first password

Provider/passkey-only Account:

```text
valid AuthSession
+ CSRF
+ recent authentication
+ password policy
+ HIBP fail-closed screening
+ Argon2id/pepper
→ Account security lock
→ assert PasswordCredential still absent
→ invalidate pending password_recovery_challenge for Account
→ INSERT PasswordCredential
→ rotate current AuthSession bearer
```

## 14.2 Remove password

```text
valid AuthSession
+ CSRF
+ recent authentication
→ Account security lock
→ anti-lockout recheck
→ invalidate pending password recovery challenge
→ DELETE PasswordCredential
→ rotate current AuthSession bearer
```

`PasswordCredential` remains the existing 0..1 table; no tombstone table is added in M5.

## 14.3 Passwordless recovery

Existing M4 `password_recovery_challenge` remains the proof table.

Reset terminal action becomes create-or-replace:

```text
strong exact EmailIdentity+Account recovery proof
→ Account security lock
→ PasswordCredential exists?
   yes → replace verifier
   no  → insert first PasswordCredential
→ conditionally consume recovery proof
→ revoke ALL AuthSessions
→ COMMIT/reconcile
→ NO auto-login
→ fresh normal signin
```

M4 anti-enumeration, supersession, exact identity binding and single-use semantics do not change.

Any normal password add/remove/change invalidates older pending recovery proof under the same Account lock.

---

# 15. Provider state machines

## 15.1 Known provider identity sign-in

```text
begin
→ transaction + nonce/state capability
→ provider proof
→ claim transaction
→ verify provider evidence/network outside DB write transaction
→ resolve active ExternalIdentity by issuer+subject
→ Account security lock
→ re-read Account active + ExternalIdentity active
→ reconcile Apple grant if Apple
→ create canonical AuthSession
→ COMMIT/reconcile
→ session cookie only after durable success
```

## 15.2 New provider identity with authoritative mailbox

```text
provider proof
→ normalize/classify exact email
→ no existing EmailIdentity collision
→ Account transaction
→ create Account
→ verified EmailIdentity
→ ExternalIdentity
→ AppleAuthGrant bind if Apple
→ Web/profile bootstrap staging when useful
→ AuthSession
→ COMMIT/reconcile
```

## 15.3 New provider identity requiring DANTE mailbox proof

```text
provider proof
→ ExternalSignupChallenge
→ user supplies mailbox if necessary
→ DANTE OTP
→ valid OTP
→ terminal new-account or collision transition
```

No Account exists before accepted mailbox proof.

## 15.4 Provider-first collision

```text
valid provider proof
+ provider email matches existing EmailIdentity
→ no Account creation
→ ExternalLinkChallenge targeted to exact Account/EmailIdentity
→ Secure HttpOnly link-flow cookie
→ user authenticates existing Account using any accepted authenticator
→ GET link state validates challenge target == current Account
→ explicit Confirm
→ Account lock + recent-auth recheck
→ issuer+subject uniqueness recheck
→ create/reactivate ExternalIdentity
→ bind AppleAuthGrant if Apple
→ consume challenge
→ rotate current AuthSession bearer
```

Before mailbox/account proof, public copy never reveals additional Account existence detail.

## 15.5 Authenticated provider link

From authenticated Security/Access settings:

```text
begin purpose=link
requires session + CSRF + recent auth
→ provider proof
→ Account lock
→ recent-auth recheck at completion
→ issuer+subject uniqueness recheck
→ create/reactivate ExternalIdentity for same Account
→ rotate session bearer
```

No `ExternalLinkChallenge` is needed because Account control already exists.

## 15.6 Provider reauthentication

```text
begin purpose=reauthenticate
requires valid session + CSRF
DOES NOT require recent auth
→ provider proof
→ exact auth_session_ref + begin-time bearer-verifier snapshot must still match
→ Account lock
→ same session remains
→ recent_auth_at refreshed
→ bearer rotated
```

This mirrors M4 password reauthentication semantics rather than creating a separate session.

---

# 16. Apple callback and notification topology

## 16.1 Web callback

Apple callback is:

```text
POST /api/v1/auth/apple/callback
Content-Type: application/x-www-form-urlencoded
```

It is the single reviewed external browser-ingress exception to normal same-origin unsafe-API CSRF handling.

Security authority is the bounded server transaction:

```text
state verifier
+ nonce
+ expected provider/client audience
+ authorization-code exchange
+ signed ID-token verification
+ session snapshot for link/reauth where applicable
```

The callback must not weaken global DANTE cookie policy.

For authenticated Apple link/reauth, the normal SameSite cookie may be absent on the cross-site POST; the transaction carries `auth_session_ref` plus exact begin-time bearer verifier snapshot. Completion rejects revoked/expired/rotated sessions.

After terminal processing Apple returns a `303 See Other` to a **fixed DANTE destination** selected only from the stored bounded `return_target_code`. Never reflect arbitrary return URLs.

## 16.2 Apple notifications

```text
POST /api/v1/auth/apple/notifications
```

No browser CSRF. Verify Apple signed payload/JWS first.

Use provider event time to apply bounded idempotent transitions.

Relevant M5 classes:

```text
email-disabled
email-enabled
consent-revoked
account-deleted
```

Rules:

```text
email disabled/enabled
→ exact bound EmailIdentity recovery restriction with event-time ordering

consent revoked/account deleted
→ Account lock where bound
→ ExternalIdentity local revoke (monotonic)
→ AppleAuthGrant revocation/reconciliation state
→ never delete DANTE Account merely because Apple Account state changed
```

Full DANTE Account deletion/privacy lifecycle remains separately governed.

---

# 17. Exact M5 public API inventory

All routes are under `/api/v1`, use explicit stable `operationId`, RFC 9457 problems, request IDs and `Cache-Control: no-store` for sensitive Auth responses.

## 17.1 Google

```text
POST /api/v1/auth/google/begin
operationId: auth_begin_google_authentication

POST /api/v1/auth/google/complete
operationId: auth_complete_google_authentication
```

`begin` body:

```text
purpose: sign_in | link | reauthenticate
```

Policy:

```text
sign_in        → anonymous allowed
link           → AuthSession + CSRF + recent auth
reauthenticate → AuthSession + CSRF; recent auth NOT required
```

Begin returns a typed transaction reference, raw in-memory transaction capability, OIDC nonce and expiry. Raw capability/nonce are never persisted in browser storage.

Complete submits the transaction reference/capability plus GIS credential. Backend verifies signature/JWK/issuer/audience/azp where required/expiry/nonce/subject.

## 17.2 Apple

```text
POST /api/v1/auth/apple/begin
operationId: auth_begin_apple_authentication

POST /api/v1/auth/apple/callback
operationId: auth_handle_apple_callback

POST /api/v1/auth/apple/notifications
operationId: auth_process_apple_notification
```

Begin body/policy uses the same purpose vocabulary as Google. Response contains the server-built Apple authorization URL and expiry, not arbitrary client-composed security parameters.

## 17.3 Provider enrollment

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

Enrollment state is authorized by the Secure HttpOnly provider-enrollment flow cookie, not localStorage/sessionStorage.

Successful verify returns either:

```text
authenticated
link_required
```

according to authoritative terminal state.

## 17.4 Provider link / methods

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

`provider-link` requires an authenticated Account after the user proves the existing Account. GET verifies challenge target Account before returning safe provider-link UI data. Confirm requires CSRF + recent auth.

`auth_get_authentication_methods` returns only safe management metadata, such as active method type, stable DANTE ref, provider hint/private-relay indicator, passkey label/created/last-used and reconciliation state. No provider tokens/subjects/public keys are exposed.

## 17.5 Password management

```text
POST /api/v1/auth/password/establish
operationId: auth_establish_password

DELETE /api/v1/auth/password
operationId: auth_remove_password
```

Both require session + CSRF + recent auth and backend anti-lockout/account-lock checks.

Existing M4 `/auth/reset-password` is adapted internally to create-or-replace PasswordCredential; its public path remains stable.

## 17.6 Passkeys

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

Reauthentication requires current session + CSRF but no initial recent-auth requirement; complete refreshes `recent_auth_at` and rotates the same session bearer.

PATCH changes the user-facing label only in M5.

---

# 18. Provider authentication success union

Google complete and server-internal Apple callback resolve to the same application outcome union:

```text
authenticated
link_required
enrollment_required
```

`authenticated` issues/rotates canonical DANTE AuthSession according to purpose.

`link_required` creates/retains provider-link flow state and never creates a duplicate Account.

`enrollment_required` creates/retains provider-enrollment flow state and never creates an Account before mailbox proof.

Frontend does not infer success from provider SDK callbacks alone.

---

# 19. Machine problem codes

M5 adds the smallest stable set needed by client behavior:

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

Existing codes remain authoritative where they already fit:

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

Provider email collision itself is **not** an error; it is a typed `link_required` outcome.

No client parses provider/backend English text.

---

# 20. Browser flow-cookie contract

M5 may use two bounded Secure HttpOnly host-only flow cookies:

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
bounded Max-Age <= backing challenge TTL
raw high-entropy continuation capability only
cleared on terminal success/cancel/invalid expiry where response control exists
never localStorage/sessionStorage
```

The ordinary `__Host-dante-session` policy is unchanged.

Google begin/complete transaction capability stays in browser memory only; Apple transports its transaction capability as provider `state`.

---

# 21. WebAuthn RP/origin contract

Production:

```text
RP ID = exact DANTE registrable application domain configured for deployment
allowed origins = explicit canonical HTTPS origins
```

No suffix/substring origin acceptance.

Local browser proof changes the M4 harness target from IP-host RP posture to:

```text
origin = https://localhost:<ephemeral-port>
RP ID  = localhost
```

or an explicitly reviewed local domain with equivalent security.

`https://127.0.0.1` is not the M5 WebAuthn RP test authority.

The exact `rp_id` and `expected_origin` are copied into each WebAuthnChallenge so a config change cannot reinterpret an already-issued ceremony.

---

# 22. Dependency qualification result

As of 2026-08-30, M5.2 approves these **families/versions as implementation candidates**, not yet as locked dependencies:

```text
fido2        2.2.1  — Yubico WebAuthn/FIDO server primitives
joserfc      1.7.4  — JOSE/JWS/JWT/JWK
cryptography 50.0.0 — AEAD / cryptographic backend
httpx2       existing governed provider HTTP boundary
```

Before the dependency write gate actually changes `pyproject.toml`/`uv.lock`, implementation must prove:

```text
Python 3.14 compatibility
current advisory status
no unsafe implicit algorithm selection
explicit JOSE algorithm allowlists
JWK parsing/key rotation vectors
WebAuthn ceremony vectors
counter policy owned by DANTE rather than hidden auto-lock behavior
no credential/token logging by dependency defaults
Ruff/mypy/test/build compatibility
uv lock determinism
```

Do not hand-roll JWT/JWS/JWK, CBOR/COSE/WebAuthn or AES-GCM.

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

Unknown `kid` may cause one bounded JWK refresh per cache coordination window, not one refresh per concurrent request.

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
raw provider state/transaction capability
raw OIDC nonce
raw passkey challenge
raw WebAuthn assertion/signature beyond protected bounded diagnostics
session/CSRF secret
OTP/recovery secret
password
```

Safe logs use DANTE refs, provider class, request ID and bounded machine failure category.

Provider email/name/avatar/locale are personal data.

Provider subject is security identity data; do not expose it to normal UI or logs merely for convenience.

---

# 25. Concurrency/race contract

Every case below must be assigned a deterministic real-PostgreSQL proof where DB state is the arbiter:

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
add password vs password recovery reset
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

## 26.1 Pure/unit

```text
provider claim normalization
issuer/audience/nonce rules
Google mailbox-authority classification
Apple event ordering decision
AEAD AAD/key-ring behavior
flow verifier hashing
anti-lockout decision function
WebAuthn option policy
signCount risk policy
problem mapping
```

## 26.2 Real PostgreSQL

```text
all M5 PK/FK/UQ/CHECK/index/ACL
EmailIdentity reachability ordering
ExternalIdentity lifetime uniqueness/revocation
flow TTL/claim/consume
pending AppleGrant lifecycle
Account lock races
provider collision/account creation races
passkey duplicate/removal/auth races
password/recovery races
```

## 26.3 FastAPI HTTP

```text
exact paths/status/media/cache-control/request-id
CSRF/session requirements by purpose
Apple form_post boundary
Apple notification boundary
RFC9457 problems
no unsafe field exposure
```

## 26.4 OpenAPI/generated client

```text
deterministic OpenAPI without live providers/secrets
generated operationIds exactly frozen
success-union schemas
RFC9457 typed problems
governed client only
no raw generated operation export to product UI
```

## 26.5 Web/browser

```text
Google/Apple buttons and cancel/error states
provider-enrollment OTP flow
provider collision → sign in → explicit link
smart bootstrap without redundant name questions
passkey registration
username-less passkey authentication
passkey reauth
flow-cookie/URL scrubbing
hard refresh remains authoritative
Chromium/Firefox/WebKit truthful capability matrix
```

## 26.6 Real providers

Before M5 production-ready closure:

```text
real Google configured client smoke/UAT
real Apple registered HTTPS Services ID/domain smoke/UAT
Apple Private Email Relay delivery configuration proof
real provider revoke/account-change path where safely testable
```

CI remains deterministic and does not depend on public providers.

---

# 27. M5-A implementation order

After this contract is committed, implementation begins in bounded slices:

```text
M5-A1  Dictionary exact objects / EmailIdentity delta
M5-A2  SQLAlchemy mappings
M5-A3  Alembic migration + least-privilege ACL
M5-A4  real PostgreSQL catalog/constraint/ACL/race acceptance

M5-B   provider/JWK/JOSE/AEAD infrastructure + dependency lock
M5-C   Google
M5-D   Apple grant/callback/notifications
M5-E   linking + authenticator management/anti-lockout
M5-F   WebAuthn/passkeys
M5-G   add/remove password + passwordless recovery adaptation
M5-H   FastAPI/OpenAPI public materialization
M5-I   governed generated client
M5-J   Access Web/smart onboarding
M5-K+  focused proof → real provider/browser UAT → docs/user acceptance
```

Do not combine the entire M5 implementation into one uncontrolled patch.

---

# 28. M5.2 closure condition

M5.2 is complete when this document and current status/handoff sources agree that:

```text
exact persistence design frozen     YES
exact API inventory frozen          YES
state/race lifecycle frozen         YES
callback/RP/origin topology frozen  YES
dependency direction qualified      YES
proof layering frozen               YES
runtime/schema materialization      NO
```

Next action is **M5-A persistence foundations**, under a new exact Git write gate.
