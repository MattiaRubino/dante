# DANTE — Access/Auth M5 Contract

- **Status:** CURRENT / BRANCH-LOCAL AUTHORITATIVE FOR M5 / M5.1 ARCHITECTURE + EXTERNAL-AUTHORITY FREEZE COMPLETE
- **Vertical:** Access/Auth
- **Branch:** `feature/access-auth`
- **Prerequisite:** M1–M4 CLOSED; M4 ENGINEERING PASS; M4 MANUAL UAT PASS; USER ACCEPTED
- **M5 runtime implementation:** NOT STARTED at this contract checkpoint
- **M5 persistence/OpenAPI/Web materialization:** NOT STARTED at this contract checkpoint
- **Next step:** M5.2 — exact persistence + API design under CP6 and existing Access/Auth contracts
- **Companion authorities:** `access-auth-architecture.md`, `access-auth-security-contract.md`, `access-auth-api-contract.md`, `access-auth-testing-contract.md`, ADR-011, Database System of Record and CP6 persistence constitution

This contract freezes the product/security semantics required before materializing Google authentication, Sign in with Apple, passkeys/WebAuthn, explicit account linking, provider-enriched onboarding and multi-authenticator account management.

It does **not** authorize speculative schema/code outside a separately approved implementation gate. Exact SQL names, columns, endpoint paths and dependency pins are decided in M5.2+ only after this semantic contract is applied to current repository truth.

---

## 1. M5 objective

M5 turns DANTE Account authentication from a password-capable system into a production-grade multi-authenticator system without creating parallel account/session authorities.

Target conceptual shape:

```text
Account
├── 1..N verified recovery/contact EmailIdentity over lifecycle
├── 0..1 PasswordCredential
├── 0..N ExternalIdentity
│   ├── Google issuer + subject
│   └── Apple issuer + subject
├── 0..N PasskeyCredential
└── 0..N AuthSession
```

The quality target is the account/authentication standard expected from mature products such as Linear, Notion, GitHub, Figma, Slack and Todoist where materially comparable, while DANTE keeps the stricter security boundaries already accepted in M2–M4.

M5 is not “add social-login buttons”. It must close the provider/passkey identity lifecycle under the same production-quality standards already used for password Auth.

---

## 2. Frozen invariants

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
ExternalIdentity != provider email
provider identity key = issuer + subject
provider email coincidence != Account ownership proof
provider authentication != provider-data integration authorization
provider token/assertion != DANTE AuthSession
PasswordCredential remains optional
passwordless Account remains valid
PasskeyCredential is an authenticator, not an Account
method != factor != assurance
provider/profile data != permanent provider ownership of DANTE profile
frontend request/provider callback != backend-authoritative Auth success
```

Successful Google, Apple or passkey authentication ends in the **same canonical DANTE AuthSession lifecycle** already proven in M3/M4.

Rejected:

```text
JWT/localStorage browser Auth
provider token as DANTE session
provider email auto-link
email-as-federated-identity key
provider-specific Account rows
one Account per login method
one permanent passkey only
passkey == MFA unconditionally
generic auth_token/proof god-table
provider profile fields stuffed into Account
Google/Apple Auth scopes reused as Calendar/Gmail/iCloud integration grant
silent provider overwrite of later user-owned profile values
```

---

## 3. Provider-enriched first-account bootstrap

Provider authentication may supply useful bootstrap data. DANTE should use that data to remove redundant onboarding, but only with explicit trust/provenance semantics.

Conceptual provider evidence may expose, when actually returned and validated:

```text
provider
issuer
subject
email?
email_verified / provider email authority classification
display_name?
given_name?
family_name?
picture_url?
locale?
provider-specific non-authoritative metadata?
authentication time / assurance properties where actually available
```

The data path is deliberately split:

```text
VERIFIED SECURITY EVIDENCE
→ ExternalIdentity / EmailIdentity / AuthSession decisions

PROFILE BOOTSTRAP EVIDENCE
→ name/avatar/locale/setup suggestions
→ downstream profile/settings owner
```

Rules:

```text
provider profile = bootstrap source
provider profile != continuous DANTE profile sync

first account creation
→ initialize/pre-fill useful product state where semantically valid

