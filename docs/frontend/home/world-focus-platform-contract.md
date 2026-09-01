# DANTE — World Focus Platform Contract v0

**Status:** CURRENT WORKING PLATFORM CONTRACT — PRE-IMPLEMENTATION / PRE-BACKEND  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Scope:** World Focus application/platform architecture inside the already-frozen World Focus structural shell and workspace. This document intentionally excludes final visual skin/VFX and does not authorize backend, database, provider or real-LLM integration.

---

# 0. Purpose, authority and change boundary

This document turns the accumulated World Focus product research, scenario work, frontend architecture, production-readiness contracts, DANTE product identity, current database/domain constraints and current Intelligence Platform direction into one implementation-oriented platform contract.

It exists to reduce the risk of a future rewrite caused by prematurely freezing page-specific UI, data shapes, AI plumbing or layout behavior.

It consumes, without redefining:

- `docs/product/product-identity-and-north-star.md`;
- `docs/product/feature-discovery-simulation-2026-08.md`;
- `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`;
- `docs/product/v1-adaptive-intelligence-and-future-social.md`;
- closed Domain / Logical / Physical authorities;
- current Database source-of-record documentation;
- `docs/frontend/production-readiness/component-architecture.md`;
- `docs/frontend/production-readiness/backend-integration-contract.md`;
- `docs/frontend/production-readiness/quality-gates.md`;
- `docs/frontend/home/world-focus-architecture.md`;
- `docs/frontend/home/world-focus-wf0-scenario-oracle.md`;
- `docs/frontend/home/world-focus-structural-contract.md`;
- `docs/frontend/home/world-focus-geometry-contract.md`;
- `docs/frontend/home/world-focus-wf1-checkpoint.md`.

Where this document is more specific than the older World Focus architecture document about the **interior application platform**, this is the newer working contract. It does **not** reopen WF0 structure or WF-G3 geometry.

This document is intentionally exhaustive about ownership and invariants, but it is not a pixel-layout freeze. Exact UI placement, exact first module set, exact production numeric budgets, exact backend endpoints and exact persistence schema remain later gates.

---

# 1. Product statement

World Focus is the application surface for:

> **Understand this part of my life and continue from here.**

It is not:

- a generic analytics dashboard;
- a folder browser;
- a page-per-World template system;
- a chatbot with cards attached;
- a universal `WorldItem` database model;
- a free-form website builder;
- a replacement for specialist tools;
- a new canonical ontology above DANTE Domain owners.

The architecture must remain useful when a World is:

- quantitative or mostly qualitative;
- sparse or dense;
- finite or persistent for years;
- centered on a Goal or with no Goal at all;
- personal, multi-actor or partly external-provider-backed;
- familiar today or completely unknown to the current product team.

---

# 2. Permanent semantic invariants

```text
World != canonical Domain owner
World != folder
World != life-area taxonomy
World != universal relation container
WorldProjection != canonical truth
ModuleConfig != canonical source data
ModuleProjection != canonical source data
LayoutConfig != Domain semantics
AI output != accepted fact
AI proposal != user Decision
Tool call != authorization
Provider state != DANTE canonical state
Planned != actual
Effort != execution != outcome != Goal progress
Observation != causation
Observed pattern != confirmed preference
Absence != false
UI hiding != authorization
```

One canonical DANTE reality may be projected into several Worlds without canonical duplication.

Removing a module from a World never implies deleting the Goal, Event, Session, Person, Place, Artifact or other reality that supplied it.

---

# 3. Architecture thesis

World Focus is a **small application platform**, not a dashboard engine pretending to be a page.

Target ownership:

```text
WORLD FOCUS HOST
  route · lifecycle · entry/exit · page boundary
            │
            ▼
WORLD FOCUS SESSION
  active World · Lens · selection · request generations
            │
   ┌────────┴──────────────────────────────┐
   ▼                                       ▼
APPLICATION / PROJECTION BOUNDARY    INTERACTION COORDINATOR
   │                                       │
   │                                       ├─ contextual DANTE
   │                                       ├─ Peek
   │                                       ├─ Insight
   │                                       ├─ Explore
   │                                       └─ proposal/action surfaces
   │
   ├─ bootstrap
   ├─ bounded projections
   ├─ capability invocation
   ├─ provenance/freshness
   └─ typed source/action intents
            │
            ▼
COMPOSITION PLATFORM
   ├─ stable composition
   ├─ adaptive region
   ├─ module host
   └─ module registry
```

Cross-cutting concerns are not separate runtime managers. They are contracts applied across these owners:

- accessibility;
- performance;
- security/privacy/disclosure;
- localization/time/units;
- observability;
- testability;
- versioning/evolution;
- responsive behavior.

The implementation should prefer fewer explicit owners over a chain of managers, global stores or event buses.

---

# 4. Top-level ownership

## 4.1 World Focus Host

Owns:

- `/worlds/:worldId` route lifecycle;
- entry and return source;
- browser navigation/back semantics;
- top-level usable/unavailable/error boundary;
- restoration of focus where appropriate;
- mounting/unmounting the World Focus application surface;
- integration with the frozen World Focus shell/workspace.

Does not own:

