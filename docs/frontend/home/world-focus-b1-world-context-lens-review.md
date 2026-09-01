# DANTE — World Focus B1 World Context / Session / Lens Review

**Status:** B1 ANALYSIS OPEN — NO IMPLEMENTATION AUTHORIZED YET  
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

B1 should therefore implement:

```text
WorldLens
└── time: optional bounded temporal scope
```

and a narrow extension seam for future contextual/sub-scope dimensions.

Do not implement a generic `filters[]` collection now.

Why:

- generic filters would require semantics that only later projection/module verticals can define truthfully;
- category/status/person meanings differ by capability and source owner;
- the platform already has a clean extension boundary;
- avoiding generic filter grammar preserves the Domain/Logical model and future authorization boundaries.

Re-evaluation trigger:

> At least two concrete later module/capability verticals require the same non-temporal Lens dimension with identical semantics.

---

# 6. Temporal Lens semantic model

The Lens must distinguish **relative viewing intent** from the absolute interval eventually used by a projection query.

Do not persist only already-resolved timestamps for presets such as “last 30 days”, because after reload they would silently stop meaning “last 30 days”.

Conceptual model:

```text
WorldTimeLens
  NONE
  RELATIVE
    preset identity
  ABSOLUTE
    start/end calendar boundary
```

B1 should not hard-code backend query DTOs.

The frontend model should preserve semantic intent; a future application adapter resolves it into authoritative query boundaries using current timezone/calendar context.

## Initial preset pressure

Potential initial presets to evaluate in UI:

```text
7 days
30 days
90 days
this year / year-to-date
all time
```

These are **not yet frozen copy or mandatory availability**. Each World may expose a smaller meaningful subset and one default.

Do not add “Now” as a universal time preset: some modules represent past actuals, some future schedules, some persistent context.

## Absolute/custom range

The architecture must allow it, because Finance, Travel, Study and historical inspection will eventually require precise intervals.

Whether B1 ships the full custom date-range picker is a UI/product decision to close before implementation. Do not fake a low-quality date picker merely to satisfy extensibility.

---

# 7. Timezone/calendar semantics

B1 must not use ad-hoc date arithmetic.

The repository already owns `@dante/time`, currently backed by `temporal-polyfill` and Temporal types/functions.

Native browser Temporal remains non-Baseline as of 2026-09-01, so B1 must continue to use the DANTE time abstraction rather than switching to native Temporal availability checks.

Required distinctions for future queries:

```text
instant
calendar date
local/wall-clock date-time
timezone
relative window intent
```

A “day” or “month” boundary must be resolved in a known timezone when semantics require it.

Travel is a mandatory pressure case because World/user/source timezone can differ.

---

# 8. URL / history decision

Not every Lens interaction belongs in the URL.

The rule is:

> Put in the URL only Lens state that is useful to refresh, restore, bookmark, share or browser-navigate.

Current mature patterns support this:

- Linear reflects applied filters in the URL and allows filtered views to be shared;
- Grafana exposes selected time range/timezone through URL state for links/drill-down;
- TanStack Router treats search params as validated typed application state and explicitly supports defaults/stripping/retention.

DANTE-specific decision:

- route `worldId` remains path identity;
- accepted restorable Lens state may use validated search params;
- transient selection/hover/component state stays local;
- defaults should be omitted/stripped from the URL where possible;
- malformed Lens URL state must fall back safely instead of breaking World Focus;
- URL state is presentation/query context, never authorization.

No arbitrary nested filter JSON is authorized.

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

This is consistent with mature dashboard/view products:

- Notion distinguishes temporary view-mode filters from explicitly saved configuration;
- Linear lets users filter temporarily and explicitly save a custom view when durability is desired.

DANTE-specific future rule:

A user may later explicitly choose to save a module's fixed scope or a World default Lens. That belongs to personalization/configuration semantics, not to the default B1 interaction.

---

# 10. Future module participation contract

B1 should establish the semantic shape but not implement module families.

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

This prevents a global Lens from blindly changing every module.

Exact enum names remain a later ModuleConfig contract decision.

---

# 11. World switch/session lifecycle

B1 must define deterministic reset/restore behavior.

Baseline:

```text
open World A
set temporary Lens A
switch to World B
-> B receives B's own default/restored Lens policy
-> A's transient component state cannot leak into B
```

Do not create one application-global Lens shared by every World.

Future persistence may restore a user-owned World default or restorable URL state, but current pre-backend fixtures remain deterministic.

Race protection uses B0 request-generation/cancellation primitives.

Late results from a previous World/Lens generation may not commit to the active session.

---

# 12. Current product research — findings adopted

## Notion dashboard/global filters

Current Notion dashboard views support global filters across widgets, but only widgets whose underlying views expose the relevant property are affected. View-mode filters are temporary/local unless explicitly saved with appropriate authority.

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

# 13. Technology review — current B1 decisions

## State management

Keep React local/reducer state. No Zustand/Redux/XState.

Trigger to reconsider remains genuine cross-tree workflow complexity, not B1 existence.

## Routing/search state

Use current TanStack Router when restorable Lens state is accepted for URL encoding.

It already provides typed/validated search state; no second URL-state library is justified.

## Runtime schema library

