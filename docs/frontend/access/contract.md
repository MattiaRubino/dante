# DANTE Access — cross-platform pre-implementation contract

- Status: **APPROVED PRODUCTION-READY SPECIFICATION / PRG-0 PASS / PRE-IMPLEMENTATION**
- Desktop selected checkpoint: **A3.4**
- Mobile selected checkpoint: **M1.2 + PRG-0**
- Branch: `prototype/access-system`

## Purpose

Access gets a person from an unauthenticated entry point to an authenticated DANTE session and, for a new account, through the smallest useful first-run handoff. Web, iOS and Android are different representations of the same semantic Access system.

This contract is implementation input. It is not production React/mobile code and it does not freeze HTTP routes, DTOs, DB schema, token shape or framework choice.

## Product invariants

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
provider authentication != permission to read provider data
verification != profile setup
reauthentication != initial sign-in
client integrity != person identity
```

Google/Apple sign-in can authenticate a DANTE account. It must never imply permission to read Calendar, Gmail, iCloud or unrelated provider data. Those permissions require a separate explicit integration-authorization flow.

## Visual authorities

### Desktop / web review authority

A3.4 remains the desktop visual/behavior oracle:

```text
size     93897 bytes
SHA-256  b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6
```

Its large muted Living Orbits corner treatment is desktop-only. A3.5 full-opacity treatment remains rejected.

### Mobile review authority

M1.2 + PRG-0 is the mobile visual/behavior oracle:

```text
size     107010 bytes
SHA-256  2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676
```

Mobile is not a scaled-down desktop. It uses a full-screen phone expression, safe-area/IME-aware layout, platform-appropriate provider order/behavior, large touch targets and a compact brand treatment without the desktop brand stage.

## Semantic screen/state inventory

| Technical ID | Review state | Contract |
|---|---|---|
| `access.signIn` | `signin` | Existing-account access through provider or email/password. |
| `access.signUpEmail` | `signup` | Start DANTE-owned registration with email. |
| `access.signUpPassword` | `signup-password` | Choose account password after valid email. |
| `access.verifyEmail` | `verify` | Verify email challenge. |
| `access.forgotPassword` | `forgot` | Start neutral recovery. |
| `access.recoverySent` | `recovery-sent` | Neutral acknowledgement; no account-existence leak. |
| `access.resetPassword` | `reset` | Replace password from valid recovery context. |
| `access.resetComplete` | `reset-done` | Recovery completion; return toward sign-in. |
| `access.providerPending` | `provider` | DANTE-side provider launch/wait state only. |
| `access.providerError` | `provider-error` | Provider cancel/failure return. |
| `access.accountLink` | `link` | Identity collision/linking path; no silent merge. |
| `access.reauth` | `reauth` overlay/dialog | Reauthenticate expired/security-sensitive session context. |
| `access.setupName` | `setup-name` | Lightweight preferred-name setup after account creation. |
| `access.setupLocale` | `setup-locale` | Confirm language/time zone. |
| `access.setupStart` | `setup-start` | Choose first-run path without making it permanent. |
| `access.firstAction` | `first-action` | Create first real item. |
| `access.import` | `import` | Separate import route; not implied by provider sign-in. |
| `access.demo` | `demo` | Tutorial-only demonstration isolated from real history. |
| `access.homeHandoff` | `home` | Access completion mock/handoff; not canonical Home implementation. |

The generic state graph remains in `docs/frontend/access/state-model.md`; mobile lifecycle/security detail lives in `mobile-technical-contract.md`.

## DANTE-owned email/password signup

Approved semantic sequence:

```text
email
→ password
→ verify email
→ account ready
→ lightweight setup
```

No name, lifestyle, goals, health profile or broad questionnaire is required before account creation.

### Password V1 policy

```text
minimum                    12 characters
support                    >=64 characters
mandatory composition      none
paste/password manager     allowed
show/hide                   allowed
common/breached blocklist  required server-side
```

The 12-character policy is a deliberate DANTE decision and is not represented as compliance with the current NIST 15-character password-only baseline. A3.4's immutable archive retains the earlier 15+ review copy as historical evidence; Mobile M1.2 and shared production-migration locales supersede it for implementation.

## Provider authentication

DANTE owns only:

- provider launch affordance;
- transaction/context binding;
- pending/wait feedback;
- cancellation/failure return;
- provider-result validation handoff to backend;
- account-collision/linking UX;
- authenticated return destination.

DANTE does not fake provider-owned chooser/consent UI and does not collect Google/Apple credentials inside a DANTE embedded WebView.

Native public-client OAuth uses the provider/platform-supported external-user-agent path and Authorization Code + PKCE where applicable. Callback/redirects are exact-validated and provider assertions are validated server-side.

## Account linking

An existing-account collision must not silently merge identities based on email or provider UI completion.

Required semantic rule:

```text
collision
→ prove control of existing DANTE account
→ explicit link decision
→ backend-authoritative link
```

Provider link/unlink is security-sensitive and must not silently remove the account's last viable authentication path.

## Recovery / verification

- recovery start response remains neutral to account existence;
- verification/recovery proofs are backend-owned, short-lived and replay/single-use aware;
- invalid / expired / consumed / superseded states are distinguishable internally;
- resend cooldown/abuse controls are server-owned;
- reset does not imply an unsafe automatic authenticated session unless later explicitly designed;
- security-sensitive links use owned HTTPS + verified platform association.

## Session / reauthentication

The backend remains authoritative for session validity.

Required capabilities include:

- authenticated / unauthenticated / expired / revoked bootstrap;
- rotation after authentication/material reauthentication;
- inactivity and absolute lifetime policy;
- current-session revocation;
- safe credential-change/session consequences;
- sensitive-account-change reauthentication;
- account disable/delete invalidating active sessions;
- replay-resistant refresh design if refresh tokens exist;
- future user-visible session/device revocation capability.

Cancelling an expired-session reauth must return to signed-out Access rather than restore interactive access to stale authenticated context.

## Mobile platform contract

Shared semantic result; platform-native expression.

### Android

- edge-to-edge/system insets/IME respected;
- effective interactive targets >=48×48 dp for Access controls;
- system/predictive back follows the logical Access state graph;
- evaluate modern Credential Manager / provider integration at implementation;
- use Verified App Links for owned HTTPS security-sensitive continuation;
- evaluate Play Integrity as risk/abuse signal where justified.

### iOS

- safe areas/keyboard/Dynamic Type respected;
- platform AutoFill content types for email/username/password/new password/one-time code;
- Sign in with Apple through Authentication Services/provider-owned UI;
- use Universal Links / Associated Domains for owned HTTPS continuation;
- evaluate App Attest as risk/abuse signal where justified.

### Both

- password managers and paste are first-class behavior;
- no generic persistence of password/OTP/provider/recovery secrets;
- VoiceOver/TalkBack and large-text behavior are release gates;
- process death/background/cold-start continuation stores only minimum safe metadata;
- offline/transport failures never masquerade as invalid credentials.

## Deep-link contract

Security-sensitive continuation uses DANTE-owned HTTPS links with verified app/domain association. Server proof validation remains authoritative regardless of browser/app routing.

Custom URI schemes, if later used at all, are secondary and never the sole security boundary.

## Network / app integrity

Production transport is TLS-only.

Endpoint pinning for DANTE-controlled native API endpoints is a production assurance decision constrained by MASVS/testing-profile requirements and operational safety. If adopted it requires backup material, rotation and break-glass procedures; third-party provider domains are not pinned by DANTE.

Play Integrity/App Attest may be used as defense-in-depth risk signals for selected high-abuse/high-impact operations. Integrity verdicts are never person identity or authorization and require safe degraded/unavailable handling.

## Abuse / privacy

Backend implementation must cover credential stuffing/brute force, enumeration, OTP/recovery abuse, provider transaction attacks, replay, account-link takeover and session hijack.

Do not log/persist raw password, OTP, recovery proof, authorization code, PKCE verifier, access/refresh/session secret or provider token/assertion.

## First-run boundary

After account creation, Access may collect only a lightweight operational baseline. Deeper personal profiling remains progressive/contextual.

First-run choices remain:

- create a first real item;
- import existing material;
- run an isolated demo;
- skip and explore Home.

Demo data must not contaminate canonical real history.

## Localization

The durable shared namespace is `access.*` in:

- `prototypes/frontend/shared/locales/it-IT.json`
- `prototypes/frontend/shared/locales/en-US.json`

M1.2 has 128 Access keys per locale with exact IT/EN parity. The shared locale registry also preserves the existing Home keys unchanged.

## Assurance / readiness

Read:

- `docs/frontend/access/mobile-technical-contract.md`
- `docs/frontend/access/mobile-research-matrix.md`
- `docs/frontend/access/mobile-production-readiness.md`
- `docs/frontend/access/mobile-qa.md`

PRG-0 targets relevant OWASP MASVS v2 controls + current MAS testing profiles for native clients and OWASP ASVS 5.0.0 Level-2 alignment for backend Access with an explicit exception register rather than false compliance claims.

## Production migration boundary

Production implementation migrates:

- semantic state IDs;
- copy/localization keys;
- behavior/capability contract;
- security/session/deep-link/provider invariants;
- acceptance/release gates.

It does **not** mechanically preserve prototype DOM structure.

Implementation choices still open include React/mobile framework, router/forms/state libraries, API route names, DTOs, token representation, secure-storage wrapper, provider library versions and exact session/challenge lifetimes.

Those choices must satisfy this contract. They must not redefine Access merely because a library makes another flow easier.

## Reopen rule

After PRG-0, ordinary implementation does not reopen Access product design. Reopen only for material platform/standard changes, discovered security defects, backend impossibility/safety conflicts, real-device accessibility/usability failures, provider-policy requirements or accepted DANTE semantic changes.
