# B12-A — Current-truth conflict diagnosis and replan basis — scope proposal

- **Status:** APPROVED 2026-09-29; implementation candidate published, local proof and real-app acceptance pending
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Preparation basis:** `c46ba83ddd05c6f07e81a12ce3424a22bd68cc4b`
- **Entering DB source head:** `20260929_92`; Dictionary current materialization `196|5|152|100|397|344|497|0|0|0`
- **Runner:** user worktree `~/projects/dante`; no CI/GitHub Actions
- **Parent:** `timeline-temporal-operational-b12-scope-2026-09-29.md`

## 1. Purpose and supported case

B12-A completes the first vertical slice of B12: from an explicit Home Plan action, show a truthful current-truth diagnosis for one self-owned Plan with linked Activities. The diagnosis explains *which supported condition currently blocks or conflicts with a placement* and what material basis was read. It does not choose a new time.

The initial supported case is a bounded flat Plan containing one or more linked Activities, optionally with current accepted absolute Schedule placement, supported hard Activity Temporal Constraints, and active Plan-qualified Dependencies. It may inspect the accepted current placement of a linked Activity and evaluate the applicable hard rules at that placement using existing canonical evaluators. Each Dependency evaluation is reported separately with its qualifier/current evidence.

Do not infer that Step order creates a Dependency, that an unplaced Activity is a conflict, or that `no known conflict` proves all real-world availability is clear. A currently unsatisfied Dependency is a *blocked prerequisite*; an unknown prerequisite remains *unknown*. A hard temporal rule violated by an accepted placement is a *known violation*; it does not retroactively delete or rewrite that Schedule.

## 2. Exact output contract

For each inspected linked Step, the read-only result exposes:

- Plan/Step/Activity names or labels suited to the product, with structured references only in the API;
- supported current placement form and exact accepted placement MaterialState basis where available;
- individual supported Temporal Constraint evaluations and hard-set result, without weakening rules;
- each applicable active Dependency direction, qualifier and current `satisfied / unsatisfied / unknown` result, preserving source state provenance where available;
- a bounded set of diagnostics with typed reasons, including `known_hard_violation`, `blocked_prerequisite`, `unknown_basis`, `unsupported_placement`, and `no_known_conflict_in_supported_rules` as applicable;
- the exact Plan state and other material read bases needed for a subsequent B12-B candidate to detect staleness.

The terms above are application response categories, not new universal Domain states. A mixed result can contain a known violation and an unknown prerequisite; do not collapse it into one misleading boolean. An empty diagnostic is not an assertion of global feasibility.

## 3. Data and application boundary

Use authenticated self-scoped reads of the existing accepted Plan and active Dependencies, the existing current Schedule/placement path for linked Activities, and B04 Temporal Constraint evaluation. Re-read current truth on each explicit diagnosis request; do not trust browser-cached, projection-latest or unsigned caller-supplied state as authority. Bound Plan size, interval/horizon and query cost by a documented request limit chosen from repository evidence before implementation. Avoid N+1 unbounded reads.

The implementation inventory must first establish the exact safe read path for current Schedule placements and the currently supported absolute form. If a guarded PostgreSQL read function is required, add only a forward migration and full Dictionary/catalog/ACL proof. No new canonical conflict or solver table is approved for B12-A. If a safe basis cannot be read without widening semantics, stop and revise this gate before writing DDL.

A diagnosis must not create, revise, unschedule, accept or retire a Schedule, Plan, Dependency, Actual, Outcome, Temporal Constraint or Movement Policy. It must not materialize a Proposal/solver result, infer capacity blocking from timestamp overlap, or silently assume missing Availability/Capacity data is free time.

## 4. Public and product path

Provide a typed authenticated HTTP response, deterministic OpenAPI/generated client and a contextual control in the Home Plan flow such as **Analizza conflitti**. The user selects the Plan already visible in **Plan e Step**, clicks once and sees Step-level reasons in ordinary language, including explicit `sconosciuto/non valutabile` where material input is missing. No DevTools, UUID copy/paste or manual technical reference is part of the product path.

Preserve accepted states and values on refresh; reevaluation after a canonical state correction reflects the new current truth. If the current product surface cannot display a material basis safely, display a concise reason rather than a raw internal identifier.

## 5. Local acceptance criteria

1. A self-owned Plan with two linked Activities is diagnosed through the real guarded backend/API and Home control.
2. Supported hard Temporal Constraint violation at a current absolute placement is reported without Schedule mutation; a compliant placement is not mislabeled globally feasible.
3. An active Record → Mix Dependency is displayed directionally; absent prerequisite Actual stays unknown, accepted non-occurrence blocks the dependent Step, later correction to occurred updates the diagnosis.
4. Reordering Steps does not change Dependency direction. An unplaced/unsupported placement and incomplete Availability/Capacity data remain explicit unknown/unsupported, never an invented conflict or free slot.
5. Repeated read returns stable material bases without new write rows; changing current Plan/Dependency/Schedule/Actual/constraint state changes or invalidates the displayed basis on the next request.
6. Another self Person cannot inspect the Plan or private related truth; limits and invalid input produce bounded errors.
7. Focused PostgreSQL/API, OpenAPI/generated-client, web/component and typecheck gates pass on the user's local worktree, with Dictionary/catalog checks if a new guarded DB read is added. A real-app walkthrough confirms the control and its wording.

The exact test filenames and any required read function are selected only after inspecting owning modules and tests at implementation start. B12-A closes only after the complete slice, local proof and user-reported product result; do not split it into superficial subgates.

## 6. Explicit non-goals and handoff

No candidate search, OR-Tools invocation, optimization, objective weights, Proposal acceptance, direct or automatic Schedule movement, broad day/week replanning, new capacity claims, generic overlap-conflict inference, provider/calendar orchestration, AI scheduling authority or multi-actor governance. B12-B owns bounded candidates; B12-C owns review/governed effect; B12-D owns whole-block integration.

**Approval received:** B12-A on 2026-09-29. Implementation and user-run local tests follow this bounded scope. An unexpected need for a new semantic owner, unsupported data authority or multi-item effect requires a revised gate, not an implicit scope expansion.
