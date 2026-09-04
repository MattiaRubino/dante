# DANTE — World Focus M3-4 Integrated Adaptive Composition Review

**Status:** M3-4 CLOSED / VALIDATED — CODE/TEST FULL PASS  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`  
**Authorized PRE-SCOPE:** `688e1ab0c7a42f8d83274dedf5a2988a9388bda4`  
**Code/Test HEAD:** `b10dc2bef8bab6ae863ce3c8331da6de96094a66`  
**Frontend CI:** `33904052325` / run #934 PASS

M3-4 is the phase that connected the already-validated M1 -> M3-2 -> Workspace Platform -> M2 path to normal live World rendering. It does not close M3 as a whole. M3 final hostile closure is next.

## 1. Permanent authority retained

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

A World remains a shared coordinate system between user and DANTE, not a shared source of truth.

Permanent non-collapses remain in force:

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
AI output != accepted fact
Proposal != Decision != effect
Comparison != Decision
client composition config != canonical Domain state
client revision != backend persistence revision
renderer availability != mandatory mounting
adopt != semantic truth != authorization != persistence
```

## 2. Integrated production path

Normal World rendering now uses:

```text
seven existing M1 runtime readers
  Situation
  Continuity
  Attention
  Next
  Comparison
  Trajectory
  Evidence / History
-> one bounded adaptive-composition snapshot
-> M3-2 meaningful opportunity extraction
+ the exact accepted M3-3 composition-config owner
+ no invented M4/DANTE ranking signals
-> M3-2 candidate resolver
-> existing resolveWorldFocusCompositionPlan()
-> finite World module registry
-> WorldFocusCompositionHost
-> M2 display-safe renderers
```

The same snapshot supplies both opportunity meaning and renderer-safe display bindings. Apply does not create a second store or a second read path.

## 3. New production owners

```text
application/world-focus-adaptive-composition.ts
ui/presentation/world-focus-pre-backend-display-bindings.ts
ui/world-focus-adaptive-composition.tsx
```

Existing owners were integrated rather than replaced:

```text
model/world-focus-composition-plan.ts
ui/world-focus-core-composition.tsx
ui/world-focus-composition-host.tsx
ui/world-focus-continuity.tsx
ui/world-focus-page.tsx
ui/world-focus-workspace.tsx
```

No second planner, second registry, AppShell composition engine or page-per-World fork was added.

## 4. Behavior proven

```text
sparse projection set -> sparse composition
empty/unavailable semantic result -> no fabricated module
hidden config -> hidden candidate
pinned meaningful content -> survives adaptive budget
unresolved pinned intent -> explicit unresolved intent, no renderer fabrication
configured user relative order -> preserved
pin -> budget survival, not implicit reorder
promote -> prominenceOverride=lead, not implicit reorder
configured supporting -> remains supporting unless explicitly promoted
unknown future kind -> local unsupported fallback
registered renderer failure -> local error boundary fallback; healthy siblings remain
accepted config after Apply -> immediately consumed by normal composition owner
client accepted config remains in-memory composition metadata only
```

## 5. Ordering reconciliation discovered during integration

M3-2 correctly preserved configured order before the planner, but the pre-existing planner then sorted adaptive candidates by prominence. M3-4 integration exposed the cross-layer contradiction.

The final planner keeps selection/budgets/grid packing unchanged and resolves a deterministic partial order satisfying all retained laws:

```text
explicit user move order
stable relative order
non-user dynamic lead policy
stable before non-user dynamic non-lead
existing platform policy as deterministic tie-break where unconstrained
```

This prevents `pin` or `promote` from silently becoming `move` while preserving older Workspace Platform guarantees.

## 6. Accessibility correction discovered by live mounting

Once normal World composition grew beyond the former Continuity-only feed, the main plane became materially scrollable. Axe correctly reported `scrollable-region-focusable`.

The active main plane is now keyboard focusable; when allocation makes it inert, it does not receive a tab stop. No axe rule was disabled and no CSS workaround was used.

## 7. Renderer failure falsification

A final test-only RED proved that calling a registry renderer directly in the parent meant a synchronous renderer throw happened before `WorldFocusRenderBoundary` could catch it.

Valid RED:

```text
HEAD d2af7a47df8562439487fb4ab4298bff4653f098
Frontend CI 33903884239 / run #933 EXPECTED FAILURE
386 pre-existing web tests PASS
1 new renderer-isolation test FAIL
failure: `renderer failed` escaped before the boundary
```

Root-cause fix:

