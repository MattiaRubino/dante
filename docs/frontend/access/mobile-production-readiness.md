# DANTE Access — PRG-0 Production Readiness Gate

Status: **PASS — PRODUCTION-READY SPECIFICATION / PRE-IMPLEMENTATION**  
Date: **2026-08-20**  
Branch: `prototype/access-system`  
Desktop authority: **A3.4**  
Mobile authority: **M1.2 + PRG-0**

## 1. Verdict

PRG-0 passes.

Access is sufficiently specified to proceed to production frontend/mobile and AuthN backend implementation without another ordinary product-design pass. `production-ready specification` does **not** mean released production software: native provider SDKs, secure storage, real links, backend AuthN, real-device accessibility and security verification remain implementation/release gates.

```text
semantic/product blockers          0
known security-design blockers     0
known backend-capability blockers  0
premature framework/API freezes    0
VERDICT                            PASS
```

## 2. Selected mobile oracle

```text
DANTE Access Mobile M1.2 + PRG-0
size       107010 bytes
SHA-256    2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676
```

The standalone is a coded review oracle, not a production bundle and not a DOM-to-DOM implementation template.

## 3. What is frozen

Frozen unless later evidence invalidates it:

- cross-platform Access state semantics;
- staged signup -> password -> verification;
- neutral recovery/reset behavior;
- provider authentication separate from provider-data authorization;
- no silent account merge/link;
- session-expiry/reauth semantics;
- verified HTTPS deep-link requirement;
- platform-native provider behavior;
- offline/back/lifecycle semantics;
- client ↔ backend capability requirements;
- security/privacy invariants;
- V1 password UX/policy boundary;
- assurance target and implementation release gates.

Framework, endpoint, DTO, schema, token and library choices remain open.

## 4. Password V1 decision

```text
minimum                     12 characters
support                     >=64 characters
composition checklist       none
paste/password manager      required support
show/hide                   required support
common-password blocklist   required server-side
breached-password blocklist required server-side
periodic forced rotation    not required absent compromise/risk
```

This is a deliberate DANTE decision. It is **not** described as satisfying the current NIST 15-character password-only baseline. A3.4's immutable 15+ archive remains historical evidence; M1.2/shared locales supersede it for implementation.

## 5. Assurance target

### Native mobile

Target all relevant **OWASP MASVS v2 controls** and assess the implemented apps with current MAS Testing Profiles, including L2-profile testing where applicable to Access risk. MASVS v2 itself no longer uses the old formal L1/L2 verification-level model; documentation must not claim a nonexistent modern “MASVS L2 certification.”

### Backend

Target **OWASP ASVS 5.0.0 Level 2 alignment** with an explicit exception register. DANTE V1 does not currently mandate MFA/passkeys for every account, so MFA-related L2 requirements remain declared exceptions until an accepted mechanism exists. Compensating controls and MFA/passkey-ready architecture are mandatory meanwhile.

## 6. Threat/abuse coverage required in implementation

Implementation and tests must cover:

- credential stuffing and distributed brute force;
- account enumeration;
- OTP guessing/resend abuse;
- recovery proof theft/replay;
- OAuth state/nonce/PKCE/redirect attacks;
- authorization-code replay;
- refresh-token theft/replay;
- account-link takeover;
- deep-link interception/tampering;
- malicious/tampered clients;
- rooted/jailbroken/compromised devices as risk context, not identity;
- network interception/endpoint identity failure;
- stolen-device/session hijack;
- process kill/resume with secret leakage;
- password/email/provider-factor mutation;
- account disable/delete with stale sessions;
- logging/analytics/crash leakage.

## 7. Session/account lifecycle requirements

The production AuthN design must support:

- server-authoritative session bootstrap;
- documented inactivity and absolute lifetime policy;
- session rotation after authentication/material reauth;
- current-session revocation;
- safe password/email/provider-change consequences;
- sensitive-account-change reauthentication;
- account disable/delete invalidating active sessions;
- provider link/unlink safeguards so the last viable auth path is not silently removed;
- future user-visible device/session revocation capability;
- security-event notification capability for material account/credential changes.

If refresh tokens are issued to public mobile clients, replay protection through sender-constraining or refresh-token rotation is mandatory under current OAuth BCP.

