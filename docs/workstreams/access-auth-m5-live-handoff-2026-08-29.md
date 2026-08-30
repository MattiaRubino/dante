# DANTE — Access/Auth M5 Live Handoff — 2026-08-29

- **Status:** CURRENT CONTINUATION SAVE-GAME / M5.1 COMPLETE / M5.2 COMPLETE / M5-A NEXT
- **Vertical:** Access/Auth
- **Repository:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Worktree:** `/home/mattia/projects/dante`
- **M4 implementation checkpoint:** `c95e3b2ca664725bcacc374cb5ba6ed49409fe2b`
- **M4 documentation closure:** `a95955da72cbb9119982aa1544c2aaa356fc5e6a`
- **M5.1 architecture freeze checkpoint:** `8f993ace74d21c98d4034b0e521a1f9b458b007a`
- **M5 architecture authority:** `../architecture/access-auth-m5-contract.md`
- **M5.2 exact persistence/API authority:** `../architecture/access-auth-m5-persistence-api-contract.md`
- **Forward plan:** `access-auth-m4-m7-execution-plan.md`

> This file is the live save-game for continuation. Repository truth wins if the branch has moved after this handoff. A new chat should not replay the conversation or redo broad M5 research; it should verify current branch state, read the authorities above, and continue from M5-A.

---

# 1. Mandatory continuation

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not create another Access branch/worktree merely because the chat changed.

Do not touch without explicit topology/write gate:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

Before every remote Git write, obey `docs/development/agent-operating-manual.md`:

```text
1. fetch current branch HEAD
2. establish exact PRE-SCOPE SHA
3. list exact CREATE/UPDATE/DELETE paths
4. list exact purpose and exclusions
5. obtain explicit user approval
6. re-fetch HEAD before first write
7. post-write compare actual path/status set against gate
```

No merge/rebase/force-push/protected-main write without explicit authorization.

Recommended read order:

1. `docs/PROJECT-STATUS.md`
2. `docs/ROADMAP.md`
3. `docs/workstreams/access-auth.md`
4. **this file**
5. `docs/architecture/access-auth-m5-contract.md`
6. `docs/architecture/access-auth-m5-persistence-api-contract.md`
7. `docs/workstreams/access-auth-m4-m7-execution-plan.md`
8. `docs/architecture/access-auth-architecture.md`
9. `docs/architecture/access-auth-security-contract.md`
10. `docs/architecture/access-auth-api-contract.md`
11. `docs/architecture/access-auth-testing-contract.md`
12. `docs/decisions/ADR-011-access-auth-architecture.md`
13. `docs/database/README.md`
14. `docs/database/access-auth.md`
15. current Access/Auth Dictionary entries
16. `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
17. `docs/frontend/access.md`
18. current backend/Web implementation and tests for the M5-A slice

---

# 2. User quality bar / working style

The user requires DANTE to be built at the level expected from large mature applications such as Google, Notion, Linear, Facebook and comparable serious products.

Interpretation:

```text
production-quality architecture
security-first consumer-grade UX
high performance
strong PostgreSQL integrity
clean maintainable code
no hidden technical debt for convenience
configurable/tokenized UI rather than hardcoded one-offs
strong accessibility/responsive behavior
real boundary proof rather than mock-only confidence
no gratuitous enterprise theatre/overengineering without consumer value
```

The user does not want a yes-man. If a design is weaker than mature-product practice, identify and fix it.

Testing preference learned in M4:

```text
prove each invariant at the truthful layer
avoid rerunning heavy browser/PostgreSQL suites after every tiny edit
use focused proof during development
one heavy closeout QA when candidate is actually ready
never hide flaky Auth behind retries
```

For manual UAT, advance one action at a time.

Avoid top-level `exit` in shell snippets.

---

# 3. Closed foundation — do not reopen casually

```text
M1 — Access Visual/UX Freeze
CLOSED / ACCEPTED

M2 — Auth Architecture Freeze
CLOSED / ACCEPTED / QA PASS

M3 — Email/Password Signin + AuthSession Spine
CLOSED / ENGINEERING PASS / USER ACCEPTED