- module data semantics;
- backend authorization;
- AI orchestration internals;
- per-World page branching;
- persistence schema;
- visual VFX implementation.

## 4.2 World Focus Session

A feature-local session owns only the current interaction context:

```text
activeWorldId
WorldLens
currentSelection / exploration context
request/generation ownership
transient surface state reference
customization mode reference
```

It is not a second canonical store and must not duplicate source-backed data already owned by the data/server-state layer.

The session should be implementable with narrow React state/reducer primitives until real complexity proves that a broader state library is required.

## 4.3 Application / Projection Boundary

This is the only frontend-facing boundary to future backend/application functionality.

It owns frontend needs, not transport mechanics:

```text
load World bootstrap
load/refine bounded projections
inspect source/detail
invoke approved capability
request contextual Insight
apply validated personalization command
submit/accept/reject application proposal when allowed
```

Current deterministic fixtures satisfy this boundary without pretending to be a real backend.

Future transport/client adapters satisfy the same frontend needs through validated contracts.

## 4.4 Composition Platform

Owns:

- stable composition resolution;
- bounded adaptive content placement;
- deterministic module ordering/presentation;
- responsive layout policy;
- module host and module registry;
- customization draft/application behavior.

It never derives Domain meaning from a label, color, World name or arbitrary ID.

## 4.5 Interaction Coordinator

Owns transient exploration and application-facing interactions:

- DANTE contextual entry;
- Peek / Insight / Explore lifecycle;
- source/detail inspection handoff;
- action proposal and confirmation presentation;
- focus/history semantics for transient surfaces.

It does not become a generic modal manager for the whole app.

---

# 5. Required model separation

The platform must preserve these separate concepts.

## 5.1 Canonical Reality

Owned by DANTE Domain/application/backend.

Examples include Goal, Plan, Activity, Event, Routine, Occurrence, Session, Observation, Person, Place, Asset, Content Artifact and accepted derived/application semantics.

## 5.2 World Descriptor

Presentation/product identity for the focused World.

It may contain a display identity/theme/profile, but is not automatically a canonical Domain owner or DB row.

## 5.3 CompositionConfig

Durable or deterministic configuration describing **what the stable World surface should contain and how it should be presented**.

Conceptually:

```text
layoutSchemaVersion
compositionOwnership
moduleConfigs[]
layout/order/presentation profile data
optional base/default provenance
```

## 5.4 ModuleConfig

Answers:

> What should this stable module keep showing?

It stores a stable approved query/capability/configuration intent, not current result values.

Conceptually:

```text
instanceId
kind
moduleConfigVersion
capability/source configuration
bounded parameters
Lens participation policy
presentation profile
user label/metadata when allowed
```

## 5.5 ModuleProjection

Answers:

> What is true/showable for this module right now?

Conceptually:

```text
instanceId
kind
status
validated semantic payload
basis / scope
freshness / asOf
provenance / method when required
available semantic actions
```

`ModuleConfig` and `ModuleProjection` are deliberately separate so persistent UI configuration can survive changing values.

## 5.6 AdaptiveCandidate

A bounded, non-pinned current-relevance candidate produced by authorized application logic, not by arbitrary frontend ranking over raw life data.

## 5.7 InsightProjection

A typed transient result for contextual exploration.

It may contain:

```text
narrative summary
primary typed presentation
bounded supporting evidence/presentation blocks if justified
scope/Lens basis
provenance/freshness/uncertainty
available next semantic actions
promotability metadata
```

It is not arbitrary generated UI.

## 5.8 Proposal / Effect presentation

Information, recommendation, proposal, effect execution and receipt are separate states and must not be collapsed into one “AI answer”.

---

# 6. Stable / adaptive / ephemeral is one dimension, origin is another

The existing product classes remain:

```text
STABLE
ADAPTIVE
EPHEMERAL
```

But they must not be confused with who created them.

Origin/ownership metadata is a separate axis:

```text
SYSTEM_DEFAULT
USER
DANTE_PROPOSED
APPLICATION_DERIVED
```

Examples:

```text
new untouched World default
= STABLE + SYSTEM_DEFAULT

user customized module
= STABLE + USER

DANTE temporary answer
= EPHEMERAL + DANTE_PROPOSED

current risk surfaced by application relevance
= ADAPTIVE + APPLICATION_DERIVED

Insight explicitly promoted by user
= STABLE + USER
```

DANTE does not silently turn an ephemeral/adaptive object into user-owned stable composition.

---

# 7. Initial Composition Resolver

Unknown future Worlds require a deterministic first-use behavior.

When no accepted user composition exists, the platform resolves a useful initial composition from bounded available presentation capabilities/projections.

Conceptual flow:

```text
World context
+ available approved module candidates
+ product/default policy
+ current projection availability
-> deterministic initial composition
```

Rules:

- sparse Worlds stay sparse;
- qualitative Worlds do not receive fake KPI cards;
- missing data never creates ghost entities;
- a large World receives summaries and deeper entry points rather than an infinite surface;
- specialist modules are selected only when their semantics are actually supported;
- default resolution is deterministic for the same effective input/policy version;
- the resolver does not write canonical reality merely to fill UI.

## 7.1 Default evolution

A future product update may improve system defaults.

Two states must be distinguished:

### System-managed stable composition

