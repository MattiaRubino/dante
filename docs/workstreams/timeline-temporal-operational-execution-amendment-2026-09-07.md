# Timeline / Temporal-Operational — Execution Amendment 2026-09-07

- **Status:** ACTIVE EXECUTION AMENDMENT
- **Workstream branch:** `feature/timeline-temporal-operational`
- **Protected-main SHA reverified before B00 implementation:** `981f6cf9ad985d0b811bc4172c12a7529fbc9b15`
- **Database authority:** PostgreSQL 18.6 / Alembic `20260906_18`

## 1. Branch discipline amendment

The product owner explicitly selected **one branch for the whole Timeline / Temporal-Operational vertical**.

Therefore this amendment supersedes only the branch-per-block guidance in
`timeline-temporal-operational-roadmap.md §0.7`.

Canonical execution rule from this point forward:

```text
feature/timeline-temporal-operational
└── B00 → B01 → ... → B14
```

No `feature/temporal-b00-*`, `feature/temporal-b01-*`, or equivalent implementation branches are part of the accepted execution plan.

The semantic map, block ordering, Definition-of-Done gates, no-runtime-mock rule, forward-migration rule and protected-main safety rules remain unchanged.

Reviewability is preserved through bounded commits/slices and the live implementation ledger rather than branch proliferation.

## 2. B00 first implementation slice

This slice establishes the first real transport/data-source seam without inventing product persistence:

```text
authenticated request
→ require_dante_context()
→ Account → self Person
→ effective request timezone
→ Temporal Timeline application boundary
→ bounded half-open local-date window
→ HTTP transport
→ governed web fetch
→ strict frontend temporal Timeline data source
```

B00 deliberately returns a truthful empty projection until a later block activates a semantically justified real temporal projection family.

This is not authorization for:

- generic `temporal_item` persistence;
- generic `timeline_entry` persistence;
- Activity/Event/Routine schema invented merely to create demo cards;
- frontend inference of canonical semantics;
- fake success after transport/backend failure.

## 3. Current B00 checkpoint semantics

The first code slice may prove only the capabilities it actually implements. It does **not** close B00 by itself.

Still required before B00 can become `✅` include at minimum:

- normal Timeline runtime cutover away from prototype cards/clock;
- explicit fixture/test-only isolation;
- real PostgreSQL-backed temporal query activation when a legitimate readable family exists;
- isolated `userTest`/test-data setup and cleanup;
- real backend + real PostgreSQL E2E harness;
- manual empty/error/real-path acceptance;
- full F0/T1 regression proof.

No checklist item may be marked green merely because this boundary exists.