later user edit in DANTE
→ DANTE value wins
→ later provider login MUST NOT silently overwrite it
```

DANTE must track or preserve enough provenance to distinguish at least:

```text
user entered
Google supplied
Apple supplied
browser inferred
DANTE default
```

No new canonical “username” is invented in M5. Google/Apple names are profile/display inputs, not a DANTE globally unique username contract.

### 3.1 One-shot provider data must not be lost

Apple may supply name fields only during the first authorization. M5 therefore requires a durable handoff/staging mechanism for useful one-shot bootstrap data when the canonical downstream profile/settings owner is not yet materialized.

That staging mechanism:

```text
must preserve provenance
must be bounded to onboarding/bootstrap purpose
must not turn Account or ExternalIdentity into a profile table
must be consumable/reconcilable by the future canonical profile/settings owner
must not silently overwrite later user-owned state
```

M5.2 must inspect current Domain/Logical/Physical ownership before choosing the exact persistence shape.

### 3.2 Avatar

A provider `picture` URL is a bootstrap source, not automatically a canonical DANTE Asset.

Until the proper DANTE Asset/profile owner is materialized:

```text
provider picture may be offered/displayed as a suggestion
arbitrary remote URL must not become an unrestricted server-side fetch primitive
accepted avatar import later goes through the governed Asset/media path
```

### 3.3 Locale

Bootstrap precedence direction:

```text
explicit DANTE user choice
> previously persisted DANTE preference
> provider locale when present/useful
> browser locale
> DANTE fallback
```

A later provider login never reverses an explicit DANTE locale choice.

---

## 4. Google authentication contract

### 4.1 Product/protocol direction

Use current Google Identity Services for Web. Prefer explicit user-initiated Google sign-in rather than introducing One Tap/automatic account selection as an M5 prerequisite.

Initial product posture:

```text
official Google button/branding
explicit user action
auto-select off by default
FedCM-compatible current GIS behavior where supported
One Tap = future UX enhancement only if evidence justifies it
```

M5 Auth does not request Gmail/Calendar/Drive scopes.

### 4.2 Identity authority

Canonical Google external identity:

```text
issuer + sub
```

Never use:

```text
email as Google identity key
name as identity
picture as identity
hosted-domain claim as authorization
```

### 4.3 ID-token verification

DANTE verifies current Google protocol evidence server-side, including as applicable:

```text
signature against current Google JWKs
allowed algorithm
issuer
audience
azp where protocol requires it
expiry / not-before semantics where present
server-issued nonce
subject
required claim shape
```

Provider key handling:

```text
bounded JWK cache
respect provider/cache lifetime where practical
unknown kid may trigger one bounded refresh
no unbounded refresh storm
unverifiable token fails closed
provider/JWK network work outside DB transaction
```

### 4.4 Google email authority

Email is metadata/evidence, never the federated key.

DANTE distinguishes Google’s authority over the mailbox:

```text
Gmail account with verified Google claim
→ Google can be accepted as mailbox authority for that exact address

Google Workspace account with verified claim + hosted-domain context
→ Google can be accepted as mailbox authority for that hosted account

