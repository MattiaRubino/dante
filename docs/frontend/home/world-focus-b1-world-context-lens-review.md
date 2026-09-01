# DANTE — World Focus B1 World Context / Session / Lens Review

**Status:** B1 IMPLEMENTATION IN PROGRESS — AUTOMATED GATES PENDING / USER ACCEPTANCE PENDING  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Parent:** `world-focus-platform-contract.md`, `world-focus-delivery-methodology.md`, B0 ENGINEERING CLOSED  
**Scope:** first visible World Focus mini-vertical inside the frozen workspace. Real backend/API/database/provider/LLM integration remains out of scope until the final vertical.

---

# 0. Delivery rule for B1 and every later mini-vertical

A mini-vertical is one **complete product capability**, not one technical layer.

For the current pre-backend phase, “complete” means:

```text
DANTE/product semantics
-> scenario pressure
-> comparison with mature products/patterns
-> current technology review
-> architecture/state ownership
-> deterministic pre-backend data/config
-> real visible UI
-> interactions
-> responsive behavior
-> accessibility
-> security/privacy/disclosure
-> performance
-> degraded/error/race behavior
-> automated + browser tests
-> explicit future backend/API/DB/Intelligence requirements
-> acceptance/freeze
```

The real backend/API/DB/provider/LLM implementation is deliberately **not** built per mini-vertical now. It is built after frontend/product behavior is proven and the pre-backend vertical requirements are frozen.

This does not mean “frontend prototype”. Every mini-vertical must expose a narrow future backend seam and state exactly what authoritative data/commands it will later require.

---

# 1. Why B1 is first

B0 created the common platform foundation but intentionally did not decide final World Lens behavior.

Before modules, Adaptive or DANTE can react coherently to a focused World, the product needs a stable answer to:

> What is the user currently looking at inside this World?

The answer cannot be inferred independently by every widget.

B1 therefore owns the first visible semantic layer inside the workspace:

```text
WORLD CONTEXT
+
WORLD SESSION
+
BOUNDED WORLD LENS
```

It must remain useful before any analytics/module family exists.

---

# 2. Authorities re-read

B1 consumes the current accepted authorities rather than defining a new ontology.

## Product / North Star consequences

- life, not a task/calendar/metric, remains the center;
- time is foundational but is not the container of all life;
- planned and actual reality remain distinct;
- effort, execution, outcome and Goal progress remain distinct;
- observed pattern is not automatically preference;
- AI inference is not confirmed fact;
- simple situations remain simple;
- user authority remains central.

## WF0 scenario consequences

WF0 explicitly identified a bounded World Lens as a missing hardening.

The deep scenarios show materially different time/scope pressure:

- Music: this month, recent Sessions, upcoming releases, artifact history;
- Travel: upcoming itinerary, exact trip period, next segment, historical trip reality;
- Finance: month/quarter/year comparisons, long history and reconciliation freshness;
- Study: week/month/assessment windows plus upcoming lessons/exams;
- Body/Wellbeing: time-bounded confirmed observations with sensitive provenance;
- Relationships: often qualitative, where forcing a global metric/time control would be harmful;
- Home/Vehicle: persistent long-lived context plus maintenance windows;
- unknown Worlds: Lens must degrade to no visible filter rather than invent semantics.

## Platform Contract consequences

Current accepted contract states that `WorldLens` is bounded presentation/query context, not a universal query language.

It may include:

```text
selected time range
selected sub-scope/category when supported
temporary selection/filter
```

but must not become arbitrary predicates/operators/SQL-like expressions.

Modules later declare whether they inherit, fix, derive or ignore Lens dimensions.

---

# 3. Core B1 problem

There are three related but different concepts.

## World identity/context

Answers:

> Which continuity context am I inside?

It is presentation/product identity, not a new canonical Domain owner.

## World Session

Answers:

> What is the current interaction state while I am inside this World?

It may own:

```text
active World identity
current Lens
current temporary selection/exploration context
request generation ownership
```

It must not duplicate source-backed/canonical reality.

## World Lens

Answers:

> Through which bounded scope am I currently viewing the World?

It is a read/exploration context. By default it is not a durable preference and it is not a mutation to canonical reality.

---

# 4. Major architectural decision: Lens dimensions are capability-driven