M4 — Signup + Verification + Recovery + Reset + Reauth
CLOSED / ENGINEERING PASS / USER ACCEPTED
```

Whole Access/Auth remains:

```text
ACTIVE / NOT CLOSED
```

Permanent Auth constitution:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
multiple independent AuthSessions normal
same-origin Web Auth
Secure HttpOnly host-only __Host-dante-session
session-bound CSRF + Origin + Fetch Metadata + X-Dante-Client
provider identity = issuer + subject
provider email != identity/link authority
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
method != factor != assurance
frontend/provider callback != backend-authoritative success
unknown/loading != signed-out/signed-in/error
```

Do not reintroduce:

```text
JWT/localStorage browser Auth
Redis/JWT session authority
Principal table
silent provider-email merge
provider-specific parallel Account/session authority
Account advisory-lock replacement
wide credentialed CORS
Axios just for Auth
raw fetch from Access UI
fake frontend Auth success
persisted browser Auth cache
login-first + useEffect session repair
```

---

# 4. M4 accepted baseline

Final M4 implementation checkpoint:

```text
c95e3b2ca664725bcacc374cb5ba6ed49409fe2b
fix(auth): reconcile M4 PostgreSQL acceptance
```

Current materialized DB truth remains:

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

Accepted automated proof:

```text
backend static / typing / lint / build        PASS
backend fast                                 87 / 87 PASS
real PostgreSQL marked suite                 87 / 87 PASS
Web Access UI                                22 / 22 PASS
real Auth full-stack browser                 33 / 33 PASS
Chromium / Firefox / WebKit                  11 / 11 PASS each
```

Accepted manual UAT:

```text
login/session/logout
new signup → OTP → Account/AuthSession → setup handoff
recovery → reset → fresh replacement signin
existing-account signup → OTP → safe existing_account result
```

Do not rerun M4 QA absent direct regression evidence.

---

# 5. M5 current status

```text
M5 overall                                  ACTIVE
M5.1 external-authority/benchmark freeze    COMPLETE
M5.1 architecture/security freeze           COMPLETE
M5.2 persistence/API design                 COMPLETE

M5-A persistence implementation             NEXT / NOT STARTED
M5 backend provider runtime                 NOT STARTED
M5 Database Dictionary materialization      NOT STARTED
M5 SQLAlchemy materialization               NOT STARTED
M5 Alembic migration                        NOT STARTED
M5 dependency lock                          NOT STARTED
M5 OpenAPI/client materialization           NOT STARTED
M5 Web runtime integration                  NOT STARTED
```

The design authorities are:

```text
docs/architecture/access-auth-m5-contract.md
docs/architecture/access-auth-m5-persistence-api-contract.md
```

Do not perform another broad “what should Google/Apple/passkeys do?” discovery sweep unless provider standards materially changed. M5-A starts from the frozen contract.

---

# 6. What M5 is

M5 is the **multi-authenticator Account layer**:

```text
Google authentication
+ Sign in with Apple
+ passkeys/WebAuthn
+ explicit Account linking
+ provider-enriched onboarding/bootstrap
+ passwordless Accounts
+ add/remove password capability
+ safe authenticator add/remove
+ anti-lockout
+ provider grant/revocation lifecycle
+ Apple relay/account-change lifecycle
+ passwordless recovery coherence
+ Auth vs provider-data integration isolation
+ future Home/Security-settings readiness
```

All successful methods converge on canonical DANTE `AuthSession`.

---

# 7. Provider-enriched onboarding

User requirement: take **all provider data genuinely useful to DANTE** at mature-app quality, then let DANTE own/edit the resulting profile/settings later.

Frozen rule:

```text
provider data
→ validate/classify provenance
→ eliminate redundant onboarding
→ initialize/stage useful setup/profile values
→ user later edits in DANTE
→ future provider login never silently overwrites DANTE-owned values
```

Google useful bootstrap when actually returned:

```text
email
email_verified
name
given_name
family_name
picture
locale
hosted-domain metadata
security/authentication claims where protocol actually supplies them
```

Apple useful bootstrap:

```text
email or Private Email Relay
first name on initial authorization when supplied
last name on initial authorization when supplied
private-email/reachability semantics
security/authentication claims actually supplied
```

No DANTE username is inferred.

Apple name may be one-shot. M5.2 therefore freezes bounded `account_profile_bootstrap` staging rather than losing it or dumping profile fields into Account/ExternalIdentity.

