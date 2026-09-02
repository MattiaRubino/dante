# DANTE — World Focus Post-WS8 Coherence / Hygiene Audit

**Status:** APPLIED — LOCAL POST-CLOSURE HYGIENE, WS0–WS8 NOT REOPENED  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`  
**Initial pre-scope:** `7b1a862e02475f9ecb8efcfb1111a9eca526a827`

This audit was performed after WS8 closure to answer a different question from substrate convergence:

> Does the current repository still contain stale live routing, local runtime bugs, orphaned scaffolding or superseded implementation residue that contradicts the state we now claim?

It does not replace WS8 falsification evidence and does not authorize M0/M1–M7 or backend work.

---

## 1. Scope reviewed

The pass cross-checked:

```text
branch-level current checkpoint / handoff
World Focus current checkpoint / evidence map
WS7 executable harness evidence
WS8 stateful + mutation + confirmation evidence
World Focus model/application/UI ownership
route-backed Home -> World Focus entry
finite module/surface registries
workspace reducer/allocation contracts
D1 contextual DANTE entry boundary
visual frame / WebGL candidate residue
explicit deprecated frontend debt
```

The audit distinguished:

```text
semantic/substrate contradiction
runtime-local bug
live-authority documentation drift
orphaned/premature scaffold
superseded dead implementation residue
explicit cross-workstream deprecated debt
```

---

## 2. Closure result

The WS0–WS8 substrate closure still holds.

No evidence required:

```text
new L1 primitive
new World ownership layer
new generic root
page-per-World architecture
AI-required basic World path
new Domain/Logical/Physical interpretation
new privacy/disclosure architecture
new backend owner
```

Therefore WS0–WS8 were not reopened.

---

## 3. HYG-01 — Unknown popover fallback pointer barrier

Registered popovers already rendered inside a pointer-transparent surface wrapper so the non-modal World remained physically interactive outside the actual panel.

The unregistered-surface fallback bypassed that behavior: `.world-focus-surface` restored `pointer-events:auto`, and an overlay-slot unknown `popover` could therefore become a full-area physical click barrier even though the allocation contract still considered the main World interactive.

Fix:

```text
full overlay fallback remains pointer-transparent
explicit dismiss control remains pointer-interactive
local unsupported-content degradation retained
keyboard dismissal retained
```

A regression test covers the unregistered-popover combination directly.

Classification: runtime-local surface fallback bug; not a new substrate class.

---

## 4. HYG-02 — Unused motion-preference scaffold

`world-focus-motion-preference.ts` exposed and persisted `immersive | instant` through localStorage and exported it from the feature API, but the active Home -> World route and `WorldFocusPage` did not consume that preference.

The real WebGL renderer independently honors `prefers-reduced-motion`.

Removed:

```text
world-focus-motion-preference.ts
world-focus-motion-preference.test.ts
public exports from world-focus/index.ts
```

This removes premature hidden persistence without rejecting a future earned user-facing preference.

---

## 5. HYG-03/HYG-04 — Superseded visual residue

The active page imports the V4 candidate stylesheet, but V2 and V3 remained in the source tree. The structural base stylesheet also retained selectors for an older SVG corona/halo/thread/orbit/particle renderer no longer emitted by the current `WorldFocusVisualFrame`.

Removed:

```text
world-focus-visual-frame-v2.css
world-focus-visual-frame-v3.css
legacy SVG renderer rules from world-focus-visual-frame.css
```

The base stylesheet now owns only structural visual-frame placement and ambient-field geometry. V4 owns the current candidate visual treatment.

WF0 and WF-G3 are unchanged.

---

## 6. HYG-05 — Stale live branch routing

The detailed World Focus checkpoint correctly said `WS0–WS8 CLOSED / M0 NEXT`, while the two branch-level entry documents still routed a new chat/agent to `D2 NEXT`.

Aligned:

```text
docs/frontend/home/current-checkpoint.md
docs/frontend/home/production-depth-handoff.md
world-focus-current-checkpoint.md
world-focus-evidence-index.md
```

Current sequencing is now unambiguous:

```text
WS0–WS8 CLOSED
post-WS8 hygiene applied
M0 NEXT / NOT STARTED
D2–D6 deferred to later M4 materialization
```

---

## 7. HYG-06 — World switch retained stale route-entry provenance

### Finding

`WorldFocusPage` initialized the transient route entry with:

```text
useState(() => readWorldFocusEntry(world.id, source))
```

The workspace owner already resets by `worldId`, but the page-level entry snapshot did not. If the same page component instance receives a different World, the old entry provenance could survive and incorrectly preserve:

```text
data-entry-origin = live
preferHistory = true
```

for a World that was actually reached as a fallback/direct route.

### Fix

Entry resolution is now memoized by the actual route identity:

```text
world.id + source
```

A regression test rerenders the same page instance from a live Home-opened Music World to a direct/fallback Travel World and asserts both the provenance and Escape close policy are rebound.

### Classification

```text
runtime-local route lifecycle bug
not a new substrate/race class
```

---

## 8. Explicitly not changed — Global Topbar Review

The global `Review` control remains visibly disabled and is already classified `DEPRECATED` in Home/AppShell authorities because its role overlaps the accepted Resolution concept.

It is real debt, but it is owned by shared AppShell/Home rather than World Focus. Removing or redirecting it changes a global access pattern and requires its own bounded AppShell/Home cleanup scope with synchronized `contract.md`, `ui-registry.md`, tests and shell behavior.

This audit records but does not silently mutate it.

---

## 9. Evidence truth

The validated WS8 proof/runtime evidence remains:

```text
HEAD 88db899391a3a41e23e76177d4896a657232b5eb
Frontend CI 33639741630 PASS — attempt 1
```

Post-WS8 hygiene is later code/documentation state and must be evaluated on its own final commit. This document does not pre-claim a PASS.

---

## 10. Final disposition

```text
WS0–WS8 semantic/substrate closure        HOLDS
unknown-popover pointer barrier            FIXED
stale World-switch entry provenance        FIXED
orphaned persisted motion preference       REMOVED
superseded V2/V3 visual CSS                 REMOVED
legacy SVG visual CSS                       REMOVED
live D2 routing drift                       FIXED
Global Topbar Review debt                   DEFERRED TO ITS OWNER
M0                                          NEXT / NOT STARTED
backend                                     NOT STARTED
```

The repository is materially more coherent after this pass without manufacturing new product capability or changing closed substrate semantics.