Google Account using a third-party mailbox
→ verified Google-account email alone is not assumed to prove current mailbox control forever
→ DANTE mailbox verification is required when the DANTE EmailIdentity/recovery invariant needs current mailbox proof
```

If email is absent or insufficiently authoritative for creation, DANTE may continue through a purpose-specific pending enrollment + DANTE mailbox-verification path. No canonical Account is created before the accepted proof set is satisfied.

### 4.5 Google profile bootstrap

When present and useful:

```text
name
given_name
family_name
picture
locale
email
email_verified
hosted-domain metadata
```

may feed first-account bootstrap according to Section 3.

Hosted-domain metadata is never organization membership or authorization authority by itself.

---

## 5. Sign in with Apple contract

### 5.1 Web flow

Use the current server-backed Sign in with Apple Web authorization flow.

Canonical direction:

```text
DANTE begins Apple transaction
→ high-entropy state + nonce + bounded transaction record
→ Apple authorization
→ provider-defined callback/form_post
→ DANTE validates state and exchanges authorization code server-side
→ verify Apple identity token
→ resolve issuer + subject
→ DANTE account/link/session decision
```

The normal DANTE session cookie is not weakened globally to accommodate a provider callback.

Provider-defined callback HTTP method/content-type is allowed under the API contract; it is immediately translated into a DANTE application/security intent.

### 5.2 Apple token validation

Validate at least:

```text
signature against current Apple public keys
allowed algorithm
issuer
audience
expiry
nonce
subject
required claim shape
```

Authorization code exchange and JWK fetch use bounded timeouts and occur outside authoritative DB transactions.

No blind replay of a single-use code after an ambiguous provider exchange. If the provider outcome cannot be safely determined, restart the bounded provider transaction instead of guessing.

### 5.3 Apple email and Hide My Email

A verified Apple email claim may establish the exact EmailIdentity supplied by Apple, including a Private Email Relay address.

```text
user chooses Hide My Email
→ relay address is a valid DANTE EmailIdentity/recovery/contact address
→ DANTE MUST NOT demand the hidden real address merely for convenience
```

Production delivery to Apple relay addresses requires the Apple Private Email Relay configuration and authenticated sender posture, including registered sender domains/addresses and SPF/DKIM as required by Apple.

Email-relay lifecycle changes must affect recovery/contact eligibility truthfully. A disabled relay must not remain silently treated as a known-deliverable recovery channel.

Exact EmailIdentity state/persistence implications are decided in M5.2 after current owner constraints are reviewed.

### 5.4 Apple name semantics

Requested bootstrap scope is minimized to data actually useful to DANTE, primarily name/email.

Apple first/last name supplied through the first authorization browser payload:

```text
is useful profile bootstrap
may be available only once
must be validated/sanitized as user-supplied profile data
must not be treated as a cryptographically signed identity claim
must not be lost before downstream setup/profile ownership can consume it
```

### 5.5 Apple grant lifecycle

Apple Auth has a real server-side grant lifecycle.

M5 must support the provider requirements necessary for production account creation and revocation, including:

```text
secure authorization-code validation
secure handling of returned token material
retention of the minimum provider token/grant material actually required for validation/revocation/lifecycle
server-side revocation when DANTE/provider association is removed or account deletion requires it
provider key rotation
server-to-server account-change notifications
```

Any retained Apple refresh/access token is security-sensitive application data:

```text
never raw in logs/errors/client storage
not stored as plaintext convenience data
application-layer authenticated encryption / secret-key versioning required
runtime encryption key remains outside PostgreSQL/Git
rotation/revocation path required
```

Exact token-retention set and refresh-validation schedule are rechecked against current Apple requirements at adapter implementation time and encoded in M5.2/M5 implementation tests.

### 5.6 Apple server-to-server notifications

Production Apple configuration must register and handle the required server-to-server notification boundary.

DANTE must verify notification signatures and idempotently reconcile relevant classes such as:

```text
email forwarding preference changes
consent/credential revocation
app-account deletion notifications
permanent Apple Account deletion notifications
```

These notifications do not automatically collapse DANTE Account lifecycle into Apple lifecycle. They update/revoke the Apple identity/grant and associated provider-derived reachability state according to DANTE privacy/account rules.

Full whole-product deletion/retention policy remains a later privacy/account-lifecycle authority; M5 must not ignore provider revocation/deletion evidence.

### 5.7 Apple future transfer compatibility

Do not select an identity schema that assumes Apple subjects can never require provider-supported migration/app-transfer mapping. `issuer + subject` remains current identity; future transfer identifiers can be handled through a bounded migration mechanism without rewriting Account identity.

---

## 6. ExternalIdentity contract

`ExternalIdentity` is a durable security identity binding, not a provider profile dump.

Required semantic properties:

```text
stable DANTE-owned external_identity_ref
owning account_ref
provider/issuer identity
subject
created/linked lifecycle evidence
provider identity uniqueness
```

Global invariant:

```text
UNIQUE(issuer, subject)
```

The same provider identity can never belong to two Accounts.

Do **not** impose an artificial `UNIQUE(account_ref, provider)` unless product evidence proves DANTE must prohibit multiple Google/Apple identities on one Account. Architecture remains capable of multiple ExternalIdentity bindings per provider.

Provider email/name/avatar/locale are not canonical identity columns merely because they arrive during login.

---

## 7. Provider account creation

New provider identity with no existing binding follows a proof-driven path.

Conceptually:

```text
verify provider protocol
→ classify provider email authority / collect required recovery EmailIdentity proof
→ check canonical EmailIdentity collision
→ if safe new-account path:
     BEGIN
     create Account
     create verified EmailIdentity
     create ExternalIdentity
     create canonical AuthSession
     persist/stage one-shot useful profile bootstrap where required
     COMMIT/reconcile
     issue session only after authoritative success