Do not add Zod/Valibot solely for B1 unless the concrete search-state or fixture boundary becomes complex enough to justify it. A small explicit parser can remain clearer for a finite preset vocabulary.

The B0 generic boundary seam remains available for future untrusted transport payloads.

## Time

Use `@dante/time` / Temporal polyfill abstraction already in the repository.

Do not migrate B1 to native `Temporal` because native availability is still incomplete across widely used browsers.

## UI controls

Prefer native semantic buttons/menus/dialog patterns plus DANTE design tokens.

Do not add a component-system dependency for one Lens control.

## Layout

Use the B0 workspace container-query foundation. Do not couple Lens responsiveness to viewport JS.

---

# 14. UI/product target

B1 must leave the workspace visibly more useful.

It should introduce a restrained **World context header/lens region** inside the workspace, not a dashboard toolbar.

The visual hierarchy should communicate:

```text
where am I?
what scope am I viewing?
can I change/reset that scope?
```

without competing with the global Topbar or the future World content.

## Desired qualities

- visually quiet compared with modules/content;
- premium/intentional, not generic admin-dashboard chrome;
- usable with one hand/touch at narrow widths;
- keyboard complete;
- no horizontal overflow;
- no giant toolbar of filters;
- current scope always understandable;
- default/no-filter state not visually noisy;
- future additional Lens dimensions can be added without redesigning the whole header.

Exact visual composition is **not yet frozen** and must be reviewed against the live workspace before implementation acceptance.

---

# 15. Accessibility requirements

At minimum:

- current World remains the document/page heading context;
- Lens region has an accessible name;
- controls have explicit current/selected state;
- keyboard use does not depend on arrow-key behavior unless the selected ARIA pattern specifically requires it;
- focus remains stable after changing scope;
- menus/popovers restore focus correctly;
- touch targets meet current product/WCAG pressure;
- selected state is not color-only;
- changing Lens does not create unexpected focus jumps;
- reduced motion keeps identical semantic behavior.

If a custom date-range dialog is implemented, it must be independently keyboard/focus tested rather than relying on automated axe only.

---

# 16. Performance requirements

B1 itself should be extremely cheap.

- no chart/data library;
- no global state dependency;
- no continuous timers just to maintain relative labels;
- no rerender of decorative VFX due to every Lens interaction;
- Lens change becomes a future query-generation boundary, not a page remount;
- URL updates must not recreate unrelated shell state;
- preset resolution uses shared time utilities;
- performance marks may later measure Lens-to-usable-projection latency when B2 exists.

Current B0 VFX degradation rule remains untouched.

---

# 17. Security/privacy/disclosure requirements

Lens is not authorization.

Changing scope must never make the frontend fetch/show data that the authoritative future projection boundary is not allowed to disclose.

URL search state must not contain sensitive source payloads, private notes, authorization tokens or provider identifiers merely for convenience.

A shareable URL may describe a viewing scope; the receiver's authoritative access still determines what can be projected.

---

# 18. Deterministic pre-backend strategy

B1 may extend the synthetic World fixture with **presentation capability metadata only**, for example whether a temporal Lens is available and its deterministic default/preset set.

Such fixture metadata is explicitly:

```text
frontend product fixture
!= Domain identity
!= backend DTO
!= DB row
!= canonical World model
```

Do not invent source data, metrics or fake API latency in B1.

B2 will introduce the real deterministic projection adapter boundary.

---

# 19. Failure/adversarial matrix

B1 implementation must prove at least:

```text
invalid URL Lens value
missing Lens value
World with no temporal Lens
World with smaller preset set
World A -> World B switch
Back/Forward through accepted Lens changes
refresh/deep-link with accepted Lens
compact viewport
200% zoom pressure
keyboard-only
reduced motion
very long translated labels
Italian + English
future timezone different from browser timezone
rapid Lens changes before future projections finish
```

Where B2 is required to exercise projection races, B1 must at least expose deterministic generation/change identity that B2 can consume without redesign.

---

# 20. Explicit non-goals

B1 does not implement:

```text
generic filter/query language
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

# 21. Open decisions to close before implementation

1. exact first temporal preset vocabulary and per-World availability;
2. whether B1 includes a polished custom absolute date-range flow or only leaves the typed seam;
3. exact URL parameter shape and whether Lens changes push or replace browser history by interaction class;
4. exact visual composition of World context + Lens inside the frozen workspace;
5. whether the World title remains visually hidden from WF1 or becomes visible as part of the new context region;
6. compact/narrow control transformation;
7. exact deterministic fixture capability metadata;
8. whether an explicit Reset control is shown only after deviation from default or represented through preset selection.

These are product/UI decisions, not backend blockers.

---

# 22. B1 completion target

B1 is complete only when the user can open contrasting fixture Worlds and see a polished, useful World context/Lens experience whose behavior is deterministic and production-depth.

Expected exit evidence:

```text
visible World context inside workspace
bounded optional temporal Lens
validated/restorable URL behavior where accepted
no generic filter grammar
World-specific Lens capability without World-specific pages
stable world-switch/reset/history semantics
container-responsive UI
keyboard/a11y complete
safe translated state
strict typing/tests/build/E2E green
no WF0/WF-G3 regression
no Access/Auth/Timeline regression
future B2 projection boundary can consume Lens without redesign
```

Only after these decisions and implementation pass should B1 freeze and B2 begin.
