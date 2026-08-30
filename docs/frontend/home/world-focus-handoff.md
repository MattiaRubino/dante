# DANTE — World Focus Workstream Handoff

**Status:** ACTIVE / PRODUCT DIRECTION ACCEPTED / PRE-BACKEND IMPLEMENTATION NOT STARTED  
**Date:** 2026-08-30  
**Working branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`  
**Handoff integration base HEAD:** `5e9db94b643cdd4a4be7b5ffc0d99dcaec615bed`  
**Accepted Home Mondi/Sintesi visual-geometry checkpoint:** `5e780498d823aa242ee6caf5b326c81c19bfce8f`

This file is the **entry point for continuing the World Focus workstream in a new chat**. It records the decisions already made, the semantic boundaries that must not be reinterpreted, the exact scope stop before backend integration and the next implementation gate.

Read together with:

1. `docs/frontend/home/world-focus-architecture.md`
2. `docs/frontend/home/world-focus-frontend-roadmap.md`
3. `docs/frontend/home/contract.md`
4. `docs/frontend/home/production-depth-handoff.md`
5. `docs/frontend/production-readiness/component-architecture.md`
6. `docs/frontend/production-readiness/backend-integration-contract.md`
7. `docs/frontend/production-readiness/quality-gates.md`
8. `docs/domain/README.md` + complete Domain Language Map
9. `docs/logical-model/README.md` + Whole Logical model
10. `docs/physical-model/README.md`
11. `docs/database/README.md` + Database Dictionary where persistence meaning matters
12. `docs/product/product-identity-and-north-star.md`
13. product discovery simulations under `docs/product/`

The Domain / Logical / Physical / Database authorities outrank this frontend workstream for semantic meaning. This handoff does **not** create a new Domain concept or authorize database changes.

---

# 1. Why this workstream exists

The Home Central Stage already exposes `Mondi` as a continuity projection. A World is useful because it lets the person quickly recover, resume or explore a significant part of their life.

The next product step is not to turn the Home sphere into a CRUD card. The accepted direction is an immersive, reusable **World Focus** surface:

```text
HOME
  -> select / center World
  -> open active World
  -> WORLD FOCUS
     "fammi capire questa parte della mia vita"
```

World Focus is a deep contextual view of **one** World.

It is distinct from the top-level `Mondi` application destination:

```text
TOPBAR -> MONDI
  -> MONDI OVERVIEW
     broad view of all Worlds as a system
     management / relationships / global exploration

MONDI OVERVIEW -> select one World
  -> same reusable WORLD FOCUS surface
```

Do not collapse these two surfaces.

---

# 2. Semantic decision — what a World is and is not

The current accepted Home contract already states that `Mondi` is:

> Significant realities the user wants readily recoverable, resumable or explorable over time.

Permanent semantic guardrails:

```text
World != Domain taxonomy
World != universal Entity / Thing
World != Goal
World != Plan
World != Project
World != category folder
World != database super-parent for life records
World != mandatory owner of every item shown inside it
```

There is no canonical `World` Domain owner in the closed 57-owner model and no current canonical `world` table in the materialized CP6 database.

For this frontend phase, treat a World as a **product-level continuity/profile + projection concept** over existing DANTE reality. This is a bounded product/frontend architecture interpretation, not a Domain-model amendment.

A World may surface heterogeneous canonical realities without changing their meaning, e.g. Goal, Plan, Activity, Event, Routine, Session, Observation, Possibility, Place, Person, Asset, Content Artifact, Actual/Outcome-related projections and derived Signals.

The same canonical reality may be relevant to multiple Worlds without duplication of canonical identity.

---

# 3. Product decisions already accepted

The following decisions are **closed for the current pre-backend phase** unless new evidence proves a contradiction.

## 3.1 Entry model

- Home lateral-world interaction continues to navigate/center the carousel.
- Opening the already active/central World transitions into World Focus.
- World Focus is reusable from Home and later from Mondi Overview, Search and contextual AI/navigation entry points.
- World Focus must be application-navigation aware / route-backed or equivalently history-safe; it must not be a Home-only local modal whose state disappears incorrectly on refresh/back.
- Exact final route syntax is not frozen yet; do not invent backend/API semantics from a route name.

## 3.2 Immersive transition

Desired product grammar:

```text
selected sphere
-> focus / pause
-> geometric-orbital expansion
-> sphere / field expands toward full viewport
-> Home recedes
-> World Focus becomes foreground application surface
```

Visual inspiration is cosmic / galaxy / geometric-circle / ritual-orbital, with a mild “enter the World” feeling.

Different Worlds **may** vary accent color, particle density, orbital rhythm/texture or similar parameters, but only through **one shared transition engine**. No separate animation implementation per World.

Complexity rule:

```text
world-specific variation is allowed
ONLY if it remains parameterized, performant and maintainable.
```

If a richer effect requires disproportionate complexity, prefer the shared base animation.

Reduced-motion must have a simple, intentional equivalent.

## 3.3 World Focus surface

World Focus is not a fixed static dashboard and not one hard-coded React page per World.

Different Worlds may legitimately contain very different realities. Therefore the accepted direction is:

```text
stable World Focus shell
+
typed dynamic composition canvas
+
finite module registry
+
universal modules where useful
+
specialist modules only when they create real value
```

Forbidden:

```text
if (world === "music") ... entire page
if (world === "travel") ... entire page
arbitrary user-supplied JSX/HTML
LLM-generated React components
Notion-like unrestricted block-builder as the core architecture
```

## 3.4 AI is native to World Focus

The DANTE conversational capability is essential inside World Focus.

It is the same DANTE interaction layer with an active World context, not a second unrelated chatbot/product.

Examples:

```text
"Perché sto rallentando?"
"Fammi vedere le spese dell'ultimo mese."
"Confrontalo con gli ultimi tre mesi."
"Cosa manca ancora per questo viaggio?"
```

The AI may cause a visual Insight surface to appear instead of answering only with prose.

This is **accepted and technically feasible**, but must be implemented through typed capabilities and registered renderers, never by allowing the model to generate arbitrary UI code or query the database directly.

## 3.5 Insight surfaces

AI-driven visual response uses one controlled grammar with progressive depth, conceptually:

```text
PEEK
small, quick answer / value / explanation

