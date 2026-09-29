# B12 — Replanning / Conflict / Solver — prepared block scope

- **Status:** PRE-SCOPE PREPARED; B12-A approval and implementation pending
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Preparation basis:** `c46ba83ddd05c6f07e81a12ce3424a22bd68cc4b`
- **Entering frontier:** B13 closed on qualified user-reported acceptance; Alembic `20260929_92`
- **B13 verification debt:** final post-repair seven-file web rerun not reported; do not claim PASS
- **CI:** not authorized; the user runs local tests and real-app gates

This is the B12 block plan, not approval to implement its A/B/C/D gates. Each gate must be scoped and approved before implementation. Complete each gate vertically, including its real product path and focused local proof, before moving to the next.

## 1. Authority and repository inventory

Read current branch, roadmap, map, handoff, North Star, Product `v1-scheduling-flexibility.md`, Domain `schedule.md` and `schedule-part-2.md`, `temporal-constraint.md`, `availability-capacity.md`, `plan.md`, `dependency.md`, `proposal.md`, the Whole Logical Model and relevant Time/Reality and Resource/Capacity slices, accepted Physical PM-12 and the solver boundary architecture before implementation decisions. The candidate DB overlay and Dictionary `current_materialization` remain the persistence source for this branch.

At entry, B04-D already accepts a supplied absolute Schedule move: blocked automation rejects; direct movement checks current placement, Movement Policy and hard Temporal Constraints; confirmation-required movement creates a pending proposal and revalidates at acceptance. **B04-D does not search for candidates.** B13 provides flat Plan/Step structure, qualified Dependency evaluation and read-only execution-slice assessment. Selected Physical solver target is OR-Tools 9.15 CP-SAT; direct solver validation has not been reported, and solver output is not canonical. No new B12 schema or solver behavior is proven at this checkpoint.

## 2. Permanent boundaries

```text
canonical accepted Schedule != proposed placement
Schedule != Session != Actual
Plan/Step ordering != Dependency
Dependency satisfaction != automatic Schedule
Temporal Constraint != Movement Policy
availability/capacity != simple timestamp overlap
unknown input/status != infeasible
no known conflict != proof of global feasibility
solver candidate != Proposal act != Decision/accepted effect
AI explanation/ranking != scheduling authority
```

Hard constraints are not silently relaxed. Soft preferences remain soft. An accepted Schedule is retained even if later truth reveals a conflict. A changed Actual/Outcome/Dependency/Plan/constraint/policy/Schedule basis must not silently authorize an old candidate. Start with the smallest useful replan scope; widen only explicitly when necessary. Self ownership, privacy and authorization remain enforced on every read and effect.

## 3. Vertical gate sequence

### B12-A — Current-truth conflict diagnosis and replan basis

One self-owned Plan and its linked Activities are inspected through a bounded, explicit, read-only application path. Report supported hard Temporal Constraint violations against a current accepted absolute placement and the current qualified Dependency status as distinct diagnostics. Preserve unknown/missing/unsupported inputs honestly. Expose the result in the real Home product flow with no identifiers or DevTools. Do not generate candidate placements or mutate Schedule. See `timeline-temporal-operational-b12-a-scope-2026-09-29.md`.

### B12-B — Bounded candidate generation / solver

After A is proven, define an exact B12-B scope for a small, bounded absolute-time replanning horizon. Use the selected deterministic OR-Tools CP-SAT target when a constraint solver is warranted, with direct corpus/status tests. Preserve `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, `MODEL_INVALID` and `UNKNOWN` distinctly; timeouts and incomplete inputs cannot masquerade as infeasibility. Candidate/scenario output carries material basis, scope and model/version; it performs no accepted Schedule write. The B12-B gate must decide supported candidate variables and availability evidence from live repository capabilities before implementation.

### B12-C — Review and governed admission

Scope candidate review, explicit user choice and freshness revalidation against current Schedule, Movement Policy, hard constraints, Plan and Dependency basis. Reuse the B04-D single Schedule move request/acceptance path where its semantics match. Do not promote a solver result into a generic Proposal root, automatically commit a multi-Schedule batch through repeated single-item calls, or claim atomic group effects without a separately designed and proven transaction. A true multi-item acceptance contract, if necessary, must be explicitly designed in this gate before DDL. Provide a real product review path and idempotent conflict handling.

### B12-D — Whole-block integration and acceptance

Prove one real end-to-end conflict → bounded candidate → review → governed effect chain, negative cases for hard/unknown/stale/blocked/changed Dependency, ownership and non-effects, reload/current-state truth, and user-run real-app acceptance. Reconcile roadmap/map/handoff and any Dictionary/catalog changes; only then close parent B12.

## 4. Deliberate limits

No universal work-item/Proposal/solver-result Domain root. No arbitrary cross-account or provider calendar authority, no inference of resource conflicts solely from overlap, no fake Activity/Occurrence/Session/Actual, no autonomous AI Schedule writes, no silent broad replan or hard-rule relaxation. B14 Create completeness and B07 UX consolidation remain later gates.

B12-A does not claim to solve all capacity, preference, resource, recurrence, multi-actor or multi-Schedule replanning cases. Unknown or unsupported is a truthful output. The later gate scopes must make those limits visible in the product.

## 5. Proof discipline and next gate

The user runs PostgreSQL/backend/web/typecheck/generated-client checks locally; no GitHub Actions or CI. Changed migrations, if any, are forward-only and must reconcile the Dictionary, ORM and live catalog. Each gate records exact observed results and distinguishes focused proof from user-reported product acceptance.

**Next:** approve the exact B12-A semantic scope in its companion document. Its implementation has not begun.
