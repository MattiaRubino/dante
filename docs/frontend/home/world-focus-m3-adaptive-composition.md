# DANTE — World Focus M3 Adaptive Composition

**Status:** M3 ACTIVE / M3-1 CLOSED / VALIDATED / M3-2 CLOSED / VALIDATED / M3-3 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`

This is the bounded engineering record for M3. It inherits closed M0–M2 semantics and does not reopen Domain, rendering, AuthZ, DANTE runtime or backend ownership.

## 1. M3 scope

Frozen M0 assignments:

```text
M0-37 production candidate resolver from meaningful projections     M3
M0-38 Customize Draft -> Apply/Cancel, pin/hide/reorder/promote     M3
M0-39 client config revision/conflict/migration representation      M3
M0-40 durable persistence/cross-device sync/conflict authority      BACKEND
```

M3 must reuse M1 application projections, M2 renderer vocabulary, the existing Workspace Platform composition planner, finite registry and CompositionHost. It must not create a second planner, page-per-World renderer fork, universal ranking score or fake persistence.

## 2. Permanent product rule — manual and DANTE share canonical paths

> Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI path where they are meaningful product functions.

```text
MANUAL UI [M3-3] ----\
                       -> finite commands -> DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

DANTE has no hidden mutation path and cannot bypass Apply, revision checking or conflict handling.

## 3. M3-1 — Composition Configuration Foundation — CLOSED / VALIDATED

Production owners:

```text
model/world-focus-composition-config.ts
application/world-focus-composition-customization.ts
```

Client configuration snapshot:

```text
schemaVersion
revision
worldId
ordered entries[]

entry
  instanceId
  kind
  visibility: visible | hidden
  pinned: boolean
  prominenceOverride: lead | null
```

It carries composition metadata only: no canonical Domain payload, AuthZ/disclosure authority, provider/runtime truth, renderer code or generic property bag.

Schema disposition is explicit:

```text
current
migration-required
unsupported
```

Customization transaction:

```text
CURRENT revision N
  -> DRAFT(baseRevision=N)
  -> pin / unpin / hide / show / move / promote / restore
  -> Apply | Cancel
```

Apply is the only transition creating revision `N+1`. Stale Apply returns `revision-conflict`; cross-World Apply fails closed; no implicit merge.

Evidence:

```text
RED  b68b6e8fa0d70844f6d058c7b77ded676f1e675f / CI 33850177297 EXPECTED FAILURE
PASS 49304c9231375a22ef74a81b4fffa920d5a1e849 / CI 33850441232 PASS
72 / 72 web test files
344 / 344 web unit tests
283 modules / 777 dependencies / 0 violations
```

## 4. M3-2 — Adaptive Candidate Resolver — CLOSED / VALIDATED

Production owners:

```text
application/world-focus-composition-opportunities.ts
application/world-focus-composition-resolver.ts
```

Tests:

```text
application/world-focus-composition-opportunities.test.ts
application/world-focus-composition-resolver.test.ts
```

M3-2 remains pre-planner and pre-renderer:

```text
validated M1 results
  -> meaningful opportunity extraction
  -> user config + finite value signals
  -> candidate resolver
  -> WorldFocusCompositionCandidate[]
  -> existing resolveWorldFocusCompositionPlan()
```

It does **not** mount UI and does not modify `world-focus-core-composition.tsx`.

### 4.1 Meaningful opportunity extraction

Only validated, meaningful application results become opportunities:

```text
Situation ready + non-empty               -> situation
Continuity ready/partial/stale + content  -> continuity
Continuity empty/unavailable              -> no opportunity
Attention ready                           -> attention:<primitive.instanceId> per item
Next ready + non-empty                    -> next
Comparison ready                          -> comparison:<primitive.instanceId> per item
Trajectory ready                          -> trajectory:<primitive.instanceId> per item
Evidence/History ready + any role content -> evidence-history
```

Sparse Worlds stay sparse. Renderer availability does not create an opportunity.

Opportunity metadata is deliberately narrow:

```text
instanceId
kind
defaultProminence
footprint
```

No source projection, context reference, `reasonCode`, canonical payload, disclosure/AuthZ state or executable renderer crosses this boundary. Opportunity set is bounded to 16 and rejects duplicate instance ids. Unknown future World/module kinds remain representable.

### 4.2 Finite value signals — no magic score

Allowed value signals:

```text
material-consequence
immediacy
resumability
meaningful-change
current-intent
```

There is no `score`, `confidence` or `aiRelevance` authority.

Deterministic bands:

```text
FOREGROUND
material-consequence OR immediacy OR current-intent
-> minimum prominence lead

ACTIVE
resumability OR meaningful-change
-> minimum prominence primary

ORDINARY
no asserted value signal
-> default opportunity prominence
```

