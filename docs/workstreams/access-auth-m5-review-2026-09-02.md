# DANTE — Access/Auth M5 Review and UAT Reconciliation — 2026-09-02

- **Status:** CURRENT REVIEW / BRANCH-LOCAL EVIDENCE
- **Branch:** `feature/access-auth`
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Real-SMTP UAT tooling checkpoint:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Accepted Alembic head:** `20260831_13`
- **PostgreSQL:** 18.6
- **Scope:** Group-4 engineering proof, manual password/passkey UAT, real Google UAT, direct database verification, deprecation/coherence review, external product/security benchmark, outbound-email architecture review
- **Out of scope:** Apple registered-domain UAT, exact Email Platform persistence/implementation, SES production qualification, branch merge
- **Email architecture outcome:** `../architecture/access-auth-email-delivery.md` + `../decisions/ADR-012-email-delivery-platform.md`

This document is the durable 2026-09-02 reconciliation point for the Access/Auth vertical. It records observed evidence without converting open Internet-delivery/Apple obligations into false PASS claims.

## 1. Current conclusion

```text
M1–M4                                      CLOSED / ACCEPTED
M5.1 / M5.2                                COMPLETE
M5-A–D                                     COMPLETE
GROUP 1 / M5-E+G                           COMPLETE / ENGINEERING PASS
GROUP 2 / M5-F                             COMPLETE / ENGINEERING PASS
GROUP 3 / M5-H+I                           COMPLETE / ENGINEERING PASS
GROUP 4 product implementation             ENGINEERING QA PASS
GROUP 4 local password/passkey UAT          PASS
GROUP 4 real Google UAT                    PASS

email-delivery architecture                ACCEPTED DIRECTION
primary production delivery target         AMAZON SES API V2 / QUALIFICATION OPEN
durable Email Platform implementation       OPEN
real Internet email delivery               OPEN
real Apple registered-domain UAT            DEFERRED / OPEN
whole M5                                    ACTIVE / NOT FORMALLY CLOSED
```

The full automated Web gate was executed at `ab2716...`. The later `9c0587...` delta is isolated to the opt-in local-UAT SMTP runner and does not change product Auth code, DB, Alembic or UI. That tooling delta still requires its own targeted format/lint/compile/real-delivery qualification before it can be called accepted.

ADR-012 closes the architecture direction for outbound transactional/security email. It does **not** claim that the durable outbox, SES adapter, DNS/reputation configuration, provider-event path or real inbox UAT already exist.

## 2. Automated Group-4 evidence

Observed final product-code gate at `ab2716...`:

```text
Prettier format check                       PASS
TypeScript typecheck                        PASS
ESLint                                      PASS
architecture/dependency-cruiser             PASS
Web unit/component tests                    68 / 68 PASS
Auth Playwright HTTPS suite                 60 / 60 PASS
Chromium / Firefox / WebKit                 PASS through the canonical suite
production Vite build                       PASS inside Playwright harness
```

The 60 browser tests include the M5 functional/quality matrix and retained M3/M4 regressions. Browser evidence does not replace PostgreSQL/protocol proof, and PostgreSQL/protocol proof does not replace browser evidence.

## 3. Live manual UAT evidence

### 3.1 Password/session

Observed PASS:

```text
seeded password signin
server-authoritative authenticated return
session persistence across navigation + hard reload
password reauthentication
same-session bearer/cookie rotation remains authoritative
logout
password removal when another authenticator remains
password re-establishment
fresh logout + password signin with re-established password
```

### 3.2 Passkey / Windows Hello

Observed with a real Windows platform authenticator, not Playwright simulation:

```text
WebAuthn registration begin
browser conversion of canonical options.publicKey envelope
navigator.credentials.create
native Windows Hello passkey prompt
backend FIDO2 verification
PasskeyCredential persistence
inventory display
passkey reauthentication
anonymous username-less/discoverable passkey signin
passkey rename + reload persistence
anti-lockout protection
```

The retained passkey label used during UAT was `PC Mattia - Windows`.

### 3.3 Anti-lockout

Live sequence:

```text
Account has Password + Passkey
→ remove Password
→ PASS; Account remains passkey-only
→ attempt removal of remaining Passkey
→ backend rejects with auth.authenticator_removal_blocked
→ explicit Italian UI explanation
→ Passkey remains present
→ establish Password again
→ fresh logout/login with new Password succeeds
```

