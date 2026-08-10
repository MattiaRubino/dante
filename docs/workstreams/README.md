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

- [`today-home.md`](today-home.md) — Phase 4 Home/Today UX prototype, in progress
- [`backend-foundation.md`](backend-foundation.md) — backend technical foundation, ready to start
- [`domain-model.md`](domain-model.md) — core domain model v0, ready to start

## Operational rule

The handoff is the workstream's live save game. Update it after meaningful progress on that branch.

Do not use `docs/PROJECT-STATUS.md` as a per-iteration log. Update global status only when the workstream starts, finishes, becomes blocked, changes branch/PR, reaches an integrated milestone or otherwise changes the global project state.

Before continuing a workstream:

1. read [`../development/operating-rules.md`](../development/operating-rules.md);
2. verify the named branch/PR still exists and compare it with current `main`;
3. use current `main` as the accepted baseline and the branch handoff as authority only for unmerged work inside that workstream;
4. read any branch-local master log named by the handoff before editing.

If the work materially changes durable product/architecture truth, update the appropriate durable document/ADR in the same PR rather than leaving that decision only in this handoff.
