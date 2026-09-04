# DANTE — World Focus M3 Adaptive Composition

**Status:** M3 ACTIVE / M3-1 COMPOSITION CONFIGURATION FOUNDATION CLOSED / VALIDATED / M3-2 NEXT  
**Date:** 2026-09-04  
**Branch:** `feature/home-react`

This document is the bounded engineering record for M3. It inherits the closed M0–M2 semantics and does not reopen renderer, Domain, AuthZ, DANTE-runtime or backend ownership.

## 1. M3 scope

M3 owns adaptive World composition over already-earned application semantics and approved renderers.

Frozen M0 assignments:

```text
M0-37 production candidate resolver from meaningful projections     M3
M0-38 Customize Draft -> Apply/Cancel, pin/hide/reorder/promote     M3
M0-39 client config revision/conflict/migration representation      M3
M0-40 durable persistence/cross-device sync/conflict authority      BACKEND
```

M3 must reuse:

```text
M1 semantic/application projections
M2 finite renderer vocabulary
Workspace Platform composition planner
finite module registry
CompositionHost placement/isolation
```

M3 must not create a second planner, page-per-World renderer fork, universal ranking score or fake backend persistence.

## 2. Product rule — manual capability and DANTE use the same canonical path

Permanent product rule established before M3:

> Canonical app capabilities that DANTE may propose or accelerate must remain usable through a manual/non-AI path where they are meaningful product functions.

M3-1 encodes this at the configuration-command boundary:

```text
MANUAL UI [M3-3]
        \
         -> finite customization commands -> DRAFT -> REVIEW/APPLY -> CONFIG
        /
DANTE proposal [M4]
```

DANTE does not receive a hidden mutation path. A `dante-proposed` command modifies the same draft as a manual command and cannot bypass Apply, revision checking or later review UX.

This does not require a one-button UI equivalent for arbitrary natural-language requests. It requires that canonical application state transitions remain product capabilities rather than chat-only magic.

## 3. M3-1 production owners

```text
apps/web/src/features/world-focus/model/
  world-focus-composition-config.ts

apps/web/src/features/world-focus/application/
  world-focus-composition-customization.ts
```

Tests:

```text
apps/web/src/features/world-focus/model/
  world-focus-composition-config.test.ts

apps/web/src/features/world-focus/application/
  world-focus-composition-customization.test.ts
```

M3-1 does not touch live `world-focus-core-composition.tsx` and does not mount new renderers.

## 4. Composition configuration snapshot

`WorldFocusCompositionConfig` is client composition metadata only:

```text
schemaVersion
revision
worldId
ordered entries[]
```

Each entry contains only:

```text
instanceId
kind
visibility: visible | hidden
pinned: boolean
prominenceOverride: lead | null
```

The constructor reconstructs only allowed fields, so arbitrary extra payload is stripped rather than retained.

Explicit exclusions:

```text
NO canonical Domain payload
NO AuthZ/disclosure authority
NO provider/runtime truth
NO renderer JSX/functions/executable code
NO generic property bag
```

Unknown future `kind` values remain representable because module kind is an open renderer identifier, not a permanent World/Domain taxonomy.

## 5. Schema/revision semantics

Current client schema:

```text
WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION = 1
```

Version inspection is explicit:

```text
current
migration-required { fromVersion }
unsupported { schemaVersion }
```

M3-1 does not silently migrate and does not invent a universal migrator.

`revision` must be a non-negative safe integer. `worldId`, `instanceId` and `kind` are normalized/non-empty. Duplicate `instanceId` fails closed.

Durable persistence, server revision, cross-device merge and authoritative conflict resolution remain backend-deferred.

## 6. Customization transaction

Customization begins from an immutable current config:

```text
CURRENT CONFIG revision N
        ↓
begin customization
        ↓
DRAFT
  worldId
  baseRevision = N
  baseConfig
  workingConfig
  operations[]
```

Draft operations never mutate the current config.

Finite command language:

```text
pin
unpin
hide
show
move
promote
restore
```

Sources are finite:

```text
manual
dante-proposed
```

No generic `patch`, arbitrary `Record<string, unknown>` or remote/model-generated mutation language exists.

## 7. Command semantics

