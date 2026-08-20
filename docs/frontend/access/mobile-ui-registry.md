# DANTE Access — Mobile UI / behavior registry

Status: **ACTIVE PRE-IMPLEMENTATION REGISTRY / M1.2 + PRG-0**  
Parent registry: `docs/frontend/ui-registry.md`  
Contract: `docs/frontend/access/contract.md`

The global Access semantic IDs remain those already registered in `docs/frontend/ui-registry.md`. Mobile does not fork those meanings. This file registers mobile-specific representation/behavior that does not warrant new product-state IDs.

| Technical ID | Status | Mobile behavior / contract |
|---|---|---|
| `access.mobile.shell` | ACTIVE / PRE-IMPLEMENTATION | Full-screen phone Access expression; not a scaled desktop panel. Safe-area/inset/IME-aware. |
| `access.mobile.providerOrder` | ACTIVE / PLATFORM-ADAPTIVE | iOS may prioritize Apple and Android may prioritize Google; semantic provider capability remains unchanged. |
| `access.mobile.systemBack` | ACTIVE / PRE-IMPLEMENTATION | OS back/predictive back maps to logical Access state graph and must never reveal expired authenticated context. |
| `access.mobile.networkStatus` | ACTIVE / PRE-IMPLEMENTATION | Non-modal offline/transport status layered over current Access state; not an invalid-credential state. |
| `access.mobile.autofill` | ACTIVE / PRE-IMPLEMENTATION | Correct platform semantics for email/username/current password/new password/one-time code; password managers and paste supported. |
| `access.mobile.deepLink` | ACTIVE / PRE-IMPLEMENTATION | DANTE-owned HTTPS continuation through Universal Links / Verified App Links; server proof remains authoritative. |
| `access.mobile.reauthDialog` | ACTIVE / PRE-IMPLEMENTATION | Security-sensitive reauth dialog; password marked current-password; cancel returns to signed-out Access when session is expired. |
| `access.mobile.touchTargets` | ACTIVE / PRE-IMPLEMENTATION | Android review expression uses >=48×48 dp effective targets; iOS uses platform-appropriate large hit areas. |
| `access.mobile.textScaling` | ACTIVE / PRE-IMPLEMENTATION | Layout must survive large system text without hidden/clipped critical actions or horizontal scrolling. |
| `access.mobile.lifecycle` | ACTIVE / PRE-IMPLEMENTATION | Process death/background/cold-start restores only safe continuation metadata; secret auth material is not generically persisted. |
| `access.mobile.integritySignal` | IMPLEMENTATION GATE | Play Integrity/App Attest may harden selected high-risk actions as risk signals; never identity/AuthZ. |
| `access.mobile.endpointPinning` | IMPLEMENTATION GATE | DANTE-controlled endpoint pinning evaluated/implemented per selected MAS profile/risk target with backup/rotation/break-glass readiness. |

## Shared semantic-state note

The following global IDs are reused unchanged on mobile:

`access.signIn`, `access.signUpEmail`, `access.signUpPassword`, `access.verifyEmail`, `access.forgotPassword`, `access.recoverySent`, `access.resetPassword`, `access.resetComplete`, `access.providerPending`, `access.providerError`, `access.accountLink`, `access.reauth`, `access.setupName`, `access.setupLocale`, `access.setupStart`, `access.firstAction`, `access.import`, `access.demo`, `access.homeHandoff`, `access.localeSelector`.

## Explicit exclusions

Mobile representation must not introduce:

- a second semantic auth state model;
- provider-data permission bundled into login;
- silent identity merge;
- device-integrity verdict as authorization;
- password/OTP/recovery/provider secrets in generic persistence;
- a custom WebView that collects Google/Apple credentials;
- a mobile-only reinterpretation of first-run/domain semantics.
