# DANTE Access — pre-production contract

- Status: **APPROVED REVIEW CONTRACT / PRE-PRODUCTION**
- Selected checkpoint: **A3.4**
- Selected artifact SHA-256: `b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6`
- Branch: `prototype/access-system`

## Purpose

Access gets a person from an unauthenticated entry point to an authenticated DANTE session and then, for a new account, through the smallest useful first-run handoff. It must feel like part of DANTE rather than a generic auth template.

## Product boundaries

Access is an account/security boundary, not a profile questionnaire and not an integration-permission screen.

Keep these distinctions explicit:

```text
Person != Account != Principal != Actor
sign-in != external-integration authorization
provider state != canonical DANTE state
```

Google/Apple sign-in may authenticate an account; it must not imply permission to read Calendar, Gmail, iCloud or unrelated provider data. Any later integration requires a separate explicit authorization flow.

## Selected visual system

A3.4 uses:

- warm light canvas and elevated warm-white Access surface;
- locked vector DANTE symbol + wordmark in the top bar;
- desktop-only large cropped locked Living Orbits symbol at low-but-visible opacity on the left brand stage;
- one focused Access column on the right;
- charcoal primary action, orange brand/focus accent;
- no mascot and no decorative fake-provider branding;
- mobile removes the desktop brand stage and keeps the Access surface primary.

A3.5 full-opacity corner mark is rejected. A3.1 remains the prior approved restore point.

## Screen/state inventory

| Technical ID | Prototype screen | Role |
|---|---|---|
| `access.signIn` | `signin` | Existing-account access through Google, Apple or email/password. |
| `access.signUpEmail` | `signup` | Start DANTE-owned registration with email. |
| `access.signUpPassword` | `signup-password` | Choose the account password after a valid email. |
| `access.verifyEmail` | `verify` | Six-digit email verification UX. |
| `access.forgotPassword` | `forgot` | Start neutral recovery flow. |
| `access.recoverySent` | `recovery-sent` | Neutral acknowledgement that does not reveal account existence. |
| `access.resetPassword` | `reset` | Enter and confirm a new password from recovery context. |
| `access.resetComplete` | `reset-done` | Recovery completion; return to normal sign-in. |
| `access.providerPending` | `provider` | DANTE-side provider launch/wait state only. |
| `access.providerError` | `provider-error` | Provider cancellation/failure return state. |
| `access.accountLink` | `link` | Existing-account collision/linking UX; no silent merge. |
| `access.reauth` | overlay `reauth` | Session-expired re-auth while preserving current context where safe. |
| `access.setupName` | `setup-name` | Lightweight preferred-name setup after account creation. |
| `access.setupLocale` | `setup-locale` | Confirm language and time zone. |
| `access.setupStart` | `setup-start` | Choose first-run path without making the choice permanent. |
| `access.firstAction` | `first-action` | Create a first real event/activity/routine/goal. |
| `access.import` | `import` | Separate import choice; not implied by provider sign-in. |
| `access.demo` | `demo` | Tutorial-only demonstration, isolated from real history. |
| `access.homeHandoff` | `home` | Prototype handoff after setup; not the canonical Home implementation. |

## DANTE-owned email/password signup

Reviewed sequence:

```text
email
→ password
→ verify email
→ account ready
→ lightweight setup
```

The first account-creation screen does not ask for name, lifestyle, goals, health information or other profile enrichment.

A3.4 currently presents `15+` characters as the reviewed password-length guidance. This is a prototype/security UX decision informed by current NIST guidance; it is **not** a frozen backend password contract. Production backend/security may supersede the exact enforcement rule while preserving password-manager, paste/show-hide and long-password-friendly behavior.

## Provider behavior

DANTE owns only:

- launch affordance;
- pending/wait feedback;
- cancellation/failure return;
- account-collision/linking UX;
- authenticated return destination.

DANTE must not fake the provider-owned account chooser or consent screen. Production Google/Apple buttons/marks must follow the provider's current official integration/branding guidance.

## Recovery/security behavior

- recovery acknowledgement remains generic whether or not the address exists;
- email recovery link/token semantics remain backend/security-owned;
- reset does not silently auto-login in this checkpoint;
- account collision never silently merges identities;
- re-auth is distinct from full sign-in because application context may already exist.

## First-run boundary

After successful account creation, Access can collect only a lightweight operational baseline before entering the product. Deeper profile information remains progressive/contextual. The available first-run choices remain:

- create a first real item;
- import existing material;
- run an isolated demo;
- skip and explore Home.

These follow current product onboarding/first-run specifications on `main` and do not redefine their domain semantics.

## Localization

A3.4 has complete Italian/English prototype dictionaries. The accepted strings are mirrored under the `access.*` namespace in the shared locale registry for future production migration. Visible wording can change without renaming technical IDs.

## Brand provenance

No logo/wordmark is typed or reconstructed. A3.4 embeds geometry from the locked symbol and wordmark masters. The large corner mark is a visual treatment of the locked symbol, not a new brand master.

## Production migration boundary

When the production frontend begins, migrate the contract/state IDs, locale keys and semantic roles; do not mechanically preserve prototype DOM structure. Real React/router/form/auth-provider choices remain a separate engineering scope.
