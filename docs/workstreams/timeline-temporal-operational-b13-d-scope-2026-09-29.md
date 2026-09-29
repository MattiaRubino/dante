# B13-D — Whole-block Integration / Proof / Acceptance scope

- **Status:** APPROVED — B13-D integration candidate scope
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Pre-scope HEAD:** `4eac3e971d50cb3c0f04d2699e35275a2dacbe9b`
- **Entering frontier:** B13-A/B/C CLOSED / focused local automated proof; Alembic `20260929_92`
- **CI:** not authorized; the user runs local PostgreSQL and real-app gates

## Purpose

Prove the existing B13 work structure, qualified Dependency and Plan-contextual execution policy together on one self-owned Plan and in the Home product surface. B13-D is the whole-block integration and acceptance gate. It does not add a fourth canonical work concept or infer accepted scheduling from a proposal.

## One canonical chain

1. Create two distinct self-owned Activities, a Plan and two ordered internal Steps, each linked to one Activity. Configure a hard proposed-slice limit and merge permission on the dependent Step. Read back the same accepted Plan revision and policy.
2. Create a directional `actual_occurred` Dependency from the prerequisite Step to the dependent Step. With no Actual it is `unknown`. Reordering titles/positions and revising the dependent Step policy produces a new Plan revision without changing Dependency direction or the Activity endpoints. Removing or relinking an active endpoint is rejected; a stale Plan revision also fails.
3. Assess explicit proposed slices against the current Plan state. A hard count violation is diagnostic. A requested pair has a compatibility result grounded in permission, contiguity and applicable Activity Temporal Constraints. The assessment does not create accepted Schedules or performed Sessions. A stale assessment basis fails.
4. Record and, where appropriate, correct the prerequisite Activity's Actual or Outcome. Dependency evaluation follows current accepted truth, including `unknown` when evidence is missing/stale. That evaluation neither alters the dependent Step policy nor admits a proposed Schedule. Re-read after a fresh application session and verify stable identities and current state.
5. Retire the policy and Dependency explicitly; historical revisions and receipts stay queryable. Confirm another self Person cannot read or mutate the Plan or relation.

The integrated test should check the intersection of A/B/C, not repeat every isolated proof already covered by their focused suites. Use a real migrated PostgreSQL database and guarded application/API paths. A user-facing component test should cover the Plan panel's shared accepted state, Dependency and execution controls, including reload and revised-state assessment. The PostgreSQL test covers stale-state rejection.

## Real-app walkthrough

After automated gates pass, the user runs the local app and reports a real Home walkthrough: create/link the two Activities and Steps; author the Dependency and execution policy; refresh; assess proposed slices; reorder the Steps; check Dependency direction/evaluation and policy persistence; try a forbidden active-endpoint removal; record or correct a prerequisite Actual through the existing product path and check the updated evaluation; retire the policy/relation and refresh. Record what was actually observed, including any unavailable product path. Do not claim acceptance from automated tests alone.

If a defect appears, repair it in its existing owner with focused regression and rerun the affected gates. A missing or unsupported capability is recorded explicitly; avoid new database columns, generated-client hand edits or an implicit solver.

## Local acceptance gate

- One new integrated PostgreSQL test of the chain above, followed by B13-A/B/C regression files and both exact Dictionary/catalog tests at `_92`.
- Existing B13-A/B OpenAPI contract tests plus the B13-C assessment contract; deterministic generated-client check and API-client typecheck.
- Focused Plan work, Dependency, execution and remote-source web tests plus a whole-panel integration test and web typecheck.
- Ruff for changed Python, repository format checks where applicable, and an explicit readback of changed files from the published branch.
- User-run real-app walkthrough and recorded findings. Only then mark B13-D and parent B13 closed and release B12.

No CI/GitHub Actions. Published migrations remain immutable and PostgreSQL stays canonical. B12 proposal generation/admission, B14 Create completeness and B07 UI consolidation remain separate.

## Git write gate for the integration candidate

```text
BRANCH
feature/timeline-temporal-operational
PRE-SCOPE
4eac3e971d50cb3c0f04d2699e35275a2dacbe9b
CREATE
apps/backend/tests/integration/temporal/test_b13_d_whole_block.py
apps/web/src/features/temporal/plan-whole-block.test.tsx
docs/workstreams/timeline-temporal-operational-b13-d-scope-2026-09-29.md
docs/workstreams/timeline-temporal-operational-b13-d-gate-2026-09-29.md
docs/workstreams/timeline-temporal-operational-b13-d-implementation-2026-09-29.md
UPDATE
apps/backend/tests/test_b13_a_openapi_contract.py
docs/workstreams/timeline-temporal-operational-roadmap.md
docs/workstreams/timeline-temporal-operational-map.md
docs/workstreams/timeline-temporal-operational-handoff.md
DELETE
none
PURPOSE
publish B13-D integrated PostgreSQL and Home proof candidate plus local acceptance gate
EXPLICITLY OUT OF SCOPE
schema/Dictionary changes, generated-client edits, B12/B14/B07 implementation, B13 or B13-D closure
```

If local or user-run proof reveals a defect, repair it in the owning path and record the additional changed files and test evidence before claiming acceptance.
