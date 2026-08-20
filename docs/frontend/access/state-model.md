# DANTE Access — state model

- Status: **A3.4 approved review state model**
- Production/backend semantics: **not frozen**

## Primary state graph

```text
SIGN_IN
├─ provider → PROVIDER_PENDING → authenticated return | PROVIDER_ERROR | ACCOUNT_LINK
├─ email/password → authenticated return
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
→ RESET_PASSWORD
→ RESET_COMPLETE
→ SIGN_IN

SESSION_EXPIRED
→ REAUTH overlay
→ restore current destination/context when safe
```

## Review-state identifiers

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
reauth (overlay)
```

## State rules

- a provider pending state is not a provider chooser/consent clone;
- cancellation/failure returns control to DANTE without claiming account mutation;
- provider collision requires secure existing-account reauthentication before any eventual link;
- email verification is distinct from account/profile setup;
- recovery copy is neutral to account existence;
- setup can be lightweight and optional except for genuinely required operational/account data;
- demo content never becomes real history unless explicitly converted later;
- the `home` review state is only a handoff mock and must not replace the accepted Home artifact.

## Prototype fixtures

The review HTML is intentionally self-contained and uses local-only simulated interactions. It must not be read as proof of API endpoints, database schema, token lifetime, OTP implementation, provider linking policy or session persistence.