The user has not materially customized it. Compatible system-default evolution may update it through an explicit default/config evolution policy.

### User-managed stable composition

The user has customized it. Product upgrades must not silently rearrange/remove user-owned structure merely because defaults changed.

New useful capabilities may be suggested or offered for addition, but user-managed composition remains user-owned.

This prevents future default improvements from overwriting established user intent.

---

# 8. Composition architecture

Do not build a free-coordinate website-layout engine unless a validated product case later requires one.

Initial target:

```text
ordered stable composition
+ bounded adaptive region
+ discrete presentation profiles
+ CSS layout/container behavior
```

Prefer semantic/discrete profiles such as:

```text
compact
standard
wide
full
```

rather than persistent pixel coordinates.

Exact names remain an implementation gate.

## 8.1 Layout ownership

- parent composition owns outer placement;
- module owns only its inner layout;
- module must not patch global viewport geometry;
- container geometry, not duplicated JS breakpoints, should govern responsive module presentation;
- CSS Grid/Flex and container queries are preferred where sufficient;
- JS measurement is reserved for real chart/canvas/geometry requirements.

## 8.2 Normal scroll ownership

Default vertical flow is page/workspace scroll.

Avoid multiple nested scroll panes.

Large browsing experiences should usually use:

```text
bounded summary -> Explore/detail
```

## 8.3 Future structural growth

The persisted layout contract must not assume that the only future layout is one flat list forever.

It should remain evolvable toward bounded sections/tabs/grouping if real dense-World evidence later requires them, without introducing page-per-World branching.

Do not implement tabs/section trees now merely for hypothetical extensibility.

## 8.4 Composition budget

Do not freeze an arbitrary module maximum before profiling.

The quality matrix must at least pressure:

```text
4 modules
8 modules
12 modules
20-module stress case
```

The production maximum, if any, is chosen from comprehension, responsive quality, accessibility, payload and render measurements.

---

# 9. Module semantics and registry

WF0 candidate semantic families remain the current starting grammar:

```text
metric
trend
comparison
breakdown
trajectory
planned-actual
timeline
collection
context
pipeline
```

They are not yet a promise that all ten ship in the first slice.

Semantic kind answers the question being represented; presentation variant answers how it is shown.

Example:

```text
trend -> line / bars / bounded range
```

must not become three unrelated module kinds if the semantic question is unchanged.

## 9.1 Registry contract

The registry should remain deliberately small:

```text
kind
contract/version compatibility
projection validator
renderer
supported presentation profiles
supported cross-boundary semantic actions
optional lazy loader
```

It must not become a dependency-injection/service-locator container.

Common loading/error chrome belongs to `ModuleHost` where semantics permit.

## 9.2 Specialist modules

A specialist module is allowed only when generic modules materially fragment or misrepresent one coherent interaction.

Current strongest candidate remains a travel itinerary representation combining time/place/transport/booking/participation.

Specialist modules:

- extend the registry;
- can be lazy-loaded;
- obey the same lifecycle/a11y/performance/error contracts;
- do not fork World Focus;
- do not create a new canonical Domain owner.

## 9.3 Unknown kind

Unknown module kind:

- never executes remote code;
- never evaluates arbitrary component paths;
- fails safely;
- produces development/telemetry evidence;
- preserves the rest of the World.

---

# 10. World Lens and exploration context

`WorldLens` is bounded presentation/query context, not a universal query language.

Initial responsibility may include:

```text
selected time range
selected sub-scope/category where supported
temporary user filter/selection
```

Do not create arbitrary predicates/operators/SQL-like expressions.

Each stable module declares a participation policy conceptually equivalent to:

```text
INHERIT
FIXED
DERIVE
IGNORE
```

Exact naming is deferred.

A pinned module may intentionally keep a fixed saved scope while other modules follow the current Lens.

Lens changes are ephemeral unless the user explicitly changes/saves a module configuration.

Only useful restorable/shareable state should later be reflected in URL search state. Hover state, temporary chart selection and incidental component state do not belong in browser history.

---

# 11. Semantic interactions across ownership boundaries

Do not build a global event bus.

DOM/component-local interactions remain local.

Only interactions that cross a feature/application ownership boundary become typed semantic intents/commands.

Candidate classes include:

```text
OPEN_DETAIL
OPEN_SOURCE
OPEN_SCOPED_COLLECTION
SET_WORLD_LENS
RESET_WORLD_LENS
REQUEST_INSIGHT
REFINE_INSIGHT
DISMISS_INSIGHT
EXPLORE_INSIGHT
PROMOTE_INSIGHT
OPEN_CUSTOMIZE
APPLY_COMPOSITION_DRAFT
CANCEL_COMPOSITION_DRAFT
PROPOSE_ACTION
ACCEPT_PROPOSAL
REJECT_PROPOSAL
```

Do not encode transient UI events such as hover, legend collapse or local menu state as platform-level intents.

---

# 12. Data loading and projection strategy

World Focus must not become one-request-per-widget.

Use three conceptual loading classes:

```text
CRITICAL
DEFERRED
ON_DEMAND
```

## CRITICAL

Enough to make the World understandable and stable on open.

## DEFERRED

Secondary/offscreen projections that can load after the usable surface without disruptive layout shift.

