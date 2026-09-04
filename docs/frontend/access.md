# DANTE — Access Web Contract

- **Status:** CURRENT / AUTHORITATIVE FOR BRANCH-LOCAL ACCESS WEB
- **Last reconciled:** 2026-09-03
- **Branch:** `feature/access-auth`
- **Architecture:** `../architecture/access-auth-architecture.md`
- **Security:** `../architecture/access-auth-security-contract.md`
- **M5:** `../architecture/access-auth-m5-contract.md`
- **Current workstream:** `../workstreams/access-auth.md`
- **Email Platform:** `../architecture/email-platform.md`
- **Real Email evidence:** `../development/email-platform-acceptance-2026-09-03.md`

## 1. Purpose

Access moves an unauthenticated person through real DANTE authentication/account lifecycle into a server-authoritative AuthSession. The same product boundary supports password, Google, Apple and passkeys without creating parallel Account/session authorities.

## 2. Permanent semantics

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
provider identity != provider email
provider authentication != provider-data authorization
verification != profile setup
reauthentication != initial signin
frontend/provider callback != backend-authoritative success
unknown/loading != signed-out
method != factor != assurance
```

## 3. Visual baseline

Preserve the accepted Access composition unless a real product defect requires change:

```text
warm open canvas
Living Orbits / DANTE brand stage
locked topbar
compact locale control
separate rounded Access card
responsive mobile-Web composition
```

Hero copy:

```text
IT  Comprendi la vita. / Dai forma al prossimo passo.
EN  Understand life. / Shape what comes next.
```

Provider controls use official provider interaction/branding rather than fake DANTE account-chooser UI.

## 4. Current runtime capability

Materialized and proved:

```text
email/password signin
critical session bootstrap
logout
signup initiation
six-digit email OTP verification/resend
neutral recovery initiation
memory-only recovery bearer + URL scrub
password reset + fresh signin
password reauthentication + bearer rotation
Google sign-in/link/reauth browser integration
Apple begin/continuation browser integration
provider enrollment + mailbox proof
provider link-required + explicit confirmation
passkey signin/register/reauth/rename/remove
password establish/remove
/security authenticator inventory/management
backend anti-lockout
IT/EN localization
```

This supersedes old statements that runtime ends at M4 or that M5 Web semantics are not materialized.

## 5. Application/transport ownership

```text
TanStack Router
→ navigation/bootstrap only

Access feature
→ product/application Auth behavior

TanStack Query
→ remote lifecycle only

Web Auth platform adapters
→ same-origin transport + Google/WebAuthn browser integration

@dante/api-client
→ governed generated wire contract

backend + PostgreSQL
→ canonical Auth truth
```

No presentation component may decide that Google/passkey/browser completion means DANTE authentication succeeded.

Email provider details are also not Web authority. Access UI triggers/consumes Auth lifecycle; the shared backend Email Platform owns durable delivery and provider interaction.

## 6. Session bootstrap and rotation

Hard document load resolves/prefetches `/auth/session` before the first business render. Unknown/loading is never painted as signed-out.

When a mutation creates/rotates/revokes AuthSession authority, the application boundary cancels the exact in-flight session query before committing the authoritative result to avoid stale read overwrite.

Web Auth state is process/query memory only; no session JWT/token goes to localStorage/sessionStorage/IndexedDB.

## 7. Password UX

```text
minimum                 15 Unicode code points
support                 >=64 characters
composition rules       none
paste/password managers first-class
show/hide               allowed
silent truncation       forbidden
compromised screening   server-side HIBP
periodic forced change  no absent security reason
```

Password is optional. Provider/passkey-created Accounts may add it later; it can be removed only when backend anti-lockout says the Account remains viable.

## 8. Google Web UX

Current flow:

```text
DANTE /google/begin
→ DANTE transaction + nonce
→ official Google Identity Services renderButton
→ real Google credential evidence
→ DANTE /google/complete
→ authenticated | enrollment_required | link_required | safe failure
```

Current browser adapter uses GIS `https://accounts.google.com/gsi/client`, `use_fedcm_for_button`, `auto_select=false` and `button_auto_select=false`.

