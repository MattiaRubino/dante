# Timeline / Temporal-Operational — B04-F / Whole-B04 Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-20
- **Branch:** `feature/timeline-temporal-operational`
- **Slice:** B04-F Whole-B04 closure
- **Previous slice:** B04-E Advanced-family applicability ✅ CLOSED / PROVEN
- **Next block:** B05 Product Organization ⬜ NEXT
- **Candidate DB head:** `20260920_42`
- **Candidate topology:** `116|5|44|90|233|153|331|0|0|0`
- **CI:** not dispatched; evidence is local and real-stack only

## 1. Closure decision

```text
B04-A ✅ CLOSED / PROVEN
B04-B ✅ CLOSED / PROVEN
B04-C ✅ CLOSED / PROVEN
B04-D ✅ CLOSED / PROVEN
B04-E ✅ CLOSED / PROVEN
B04-F ✅ CLOSED / PROVEN

B04 Temporal Constraints + Movement Policy ✅ CLOSED / PROVEN
B05 Product Organization ⬜ NEXT
```

B04 is closed as typed Temporal Constraint truth plus bounded Schedule Movement Policy. It does not claim a solver, recurrence execution, Session/Actual truth, multi-actor Authority, or Product Organization.

## 2. Final semantic and persistence authority

The completed B04 contract preserves:

```text
Temporal Constraint != Schedule
Temporal Constraint != Movement Policy
Movement Policy != Authority itself
Movement Policy != solver result
hard planning violation != impossible reality
deadline passage != Outcome
constraint revision != Schedule revision
policy revision != Schedule revision
planned Schedule duration != estimated effort != Session/Actual duration
```

The final forward-only persistence addition is:

```text
20260920_42  dante.assert_schedule_placement_hard_admissible(uuid,jsonb)
```

Canonical Schedule establish/revise paths invoke this internal, `SECURITY DEFINER` hard-admissibility guard. It rejects unevaluable or violated current hard Temporal Constraints and grants no direct EXECUTE to runtime, migrator or `PUBLIC`.

The final Dictionary/SQLAlchemy/Alembic authority is reconciled at:

```text
Alembic     20260920_42
Tables      116
Views         5
Routines     44
Triggers     90
Indexes      233
FKs          153
CHECKs       331
```

## 3. Whole-B04 evidence

Completed B04-A through B04-E closure records remain the exact evidence for their owned typed persistence, CAS/idempotency, API/OpenAPI/client, evaluator, movement-policy and applicability obligations.

B04-F adds and records the final cross-slice proof:

```text
B04-F constrained Activity + hard-Schedule PostgreSQL integration    4 PASS
B04-focused web runtime                                               5 PASS
web TypeScript                                                        PASS
Dictionary/current-catalog reconciliation                             _42 / 116|5|44|90|233|153|331|0|0|0
```

The direct PostgreSQL guard proof covers:

```text
atomic constrained Activity creation and idempotent replay
rollback when a child constraint operation collides
absolute placement inside a hard window is accepted
absolute placement outside a hard window is rejected
floating placement against an absolute hard window fails closed
rejected establish creates no Schedule
rejected revision leaves the current placement MaterialState unchanged
```

No B04-F public API widening was introduced. The public Temporal API/OpenAPI/client contract remains the one established and proven in the applicable B04-A/B/C slices; E and F add no invented public route or prototype-only claim.

## 4. Real-stack manual product acceptance

The user executed the accepted real local stack flow on 2026-09-20:

```text
Activity → Da collocare → Opzioni avanzate → Vincolo: Finestra
save + reload
placement inside the hard window
attempted placement outside the hard window
```

Result: **PASS**. The accepted placement persisted; the outside placement was rejected and did not replace accepted Schedule truth.

Product-boundary clarification recorded during acceptance:

```text
Fascia = B02 coarse Schedule placement (for example, Mattina)
Fascia != Temporal Constraint
Orario = B02 precise Schedule placement
```

Therefore constraint authoring intentionally appears only for an Activity selected as `Da collocare`, under `Opzioni avanzate`. The UI’s preferred-window path remains fail-closed until its non-absolute semantics are genuinely activated; it is not B04 proof.

Movement Policy enforcement is proven by canonical application/PostgreSQL tests, not misrepresented as a solver or automated product UI.

## 5. Explicit later ownership

```text
B05  Calendar / Life Area / Tags / product organization
B06  Routine / Recurrence / Occurrence baseline
B08  Session runtime
B09  participation / multi-actor Authority maturity
B10  Actual / Outcome / Confirmation
B12  solver / replanning / candidate search
```

No B04 table, API, UI field or status is reused to pretend that one of these later-owned semantics exists already.

## 6. Closure

All frozen B04 capability items are either implemented/proven in B04-A through B04-F or explicitly transferred with an owner and reopening trigger. Same-change Dictionary, Alembic and workstream documentation are reconciled.

```text
B04 Temporal Constraints + Movement Policy ✅ CLOSED / PROVEN
Next authorized planning boundary              B05 Product Organization
```