Do **not** make every World show the same fixed filter bar.

Wrong:

```text
Every World:
[7d] [30d] [90d] [1y] [category] [person] [status]
```

This would turn DANTE into a generic dashboard/query tool and would misrepresent qualitative Worlds.

Target:

```text
World presentation capability
        ↓
available Lens dimensions
        ↓
only meaningful controls render
```

A World may support:

```text
temporal Lens only
contextual scope only
both
or no visible Lens control
```

The presence of a Lens dimension is presentation/query capability, not Domain membership.

---

# 5. Major architectural decision: start with temporal Lens, keep contextual scope extensible

Time is the only Lens dimension with enough cross-scenario evidence to justify first implementation.

However, even temporal Lens is **optional per World/context**.

B1 therefore implements:

```text
WorldLens
└── time: optional bounded temporal scope
```

and keeps a narrow extension seam for future contextual/sub-scope dimensions.

No generic `filters[]` collection is introduced.

Why:

- generic filters would require semantics that only later projection/module verticals can define truthfully;
- category/status/person meanings differ by capability and source owner;
- the platform already has a clean extension boundary;
- avoiding generic filter grammar preserves the Domain/Logical model and future authorization boundaries.

Re-evaluation trigger:

> At least two concrete later module/capability verticals require the same non-temporal Lens dimension with identical semantics.

---

# 6. Temporal Lens semantic model

The Lens distinguishes **relative viewing intent** from the absolute interval eventually used by a projection query.

The implemented B1 model preserves a finite preset intent rather than pre-resolved timestamps:

```text
WorldTimeLens
  RELATIVE
    7d / 30d / 90d / 1y
  ALL_TIME
    all
```

The model deliberately leaves an extension point for future absolute/custom calendar ranges, but B1 does not ship a date-range picker before a real projection consumer proves the UX and timezone semantics required.

## Frozen B1 preset vocabulary

```text
7d
30d
90d
1y
all
```

The vocabulary is finite; availability is per World capability.

## Frozen deterministic fixture capabilities

```text
Body     -> 7d / 30d / 90d / 1y      default 30d
Music    -> 7d / 30d / 90d / 1y      default 30d
Study    -> 7d / 30d / 90d / 1y      default 30d
Finance  -> 30d / 90d / 1y / all     default 30d
Work     -> 7d / 30d / 90d           default 30d
Routine  -> 7d / 30d / 90d           default 30d
Travel / Relationships / Growth / Projects
         -> no visible temporal Lens in B1
```

This is frontend presentation capability metadata only. It is not a Domain classification or backend contract.

## Absolute/custom range decision

B1 does **not** implement a custom absolute range picker.

Reason:

- it would introduce substantial calendar/focus/mobile/timezone UX before any real projection needs it;
- Travel requires trip-relative/future semantics that a generic historic picker would misrepresent;
- the future model can extend without changing the current relative intent contract.

Re-evaluate when the first real projection requires an exact user-selected calendar interval.

---

# 7. Timezone/calendar semantics

B1 does not perform ad-hoc date arithmetic.

The repository already owns `@dante/time`, currently backed by `temporal-polyfill` and Temporal types/functions.

Native browser Temporal remains non-Baseline as of 2026-09-01, so future B1/B2 resolution continues through the DANTE time abstraction rather than native feature checks.

Required distinctions for future queries remain:

```text
instant
calendar date
local/wall-clock date-time
timezone
relative window intent
```

A “day” or “month” boundary must be resolved in a known timezone when semantics require it.

Travel remains a mandatory pressure case because World/user/source timezone can differ.

---

# 8. URL / history decision

Not every Lens interaction belongs in the URL.

The rule remains:

> Put in the URL only Lens state that is useful to refresh, restore, bookmark, share or browser-navigate.

B1 implementation uses:

```text
/worlds/:worldId?time=<preset>
```

Rules:

- `worldId` remains path identity;
- only the finite accepted temporal preset is parsed from `time`;
- malformed values safely fall back to the World default;
- a recognized preset unsupported by the current World also falls back to that World's default;
- the default preset is omitted when the user returns to it;
- explicit non-default Lens changes create browser history rather than replacing it;
- refresh/deep-link restore the accepted non-default scope;
- transient hover/selection/component state does not enter the URL;
- URL state is presentation/query context, never authorization.

