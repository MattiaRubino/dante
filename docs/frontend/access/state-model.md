# DANTE Access — cross-platform state model

- Status: **APPROVED / PRG-0 PASS / PRE-IMPLEMENTATION**
- Desktop oracle: **A3.4**
- Mobile oracle: **M1.2 + PRG-0**

## Primary semantic graph

```text
SIGN_IN
├─ provider → PROVIDER_PENDING → AUTHENTICATED_RETURN | PROVIDER_ERROR | ACCOUNT_LINK
├─ email/password → AUTHENTICATED_RETURN
├─ create account → SIGN_UP_EMAIL
└─ forgot password → FORGOT_PASSWORD

SIGN_UP_EMAIL
→ SIGN_UP_PASSWORD
→ VERIFY_EMAIL
→ SETUP_NAME
→ SETUP_LOCALE
→ SETUP_START
   ├─ FIRST_ACTION → HOME_HANDOFF
   ├─ IMPORT → HOME_HANDOFF
   ├─ DEMO → HOME_HANDOFF
   └─ skip → HOME_HANDOFF

FORGOT_PASSWORD
→ RECOVERY_SENT
→ recovery proof/link
→ RESET_PASSWORD
→ RESET_COMPLETE
→ SIGN_IN

SESSION_EXPIRED / SECURITY_REAUTH_REQUIRED
→ REAUTH
→ success: restore only safe valid context
→ cancel/cannot continue: SIGN_IN
```

## Stable review/state identifiers

```text
signin
signup
signup-password
verify
forgot
recovery-sent
reset
reset-done
provider
provider-error
link
setup-name
setup-locale
setup-start
first-action
import
demo
home
reauth (dialog/overlay)
```

Visible wording and platform representation may change without renaming these semantic roles unless the underlying meaning changes.

## Orthogonal conditions

The following are **not** new canonical account states. They layer over a current state and affect which transitions are safe:

```text
OFFLINE / REACHABILITY_FAILURE
REQUEST_IN_FLIGHT
RATE_LIMITED
SERVER_UNAVAILABLE
APP_BACKGROUND
APP_COLD_START
PROVIDER_EXTERNAL_UI_ACTIVE
SECURITY_REAUTH_REQUIRED
```

For example, offline on `SIGN_IN` remains `SIGN_IN`; the transport-dependent action is blocked and the UI exposes a transport condition rather than inventing an invalid-credential result.

## Mobile navigation rules

System back / visible back follows the logical state graph, not raw screen order or DOM history.

Priority:

1. dismiss a safe transient surface;
2. return to the previous valid Access state;
3. never reveal expired authenticated context;
4. never imply success for an incomplete provider/credential mutation;
5. at Access root, defer to normal OS navigation behavior.

Predictive Back on Android must map to the same semantic destination as the visible back action.

## Provider transaction rules

`PROVIDER_PENDING` means only that DANTE initiated provider-owned authentication. It is not evidence of canonical DANTE identity mutation.

Required transaction semantics:

```text
begin provider auth
→ bind short-lived transaction/context
→ external provider UI
→ callback/return
→ validate transaction + provider result server-side
→ success | cancellation | provider failure | identity collision
```

A provider collision can enter `ACCOUNT_LINK`, but the link is not complete until control of the existing DANTE account is securely proven and the backend authoritatively commits the link.

## Verification / recovery rules

- verification is distinct from profile/setup;
- recovery start is neutral to account existence;
- proof invalid / expired / consumed / superseded states must be representable;
- resend/cooldown/attempt semantics are server-owned;
- security-sensitive link handling does not make a URL valid merely because the app opened it.

## Session rules

`AUTHENTICATED_RETURN` is only valid after backend-authoritative session establishment/validation.

Session bootstrap must be able to resolve at least:

```text
authenticated
unauthenticated
expired
revoked
security reauth required
```

An expired/revoked session cannot be restored by dismissing a reauth surface.

## App lifecycle / resume

On process death, cold start or background resume, the client may restore only the minimum safe continuation metadata necessary to reconstruct a valid flow.

Never generically persist:

- password;
- OTP;
- recovery proof/token;
- OAuth authorization code;
- PKCE verifier;
- provider token/assertion;
- access/refresh/session secret outside the approved secure-storage/session design.

The backend remains authoritative after resume.

## First-run state rules

- setup occurs after account readiness;
- setup is lightweight/progressive;
- demo content is isolated from real history;
- `home` is a prototype handoff state only and never replaces canonical Home;
- skipping first-run guidance does not imply missing profile facts are false.

## Cross-platform invariant

```text
same semantic outcome
+ platform-native representation
!= pixel-identical interaction
```

Web/iOS/Android may differ in provider ordering, keyboard/AutoFill behavior, safe-area/inset handling, navigation animation and system-owned surfaces while preserving the same semantic state transitions and backend outcomes.

## Detailed implementation contract

See `docs/frontend/access/mobile-technical-contract.md` for capability outcomes, deep-link behavior, session/security requirements, error taxonomy, lifecycle and production release gates.