---

# 8. M5.2 exact persistence design

M5-A target:

```text
ALTER
  dante.email_identity
    + recovery_restriction_code
    + recovery_restriction_observed_at

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

Exactly 9 new tables.

No generic provider/auth token/challenge table.

**Current database is still `20260829_11`.** None of these objects exist in accepted Dictionary/SQLAlchemy/Alembic/PostgreSQL yet.

---

# 9. EmailIdentity reachability evolution

Existing `verified_at` remains historical proof that the exact mailbox was controlled.

M5 adds:

```text
recovery_restriction_code
recovery_restriction_observed_at
```

Initial restriction code:

```text
provider_delivery_disabled
```

Apple ordering:

```text
email-disabled at T
→ apply only if T is newer than current observed_at
→ code=provider_delivery_disabled
→ observed_at=T

email-enabled at T
→ apply only if T is newer
→ code=NULL
→ observed_at=T remains
```

This prevents replay/out-of-order stale provider events from overwriting newer reachability truth.

Do not reset `verified_at` when relay is disabled.

---

# 10. ExternalIdentity

Frozen columns/semantics are in the exact M5.2 contract. Key points:

```text
identity key = issuer + subject
UNIQUE(issuer,subject)
provider = google | apple
exact provider/issuer canonical pair
optional provider email display hint only
optional exact email_identity_ref bound to same Account
status = active | revoked
```

Normal unlink is **logical revoke, not DELETE**.

Reason: lifetime provider identity should not silently be recyclable onto another Account after unlink.

No `UNIQUE(account_ref, provider)` — one Account may have multiple provider identities if product needs it.

Provider email/name/avatar changes never move the identity to another Account.

---

# 11. ExternalAuthTransaction

Shared Google/Apple transaction because security lifecycle is genuinely the same.

```text
purpose = sign_in | link | reauthenticate
TTL <= 15 min
state_verifier 32 bytes UNIQUE
nonce_verifier 32 bytes UNIQUE
claimed_at single terminal claim
```

For link/reauth:

```text
auth_session_ref
+ exact begin-time auth_session_secret_verifier snapshot
```

No raw session secret is persisted.

Security policy:

```text
sign_in
→ anonymous

link
→ current AuthSession + CSRF + recent auth
→ recent auth rechecked at completion

reauthenticate
→ current AuthSession + CSRF
→ NO recent-auth requirement at begin
→ successful provider proof refreshes recent_auth_at
→ same auth_session_ref
→ bearer rotation
```

**Do not accidentally require recent auth to start reauthentication.** That would make reauth impossible exactly when freshness has expired.

Apple transaction is claimed before single-use authorization-code exchange. Ambiguous exchange is not retried.

---

# 12. AppleAuthGrant — important M5.2 refinement

M5.2 discovered that putting the Apple refresh token only in link/signup challenge state is insufficient: an authorization can succeed and then the user can abandon DANTE before Account/link finalization. DANTE still needs to revoke that Apple grant safely.

Therefore dedicated lifecycle:

```text
apple_auth_grant
status:
  pending
  active
  revocation_pending
  revoked
```

Pending may be unbound to ExternalIdentity.

Encrypted refresh token:

```text
application-layer AEAD
baseline AES-256-GCM
12-byte nonce
key id/version
key outside PostgreSQL/Git
stable AAD binds grant ref + issuer + subject + client_id
```

Lifecycle:

```text
Apple code exchange succeeds
→ pending grant persisted

DANTE Account/link succeeds
→ bind external_identity_ref
→ active

user unlink / provider revoke
→ revoke ExternalIdentity locally first
→ grant revocation_pending
→ commit
→ remote Apple revoke OUTSIDE DB tx
→ confirmed → revoked + encrypted secret cleared