Do not regress to a DANTE-drawn fake Google chooser or provider-token-as-session model.

The live Google UAT proved the third-party-mailbox path: Google identity proof succeeded, but DANTE still required direct mailbox proof before Account creation because Google was not authoritative for that mailbox.

## 9. Apple Web UX

```text
DANTE /apple/begin
→ redirect only to appleid.apple.com
→ Apple form_post/backend callback
→ server validation/exchange
→ fixed DANTE return target
```

No Apple transaction secret becomes JavaScript storage authority. Private Email Relay is respected; users choosing Hide My Email are not forced to disclose an unrelated “real” mailbox.

Real Apple registered-domain UAT remains open/deferred.

## 10. Passkey UX

```text
Use a passkey
→ browser/platform authenticator selector
→ navigator.credentials.get/create
→ backend FIDO2 verification
→ canonical DANTE AuthSession or credential mutation
```

Support discoverable username-less signin and multiple passkeys. DANTE does not build a fake authenticator chooser or claim that all user verification is biometric.

Live Windows Hello UAT proved registration, persistence, reauth and passwordless signin.

## 11. Security management

Current `/security` supports:

```text
current authenticator inventory
password present/absent
add/remove password
provider linked identities + link/unlink
passkey add/rename/remove
password/passkey/provider reauthentication where configured
recent-auth feedback
anti-lockout errors
```

Backend authority decides removals. Live UAT proved that removing a password is allowed when a passkey remains and removing the final remaining passkey is rejected.

## 12. Recovery

Public recovery remains anti-enumeration neutral.

```text
request
→ shared Email Platform durable intent
→ real email proof
→ one-use recovery bearer
→ create-or-replace PasswordCredential as applicable
→ revoke prior sessions
→ fresh signin required
→ password-reset security notification
```

Final real SES UAT on 2026-09-03 directly proved:

```text
recovery email received in a real mailbox
recovery link opened the DANTE reset surface
password reset succeeded
reset did not auto-login
previous authenticated session was revoked
password-change security notification arrived
```

The exact same consumed recovery link was not manually opened a second time in that final live run because the message had already been removed before that check. Do not label same-link replay rejection as manually observed evidence from this UAT.

## 13. Signup email verification

Final real SES UAT directly proved the normal password-signup browser path:

```text
Create account
→ DANTE signup challenge + durable EmailIntent
→ SES provider_accepted
→ real mailbox receives six-digit verification mail
→ user enters received code
→ verification succeeds
→ Account created
```

This replaces the old claim that signup/recovery Internet delivery was still open.

## 14. Accessibility / responsive quality

Release target remains WCAG 2.2 AA-quality behavior. Group-4 browser tests cover accessibility/keyboard/focus/responsive concerns across the canonical browser matrix. Provider/passkey native dialogs remain browser/platform-owned.

## 15. Current evidence

Automated product evidence:

```text
format/typecheck/lint/architecture PASS
Web unit/component PASS
Auth Playwright PASS across Chromium/Firefox/WebKit
```

Manual/real-boundary evidence:

```text
password/session/security-management PASS
Windows Hello passkey PASS
Google real-provider PASS
real SES signup verification PASS
real SES password recovery PASS
real SES reset-notification PASS
post-reset no-auto-login PASS
post-reset previous-session revocation PASS
PostgreSQL direct inspection PASS
```

Exact Email Platform live evidence: `../development/email-platform-acceptance-2026-09-03.md`.

## 16. Remaining product maturity

M7 should add session/device inventory, remote revoke, new-login/security-event response and final authenticated Home handoff. The large Security page should also be componentized by bounded responsibility without changing accepted semantics.

Production email sender-domain/DNS/reputation and live cloud-event routing are deployment/operations concerns, not reasons to reopen the Access Web recovery/signup implementation.

Current implementation/code/tests plus current workstream/status documents beat older pre-M5 phase labels.
