# DANTE Mobile — Application Architecture

Status: **CURRENT MOBILE EXECUTION ARCHITECTURE**

This document specializes the accepted repository frontend architecture for `apps/mobile/**`. It does not supersede ADR-008 or ADR-009.

## 1. Architectural goals

The Mobile app must remain:

- understandable by capability, not by framework artifact;
- independently evolvable from Web UI;
- compatible with Android-first delivery and later iOS activation;
- explicit about state/data authority;
- resistant to route, storage, networking and state-management leakage;
- easy to test at feature boundaries;
- small enough that abstractions are earned rather than pre-created.

## 2. Top-level structure

```text
apps/mobile/
├── app/                  # Expo Router adapters only
├── docs/                 # Mobile execution documentation
└── src/
    ├── bootstrap/        # composition/startup
    ├── features/         # product capability ownership
    ├── ui/               # DANTE Mobile UI system
    ├── platform/         # native/device/platform adapters
    └── testing/          # Mobile-specific test support
```

Do not create empty folders beyond real ownership needs.

## 3. `app/` — route adapters

`app/` is owned by Expo Router and should stay thin.

Allowed responsibilities:

- route groups and route identity;
- stack/tab composition;
- route-level guards when auth exists;
- route parameter adaptation/validation entry;
- wiring route destinations to feature screens;
- route-specific presentation options.

Not allowed:

- business/domain decisions;
- direct HTTP/storage implementation;
- feature data orchestration that belongs to the feature;
- duplicated feature UI;
- canonical authorization decisions.

A route should normally import a feature screen or small application composition surface and stop there.

## 4. `src/bootstrap/` — application composition

Bootstrap is the composition root of the Mobile application.

It may own:

- provider assembly;
- startup/lifecycle sequencing;
- theme/application appearance composition;
- i18n initialization integration;
- future session restoration orchestration;
- future query/runtime clients as application-scoped dependencies;
- application-level error boundary composition;
- app-wide dependency wiring.

Bootstrap may depend on app-local feature public APIs, UI and platform adapters as required for assembly. Features must not depend back on bootstrap.

Bootstrap is not a second feature layer and must not accumulate business use cases.

## 5. `src/features/` — product capability ownership

Create a feature directory only when a real product capability exists.

Illustrative future shape, not a mandatory template:

```text
src/features/<capability>/
├── screens/          # route-consumable feature presentation
├── components/       # capability-private UI
├── model/            # feature-local state/types/pure logic
├── data/             # feature data boundary/adapters
└── index.ts           # public API when cross-boundary use exists
```

Only create subdirectories actually required by that capability.

Rules:

- feature implementation is private by default;
- cross-feature imports use a deliberate public API when real reuse is justified;
- deep-importing another feature's internals is forbidden;
- feature cycles are architectural defects, not reasons to add aliases;
- orchestration spanning capabilities belongs in an explicit higher-level composition/use-case boundary rather than mutual feature imports;
- backend/domain semantics are consumed, not reinvented.

Examples of potential future features include authentication, home, profile, settings and temporal surfaces. Their existence is not assumed until scoped.

## 6. `src/ui/` — DANTE Mobile UI system

Owns reusable Mobile visual/interaction primitives that are not capability-specific.

Examples when real use appears:

- typography primitives;
- surfaces/cards;
- buttons/icon buttons;
- input wrappers;
- app bars/headers;
- loading/empty/error primitives;
- layout primitives;
- theme adapters;
- motion primitives with repeated semantic use.

Rules:

- use shared semantic design tokens where available;
- do not copy Web implementation components;
- UI components do not own HTTP/storage/domain workflows;
- avoid one mega component library created ahead of product evidence;
- accessibility semantics are part of the component contract;
- platform behavior can delegate to `platform/` rather than branching everywhere.

Feature-specific components stay in the feature until repeated cross-feature use proves a shared UI abstraction.

## 7. `src/platform/` — native and device integration

Owns direct interaction with platform/native capabilities.

Potential responsibilities when activated:

- secure credential/token storage;
- app lifecycle/device signals;
- deep-link/native intent adaptation;
- notifications;
- haptics;
- permissions;
- background execution;
- native appearance/window integration;
- platform-specific accessibility/device behavior;
- Android/iOS-specific implementation seams.

Feature code should consume narrow capability interfaces rather than import native libraries throughout the tree.

Platform adapters do not become canonical product truth.