INSIGHT
chart / comparison / breakdown / bounded analysis

EXPLORE
larger temporary surface when the question requires deeper exploration
```

Exact names/copy/geometry are still open.

An ephemeral insight may later be promoted into a persistent World widget when product semantics permit it.

## 3.6 Personalization / widgets

Accepted high-level model:

```text
PINNED
user-owned stable composition

ADAPTIVE
bounded DANTE-selected current relevance

EPHEMERAL
AI/query-generated temporary insight
```

The user must retain spatial/interaction predictability. DANTE must not arbitrarily rearrange the stable World every time it opens.

A World may support a deliberate customization mode and an `Add to World` / equivalent capability.

Persistent widget principle:

```text
saved widget
= saved presentation/query/configuration intent
!= copied result data by default
```

If an exact historical snapshot is semantically required in a future vertical, it must use the correct Domain/material-history semantics rather than silently turning widget payload into canonical truth.

Removal of a widget from a World does not delete the underlying Goal/Event/Observation/etc.

## 3.7 Suggestion vs persistence

DANTE may suggest a useful widget, connection or possible World.

```text
suggest != accept
suggest != persist
AI inference != canonical accepted effect
```

Promotion into stable user configuration requires the appropriate explicit user-owned action unless a later separately accepted autonomy policy says otherwise.

---

# 4. Current implementation scope — PRE-BACKEND

The current decision is **not** to build the full backend vertical yet.

Reason: exact World Focus content, module families and user interaction model still need product validation across several radically different Worlds. Freezing persistence/API contracts before that discovery is stable would create expensive backend debt.

The current phase must nevertheless be built to **production frontend depth**, not as a disposable mock.

Target stop line:

```text
REAL React/TypeScript architecture
REAL routing/navigation lifecycle
REAL composition engine
REAL module contracts/registry
REAL UI state machine / async state representation
REAL responsive/accessibility/performance behavior
REAL error isolation
REAL typed frontend ports/adapters
REAL tests
REAL deterministic scenario fixtures

STOP BEFORE
real business API
real database changes
real provider integration
real LLM/tool execution
real cross-device persistence
invented backend success
```

At the end of the pre-backend phase, replacing the fixture/local adapter with a real generated-client/backend adapter must **not require rewriting the World Focus UI architecture**.

---

# 5. Required frontend architecture boundary

Expected dependency direction:

```text
WorldFocus UI
    ↓
World Focus application/frontend capability
    ↓
typed ports + view models + semantic UI intents
    ↓
