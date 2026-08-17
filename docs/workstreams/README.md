# Workstream Handoffs

Each active workstream has one operational handoff file. This is the fastest and safest entry point for another chat, AI model or developer continuing that work.

A workstream handoff must contain, where applicable:

- status;
- active/intended branch and PR;
- purpose and current scope;
- last known completed work;
- current task;
- exact next steps;
- important linked architecture/product/ADR documents;
- files/areas involved;
- decisions that must not be casually changed;
- known issues/open questions;
- validation/tests;
- last validated commit when implementation exists.

## Current workstreams

- [`pre-physical-coherence.md`](pre-physical-coherence.md) — **active backend/architecture preparation workstream**; aligns repository current truth, supersession, pre-Physical requirements and benchmark inputs before any Physical Model authorization.
- [`today-home.md`](today-home.md) — active Phase 4 Home/Today UX/product-structure workstream.

## Deferred / not currently executable workstreams

- [`backend-foundation.md`](backend-foundation.md) — **NOT STARTED / DEFERRED** until Pre-Physical Coherence closes and later Physical/runtime prerequisites are explicitly accepted. Its existing pre-Domain/Logical assumptions are scheduled for bounded cleanup; do not execute old Domain/persistence instructions as current truth.

## Completed model workstreams

- [`domain-model.md`](domain-model.md) and its canonical continuation parts — historical operational record for the **CLOSED** Core Domain Model / Domain Atlas integrated into `main` via PR #10. Do not treat the older "ready to start" state as current.
- Logical Model workstream documents and continuations — historical operational record for the **CLOSED** Logical Model integrated into `main` via PR #11.

Completed/historical handoffs remain useful evidence, but `main` is authoritative for their integrated accepted state.

## Operational rule

The active handoff is the workstream's live save game. Update it after meaningful progress on that branch.

Do not use `docs/PROJECT-STATUS.md` as a per-iteration log. Update global status only when a workstream starts, finishes, becomes blocked, changes branch/PR, reaches an integrated milestone or otherwise changes global project truth.

Before continuing a workstream:

1. read [`../development/agent-operating-manual.md`](../development/agent-operating-manual.md);
2. read [`../development/operating-rules.md`](../development/operating-rules.md);
3. verify the named branch/PR still exists and compare it with current `main`;
4. use current `main` as the accepted integrated baseline and the branch handoff as authority only for unmerged work inside that workstream;
5. read the complete canonical workstream document, including required continuation/split parts;
6. read linked accepted model/architecture sources before proposing edits.

If the work materially changes durable product/architecture truth, update the appropriate durable document/ADR/current baseline in the same PR rather than leaving that decision only in the handoff.

A stale historical handoff never overrides a later accepted Domain/Logical closure or current project status merely because it contains detailed instructions.