This proves that the UI is not the authority: durable backend state prevents the last direct authenticator from being removed.

## 4. Defects found by live UAT and repaired

UAT found real defects that automated proof had not previously exposed:

1. **AuthSession rotation race** — an in-flight session read could overwrite the freshly rotated authenticated state after sensitive mutations. The application boundary now cancels the exact in-flight session query before committing authoritative rotated/new session state; a regression test covers reauth → navigation → reload.
2. **Cross-chunk remote error identity** — security UI error classification was hardened so remote failures remain classifiable across lazy/chunk boundaries.
3. **WebAuthn response-envelope mismatch** — the browser adapter incorrectly treated ceremony options as flattened. Canonical backend output is `ceremony.options.publicKey`; adapter and tests were corrected. Live Windows Hello registration then succeeded.

These are closed defects. They are evidence for retaining manual UAT in addition to automated tests.

## 5. Real Google UAT

Real Google Identity Services was configured with a dedicated Web OAuth client for `https://localhost:4173` and exercised through the official Google-rendered control.

Observed live chain:

```text
DANTE /google/begin
→ ExternalAuthTransaction + nonce
→ official Google Identity Services account interaction
→ real Google ID token
→ backend JWK/signature/issuer/audience/nonce validation
→ issuer + subject identity resolution
→ third-party mailbox classification
→ DANTE mailbox verification challenge
→ Account creation
→ canonical DANTE AuthSession
→ authenticated onboarding
```

The chosen Google Account used a third-party mailbox rather than Gmail/Workspace. DANTE therefore required direct mailbox proof before Account establishment. This is intentional policy, not a provider failure.

The mailbox-verification message in this specific run was consumed through the deterministic loopback SMTP capture because the runner had not yet been switched to a real Internet delivery provider. Therefore:

```text
Google provider authentication       REAL / PASS
DANTE mailbox-verification logic     REAL BACKEND + CAPTURE / PASS
Internet email deliverability        NOT PROVED BY THIS RUN
```

Direct PostgreSQL inspection after completion proved:

```text
Account                         1 / active
EmailIdentity                   verified
ExternalIdentity.provider_code  google
ExternalIdentity.issuer         https://accounts.google.com
ExternalIdentity.subject        present / stable provider subject
ExternalIdentity.status         active
PasswordCredential              0
AuthSession                     ACTIVE
```

Personal email address and provider subject are intentionally not copied into repository documentation.

The `PasswordCredential = 0` result is important: a Google-created DANTE Account is genuinely passwordless and still converges on the same canonical Account/AuthSession model.

## 6. Google configuration incident — non-product defect

The first real Google attempt returned `401 invalid_client` because the OAuth Client ID had been manually transcribed with one wrong character while starting the UAT runner. Copying the exact Client ID from Google resolved it without a DANTE code change.

Classification:

```text
external/UAT configuration transcription error
!= backend defect
!= missing client secret
!= OAuth architecture defect
```

DANTE's GIS ID-token flow requires the public Web client ID; it does not use the OAuth client secret in the browser.

## 7. Current deprecation/coherence review

### 7.1 Google

Current code uses:

```text
https://accounts.google.com/gsi/client
Google Identity Services renderButton
nonce bound to DANTE transaction
use_fedcm_for_button = true
button_auto_select = false
```

Google's current API reference still supports `use_fedcm_for_button`. The deprecated property is `use_fedcm_for_prompt`, which DANTE does not use.

### 7.2 Google identity authority

DANTE uses provider `sub` under the canonical Google issuer and never email as the federated identity key. This matches current Google OIDC guidance. Gmail and verified Workspace+`hd` can establish the represented mailbox; a third-party mailbox Google Account requires additional proof when current mailbox control matters. The live UAT exercised exactly this branch.

### 7.3 WebAuthn

DANTE uses the browser WebAuthn API only for ceremony interaction/serialization and `python-fido2` for RP verification. Current policy requires discoverable credentials and user verification, uses exact RP/origin binding and attestation `none`, and stores public credential material rather than biometric/PIN data.

The standards literature increasingly prefers the term “discoverable credential” over “resident key”; the WebAuthn API field/enum still retains `residentKey` naming. DANTE's use is an API compatibility term, not a stale custom concept.

