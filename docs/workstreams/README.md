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

- [`today-home.md`](today-home.md) — active Phase 4 Home/Today UX/product-structure workstream.

## Completed / integrated workstreams

- [`physical-model.md`](physical-model.md) — **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED / integrated into `main` via PR #15**, with Physical integration commit `e6f191bad947388a44defe2c15f4939345084f58`. Former branch `feature/physical-model` was merged and auto-deleted. Direct selected-stack implementation validation remains **NOT STARTED / DIRECT HG PASS 0**; the next separate operational scope is **Development Profile v0**.
- [`pre-physical-coherence.md`](pre-physical-coherence.md) — **DEFINITIVE CLOSED / FINAL QA PASS / integrated into `main` via PR #13 / POST-MERGE VERIFIED**, with post-merge current-truth alignment through PR #14. Former branch `chore/pre-physical-coherence` was merged and auto-deleted.
- [`domain-model.md`](domain-model.md) and its canonical continuation parts — historical operational record for the **CLOSED** Core Domain Model / Domain Atlas integrated into `main` via PR #10. Do not treat older readiness/in-progress prose as current closure state.
- Logical Model workstream documents and continuations — historical operational record for the **CLOSED** Logical Model integrated into `main` via PR #11.

## Deferred / not currently executable workstreams

- [`backend-foundation.md`](backend-foundation.md) — **NOT STARTED / DEFERRED**. The accepted Physical Model is now integrated, but Backend still requires its own explicit authorization and must consume the Development Profile/current security/runtime/integration/API prerequisites applicable to the chosen first slice. Do not create `feature/backend-foundation` or execute production backend/schema/API instructions without that separate gate.

Completed/historical handoffs remain useful evidence, but current model/architecture authority and current `main` determine accepted execution truth.

## Physical carry-forward rule

The Physical target is closed and integrated. Current implementation must consume `docs/physical-model/**`, especially PM-11/12 and the post-selection validation register.

```text
PHYSICAL TARGET CLOSED / SELECTED / ACCEPTED
INTEGRATED INTO MAIN VIA PR #15
DIRECT HG PASS 0
DIRECT IMPLEMENTATION VALIDATION NOT STARTED
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
NOT RUN != PASS
NEXT Development Profile v0
```

Version-sensitive selected-component claims still require current official primary-source verification where material. Any direct validation, implementation or Physical reopen requires a fresh exact branch/PRE-SCOPE/write gate.

## Operational rule

The active handoff is the workstream's live save game. Update it after meaningful progress on that branch.

Do not use `docs/PROJECT-STATUS.md` as a per-iteration log. Update global status only when a workstream starts, finishes, becomes blocked, changes branch/PR, reaches an integrated milestone or otherwise changes global project truth.

Before continuing a workstream:

1. read [`../development/agent-operating-manual.md`](../development/agent-operating-manual.md);
2. read [`../development/operating-rules.md`](../development/operating-rules.md);
3. read [`../development/repository-engineering-safety.md`](../development/repository-engineering-safety.md);
4. verify the named branch/PR still exists and compare it with current `main`;
5. use current `main` as the accepted integrated baseline and an active branch handoff as authority only for unmerged work inside that workstream;
6. read the complete canonical workstream document, including required continuation/split parts;
7. read linked accepted model/architecture sources before proposing edits;
8. for work consuming the Physical target, read current PM-11/12/13, the PSV register and relevant Phase-5..10 authority before proposing implementation choices.

If the work materially changes durable product/architecture truth, update the appropriate durable document/ADR/current baseline in the same PR rather than leaving that decision only in the handoff.

A stale historical handoff never overrides a later accepted Domain/Logical/Pre-Physical/Physical closure or current project status merely because it contains detailed instructions.
