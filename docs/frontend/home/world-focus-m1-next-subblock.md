# DANTE — World Focus M1 Next Subblock

**Status:** M1 ACTIVE — NEXT EXECUTION SCOPE FROZEN  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`

This is the narrow continuation after the validated identity/reference subblock.

## Next objective

Materialize the remaining reusable non-visual frontend facets and typed application seams earned by M0, while preserving Domain/backend authority boundaries.

### Required model/application work

```text
1. reference-resolution presentation vocabulary
   usable / unresolved / retired-style safe frontend states
   no silent merge/split retarget authority

2. L2 narrow facets
   freshness / as-of
   material basis reference
   coverage/incomplete/conflict
   validity / superseded / retracted
   redaction/tombstone-safe presentation metadata
   evidence/provenance metadata only where needed

3. L3 sanitized disclosure outcome
   available / restricted / unavailable-style frontend outcome
   no frontend AuthZ decision
   no recipient/purpose widening

4. L6 effect-presentation vocabulary
   pending / ambiguous / partial-real / reconciliation-required / reversed-or-compensated distinctions
   execution-time revalidation flag/state
   no real execution

5. L8 offline/sync presentation
   offline/replay/provider-lag/timeout as truthful frontend states
   provider timeout != semantic negative

6. direct typed Output Grammar seams
   O2 Situation
   O5 Next
   O8 Evidence / History

7. L1 application seams
   strengthen WP-01 Continuity alignment
   WP-02 Attention
   WP-03 Comparison
   WP-04 Trajectory
```

## Design constraint

Do NOT create one universal `ProjectionEnvelope` containing every possible field. Prefer narrow reusable facets composed only by projections that need them.

Do NOT create generic `Thing`, `Entity`, `Fact`, `Relationship`, `PropertyBag`, frontend ACL or World-owned canonical state.

## Test pressure

At minimum pressure:

```text
current vs stale vs superseded/retracted
partial/conflicted/missing evidence
redacted/tombstoned source visibility
stable vs ambiguous vs retired reference
allowed vs restricted disclosure outcome
offline/replay/provider lag
pending/ambiguous/partial real effect
execution revalidation requirement
unknown future World id
authorized basic path without DANTE
late/stale generation rejection where applicable
```

Reuse the WS7/WS8 invariants as falsification reference, but do not promote the oracle to production runtime.

## Explicitly out of scope

```text
M2 renderers/cards/charts
M3 pin/hide/reorder/customization
M4 D2–D6
M5 complete Worlds
M6 integrated visual review
backend/API/DB/Alembic/AuthZ/provider/LLM/tools/effects
```

## Closure rule

This subblock is closed only after:

```text
implementation
focused tests
typecheck/lint/architecture/unit/build
full Frontend CI including Chromium/Firefox/Mobile
exact validated HEAD + CI recorded
live docs synchronized
```