No nested query/filter JSON is introduced.

---

# 9. Ephemeral vs durable Lens

Default behavior:

```text
change Lens
-> changes current exploration context
-> does NOT rewrite stable ModuleConfig
-> does NOT create a user preference automatically
-> does NOT change canonical reality
```

A future explicit save action may persist a module fixed scope or World default Lens, but that belongs to later personalization/configuration semantics.

---

# 10. Future module participation contract

B1 establishes the semantic shape but does not implement module families.

Later ModuleConfig may declare a relationship conceptually equivalent to:

```text
INHERIT
FIXED
DERIVE
IGNORE
```

Examples:

```text
Music creative time trend
-> INHERIT current temporal Lens

Upcoming release module
-> DERIVE a future-facing window from World/session context

Persistent active-project collection
-> IGNORE temporal Lens

User-saved “last 12 months” trend
-> FIXED
```

Exact enum names remain a later ModuleConfig contract decision.

---

# 11. World switch/session lifecycle

B1 implements deterministic session scope identity.

```text
WorldFocusSessionSnapshot
  activeWorldId
  lens
  scopeKey
```

Example:

```text
music|time:30d
music|time:90d
travel|time:none
```

The key is not canonical identity and is not a durable run ID. It is a deterministic frontend scope identity that B2 can combine with the B0 latest-read coordinator to reject stale projection completions.

World switch behavior:

```text
open World A
change Lens A
switch to World B
-> B resolves only B's capability/default/URL state
-> A state cannot leak into B
```

No application-global Lens store is created.

---

# 12. Current product research — findings adopted

## Notion dashboard/global filters

Current Notion dashboard views support global filters across widgets, but only widgets whose underlying views expose the relevant property are affected.

DANTE lesson:

```text
Lens dimension applies only where supported
+
temporary viewing context != durable configuration
```

Do not copy Notion's database/property ontology.

## Linear filters/custom views

Current Linear filters immediately narrow a view, appear in the URL, and filtered states can be explicitly saved as custom views.

DANTE lesson:

```text
restorable/shareable scope may live in URL
+
explicit save is separate from temporary exploration
```

Do not copy Linear's issue-specific filter grammar.

## Grafana time range/variables

Grafana exposes selected dashboard time range and timezone as shared context and can carry them through dashboard/data links.

DANTE lesson:

```text
time context can be shared across compatible projections
+
drill-down should preserve relevant scope
```

Do not copy Grafana's generic variable/query system.

---

# 13. Technology review — B1 decisions

## State management

React/TanStack route state remains sufficient. No Zustand/Redux/XState.

## Routing/search state

Current TanStack Router owns validated/restorable `time` search state. No second URL-state library is added.

## Runtime schema library

No Zod/Valibot dependency is added for a five-value search vocabulary. The route uses a finite explicit parser; B0's validator-neutral transport seam remains available for real backend payloads.

## Time

`@dante/time` remains the future range-resolution authority. B1 preserves intent and does not resolve fake date boundaries merely to exercise the package.

## UI controls

No UI component dependency is added.

- wide workspace: native semantic buttons with `aria-pressed`;
- narrow workspace: native `select`/combobox;
- both consume the same session state and route intent.

## Layout

B0's named workspace container owns responsiveness. No viewport JavaScript or duplicated device breakpoint logic is added.

---

# 14. UI/product decision

B1 introduces a visible, quiet World context header inside the frozen workspace.

Frozen functional hierarchy for B1:

```text
WORLD kicker
World title
World presentation description
optional temporal Lens
```

The title becomes visibly rendered as the page-level `h1` rather than remaining visually hidden.

Wide workspace:

```text
context copy                           segmented temporal Lens
```

Narrow workspace:

```text
context copy
native compact temporal selector
```

Worlds without a temporal capability show the context header without empty filter chrome.

No explicit Reset button is added: selecting the World default is the reset operation and removes the non-default search state.

The visual styling is intentionally restrained and subordinate to future module content. Final user visual acceptance remains mandatory before B1 freeze.

---

# 15. Accessibility requirements

B1 implementation provides:

- visible page-level World heading;
- accessible Lens region name;
- button group name on wide layout;
- explicit `aria-pressed` state;
- native labelled combobox on compact layout;
- >=44px Lens controls;
- visible focus treatment;
- no color-only selected-state semantics;
- stable focus after Lens changes;
- disabled Lens controls while the shell is not ready or no interaction owner exists;
- reduced-motion behavior with identical semantics.

Automated axe remains required but does not replace the user's/manual keyboard and visual gate.

---

# 16. Performance requirements

B1 is deliberately cheap:

- no chart/data library;
- no global state dependency;
- no timers;
- no date arithmetic on render;
- no VFX coupling to Lens state;
- no page remount requirement for Lens change;
- pure finite parsing/resolution;
- CSS container-query responsive transformation;
- session scope identity is a short deterministic string, not serialized state.

B2 may add `Lens -> projection usable` timing once projections exist.

---

# 17. Security/privacy/disclosure requirements

Lens remains non-authoritative.

The URL contains only a finite presentation preset token. It contains no source payload, token, provider ID, note, subject identity or authorization information.

Future projection authorization/disclosure remains backend authoritative.

---

# 18. Deterministic pre-backend strategy

B1 extends only the synthetic World fixture with presentation capability metadata.

It does not add:

- metrics;
- source records;
- fake API latency;
- fake backend success;
- DB persistence;
- provider data.

B2 will introduce deterministic projection adapters on top of the B1 session/Lens contract.

---

# 19. Failure/adversarial matrix

Implementation/tests cover or are required to cover:

```text
invalid URL Lens value
missing Lens value
recognized but unsupported Lens value
World with no temporal Lens
World with smaller preset set
Back/Forward through Lens changes
refresh/deep-link with accepted Lens
wide + compact workspace
keyboard semantics
axe pressure
reduced motion through existing global pressure
Italian + English resource parity
no horizontal overflow across frozen widths
World-specific scope identity
```

Projection-race execution itself belongs to B2, which will consume `scopeKey` plus B0 request cancellation rather than redesign session ownership.

---

# 20. Explicit non-goals

B1 does not implement:

```text
generic filter/query language
custom absolute date picker yet
arbitrary category/person/status filters
module families
ModuleConfig persistence
projection backend/data loading
Adaptive
DANTE/AI
Peek/Insight/Explore
Customize
cross-device preference persistence
real backend/API/DB/provider integration
new Domain/Logical/Physical semantics
```

---

# 21. Implementation inventory

B1 implementation introduces/changes:

```text
model/world-focus-lens.ts
  finite temporal preset vocabulary
  capability definition validation
  safe URL preset normalization
  per-World preset resolution
  relative/all-time Lens intent

application/world-focus-session.ts
  deterministic World + Lens session snapshot
  scope identity for later projection ownership

model/world-focus-fixtures.ts
  presentation-only per-World temporal capability metadata

ui/world-focus-context.tsx
  visible World context
  wide semantic segmented controls
  compact native selector

ui/world-focus-page.tsx
  session creation + context integration

ui/world-focus-workspace.tsx
  persistent context slot independent of future content slot

route
  validated `time` search state
  push-history Lens changes
  default-search reset behavior

world-focus.css
  container-responsive context/Lens design

i18n it/en
  Lens labels and preset copy

unit + E2E
  model/session invariants
  URL/history/deep-link/unsupported/no-Lens/compact behavior
```

---

# 22. Future backend / B2 handoff requirements

B1 deliberately does not invent an endpoint.

B2/future backend must be able to consume a bounded frontend request intent containing, as applicable:

```text
World presentation/context identity
validated temporal Lens intent
resolved authoritative timezone/calendar context when needed
request/scope generation identity client-side
```

The future backend/application layer remains responsible for:

- authoritative data selection;
- disclosure/authorization;
- timezone-aware range resolution where source semantics require it;
- aggregation/downsampling;
- provenance/freshness;
- partial/unavailable/error semantics.

The client `scopeKey` is never accepted as authorization or canonical state.

---

# 23. B1 gate / acceptance state

B1 is **not frozen** merely because implementation exists.

Required gate sequence:

```text
implementation
-> automated CI
-> browser/E2E evidence
-> user functional test
-> user visual/interaction review
-> fixes if needed
-> rerun gates
-> explicit user OK
-> B1 freeze
-> B2
```

At the time of this update the implementation commit exists, but automated gates and user acceptance are still pending.
