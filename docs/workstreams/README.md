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

- [`physical-model.md`](physical-model.md) — **AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP QA PASS / PM-01 READ-ONLY NEXT** on `feature/physical-model`, based on `main @ 3de84bb49f9cef30e88e9bde4961ed84335daa79`. Physical mapping/benchmark execution is not started and no technology is selected. The exact next step is PM-01 read-only candidate/version/edition/deployment/environment freeze.
- [`today-home.md`](today-home.md) — active Phase 4 Home/Today UX/product-structure workstream.

## Completed / integrated workstreams

- [`pre-physical-coherence.md`](pre-physical-coherence.md) — **DEFINITIVE CLOSED / FINAL QA PASS / integrated into `main` via PR #13 / POST-MERGE VERIFIED**, with post-merge current-truth alignment through PR #14. Former branch `chore/pre-physical-coherence` was merged and auto-deleted.
- [`domain-model.md`](domain-model.md) and its canonical continuation parts — historical operational record for the **CLOSED** Core Domain Model / Domain Atlas integrated into `main` via PR #10. Do not treat older readiness/in-progress prose as current closure state.
- Logical Model workstream documents and continuations — historical operational record for the **CLOSED** Logical Model integrated into `main` via PR #11.

## Deferred / not currently executable workstreams

- [`backend-foundation.md`](backend-foundation.md) — **NOT STARTED / DEFERRED**. Pre-Physical integration is satisfied, but Backend still requires a separately accepted Physical Model plus all applicable current security/runtime/integration/API prerequisites before implementation may start. Do not create `feature/backend-foundation` or execute backend/schema/API instructions yet.

Completed/historical handoffs remain useful evidence, but current model/architecture authority and current `main` determine accepted execution truth. The active Physical branch may contain newer bounded Physical-workstream state only inside its approved scope.

## Physical workstream rule

Physical execution must use `docs/physical-model/**` plus the Phase-10 benchmark specification/corpus/register.

```text
PM-00 QA PASS
PM-01 READ-ONLY FIRST
PREFERRED != SELECTED
NOT RUN != PASS
unexecuted tier != VERIFIED-RUN
semantic hard-gate failure cannot be offset by performance
```

Current/version-sensitive candidate claims require official primary-source verification and exact product + version + edition + deployment pinning. Selection requires the explicit PM-11 gate.

PM-01 does not authorize mapping/schema/harness/database writes. It produces the candidate/environment freeze and the next exact write gate.

## Operational rule

The active handoff is the workstream's live save game. Update it after meaningful progress on that branch.

Do not use `docs/PROJECT-STATUS.md` as a per-iteration log. Update global status only when a workstream starts, finishes, becomes blocked, changes branch/PR, reaches an integrated milestone or otherwise changes global project truth.

Before continuing a workstream:

1. read [`../development/agent-operating-manual.md`](../development/agent-operating-manual.md);
2. read [`../development/operating-rules.md`](../development/operating-rules.md);
3. read [`../development/repository-engineering-safety.md`](../development/repository-engineering-safety.md);
4. verify the named branch/PR still exists and compare it with current `main`;
5. use current `main` as the accepted integrated baseline and the branch handoff as authority only for unmerged work inside that workstream;
6. read the complete canonical workstream document, including required continuation/split parts;
7. read linked accepted model/architecture sources before proposing edits;
8. for Physical work, read all `docs/physical-model/**` documents and all three Phase-10 benchmark-method documents before proposing mapping/harness/selection changes.

If the work materially changes durable product/architecture truth, update the appropriate durable document/ADR/current baseline in the same PR rather than leaving that decision only in the handoff.

A stale historical handoff never overrides a later accepted Domain/Logical/Pre-Physical closure or current project status merely because it contains detailed instructions.