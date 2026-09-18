# DANTE Mobile — Roadmap

Status: **EXECUTION ROADMAP — FIRST MOBILE TRANCHE**  
Execution rule: work in a small number of complete blocks, not hundreds of micro-milestones. Validate each block before opening the next one.

The objective of this tranche is concrete: reach a real Android DANTE application with production-oriented runtime foundation, app shell/navigation, a coherent Mobile design system, a polished access flow shell, and a first Home v0. Then stop and reassess before entering the moving Temporal vertical.

## Scope policy

Default write boundary remains:

```text
apps/mobile/**
```

Small cross-boundary changes are allowed when they are mechanical, low-risk and easy to reconcile, but they must be explicitly scoped before the write. Typical acceptable examples are:

- `pnpm-lock.yaml` after Mobile dependency changes;
- version/pin files required by the Mobile toolchain;
- narrowly bounded Mobile CI/tooling changes.

Shared packages, root architecture rules, backend, Web, migrations and Temporal semantics are not modified implicitly. A need to change them becomes an integration checkpoint.

---

## MA — Android production foundation

### Goal

Turn the existing proven Expo/React Native skeleton into the stable development baseline for the real app.

### Work

Perform this as one coordinated foundation pass:

- verify the existing local Android toolchain and repository baseline quickly rather than creating a long audit workstream;
- inspect the exact versions resolved by the workspace lockfile;
- align the current Expo SDK 57 line to the latest compatible stable patch set using Expo-supported tooling rather than hand-picking package versions;
- keep Expo 58 or other prerelease lines out of scope until stable adoption is justified;
- update `apps/mobile/package.json` and `pnpm-lock.yaml` where required;
- preserve TypeScript strictness and the accepted New Architecture/Hermes baseline;
- move from Expo Go as a probe environment toward a DANTE Development Build when justified;
- add `expo-dev-client` only if required by that Development Build step;
- define Android application identity, package/application id, deep-link scheme and versioning posture before they become expensive to change;
- ensure native-generated output is treated correctly and does not accidentally become canonical source;
- establish safe-area, edge-to-edge, keyboard and adaptive-layout behavior suitable for modern Android;
- review the current portrait lock rather than assuming it is permanent;
- validate emulator/device launch, navigation runtime dependencies, Gesture Handler, Reanimated, Hermes, i18n and time support;
- run the relevant repository gates: compatibility, typecheck, lint, architecture and bundle/runtime checks.

### Exit

MA is complete when DANTE can be launched as a trustworthy Android development application, the dependency graph is aligned and reproducible, the repository is clean relative to the approved scope, and the baseline is ready for product work.

### Non-scope

No product navigation design, login backend integration, Home product semantics, Temporal features, offline/sync or iOS release work.

---

## MB — App shell and navigation

### Goal

Define and build the real application structure a user will move through.

### First decide

Before coding the final shell, determine at product level:

- the truly primary destinations of DANTE;
- what deserves permanent navigation;
- the role of Home;
- the future role of Timeline;
- whether there is a global create/action affordance;
- where Profile/Settings belong;
- whether bottom tabs are actually the best primary-navigation pattern for DANTE;
- startup/splash behavior;
- unauthenticated versus authenticated route topology.

### Build

Then materialize:

```text
Root application shell
├── Public area
│   ├── Welcome
│   ├── Sign in
│   └── other access routes only when justified
└── Authenticated area
    ├── primary navigation
    ├── detail stacks
    └── modal flows where appropriate
```

Expo Router route files remain thin adapters. Product logic lives under `src/features/**`; assembly belongs to bootstrap.

Validate Android Back/predictive-Back behavior, deep-link readiness and clean transitions between startup/public/authenticated states.

### Exit

The app has an intentional, scalable navigation shell and lifecycle structure even though real backend authentication is not yet wired.

---

## MC — DANTE Mobile design system

### Goal

Make the application look and behave like DANTE rather than a technical Expo prototype.

### Build from real needs

Create the smallest coherent system required by the shell, access screens and Home:

- light/dark theme strategy;
- semantic color usage;
- typography hierarchy;
- spacing/layout rules;
- responsive containers and max-width behavior;
- screen/surface/card primitives;
- buttons and icon actions;
- app header/navigation chrome;
- loading, skeleton, empty, error and retry states;
- touch feedback and motion rules;
- accessibility semantics, target sizes, contrast and text scaling;
- keyboard and safe-area behavior.

Use shared semantic design tokens where appropriate, but keep the actual React Native UI implementation Mobile-local. Do not create a giant internal UI framework or generic dumping-ground folders.

Additional packages such as `expo-font` are introduced only if a real visual decision requires them.

### Exit

The first real screens can be built consistently without one-off styling everywhere, while the UI layer remains small, native-feeling and recognizably DANTE.

---

## MD — Welcome / Login / access shell

### Goal

Build the complete user-facing entry experience up to the point where real backend authentication begins.

### Product flow

Target shape:

```text
DANTE icon
   ↓
Splash / bootstrap
   ↓
Welcome
   ↓
Sign in
   ├── Registration, if the product/backend supports it
   └── Recovery, if the product/backend supports it
```

The UI and route architecture should already support the future authenticated state, session restoration and protected application area.

### Important boundary

Do not fake production authentication or invent token semantics.

Before real AuthN integration, inspect the actual backend/account/session model and determine login, registration, refresh, expiry, revocation, recovery and passkey/credential capabilities. Secure native storage such as `expo-secure-store` is added when real session material exists.

For this first tranche, it is acceptable to stop with a polished access shell and a clearly separated adapter/contract boundary ready for the real backend.

### Exit

Welcome/Login are production-quality screens and the application lifecycle is structurally ready for real authentication without encoding a fake backend contract.

---

## ME — Home v0

### Goal

Build the first real DANTE product surface and establish the visual direction of the application.

### Product questions

Home should be designed to answer, at minimum:

- where am I in DANTE now;
- what matters now or today;
- what requires attention;
- what meaningful action can I take;
- how do I reach the rest of DANTE quickly.

### Work

- define information hierarchy before decorative layout;
- create the Home wireframe/structure;
- apply the DANTE Mobile design system;
- begin integrating the established DANTE visual identity where it improves the product;
- keep responsive/adaptive behavior from the first implementation;
- use only real stable data contracts when available;
- if placeholder/development content is needed, make it explicitly noncanonical and do not let it define future domain semantics.

Temporal concepts may be represented visually only to the extent that their semantics are already stable enough; this tranche does not implement the real Temporal vertical.

### Exit

Opening DANTE produces a coherent, polished application experience from icon/startup through navigation/access shell to a first intentional Home v0.

---

# STOP / CHECKPOINT AFTER ME

After ME, stop the first Mobile tranche.

Do **not** automatically continue into:

- real Timeline integration;
- Create Activity/Event/Routine;
- Schedule editing;
- Planning Tray;
- recurrence/occurrence;
- temporal constraints;
- Temporal mutations;
- PowerSync/offline write paths.

At that point review the current state of the parallel Temporal workstream and decide the next Mobile vertical from the then-current canonical product/API truth.

## What success looks like for this tranche

At the checkpoint we should have:

```text
real Android DANTE development app
+ stable Expo/RN foundation
+ app identity/startup
+ scalable navigation shell
+ DANTE Mobile design system
+ polished Welcome/Login access shell
+ Home v0
```

The goal is not to maximize screen count. The goal is to arrive quickly at a credible, production-oriented application foundation that can continue once the relevant product contracts are stable.

## iOS posture

iOS remains dormant as a release target but supported by architecture. Avoid unnecessary Android-only product design. Future iOS activation should be an adaptation/validation track, not a second application rewrite.

## Definition of completion

A block counts as complete only when:

- the intended behavior exists;
- direct validation evidence is available;
- known failures are explicit;
- repository changes remain inside approved scope or approved low-risk exceptions;
- architecture remains consistent with repository ADRs;
- documentation is updated when a decision materially changes.