```text
b10dc2bef8bab6ae863ce3c8331da6de96094a66
fix(home): isolate M3-4 renderer failures
```

Renderer execution now occurs in a small child component inside the existing boundary. Unknown-kind (`unsupported`) and registered-runtime-error (`error`) remain distinct states.

## 8. Implementation / falsification sequence

```text
5221467f260450b339e37021984365884d0b22d5  integrate M3-4 adaptive composition
f527df982c234df5b0761ea4b96a9ff00d7ae1d7  clear lint/typing gate
50725c44f6b3d83069abc3654a36b0c7b0ddbd99  harden integrated invariants
b17a42e348bf4e87b0a229edebccdbc97d134ca9  first order correction; later falsified as too local
6a1583c7499eb9eeda34aa7b7c13072d8db24a2c  reconcile planner ordering laws
7d5dbd6df986227de73078ae1664ccd8c8534109  restore browser scroll accessibility
 d2af7a47df8562439487fb4ab4298bff4653f098 renderer-isolation RED
b10dc2bef8bab6ae863ce3c8331da6de96094a66  isolate renderer failures / final code-test baseline
```

Intermediate red gates were fixed at root cause; assertions were not weakened to obtain green.

## 9. Final validation evidence

Code/Test HEAD `b10dc2bef8bab6ae863ce3c8331da6de96094a66`:

```text
Frontend CI                         33904052325 / run #934 PASS
Frontend pre-production contracts   PASS
World Focus pre-production contracts PASS
Web test files                      79 / 79 PASS
Web unit tests                      387 / 387 PASS
Architecture                        299 modules / 891 dependencies / 0 violations
Lint                                PASS
Typecheck                           PASS
Generated-source drift              PASS
Production build                    PASS
Diff check                          PASS
Repository mutation check           PASS
Mobile Bundle                       PASS
Chromium                            PASS
frozen Timeline Firefox             PASS
Frontend CI Gate                    PASS
```

Automated green does not equal human visual acceptance. Human/manual visual review remains **NOT PERFORMED**.

## 10. Exact scope audit

Compare:

```text
688e1ab0c7a42f8d83274dedf5a2988a9388bda4
...
b10dc2bef8bab6ae863ce3c8331da6de96094a66

status    ahead
ahead_by  8
behind_by 0
```

Changed non-doc paths:

```text
apps/web/e2e/world-focus-composition-customization.spec.ts
apps/web/e2e/world-focus-workspace-platform.spec.ts
apps/web/src/features/world-focus/application/world-focus-adaptive-composition.test.ts
apps/web/src/features/world-focus/application/world-focus-adaptive-composition.ts
apps/web/src/features/world-focus/model/world-focus-composition-plan.test.ts
apps/web/src/features/world-focus/model/world-focus-composition-plan.ts
apps/web/src/features/world-focus/ui/presentation/world-focus-pre-backend-display-bindings.ts
apps/web/src/features/world-focus/ui/world-focus-adaptive-composition.tsx
apps/web/src/features/world-focus/ui/world-focus-composition-customization.test.tsx
apps/web/src/features/world-focus/ui/world-focus-composition-host.test.tsx
apps/web/src/features/world-focus/ui/world-focus-composition-host.tsx
apps/web/src/features/world-focus/ui/world-focus-continuity.tsx
apps/web/src/features/world-focus/ui/world-focus-core-composition.tsx
apps/web/src/features/world-focus/ui/world-focus-page.test.tsx
apps/web/src/features/world-focus/ui/world-focus-page.tsx
apps/web/src/features/world-focus/ui/world-focus-workspace.tsx
```

No Timeline implementation, AppShell, Access/Auth, generated route tree, backend/API/DB/Alembic/AuthZ/provider/LLM or persistence path changed.

## 11. Current sequence after closure

```text
M3-1                              CLOSED / VALIDATED
M3-2                              CLOSED / VALIDATED
PRE-M3-3 safety                   CLOSED / PASS
M3-3                              CLOSED / VALIDATED
M3-4                              CLOSED / VALIDATED
M3 final hostile closure          NEXT / NOT STARTED
M4 Contextual DANTE / D2-D6       BLOCKED BY M3
M5-M7                             BLOCKED BY SEQUENCE
BACKEND                           AFTER M7 ONLY
```

M3 final closure must attack the combined M3 layer rather than add feature scope: conflicting config, stale/partial inputs, sparse and dense worlds, many candidates, adopted/hidden/pinned combinations, unknown kinds, responsive behavior and failure isolation.