### 7.4 Apple

Current Apple guidance dated 2026-08-24 says new Sign in with Apple relay addresses will move to `private.icloud.com` later in 2026 while existing `privaterelay.appleid.com` addresses continue to work. DANTE's M5 Apple semantics already account for both domains. Apple real registered-domain UAT remains open.

### 7.5 Repository-documentation contradictions found

The 2026-09-02 documentation audit found current-looking index/register text that had not followed the executable vertical:

```text
docs/workstreams/README.md
→ still said M2 ACTIVE / M3 NOT STARTED / production Auth NOT STARTED

docs/architecture/technical-decisions.md
→ still reported protected-main CP6 counts as current Access/Auth counts
→ still said old access-frontend branch active / first backend vertical NOT STARTED
→ still described API codegen as future activation despite current materialization
```

Those current references were reconciled. Historical evidence/ADR context was not rewritten to pretend later implementation existed at the earlier checkpoint.

### 7.6 SES pricing claim correction

The previous research discussion contained an SES-specific claim that new users could rely on 3,000 message charges/month free for the first 12 months. Current AWS information makes that claim stale for **new customers after July 21, 2026**; AWS moved new customers to newer pricing-plan/general Free Tier credit mechanics.

This correction matters because provider architecture must not be justified by a promotion that no longer applies. SES remains the primary target for architectural/operational reasons, not the obsolete allowance.

## 8. Benchmark against mature products and standards

This comparison is directional evidence, not an assertion that external products share DANTE internals.

### NIST SP 800-63B-4

Current NIST guidance for single-factor passwords requires a minimum of 15 characters, recommends support for at least 64, forbids composition rules and requires checking prospective passwords against commonly used/compromised values.

DANTE currently aligns:

```text
minimum 15 Unicode code points
>=64 supported
no forced composition rules
NFC handling
HIBP compromised-password screening
rate limiting
no arbitrary periodic password change
```

### GitHub

GitHub uses reauthentication (“sudo mode”) before sensitive account actions and supports passkeys for signin and sensitive reauthentication. DANTE's recent-auth requirement before authenticator mutations follows the same mature security pattern, with its own policy window.

### Notion

Notion publicly supports password/email-provider/passkey combinations, multiple passkeys, passwordless passkeys, fallback to other methods, remote session sign-out and new-login alerts. DANTE already matches the flexible multi-authenticator/passwordless model and has backend anti-lockout invariants; remote session management and security alerts remain M7 work.

### Linear

Linear exposes a Security & Access area with multiple passkeys, current/other active sessions, per-session revoke and revoke-all-other controls. DANTE's server model already supports multiple AuthSessions; equivalent mature session/device management UX is deliberately deferred to M7.

### Microsoft / large-account pattern

Large account systems commonly provide account-wide sign-out/revocation controls. DANTE's persistence/session model can support this without redesign; the consumer-facing management surface remains open.

### Netflix email delivery evidence

Netflix publicly documents moving its email delivery workload from in-house systems to Amazon SES and separating transactional/marketing reputation pools. This supports the architectural boundary `application/platform owns product behavior; specialist infrastructure owns last-mile delivery`.

It does not imply DANTE must copy Netflix scale topology or dedicated-IP decisions at low volume.

### Fanatics email platform evidence

Fanatics publicly describes building an internal email platform while using SES for scalable delivery and maintaining granular traffic segmentation. This is especially relevant to DANTE's chosen direction:

```text
DANTE lifecycle / queue / state / policy
+
provider delivery engine
```

Again, this is directional evidence, not permission to copy undocumented internals or scale machinery mechanically.

### Evidence discipline

No claim is made here that Notion, Linear or another named app uses SES/Postmark/SendGrid/etc. unless there is direct current public evidence. Security/product UX comparison and provider-infrastructure comparison are separate evidence categories.

## 9. Quality findings

### Strong/current

```text
single canonical Account/AuthSession authority
provider ID token never becomes DANTE session
passwordless Accounts are first-class
backend anti-lockout
recent-auth for sensitive changes
same-origin cookie + CSRF browser posture
real PostgreSQL authority
real provider + real authenticator UAT
Google third-party mailbox handling
WebAuthn private-key/biometric non-persistence
provider-neutral EmailDeliveryPort already exists
bounded SMTP worker + no blind retry already exists
```