## 8. Deep links and provider flows

Security-sensitive continuation must use DANTE-owned HTTPS links with:

- iOS Universal Links / Associated Domains;
- Android Verified App Links / Digital Asset Links;
- server-side proof validation independent of client routing.

Native provider auth must use official/platform-supported external flow; no embedded credential WebView. Provider UI completion is not canonical account mutation until backend validation succeeds.

## 9. Network and app-integrity gates

TLS-only production transport is mandatory.

For DANTE-controlled native API endpoints, implementation must evaluate endpoint identity pinning against the selected MAS profile/risk target. If adopted, it requires backup key/pin material, rotation and break-glass procedures. Brittle single-pin deployment is rejected; third-party provider domains are not pinned by DANTE.

Evaluate Play Integrity and App Attest for selected high-abuse/high-impact requests. Attestation is defense-in-depth/risk evidence, never identity or authorization, and must have explicit unavailable/degraded handling.

## 10. Privacy/telemetry lock

Never place raw password, OTP, recovery proof, authorization code, PKCE verifier, provider token/assertion or access/refresh/session secret in routine logs, analytics, crash breadcrumbs, URLs or generic persistence.

Security monitoring may use minimum necessary server-side signals under explicit retention/access policy; it must not become unrelated behavioral surveillance.

## 11. QA evidence already completed

M1.2 browser QA before the final PRG-0 static delta recorded **30/30 PASS**, including phone/stress viewports, 100/125/150/200% text scale, Android touch targets, 12-character password behavior, offline behavior, session-expired cancellation and state-aware Back.

Final PRG-0 static/mechanical verification recorded **18/18 PASS**, including:

```text
duplicate IDs                  0
Access screens                 18
stale 15+ rule                 0
12-char enforcement            PASS
reauth semantics               PASS
current-password semantics     PASS
forgot-email autofill          PASS
credential persistence         NONE
embedded IT/EN parity          128 / 128
shared locale parity           146 / 146
JS syntax                      PASS
OTP semantics                  PASS
password autofill coverage     PASS
```

The final tiny PRG-0 delta could not be re-run in Chromium in the execution environment because local file/localhost navigation was administrator-blocked. This is recorded transparently rather than falsely reported as another browser PASS.

## 12. Mandatory implementation release gates

Before release, the implemented system still requires:

### Native clients
- Keychain / Android protected-storage verification;
- actual Google/Apple provider integration;
- Universal/App Links association and cold-start routing;
- real keyboard/IME/password-manager/OTP AutoFill;
- VoiceOver/TalkBack and native large-text testing;
- Android Predictive Back;
- process death/background/resume/app update;
- biometrics if shipped;
- Play Integrity/App Attest if adopted;
- TLS/pinning/rotation tests where adopted;
- real-device iOS/Android regression.

### Backend
- password hashing/rehash implementation review;
- breached/common-password checks;
- enumeration/timing review;
- credential-stuffing/rate-limit tests;
- OTP/recovery single-use/replay tests;
- OAuth provider state/nonce/PKCE/redirect/token validation tests;
- account-link takeover tests;
- session expiry/rotation/revocation/replay tests;
- account lifecycle consequences;
- audit/log redaction;
- ASVS exception register and verification evidence.

These are implementation verification obligations, not reasons to reopen ordinary Access product design.

## 13. Intentional implementation deferrals

PRG-0 does not select:

- React Native/native/other client stack;
- web React runtime details;
- router/forms/state libraries;
- exact API paths/DTO names;
- JWT vs opaque token/session representation;
- exact token/challenge lifetimes;
- secure-storage wrapper;
- exact hashing cost parameters;
- exact provider/email/OTP service;
- pinning implementation library;
- attestation enforcement thresholds;
- passkey/MFA rollout timing.

## 14. Reopen rule

Access design is frozen for ordinary implementation after PRG-0. Reopen only for:

1. material platform/API/standard change invalidating a locked assumption;
2. real security review finding a material flaw;
3. backend implementation proving a required capability impossible or materially unsafe;
4. real-device accessibility/usability failure;
5. provider policy/SDK requirement forcing behavior change;
6. accepted DANTE product/domain semantic change.

Framework preference or library convenience is **not** a valid reason to redefine the flow.
