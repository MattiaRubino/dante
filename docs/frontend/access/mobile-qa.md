# DANTE Mobile Access M1.2 — QA / PRG-0 evidence

Status: **PASS FOR APPROVED PRODUCTION-READY SPECIFICATION / PRE-IMPLEMENTATION**  
Date: **2026-08-20**

Selected artifact:

```text
size     107010 bytes
SHA-256  2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676
```

## Executable browser baseline

The immediately preceding M1.2 artifact passed the executable Chromium review suite **30/30** before PRG-0. That suite covered:

- iPhone 393×852;
- Android 412×915;
- compact 360×800;
- reduced-height 393×520 keyboard stress viewport;
- simulated text scale 100%, 125%, 150%, 200%;
- zero horizontal overflow;
- Android effective interaction targets >=48×48 in the review expression;
- 11-char password blocked / 12-char password accepted and advanced;
- provider/password network-required transitions blocked while offline;
- reauth cancellation returned to signed-out Access;
- logical back-state handling;
- no LocalStorage/SessionStorage credential persistence.

## PRG-0 hardening delta

PRG-0 then made only bounded Access hardening changes:

- corrected internal review label from A3 to M1.2;
- changed password wording from recommendation language to the approved 12-character minimum;
- made forgot-email AutoFill semantics explicit;
- added explicit dialog semantics to reauthentication;
- made reauth password `current-password` and focus it on open;
- restored previous focus after successful reauth;
- made Escape use the security-safe reauth cancel path;
- fixed missing Italian offline dictionary keys discovered by locale-parity inspection.

No Home implementation, backend code, provider SDK, token/session implementation or brand master changed.

## PRG-0 static/mechanical revalidation

The final selected bytes pass **18/18** deterministic checks:

```text
duplicate IDs                              PASS (0)
declared Access screens                    PASS (18)
no stale 15+ password copy/threshold       PASS
12-character enforcement present           PASS
reauth dialog ARIA semantics               PASS
reauth current-password semantic           PASS
forgot-email AutoFill semantic             PASS
no generic credential persistence          PASS
current M1.2 debug label                    PASS
embedded locale object extractable         PASS
IT/EN embedded key parity                  PASS (128 / 128)
Italian offline keys complete              PASS
English offline keys complete              PASS
12+ password copy parity                   PASS
inline JavaScript syntax                    PASS
OTP one-time-code semantic                 PASS
password AutoFill semantic coverage        PASS
shared future locale parity                 PASS (146 / 146)
```

Machine-readable static QA: `prototypes/frontend/access/archive/mobile-m1-2-approved-2026-08-20/prg0-static-qa.json`.

## Browser rerun note

A fresh Chromium launch against the final PRG-0 bytes was attempted after the bounded hardening delta, but the execution environment blocked both local-file and localhost navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. This is an environment policy restriction, not an observed page/runtime failure.

For that reason PRG-0 does **not** falsely claim a second fresh browser execution against the last bytes. Confidence rests on:

1. the immediately preceding executable M1.2 30/30 browser pass;
2. the bounded/non-structural nature of PRG-0 deltas;
3. the final 18/18 static/mechanical validation above;
4. mandatory real-native implementation gates below.

## Native implementation QA still mandatory

These cannot be honestly closed with an HTML oracle and remain release gates:

- real iOS keyboard, Dynamic Type and VoiceOver;
- real Android IME, font scaling, TalkBack and predictive back;
- Universal Links / Verified App Links association and cold-start routing;
- real Google / Apple provider callback/cancellation;
- process death / background / resume;
- Keychain / Android protected storage;
- biometric enrollment change/lockout if biometrics ship;
- TLS/pinning/rotation where adopted;
- Play Integrity / App Attest where adopted;
- real backend rate-limit, recovery, session, replay and account-link behavior.

These are implementation-verification requirements, not unresolved product-flow questions.
