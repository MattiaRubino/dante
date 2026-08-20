# DANTE Access — current checkpoint

- Status: **CROSS-PLATFORM PRODUCTION-READY SPECIFICATION / PRG-0 PASS / PRE-IMPLEMENTATION**
- Date: **2026-08-20**
- Branch: `prototype/access-system`
- Production frontend/mobile executable: **not implemented here**
- Backend AuthN/AuthZ executable: **not implemented here**

## Current authorities

DANTE Access now has two complementary visual/behavior oracles over one semantic system.

### Desktop / web — A3.4

```text
artifact    DANTE Access A3.4 — strong corner mark
size        93897 bytes
SHA-256     b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6
status      APPROVED DESKTOP REVIEW ORACLE
archive     prototypes/frontend/access/archive/a3-4-approved-2026-08-20/
```

A3.5 full-opacity corner mark remains rejected.

### Mobile — M1.2 + PRG-0

```text
artifact    DANTE Access Mobile M1.2 — PRG-0
size        107010 bytes
SHA-256     2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676
status      APPROVED MOBILE REVIEW ORACLE / PRODUCTION-READY SPEC
archive     prototypes/frontend/access/archive/mobile-m1-2-approved-2026-08-20/
```

Mobile M1.2 is not a scaled desktop composition. It preserves the same semantics through a phone-native layout and platform-specific behavior rules.

## PRG-0 verdict

```text
semantic/product blockers          0
known security design blockers     0
known backend capability blockers  0
premature framework/API freezes    0
native implementation gates        OPEN BY DESIGN
backend implementation gates       OPEN BY DESIGN

PASS — PRODUCTION-READY SPECIFICATION / PRE-IMPLEMENTATION
```

Read:

- `docs/frontend/access/contract.md`
- `docs/frontend/access/state-model.md`
- `docs/frontend/access/mobile-technical-contract.md`
- `docs/frontend/access/mobile-research-matrix.md`
- `docs/frontend/access/mobile-production-readiness.md`
- `docs/frontend/access/mobile-qa.md`

## Mobile QA evidence

The immediately preceding M1.2 executable artifact passed the Chromium suite 30/30 across the mobile review/stress viewports. PRG-0 then made a bounded hardening delta and the final bytes pass 18/18 deterministic static/mechanical checks.

A fresh Chromium rerun against the final bytes was attempted but local-file and localhost navigation were blocked by the execution environment with `ERR_BLOCKED_BY_ADMINISTRATOR`; the checkpoint records this limitation explicitly rather than claiming a test that did not run.

Mandatory native iOS/Android/device/backend verification remains a release gate and is enumerated in `mobile-production-readiness.md` and `mobile-qa.md`.

## Password policy transition

The future implementation authority is now:

```text
minimum                    12 characters
maximum support            >=64 characters
composition requirements   none
password managers / paste  allowed
common/breached blocklist  required server-side
```

This is a deliberate DANTE V1 policy. It is not represented as compliance with the current NIST 15-character password-only baseline.

The exact A3.4 archive remains byte-immutable and therefore still contains the earlier 15+ review copy. That historical copy is superseded for production migration by Mobile M1.2 and the shared `access.*` locales.

## Accepted Access boundary

The cross-platform specification covers:

- Google / Apple / DANTE email-password entry;
- staged registration;
- verification;
- neutral recovery/reset;
- provider pending/cancel/error;
- secure account collision/linking semantics;
- session bootstrap/expiry/reauth/revocation requirements;
- IT/EN localization;
- lightweight first-run;
- offline/transport/failure taxonomy;
- mobile back/keyboard/AutoFill/lifecycle requirements;
- Universal Links / Verified App Links;
- OAuth native-client rules;
- abuse/threat/session/account-lifecycle requirements;
- assurance and future release-verification gates.

## Explicit non-freezes

PRG-0 does not choose:

- React / React Native / Flutter / native client stack;
- router/form/state libraries;
- HTTP path names or DTO classes;
- DB/auth schema;
- JWT vs opaque token/session representation;
- exact token/session/challenge lifetimes;
- exact password hashing parameters;
- exact provider/email/OTP library/provider;
- exact pinning implementation;
- exact Play Integrity/App Attest enforcement thresholds;
- passkey/MFA rollout timing;
- canonical Home implementation.

## Backend handoff

The current `feature/backend-scaffold` CP1 explicitly excludes AuthN/AuthZ and product API routes. This Access checkpoint is therefore a requirements/acceptance input to the later AuthN backend scope; it does not modify or pretend that auth already exists.

## Reopen discipline

Access is frozen for ordinary implementation after PRG-0. Reopen only for a material platform/standard/provider change, discovered security defect, backend safety/impossibility conflict, real-device accessibility/usability failure, or accepted DANTE semantic change.

Framework convenience or preference churn is not sufficient reason to redesign the flow.

## Next boundary

Proceed to production frontend/mobile stack selection and implementation. The production clients/backend must satisfy this checkpoint and then pass the native/backend release gates before any claim of production software readiness.
