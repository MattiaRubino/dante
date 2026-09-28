# Timeline / Temporal-Operational — B13-B Qualified Dependencies gate

- **Status:** APPROVED — semantic scope frozen; implementation pending
- **Date:** 2026-09-28
- **Branch:** `feature/timeline-temporal-operational`
- **Pre-scope HEAD:** `4a0a95c94a746173af6d965dfc791339111560c0`
- **Previous gate:** B13-A CLOSED / focused local proof at Alembic `20260928_89`
- **Parent:** B13 Work Structure / Decomposition / Dependencies
- **CI:** not authorized; user runs local gates

## 1. Purpose and first supported context

B13-B establishes a *qualified* Dependency inside one self-owned Plan. A user can say that proceeding with the real Activity linked to one Step is contingent on a specified current Actual or Outcome of the real Activity linked to another Step. The two Steps locate the relation in Plan structure; the actual prerequisite and dependent subjects retain their Activity identities.

This gate supports only two current Steps in the same Plan, each linked to a distinct existing Activity owned by the same self Person. Unlinked Steps have no canonical realization/result state to evaluate and cannot be endpoints in this first vertical. Plan ordering or adjacency never creates a Dependency.

## 2. Exact semantic contract

Each authored relation preserves:

1. prerequisite Step and its linked Activity;
2. dependent Step and its linked Activity;
3. purpose: admissibility of proceeding with the dependent Activity *in this Plan*;
4. one explicit, typed prerequisite condition:
   - **Actual occurred:** the prerequisite Activity has a current established Actual with `realization_occurred=true`; or
   - **Outcome disposition equals code:** the prerequisite Activity has a current established Outcome tied to its current Actual material state, with the exact authored `disposition_code`;
5. stable Plan-scoped relation reference, accepted material revision, current binding, operation provenance, and reconstructible history;
6. active/retired applicability without deleting consequential past assertions.

An Actual that occurred is not automatically a completed or successful Activity. An Outcome code is compared exactly and is not a universal success enum. These qualifiers must be visible in authoring and reads; an unlabeled arrow between Steps is insufficient.

Per relation, the current evaluation is **satisfied**, **unsatisfied**, or **unknown**. An established `realization_occurred=false` makes the Actual-occurred qualifier unsatisfied; absence of established Actual is unknown. A current, applicable Outcome with another code makes the exact-code qualifier unsatisfied; absence of an applicable current Outcome, including an Outcome tied to an obsolete Actual material state, is unknown. A retired relation is not evaluated as currently applicable. Corrections to Actual/Outcome cause reevaluation without mutating Dependency history.

Multiple direct relations may be stored and read separately. This gate does not define an all/any/quorum aggregation or a universal `blocked` flag for the dependent Activity.

## 3. Ownership, mutation and history

- Both Step refs must belong to the same current Plan structure, with the same self Person's linked Activities. Cross-Plan, foreign-owner, missing and stale endpoint references are rejected.
- An active relation retains the Activity refs to which its Step refs were bound. Reordering Steps or changing their titles leaves the relation intact. A Plan revision that removes one of those Steps or relinks its Activity is rejected while the relation is active; retire or explicitly replace the Dependency first. There is no silent retargeting or deletion.
- Create, revise and retire use replay-safe operation IDs and expected-current revision checks. Materially changed qualifiers produce a new accepted relation state; older state/history remains queryable. A dependency edit does not automatically replace the Plan identity or Plan work-state snapshot.
- Exact duplicate active assertions for the same bounded pair, purpose and condition are rejected. Reversing endpoints is a different claim. Cycles are allowed and surfaced as a bounded diagnostic; they are not silently removed or treated as proof of feasibility. No transitive relation is persisted by inference.
- Guarded PostgreSQL operations enforce self scope and invariants. Runtime has no direct table DML. The implementation follows the forward-only migration, Dictionary, mapping and exact-catalog discipline.

## 4. Public and product path

Expose Plan-scoped author, list/read, revise and retire operations via backend HTTP/OpenAPI and a deterministic generated client. The Home Plan/Step panel lets the user choose prerequisite and dependent Steps, choose one of the two typed conditions, enter an Outcome code when needed, and see each relation's condition, current evaluation and cycle warning. A relation edit does not move a Schedule or execute an Activity.

## 5. Explicit non-goals

```text
generic WorkflowNode / WorkItem / universal Relation or graph table
universal DAG restriction, topological scheduler or transitive closure
cross-Plan, shared multi-Actor or unlinked-Step dependency authoring
arbitrary boolean expressions, all/any/quorum/fallback conditions
lag, lead, spacing or pure before/after Temporal Constraints
automatic Schedule/Session/Actual/Outcome mutation or Trigger
solver/replanning and feasibility guarantees (B12)
maximum Session, merge, preparation/recovery constraints (B13-C)
whole B13 real-app acceptance (B13-D)
```

## 6. Required implementation discovery before DDL

Inspect the current `_89` Plan structure functions, Actual/Outcome current-binding APIs and guarded PostgreSQL patterns. Decide and document: the smallest LR-03 Plan-scoped relation representation; how its stable scoped ref differs from native Domain identity; how exact current Actual/Outcome states are qualified; accepted-current/history and retirement shape; locking of Plan replacement versus relation authoring; bounded cycle diagnostics; and deterministic API/client/UI names. No physical shortcut may broaden the semantic gate.

## 7. Acceptance gate

1. Self-owned Plan author/read/revise/retire is usable through one guarded canonical path and the product panel.
2. Both typed qualifiers evaluate satisfied, unsatisfied and unknown from *current accepted* Actual/Outcome truth, including correction and stale Outcome basis.
3. A relation has stable scoped address, explicit direction, purpose and qualifier. Revision/replay/CAS/retirement preserves history and currentness.
4. Cross-Plan, foreign owner, unlinked/missing Step, stale link, duplicate assertion and invalid intent cases fail deterministically.
5. Reorder/title edit does not retarget a relation; removal/relink is guarded while active. Cycles remain representable and visible; no inferred transitive Dependency is stored.
6. Dependency operations do not mutate Plan structure, Activity, Schedule, Session, Actual or Outcome. Actual/Outcome correction only changes derived evaluation.
7. Forward-only Alembic, Dictionary, SQLAlchemy mapping inventory, ACLs and exact live catalog reconcile with PostgreSQL.
8. OpenAPI inventory/contract, generated client and its determinism check, web tests and typechecks pass.
9. The user runs focused local PostgreSQL and web gates; no CI/Actions. Roadmap, map, handoff and database overlay record the measured evidence before B13-B closes.

The integrated real-app A/B/C walkthrough remains B13-D. B13-B can close on this focused automated vertical proof.

## 8. Next boundary

After B13-B closes, B13-C owns execution-structure constraints. B12 remains held until B13-D closes. Approval of this gate authorizes only the bounded B13-B work described here; any material semantic expansion requires a new gate.