## ON_DEMAND

Explore details, large collections, artifact bytes, high-volume history, specialist-heavy data and similar deep work.

The future backend may provide a bootstrap/aggregate projection endpoint or another batching strategy, but this frontend contract does not invent HTTP endpoints.

## 12.1 Projection coherence

A World must not show mutually confusing values merely because separate projections resolved at different instants.

Critical projection bundles must provide either:

- a coherent common read/generation basis; or
- truthful per-projection freshness/as-of metadata when sources legitimately differ.

Provider-backed values may be older than canonical DANTE data; this is acceptable when surfaced truthfully.

Conceptual metadata may include:

```text
projectionGeneration / request generation
asOf
source freshness
provider freshness
```

Exact transport fields are future API scope.

## 12.2 Stale completion protection

```text
open Musica
start request A
switch to Viaggi
A resolves late
```

Late A must not overwrite active Viaggi state.

Use AbortSignal/request identity/generation ownership as appropriate.

## 12.3 Read request lifetime != durable execution lifetime

Ordinary obsolete projection requests should be cancelable on route/context changes.

A future durable Intelligence run or approved external effect may legitimately outlive the current React surface. Unmounting World Focus must not imply that a durable backend execution was cancelled unless cancellation was explicitly requested and supported.

The UI may later reattach to a durable run by stable run identity.

This separation is required for future governed/long-running Intelligence workflows.

---

# 13. Server state and cache boundary

Source-backed projections need explicit identity, freshness, cancellation, retry and invalidation semantics when the real backend lands.

Do not select a server-state library merely for enterprise appearance.

Current TanStack Router may coordinate critical route loading/preloading/deferred loading while the product remains small enough.

A future external server-state cache is justified when real requirements prove needs such as:

- cross-route shared data identity;
- fine-grained invalidation;
- mutation orchestration;
- optimistic cache coordination;
- long-lived deduplication beyond route scope.

If such needs appear, the router remains the navigation/load coordinator rather than becoming a competing canonical cache.

---

# 14. Adaptive intelligence policy

Adaptive content must be useful without becoming unstable or intrusive.

The authoritative application/intelligence layer should produce disclosure-safe `AdaptiveCandidate` values rather than the frontend scanning arbitrary life data and inventing relevance.

Candidate metadata may conceptually include:

```text
stable candidate identity
reason/explanation handle
priority/relevance class or score
freshness
validity window / expiry when applicable
source/evidence references
sensitivity/presentation metadata when applicable
```

The frontend owns only display policy such as:

```text
bounded capacity
stable placement
hysteresis / anti-jitter
user dismissal/snooze lifecycle
local replacement timing
```

## 14.1 Hysteresis

Small relevance changes must not cause visible items to continually reorder or swap.

Adaptive UX optimizes for **stable usefulness**, not instantaneous ranking purity.

## 14.2 Dismissal

A dismissed adaptive item requires stable identity so the same unchanged condition does not immediately reappear.

Future application policy may define when a materially changed/new condition is eligible to resurface.

## 14.3 Scope boundary

Adaptive Region is not:

- the Review Queue;
- a Notification Center;
- an error log;
- a second task list.

It may point into those features when relevant.

## 14.4 User ownership

Adaptive content cannot silently move/remove user-managed stable modules.

If DANTE believes a stable addition would be useful, it may propose it; persistence requires an accepted flow.

---

# 15. DANTE Intelligence integration boundary

World Focus must **not** implement a parallel AI architecture.

It consumes the future DANTE Intelligence Platform through application/intelligence contracts.

Current Intelligence direction assumes, among other things:

- DANTE-owned orchestration;
- contextual/capability-based execution rather than raw DB/API access;
- provider/model gateway behind stable application semantics;
- governance before disclosure/tool/effect execution;
- proposal/effect/receipt separation;
- durable execution only for workflows that require it;
- structured result envelopes independent of any one model/provider/protocol;
- audit distinct from ordinary observability.

World Focus therefore acts as a **presentation/context adapter**, not as the Intelligence control plane.

## 15.1 Context envelope

World Focus may supply bounded interaction context such as:

```text
active World identity/context reference
current World Lens
selected module/source reference
current exploration reference
entry/surface context where relevant
```

It must not serialize the entire React tree or treat client-supplied context as authorization/canonical truth.

The authoritative Context Engine/application layer reconstructs and filters the usable context.

## 15.2 Structured result mapping

Future structured DANTE results may be adapted into `InsightProjection` / proposal presentations.

World Focus must not make A2UI, MCP, A2A, a model-specific schema or another external protocol its internal application contract.

Protocols/providers remain adapters at appropriate boundaries.

## 15.3 Streaming lifecycle

The interaction model must be able to represent future phases such as:

```text
requesting
streaming narrative/progress
capability/tool work
partial structured result
validated completion
cancelled
failed
```

Do not claim final facts merely because streamed model text mentioned them before validation/application completion.

## 15.4 Information / proposal / effect separation

The UI must distinguish:

```text
INFORMATION
SUGGESTION / RECOMMENDATION
PROPOSAL
PERMISSION / CONFIRMATION
EXECUTION ATTEMPT
RECEIPT / OUTCOME
RECONCILIATION when needed
```

