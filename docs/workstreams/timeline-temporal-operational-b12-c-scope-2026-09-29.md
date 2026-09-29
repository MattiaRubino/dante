# B12-C — review and governed admission — scope proposal

- **Status:** APPROVED 2026-09-29; implementation checkpoint pending focused local proof
- **Date:** 2026-09-29
- **Entry:** B12-A and B12-B closed / proven on focused user-run gates; DB head `20260929_92`
- **Parent:** `timeline-temporal-operational-b12-scope-2026-09-29.md`
- **Acceptance cadence:** focused user-run automated proof at B12-C; integrated real-app walkthrough once at B12-D before parent closure

## 1. One reviewed effect

Let the authenticated self Person inspect a B12-B result for one selected Plan Step, explicitly choose one of its at most three absolute-time candidates in Home, review the old/new interval and the limitations, and submit **one** move request for its linked Activity's sole current Schedule. No copied references, DevTools, generic Plan-wide apply, batch of Schedule moves, inferred dependency from Step order, altered duration, automatic submission or unreviewed AI action.

The product must distinguish a committed direct move from a B04-D `confirmation_required` pending Schedule move proposal and provide a usable confirmation action for the latter. A pending proposal is not a Schedule change. Show the current Schedule after a committed/accepted effect; show a typed stale/blocked result and refresh the review when evidence changed. Do not claim availability or capacity was evaluated.

## 2. Freshness and authority

The submit command carries selected Plan/Step and the exact reviewed basis: Plan state, sole Schedule placement MaterialState, relevant Temporal Constraint states, qualified Dependency states and Actual/Outcome evidence, Movement Policy state, selected interval, model version and horizon. Server-side it authenticates/self-scopes all of them, reconstructs B12-B's eligible candidate set, verifies the selected interval belongs to it, and rejects unsupported, unknown, blocked, `UNKNOWN`/`MODEL_INVALID`/`INFEASIBLE` input or changed material evidence. UI-derived solver results are never trusted as authority.

Revalidate current Plan/Dependency, Schedule, constraints and Movement Policy at the effect boundary. B04-D's guarded single-Schedule request already owns direct vs confirmation-required movement, current placement/policy/hard-rule enforcement and idempotent operation receipts. Inspect its PostgreSQL transaction/locking semantics and the Plan/Dependency mutation paths before choosing the B12-C orchestration: the check and B04-D request must have a proven race-safe relationship. If existing locks or transaction isolation cannot provide it, design a narrow forward-only guard/change and focused concurrent correction tests within B12-C rather than treating a preflight read as atomic. On proposal acceptance, revalidate the Plan/Dependency review basis again as well as B04-D's proposal/placement/policy/constraint checks; changed evidence requires explicit fresh review, never silent acceptance.

Movement Policy `blocked` or missing has no B12-C effect path. The `direct` path may commit only after the explicit review action. The `confirmation_required` path creates one B04-D pending move proposal and needs a separate explicit confirmation action to accept it. All operations must be self-scoped, idempotent under replay and reject reuse of an operation id with materially different intent. No new generic Proposal root/table; any DDL must preserve Dictionary/catalog and migration rules.

## 3. Product/API proof

Add typed authenticated submit and confirmation contracts plus a Home review flow using the existing Plan/Step context. Show old/new local date/time, fixed duration, relevant soft-rule findings and uncertainty about capacity. After a successful effect, refetch accepted truth; a pending proposal remains visibly pending until confirmed. Distinguish user-visible stale, unsupported, blocked policy, hard violation, unknown prerequisite, and already-applied/replayed cases without turning a retry into a second move.

Focused local tests must cover direct commit; pending proposal then confirmation; no Schedule effect before confirmation; changed Plan, Dependency, Actual/Outcome, Schedule, hard/soft Constraint and Movement Policy between search, review, submit and acceptance; another self Person; retries and operation-id collisions; concurrent correction against admission; no capacity claim; generated client, web component, typechecks, Ruff and current PostgreSQL catalog. Preserve `20260929_92` if no migration is needed, otherwise migrate forward and reconcile catalog. No CI/GitHub Actions.

**Approved boundary:** single reviewed Schedule move and guarded B04-D admission. Multi-item batch effects, automatic broad replanning and parent B12 closure remain outside this gate.
