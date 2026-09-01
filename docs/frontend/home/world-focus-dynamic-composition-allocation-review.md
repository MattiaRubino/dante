# World Focus — Dynamic Composition & Surface Allocation Review

Status: **ENGINEERING AUTOMATED PASS — CONCRETE SURFACE VERTICAL ACCEPTANCE PENDING**

This document records the product/architecture contract for the dynamic World Focus workspace before concrete DANTE / Insight / Explore surface verticals are implemented.

## Problem

World Focus cannot be a fixed dashboard and cannot contain World-specific layout branches such as `if music -> layout A` or `if finance -> layout B`.

The same rectangular workspace must remain coherent when:

- different Worlds expose different answer families;
- a World is sparse or dense;
- adaptive/ephemeral outputs appear or disappear;
- a contextual DANTE / Insight / Explore surface opens;
- a sidecar consumes real canvas width;
- the same sidecar must fall back to overlay in a narrow allocation;
- a modal or focused surface sits above an already split workspace;
- the browser/parent layout changes the actual space granted to World Focus;
- future specialist modules are added without reauthoring the page shell.

## External high-level patterns reviewed

### Microsoft Fluent 2 — Drawer

Reference:
https://fluent2.microsoft.design/components/web/react/core/drawer/usage

Useful pattern:

- inline drawer = passive side-by-side surface when main + secondary content must remain usable together;
- overlay drawer = elevated surface that covers main content;
- modal overlay is intentionally blocking;
- non-modal overlay may remain interactive with the main page;
- prolonged/complex flows should move to a more focused surface;
- drawer body owns overflow rather than silently clipping content.

DANTE conclusion:

`inline/sidecar`, `overlay`, and `focus` are distinct physical/interaction behaviors. They must not collapse into one generic drawer state.

### WAI-ARIA APG — Modal Dialog

References:
https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/

Useful pattern:

- content below a modal is inert;
- focus belongs inside the modal while it is open;
- `Escape` normally dismisses the modal when dismissal is allowed;
- focus returns to the invoking/logically subsequent element;
- nested modal dialogs are valid when they are deliberate;
- modal semantics must never be declared if the implementation does not actually block outside interaction.

DANTE conclusion:

Geometric overlay and modal interaction are separate concerns. A popover or a narrow sidecar fallback is not automatically modal. Modal/focused surfaces make every underlying interactive workspace plane inert; concrete surface verticals remain responsible for their own correct role/label/focus lifecycle.

### MDN — CSS Container Queries

References:
https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries
https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_size_and_style_queries

Useful pattern:

Reusable components should adapt to their actual containing allocation, not only the global viewport.

DANTE conclusion:

The outer World workspace remains a named query container, but actual composition adapts against a nested `world-focus-main` container whose inline size is the canvas remaining after sidecar allocation.

Example:

```text
workspace 1280
├ main 844  <- component/container queries resolve here
├ gap 16
└ sidecar 420
```

A module must see `844`, not `1280`.

### MDN — Top layer / Popover stack behavior

References:
https://developer.mozilla.org/en-US/docs/Glossary/Top_layer
https://developer.mozilla.org/en-US/docs/Web/API/Popover_API

Useful pattern:

- elevated UI has explicit layer ownership rather than accidental z-index competition;
- modal and popover behavior are not interchangeable;
- stack relationships are deliberate and browser interaction semantics matter independently from raw geometry.

DANTE conclusion:

A blocking modal/full-focus surface must remain authoritative until it is deliberately replaced/closed by a compatible blocking flow. A weaker sidecar, popover or route event must not be able to overtake an active blocker simply because an async callback or synthetic event arrives later.

## Architecture

```text
REALITY / APPLICATION PROJECTIONS
              |
              v
PRODUCT OUTPUT CANDIDATES
              |
              v
DYNAMIC COMPOSITION PLANNER
- stable / adaptive / ephemeral
- lead / primary / supporting
- wide / standard / compact
- bounded first-open budget
              |
              v
LOGICAL 12-UNIT PLAN
              |
              v
ALLOCATED MAIN CANVAS
              |
              v
CSS CONTAINER RENDERING
(world-focus-main)
```

Transient/deeper surfaces are resolved on an independent path:

```text
WORLD WORKSPACE STATE
              |
              v
SURFACE ADMISSION BARRIER
              |
              v
WORKSPACE SURFACE ALLOCATION RESOLVER
              |
      +-------+--------+
      |                |
      v                v
MAIN ALLOCATION     TOP LAYER
full | split        none | overlay | focus
      |                |
      +-------+--------+
              |
              v
BACKGROUND INTERACTION
interactive | inert
```

Each active surface placement also carries its own interaction state:

```text
placement.interaction
interactive | inert
```

That is required because a visible allocated sidecar can remain physically present underneath a blocking layer while being intentionally non-interactive.

## Why the axes are separate

The following state is valid and must not require a synthetic combined enum:

```text
MAIN + DANTE SIDECAR
        +
CONFIRMATION MODAL ABOVE IT
```

Therefore:

```text
mainAllocation = split
topLayer        = overlay
mainInteraction = inert
sidecar         = visible + allocated + inert
modal           = visible + interactive
```

The sidecar stays allocated only to preserve visual/layout continuity and deterministic restoration after the modal closes. It is **not** clickable through the modal.

A full-screen Explore surface may similarly sit above a split workspace while preserving the underlying allocation:

```text
mainAllocation = split
topLayer        = focus
mainInteraction = inert
sidecar         = visible + allocated + inert
focus surface   = visible + interactive
```

## Allocation rules

Current pre-backend allocation policy:

```text
min split workspace     900px
min useful main         520px
min sidecar             300px
max sidecar             420px
preferred sidecar       36%
split gap               16px
```

These are presentation policy values, not Domain concepts and not persisted World truth.

Rules:

1. At most one sidecar consumes canvas width.
2. The most recent admissible sidecar is the candidate active sidecar.
3. Earlier sidecars remain dormant in interaction state so close/back can restore them.
4. A sidecar becomes split only when both workspace and main minima remain satisfied.
5. Otherwise the same requested sidecar degrades to non-modal overlay.
6. At most one overlay/focus surface is active above the workspace stack.
7. A newer modal makes a narrow overlay sidecar dormant until the modal closes.
8. A wide split sidecar may remain visible and allocated underneath a newer modal/focus layer, but it becomes inert while that blocking layer is active.
9. `route` presentation remains external to workspace geometry.
10. `inline` content belongs to composition, not the transient surface plane.
11. Dormant surfaces are inert and are not rendered as competing DOM surfaces.
12. A modal/full-screen blocker is authoritative over weaker later entries, including malformed/legacy state that bypassed reducer admission.

## Blocking stack admission barrier

Blocking presentations:

```text
modal
full-screen
```

Accepted reducer policy:

```text
non-blocking -> may open non-blocking or blocking
blocking     -> may append only another blocking surface
nested blocking surfaces are allowed
close top blocker -> restores the previous blocker/base allocation
replace/promote below an active blocker -> no-op
explicit close/cleanup -> allowed
```

The invariant is a **blocking tail**:

```text
[nonblocking ...] [blocking ...]
```

Once the first blocker enters the stack, no weaker/nonblocking surface may be appended after it.

This is intentionally stricter than relying on `inert` or CSS alone. A late async result, synthetic click or future integration bug cannot legally create a weaker top owner above a blocking interaction.

### Defense in depth

The barrier is enforced at four independent levels:

1. **Reducer admission** — rejects nonblocking opens while a blocker exists and rejects hidden lower replace/promote mutations.
2. **Allocation normalization** — forged/legacy malformed stacks still keep the latest blocker authoritative; weaker entries after the first blocker are dormant/inert.
3. **DOM interaction** — main and allocated underlying sidecars carry `inert` while a blocking surface owns interaction.
4. **Integration tests** — a forced synthetic click beneath a modal is dispatched deliberately; the reducer still prevents a sidecar from appearing.

This is not an authorization boundary. It is a presentation/interaction consistency boundary.

## Interaction rules

```text
sidecar split, no blocking layer     -> main interactive, sidecar interactive
sidecar degraded overlay             -> main interactive, sidecar interactive
popover                              -> main interactive
modal                                -> main inert, underlying sidecar inert
full-screen                          -> main inert, underlying sidecar inert
active modal/full-screen             -> active surface interactive
nested blocker                       -> newer blocker owns interaction
```

This is deliberately not inferred from visual elevation alone.

Concrete modal/focus surface verticals must later close the remaining accessibility loop:

- correct semantic role and accessible name;
- initial focus placement;
- focus containment where required;
- Escape policy consistent with dismissibility;
- focus restoration;
- inert background behavior verified in browser/AT tests.

## Rendering rules

The persistent outer workspace remains:

```text
world-focus-workspace
```

The main content plane is now:

```text
world-focus-main-plane
container: world-focus-main / inline-size
```

When split, `world-focus-main-plane` receives the resolver's actual main inline size.

Composition container queries are evaluated against `world-focus-main`, not the global viewport and not the full outer workspace.

This allows the exact same World composition to reflow when a sidecar opens without re-running product ranking or introducing World-specific layout code.

Active surface wrappers receive their resolved slot and interaction state. If a blocking modal/focus surface is above a split sidecar, the sidecar wrapper remains in its slot but carries `inert`; the active blocking surface remains interactive.

## Logical grid vs physical tracks

The planner keeps a logical 12-unit layout contract.

This does **not** require 12 physical CSS tracks at every width.

A real compact-browser failure showed that 12 physical tracks plus 11 gaps can exceed a very narrow workspace even when the logical plan itself is valid.

Accepted rule:

```text
logical plan = 12 units
physical renderer = adaptive
```

Below the compact main-container threshold, the physical renderer collapses to one column while preserving logical entry order and semantic prominence.