A consequential operation is not complete because an LLM said it was done or because a tool call was attempted.

The future governed flow may conceptually follow:

```text
EffectIntent -> Permit -> Attempt -> Receipt -> Reconciliation
```

World Focus displays the relevant stages but does not own governance semantics.

## 15.5 Autonomy

User/product autonomy policy may permit different behavior by scope/consequence.

World Focus must support this without hard-coding one universal confirmation rule.

However, adaptive UI rearrangement remains bounded by the stable composition ownership rules even if some other application actions have higher autonomy.

---

# 16. Interaction depth != presentation surface

Semantic depth:

```text
PEEK
INSIGHT
EXPLORE
```

is distinct from the concrete responsive presentation mechanism:

```text
inline
popover
sidecar/drawer
modal
full-screen
route
```

Example:

- desktop Insight may be a sidecar;
- narrow viewport Insight may become full-screen;
- semantic depth remains `INSIGHT`.

This prevents screen-size choices from infecting application semantics.

## 16.1 Stack policy

Default rule:

```text
one primary transient exploration surface
+ optional confirmation/action surface when required
```

`Peek -> Insight -> Explore` is promotion/replacement, not an infinite nested modal stack.

## 16.2 Navigation/focus

Every transient depth must define:

- open trigger;
- Escape/back behavior;
- focus entry;
- focus restoration;
- browser-history participation if any;
- responsive transformation;
- loading/error state.

True modal surfaces obey modal focus/inertness semantics.

---

# 17. Insight promotion into stable composition

An ephemeral result becomes persistent only when it can be represented as a stable approved `ModuleConfig`.

Correct shape:

```text
Insight result
+ promotable capability/source identity
+ validated bounded parameters
+ selected presentation profile
+ explicit accepted user action
-> ModuleConfig
```

Forbidden durable definitions:

```text
raw generated HTML
raw JSX/React component path
arbitrary JavaScript
arbitrary SQL
model-generated executable query
prompt text as sole execution semantics
current result values pretending to be future source
```

Prompt/original request may be retained later as provenance/history/label, not as the only executable contract.

---

# 18. Personalization / Customize mode

Normal World consumption remains clean.

Customization is a deliberate mode.

Minimum conceptual state:

```text
VIEW
  -> CUSTOMIZE_DRAFT
      -> APPLY
      -> CANCEL
```

The draft may support reorder, add/remove and bounded presentation-profile changes as product design validates them.

Undo/redo is not mandatory in the first slice; architecture must not make it impossible later.

## 18.1 Transaction semantics

During customization, edits operate on a draft representation.

`Cancel` restores the pre-edit accepted composition.

`Apply` validates and accepts the new composition through the current adapter.

Future cross-device persistence must use expected-state/revision/concurrency semantics rather than silently overwriting a newer accepted configuration.

## 18.2 Remove semantics

Remove-from-World removes presentation/configuration only.

It never means delete source reality unless the user explicitly invokes a separate canonical delete action through the owning feature.

## 18.3 DANTE-driven customization

If the user explicitly asks DANTE to alter layout, Intelligence may produce a bounded personalization proposal/config command.

It still passes through the same composition validation/ownership rules; no model writes arbitrary layout state directly.

---

# 19. Multi-actor, privacy and disclosure compatibility

World Focus must remain compatible with future shared/coordination scenarios without implementing collaboration prematurely.

Principles:

```text
shared canonical fact != private personal overlay
person != account
participant != owner
responsibility != generic relation
absence of disclosed data != proof of absence
```

Projection payloads must already be disclosure-safe before React receives them.

Frontend hiding is not authorization.

A generic `context` module may show people/roles supplied by authoritative semantics, but must not invent a generic relationship ontology.

Future role labels such as Responsible, Participant, Reviewer or Subject remain application/domain semantics, not new universal World roles.

Aggregates and explanations must not leak concealed records through counts, reasons or existence placeholders.

---

# 20. Rich-content and browser security boundary

AI text, imported artifacts, provider labels, user text and external URLs are untrusted content at rendering boundaries.

Rules:

- plain text by default;
- approved/sanitized rich-text grammar only where a product requirement exists;
- no model/provider arbitrary HTML execution;
- no arbitrary iframe/embed execution;
- safe URL/protocol policy;
- no `javascript:`-style executable links;
- no secrets/tokens in module/view-model logging;
- sensitive data must not be placed in uncontrolled persistent browser storage merely for convenience;
- future CSP/session/CSRF strategy follows the real deployment contract.

Local deterministic fixtures do not justify production `localStorage` architecture.

---

# 21. Localization, timezone, units and formatting

World Focus is inherently exposed to money, duration, dates, timezone, distance, quantities, percentages and custom units.

Do not persist or transport translated labels as identifiers.

Do not reduce semantically meaningful values to preformatted display strings too early.

Presentation contracts should preserve enough typed information for locale-aware rendering when needed, for example:

```text
numeric value
currency / unit
instant / local-time semantics
timezone when materially relevant
format/display intent
```

Travel and cross-timezone scenarios are mandatory tests.

Use existing DANTE i18n/time utilities where applicable rather than ad-hoc `Date` formatting in each module.

---

# 22. Accessibility contract