abandoned pending grant expires
→ revocation_pending
→ bounded reconciliation
→ remote revoke
→ revoked + secret cleared
```

Provider outage must never keep Apple Auth locally enabled.

---

# 13. Provider-first collision / linking

No silent email merge.

Provider-first collision:

```text
verified provider proof
+ email matches existing EmailIdentity
→ DO NOT create Account
→ ExternalLinkChallenge targeted to exact Account/EmailIdentity
→ raw continuation only in Secure HttpOnly provider-link flow cookie
→ user proves exact DANTE Account with any accepted authenticator
→ explicit confirmation
→ session + recent auth
→ Account security lock
→ final issuer+subject uniqueness check
→ create/reactivate ExternalIdentity
→ bind Apple grant if needed
→ consume challenge
→ rotate current session bearer
```

Authenticated Settings linking does not need `ExternalLinkChallenge`; the existing session/Account already provides the target context.

---

# 14. Provider enrollment

`external_signup_challenge` handles provider identity that is valid but still needs DANTE mailbox proof.

Main expected case:

```text
Google Account backed by third-party mailbox
→ provider identity proof valid
→ DANTE still requires current mailbox proof for recovery invariant
```

State includes provider identity evidence, optional Apple pending grant ref, flow verifier, mailbox/OTP state, one-shot bootstrap fields, TTL.

TTL:

```text
challenge <= 30 min
OTP <= 15 min
failed verification <= 5
```

Enrollment OTP is purpose/domain-separated from M4 password signup OTP.

Valid terminal OTP:

```text
email still unowned
→ Account + verified EmailIdentity + ExternalIdentity + AuthSession + profile bootstrap

email now owned because of race
→ no duplicate Account
→ convert verified provider evidence into ExternalLinkChallenge
```

DB uniqueness remains final race arbiter.

---

# 15. AccountProfileBootstrap

Non-canonical one-shot staging:

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

No update lifecycle.

```text
first provider Account creation → optional INSERT
canonical profile/setup consumes → DELETE
later provider login → never refresh/overwrite
expiry → DELETE
```

`picture_url` is not permission for unrestricted server-side fetching; future avatar import uses governed Asset/media pipeline.

---

# 16. WebAuthn/passkeys exact design

`webauthn_account`:

```text
account_ref PK/FK
user_handle random immutable 32 bytes UNIQUE
```

Never use AccountRef/UUIDv7 as WebAuthn `user.id`.

`passkey_credential`:

```text
passkey_credential_ref UUIDv7
account_ref
credential_id UNIQUE bytea 1..1023
credential_public_key bounded bytea
cose_algorithm
sign_count uint32 semantics
backup_eligible
backup_state
transports text[] bounded
label
status active/revoked
created/updated/last_used/revoked metadata
```

No AAGUID/device fingerprint in M5 without a real consumer.

Do not DB-enumerate transport strings; preserve future standardized values after bounded validation.

Passkey remove = logical revoke, not DELETE.

Counter:

```text
verified assertion + larger counter → advance stored counter
verified assertion + zero/non-increasing counter → do not lower counter
→ risk signal
→ NOT automatic Account lock
```

`webauthn_challenge` ceremonies:

```text
registration
authentication
reauthentication
```

TTL <= 5 min, verifier 32 bytes unique, exact RP ID + expected origin copied into challenge, conditional single claim.

Anonymous authentication has no pre-bound Account/session and uses discoverable credential + returned userHandle.

Registration and passkey mutation require recent auth.

Passkey reauthentication requires a valid session + CSRF but **does not require recent auth before proof**; success refreshes same session and rotates bearer.

---

# 17. Anti-lockout / password lifecycle

Active direct authenticators:

```text
PasswordCredential present
active ExternalIdentity count
active PasskeyCredential count
```

Normal authenticator removal must leave at least one direct authenticator.

Passwordless Account must additionally retain at least one verified recovery-eligible EmailIdentity.

UI checks are advisory; backend Account-lock transaction is authority.

Add password:

```text
session + CSRF + recent auth
+ password policy
+ HIBP fail-closed
+ Argon2id/pepper
→ Account lock
→ assert still absent
→ invalidate old password-recovery proof
→ INSERT PasswordCredential
→ rotate current bearer
```

Remove password:

```text
session + CSRF + recent auth
→ Account lock
→ anti-lockout recheck
→ invalidate old recovery proof
→ DELETE PasswordCredential
→ rotate current bearer
```

Passwordless recovery adapts M4:

```text
strong exact EmailIdentity+Account proof
→ Account lock
→ PasswordCredential exists? replace
→ absent? create first
→ conditionally consume proof
→ revoke ALL AuthSessions
→ NO auto-login
→ fresh signin
```

M4 anti-enumeration/supersession/exact binding/single-use remain.

---

# 18. Exact M5 API inventory

```text
POST /api/v1/auth/google/begin
  auth_begin_google_authentication