### Remaining maturity gaps

1. **Email Platform operational/provider qualification** — SES account/sandbox/region/IAM/domain/privacy/cost/event path must be researched and proved before production implementation.
2. **Durable Email Platform implementation** — transactional outbox, delivery attempts/provider IDs, sensitive payload handling, event ingestion, suppression and observability are not materialized.
3. **Real Internet email acceptance** — signup/provider verification/recovery/reset notification must reach a real inbox and be verified with direct state evidence.
4. **Session/device management UI** — list/revoke one/revoke others/log out everywhere; M7.
5. **New-login/security-event notifications and “this wasn't me” response** — M7; should reuse the Email Platform rather than create a parallel mail path.
6. **Security UI maintainability** — `access-security-page.tsx` has grown into a large orchestration/rendering component; functionality is accepted, but later hardening should split bounded password/provider/passkey/reauth sections without changing semantics.
7. **Apple registered-domain real UAT** — deferred until a usable Apple test account/domain setup is available.

## 10. Email architecture review outcome

The email architecture question is now closed at the **direction** level.

Accepted North Star:

```text
DANTE owns the email lifecycle.
Amazon SES is the primary target for last-mile production delivery.
```

More precisely:

```text
Auth / DANTE feature
→ durable Email Intent
→ PostgreSQL transactional outbox
→ bounded worker/orchestrator
→ provider-neutral adapter
→ Amazon SES API v2
→ recipient infrastructure
→ delivery/bounce/complaint feedback
→ DANTE delivery state / suppression / metrics
```

Preferred initial SES region target is `eu-south-1` Europe/Milan, subject to operational/provider qualification.

### Why not self-host production SMTP by default

DANTE would inherit disproportionate operational work unrelated to product differentiation:

```text
MTA operations
IP/domain reputation management
bounce/complaint infrastructure
provider-specific deliverability tuning
abuse controls
queue/retry edge cases
TLS/DNS operations
blacklist/remediation burden
```

Owning lifecycle/state while outsourcing last-mile delivery preserves product control without turning DANTE into a mail operator.

### Why API over SMTP for primary production adapter

SES API v2 is preferred because it better exposes:

```text
structured provider responses
provider message references
configuration sets/tags
IAM/workload identity
native event-publishing integration
operational error classification
```

SMTP remains valuable for deterministic local capture, explicit real-provider UAT and generic compatibility.

### Durable outbox requirement

The current process-owned `asyncio.Queue` is bounded and correctly avoids blind transport retry, but it is not crash-durable.

Production target must ensure:

```text
security/business COMMIT succeeds
→ required email intent cannot disappear because process dies
```

Therefore outbound security email becomes the first concrete TD-04 Class-A transactional-outbox consumer.

Exact tables/columns/indexes/ACLs are **not** frozen by this review. They require a separate ADR-010 persistence design/write gate.

### Sensitive payload requirement

OTP/recovery proof must never become normal long-lived plaintext outbox/log material.

The exact implementation needs a short-lived protected payload design, likely envelope encryption or equivalent, with purpose-separated keys, TTL and cleanup/erasure after provider acceptance or expiry.

This remains an implementation design gate, not a solved detail.

### Ambiguous send outcome

```text
provider definitively rejected before acceptance
→ bounded retry may be safe

provider accepted / message ID returned
→ record acceptance; do not duplicate

network timeout / ambiguous outcome
→ NO blind retry
→ preserve uncertainty and reconcile/policy-handle explicitly
```

### Feedback/suppression

Production acceptance requires normalized handling for at least:

```text
accepted/sent
delivered
delivery_delayed
bounced
complained
rejected
```

Hard bounce/complaint must be able to create a DANTE-owned delivery restriction/suppression without redefining `EmailIdentity` itself.

### Sender/reputation posture

Before production sender acceptance:

```text
DANTE-owned sender domain/subdomain
SPF
DKIM
DMARC
```

Auth/security email:

```text
open tracking        OFF
click tracking       OFF
link rewriting       OFF
marketing content    FORBIDDEN
```

Auth/security, normal product notifications and future marketing must remain separable traffic/reputation classes.

### Current acceptance status

