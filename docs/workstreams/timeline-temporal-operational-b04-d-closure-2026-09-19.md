# Timeline / Temporal-Operational — B04-D Movement Policy Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-19
- **Branch:** `feature/timeline-temporal-operational`
- **Previous slice:** B04-C Windows / Preferences / Evaluation ✅ CLOSED / PROVEN
- **Next slice:** B04-E Advanced-family applicability
- **Candidate PostgreSQL:** 18.6
- **Candidate Alembic head:** `20260919_39`
- **Candidate topology:** `115|5|42|89|232|152|329|0|0|0`
- **B04 execution authority:** `timeline-temporal-operational-b04-execution-plan.md`
- **Live ledger:** `timeline-temporal-operational-map.md`
- **Database overlay:** `../database/timeline-temporal-operational.md`
- **CI:** not used; local PostgreSQL gates are the closure evidence

---

# 1. Closure decision

B04-D is closed because the candidate branch now contains and proves a bounded Movement Policy capability that governs automatic changes to accepted Schedule placement without collapsing policy, Temporal Constraint, proposal, solver result or accepted effect.

```text
B04-D Movement Policy ✅ CLOSED / PROVEN
```

B04-D does **not** close B04 overall. B04-E and B04-F remain open.

---

# 2. Canonical semantic result

B04-D preserves:

```text
Temporal Constraint
= where/when a placement is valid or preferred

Schedule
= current accepted temporal assignment

Movement Policy
= whether automatic movement is admitted and through which acceptance path

proposal
= candidate effect awaiting explicit acceptance when required

accepted Schedule effect
= canonical placement mutation after all governance checks pass
```

Permanent distinctions proven by this slice:

```text
Schedule != Temporal Constraint
Schedule != Movement Policy
Temporal Constraint != Movement Policy
Movement Policy != Authority itself
Movement Policy != solver result
proposal != accepted effect
Movement Policy revision != Schedule revision
Temporal Constraint revision != Schedule revision
hard planning violation != impossible reality
soft preference violation != automatic rejection
violation != automatic mutation
```

The prototype vocabulary `locked | window | confirm | free` was not copied as a kernel enum. B04-D decomposes the governed behavior into independent typed dimensions while B04-C remains owner of validity/preference windows.

---

# 3. Frozen B04-D state model

Movement Policy is a typed Schedule-owned MaterialState facet:

```text
facet                     schedule.movement_policy
owner                     accepted Schedule
scope                     self-Person Activity/Event schedules

automatic_movement_code   blocked | automatic
acceptance_path_code      direct | confirmation_required
```

Valid combinations are bounded:

```text
blocked   + direct
automatic + direct
automatic + confirmation_required
```

`blocked + confirmation_required` is rejected because confirmation is an acceptance path for admitted automation, not a second spelling of locked state.

Movement Policy is independently revisable through expected-state CAS and retained MaterialState/current-history chronology.

---

# 4. Persistence result

Migration chain added by B04-D:

```text
20260919_37 b04_schedule_movement_policy_core
20260919_38 b04_governed_schedule_move
20260919_39 b04_schedule_move_accept_replay_fix
```

Canonical tables:

```text
schedule_movement_policy_state
schedule_movement_policy_current_history
schedule_movement_policy_mutation_operation
schedule_move_proposal
schedule_move_request_operation
schedule_move_accept_operation
```

Canonical capability / integrity routines:

```text
enforce_schedule_movement_policy_history()
mutate_self_schedule_movement_policy(...)
resolve_self_schedule_movement_policy(...)
assert_absolute_schedule_move_hard_admissible(...)
apply_governed_absolute_schedule_move(...)
request_self_absolute_schedule_move(...)
accept_self_absolute_schedule_move_proposal(...)
```

Shared control changes:

```text
material_state_address
  + schedule.movement_policy facet

enforce_material_state_totality()
  + exact Movement Policy owner/facet/payload branch
```

No generic Rule/Movement JSON root was introduced.

---

# 5. Governed movement semantics

## 5.1 Blocked automation

```text
automatic_movement_code = blocked
→ automatic Schedule move rejected
```

Manual/explicit user Schedule paths remain distinct from automatic Movement Policy enforcement; B04-D does not reinterpret unschedule/Undo or all manual edits as automatic movement.

## 5.2 Direct automatic movement

```text
automatic + direct
→ verify self scope
→ verify exact expected placement MaterialStateRef
→ verify current Movement Policy
→ evaluate all current hard Temporal Constraints against supplied absolute interval
→ append new Schedule placement MaterialState/current-history
→ retain immutable request receipt
```

The B04-D engine accepts or rejects a supplied candidate; it does not search for one.

## 5.3 Confirmation-required movement

```text
automatic + confirmation_required
→ request persists schedule_move_proposal
→ Schedule placement remains unchanged
→ explicit acceptance required
→ acceptance rechecks placement basis
→ acceptance rechecks same current Movement Policy basis
→ acceptance rechecks hard Temporal Constraints
→ only then append accepted Schedule placement state
```

This makes `proposal != accepted effect` structural rather than merely conventional.

---

# 6. B04-C hard-admissibility integration

Automatic Schedule movement composes current effective hard Temporal Constraints from B04-B/C.

