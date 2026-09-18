# DANTE Mobile — Technical Baseline

Status: **CURRENT BASELINE**  
Snapshot date: **2026-09-18**

This document records the Mobile technology posture that is authoritative inside `apps/mobile/**`. Repository-wide architecture remains owned by the accepted frontend ADRs; this document specializes those decisions for Mobile execution.

## 1. Product/platform posture

DANTE Mobile is **Android-first, not Android-only**.

Android is the active development and validation target. iOS remains an architectural target so application structure, feature logic and UI ownership must not assume Android-specific behavior unless a platform adapter genuinely requires it.

The Mobile client is a first-class DANTE application. It is not a Web wrapper and it does not force UI component sharing with the Web client.

## 2. Adopted stack

### Core

- TypeScript in strict mode.
- React 19.2 family as qualified by the Expo workspace.
- React Native 0.86 family.
- Expo SDK 57 stable line.
- Expo Router for route/navigation adapters.
- React Native New Architecture.
- Hermes JavaScript engine.

### Existing native/runtime capabilities

- `react-native-gesture-handler` for gesture integration.
- `react-native-reanimated` for UI-thread-oriented animation where justified.
- `react-native-safe-area-context` for safe-area ownership.
- `react-native-screens` through the navigation stack.
- `react-native-worklets` as required by the current Reanimated graph.
- `@dante/design-tokens`, `@dante/i18n`, and `@dante/time` as the current real shared semantic packages.

The repository already directly validated the Expo/Metro/Hermes Android runtime and production-bundle smoke for the materialized baseline. We build forward from that evidence rather than restarting the Mobile stack.

## 3. Version policy

### Stable over newest

Production work follows the newest **qualified stable line**, not the newest announcement.

As of this snapshot:

- Expo SDK 57 is stable and was released with React Native 0.86.
- Expo SDK 58 is in beta and includes a React Native 0.88 release candidate.
- DANTE therefore stays on Expo 57 until a stable upgrade is deliberately evaluated and validated.

No production milestone may move to a beta/canary framework merely to be current.

### Patch maintenance

The current repository package manifest still declares the earlier materialized Expo 57/RN 0.86 patch set. Expo later published fixes in the same SDK 57 line, including RN 0.86.3 for a Hermes development-startup regression and earlier fixes relevant to Worklets/Reanimated memory behavior.

Therefore M00 includes an explicit compatibility audit and, if clean, a patch-only alignment inside Expo SDK 57.

A package change that requires `pnpm-lock.yaml` is a cross-boundary change and must receive a separate approved scope. Do not hand-edit, duplicate or bypass the workspace lockfile.

## 4. Development environment

### Adopt

Use a **DANTE development build** as the production-oriented development environment once M00 activates it.

Expo Go is acceptable only as an early runtime/probe convenience. It is not the long-term environment for a production-grade DANTE client because it cannot represent arbitrary native dependencies and application-native configuration.

Development-build activation must be deliberate because adding `expo-dev-client`, native configuration or build profiles may require files outside the current Mobile-only boundary.

### Device strategy

Primary validation order:

1. Android emulator for repeatable development checks.
2. Real Android phone for touch, keyboard, lifecycle, performance and device-behavior evidence.
3. Additional Android window sizes/form factors at defined quality checkpoints.
4. iOS simulator/device validation only when iOS becomes an activated release target.

## 5. Android target posture

DANTE must be compatible with the modern Android 16 / API 36 environment and Google Play targeting requirements.

Design consequences:

- edge-to-edge is treated as normal application behavior;
- status/navigation bars and cutouts are not hard-coded away;
- Android system Back and predictive-back behavior are respected;
- layouts must be responsive to available window dimensions;
- phone portrait is the primary product canvas, not the only supported geometry;
- tablet/foldable/large-window behavior must degrade intentionally rather than stretch accidentally.

The current `orientation: 'portrait'` configuration is legacy baseline state, not a permanent product decision. Android 16 can ignore orientation/aspect restrictions on large screens. Any future orientation policy must therefore be judged against adaptive-layout requirements rather than assumed to enforce layout safety.

## 6. Navigation and application lifecycle

Adopt Expo Router as the navigation adapter.

Target lifecycle model:

```text
OS launches DANTE
        ↓
native splash / bootstrap
        ↓
restore required local application state
        ↓
resolve authentication state when AuthN exists
        ↓
public route tree OR protected application route tree
```

Routes declare navigation composition. They must not become feature/business-logic containers.

Expo Router protected routes are the preferred client navigation mechanism when real authentication is activated. They are navigation protection, not backend authorization.

## 7. UI posture

DANTE owns a Mobile-specific UI system built on React Native primitives and shared semantic design tokens.

Principles:

- platform-native behavior, DANTE-specific visual identity;
- no forced Web/Mobile renderer sharing;
- reusable UI only after repeated real usage demonstrates the abstraction;
- accessible touch targets and readable typography from first implementation;
- safe-area, keyboard and dynamic window behavior treated as layout inputs;
- motion supports comprehension and feedback; it does not decorate every interaction.

`@expo/ui` / native Compose or SwiftUI-backed primitives may be evaluated component-by-component when they provide a real platform-quality benefit. They are not a blanket UI framework decision.

## 8. State and data ownership

State classes remain separate:

```text
canonical accepted state/effects   backend + PostgreSQL
remote request state               TanStack Query when activated
form state                         TanStack Form when activated
component transient state          React
cross-tree transient UI state      Zustand only when justified
synced local projection            PowerSync + encrypted SQLite when activated
offline pending mutation           local staging only
```

No all-purpose global Mobile store.

No client-side object may silently become canonical DANTE truth.

## 9. Authentication posture

Authentication is required for the real product, but concrete protocol/identity-provider activation is intentionally deferred until the backend AuthN contract is inspected and approved.

When activated:

- authenticated and public route trees are explicit;
- secrets/tokens use secure native storage, not generic async/local JS persistence;
- session restore occurs during bootstrap;
- session expiry/revocation has a truthful user-visible state;
- backend authorization remains authoritative even if navigation is protected locally;
- future password, federated identity and passkey support must not require rewriting the whole app shell.

A fake login must never be presented as completed authentication architecture.

## 10. Offline posture

Offline is a designed capability, not an automatic property of Mobile.

Do not install or activate PowerSync/SQLite merely to claim offline readiness. Activate local persistence at the first real offline operation, with explicit classification of:

- what can be read offline;
- what can be staged offline;
- what requires online governed acceptance;
- how conflicts/rejections reconcile;
- which local data is cache/projection versus user-authored pending intent.

## 11. API posture

Feature UI must depend on feature-specific data/model boundaries, not raw HTTP calls scattered through screens.

OpenAPI -> Orval typed transport generation activates only when a real backend product API contract needs a Mobile consumer. Generated transport types are not the domain model and are not a universal repository abstraction.

## 12. Testing/observability posture

Adopt progressive evidence:

- strict TypeScript and architecture checks continuously;
- deterministic unit tests for pure logic;
- component/integration tests for meaningful UI behavior;
- navigation/auth lifecycle tests when those capabilities exist;
- real-device Android checks at milestone gates;
- E2E automation when a stable end-to-end user flow exists;
- startup, rendering, memory, jank and crash evidence before release-quality claims.

Do not mark manual/device tests PASS without observed evidence.

## 13. ADOPT / LATER / AVOID

### ADOPT now

- Expo 57 stable line.
- React Native 0.86 family.
- TypeScript strict.
- Expo Router.
- New Architecture + Hermes.
- Gesture Handler / Reanimated where justified.
- feature-first ownership.
- app-local UI and platform adapters.
- Android-first validation.
- responsive/adaptive layout discipline.

### ACTIVATE LATER, on real trigger

- patch alignment of Expo 57 baseline after compatibility audit;
- Development Build / `expo-dev-client`;
- secure auth storage and concrete AuthN protocol;
- TanStack Query;
- TanStack Form;
- Zod runtime validation at external boundaries where justified;
- OpenAPI -> Orval generated client;
- PowerSync + encrypted SQLite;
- EAS Build / Submit / Update / Observe;
- automated Mobile E2E;
- push notifications/background capabilities;
- iOS signing/release pipeline.

### AVOID without evidence

- Expo beta/canary in the production baseline;
- framework rewrite to Flutter/Kotlin/Swift without architectural evidence;
- universal Web/Mobile component renderer;
- root-level generic `services`, `utils`, `hooks`, `stores` dumping grounds;
- mega global state store;
- universal `Repository<T>` abstraction;
- direct feature dependence on storage/network implementation details;
- offline writes that bypass backend governance;
- platform-specific hacks in feature code when a platform adapter can contain them;
- dependency upgrades that silently modify shared/root files outside approved scope.

## 14. Official references used for this snapshot

- Expo SDK 57 changelog: https://expo.dev/changelog/sdk-57
- Expo SDK 58 beta: https://expo.dev/changelog/sdk-58-beta
- Expo development builds: https://docs.expo.dev/develop/development-builds/introduction/
- Expo Router protected routes: https://docs.expo.dev/router/advanced/protected/
- React Native 0.86 release: https://reactnative.dev/blog/2026/06/11/react-native-0.86
- Android adaptive orientation/resizability: https://developer.android.com/develop/adaptive-apps/guides/app-orientation-aspect-ratio-resizability
- Android 16 target behavior changes: https://developer.android.com/about/versions/16/behavior-changes-16

Review this baseline whenever a framework major, Android target requirement, activated iOS target, auth/offline architecture or repository-wide frontend ADR materially changes.