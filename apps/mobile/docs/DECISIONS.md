# DANTE Mobile — Decision Log

Status: **ACTIVE**

This file records Mobile-local execution decisions and their reopen triggers. Repository-wide decisions remain owned by the canonical ADRs.

Use this log for decisions that materially constrain future Mobile work. Do not record every implementation detail.

---

## MD-001 — Android-first, iOS-compatible

**Status:** ACCEPTED  
**Date:** 2026-09-18

DANTE Mobile develops and validates Android first. iOS remains an architectural target but not an active release target.

### Consequences

- Android can receive direct device/emulator evidence now.
- iOS signing/store work is dormant.
- feature/application code should remain cross-platform unless platform-specific behavior is real.
- platform differences belong behind app-local adapters or platform-specific files.

### Reopen when

- iOS release is activated;
- an Android requirement would create significant iOS migration cost;
- evidence shows a native platform split is cleaner for a capability.

---

## MD-002 — Keep React Native + Expo

**Status:** ACCEPTED  
**Date:** 2026-09-18

Continue the repository-selected TypeScript/React Native/Expo Mobile stack. Do not rewrite DANTE Mobile in Flutter, Kotlin/Compose or Swift.

### Rationale

The current stack is already architecture-approved and directly materialized on Android, preserves TypeScript/React ecosystem alignment, and supports future iOS without forcing one Web/Mobile renderer.

### Reopen when

Only with concrete evidence of a structural blocker that cannot be repaired inside the current stack at acceptable cost.

---

## MD-003 — Stay on Expo 57 stable line during current foundation

**Status:** ACCEPTED  
**Date:** 2026-09-18

Expo 58 is currently beta and includes a React Native release candidate. Current foundation work remains on the Expo 57 stable family.

### Consequences

- evaluate current Expo 57 patch alignment in M00;
- do not upgrade to beta/canary for novelty;
- future stable major upgrade requires compatibility/device evidence.

### Reopen when

- Expo 58 becomes stable and its migration is justified;
- a security/platform requirement makes remaining on 57 inappropriate.

---

## MD-004 — Production development moves toward a DANTE Development Build

**Status:** ACCEPTED DIRECTION / NOT YET ACTIVATED  
**Date:** 2026-09-18

Expo Go remains acceptable for legacy probe convenience but is not the long-term production development environment. Activate a DANTE development build in a dedicated approved scope.

### Activation trigger

M00 compatibility baseline is green and the required dependency/build-file scope is approved.

---

## MD-005 — Thin routes, feature-first application ownership

**Status:** ACCEPTED  
**Date:** 2026-09-18

`app/` owns Expo Router adapters. Real product behavior belongs under `src/features/<capability>`; application-wide composition belongs to `src/bootstrap`; reusable Mobile UI to `src/ui`; native/device adapters to `src/platform`.

### Constraint

Do not create generic root `services`, `utils`, `hooks`, `stores`, `models` or `components` directories as dumping grounds.

### Reopen when

A real capability produces a repeated dependency problem that cannot be cleanly represented by the current boundaries.

---

## MD-006 — Create architecture folders only with ownership documentation; create substructure only with real code

**Status:** ACCEPTED  
**Date:** 2026-09-18

The Mobile foundation may establish the top-level ownership boundaries with README contracts. Feature subdirectories and additional architectural layers are created only when real implementation requires them.

### Rationale

This allows the branch to document stable ownership without manufacturing empty capability architecture.

---

## MD-007 — Mobile-only parallel branch hard boundary

**Status:** ACCEPTED FOR CURRENT WORKSTREAM  
**Date:** 2026-09-18

Default writes are restricted to:

```text
apps/mobile/**
```

Changes to root/shared/backend/Web/docs/CI require a fresh explicit scope.

### Consequences

- avoids accidental coupling to the active Temporal branch;
- package upgrades that require the root lockfile become explicit checkpoints;
- do not work around the boundary by vendoring/copying shared code inside Mobile.

### Reopen when

A real Mobile milestone necessarily requires a repository-wide integration change.

---

## MD-008 — Android phone portrait is primary, adaptive layout is required

**Status:** ACCEPTED  
**Date:** 2026-09-18

Design primarily for normal phone portrait use, while keeping layouts correct under legitimate Android window-size changes and large-screen behavior.

### Consequences

- no dependency on orientation lock for correctness;
- use responsive sizing/max widths/scroll behavior;
- add large-window/foldable/tablet checks at quality gates.

### Reopen when

Product requirements deliberately restrict supported form factors and platform policy permits that restriction without quality loss.

---

## MD-009 — Auth is real product infrastructure, not a mock milestone

**Status:** ACCEPTED  
**Date:** 2026-09-18

DANTE will require authentication, but implementation waits for inspection of the actual backend identity/session contract.

### Consequences

- route topology can anticipate public/protected trees;
- do not present a local toggle/fake login as completed auth;
- secure storage and backend/session changes require explicit scope;
- local route protection never replaces backend AuthZ.

---

## MD-010 — Offline activates on a real operation

**Status:** ACCEPTED  
**Date:** 2026-09-18

PowerSync/encrypted SQLite remain selected future capabilities but are not installed/activated merely for architectural completeness.

### Activation trigger

The first real Mobile operation has an approved offline requirement with classified acceptance/conflict semantics.

---

## MD-011 — No mega global state store

**Status:** ACCEPTED  
**Date:** 2026-09-18

Choose state mechanism by state class. React local state is the default for transient component state; server/query, form, auth and synced local state use dedicated owners when activated. Zustand is allowed only for justified cross-tree transient state.

### Reopen when

Evidence shows repeated cross-tree state cannot be cleanly handled by composition or a bounded specialist store.

---

## MD-012 — One milestone/substep at a time

**Status:** ACCEPTED PROCESS RULE  
**Date:** 2026-09-18

Mobile work proceeds through bounded roadmap steps with scope, direct validation and closure evidence before opening the next step.

This rule is specifically intended to prevent broad speculative implementation while the product and Temporal vertical continue evolving.

---

## MD-013 — Continuous Native Generation owns native project generation

**Status:** ACCEPTED  
**Date:** 2026-09-18

DANTE Mobile uses Expo Continuous Native Generation (CNG). Native `android/` and `ios/` projects are generated from application configuration and dependencies rather than maintained as canonical source directories.

### Consequences

- `apps/mobile/android/` and `apps/mobile/ios/` are ignored by Git;
- native changes must be represented through app config, config plugins or an explicitly approved exception;
- `expo prebuild --clean` may regenerate native projects when native dependencies or application configuration change;
- generated native code must not silently become a second configuration authority.

### Reopen when

A real native capability cannot be represented safely through CNG/config plugins and requires maintained native source ownership.

---

## MD-014 — Android application identity belongs to dantearc.com

**Status:** ACCEPTED  
**Date:** 2026-09-18

The canonical Android application ID is:

```text
com.dantearc.dante
```

The namespace is based on the project-owned `dantearc.com` domain and represents the DANTE product independently of an individual development machine or repository username.

### Consequences

- development and future production builds share a stable product namespace unless an explicit variant strategy is introduced;
- Play Store publication must preserve this identity once established;
- alternate development/store variants, if later required, must be introduced deliberately rather than by changing the canonical package ID.

---

## Decision entry template

```text
## MD-XXX — Title

Status: PROPOSED | ACCEPTED | SUPERSEDED
Date: YYYY-MM-DD

Decision...

Rationale...

Consequences...

Reopen when...
```

When a decision is superseded, retain it for history and link/name the replacing decision rather than deleting the old record.