POST /api/v1/auth/google/complete
  auth_complete_google_authentication

POST /api/v1/auth/apple/begin
  auth_begin_apple_authentication
POST /api/v1/auth/apple/callback
  auth_handle_apple_callback
POST /api/v1/auth/apple/notifications
  auth_process_apple_notification

GET /api/v1/auth/provider-enrollment
  auth_get_provider_enrollment
POST /api/v1/auth/provider-enrollment/email
  auth_set_provider_enrollment_email
POST /api/v1/auth/provider-enrollment/verify
  auth_verify_provider_enrollment
POST /api/v1/auth/provider-enrollment/resend
  auth_resend_provider_enrollment_verification

GET /api/v1/auth/provider-link
  auth_get_provider_link
POST /api/v1/auth/provider-link/confirm
  auth_confirm_provider_link

GET /api/v1/auth/methods
  auth_get_authentication_methods
DELETE /api/v1/auth/providers/{external_identity_ref}
  auth_unlink_provider

POST /api/v1/auth/password/establish
  auth_establish_password
DELETE /api/v1/auth/password
  auth_remove_password

POST /api/v1/auth/passkeys/registration/begin
  auth_begin_passkey_registration
POST /api/v1/auth/passkeys/registration/complete
  auth_complete_passkey_registration
POST /api/v1/auth/passkeys/authentication/begin
  auth_begin_passkey_authentication
POST /api/v1/auth/passkeys/authentication/complete
  auth_complete_passkey_authentication
POST /api/v1/auth/passkeys/reauthentication/begin
  auth_begin_passkey_reauthentication
POST /api/v1/auth/passkeys/reauthentication/complete
  auth_complete_passkey_reauthentication
PATCH /api/v1/auth/passkeys/{passkey_credential_ref}
  auth_update_passkey
DELETE /api/v1/auth/passkeys/{passkey_credential_ref}
  auth_remove_passkey
```

Google/Apple application outcome union:

```text
authenticated
link_required
enrollment_required
```

Collision is not an error.

All sensitive Auth responses remain no-store/RFC9457/request-id governed.

---

# 19. M5 machine problem codes

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

Reuse existing generic Auth/CSRF/conflict/validation/service codes where semantically correct. Never branch client behavior on English text.

---

# 20. Flow cookies / callback topology

Potential M5 bounded flow cookies:

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
raw high-entropy continuation only
no localStorage/sessionStorage
```

Ordinary `__Host-dante-session` policy remains unchanged.

Google transaction raw capability lives only in browser memory until complete.

Apple uses provider `state` and `form_post` callback.

Apple callback:

```text
POST /api/v1/auth/apple/callback
Content-Type application/x-www-form-urlencoded
```

It is the one reviewed cross-site provider protocol boundary. It does not weaken ordinary DANTE same-origin mutation CSRF rules.

Callback returns `303` only to fixed DANTE destinations derived from stored bounded enum; no open redirect.

---

# 21. Apple notification semantics

Signed/JWS verification first.

Relevant M5 classes:

```text
email-disabled
email-enabled
consent-revoked
account-deleted
```

Reachability updates use provider event timestamp ordering.

Consent/account deletion:

```text
locally revoke ExternalIdentity
reconcile AppleAuthGrant
never auto-delete DANTE Account merely from Apple state
```

Full DANTE deletion/privacy lifecycle remains separately governed.

---

# 22. WebAuthn deployment topology

Current M4 browser harness uses IP host. That is not M5 WebAuthn RP authority.

M5 target:

```text
origin = https://localhost:<ephemeral-port>
RP ID  = localhost
```

Production RP ID/origins are exact configured HTTPS values; never suffix/substring matching.

Real Apple Web proof requires registered HTTPS Services ID/domain. Real Google/Apple provider smoke/UAT is mandatory before M5 closure. CI must remain deterministic without public-provider dependency.

---

# 23. Dependency direction

As of 2026-08-30 qualified **candidate** baselines:

```text
fido2        2.2.1
joserfc      1.7.4
cryptography 50.0.0
httpx2       already present
```

