# DANTE — Mobile Access technical contract

Status: **APPROVED CROSS-PLATFORM CONTRACT / PRG-0 PASS / PRE-IMPLEMENTATION**  
Date: 2026-08-20  
Desktop authority: **Access A3.4**  
Mobile authority: **Access M1.2 + PRG-0** — `107010` bytes — SHA-256 `2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676`

## 1. Purpose and boundary

This document defines what iOS/Android Access and the future AuthN backend must support before production implementation. It does **not** freeze React Native/native/Flutter, HTTP paths, DTO names, token representation, DB schema, provider SDK versions or exact session/challenge lifetimes.

Permanent invariants:

```text
Person != Account != Principal != Actor
sign-in != provider-data authorization
provider authentication != Calendar/Gmail/iCloud permission
provider state != canonical DANTE state
verification != profile setup
reauthentication != initial sign-in
client integrity != person identity or authorization
```

## 2. Cross-platform state model

```text
APP_LAUNCH
├─ valid session -> destination
├─ refreshable session -> SESSION_REFRESH
├─ reauth required -> REAUTH
└─ no session -> SIGN_IN

SIGN_IN
├─ password -> AUTHENTICATE_PASSWORD
├─ Google/Apple -> PROVIDER_START -> PROVIDER_RETURN
├─ create account -> SIGN_UP_EMAIL
└─ forgot password -> RECOVERY_BEGIN

SIGN_UP_EMAIL -> SIGN_UP_PASSWORD -> VERIFY_EMAIL -> ACCOUNT_READY
-> SETUP_NAME -> SETUP_LOCALE -> SETUP_START
   ├─ FIRST_ACTION -> HOME_HANDOFF
   ├─ IMPORT -> HOME_HANDOFF
   ├─ DEMO -> HOME_HANDOFF
   └─ SKIP -> HOME_HANDOFF

RECOVERY_BEGIN -> RECOVERY_SENT -> RECOVERY_LINK_RETURN
-> RESET_PASSWORD -> RESET_COMPLETE -> SIGN_IN

PROVIDER_RETURN
├─ authenticated -> SESSION_ESTABLISH -> destination
├─ new account -> setup
├─ collision -> ACCOUNT_LINK
├─ cancel -> SIGN_IN
└─ failure -> PROVIDER_ERROR

SESSION_EXPIRED -> REAUTH
├─ success -> restore safe context
└─ cancel/failure-to-continue -> signed-out Access
```

System Back/predictive Back follows this logical graph, not arbitrary component history.

## 3. Mobile presentation contract

Mobile is not scaled-down desktop. Required behavior:

- full-screen phone surface; no desktop brand stage behind forms;
- safe-area/system-bar/cutout/IME awareness;
- no horizontal scroll;
- usable at 393×852, 412×915 and stress 360×800;
- low-height/keyboard-visible layouts remain scrollable with primary action reachable;
- high text scaling must reflow rather than clip;
- Android effective interactive targets >=48×48 dp;
- password-manager, paste and OTP AutoFill semantics are first-class;
- platform provider order may differ without changing outcomes;
- provider-owned chooser/consent UI is never recreated by DANTE.

## 4. Client ↔ backend capability contract

Names below are capability identifiers, **not endpoint names**.

### `access.bootstrapSession`
Determines startup auth state.

Results: `authenticated`, `refresh_required`, `reauth_required`, `unauthenticated`.  
Failures: transport/service unavailable, client update required where later supported.

### `access.authenticatePassword`
Inputs: normalized account identifier, password proof over TLS, client context required for risk controls.  
Public results: authenticated or stable non-enumerating failure.  
Required distinctions internally: invalid credential, throttled/temporarily blocked, service unavailable.

### `access.beginRegistration`
Starts registration without broad profile collection and without unsafe account enumeration.

### `access.setRegistrationCredential`
Accepts/rejects candidate credential under server-owned policy. Password is never persisted locally by DANTE.

### `access.issueEmailChallenge`
Returns challenge reference, masked destination and UX-safe expiry/resend metadata. Backend owns attempts, expiry, supersession and abuse controls.

### `access.verifyEmailChallenge`
Results must represent verified, invalid, expired, consumed and temporarily limited conditions without client guesswork.

### `access.beginRecovery`
Always exposes a neutral acknowledgement independent of account existence. Backend owns one-time proof, rate limiting, expiry and abuse monitoring.

### `access.resolveRecoveryLink`
Server-validates the proof received through browser/app routing. Links never contain an access/session token.

### `access.resetPassword`
Consumes a validated recovery context and replaces the credential. Session consequences and security notification are backend-owned.

### `access.beginProviderAuthentication`
Creates short-lived provider transaction state including PKCE/nonce/state as applicable and exact allowed redirect context.

### `access.completeProviderAuthentication`
Server validates provider result/issuer/audience/signature/nonce/transaction binding and returns existing account, new account, link required, cancelled or provider failure. Provider email alone is not silent-link authority.

### `access.authorizeAccountLink`
Requires proof of control of the existing DANTE account before mutation. No silent merge. Mutation must be auditable and replay-safe.

### `access.refreshSession`
If public mobile refresh tokens exist, design must detect token replay using sender-constraining or refresh-token rotation consistent with current OAuth BCP.

### `access.reauthenticate`
Restores/steps-up an expired or sensitive session context through an accepted remote-auth path. Local biometrics alone are not remote identity proof unless later cryptographically bound by an explicit design.

### `access.logoutCurrentSession`
Revokes server-side authority; deleting local UI state alone is insufficient.

Architecture must remain compatible with future `logoutAllSessions` / user-visible device-session revocation.

## 5. Password V1 policy

Approved V1 policy:

