# B13-A — Work Structure Core closure

- **Date:** 2026-09-28
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** CLOSED / focused local automated proof
- **Persistence frontier:** Alembic `20260928_89`
- **Catalog-verified topology:** `191|5|148|100|386|334|488|0|0|0`
- **Real-app whole-block acceptance:** reserved for B13-D

## Scope closed

B13-A adds canonical self-owned Plan structure with internal Step references, immutable normalized revision snapshots, an explicit accepted-current binding and history, stable presentation order, and optional links to existing self-owned Activities. A Step remains distinct from an Activity; ordering does not create a Dependency. Guarded Plan operations provide idempotent creation, expected-current replacement, historical receipts, and bounded self-scoped reads. The Home panel authors and reads this canonical path.

The published migration chain is `_87` structure, `_88` replay/catalog-name repair and `_89` accepted-current update qualification. The `_88` SQL alias was corrected in its source after its first published form failed transactionally before application; the checkpoint records that exception. `_89` is a forward revision after `_88` was applied in the local gate.

## Local proof reported by the user

```text
Python Ruff check + format             passed (checked repair/application files)
OpenAPI contract + inventory            4 passed
PostgreSQL B13-A + exact catalog        9 passed in 24.09s at _89
Web data source                          3 passed
Web Plan/Step panel                      1 passed
Web typecheck                            passed
Deterministic generated-source check     371 files current
API-client typecheck                     passed
```

The exact PostgreSQL catalog tests compare live topology, constraints, indexes, mappings, Dictionary entries, ACLs and Alembic head. The focused Plan test exercises self ownership, replay, expected-current conflict, Step reorder and history, duplicate membership/link rejection, foreign Activity rejection and cross-Plan Step rejection. The generated OpenAPI/client artifacts were committed as `96f2f7b9`.

This is a focused automated closure. There is no claim of a B13 whole-block real-app walkthrough; B13-D owns integrated A/B/C acceptance.

## Continuation

B13-B is the next gate. Freeze qualified Dependency semantics against the current Domain/Logical/Physical authority before implementation. Dependency remains separate from containment and Step presentation order. B12 stays held until B13-D closes.
