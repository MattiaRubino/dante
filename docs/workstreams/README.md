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

- [`frontend-foundation.md`](frontend-foundation.md) — **ACTIVE on `feature/frontend-foundation`; Passo 1 technology selection DESIGN COMPLETE; Passo 2 architecture/structure DESIGN COMPLETE; Passo 3 whole-foundation review/closure NEXT; production frontend code and direct validation NOT STARTED**.
- [`today-home.md`](today-home.md) — active Phase 4 Home/Today UX/product-structure workstream.

## Completed / integrated workstreams

- [`engineering-foundation.md`](engineering-foundation.md) — **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated into `main` via PR #21**, establishing the current pre-implementation engineering baseline and deferring frontend-internal details to the dedicated frontend workstream.
- [`physical-model.md`](physical-model.md) — **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED / integrated into `main` via PR #15**. Direct selected-stack implementation validation remains carried forward and **NOT STARTED / DIRECT HG PASS 0**.
- [`pre-physical-coherence.md`](pre-physical-coherence.md) — **DEFINITIVE CLOSED / FINAL QA PASS / integrated into `main` via PR #13 / POST-MERGE VERIFIED**, with post-merge current-truth alignment through PR #14.
- [`domain-model.md`](domain-model.md) and its canonical continuation parts — historical operational record for the **CLOSED** Core Domain Model / Domain Atlas integrated into `main` via PR #10. Do not treat older readiness/in-progress prose as current closure state.
- Logical Model workstream documents and continuations — historical operational record for the **CLOSED** Logical Model integrated into `main` via PR #11.

## Historical / superseded planning handoffs

- [`backend-foundation.md`](backend-foundation.md) — historical pre-Engineering-Foundation deferred planning handoff. It is **not current implementation authority** and must not override the later closed [`engineering-foundation.md`](engineering-foundation.md) or current `main`.

Completed/historical handoffs remain useful evidence, but current model/architecture authority and current `main` determine accepted execution truth.

## Physical/Engineering carry-forward rule

Current implementation must consume the closed Physical/Engineering authorities and applicable validation registers.

```text
PHYSICAL TARGET CLOSED / SELECTED / ACCEPTED
ENGINEERING FOUNDATION v0 CLOSED / ACCEPTED
FRONTEND PASSO 1 DESIGN COMPLETE
FRONTEND PASSO 2 DESIGN COMPLETE
DIRECT HG PASS 0
FRONTEND DIRECT VALIDATION NOT STARTED
SELECTED != DEPLOYED
SELECTED != DIRECT PASS
NOT RUN != PASS
```

Version-sensitive selected-component claims still require current official primary-source verification where material. Any direct validation, implementation or architecture/model reopen requires a fresh exact branch/PRE-SCOPE/write gate.

## Operational rule

The active handoff is the workstream's live save game. Update it after meaningful progress on that branch.

Do not use `docs/PROJECT-STATUS.md` as a per-iteration log. Update global status only when a workstream starts, finishes, becomes blocked, changes branch/PR, reaches an integrated milestone or otherwise changes global project truth.

Before continuing a workstream:

1. read `../development/agent-operating-manual.md`;
2. read `../development/operating-rules.md`;
3. read `../development/repository-engineering-safety.md`;
4. verify the named branch/PR still exists and compare it with current `main`;
5. use current `main` as accepted integrated baseline and an active branch handoff as authority only for newer unmerged work;
6. read the complete canonical workstream document including required continuation parts;
7. read linked accepted model/architecture sources before proposing edits;
8. for Physical-consuming implementation, read the current accepted Physical/Engineering sources and applicable validation register.

If work materially changes durable product/architecture truth, update the appropriate durable document/ADR/current baseline in the same PR rather than leaving that decision only in the handoff.

A stale historical handoff never overrides later accepted Domain/Logical/Pre-Physical/Physical/Engineering or current active-branch truth merely because it contains detailed instructions.