Supported hard rules at B04-D closure:

```text
earliest_start     + schedule.start
latest_start       + schedule.start
latest_completion  + schedule.completion
start_within              + schedule.start
completion_within         + schedule.completion
full_placement_contained  + schedule.placement
placement_overlaps        + schedule.placement
```

Behavior:

```text
hard satisfied       → may proceed if policy/CAS also permit
hard violated        → reject automatic movement
hard not evaluable   → fail closed
soft violated        → does not block movement
```

No Actual/Outcome truth is inferred from constraint violation.

---

# 7. CAS / idempotency / chronology

B04-D preserves the same governance discipline as earlier Timeline slices:

- Movement Policy create/revise/retire has operation-id replay and changed-intent collision rejection.
- Policy revise/retire requires the exact current expected MaterialStateRef.
- Automatic move request requires the exact expected current placement MaterialStateRef.
- Confirmation proposal retains the exact policy and placement basis on which it was proposed.
- Acceptance rejects stale placement or stale policy basis.
- Direct request and proposal acceptance have immutable idempotency receipts.
- Schedule placement history remains monotonic; accepted movement appends a new placement state rather than rewriting the previous one.
- `_39` fixes proposal-accept replay so replay returns the original accepted effect without PL/pgSQL output-column ambiguity.

---

# 8. Security boundary

Canonical B04-D tables remain default-deny to `dante_runtime` for direct DML/read mutation surface.

Runtime receives EXECUTE only on governed entrypoints required by the application:

```text
mutate_self_schedule_movement_policy(...)
resolve_self_schedule_movement_policy(...)
request_self_absolute_schedule_move(...)
accept_self_absolute_schedule_move_proposal(...)
```

Internal helper routines remain non-runtime surfaces:

```text
enforce_schedule_movement_policy_history()
assert_absolute_schedule_move_hard_admissible(...)
apply_governed_absolute_schedule_move(...)
```

This prevents callers from bypassing policy/hard-constraint governance through direct canonical-table mutation or the internal apply helper.

---

# 9. Public API disposition

B04-D adds no public Temporal HTTP endpoint.

Therefore:

```text
Temporal API inventory      unchanged from B04-C
OpenAPI snapshot            no B04-D churn required
@dante/api-client           no B04-D regeneration required
frontend generated client   unchanged by design
```

The capability boundary is application/PostgreSQL for this slice. Public product exposure can occur in the later owning product/integration slice without changing B04-D canonical semantics.

---

# 10. Database reconciliation

Observed PostgreSQL authority after `_39`:

```text
DATABASE_CURRENT_TOPOLOGY=115|5|42|89|232|152|329|0|0|0
```

Dictionary, SQLAlchemy mappings, Alembic and live PostgreSQL are reconciled at:

```text
115 tables
5 views
42 routines
89 triggers
232 indexes
152 foreign keys
329 CHECK constraints
0 enum/domain
0 sequences/materialized/partitioned
0 RLS
```

Six B04-D tables and seven B04-D routines are represented in the Dictionary, and shared `material_state_address` / `enforce_material_state_totality()` entries reflect the new facet.

---

# 11. Observed local proof

First B04-D functional gate after replay fix:

```text
7 passed in 14.57s
```

Covered suites:

```text
apps/backend/tests/integration/temporal/test_b04_movement_policy_core.py
apps/backend/tests/integration/temporal/test_b04_governed_schedule_move.py
apps/backend/tests/integration/database/test_b04_d_movement_catalog_probe.py
```

Final whole-catalog reconciliation gate:

```text
3 passed in 9.50s
```

Covered suites:

```text
apps/backend/tests/integration/database/test_database_current_catalog.py
apps/backend/tests/integration/database/test_b04_d_movement_catalog_probe.py
```

Proofed behaviors include:

```text
locked/blocked automation rejection
admissible direct automatic move
confirmation proposal with no immediate Schedule mutation
explicit proposal acceptance
stale placement CAS rejection
stale Movement Policy basis rejection
hard constraint rejection
soft preference non-blocking behavior
request replay
acceptance replay
Schedule history monotonicity
runtime ACL boundary
Dictionary/SQLAlchemy/Alembic/PostgreSQL exact parity
```

No CI run is claimed or required for this closure; local PostgreSQL proof was deliberately used as the faster authoritative gate.

---

# 12. Explicit non-scope / later ownership

B04-D does not implement:

```text
candidate search
optimization
conflict solving
fallback/replanning strategy
complete multi-actor Authority / Participation
provider synchronization
Session runtime
Actual / Outcome inference
date-span automatic move candidates
floating-local automatic move candidates
named-zone-local automatic move candidates
coarse-local-period automatic move candidates
advanced duration / spacing / relative Temporal Constraint families
```

Broad replanning/conflict/solver remains B12.

---

# 13. Next gate

```text
B04-A ✅ CLOSED / PROVEN
B04-B ✅ CLOSED / PROVEN
B04-C ✅ CLOSED / PROVEN
B04-D ✅ CLOSED / PROVEN
B04-E ⬜ NEXT
B04-F ⬜
```

B04-E must classify the remaining advanced-family items and activate only semantics that current canonical owners/anchors can represent and evaluate truthfully.

B05 does not begin until B04-F closes.
