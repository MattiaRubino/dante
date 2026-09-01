# DANTE — World Focus Workspace Platform Checkpoint

**Status:** ENGINEERING CLOSED — FINAL PLATFORM AUTOMATED PASS — CONCRETE DANTE SEQUENCING ACTIVE  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Final platform HEAD:** `6c441335a75bb913af8da1eda569d8094d38a539`  
**Frontend CI:** `33549465793` — PASS

This checkpoint is the durable engineering closure record for the reusable World Focus composition / interaction / surface platform. It no longer represents the active live gate; current sequencing is in `world-focus-current-checkpoint.md`.

## 1. What this platform owns

```text
WORLD FOCUS WORKSPACE HOST
├ transient workspace interaction state
├ bounded interaction cursor references
├ interaction generation
├ selected context reference
├ finite surface stack
├ composition host
│  └ finite approved module registry
├ workspace allocation resolver
│  ├ main allocation: full | split
│  ├ top layer: none | overlay | focus
│  └ interaction: interactive | inert
└ surface layer
   └ finite approved surface registry
```

It does **not** own canonical World truth, Domain ownership, authorization/disclosure, durable DANTE Run lifetime, provider state, source payload authority or backend effects.

## 2. Dynamic composition

World Focus is not a fixed dashboard. Composition is resolved from approved product outputs and finite shipped renderers.

The planner preserves distinctions between:

```text
stability:   stable | adaptive | ephemeral
prominence:  lead | primary | supporting
footprint:   wide | standard | compact
```

The logical plan uses a 12-unit contract, while physical rendering may collapse/adapt at small allocated widths. Logical grid semantics therefore do not force pathological 12-track CSS at narrow widths.

Automated deterministic stress covers 500 synthetic compositions spanning sparse/dense Worlds, unknown future kinds and 0–20 candidate answers.

Permanent rule:

```text
module kind != Domain owner
module kind != World question
renderer != canonical truth
```

## 3. Bounded interaction cursor

The workspace cursor exposes only bounded presentation references:

```text
worldId
generation
selection reference
active surface reference
```

It explicitly does not contain DOM nodes, secrets, authorization decisions, copied canonical source data or durable Run state.

Selection changes advance generation. Repeating the same selection is a no-op.

Future DANTE Context Builder logic remains purpose/recipient/sensitivity/freshness aware and reconstructs authorized context outside this React cursor.

## 4. Surface state model

The pure reducer supports finite operations:

```text
select context
clear context
open surface
replace surface
promote surface
close surface
close top surface
```

A surface descriptor keeps only finite presentation metadata:

```text
instance id
approved kind
semantic depth
presentation surface
origin
bound generation
bounded context reference
dismissibility
```

Semantic depth and geometry are separate axes.

## 5. Race / stale presentation protection

Async presentation intents may carry `expectedGeneration`.

Invariant:

```text
request starts at generation N
selection changes -> generation N+1
late presentation intent still expects N
-> deterministic no-op
```

This prevents late frontend presentation results from attaching to a newer context. It does not replace future durable DANTE Run/effect semantics.

## 6. Escape and blocking-stack ownership

Escape precedence:

```text
non-dismissible top surface
-> consume/block Escape
-> World cannot close underneath

dismissible top surface
-> close top surface only

no surface
-> route may close World
```

The platform additionally hardened the stack so a newer non-blocking surface cannot semantically jump above a currently authoritative blocking modal/full-focus surface.

This blocking-tail rule is defense-in-depth for confirmation/focus flows and prevents state/DOM ordering from silently weakening interaction authority.

## 7. Workspace physical allocation

The allocator deliberately separates concerns rather than creating a combinatorial mega-enum:

```text
mainAllocation = full | split
topLayer       = none | overlay | focus
mainInteraction= interactive | inert
```

This permits valid states such as:

```text
main + DANTE sidecar
+
confirmation modal above it
```

without losing deterministic restoration of the underlying allocation.

Current pre-backend presentation policy:

```text
minimum split workspace   900 px
minimum useful main       520 px
minimum sidecar           300 px
maximum sidecar           420 px
preferred sidecar         36%
split gap                 16 px
```

