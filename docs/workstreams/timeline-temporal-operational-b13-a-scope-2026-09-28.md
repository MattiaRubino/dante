# Timeline / Temporal-Operational — B13-A Work Structure Core Scope Freeze

- **Status:** OPEN — CURRENT IMPLEMENTATION GATE
- **Date:** 2026-09-28
- **Branch:** `feature/timeline-temporal-operational`
- **Parent block:** B13 Work Structure / Decomposition / Dependencies
- **Previous functional frontier:** B11 ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-28
- **Persistence source frontier entering gate:** B11-C / Alembic `20260927_86`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **CI:** not authorized; user runs local tests

This document freezes the semantic and delivery boundary for B13-A before persistence or application implementation begins.

---

# 1. Purpose

B13-A introduces the minimum canonical work-structure foundation required before qualified dependencies and later replanning/solver work.

The gate must let DANTE represent a Plan and its internal decomposition without pretending that structural children are Activities, dependencies, Schedules or solver proposals.

B13-A closes only when the repository can author, persist and read this structure through one coherent canonical path with explicit invariants and history/current-state behavior consistent with the rest of the Timeline / Temporal-Operational model.

---

# 2. Read order / authority

Implementation decisions must be checked against the current repository HEAD and, at minimum:

```text
docs/product/product-identity-and-north-star.md
docs/domain/README.md
docs/domain/concepts/plan.md
docs/domain/concepts/step.md            when present/applicable
docs/domain/concepts/dependency.md
docs/logical-model/whole-logical-model-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/database/timeline-temporal-operational.md
docs/workstreams/timeline-temporal-operational-roadmap.md
```

Existing accepted identity/material-state/current-history patterns are implementation evidence, not permission to collapse semantic concepts.

---

# 3. Semantic freeze

Permanent B13-A boundaries:

```text
Plan != Activity
Step != Activity
Dependency != hierarchy
ordering != dependency
decomposition != execution precedence
structure membership != Schedule
structure membership != Session
proposal != accepted effect
current accepted state != latest row
```

## 3.1 Plan

`Plan` is a canonical semantic identity. It is not an Activity wrapper and does not inherit Activity lifecycle merely because work inside a Plan can ultimately be executed by Activities.

A Plan may own work structure. B13-A must not model that ownership by creating a fake Activity for the Plan.

## 3.2 Internal Step / structural child

B13-A treats Step as internal work-structure semantics unless stronger current repository authority proves that Step must be promoted to a universal root semantic identity.

Therefore:

```text
structural Step != Activity
structural Step != Dependency
structural Step != Schedule
```

Do not introduce a generic universal `work_item`, `node` or `edge` ontology to avoid making the semantic decision.

## 3.3 Linking real Activities

A structural child may link/reference a real Activity where the accepted model permits it.

The link does not merge identities:

```text
Step references Activity
!=
Step becomes Activity
```

The Activity keeps its own identity, lifecycle, Schedule, Session and later realized truth.

## 3.4 Decomposition versus ordering

Containment/decomposition answers what belongs to the Plan or structural parent.

Ordering answers presentation/structural sequence within that decomposition.

Neither relation is a Dependency by implication.

If B13-A supports nested structure, cycle prevention and same-Plan ownership become hard invariants. If the accepted architecture chooses only `Plan -> Step` for this gate, recursive hierarchy must not be added speculatively.

---

# 4. In scope

B13-A includes:

1. canonical Plan persistence/read foundation needed by this vertical;
2. internal work decomposition owned by a Plan;
3. internal Step/structural-child authoring and read semantics;
4. optional link from a structural child to an existing real Activity, with referential and ownership invariants;
5. explicit ordering representation separate from decomposition semantics;
6. accepted/current-state and history/transition evidence using the repository's established canonical patterns where applicable;
7. actor/source/provenance metadata where current architecture requires it;
8. guarded application/backend operations;
9. HTTP/OpenAPI/generated-client surface only where B13-A exposes public author/read behavior;
10. the minimum real product surface required to prove that canonical work structure is usable, without redesigning the whole Timeline UI;
11. focused local automated proof and catalog/dictionary reconciliation for any new persistence.

