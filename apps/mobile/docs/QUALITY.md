# DANTE Mobile — Quality Bar

Status: **MANDATORY QUALITY BASELINE**

This document defines what “production-grade Mobile” means for DANTE. It is intentionally stricter than “the screen renders”.

## 1. Correctness first

Every completed behavior must be truthful to the current DANTE product/domain contract.

- planned state must not be presented as actual state;
- local projection/cache must not be presented as canonical acceptance;
- route protection must not be presented as backend authorization;
- pending/offline state must be distinguishable from accepted state when offline activates;
- unsupported or unknown states must fail visibly and safely rather than be guessed.

## 2. Type and boundary quality

- TypeScript strict remains enabled.
- Avoid `any`; exceptions require a narrow, documented interoperability reason.
- External/untrusted inputs are validated at their boundary when runtime uncertainty exists.
- Route parameters are untrusted input.
- Transport/generated types do not automatically become feature/domain types.
- Public cross-feature APIs stay narrow.

## 3. Interaction quality

Every interactive control must have:

- adequate touch target;
- clear pressed/disabled/loading behavior where applicable;
- semantic accessibility role/name/state;
- predictable focus/keyboard behavior for text entry;
- visible feedback for actions that are not instant;
- destructive-action protection proportional to consequence, not generic confirmation spam.

Motion should communicate hierarchy, transition or feedback. Avoid animation that delays routine use.

## 4. Async state quality

A real network/data surface must consider the states relevant to its operation, including:

- initial loading;
- background refresh versus blocking load;
- content;
- empty;
- partial/stale content where applicable;
- recoverable error and retry;
- offline/degraded connection when activated;
- pending mutation;
- rejection/conflict/reconciliation when activated.

Do not replace all asynchronous states with a full-screen spinner.

## 5. Android system integration

DANTE must behave like a high-quality Android application.

Validate as applicable:

- system Back and predictive Back;
- edge-to-edge insets;
- status/navigation bar readability;
- cutouts/notches;
- keyboard opening/closing and resize/pan effects;
- foreground/background lifecycle;
- app restore after process/activity recreation where state matters;
- deep links/intents when activated;
- permissions denial and permanent denial states;
- system light/dark appearance.

## 6. Responsive/adaptive UI

Primary design target: phone portrait.

Quality requirement: layouts remain usable under other legitimate window sizes.

At minimum:

- avoid hard-coded full-screen pixel dimensions;
- use available width and sensible max widths;
- allow content to scroll when vertical space contracts;
- preserve important state across window/orientation changes;
- verify large text does not clip critical actions;
- test at least compact phone and a large-window/tablet/foldable profile at the defined milestone gate.

Do not depend on orientation lock for layout correctness.

## 7. Accessibility

Accessibility is part of feature completion, not a release-week patch.

Required where applicable:

- meaningful accessibility labels/roles/states;
- logical reading/focus order;
- no information conveyed only by color;
- adequate contrast;
- scalable readable text;
- controls reachable without precision tapping;
- motion sensitivity considered for nonessential animation;
- errors associated with the relevant field/control;
- screen-reader smoke validation on critical flows before release-quality claims.

## 8. Visual consistency

Use shared semantic design tokens and Mobile UI primitives where they exist.

Avoid:

- random literal colors/spacing repeated across features;
- per-screen typography systems;
- inconsistent card radius/elevation/pressed behavior;
- feature-local clones of a shared primitive with no product reason.

Do not over-centralize feature-specific visual language merely for reuse statistics.

## 9. Performance

Performance claims require measurement.

Track at relevant maturity points:

- cold start;
- warm/resume behavior;
- first meaningful render;
- navigation transition latency;
- dropped frames/jank on high-use interactions;
- list performance;
- memory growth/leaks;
- image/resource cost;
- network request duplication/churn;
- development-versus-production differences where material.

Profile production/release-like builds for release decisions; development-mode timing alone is not authoritative.

## 10. Reliability

- failures must not strand the user in an impossible navigation state;
- retry must be safe for the operation's idempotency semantics;
- session expiry must recover deliberately;
- app restart must not silently lose accepted user state;
- locally pending work, if later supported, must have explicit persistence/reconciliation guarantees;
- no swallowed exceptions used to keep UI appearing successful.

## 11. Security/privacy

- credentials/session secrets never live in plain generic storage;
- never log secrets/tokens/passwords;
- minimize sensitive data persisted locally;
- clear sensitive local material according to logout/revocation semantics;
- treat deep links, clipboard, external intents and route params as untrusted input;
- backend AuthZ remains authoritative;
- analytics/observability payloads must not casually include private user content.

## 12. Testing ladder

Use the cheapest test that gives sufficient confidence, then escalate with risk.

### Continuous/local

- TypeScript check;
- lint/architecture checks available to the workspace;
- pure/unit tests for deterministic logic.

### Feature milestone

- component/integration behavior for meaningful state transitions;
- navigation behavior when affected;
- emulator validation;
- real-device validation for touch/keyboard/lifecycle/platform-sensitive work.

### Critical-flow/release

- E2E for stable high-value flows;
- degraded network/session failure paths;
- accessibility smoke;
- multi-window/device-size checks;
- performance profiling;
- release build smoke.

A manual test is PASS only if it was actually performed and observed.

## 13. Done criteria for a screen/flow

A production-intended screen is not done until the applicable items are true:

- semantic behavior matches product truth;
- navigation/back behavior is correct;
- loading/content/empty/error states exist as required;
- interactions have feedback;
- safe area and keyboard work;
- accessibility basics are present;
- layout survives required window sizes;
- no obvious architecture boundary leak;
- tests/evidence appropriate to risk exist;
- no known critical error hidden behind a TODO.

## 14. Release-candidate bar

Before claiming Android release readiness, require explicit evidence for:

- signed release/build pipeline;
- install/launch on physical Android device;
- critical E2E flows;
- session lifecycle;
- crash/error observability;
- startup/render performance sanity;
- Android 16/API-target behavior;
- predictive/system Back;
- accessibility critical flows;
- network degradation;
- app icon/splash/theme metadata;
- Play Store package/versioning/privacy requirements;
- no accidental development/probe surfaces exposed to users.

## 15. Quality trade-off rule

When schedule and quality conflict, distinguish:

- polish that can safely follow;
- structural debt that compounds;
- correctness/security/data-authority defects that must block.

We can ship a visually less elaborate v0. We do not knowingly ship false state, insecure session handling or architecture shortcuts that make later features unreliable.