Signals are positive, explicit application-owned assertions. Their absence is not interpreted as false.

### 4.3 Config precedence and user ownership

Precedence is explicit:

```text
hidden user config > ranking signals
pinned user config > adaptive budget
configured relative order > adaptive ranking
explicit promote -> lead presentation override only
```

Configured visible entries become user-origin candidates. Pinned meaningful entries become stable/user-owned and therefore survive adaptive budget pressure.

`hide != delete`, `pin != semantic truth`, `promote != semantic truth`.

If a pinned visible config entry currently has no meaningful projection:

```text
NO fabricated candidate
-> unresolvedPinned {
     reason: meaningful-projection-unavailable
   }
```

This preserves user intent without manufacturing content.

Unconfigured opportunities remain adaptive/application-derived and are ordered deterministically by value band, then source order.

### 4.4 Fail-closed boundaries

Resolver rejects:

```text
config World != opportunity World
config kind != meaningful opportunity kind
signal World != opportunity World
signal kind != opportunity kind
signal target no longer meaningful
multiple signal assignments for one opportunity
duplicate opportunity ids
duplicate signal kinds
```

Same inputs yield identical output.

### 4.5 Red-first and validation evidence

Operational PRE-SCOPE:

```text
c5fb717754792c2ad757444533302fbe0e0d5710
```

Its tree is byte-for-byte identical to the authorized `4f18f89e35d217c05ca0c2153e82573957e8f42d`; intervening commits only created/deleted empty connector side-effect files.

Red test-only proof:

```text
HEAD c2688c46bcbdaf06f2c5da9470bae967550b456d
CI   33854105057 EXPECTED FAILURE
```

Pre-production contracts passed. Quality failed because the two M3-2 owner modules did not yet exist.

Initial production candidate:

```text
HEAD 6486c99ce1f83d3fe463c2a1b065fa994b206c6a
CI   33854374288
```

Production itself had no observed lint issue; Quality stopped on one unsafe Vitest matcher in the new opportunity test. The assertion was strengthened, not weakened, to check every opportunity directly for absence of `projection`.

Validated code head:

```text
HEAD b7892642dd66104ec04ea4b08ca11aa123789fa4
CI   33854543037 PASS
```

Observed validation:

```text
Frontend pre-production contracts PASS
Lint                              PASS
Typecheck                         PASS
Architecture                      PASS
Generated-source drift            PASS
Web test files                    74 / 74 PASS
Web unit tests                    356 / 356 PASS
Architecture graph                287 modules / 797 dependencies / 0 violations
Production build                  PASS
Diff check                        PASS
Repository mutation check         PASS
Mobile Bundle                     PASS
Web E2E / Chromium                PASS
frozen Timeline Firefox           PASS
Frontend CI Gate                  PASS
```

## 5. M0 L5 disposition after M3-2

```text
M0-35 stability/origin semantics                         EXISTING / PRESERVE
M0-36 prominence/footprint/grid planner                  EXISTING / PRESERVE
M0-37 production candidate resolver                      M3-2 CLOSED / VALIDATED
M0-38 Draft/Apply/Cancel + pin/hide/reorder/promote     MODEL M3-1 CLOSED; UI M3-3 NEXT
M0-39 client revision/conflict/migration representation M3-1 CLOSED / VALIDATED
M0-40 durable persistence/cross-device sync/conflict    BACKEND-DEFERRED
```

## 6. Explicit non-work in M3-2

```text
NO live `world-focus-core-composition.tsx` changes
NO new renderer mounting
NO Customize UI / drag-drop / keyboard controls
NO localStorage or server persistence
NO DANTE D2–D6 runtime work
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral changes
```

## 7. Next gate — M3-3 Manual Customize UX

M3-3 is next and not started. It must materialize the **manual** product surface over the already-validated M3-1 command language and respect M3-2 composition truth.

Expected capabilities:

```text
enter Customize explicitly
operate on a draft, never current config directly
pin / unpin
hide / show
reorder
promote / restore
review changed state
Apply / Cancel
revision-conflict treatment
keyboard + touch accessibility
responsive behavior
```

Drag-and-drop may be one interaction, but it is not the state model and cannot be the only accessible reorder path.

M3-3 must not integrate adaptive candidates into live World composition yet; that remains M3-4.

## 8. Stop line

```text
M3-3 Manual Customize UX                 NEXT
M3-4 Integrated Adaptive Composition     BLOCKED BY M3-3
M3 final hostile closure                 BLOCKED BY M3-4
M4 D2–D6 contextual DANTE                BLOCKED BY M3
M5–M7                                    BLOCKED BY SEQUENCE
BACKEND                                  BLOCKED UNTIL M7
```

A fresh explicit write gate is required before M3-3.
