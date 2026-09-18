# DANTE Mobile — Roadmap

Status: **EXECUTION ROADMAP**  
Principle: one bounded milestone at a time; no milestone is closed without evidence.

This roadmap deliberately separates platform/application foundations from product verticals so Mobile can advance in parallel without inventing unstable Temporal semantics.

## Global rules

For every milestone:

1. define exact scope and non-scope;
2. inspect current branch HEAD and relevant authorities;
3. implement the smallest complete slice;
4. validate behavior and quality with direct evidence;
5. record any changed decision;
6. close before opening the next slice.

A milestone may be split into numbered substeps (`M00.1`, `M00.2`, ...) and those substeps should be executed sequentially unless independence is proven.

Current default write boundary remains `apps/mobile/**`. Any required change outside it triggers a new scope decision.

---

## M00 — Baseline and production development posture

### Objective

Turn the already-proven Mobile runtime skeleton into a trustworthy starting baseline without changing product UX yet.

### Planned concerns

- verify exact resolved Expo/React Native dependency compatibility;
- evaluate patch-only Expo 57 alignment to the current stable patch set;
- run Expo dependency/doctor checks as applicable;
- confirm TypeScript strict coverage for `app/**` and `src/**`;
- confirm Android emulator runtime still works;
- confirm Gesture Handler/Reanimated/Hermes probe still works before replacing it;
- decide/activate Development Build only through an explicitly approved dependency/build scope;
- define Android device/emulator validation baseline;
- review current portrait lock against adaptive-layout posture before changing it.

### Explicit non-scope

- product navigation design;
- login implementation;
- Home implementation;
- Temporal feature UI;
- offline runtime;
- iOS release pipeline.

### Exit gate

- dependency/runtime baseline documented and directly verified;
- no unexplained Expo compatibility errors;
- Android launch evidence exists;
- no accidental files outside approved scope;
- any required cross-boundary dependency changes separately approved.

---

## M01 — Application lifecycle and navigation architecture

### Objective

Define and materialize how a user enters and moves through DANTE before feature screens proliferate.

### Sequence

1. product-level navigation discussion;
2. identify truly primary destinations;
3. choose route-group topology;
4. define public vs authenticated lifecycle shape without faking auth;
5. define stack/tab responsibilities;
6. materialize thin route adapters;
7. verify Android Back, deep-link readiness and navigation state behavior.

### Decisions required before coding

- primary destinations (normally 3–5, not arbitrarily fixed);
- whether primary navigation is bottom tabs or another evidence-backed pattern;
- role of a global create/action affordance, if any;
- onboarding entry model;
- startup/splash behavior;
- treatment of unauthenticated state before real backend AuthN activation.

### Exit gate

A user can navigate the approved application shell predictably with correct system Back behavior, no feature logic in route files and no dead placeholder architecture presented as finished product.

---

## M02 — DANTE Mobile UI foundation

### Objective

Create the smallest reusable visual/interaction system needed by the first real surfaces.

### Build only from real usage

Likely primitives include typography, spacing/layout helpers, surface/card, button/icon button, app header and loading/empty/error states. Inputs, dialogs, bottom sheets and more advanced primitives wait until a real screen requires them.

### Quality dimensions

- light/dark appearance strategy;
- shared semantic design-token consumption;
- touch target/accessibility semantics;
- dynamic text/readability;
- safe area and keyboard behavior;
- responsive width/max-width behavior;
- motion guidelines;
- Android native feel without losing DANTE identity.

### Exit gate

The first product screens can be assembled without one-off visual constants everywhere, while the UI layer remains small and capability-independent.

---

## M03 — Authentication shell and contract checkpoint

### Objective

Design the real unauthenticated/authenticated app lifecycle and determine what is required for production authentication.

### First step is inspection, not coding

Inspect repository/backend AuthN truth and determine:

- existing identity/account/session model;
- supported login methods;
- token/session transport;
- refresh/revocation/expiry semantics;
- secure-storage requirements;
- account creation/recovery needs;
- backend AuthZ boundary.

### Possible Mobile surfaces

Only after contract truth is known:

- welcome/onboarding entry;
- sign in;
- sign up if supported;
- recovery if supported;
- session-restoration state;
- logout/session-expired UX.

### Cross-boundary warning

Real auth will likely require secure native storage and possibly backend/shared changes. Those changes are not implied by this roadmap and require their own scope approval.

### Exit gate

No fake production auth. Real session lifecycle, storage and route protection are backed by the actual backend contract and direct validation.

---

## M04 — Home v0

### Objective

Build the first true DANTE product surface.

Home must answer product questions rather than merely display decorative cards:

- where am I in DANTE now;
- what matters now/today;
- what requires attention;
- what meaningful action can I take;
- how do I reach the rest of DANTE quickly.

### Constraints

- do not invent canonical data not supplied by the backend/product model;
- placeholder/skeleton data must be visibly noncanonical development state;
- visual identity can advance here, but behavior/hierarchy comes first;
- responsive/adaptive layout is required from first implementation.

### Exit gate

Home is coherent, navigable and visually intentional even if some future data modules are not yet connected.

---

## M05 — Stable supporting surfaces

### Objective

Advance product areas whose contracts are stable and do not depend on the moving Temporal vertical.

Candidates are selected at execution time, potentially including settings, profile/account surfaces, appearance/preferences, application information or stable global navigation/search infrastructure.

Do not build a screen solely because it appears in this candidate list.

### Exit gate

Each selected surface is end-to-end coherent and meets the Mobile quality bar before another is opened.

---

## M06 — Temporal integration checkpoint

### Objective

Reconcile Mobile against the then-current Temporal vertical before implementing Timeline/Create/Planning semantics.

### Required review

- Activity/Event/Routine distinctions;
- Schedule semantics;
- recurrence/occurrence state;
- temporal constraints;
- product organization/life areas/tags as applicable;
- API/read-model stability;
- Web implementation as evidence, not as a UI template;
- current branch/main integration state.

### Output

Select the first Mobile Temporal slice and define its exact product contract.

### Exit gate

The chosen Temporal slice depends on stable enough canonical semantics that Mobile will not knowingly encode obsolete distinctions.

---

## M07 — First real Mobile vertical

### Objective

Deliver one complete capability instead of many partial screens.

A vertical must cover, as applicable:

- navigation entry;
- real backend data/operation boundary;
- loading/content/empty/error states;
- mutation feedback;
- session/auth behavior;
- offline/degraded-network truth where relevant;
- accessibility;
- responsive behavior;
- device validation;
- tests appropriate to risk.

Candidate selection occurs at M06; no capability is precommitted here.

### Exit gate

A real user flow can be demonstrated end-to-end with truthful data semantics and production-quality interaction states.

---

## M08 — Release-quality hardening

### Objective

Raise the accumulated Mobile app from development-complete to release-candidate quality.

### Areas

- crash/error observability;
- cold/warm startup;
- rendering/jank/memory profiling;
- Android system Back/predictive Back;
- accessibility pass;
- keyboard/input behavior;
- deep links;
- session expiry/revocation;
- slow/degraded network;
- background/foreground lifecycle;
- responsive phone/tablet/foldable windows;
- real-device matrix;
- E2E critical flows;
- icon/splash/application identity;
- build/signing/release configuration;
- store-readiness checks.

This milestone can begin partial quality work earlier; it is listed separately because final release evidence is broader than feature completion.

---

## iOS activation — separate release track

iOS is intentionally not a current milestone. When activated:

1. review all platform adapters and native dependencies;
2. add/configure bundle identity and signing;
3. validate layout/navigation against iOS conventions;
4. validate secure storage, deep links, keyboard, safe areas, permissions and lifecycle;
5. perform iOS-specific accessibility/performance QA;
6. activate TestFlight/App Store release gates.

The target is adaptation and validation, not a second application rewrite.

## Definition of progress

Progress is not lines of code, screen count or installed libraries.

A milestone counts as complete only when:

- its scope is implemented;
- direct validation evidence exists;
- known failures are explicit;
- architecture remains within agreed boundaries;
- documentation reflects changed decisions;
- repository state is clean relative to the approved scope.