```

No DANTE Account exists before the accepted identity/recovery proof set is complete.

If provider proof contains no usable email, DANTE requests and verifies a DANTE recovery/contact email before canonical account creation rather than weakening the standard consumer recovery invariant.

---

## 8. Existing identity signin

Known `(issuer, subject)`:

```text
verify provider evidence
→ resolve ExternalIdentity
→ resolve owning Account
→ require Account allowed
→ create fresh canonical AuthSession
→ issue normal Web session cookie after durable/reconciled commit
```

Provider email/name changes do not change Account binding.

A later provider profile change may be surfaced as a suggestion where useful, but cannot silently overwrite DANTE-owned profile/settings state.

---

## 9. Explicit Account linking

### 9.1 No silent email merge

```text
unbound Google/Apple identity
+ email matching existing DANTE EmailIdentity
!= automatic link
```

Email coincidence is a collision/signal only.

### 9.2 Required linking proof

Linking requires:

```text
valid fresh provider proof
+ control of the existing DANTE Account
+ appropriate recent authentication
+ explicit user link decision/consent
+ Account security serialization
+ final issuer+subject uniqueness recheck
+ atomic link
```

The existing Account can be proved with any allowed authenticator capable of satisfying the current recent-auth policy; code must not assume a password exists.

### 9.3 Provider-first collision UX

When an unbound provider identity collides with an existing DANTE email:

```text
provider proof
→ do not create duplicate Account
→ enter ACCOUNT_LINK / link-required flow
→ user proves existing DANTE Account
→ explicit confirmation
→ backend-authoritative link
```

Public copy must not expose more existing-account information than the proof context justifies.

### 9.4 Linking transaction

Security-sensitive linking uses the accepted Account serialization point.

Conceptual order:

```text
provider verification outside DB tx
→ authenticated/recent-auth DANTE Account proof
→ BEGIN
→ Account security lock
→ re-read Account/authenticator/provider transaction
→ recheck UNIQUE(issuer, subject)
→ insert ExternalIdentity
→ consume link transaction/proof
→ rotate initiating AuthSession bearer when retaining same session is appropriate
→ COMMIT/reconcile
```

Two concurrent links cannot bind one provider identity to two Accounts. Database uniqueness is the final race arbiter.

---

## 10. Provider transaction/challenge posture

Provider callback/login/link state is purpose-specific, bounded and server-authoritative.

Required properties:

```text
CSPRNG transaction identity / state / nonce as applicable
short TTL
single terminal consume
provider binding
purpose binding: signin vs create/link
safe intended-return identity, never arbitrary open redirect
no provider code/token/assertion in logs
replay rejection
bounded cleanup
```

For authenticated linking, the provider transaction is bound server-side to the initiating Account/AuthSession/recent-auth context. External callbacks must not depend on weakening the main DANTE session cookie.

For Apple `form_post`, a cross-site POST callback is an explicitly reviewed protocol exception to ordinary same-origin browser mutation ingress; state/nonce/transaction proof replaces normal application CSRF for that provider protocol endpoint only. The normal session cookie and ordinary unsafe DANTE API CSRF contract remain unchanged.

---

## 11. Passkey / WebAuthn contract

M5 implements real WebAuthn/passkeys, not a custom challenge/signature protocol.

### 11.1 Account capability

```text
Account → 0..N PasskeyCredential
```

Support:

```text
multiple credentials
synced passkeys
device-bound passkeys
password-manager passkeys
hardware security keys
cross-device/hybrid flows where platform/browser supports them
passwordless Accounts
username-less/discoverable signin
```

### 11.2 Registration ceremony

Registration requires an authenticated Account and appropriate recent authentication.

Baseline policy:

```text
challenge = >= 32-byte CSPRNG direction
bounded expiry
single-use/replay protected
residentKey = required
userVerification = required
user presence required by WebAuthn ceremony
attestation = none / privacy-minimizing consumer default
exact RP ID
exact allowed origin
exclude existing credentials where appropriate
```

DANTE does not store biometric templates, face/fingerprint data or device PINs.

### 11.3 Opaque WebAuthn user handle

Do not use `account_ref` directly as WebAuthn `user.id`.

M5 requires one stable opaque random WebAuthn user handle per Account, target direction 256 random bits and within WebAuthn user-handle size limits.

Reasons:

```text
avoid exposing DANTE AccountRef/UUIDv7 timestamp metadata to authenticators/passkey sync systems
preserve protocol-specific opaque identifier semantics
support username-less credential resolution cleanly
```

Exact persistence ownership is decided in M5.2.

### 11.4 Authentication ceremony

Default passkey signin is discoverable/username-less:

```text
user chooses “Use a passkey”
→ DANTE issues authentication options/challenge
→ allowCredentials absent/empty for discoverable selection
→ authenticator returns credential + userHandle + assertion
→ server verifies ceremony
→ resolve exact Account/PasskeyCredential
→ create fresh DANTE AuthSession
```

Verification includes at least:

```text
challenge
origin
RP ID / rpIdHash
credential identity
userHandle/account binding
clientData type
signature
user-presence/user-verification flags
credential public key / algorithm
replay state
```

### 11.5 Credential metadata

Persist only metadata with a concrete security/product purpose, expected to include concepts such as:

```text
credential identifier
public credential key material / algorithm representation
owning Account/WebAuthn user handle binding
creation time
last-used time when justified
signature counter
backup eligibility/state when available
transport hints when useful
user-facing credential label when product supports management
```

No invasive device fingerprinting.

### 11.6 Signature counter

Counter anomalies are security/risk evidence, not unconditional Account lockout.

```text
non-increasing/zero counter
→ evaluate according to WebAuthn/passkey semantics and synced-authenticator reality
→ security signal/event where appropriate
→ do not invent a blanket “counter mismatch = disable account” rule
```

### 11.7 WebAuthn Level 3 progressive enhancement

Modern L3 capabilities such as conditional mediation and credential-maintenance signal APIs may be used when supported.

They are progressive enhancement:

```text
normal explicit “Use a passkey” flow MUST remain functional without them
unsupported browser capability MUST NOT make account inaccessible
```

---

## 12. Authenticator management and anti-lockout

M5 establishes the multi-authenticator lifecycle even if the full long-lived management UI is placed later in authenticated Home/Settings.

Conceptual management capabilities:

```text
link Google identity
unlink Google identity
link Apple identity
unlink Apple identity
add passkey
remove passkey
add password to provider/passkey-only Account
safe password removal when another access path exists and policy permits
```

Every security-sensitive authenticator addition/removal requires appropriate current session + recent authentication + backend-authoritative confirmation.

### 12.1 Anti-lockout invariant

After an authenticator removal, DANTE must not leave an Account with no viable authentication/recovery path unless a separately explicit destructive-account flow authorizes that terminal outcome.

Before removal, evaluate:

```text
remaining authenticators
verified/reachable recovery EmailIdentity
current Account availability
provider grant/relay state where relevant
```

No UI-only check is sufficient; backend transaction rechecks the invariant.

### 12.2 Security event/notification readiness

M5 application behavior must emit/offer event capability for at least:

```text
provider linked
provider unlinked/provider consent revoked
passkey added
passkey removed
password added/removed
provider signin
Apple relay/reachability change
suspicious WebAuthn counter signal where applicable
```

Final durable security-event retention, dashboards and complete user-facing “this wasn’t me” response remain M7 unless required earlier for correctness.

---

## 13. Add-password and passwordless recovery posture

Provider/passkey-created Accounts may legitimately have no PasswordCredential.

### 13.1 Add password

Authenticated Account may establish its first PasswordCredential through a security-sensitive intent:

```text
valid AuthSession
+ recent authentication using an existing valid method
+ normal DANTE password policy
+ HIBP fail-closed establishment screening
+ Argon2id/pepper policy
+ Account security lock/recheck
+ insert PasswordCredential only if still absent
+ security event
+ session-secret rotation when current security context is retained
```

No second password system is introduced.

### 13.2 Lost-all-passkeys/provider recovery

M5 may not create a passwordless Account that becomes unrecoverable merely because all passkeys/providers are lost.

The accepted recovery/contact EmailIdentity invariant remains the fallback authority.

Minimum recovery direction for an Account with no current password:

```text
strong existing email-recovery proof
→ establish a new PasswordCredential under the same HIBP/Argon2 policy
→ revoke all existing AuthSessions as compromise-safe recovery behavior
→ fresh normal signin required
```

M5.2 must reconcile this create-or-replace credential behavior with the existing M4 recovery API/persistence without weakening M4 anti-enumeration, proof binding, single-use or no-auto-login semantics.

A future recovery flow that directly enrolls a new passkey may be added only with equally strong explicit proof; M5 does not need to invent a weaker recovery-session shortcut.

---

## 14. Auth vs provider-data integration isolation

This boundary is permanent:

```text
“Continue with Google”
!= “Connect Google Calendar/Gmail”