## Scroll ownership

The main plane owns vertical overflow:

```text
world-focus-main-plane
overflow-y: auto
overflow-x: hidden
```

The outer workspace remains clipped as the stable visual/geometry boundary.

Future sidecar implementations should give their own body explicit scroll ownership rather than relying on accidental parent overflow.

## Resilience

The workspace performs an immediate local size measurement and then observes subsequent size changes with `ResizeObserver` when available.

If `ResizeObserver` is unavailable, World Focus keeps the initial measurement and does not crash. This is a degradation path, not a claim that unsupported environments receive live allocation updates.

## Stress validation

### Composition planner

The planner has deterministic stress covering 500 synthetic World/user compositions with 0-20 candidates and combinations of:

- stable / adaptive / ephemeral;
- lead / primary / supporting;
- wide / standard / compact;
- sparse and dense scenarios;
- unknown future module kinds.

Required invariants include:

- stable entries are not lost;
- deterministic input produces deterministic plans;
- first-open budgets remain bounded;
- rows do not exceed logical capacity;
- lead prominence remains truthful;
- no World identity branch is required.

### Surface allocation resolver

The allocation resolver has deterministic stress across 500 synthetic users combining:

- workspace widths from 0 through 1900px;
- 0-8 transient surfaces;
- inline / popover / sidecar / modal / full-screen / route presentations;
- arbitrary attempted stack order.

Required invariants include:

- main width never becomes negative or exceeds workspace width;
- split sums exactly to `main + gap + sidecar = workspace`;
- at most one active sidecar;
- at most one active overlay;
- at most one active focus surface;
- `mainInteraction` is inert iff an active modal/full-screen surface requires it;
- active sidecars inherit the blocking/background interaction state;
- active overlay/focus owner remains interactive;
- dormant placements are inert;
- once a blocking tail starts, reducer state contains no later nonblocking surface;
- same state + same width = same allocation plan.

The resolver also has a forged malformed-state test proving that a late illegal sidecar/route cannot overtake a modal even when reducer admission is bypassed.

### React integration

Integration tests exercise:

- wide sidecar -> split + interactive main + interactive sidecar;
- live ResizeObserver contraction -> same sidecar becomes non-modal interactive overlay;
- split sidecar + newer modal -> sidecar remains allocated but inert, main inert, modal interactive;
- narrow sidecar + newer modal -> sidecar becomes dormant, modal owns overlay slot;
- forced click inside an inert main plane while a modal is open -> reducer refuses the weaker sidecar and surface count remains unchanged.

## Automated validation evidence

Exact code candidate:

```text
2047733bd01eeaa85b4d6e4dd2cc11e102b25248
```

Frontend CI run:

```text
33548911233
```

Result:

```text
Frontend contract drift     PASS
Home format check           PASS
Lint                        PASS
Typecheck                   PASS
Architecture                PASS
Generated-source drift      PASS
Unit tests                  PASS
Production build            PASS
Diff check                   PASS
Repository mutation check   PASS
Mobile Bundle               PASS
Chromium Web E2E            PASS
Firefox frozen contract     PASS
Frontend CI Gate            PASS
```

No Playwright failure artifact was uploaded because the browser gate passed.

## Explicit non-goals

This slice does not implement:

- DANTE chat UI;
- Insight UI;
- Explore UI;
- modal visual design;
- focus trap implementation for a concrete modal;
- backend/API persistence;
- user-authored freeform coordinates;
- a generic dashboard builder;
- World-specific layout templates.

Those concrete verticals consume this platform after the platform gates pass.

## Persistent invariants

```text
World != canonical Domain owner
layout policy != Domain semantics
surface stack != authorization
surface visibility != disclosure permission
inert != authorization
AI output != accepted fact
provider state != canonical state
planned != actual
absence != false
```

## Current disposition

Engineering foundation now includes:

- dynamic composition planner;
- logical 12-unit planning with adaptive physical rendering;
- deterministic 500-scenario composition stress;
- workspace allocation resolver;
- separate main allocation / top layer / interaction axes;
- per-placement interaction state;
- actual workspace measurement through `ResizeObserver` with safe fallback;
- nested `world-focus-main` container queries;
- active/dormant surface placement filtering;
- inert main plane and underlying sidecar for modal/full-focus allocation;
- blocking-tail admission policy with deliberate nested blockers;
- lower-surface mutation rejection while blocked;
- allocation defense against malformed/legacy stacks;
- forced-event integration defense beneath modal barriers;
- deterministic 500-scenario allocation stress;
- exact code candidate full frontend CI PASS.

The **dynamic composition / surface allocation engineering platform is automated-PASS and ready to be consumed by a real concrete vertical**.

It is not a finished DANTE/Insight/Explore experience and is not user-accepted product UI. Concrete surfaces must still prove their own product semantics, focus lifecycle, accessibility, responsive behavior, degraded states and user value before their vertical can be closed.