These are UI policy values, not Domain semantics and not persisted World truth.

## 8. Sidecar / overlay / focus behavior

Accepted allocation behavior:

```text
wide sidecar
-> consumes real canvas width
-> main remains interactive

sidecar when split minima cannot be preserved
-> degrades to non-modal overlay
-> main remains interactive

modal
-> main becomes inert
-> visible underlying sidecar also becomes inert

full-focus
-> main becomes inert
-> visible underlying sidecar also becomes inert

older competing surfaces
-> dormant rather than competing in DOM

route presentation
-> external to workspace geometry
```

The platform was benchmarked against Microsoft Fluent 2 drawer behavior, WAI-ARIA modal interaction requirements and MDN CSS Container Queries.

## 9. Actual allocated-container ownership

The persistent outer workspace remains the stable visual boundary, but reusable content adapts against the **actual main canvas**:

```text
workspace 1280
├ main 844   <- named `world-focus-main` query container
├ gap 16
└ sidecar 420
```

A module therefore sees 844 px, not 1280 px and not global viewport width.

`ResizeObserver` measures the space actually granted to the workspace. Missing ResizeObserver support degrades safely after the initial measure rather than crashing the World.

No duplicated `window.innerWidth` product breakpoint state was introduced.

## 10. Scroll / resource ownership

The main plane owns vertical scrolling; the outer workspace remains the clipped stable boundary.

Future sidecars/focus surfaces must own their internal overflow explicitly rather than rely on accidental ancestor clipping.

The platform retains B0 local error boundaries, cancellation/race safety, User Timing and VFX degradation rules.

## 11. Finite renderer/surface extension

Only code shipped by DANTE may enter the registries.

```text
approved registration -> renderer allowed
unknown kind           -> local safe degradation
renderer throw         -> local render boundary
remote/model JSX       -> forbidden
arbitrary HTML/JS      -> forbidden
```

This is controlled extensibility, not an executable plugin marketplace and not model-generated UI.

## 12. Stress / automated evidence

Final platform HEAD:

`6c441335a75bb913af8da1eda569d8094d38a539`

CI:

`33549465793`

Final gate evidence:

```text
Frontend contract drift check       PASS
Home / World Focus format checks    PASS
Lint                                PASS
Typecheck                           PASS
Architecture check                  PASS
Generated-source drift check        PASS
Unit tests                          PASS
Production build                    PASS
Diff/repository mutation checks     PASS
Mobile Bundle                       PASS
Chromium Web E2E                    PASS
Firefox frozen Timeline contract    PASS
Frontend CI Gate                    PASS
```

Stress evidence includes:

```text
500 deterministic composition scenarios
500 deterministic allocation/surface-stack scenarios
wide/narrow sidecar integration
live ResizeObserver contraction
modal over split sidecar
narrow sidecar dormant under modal
main/sidecar inert defense-in-depth
blocking-stack barrier
compact containment
```

No gate was weakened to obtain PASS.

## 13. Relationship to DANTE D0/D1

After this platform closed, `world-focus-dante-spatial-presence-review.md` resolved the previously open concrete DANTE spatial question through external product comparison and pressure testing.

Accepted direction:

```text
P0 quiet invoke
P1 compact non-modal composer
ongoing conversation wide -> sidecar
ongoing conversation constrained/mobile -> route-owned focus overlay
explicit maximize / restore
contextual/deictic invocation only with explicit bounded reference
```

D1 is now the first concrete registered surface consumer. See `world-focus-d1-dante-entry-review.md` for its final engineering disposition.

## 14. Historical notes superseded by this checkpoint

Earlier versions of this file stated:

```text
DANTE spatial gate still open
production registry intentionally empty
next gate = DANTE spatial reverse engineering
```

Those statements described the earlier implementation moment and are no longer live. They are replaced by the final platform closure above and the D0/D1 documents.

## 15. Permanent barriers

```text
World != canonical Domain owner
layout policy != Domain semantics
surface stack != authorization
surface visibility != disclosure permission
AI output != accepted fact
AI proposal != user Decision
tool call != authorization
provider state != canonical state
planned != actual
absence != false
```