Target: WCAG 2.2 AA unless a later explicit requirement is stricter.

Accessibility is part of module/surface design from the beginning, not a WF7 patch.

Required:

- semantic headings/regions/controls;
- keyboard-only operation;
- deterministic visible focus;
- correct accessible names/roles/states;
- reduced-motion behavior;
- 200%+ zoom/text pressure validation where applicable;
- no color-only meaning;
- meaningful chart summary/alternative path when visual graphics alone are insufficient;
- focus entry/containment/restoration for true modal surfaces;
- drag operations have a non-drag equivalent;
- pointer target sizing/spacing satisfies WCAG 2.2 requirements;
- touch and keyboard alternatives remain behaviorally equivalent where feasible.

Automated axe checks are necessary but not sufficient; critical flows require manual keyboard/focus/reading-order review.

---

# 23. Performance architecture

Performance is correctness for World Focus.

## 23.1 Code

- core World Focus route/shell remains small;
- specialist modules code-split/lazy-load when justified;
- heavyweight chart/map/3D libraries are not eagerly bundled by default;
- do not add a dependency because it is fashionable or “enterprise”.

## 23.2 Data

- critical data bounded;
- large source histories aggregated/downsampled before reaching normal modules;
- collections page/window/virtualize only in deep views where required;
- artifact metadata before bytes;
- no all-life-data load for one World;
- no default one-request-per-widget architecture.

## 23.3 Rendering

- module-local updates should not rerender the whole World;
- stable instance identities;
- avoid high-churn top-level Context values;
- CSS layout before JS layout;
- `content-visibility`/containment may be evaluated for long offscreen composition after profiling, with intrinsic sizing and accessibility verified;
- no persistent expensive RAF/animation loop for static content.

## 23.4 Performance measures

General field goals should remain compatible with current Core Web Vitals guidance:

```text
LCP <= 2.5s
INP <= 200ms
CLS <= 0.1
at 75th percentile where field measurement applies
```

World Focus also needs product-specific measures after real rendering exists:

```text
route -> usable World
World switch latency
critical projection latency
Peek open latency
Insight first meaningful response
Insight validated completion
specialist lazy-load latency
customize interaction latency
memory/resource cleanup over repeated use
```

Numeric product budgets are frozen only after representative profiling.

---

# 24. Resilience and failure isolation

Minimum state vocabulary across relevant boundaries:

```text
loading
ready
partial
stale
empty
error
unavailable
```

Not every object must implement every state.

Rules:

- `empty != error`;
- `unavailable != empty`;
- unknown/missing != explicit negative;
- one secondary module failure does not destroy an otherwise usable World;
- AI unavailable does not make the World unavailable;
- provider stale/unavailable degrades locally;
- specialist lazy-load failure is isolated;
- no infinite retry loop;
- cleanup listeners/observers/timers/RAF/resources on lifecycle exit;
- retry policy depends on operation semantics;
- consequential mutation/effect failures must remain truthful and recoverable.

---

# 25. Offline and sync future boundary

Current pre-backend work does not activate offline persistence or PowerSync.

Future synced/local copies remain noncanonical.

World Focus must avoid assumptions that make offline impossible, but must also avoid pretending local fixtures are durable sync.

Potential future categories differ:

- stable UI preference/config synchronization;
- read projections available from client-safe sync;
- consequential canonical mutations requiring backend authority/revalidation;
- provider/Intelligence operations that may be unavailable offline.

Offline absence must never be rendered as canonical negative state.

---

# 26. Observability vs audit

World Focus should expose instrumentation boundaries without coupling to a vendor.

Potential frontend operational events/measures:

```text
World open started / usable / failed
projection load latency/failure/bytes
module renderer/lazy-load error
Insight request / first response / completion / failure
surface open/close
customize start/apply/cancel/conflict
long task / render pressure / resource leak indicators
```

Telemetry must avoid sensitive World payloads by default.

Frontend observability is not the authoritative audit trail for consequential Intelligence/application effects.

Future audit records belong to the governed application/Intelligence/backend architecture.

---

# 27. Versioning and evolution

Version what must survive time; do not scatter version numbers across every transient payload.

Required durable evolution handles:

```text
layoutSchemaVersion
moduleConfigVersion (or module-kind config schema version)
```

Breaking transport/API/capability evolution belongs to the future backend/application contract and generated/validated client boundary.

Old stable configuration must either:

```text
migrate deterministically
remain supported
or render a truthful recoverable unsupported state
```

Never silently discard an old user-owned module because a renderer/config changed.

Migrations are pure/deterministic where possible and receive fixture regression tests.

---

# 28. Feature rollout / kill-switch compatibility

Future production needs a way to activate/deactivate risky/new capabilities without rewriting the composition engine.

Examples:

- new specialist module;
- experimental adaptive policy;
- new Intelligence insight family;
- provider-dependent projection;
- new presentation variant.

Do not select a feature-flag vendor now.

The architecture only requires that availability is declarative/capability-driven so an unavailable/disabled feature degrades truthfully rather than leaving broken saved composition.

A disabled saved module is not silently deleted.

---

# 29. Frontend technology policy

Current stack includes React 19, TanStack Router, Vite, Vitest, Playwright and axe integration.