## 8. `src/testing/` — test support

Owns shared Mobile test infrastructure only after repeated use exists.

Possible future contents:

- render helpers/providers;
- deterministic fixtures/builders;
- fake platform adapters;
- navigation harness;
- test clocks where justified;
- E2E identifiers/constants with product-stable meaning.

Do not place production business logic here.

## 9. Dependency direction

Conceptual direction:

```text
app/routes
   ↓
feature public surfaces
   ↓
feature model/data boundaries
   ↓
platform / generated transport / external adapters

bootstrap
   ↓ assembles
routes + features + ui + platform

features ──→ ui
features ──→ platform through narrow adapters when needed
ui       ──X→ features
platform ──X→ features
features ──X→ bootstrap
```

Shared repository packages may be consumed according to ADR-009. Mobile must not import Web application code.

## 10. Data firewall

A feature UI must not know every transport/storage detail.

Preferred shape:

```text
screen/component
      ↓
feature controller/hook/model boundary
      ↓
feature data contract
      ↓
remote/local adapter
```

This does not imply a universal repository pattern. The boundary should match the real capability and operation.

Examples:

- a read query can remain a query-shaped boundary;
- a governed mutation can remain an operation/command-shaped boundary;
- local offline staging can expose pending/reconciliation semantics explicitly.

Do not flatten them into `Repository<T>.save()`.

## 11. State taxonomy

Classify state before choosing a library.

- component interaction state -> React local state;
- cross-component transient UI state -> lift/compose first; Zustand only if genuine cross-tree need appears;
- remote request/cache state -> TanStack Query when activated;
- form lifecycle -> TanStack Form when activated;
- session/auth material -> dedicated auth/session boundary + secure platform storage where required;
- synced offline projection -> PowerSync/SQLite when activated;
- canonical accepted DANTE state -> backend/PostgreSQL only.

Libraries do not determine authority.

## 12. Navigation architecture

Target route topology should separate lifecycle concerns rather than mix every screen in one flat stack.

Illustrative future grouping:

```text
app/
├── _layout.tsx
├── (public)/
│   ├── _layout.tsx
│   └── ...
└── (app)/
    ├── _layout.tsx
    └── ...
```

The exact bottom-tab destinations, onboarding and auth screens are product decisions and must be designed before materialization. Do not create placeholder destinations just to satisfy this diagram.

Nested stacks should model navigation depth; bottom-level primary navigation should model genuinely primary destinations only.

## 13. Cross-platform rule

Prefer shared React/TypeScript feature code when behavior is genuinely common.

Use platform-specific files/adapters when behavior is genuinely different:

```text
thing.ts
thing.android.ts
thing.ios.ts
```

or a platform interface implemented below `platform/`.

Do not force identical UI interaction where Android and iOS conventions materially differ. Do not fork entire features merely for cosmetic platform differences.

## 14. Error and loading architecture

Every real asynchronous feature must define truthful states, normally including:

- initial/idle when meaningful;
- loading/refreshing distinction where meaningful;
- content;
- empty;
- recoverable error;
- unrecoverable/fatal boundary only at appropriate scope;
- stale/offline/pending/conflict states when those capabilities activate.

A spinner is not a complete state model.

## 15. Security boundary

The client may improve UX using session state and protected navigation, but it cannot enforce canonical authorization.

Rules:

- never trust client route protection as AuthZ;
- never persist secrets in plain generic storage;
- never log credentials/tokens or sensitive payloads;
- clear/revoke local session material according to the future AuthN contract;
- validate untrusted external inputs at the appropriate boundary;
- treat deep links and route params as untrusted input.

## 16. Architectural anti-patterns

Reject by default:

- fat route files;
- direct API calls in generic UI primitives;
- storage access scattered through screens;
- feature-to-feature cycles;
- root `utils/` dumping ground;
- root `services/` holding every backend operation;
- `store.ts` containing the application;
- platform checks (`Platform.OS`) spread through business code;
- frontend copies of canonical backend rules;
- fake generic abstractions created before two real consumers exist;
- UI components exported globally solely because they might be useful later.

## 17. Architecture change rule

If a milestone cannot fit these boundaries cleanly:

1. describe the concrete contradiction;
2. identify whether the issue is feature, UI, platform, data or repository-wide;
3. prefer the narrowest boundary repair;
4. update this document/decision log only after evidence;
5. do not silently bypass the architecture to keep coding moving.