# DANTE — World Focus Workspace Platform Checkpoint

**Status:** ENGINEERING CLOSED — PLATFORM EVIDENCE RETAINED / M1 INTEGRATION ALIGNED  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`  
**Final platform HEAD:** `6c441335a75bb913af8da1eda569d8094d38a539`  
**Frontend CI:** `33549465793` — PASS

This checkpoint is the durable engineering closure record for the reusable World Focus composition / interaction / surface platform. It no longer represents the active live gate; current sequencing is in `world-focus-current-checkpoint.md`.

The platform closure evidence above predates M1. M1 later generalized the cursor/reference contract without changing platform ownership. Sections 1, 3 and 5 below describe the current integrated production contract while retaining the original platform closure SHA/CI as historical evidence.

## 1. What this platform owns

```text
WORLD FOCUS WORKSPACE HOST
├ transient workspace interaction state
├ bounded interaction cursor references
│  ├ primary context reference
│  └ bounded ordered supporting context references
├ interaction generation
├ compatibility selection projection of primary
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

The current production workspace cursor exposes only bounded presentation references:

```text
worldId
generation
contextReferences
  primary
  supporting[]    [bounded + ordered]
selection         [compatibility projection of primary only]
activeSurface
```

`contextReferences` is a normal enumerable frozen cursor property. The cursor and reference set remain presentation/context coordinates only.

A surface inherits the **primary** context reference by default. Supporting references do not silently widen a surface's context/disclosure basis.

It explicitly does not contain DOM nodes, secrets, authorization decisions, copied canonical source data or durable Run state.

Changing the semantic context-reference set advances generation. Repeating the same normalized set is a no-op. `selection` exists only for compatibility and must not become a second context owner.

Future DANTE Context Builder logic remains purpose/recipient/sensitivity/freshness aware and reconstructs authorized context outside this React cursor.

## 4. Surface state model

The pure reducer supports finite operations:

```text
select context
set context
clear context
open surface
replace surface
promote surface
close surface
close top surface
```

`select context` remains a compatibility path around primary-context semantics; new production context ownership is `contextReferences`.

A surface descriptor keeps only finite presentation metadata:

```text
instance id
approved kind
semantic depth
presentation surface
origin
bound generation
bounded primary context reference when inherited/explicit
dismissibility
```

Semantic depth and geometry are separate axes.

`promote surface` remains transient surface-stack semantics. It does not mean persistent pin/config promotion.

## 5. Race / stale presentation protection

Async presentation intents may carry a bounded workspace expectation:

```text
expectedWorkspace {
  worldId
  generation
}
```

Invariant:

```text
request starts in World A at generation N
World/context changes or result is routed into World B
late presentation intent still expects { World A, N }
-> deterministic no-op
```

This closes both stale-generation and same-generation cross-World attachment classes. Generation alone is not a sufficient route/context identity.

This prevents late frontend presentation results from attaching to a newer or different World context. It does not replace future durable DANTE Run/effect semantics, backend authorization or execution revalidation.

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

Original platform closure HEAD:

`6c441335a75bb913af8da1eda569d8094d38a539`

Original platform CI:

`33549465793`

Final platform gate evidence at that closure:

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

M1 later added production validation for the generalized context-reference set and `expectedWorkspace { worldId, generation }` semantics. See `world-focus-m1-core-nonvisual-materialization-review.md` and `world-focus-m1-operational-handoff.md` for that later evidence.

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

D1 became the first concrete registered surface consumer. See `world-focus-d1-dante-entry-review.md` for its final engineering disposition.

D2–D6 remain deferred to M4 by current sequencing authority.

## 14. Historical notes superseded by this checkpoint

Earlier versions of this file stated:

```text
DANTE spatial gate still open
production registry intentionally empty
next gate = DANTE spatial reverse engineering
cursor = worldId + generation + selection + activeSurface only
race expectation = expectedGeneration only
```

Those statements described earlier implementation moments and are no longer live. D0/D1 and M1 provide the later accepted contracts described above.

## 15. Permanent barriers

```text
World != canonical Domain owner
layout policy != Domain semantics
surface stack != authorization
surface visibility != disclosure permission
contextReferences != authorization
supporting references != disclosure widening
AI output != accepted fact
AI proposal != user Decision
tool call != authorization
provider state != canonical state
planned != actual
absence != false
```
