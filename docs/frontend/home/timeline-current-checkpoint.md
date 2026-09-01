# DANTE — Timeline Current Checkpoint

**Status:** CURRENT LIVE TIMELINE CHECKPOINT — T1 FROZEN / NEXT TEMPORAL WORK NOT ACTIVE  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`

This is the live entry point for a new chat working specifically on Timeline / temporal UX.

## Current state

```text
Temporal architecture          accepted working authority
Temporal roadmap               active planning authority
T0 scenario/product grammar    established
T1 Timeline parity/hardening   USER ACCEPTED / FROZEN
T2+                            NOT STARTED unless explicitly resumed
```

T1 observable behavior is protected by `timeline-t1-frozen-contract.md` and its Chromium + Firefox regression coverage.

Do not infer that T2 is active merely because it is next in the roadmap. The currently active frontend product workstream is World Focus.

## T1 durable behavior

Frozen areas include:

- first-gesture custom drag;
- deselect-first focus grammar;
- title/time/subitem explicit action regions;
- no native drag ghost/text selection;
- same-day/cross-day move semantics already covered by accepted behavior;
- anchored time edit separate from drag;
- deterministic compact overlap lanes;
- expanded group/header geometry and horizontal sync;
- listener/overlay cleanup on cancellation;
- Chromium + Firefox protection of critical pointer/focus/drag behavior.

Any deliberate observable change requires explicit user approval before production writes.

## Temporal architecture direction

The accepted temporal product is not a generic calendar. Home Timeline and the future full-page temporal workspace are separate projections over one temporal application capability.

Permanent examples:

```text
Schedule != Session != Actual
Occurrence != recurrence source
planned != actual
Proposal != accepted Decision/effect
provider acknowledgement != canonical completion
```

Shared semantics/application boundaries are preferred; a single mega-renderer is rejected.

## Read order

1. `docs/frontend/home/timeline-current-checkpoint.md`
2. `docs/frontend/home/timeline-handoff.md`
3. `docs/frontend/home/timeline-t1-frozen-contract.md`
4. `docs/frontend/home/temporal-experience-architecture.md`
5. `docs/frontend/home/temporal-frontend-roadmap.md`
6. relevant current code/tests under `apps/web/src/features/home/ui/timeline/` and `apps/web/e2e/timeline-interactions.spec.ts`

## Resume gate

When Timeline work is explicitly resumed, continue from the roadmap after T1. Before any T2 production write, re-read current Domain/Logical/Physical/DB and Intelligence/effect authorities touched by the capability; do not rely on this checkpoint alone for semantic details.

## Operational rules

- do not weaken T1 tests to make unrelated work pass;
- do not redesign accepted Timeline visuals as cleanup;
- do not build a second independent temporal store for a future full-page workspace;
- no backend/API/DB/provider work without a separate authorized vertical;
- the user remains the final functional/visual gate for each future temporal mini-vertical.