They are NOT yet added to `pyproject.toml`/`uv.lock`.

Before M5-B admission prove:

```text
Python 3.14 compatibility
current advisories
explicit JOSE algorithm allowlists
JWK/key-rotation vectors
WebAuthn ceremony vectors
DANTE-owned signCount risk policy
no dangerous library logging
Ruff/mypy/test/build
uv lock determinism
```

Do not hand-roll JOSE, CBOR/COSE/WebAuthn or AEAD.

---

# 24. M5 concurrency/race classes

Must prove at the truthful layer:

```text
two first provider signins for same issuer+subject
provider identity linked to two Accounts concurrently
provider signin vs Account disable
provider signin vs ExternalIdentity revoke
provider link vs provider revoke
Apple notification vs signin/link
pending Apple grant expiry vs link completion
provider enrollment verify vs competing Account/email creation
passkey duplicate registration
passkey auth vs passkey removal
add password vs recovery reset
remove password vs pending recovery
concurrent authenticator removals
reauth vs concurrent bearer rotation
```

Rules:

```text
Account-wide mutation → Account security lock
provider uniqueness → UNIQUE(issuer,subject)
passkey uniqueness → UNIQUE(credential_id)
flow replay → conditional claim/consume
provider/network outside DB transaction
no blanket SERIALIZABLE
no blind mutation retry
```

---

# 25. Proof matrix

```text
UNIT/PURE
provider normalization, mailbox authority, event ordering, AEAD AAD,
anti-lockout, WebAuthn options/counter policy, problem mapping

REAL POSTGRESQL
Dictionary/catalog/PK/FK/UQ/CHECK/index/ACL,
flow claim/TTL, AppleGrant lifecycle, Account-lock races,
provider/passkey/password races

FASTAPI HTTP
exact path/status/media/cache/request-id/CSRF,
Apple form_post + notifications, RFC9457

OPENAPI / GENERATED CLIENT
deterministic schema, exact operationIds, typed unions/problems,
governed client boundary

WEB / BROWSER
provider UI/cancel/error, enrollment, collision/link,
smart onboarding, passkeys, reauth, flow-cookie/URL hygiene,
hard-refresh regression, Chromium/Firefox/WebKit

REAL PROVIDERS
Google configured client smoke/UAT,
Apple registered-domain UAT,
Private Email Relay delivery config,
provider revoke/account-change proof where safely testable
```

Do not duplicate DB race proof across every browser.

---

# 26. Exact next step — M5-A

```text
M5-A — persistence foundations
NEXT / NOT STARTED
```

Recommended order:

```text
M5-A1  Dictionary
  → update email_identity entry
  → create 9 table entries

M5-A2  SQLAlchemy
  → exact mappings only

M5-A3  Alembic
  → one canonical revision after 20260829_11
  → exact constraints/indexes
  → default-deny/narrow runtime ACL
  → exact downgrade

M5-A4  proof
  → Dictionary validator/parity
  → migration DAG/head
  → real PostgreSQL catalog
  → ACL exactness
  → negative constraints
  → persistence-level synchronization races
```

Do NOT add provider adapters/dependencies/frontend/OpenAPI merely because they are downstream M5 consumers unless a future exact gate explicitly includes them.

A fresh Git write gate is required for M5-A.

---

# 27. M6 / M7 boundary

```text
M6 — Native Mobile Access
PLANNED

M7 — final whole-vertical Security Hardening + Observability + Authenticated Handoff
PLANNED
```

M7 owns complete long-lived user-facing session/device/security-management, new-login alerts/“this wasn’t me”, final security-event/observability posture, privacy/legal/accessibility/dependency/release review and final whole-vertical manual acceptance.

M7 is not permission to defer correctness-critical M5 provider/passkey/link/recovery behavior.

---

# 28. Current truth summary

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED

M5 ACTIVE
  M5.1 COMPLETE
  M5.2 COMPLETE
  M5-A NEXT / NOT STARTED

M6 PLANNED
M7 PLANNED / FINAL GATE

Whole Access/Auth vertical
ACTIVE / NOT CLOSED
```

The first thing a new chat should do after verifying branch HEAD is prepare the **M5-A exact write gate**, not restart Google/Apple/passkey discovery.