“Continue with Apple”
!= “Connect iCloud/Calendar”
```

Separate concerns include:

```text
client/application configuration where provider lifecycle requires isolation
consent surface
authorization scopes
token storage
refresh/revocation lifecycle
security events
user-facing connected-app management
```

M5 Auth requests only identity scopes required for authentication/bootstrap.

Future provider-data integrations must not accidentally inherit/revoke Auth grants, and Auth disconnect/revocation must not silently destroy unrelated data-integration authorization. The exact Google/Apple provider configuration isolation mechanism is verified against the concrete provider setup at implementation time rather than assumed from memory.

---

## 15. Transaction, concurrency and network ordering

Existing M3/M4 transaction doctrine remains binding.

```text
provider network/JWK/code exchange outside DB transaction
WebAuthn client ceremony outside DB transaction
cryptographic verification outside Account lock where safe
short authoritative write transaction
Account security lock for Account-wide authenticator mutation
READ COMMITTED + targeted serialization
no blanket SERIALIZABLE
no blind mutation retry
```

Required race classes include:

```text
two concurrent first signins for same unbound provider identity
provider linking to two Accounts concurrently
link vs unlink/revoke
passkey register duplicate/race
passkey remove vs authentication
add-password vs recovery/reset
provider signin vs Account disable
provider signin vs ExternalIdentity unlink
Apple notification vs active signin/link
```

Safe ordering must be proven by deterministic synchronization on real PostgreSQL where canonical persistence is involved.

---

## 16. Persistence families to design in M5.2

M5.1 freezes semantics, **not exact SQL names**.

M5.2 must decide the minimal CP6-compliant physical delta for the following semantic needs:

```text
ExternalIdentity durable binding
provider signin/link transaction state
pending provider account-enrollment state when mailbox proof is still required
Apple grant/token secret lifecycle state
Apple notification/lifecycle reconciliation state only where durable idempotency requires it
opaque WebAuthn user handle per Account
PasskeyCredential
WebAuthn registration challenge
WebAuthn authentication challenge
one-shot provider profile-bootstrap staging when no canonical profile owner is yet available
```

A single table may serve closely related protocol state only if the semantics/lifecycle/ACL are genuinely the same. Do not collapse unrelated OAuth/provider/WebAuthn/recovery purposes into a generic token/challenge table.

M5.2 must freeze for every materialized object:

```text
canonicality / purpose
columns/types/nullability
UUIDv7 vs bounded technical identity
PK/FK/UNIQUE/CHECK
indexes / query justification
retention/cleanup
secret/verifier/encryption handling
runtime ACL / least privilege
SQLAlchemy mapping
Dictionary entry
Alembic migration
real PostgreSQL proof
```

Permanent chain:

```text
Dictionary
≈ SQLAlchemy
≈ Alembic
≈ real PostgreSQL catalog
≈ human DB reference
≈ direct tests
```

---

## 17. Public API intents to design in M5.2

M5.1 freezes intent families, not final URI spellings.

Required application intents include:

```text
begin/complete Google authentication
begin/complete Apple authentication / provider callback
complete new provider-account enrollment when additional mailbox proof is required
begin/confirm explicit provider link
unlink provider identity safely
begin/complete passkey registration
begin/complete passkey authentication
list/manage current authentication methods where needed by M5 UI/handoff
remove passkey safely
add first password to passwordless Account
recover passwordless Account through existing strong recovery proof
Apple server-notification ingress
provider grant revocation/reconciliation
```

Each material operation must follow the existing API constitution:

```text
/api/v1 application intent
stable operationId
RFC 9457 problems
no-store for sensitive auth responses
request_id
no secret disclosure
OpenAPI deterministic without live provider/network/secrets
Orval/generated-client governance
```

Provider-defined callbacks may use provider-required HTTP forms/content-types and remain outside aesthetic JSON uniformity.

---

## 18. Web Access UX contract for M5

Access remains visually consistent with the accepted M1 design and M3/M4 production implementation.

Primary unauthenticated actions:

```text
Continue with Google
Continue with Apple
Use a passkey
email/password path remains available
```

Use official provider branding/assets/rules; DANTE never imitates provider credential/consent UI.

Required states/behavior:

```text
provider pending
provider cancel
provider error/dependency unavailable
provider account created
known provider signin
link required
link confirmation
passkey selector/ceremony
passkey unavailable/cancelled
backend-authoritative success only
```

### 18.1 Smart onboarding

For a newly created provider Account:

```text
validated provider bootstrap
→ populate/skip redundant setup fields
→ ask only for information still missing
→ do not ask again for name/locale/email already safely available unless confirmation is product-required
```

If all currently required setup data is available, DANTE may proceed directly toward the authenticated handoff.

Full profile/account-security management belongs in the authenticated Home/Settings surface when that surface is materialized, but M5 backend/application design must already support it without rearchitecting Auth.

### 18.2 Passkey registration entry point

M5 must have a real product path capable of registering a passkey for UAT/production use. This may be a bounded post-auth/onboarding security prompt until the full Home Settings surface exists.

Do not create a public `/test/*` endpoint or hidden production-only bypass merely because Home Settings is not yet materialized.

---

## 19. Browser / RP / provider deployment constraints

### 19.1 WebAuthn test origin

Current M4 full-stack testing uses `https://127.0.0.1:4173`. M5 WebAuthn harness must use a valid RP/domain posture rather than relying on an IP RP ID.

Target test direction:

```text
browser origin: https://localhost:<ephemeral-port>
RP ID: localhost
```

or another explicitly configured local test domain with equivalent same-origin HTTPS guarantees.

The main `Secure`, HttpOnly, host-only DANTE session posture remains unchanged.

### 19.2 Apple real Web acceptance

Apple Web redirect configuration requires a registered HTTPS domain; localhost/IP-only proof cannot establish production Apple readiness.

Therefore M5 closure requires both:

```text
mandatory deterministic CI against protocol-faithful local Apple substitute
+ real Apple UAT/smoke against an Apple-registered HTTPS DANTE hostname before production-ready closure
```

Google real-provider acceptance receives an equivalent provider smoke/UAT requirement appropriate to the final Google configuration.

---

## 20. Dependency / cryptography policy

DANTE does not hand-roll JOSE, WebAuthn/COSE/CBOR or general-purpose cryptographic protocols.

Current candidate families identified for qualification include:

```text
maintained Python WebAuthn server library
maintained JOSE/JWK/JWT library
cryptography-backed authenticated encryption for retained provider secret material
existing bounded HTTP client boundary
```

At M5.1 no new dependency/version is approved merely because it is a candidate.

Before admission:

```text
current maintained status
Python 3.14 compatibility
security history/advisories
algorithm support and explicit allowlisting
API fit / no dangerous implicit defaults
transitive dependency impact
uv lock determinism
Ruff/mypy/test/build compatibility
real protocol-vector tests
```

No provider private key, encryption key, client secret or live token is committed to Git.

---

## 21. Rate/resource abuse controls

Apply cheap validation/rate limits before expensive or external work where possible.

Bound at least:

```text
provider transaction creation
provider callback/completion failures
JWK refresh fan-out
link attempts
passkey option/challenge issuance
passkey verification failures
add/remove authenticator attempts
Apple notification processing
```

No unbounded background task per provider callback. Provider notification/cleanup workers, if needed, use bounded queues/concurrency and defined shutdown behavior under the same M4 discipline.

---

## 22. Privacy / logging / data minimization

Authentication asks providers only for the information needed for identity/bootstrap.

Do not request contacts, calendars, mailbox content, birthday, gender or unrelated profile data as part of Auth.

Never log/expose:

```text
provider authorization code
ID/access/refresh token
Apple client private key/client-secret JWT
raw provider transaction state/nonce where it is secret-bearing
passkey challenge where log exposure would aid replay analysis
WebAuthn private material (never available to DANTE)
credential signatures/raw assertions beyond bounded protected diagnostics
session/cookie/CSRF secret
password/OTP/recovery secret
```

Allowed protected telemetry uses safe references/event codes, request IDs, provider class and bounded non-secret failure categories.

Provider emails/names/avatar URLs are personal data and follow DANTE privacy/access rules.

---

## 23. Testing / proof matrix

The existing Access/Auth testing constitution remains binding:

```text
unit
!= PostgreSQL
!= API
!= generated contract
!= Web application
!= browser full-stack
!= real external provider acceptance
```

### 23.1 Google

Prove at least:

```text
known ExternalIdentity signin
new Account with provider-authoritative email
third-party Google mailbox path requiring DANTE proof where applicable
email collision → no silent Account merge
explicit link success
wrong issuer/audience/signature/nonce/expiry
unknown kid + bounded JWK refresh/key rotation
callback/credential replay
provider cancel/error/outage
email/profile change does not alter issuer+subject binding
later provider profile does not overwrite user-owned DANTE profile state
concurrent first-signin/link races
Account disabled race
```

### 23.2 Apple

Prove at least:

```text
state/nonce/code flow
server-side code exchange
ID-token issuer/audience/signature/expiry/nonce verification
first authorization with name/email
later authorization without one-shot name data
Hide My Email / relay address
relay forwarding change reconciliation
consent/revocation notification
account-change/delete notification classes
notification signature validation/replay/idempotency
Apple JWK rotation
code/token replay/error/outage
protected retained grant secret
provider revoke behavior
email collision/linking races
real Apple UAT on registered HTTPS hostname
```

### 23.3 Passkeys

Prove at least:

```text
registration success
userVerification required
resident/discoverable credential path
opaque userHandle correctness
duplicate credential rejection
registration challenge expiry/replay
origin mismatch
RP ID mismatch
credential/userHandle mismatch
signature failure
authentication challenge expiry/replay
username-less signin
multiple passkeys one Account
synced/device-bound metadata handling
signCount anomaly policy
passkey removal anti-lockout
passwordless Account signin
lost-all-authenticator recovery → establish password + fresh signin
cross-device/hybrid behavior where platform test support exists
conditional UI only as progressive enhancement
```

### 23.4 Browser matrix

Keep Chromium + Firefox + WebKit for critical Web product/auth semantics.

Do not fake platform capability merely to claim a matrix. If virtual WebAuthn/provider automation is browser-engine-specific, prove protocol/server invariants at the lowest truthful layer, run real browser capability where supported, and record the exact bounded exception permitted by `access-auth-testing-contract.md`.

Playwright retries remain disabled for the critical Auth spine unless separately justified by evidence.

Mandatory CI remains deterministic and independent of public Internet availability. Local provider substitutes must be protocol-faithful and must exercise DANTE's real adapter/application/security path rather than bypassing it.

---

## 24. Benchmark findings carried into DANTE

Public product behavior used as benchmark, not as semantic authority:

```text
Linear
→ first identity-provider provisioning can bootstrap profile attributes
→ later logins do not own/overwrite the user profile
→ multiple passkeys / Security & Access / sessions / authorized apps patterns

Notion
→ Google/Apple/password/passkeys coexist
→ provider/social-created Accounts can establish a password
→ multiple passkeys and account/session security management

Todoist
→ social-created Accounts can add a password

GitHub
→ mature passkey flows including cross-device/nearby-device behavior

Figma / Slack / comparable products
→ authentication/security and connected-app/data integrations remain separate user concepts
```

DANTE intentionally keeps a stricter no-silent-email-link rule even where another product uses simpler matching behavior.

Benchmark behavior never overrides provider specifications or DANTE's accepted architecture/security contracts.

---

## 25. Official external authority basis reviewed for M5.1

Reviewed current official/public authorities include:

Google:

- Google Identity Services Web guides and JS reference;
- Google ID-token server verification guidance;
- Google OpenID Connect claims/identity guidance;
- current FedCM/GIS browser direction.

Apple:

- Configuring Sign in with Apple for Web;
- Sign in with Apple REST token validation/revocation;
- Apple public-key verification guidance;
- Sign in with Apple server-to-server notifications/account-change processing;
- Private Email Relay sender configuration;
- Apple button/Human Interface requirements;
- app-transfer/migration compatibility guidance where relevant to schema longevity.

WebAuthn/FIDO:

- W3C Web Authentication Level 3 Candidate Recommendation, 2026-05-26;
- FIDO Alliance passkey deployment/synced-device-bound guidance;
- current browser/platform WebAuthn capability guidance.

Primary URLs to re-check at implementation time:

```text
https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
https://developers.google.com/identity/gsi/web/reference/js-reference
https://developers.google.com/identity/openid-connect/openid-connect
https://developer.apple.com/documentation/signinwithapple/configuring-your-webpage-for-sign-in-with-apple
https://developer.apple.com/documentation/signinwithapplerestapi/revoke-tokens
https://developer.apple.com/documentation/signinwithapple/processing-changes-for-sign-in-with-apple-accounts
https://developer.apple.com/help/account/capabilities/configure-private-email-relay-service
https://www.w3.org/TR/webauthn-3/
https://fidoalliance.org/passkeys/
```

Provider documentation can change. Exact adapter behavior is revalidated at materialization; M5.1 semantics are reopened only if current provider requirements actually contradict them.

---

## 26. M5.1 closure / exact continuation point

```text
M1                         CLOSED
M2                         CLOSED
M3                         CLOSED / ENGINEERING PASS / USER ACCEPTED
M4                         CLOSED / ENGINEERING PASS / USER ACCEPTED
M5 overall                 ACTIVE
M5.1 external/spec/benchmark readback   COMPLETE
M5.1 architecture/security freeze       COMPLETE
M5 runtime implementation               NOT STARTED
M5 persistence migration                NOT STARTED
M5 OpenAPI/client changes               NOT STARTED
M5 Web runtime integration              NOT STARTED
```

**NEXT:** M5.2 — exact persistence + API design.

A continuation agent must not restart the broad Google/Apple/passkey benchmark unless current provider evidence changes materially. It must start by reconciling this contract against current Dictionary/SQLAlchemy/Alembic/application code and designing the minimal exact M5 persistence/API delta.

M5.2 deliverables before production code:

```text
1. exact object ownership and persistence semantics
2. exact tables/columns/types
3. PK/FK/UNIQUE/CHECK/indexes
4. retention/cleanup/encryption/verifier handling
5. runtime ACL / least privilege
6. transaction/lock/race state machines
7. exact API intents/paths/operationIds/problem codes
8. provider callback/redirect topology
9. WebAuthn RP/origin/challenge topology
10. dependency qualification plan
11. exact test matrix mapped to proof layer
12. bounded implementation write gate
```

No merge to `main`, new branch/worktree, M6 implementation or M7 closure work is authorized by this contract.