```text
minimum                      12 characters
maximum supported            >=64 characters
mandatory composition        none
paste/password managers      allowed
show/hide                    allowed
common-password blocklist    required server-side
breached-password blocklist  required server-side
forced periodic rotation     no, absent compromise/risk event
```

`12+` is a deliberate DANTE choice. It must not be represented as meeting the current NIST 15-character password-only baseline. A3.4's archived 15+ copy remains historical; M1.2/shared locales are implementation authority.

## 6. Provider/OAuth security

Native provider auth must use provider/platform-supported external user-agent / Authentication Services behavior; no embedded credential WebView.

Required:

- Authorization Code + PKCE for public native OAuth where applicable;
- transaction-specific state and nonce where applicable;
- exact redirect validation;
- short-lived provider transaction state;
- server-side provider assertion/token validation;
- cancellation distinguished from failure;
- provider completion never equals canonical DANTE account mutation until backend validation succeeds;
- Google/Apple authentication is separate from later data authorization.

## 7. Deep-link contract

Security-sensitive continuation uses DANTE-owned HTTPS URLs with verified platform association:

- iOS Universal Links / Associated Domains;
- Android Verified App Links / Digital Asset Links;
- browser fallback where the flow supports it.

Server proof validation remains authoritative regardless of which client opens the URL. Test cold start, foreground, background, app absent, expired, consumed, malformed/tampered, offline and outdated-client cases.

## 8. Session lifecycle

Backend must support documented inactivity/absolute lifetime policy, authoritative bootstrap, rotation after authentication/material reauth, current-session revocation, safe credential-change consequences, account disable/delete revocation, sensitive-change reauth and future session/device visibility.

Cancelling session-expired reauth returns to signed-out Access; it must not reactivate stale authenticated UI.

Secrets never go to URL, clipboard by default, generic preferences, analytics or crash breadcrumbs.

## 9. Local storage and lifecycle

Never generically persist:

- password;
- OTP;
- authorization code;
- PKCE verifier;
- provider token/assertion;
- recovery proof;
- access/refresh/session secret outside the selected platform-protected mechanism.

Process death/background resume may persist only the minimum safe continuation metadata. Production implementation must verify Keychain/Android protected storage behavior on real devices.

## 10. Failure taxonomy

UI/backend must distinguish at least:

```text
invalid credentials
throttled / temporarily limited
challenge invalid / expired / consumed / superseded
provider cancelled
provider failed
account link required
session expired / revoked / replay detected
transport offline / timeout
service unavailable
```

Offline/transport errors must never masquerade as wrong credentials. Public registration/recovery failures remain enumeration-resistant.

## 11. Abuse and privacy

Mandatory threat coverage:

- credential stuffing/distributed brute force;
- account enumeration;
- OTP guessing/resend abuse;
- recovery theft/replay;
- OAuth state/nonce/PKCE/redirect attacks;
- authorization-code and refresh-token replay;
- account-link takeover;
- session hijack/stale session;
- deep-link interception/tampering;
- malicious/tampered clients and compromised devices;
- process-death secret leakage;
- credential/provider-factor mutation;
- account disable/delete with stale sessions;
- logging/analytics/crash leakage.

Adaptive challenge/CAPTCHA friction, if required later, is risk-sensitive rather than forced on every normal sign-in.

## 12. Native integrity and network hardening gates

Play Integrity and App Attest may be used as defense-in-depth risk signals for selected high-abuse/high-impact operations. They are never identity/AuthZ and require degraded/unavailable handling. Android protected requests should bind relevant request content (for example request hash semantics) when that mechanism is adopted.

For DANTE-controlled API endpoints, production mobile must evaluate endpoint identity pinning against the selected MAS testing profile/risk target. If adopted, require backup material, rotation and break-glass procedures. Never pin third-party provider domains DANTE does not control.

## 13. Accessibility and native release gates

The HTML oracle can validate layout intent only. Before release the implemented clients must verify:

- VoiceOver/TalkBack semantics and focus order;
- Dynamic Type / Android font scaling;
- real IME/keyboard behavior;
- real password-manager/AutoFill/OTP integration;
- Android predictive Back;
- process death/background/cold start;
- Universal/App Links;
- provider SDK callbacks;
- secure storage;
- real-device iOS/Android regression.

## 14. Assurance target

Native clients target relevant **OWASP MASVS v2 controls** and current MAS Testing Profiles, including L2-profile testing where applicable to the Access threat surface. Do not claim a nonexistent modern “MASVS L2 certification.”

Future backend Access targets **OWASP ASVS 5.0.0 Level 2 alignment with an explicit exception register**. Current V1 does not mandate MFA/passkeys for every account; therefore MFA-related ASVS requirements must be recorded as explicit exceptions until an accepted mechanism exists, with compensating controls and passkey/MFA-ready architecture.

## 15. Implementation decisions intentionally open

Open until engineering gates:

- React Native vs native vs other client stack;
- router/state/forms libraries;
- API paths and versioning;
- DTO/class names;
- token/session representation;
- cookie vs token strategy for web;
- secure-storage abstraction;
- password hashing algorithm parameters/rehash policy;
- email/OTP provider and exact lifetimes;
- Google/Apple SDK/library versions;
- exact domains for Universal/App Links;
- pinning/attestation enforcement thresholds;
- passkey/MFA rollout.

Those choices must satisfy this contract and must not redefine the product flow merely because a library makes another flow easier.

## 16. Freeze / reopen rule

PRG-0 result: **PASS — production-ready specification / pre-implementation**.

Ordinary implementation does not reopen Access product design. Reopen only for a material platform/standard change, discovered security defect, backend impossibility/safety conflict, real-device accessibility/usability failure, provider-policy requirement or accepted DANTE semantic change.
