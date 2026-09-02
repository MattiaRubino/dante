# DANTE — World Focus M1 Core Non-Visual Materialization Review

**Status:** M1 ACTIVE — SUBBLOCK 1 IDENTITY / REFERENCE OWNERSHIP CLOSED / NON-VISUAL FACETS NEXT  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`

This document is the live M1 execution evidence. M0 remains the scope-freeze authority; this review records what has actually been materialized and validated in production code.

## 1. M0 prerequisite

M0 is CLOSED.

```text
M0 closure docs HEAD  6ea74f630cb35af65d58e7ae873882d6d975411e
Frontend CI           33668744509 — PASS
66 decisions assigned
unowned material rows 0
```

Authority: `world-focus-m0-materialization-mapping.md`.

## 2. Subblock 1 validated result

Validated code HEAD:

```text
e0f4003496bfbf828ed9ab7718af8e7e30342ad3
```

Frontend CI:

```text
33679425668 — PASS
```

Validated jobs:

```text
contract drift                PASS
active Home format            PASS
lint                          PASS
typecheck                     PASS
architecture                  PASS
generated-source drift        PASS
unit tests                    PASS
production build              PASS
diff check                    PASS
repository mutation check     PASS
Mobile Bundle                 PASS
Chromium Web E2E              PASS
Firefox frozen Timeline       PASS
Frontend CI Gate              PASS
```

This closes M0-03, M0-09, M0-11 and the production materialization portion of M0-12. M1 overall remains ACTIVE.

## 3. Production World identity

New neutral owner:

`apps/web/src/features/world-focus/model/world-focus-identity.ts`

Production identity is now open-ended:

```text
WorldFocusId = string
WorldFocusIdentityDescriptor = { id, label, description }
```

`normalizeWorldFocusId()` validates/normalizes an opaque identifier only. It does NOT establish:

```text
World existence
routability
canonical membership
authorization
disclosure
backend persistence
```

The ten current World IDs remain deterministic fixture/catalog data only.

`world-focus-fixtures.ts` now owns `WorldFocusFixtureId`; it is explicitly not the permanent World taxonomy.

## 4. Route validity remains explicit

`/_app/worlds/$worldId` now performs two distinct steps:

```text
URL token
-> normalize opaque WorldFocusId
-> resolve registered deterministic fixture/catalog entry
-> if unresolved: redirect /worlds
-> if resolved: build WorldFocusIdentityDescriptor
-> render WorldFocusPage
```

Therefore `/worlds/arbitrary-token` does not create a World merely because production identity is open-ended.

This is deliberate:

```text
open-ended identity != open-ended routability
```

A future real application resolver may replace the deterministic fixture catalog without changing Page/Context identity ownership.

## 5. Neutral context-reference owner

New neutral owner:

`apps/web/src/features/world-focus/model/world-focus-context-reference.ts`

It owns:

```text
WorldFocusContextReference { kind, key }
WorldFocusContextReferenceSet {
  primary
  supporting[]
}
```

Properties:

```text
normalization
non-empty kind/key
bounded supporting references
ordered supporting semantics
deduplication
primary/supporting duplicate rejection
semantic comparison
```

Default supporting-reference maximum is 4. This is a frontend bounded-context policy, not a backend/domain relationship limit.

References remain identity/hints only; they are never canonical payload copies or authorization grants.

## 6. Workspace / cursor materialization

`world-focus-workspace.ts` no longer owns the generic reference type.

Canonical transient context state is now:

```text
contextReferences: WorldFocusContextReferenceSet | null
```

The old `selection` remains temporarily as a compatibility projection of `contextReferences.primary` for existing callers/tests. It is no longer the semantic owner.

New reducer intent:

```text
set-context
```

Existing `select-context` remains a single-primary convenience.

Behavior:

```text
same semantic reference set -> exact no-op
changed set -> generation +1
clear-context -> clears entire set atomically
surface default context -> primary only
interaction cursor -> full primary + ordered supporting set
```

Supporting references are deliberately NOT silently copied into every surface. This prevents accidental over-context/disclosure widening.

`WorldFocusWorkspaceHost` exposes `setContextReferences()` while retaining `selectContext()` for bounded compatibility.

## 7. Transitional compatibility note

`getWorldFocusInteractionCursor()` currently preserves the historical enumerable cursor shape while exposing `contextReferences` as a non-enumerable frozen property.

Purpose:

```text
avoid unrelated exact-object-shape regression while M1 migrates callers
```

This is transitional compatibility, not the desired permanent representation. Before M1 closes, deliberately review/remove this compatibility trick and migrate exact-shape tests/callers to the canonical cursor contract.

Do not let this become accidental permanent architecture.

## 8. WP / oracle ownership cleanup

`world-focus-work-primitives.ts` imports `WorldFocusContextReference` from the neutral owner, not workspace.

`world-focus-substrate-oracle.ts` no longer duplicates primary/supporting normalization, bounds and dedup logic. Its compatibility helper delegates to `createWorldFocusContextReferenceSet()`.

The WS7/WS8 oracle remains proof/audit code. It is NOT promoted into runtime authority.

## 9. Continuity / Orientation alignment

`application/world-focus-continuity.ts` now validates against production `WorldFocusId`, while still requiring returned projection `worldId` to equal the requested World.

Open-ended identity therefore does not weaken request/result binding.

`WorldFocusContext` now consumes `WorldFocusIdentityDescriptor` directly instead of indexing the fixture union for label/description.

A test renders an unknown future descriptor (`future-craft`) without new component branching or invented analytical controls.

`WorldFocusPage` separates:

```text
identity descriptor -> id / label / description / workspace / DANTE coordinate
fixture presentation profile -> current pre-backend accent / VFX theme only
```

This keeps the existing VFX fixture concern from becoming the production identity model.

## 10. Public API alignment

The World Focus public feature API exports:

```text
production World identity + descriptor
fixture catalog types distinctly
neutral context-reference owner
```

This prevents downstream callers from treating the ten fixture IDs as the only legal production identity type.

## 11. Red-green engineering evidence

During this subblock the gates found real integration issues and were not weakened.

### Run 33678846241

Lint found a stale unused nested `world` prop after descriptor extraction.

Resolution: remove only that dead nested prop; the outer `world` fixture remains required by the visual frame.

### Run 33679150160

Typecheck found:

```text
exactOptionalPropertyTypes incompatibility for explicitly absent supporting refs
manual malformed allocation fixture missing contextReferences
```

Resolution:

```text
neutral constructor explicitly tolerates supporting: undefined at its input boundary
legacy malformed test fixture explicitly declares contextReferences: null
```

The production workspace type was not weakened to optional.

That run also had one unrelated Timeline Chromium flake in `split and merge remain reversible...`; all World Focus E2Es were green. No Timeline production code was modified.

### Run 33679425668

Full PASS. The Timeline failure did not reproduce; Chromium and Firefox both passed.

## 12. New/updated tests

Added:

```text
world-focus-identity.test.ts
world-focus-context-reference.test.ts
world-focus-workspace-context-set.test.ts
```

Updated:

```text
world-focus-context.test.tsx
world-focus-page.test.tsx
world-focus-workspace-allocation.test.ts
```

Coverage includes:

```text
opaque future World id
explicit production descriptor
unknown future descriptor rendering
primary + ordered supporting references
reference bounds and duplicate rejection
semantic no-op equality
workspace generation change
surface-primary inheritance only
full cursor reference set
atomic context clear
existing route/VFX/transition/focus behavior
```

## 13. Remaining M1 work

M1 is NOT closed. Next non-visual materialization must cover the remaining M0-frozen deltas:

```text
M0-15 reference resolution presentation vocabulary
M0-17 stronger WP-01 production alignment
M0-18 WP-02 Attention application/model seam
M0-20 WP-03 Comparison application/model seam
M0-22 WP-04 Trajectory application/model seam
M0-25..27 L2 basis/freshness/validity/evidence facets
M0-31 L3 sanitized disclosure outcome facet
M0-41 L6 effect lifecycle presentation model
M0-54 L8 offline/replay/provider-lag representation
O2 Situation typed direct application seam
O5 Next typed direct application seam
O8 Evidence/History typed direct application seam
deterministic pre-backend adapters/tests for these seams
```

Also revisit the transitional cursor enumerable-shape compatibility before M1 closure.

## 14. Stop lines

Still forbidden in M1:

```text
M2 shared visual renderers
M3 customization / pin / hide / reorder
D2–D6 / M4
complete World materialization / M5
integrated visual acceptance / M6
backend/API/DB/Alembic/AuthZ/provider/LLM/tools/effects
```

## 15. Final disposition

```text
M0                                  CLOSED / CI PASS
M1 overall                          ACTIVE
M1 subblock 1 identity/reference    CLOSED / CI PASS
M1 non-visual facets                NEXT
M2–M7                               BLOCKED
BACKEND                              BLOCKED UNTIL M7
```

Immediate continuation:

> Continue M1 with the narrow reusable non-visual state/facet layer and typed O2/O5/O8 + WP application seams. Do not start renderers.