---

# 5. Explicit non-goals

B13-A does **not** include:

```text
B13-B qualified Dependency semantics
B13-C execution-structure constraints
B12 replanning/conflict/solver
solver candidate generation
automatic Schedule mutation
proposal acceptance semantics
AI scheduling authority
maximum Session count
merge compatibility
spacing rules
preparation/recovery rules
hidden dependency inferred from ordering
universal generic graph ontology
promotion of Step to root identity without model authority
UI/UX consolidation reserved for B07
```

No implementation may pull one of these concerns into B13-A merely because it is convenient for a schema or UI component.

---

# 6. Persistence / transition requirements

If B13-A requires new canonical persistence, it must follow the repository's published-migration discipline:

```text
forward-only migration
published migrations immutable
Dictionary updated
catalog/topology expectations updated
SQLAlchemy mapping registered where required
current accepted state explicit
history/transition evidence preserved
no destructive rewrite of accepted prior state
```

The concrete table/function names are intentionally **not frozen here**. They must be derived from the current physical/database patterns after repository inventory; semantic names are preferred over generic graph abstractions.

An ordering change must not silently rewrite decomposition history. An Activity-link change must not rewrite the Activity itself.

---

# 7. Required implementation discovery before DDL

Before creating a migration, inspect the live repository and decide from evidence:

1. whether existing Plan identity/address primitives are sufficient or require a dedicated Plan state family;
2. whether B13-A needs only `Plan -> Step` or recursive structural nesting;
3. the smallest semantic representation for decomposition membership;
4. the smallest explicit ordering representation compatible with correction/reordering history;
5. how an optional Activity reference is represented without identity collapse;
6. which current-state/history/material-state primitives can be reused without forcing the wrong semantics;
7. which cross-entity ownership, duplicate-link and cycle constraints belong in PostgreSQL versus guarded operations;
8. whether the public vertical requires new API/client/UI in B13-A or whether persistence/backend proof is sufficient for part of the gate.

Do not write DDL until these questions are answered from repository evidence.

---

# 8. Acceptance criteria

B13-A can close only when all applicable criteria are true:

1. a canonical Plan can own and read a deterministic work structure;
2. internal structural children can be created/read/reordered without becoming Activity identities;
3. where supported, a structural child can reference a real Activity while the Activity retains independent identity/lifecycle/Schedule/Session semantics;
4. decomposition and ordering are represented without implying Dependency semantics;
5. invalid cross-Plan membership/reference cases are rejected deterministically;
6. duplicate structural membership/link cases are bounded by explicit invariants;
7. recursive-cycle cases are rejected if recursive nesting is part of the accepted B13-A architecture;
8. accepted/current-state reads are deterministic and correction/history behavior does not depend on `latest row` accident;
9. any new persistence is reconciled through Alembic, Dictionary, catalog expectations and ORM mapping inventory;
10. public API/OpenAPI/generated-client artifacts are deterministic/current if public routes are introduced;
11. focused backend/web tests exist where the corresponding surfaces exist;
12. user-run local gates pass;
13. roadmap, live ledger and handoff are reconciled before marking B13-A closed.

---

# 9. B13 continuation boundary

After B13-A is closed:

```text
B13-B — Qualified Dependencies
B13-C — Execution Structure Constraints
B13-D — Whole-block Integration / Proof / Acceptance
```

B13-B owns real dependency semantics. B13-C owns execution-structure constraints such as maximum Session count, merge compatibility, spacing and preparation/recovery where supported by current Domain/Logical authority. B13-D proves the complete B13 chain and product behavior.

B12 remains held until B13 is closed so solver/replanning logic consumes canonical work structure and dependency truth rather than inventing it.