Do not add by default:

```text
XState
Zustand/Redux/global store
TanStack Query
react-grid-layout
runtime plugin loader
generic event bus
generic DI/service locator
remote component execution
arbitrary JSON-to-UI framework
```

Any addition requires a demonstrated problem that the existing primitives cannot solve cleanly.

Prefer:

- feature-local reducers/state;
- React error boundaries at meaningful isolation levels;
- TanStack Router for route lifecycle/critical loading/preload;
- CSS Grid/Flex/container queries for layout;
- typed discriminated unions and narrow ports/adapters;
- code splitting at real expensive/specialist boundaries.

---

# 30. Visual skin/VFX boundary

The current visual/VFX candidate is explicitly not part of this platform contract.

Permanent rule:

```text
visual skin fits frozen shell/workspace geometry
platform/application semantics do not depend on visual skin
```

The future replacement visual treatment may supply declarative theme/decorative parameters but cannot:

- become layout authority;
- hide/recompose the App Shell/Topbar;
- become navigation correctness;
- become source-data truth;
- require per-World bespoke application architecture.

World Focus must remain fully operable with rich VFX disabled.

---

# 31. External product/architecture evidence — principles adopted, products not copied

This contract was re-reviewed on 2026-09-01 against current mature product/framework patterns.

## Notion Dashboard views

Observed principles:

- deliberate View/Edit separation;
- bounded widget density (current product limits up to 4 per row and 12 total);
- high-level summary -> drill into source data;
- explicit warning against large/unfiltered dashboard loads.

DANTE adoption:

```text
clean consume mode
bounded composition
summary -> Explore/source
measure before choosing our own numeric budget
```

Do not adopt Notion's database-centric ontology.

## Grafana Scenes / Dynamic Dashboards

Observed principles:

- explicit separation/composition of data, time range, variables, layout and visualization;
- nested context inheritance;
- state not tied directly to rendered React component lifetime;
- URL sync only for selected state;
- flex/grid layouts and lazy behavior;
- large dashboard architecture migrations are expensive when concerns become mixed.

DANTE adoption:

```text
World Lens separate from renderer
projection lifetime/identity separate from DOM
selective URL state
module/config/layout separation
avoid a monolithic dashboard JSON/blob
```

Do not copy Scenes' entire object-model framework.

## Home Assistant

Observed principles:

- useful dashboard generated from available devices out of the box;
- user can later construct focused/custom dashboards;
- sections provide constrained organization.

DANTE adoption:

```text
Initial Composition Resolver
system-managed default -> user-managed composition
bounded future sections only when proven
```

Do not adopt Home Assistant entity semantics or unrestricted community runtime cards.

## Apple Smart Stack / WidgetKit relevance

Observed principles:

- relevance uses contextual/behavioral clues;
- relevance may include score/duration;
- contextual content may rotate while user-selected widgets can be pinned.

DANTE adoption:

```text
AdaptiveCandidate relevance window
bounded adaptive budget
stable user ownership
anti-jitter/hysteresis
```

DANTE relevance remains governed by DANTE semantics, not an imitation of WidgetKit ranking.

## Linear Peek

Observed principle:

- inspect details without losing list/board context;
- deterministic keyboard close/navigation behavior.

DANTE adoption:

```text
Peek preserves World context
```

## Microsoft Copilot Pages / Anthropic Artifacts

Observed principle:

- AI conversation can explicitly promote a transient result into a durable/editable surface.

DANTE adoption is intentionally stricter:

```text
transient Insight
-> explicit user promotion
-> capability-backed typed ModuleConfig
```

No arbitrary AI-generated application UI becomes durable execution logic.

## TanStack Router

Observed principles:

- router coordinates critical route data early;
- supports cancellation, preload, cache and deferred data;
- external server-state layer is justified when more advanced sharing/mutation/invalidation requirements exist.

DANTE adoption:

```text
use current router capabilities first
add a server-state library only when real backend flows prove the need
```

## W3C / OWASP / Web performance guidance

Adopt:

- WCAG 2.2 AA target including drag alternative and pointer-target requirements;
- correct modal focus semantics;
- no sensitive data reliance on uncontrolled localStorage;
- current Core Web Vitals as external web-quality guardrails, supplemented by product-specific performance metrics.

---

# 32. Hard rejects

```text
one giant WorldFocus.tsx
one React page per World
WorldItem universal entity
world_id added blindly to canonical owners
one generic JSON blob pretending to be all module semantics
one generic optional-property mega-widget
AI-generated JSX/HTML/JavaScript execution
AI-generated SQL as durable widget definition
frontend SQL/provider access
frontend authorization inference
parallel World-specific AI runtime
one request per widget by architecture
load entire World history on open
arbitrary free-coordinate dashboard as first implementation
unbounded adaptive rearrangement
nested modal chain
persistent result snapshot presented as live widget source
uncontrolled sensitive localStorage persistence
silent last-write-wins customization conflict
provider failure rewriting canonical state
React unmount cancelling a durable backend effect by implication
mandatory KPI/progress slot for every World
mandatory Goal for every World
```

---

# 33. Mandatory test/invariant matrix

## World diversity

At least:

```text
Musica
Viaggi
Finanza
Studio
Corpo/Benessere
Relazioni qualitative
unknown future World
```

## Density

```text
empty
1–2 modules
4–8 normal
12 dense
20 stress
```

## Source states

```text
fresh
partial
stale
provider unavailable
module error
AI unavailable
```

## Interaction states

```text
normal View
Peek
Insight
Explore
Customize draft
proposal/confirmation
```

## Race/concurrency

```text
World A request resolves after switching to B
Lens changes rapidly
Insight refinement returns out of order
lazy module resolves after removal/navigation
customization applies against stale future revision
```

## Permanent invariants

```text
same effective composition input => deterministic placement
adaptive change => user-managed stable placement unchanged
remove module => source reality unchanged
AI unavailable => structured World remains usable
unknown module => controlled local failure
provider stale => canonical modules remain usable
old config => migrate/support/truthful recoverable state
cross-World projection => no canonical duplication
late request => cannot overwrite new World
no sensitive hidden-source leakage through aggregate/explanation
reduced motion => same functional outcome
keyboard-only => full critical-path capability
```

---

# 34. Future backend / vertical handoff requirements

The later full vertical begins only after frontend/product behavior is validated across contrasting Worlds.

The handoff must specify real requirements, not speculative tables/endpoints.

For each stable ModuleConfig / Insight capability family define:

```text
semantic input
bounded scope
required source owners
aggregation/downsampling needs
freshness expectation
provenance/method expectation
authorization/disclosure requirement
pagination/windowing
timezone/unit semantics
failure/partial semantics
cache/invalidation pressure
```

Validated future writes may include product-level configuration actions such as:

```text
create/configure/archive product World profile if accepted
pin/unpin stable module config
reorder/change presentation profile
accept DANTE proposal
promote Insight to stable ModuleConfig
```

These remain distinct from mutations to underlying Goal/Event/Session/etc.

The backend design must then re-read current Domain/Logical/Physical/Database authorities before selecting persistence consequences.

No `world` table is implied by this contract.

---

# 35. Decisions intentionally left open for block review

These are not architectural gaps. They require concrete UI/product evidence before freezing:

- exact internal workspace visual hierarchy;
- exact location/form of World Lens;
- exact location/form of DANTE entry;
- exact desktop/narrow presentation of Peek/Insight/Explore;
- exact first-shipping module subset;
- exact presentation profile names/dimensions;
- exact stable/adaptive visual balance;
- exact composition numeric budget;
- whether any specialist module ships in first implementation;
- exact server-state library after backend integration;
- exact persistent World/profile/layout DB model;
- exact transport/API endpoints;
- exact Intelligence ResultEnvelope adapter schema;
- exact feature-flag/observability vendors;
- final VFX/visual skin.

Each of these should be reviewed in a bounded logical implementation block rather than guessed globally.

---

# 36. Recommended implementation decomposition after this contract

The next phase should not implement the whole platform in one branch burst.

Recommended block order:

```text
B0  Contract review + package/file ownership map
B1  World Focus Session + bounded Lens model
B2  application/projection port + deterministic adapter + request generation
B3  ModuleConfig / ModuleProjection contracts + ModuleHost + registry
B4  Initial Composition Resolver + stable composition layout
B5  AdaptiveCandidate policy + bounded adaptive region
B6  first universal module families
B7  transient interaction coordinator + Peek/Insight/Explore shell
B8  contextual DANTE deterministic integration + streaming/race states
B9  Insight promotion + Customize draft/apply/cancel
B10 contrasting complete Worlds
B11 resilience/a11y/responsive/performance hardening
B12 pre-backend freeze + exact vertical requirements
```

For every block:

```text
re-read this contract
-> re-evaluate architecture for that concrete block
-> review product/UI behavior
-> implement smallest complete production-depth slice
-> automated gates
-> real-browser/user review
-> freeze accepted behavior
-> next block
```

A later block may reveal a genuine defect in this contract. If so, change the contract deliberately before implementation rather than creating an undocumented exception.

---

# 37. Contract exit criteria

Before declaring the pre-backend World Focus platform architecture frozen, prove:

1. materially different Worlds fit the same platform without page branches;
2. a new unknown World can resolve to a useful default without fabricated data;
3. user-managed stable composition survives adaptive changes;
4. adaptive content remains useful, bounded and visually stable;
5. Lens/refinement/drill-down preserve understandable context;
6. ModuleConfig remains separate from changing ModuleProjection data;
7. AI can be absent without losing core product usefulness;
8. AI can open typed transient views without executing arbitrary UI;
9. Insight promotion creates stable capability-backed configuration only;
10. proposals/effects/receipts are not confused with informational Insight;
11. one module/provider failure is locally isolated;
12. async race protection is deterministic;
13. critical projection values are coherent or truthfully differently fresh;
14. accessibility critical paths work without pointer-only assumptions;
15. performance remains acceptable under dense and long-session pressure;
16. no World Focus contract requires a new Domain owner or speculative DB table;
17. the future Intelligence Platform can integrate through adapters rather than rewrites;
18. the future backend can list exact reads/writes from validated requirements instead of reverse-engineering frontend hacks.

Only then should the later backend/persistence/API workstream treat World Focus as a stable vertical requirement source.
