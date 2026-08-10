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

## Rule

At the end of meaningful work, update the relevant handoff before considering the task complete. If the work materially changes global project state, update [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md) too.