local deterministic scenario adapter   [NOW]
real backend/generated-client adapter   [LATER]
```

The frontend must never consume ORM rows or database Dictionary shapes directly.

Permanent rule:

```text
frontend view model != backend DTO != Domain model != persistence row
```

The future full vertical will likely require application queries / projection builders, but those are **not invented in this phase**.

---

# 6. Dynamic composition model

World Focus must be built from a finite registry of controlled module kinds.

Illustrative families only — not a frozen catalog:

```text
metric
trend
comparison
breakdown
timeline
goal trajectory
planned vs actual
activity/event/routine projections
recent reality
people
places
assets
artifacts
observations
specialist modules where justified
```

A module kind must own a clear contract for:

- validated projection shape;
- supported sizes/presentation profiles;
- loading/ready/partial/stale/empty/error/unavailable states;
- interactions/actions it can emit;
- accessibility semantics;
- responsive behavior;
- performance characteristics;
- error isolation.

Do not create one mega-module with arbitrary optional properties.

Specialist modules are allowed only when a generic module would materially degrade the experience or semantics.

---

# 7. AI / generated-UI safety boundary

Allowed conceptual chain:

```text
user request
-> DANTE conversational interpretation
-> typed capability / presentation intent
-> authorized application query/capability
-> typed InsightProjection
-> registered frontend renderer
```

Forbidden chain:

```text
LLM -> SQL
LLM -> ORM
LLM -> arbitrary HTTP
LLM -> JSX
LLM -> HTML/JavaScript component payload
```

The future backend owns authorization and consequential action validation. Frontend capability availability is not authority.

---

# 8. Performance standard

World Focus is expected to become a central DANTE surface and must be designed accordingly.

Permanent expectations:

- do not load all user life data to open one World;
- do not load all Worlds to render one World Focus unless a specific cross-World feature requires it;
- route/shell and critical content first;
- secondary/heavy modules lazy where appropriate;
- specialist module code splitting where worthwhile;
- charting/large visualization libraries must not inflate the initial bundle without proof;
- isolate module rerenders;
- abort/cancel obsolete async work during navigation/context changes;
- avoid N+1-like frontend fetch patterns in the future integration contract;
- large lists/series require bounded windows, pagination/virtualization/downsampling as applicable;
- transitions prefer compositor-friendly transform/opacity; avoid layout-thrashing animation;
- WebGL/canvas complexity is admitted only if profiling proves the value exceeds cost;
- a failed module must not crash the full World Focus.

Numeric budgets must be established from real browser measurements during roadmap hardening; do not invent a green performance claim from code inspection.

---

# 9. Accessibility and interaction standard

Target: WCAG 2.2 AA-quality behavior.

Must cover at least:

- full keyboard access;
- deterministic focus entry/return;
- Escape/back semantics where relevant;
- screen-reader naming/state for dynamic modules and insight surfaces;
- reduced motion;
- zoom/text expansion;
- responsive/touch behavior;
- no information encoded by color alone;
- predictable personalization/edit mode;
- live-region behavior only where genuinely needed, not noisy narration of every dashboard update.

---

# 10. Open decisions — do not silently resolve

The following are deliberately **OPEN** and must be solved through roadmap scenarios/product review rather than guessed:

1. exact information hierarchy inside World Focus;
2. exact default module set;
3. exact universal vs specialist module boundary;
4. exact AI placement/expansion geometry;
5. exact Peek/Insight/Explore visual grammar and naming;
6. exact customization interaction and widget sizing grid;
7. exact method by which a reality becomes explicitly/semantically/contextually relevant to a World;
8. exact World profile/config persistence model;
9. exact widget persistence/config schema;
10. exact backend application-query/projection architecture;
11. exact authorization/disclosure contract for World projections;
12. exact route URL structure;
13. exact Mondi Overview information architecture;
14. exact AI autonomy policy for suggestions/persistence;
15. exact external/provider data integration into World Focus.

These are not missing work to hide. They are explicit gates.

---

# 11. Scenario requirement before broad implementation

The architecture must be stress-tested against at least four materially different Worlds before the module catalog is considered stable.

Recommended minimum set:

```text
Musica
Viaggi
Finanza
Studio or Corpo
```

Why:

- creative pipeline/version/artifact pressure;
- temporal/place/booking/participant pressure;
- numeric/history/comparison pressure;
- goal/routine/session/observation pressure.

If the same architecture only works by branching the entire page by World name, the architecture has failed.

---

# 12. Exact next step

Do **not** start by filling World Focus with many widgets.

Next implementation gate is `WF0` in `world-focus-frontend-roadmap.md`:

1. construct scenario oracles for several very different Worlds;
2. derive the smallest justified module grammar;
3. freeze the shell / routing / transition ownership contract;
4. only then begin `WF1` implementation.

The user has already authorized continuing this workstream. Each concrete implementation slice still requires a fresh shared-branch HEAD check and must remain bounded to the slice.

---

# 13. Operational safety

- Stay on `feature/home-react` until explicitly authorized otherwise.
- Shared branch: always inspect fresh remote HEAD before writes.
- Do not overwrite parallel Timeline work.
- No new branch/worktree without explicit authorization.
- No merge/rebase/force/history rewrite/main mutation without explicit authorization.
- Never manually edit generated route output.
- No backend/database/Alembic changes in the current World Focus pre-backend phase.
- When a roadmap slice changes accepted behavior/ownership, update this handoff/architecture/roadmap and relevant registry/contracts in the same reviewed scope.