```text
hide      != delete
pin       != canonical truth/freeze
promote   != semantic importance fact
move      != Domain ordering
restore   = restore that entry to the draft-start base state + base position
```

`move` may place before another existing instance or at the end. Missing target/destination fails closed. Same command sequence over the same base config is deterministic.

## 8. Apply / Cancel / conflict

Cancel:

```text
DRAFT -> CANCEL -> baseConfig
```

No side effect is committed.

Apply is the only M3-1 operation that creates a new current revision:

```text
current.worldId == draft.worldId
AND
current.revision == draft.baseRevision
        ↓
APPLIED config revision N+1
```

Stale revision:

```text
revision-conflict {
  baseRevision
  currentRevision
}
```

No implicit merge.

Cross-World Apply is rejected even if numeric revisions happen to match.

A `dante-proposed` operation has exactly the same Apply barrier as a manual operation.

## 9. Red-first evidence

Test-only red commit:

```text
HEAD b68b6e8fa0d70844f6d058c7b77ded676f1e675f
CI   33850177297 EXPECTED FAILURE
```

The two M3-1 tests were committed before production owners. Frontend pre-production contracts passed; Quality failed at lint/type resolution because the two new M3 modules did not yet exist. The cascade was caused by unresolved owner modules, not weakened assertions.

The tests fixed obligations before implementation, including:

```text
immutable current config / isolated draft
Cancel no-op on current state
Apply revision +1 exactly once
stale revision conflict
cross-World rejection
duplicate instance rejection
unknown future kind representation
schema disposition current/migration-required/unsupported
hide != delete
restore base state/order
missing move target fail closed
deterministic command sequence
no generic patch/property bag
manual and dante-proposed share one command language
DANTE proposal cannot bypass Apply
```

## 10. Validated implementation evidence

Production head:

```text
HEAD 49304c9231375a22ef74a81b4fffa920d5a1e849
CI   33850441232 PASS
```

Observed validation:

```text
Frontend pre-production contracts PASS
Lint                              PASS
Typecheck                         PASS
Architecture                      PASS
Generated-source drift            PASS
Web test files                    72 / 72 PASS
Web unit tests                    344 / 344 PASS
Architecture graph                283 modules / 777 dependencies / 0 violations
Production build                  PASS
Diff check                        PASS
Repository mutation check         PASS
Mobile Bundle                     PASS
Web E2E / Chromium                PASS
frozen Timeline Firefox           PASS
Frontend CI Gate                  PASS
```

No test expectation was weakened after the red run.

## 11. M3-1 closure

M3-1 is closed for:

```text
client composition config snapshot
schema-version disposition
client revision representation
isolated customization draft
finite manual/DANTE-proposed command language
pin/unpin/hide/show/move/promote/restore semantics
Cancel without side effects
Apply with optimistic revision guard
explicit revision-conflict result
cross-World apply rejection
```

M3 itself remains active.

## 12. Explicitly not implemented by M3-1

```text
NO candidate ranking/resolver                       -> M3-2
NO Customize UI / drag/drop / keyboard controls    -> M3-3
NO integration into live World composition          -> M3-4
NO localStorage fake persistence
NO durable persistence/cross-device sync            -> backend
NO new live O2/O5/O8 or WP-02..04 mounting
NO DANTE runtime / D2–D6                            -> M4
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO Timeline/AppShell/Access/Auth collateral work
```

## 13. Next gate — M3-2

M3-2 is the Adaptive Candidate Resolver.

It must derive bounded composition candidates from meaningful already-authorized application projections and user composition configuration, then feed the existing planner rather than replacing it.

Conceptual path:

```text
meaningful available projections
+ current user composition config
+ bounded contextual ranking inputs
        ↓
M3-2 candidate resolver
        ↓
WorldFocusCompositionCandidate[]
        ↓
existing resolveWorldFocusCompositionPlan()
        ↓
existing CompositionHost
```

Permanent constraints for M3-2:

```text
stable/pinned user intent cannot be silently overridden
sparse World remains sparse
renderer availability != mandatory mounting
no AI relevance score as sole authority
no universal confidence score
ranking cannot invent semantic truth
candidate resolver != AuthZ
no backend/persistence pulled forward
```

M3-2 requires a fresh explicit write gate before implementation.