```text
EmailDeliveryPort                         IMPLEMENTED
SmtpEmailDispatcher                      IMPLEMENTED
bounded process queue                    IMPLEMENTED
no blind SMTP retry                      IMPLEMENTED
loopback SMTP capture                    IMPLEMENTED / CI
opt-in real SMTP local-UAT config         IMPLEMENTED at 9c0587af...

ADR-012 architecture direction           ACCEPTED
SES primary target                       SELECTED / NOT QUALIFIED
transactional outbox                     NOT MATERIALIZED
SES API adapter                          NOT MATERIALIZED
provider event ingestion                 NOT MATERIALIZED
suppression management                   NOT MATERIALIZED
sender DNS/domain                        NOT MATERIALIZED
real Internet signup/recovery UAT         OPEN
```

`SELECTED != IMPLEMENTED != DIRECT PASS`.

## 11. Immediate next gate

Do not write production Email Platform code yet.

First perform a deep current-source qualification of:

```text
AWS account and billing posture
SES sandbox vs production-access path
SES eu-south-1 exact capability / quotas / pricing
sender identity / domain mechanics
SPF / DKIM / DMARC
IAM role / workload identity / least privilege
SES API v2 SDK/runtime integration
configuration sets / traffic segmentation
event destinations
SNS vs EventBridge ingestion boundary
privacy / retention / subprocessors
provider limits and failure semantics
alternative-provider reopen criteria
expected DANTE cost at realistic volumes
exact transactional-outbox + sensitive-payload threat model
real Internet UAT plan
```

Use official/current provider sources for version-sensitive claims. Community sources may supplement operational experience but must not override provider authority.

If SES qualification produces a material blocker, reopen only the provider target first. The provider-neutral DANTE-owned lifecycle boundary remains accepted unless evidence disproves it.

## 12. Documentation reconciliation rule

The current operational truth is owned by:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
this review
docs/architecture/access-auth-email-delivery.md
docs/decisions/ADR-012-email-delivery-platform.md
```

Older M5 contract sections that say “M5-F next”, “public routes later” or similar remain milestone-time reconciliation snapshots when embedded inside otherwise durable semantic contracts. Their semantic/security decisions remain authoritative unless superseded; their old progress metadata does not override the current operational documents above.

The old 2026-08-29 M5 live handoff is historical. The 2026-09-02 live handoff is active-branch operational material only and must be consolidated/removed before protected-main integration.

## 13. External sources reviewed on 2026-09-02

Official/current sources used for the security/provider benchmark include:

- NIST SP 800-63B-4 — `https://pages.nist.gov/800-63-4/sp800-63b.html`
- Google OpenID Connect reference — `https://developers.google.com/identity/openid-connect/reference`
- Google Identity Services JS reference — `https://developers.google.com/identity/gsi/web/reference/js-reference`
- GitHub sudo mode / passkeys — `https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/sudo-mode` and `https://docs.github.com/en/authentication/authenticating-with-a-passkey`
- Notion passkeys/login — `https://www.notion.com/help/passkeys` and `https://www.notion.com/help/log-in-and-out`
- Linear Security & Access / login methods — `https://linear.app/docs/security-and-access` and `https://linear.app/docs/login-methods`
- Apple Developer News 2026-08-24 relay-domain update — `https://developer.apple.com/news/?id=1ptvdtcm`
- AWS SES API sending — `https://docs.aws.amazon.com/ses/latest/dg/send-email-api.html`
- AWS SES endpoints/regions — `https://docs.aws.amazon.com/general/latest/gr/ses.html`
- AWS SES event publishing — `https://docs.aws.amazon.com/ses/latest/dg/monitor-using-event-publishing.html`
- AWS SES configuration sets — `https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html`
- AWS SES IAM — `https://docs.aws.amazon.com/ses/latest/dg/control-user-access.html`
- AWS SES pricing — `https://aws.amazon.com/ses/pricing/`
- AWS SES pricing-plan update — `https://aws.amazon.com/blogs/messaging-and-targeting/introducing-amazon-simple-email-service-ses-pricing-plans/`
- Netflix SES case study — `https://aws.amazon.com/ses/netflix-ses-case-study/`
- Fanatics SES platform case study — `https://aws.amazon.com/blogs/messaging-and-targeting/how-fanatics-commerce-built-a-scalable-email-platform-on-amazon-ses/`

Repository truth and executed DANTE evidence remain the authority for DANTE itself.
