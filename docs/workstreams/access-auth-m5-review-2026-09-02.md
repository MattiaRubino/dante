# DANTE — Access/Auth M5 Review and UAT Reconciliation — 2026-09-02

- **Status:** CURRENT REVIEW / BRANCH-LOCAL EVIDENCE
- **Branch:** `feature/access-auth`
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Current branch checkpoint at review start:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Accepted Alembic head:** `20260831_13`
- **PostgreSQL:** 18.6
- **Scope:** Group-4 engineering proof, manual password/passkey UAT, real Google UAT, direct database verification, deprecation/coherence review and external product/security benchmark
- **Out of scope:** Apple registered-domain UAT, production email-delivery provider selection, M7 session/device/security-event UX, branch merge

This document is the durable 2026-09-02 reconciliation point for the Access/Auth vertical. It records observed evidence without converting open external-delivery/Apple obligations into false PASS claims.

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
real Internet email delivery               OPEN / RESEARCH + QUALIFICATION REQUIRED
real Apple registered-domain UAT            DEFERRED / OPEN
whole M5                                    ACTIVE / NOT FORMALLY CLOSED
```

The full automated Web gate was executed at `ab2716...`. The later `9c0587...` delta is isolated to the opt-in local-UAT SMTP runner and does not change product Auth code, DB, Alembic or UI. That tooling delta still requires its own targeted format/lint/compile/real-delivery qualification before it can be called accepted.

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

No material deprecated Auth primitive was found in the reviewed production path.

### Google

Current code uses:

```text
https://accounts.google.com/gsi/client
Google Identity Services renderButton
nonce bound to DANTE transaction
use_fedcm_for_button = true
button_auto_select = false
```

Google's current API reference still supports `use_fedcm_for_button`. The deprecated property is `use_fedcm_for_prompt`, which DANTE does not use.

### Google identity authority

DANTE uses provider `sub` under the canonical Google issuer and never email as the federated identity key. This matches current Google OIDC guidance. Gmail and verified Workspace+`hd` can establish the represented mailbox; a third-party mailbox Google Account requires additional proof when current mailbox control matters. The live UAT exercised exactly this branch.

### WebAuthn

DANTE uses the browser WebAuthn API only for ceremony interaction/serialization and `python-fido2` for RP verification. Current policy requires discoverable credentials and user verification, uses exact RP/origin binding and attestation `none`, and stores public credential material rather than biometric/PIN data.

The standards literature increasingly prefers the term “discoverable credential” over “resident key”; the WebAuthn API field/enum still retains `residentKey` naming. DANTE's use is an API compatibility term, not a stale custom concept.

### Apple

Current Apple guidance dated 2026-08-24 says new Sign in with Apple relay addresses will move to `private.icloud.com` later in 2026 while existing `privaterelay.appleid.com` addresses continue to work. DANTE's M5 Apple semantics already account for both domains. Apple real registered-domain UAT remains open.

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

Notion publicly supports password/email-provider/passkey combinations, multiple passkeys, passwordless passkeys, fallback to other methods, remote session sign-out and new-login alerts. DANTE already matches the flexible multi-authenticator/passwordless model and has stronger backend anti-lockout invariants; remote session management and security alerts remain M7 work.

### Linear

Linear exposes a Security & Access area with multiple passkeys, current/other active sessions, per-session revoke and revoke-all-other controls, and 30-day inactive-session expiry. DANTE's server model already supports multiple AuthSessions and 30-day policy direction; the equivalent mature session/device management UX is deliberately deferred to M7.

### Microsoft / large-account pattern

Large account systems commonly provide account-wide sign-out/revocation controls. DANTE's persistence/session model can support this without redesign; the consumer-facing management surface remains open.

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
```

### Remaining maturity gaps

1. **Session/device management UI** — list/revoke one/revoke others/log out everywhere; M7.
2. **New-login/security-event notifications and “this wasn't me” response** — M7.
3. **Security UI maintainability** — `access-security-page.tsx` has grown into a large orchestration/rendering component; functionality is accepted, but later hardening should split bounded password/provider/passkey/reauth sections without changing semantics.
4. **Real outbound email architecture and deliverability** — not yet selected or qualified. The correct question is broader than “which SMTP vendor”: ownership, SMTP/HTTP provider boundary, SPF/DKIM/DMARC, bounce/complaint handling, suppression, retry ambiguity, provider portability, observability, privacy, Apple relay compatibility and DEV/UAT/PROD separation must be designed together.
5. **Apple registered-domain real UAT** — deferred until a usable Apple test account/domain setup is available.

## 10. Email status — intentionally not decided here

`9c0587...` adds a strictly opt-in real-SMTP configuration path to the local UAT runner while preserving loopback capture by default. This is tooling capability only.

It does **not** select Brevo, SES, Postmark, Resend, SendGrid, direct self-hosted SMTP or any other production architecture. Before selecting a provider DANTE must perform a dedicated email-delivery architecture/research gate.

Until then:

```text
automated CI email       loopback deterministic capture
real Internet delivery   OPEN
provider selection       OPEN
production DNS/sender    OPEN
bounce/complaint model   OPEN
```

## 11. Documentation reconciliation rule

The current operational truth is owned by:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
this review
```

Older M5 contract sections that say “M5-F next”, “public routes later” or similar remain milestone-time reconciliation snapshots when embedded inside otherwise durable semantic contracts. Their semantic/security decisions remain authoritative unless superseded; their old progress metadata does not override the current operational documents above.

## 12. External sources reviewed on 2026-09-02

Official/current sources used for the benchmark include:

- NIST SP 800-63B-4 — `https://pages.nist.gov/800-63-4/sp800-63b.html`
- Google OpenID Connect reference — `https://developers.google.com/identity/openid-connect/reference`
- Google Identity Services JS reference — `https://developers.google.com/identity/gsi/web/reference/js-reference`
- GitHub sudo mode / passkey documentation — `https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/sudo-mode` and `https://docs.github.com/en/authentication/authenticating-with-a-passkey`
- Notion passkey/login documentation — `https://www.notion.com/help/passkeys` and `https://www.notion.com/help/log-in-and-out`
- Linear Security & Access / login methods — `https://linear.app/docs/security-and-access` and `https://linear.app/docs/login-methods`
- Apple Developer News, 2026-08-24 Sign in with Apple relay-domain update — `https://developer.apple.com/news/?id=1ptvdtcm`

Repository truth and executed DANTE evidence remain the authority for DANTE itself.