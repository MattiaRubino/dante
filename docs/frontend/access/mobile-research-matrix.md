# DANTE — Mobile Access research matrix

Status: **APPROVED RESEARCH EVIDENCE / PRG-0 SUPPORT**  
Date: 2026-08-20

This file records the external/platform evidence used to constrain Mobile Access. Standards are assurance constraints; competitor/product examples are pattern evidence only and never become DANTE requirements by default.

| Authority / evidence | Relevant direction | DANTE consequence |
|---|---|---|
| IETF RFC 8252 | Native OAuth uses an external user-agent; public clients use PKCE. | No embedded credential WebView; native provider flow + Authorization Code/PKCE where applicable. |
| IETF RFC 9700 | Current OAuth security BCP; public-client refresh tokens need replay protection. | If mobile refresh tokens are issued, use sender-constraining or refresh-token rotation; strict redirect/transaction validation. |
| NIST SP 800-63B | Long/password-manager-friendly passwords; block common/compromised values; no arbitrary composition checklist; password-only baseline currently favors 15+. | DANTE keeps password managers/paste and breached/common blocklists. V1's 12+ choice is explicitly documented as more permissive than the NIST password-only baseline. |
| OWASP ASVS 5.0.0 | Modern server/application verification baseline; L2 is appropriate target for most applications. | Future AuthN backend targets ASVS 5.0.0 L2 alignment with explicit exception register, never false compliance claims. |
| OWASP MASVS v2 + MAS Testing Profiles | Modern mobile controls no longer use the old formal MASVS L1/L2 verification labels. | Cover relevant MASVS controls and use current testing profiles, including L2-profile tests where applicable. |
| OWASP Authentication/Forgot Password guidance | Resist enumeration; recovery tokens are sensitive; throttle abuse. | Generic public recovery/registration behavior, server-owned proof expiry/single-use/rate limits. |
| Android Credential Manager / Google Identity | Modern unified credential surface; authentication and Google-data authorization are distinct. | Evaluate Credential Manager for production Android; login never grants Calendar/Gmail/Drive permissions. |
| Android Verified App Links | Verified HTTPS association routes owned domains to the app. | Verification/recovery use owned HTTPS + App Links, with browser fallback where supported. |
| Android edge-to-edge / WindowInsets | Modern Android requires correct system-bar/cutout/IME handling. | Mobile shell is inset/keyboard safe; no desktop scaling. |
| Android accessibility | Effective interactive targets around 48×48 dp and accessible semantics. | All Android review controls hardened to >=48×48 effective targets; real TalkBack remains release gate. |
| Android Predictive Back | Back is OS navigation, increasingly predictive. | Map back to the logical Access state graph, not arbitrary component history. |
| Sign in with Apple / Authentication Services | Provider-owned native auth, server validation and transaction binding. | Use official flow; no fake Apple chooser; server validates result; no silent account merge from email alone. |
| Apple AutoFill content types | Username/email/password/new-password/one-time-code semantics enable native AutoFill. | Production inputs expose native semantics; OTP is one semantic code even if visually segmented. |
| Apple Universal Links / Associated Domains | Owned HTTPS links can securely associate website and app. | Recovery/verification use Universal Links on iOS; server remains proof authority. |
| Apple LocalAuthentication | Face ID/Touch ID authenticate locally under device policy. | Optional local unlock/step-up convenience; not automatically remote DANTE identity proof. |
| Play Integrity / App Attest | App/device integrity can inform server risk decisions. | Defense-in-depth only for selected high-abuse/high-impact operations; never identity/AuthZ; degraded path required. |
| Android Network Security Config / Apple ATS | Platforms provide transport-trust controls; pinning has operational cost. | TLS-only. Evaluate pinning for DANTE-owned endpoints under risk/testing profile with backup/rotation/break-glass; never pin third-party providers. |

## Mature-product pattern conclusions

Across mature authentication products, the reusable pattern is behavioral rather than visual:

- one obvious entry route;
- provider-owned authentication surfaces;
- staged email/password registration instead of one large form;
- short verification state;
- neutral recovery acknowledgement;
- consistent language/loading/error treatment;
- short progressive first-run;
- password manager/AutoFill/native Back treated as product behavior rather than afterthoughts.

DANTE deliberately does **not** clone another product's visual identity or undocumented backend behavior.

## Locked requirement candidates from evidence

- one semantic Access state model across web/iOS/Android;
- no embedded OAuth credential WebView;
- PKCE/transaction binding/strict redirect validation where protocol applies;
- authentication separate from provider-data authorization;
- verified owned HTTPS deep links;
- server-side rate limiting/abuse controls;
- secure session storage/revocation semantics;
- no local password persistence;
- password manager/AutoFill/paste support;
- no mandatory upper/lower/number/symbol composition checklist;
- server-side common/breached-password rejection;
- safe-area/IME/system Back/accessibility support;
- comprehensive failure/lifecycle testing.

## Intentional implementation deferrals

Evidence does not select:

- React Native/native/Flutter;
- concrete API routes or DTOs;
- JWT vs opaque token;
- exact access/refresh lifetimes;
- exact secure-storage wrapper;
- exact provider SDK versions;
- sender-constrained token vs refresh-token rotation implementation;
- exact password hashing parameters;
- exact attestation/pinning enforcement threshold;
- passkey/MFA rollout date.

Those remain engineering/security decisions constrained by the approved Access contract.
