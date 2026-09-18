# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B03 Event Core ✅ CLOSED / PROVEN + pre-B04 governance ✅ CLOSED / FROZEN → B04 NEXT
- **Reconciled:** 2026-09-18
- **Branch:** `feature/timeline-temporal-operational`
- **Current roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Current live map/ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **B03 closed execution authority:** `docs/workstreams/timeline-temporal-operational-b03-execution-plan.md`
- **B03-E / whole-B03 closure:** `docs/workstreams/timeline-temporal-operational-b03-e-closure-2026-09-18.md`
- **Pre-B04 governance closure:** `docs/workstreams/timeline-temporal-operational-pre-b04-governance-2026-09-18.md`
- **Timeline candidate DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Manual B03 userTest:** `docs/workstreams/timeline-temporal-operational-b03-usertest.md` ✅ PASS
- **Next implementation gate:** `APPROVE B04`
- **CI:** no CI launch is implied or authorized

## 1. Current workstream position

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ⬜ NEXT
B05 Product Organization                         ⬜
B06 Routine / Recurrence / Occurrence Baseline   ⬜
B07 UI/UX Consolidation v1                       ⬜ planned after B06
B08 Session Runtime                              ⬜
B09 Responsibility / Participation               ⬜
B10 Actual / Outcome / Confirmation / Resolution ⬜
B11 Advanced Recurrence / Conditional / Reminder ⬜
B12 Replanning / Conflict / Solver               ⬜
B13 Provider / Offline / Multi-device             ⬜
B14 Analytics / Statistics / Signals             ⬜
B15 Whole Vertical Closure                       ⬜
```

Current candidate DB:

```text
PostgreSQL 18.6
Alembic     20260917_29
Topology    101|5|31|78|198|119|297|0|0|0
```

## 2. Closed B03 foundation

B03-A established canonical Event identity/expectation/create/read.

B03-B proved Activity and Event use the same Schedule authority:

```text
Activity ─┐
          ├→ shared ScheduleRef / placement MaterialState / current/history
Event ────┘
```

B03-C activated Event placement lifecycle on that same machinery.

B03-D activated Event-internal Agenda values at `_29` without identity inflation.

B03-E proved the entire B03 surface through broad regressions, real-stack Chromium/Firefox and manual product acceptance, then reconciled generated OpenAPI/client authority.

## 3. Pre-B04 governance baseline

The pre-B04 audit found and closed two governance gaps before allowing new feature scope:

```text
1. current human DB references had candidate drift (_27 prose vs _29 reality)
2. Temporal API lacked an exact complete operation inventory equivalent to Access/Auth governance
```

Now:

```text
docs/database/README.md                         current protected-main + _29 candidate summary
docs/database/dictionary/README.md              current B03 closure prose
docs/database/timeline-temporal-operational.md  candidate-only DB overlay
Temporal OpenAPI inventory test                  exact 13-operation baseline
```

Binding DB gate for B04+:

```text
Alembic
≈ SQLAlchemy
≈ Dictionary + scope
≈ live catalog / owner / ACL
≈ current DB SoR
≈ Timeline DB overlay
≈ direct PostgreSQL proof
≈ workstream closure docs
```

Binding API gate for B04+:

```text
route/model
→ explicit stable semantic operationId for every new endpoint
→ exact Temporal inventory
→ OpenAPI snapshot
→ Orval / @dante/api-client
→ affected API/frontend tests
→ workstream docs
```

Existing pre-B04 Temporal operationIds remain frozen compatibility baseline and are not deprecated merely because their original FastAPI-generated names are verbose.

## 4. Proven B03 behavior

```text
canonical Event identity + expectation
idempotent self-scoped Event create
shared Activity OR Event Schedule authorization
atomic Event + initial Schedule creation
floating-local Event
named-zone-local Event with source/DST semantics
all-day/date-span Event
multi-day Event
Timeline scheduled_activity | scheduled_event union
strict API / TypeScript parser + hydration
minimal truthful Event Create runtime
Event reschedule through shared Schedule revision
postponed/TBD with no current placement and preserved Event/history
Event readability while current placement is absent
stale expected-state conflict protection
guarded Undo through a new MaterialState
idempotent Undo replay
immediate lifecycle after Event create without reload
ordered bounded Event Agenda values
Agenda add/edit/reorder/remove/reload
aggregate Agenda revision/CAS
Agenda operation-id idempotent replay
explicit Agenda rename Save/Cancel + Enter/Escape
real Event-detail Agenda editor backed by backend truth
Activity Schedule regression preservation
no event_schedule table/current/history engine
no NativeRef per Agenda part
```

## 5. Whole-B03 proof summary

```text
B03-D focused PostgreSQL/API Agenda          2 PASS
B03-D DB/Alembic/Dictionary                 12 PASS
B03-D affected web                           6 files / 19 PASS
B03-D final B02+B03 backend regression      13 PASS / 2 deselected
B03-D final Activity/Event web regression    5 files / 26 PASS

B03-E real-stack Chromium + Firefox          2 PASS
B03-E web broad regression                   158 files / 741 PASS
B03-E Temporal PostgreSQL broad              24 PASS / 2 deselected
B03-E backend broad                          494 PASS + sole generated snapshot mismatch
B03-E OpenAPI gate after regeneration        8 PASS
B03-E manual userTest A–F                    PASS
```

The broad backend selection was not redundantly rerun after generated-artifact regeneration because its sole failure was the governed OpenAPI snapshot; that exact guard was then rerun green.

## 6. Manual-acceptance findings disposition

### Agenda rename — CLOSED in B03

The manual test exposed an ambiguous rename commit interaction. B03 was not closed until the product gained explicit **Salva / Annulla**, retained Enter/Escape, proved cancel sends no backend mutation, and the user manually accepted the corrected behavior.

### Postponed/TBD rediscovery — transferred to B05

B03-C semantics are correct: a postponed Event stays alive with history and has no current Schedule; it is not a Planning Tray Activity.

B05 must provide a discoverable product surface for postponed/TBD Events so they can later be explicitly rescheduled without fabricated temporal truth.

### Agenda vs timed sub-events

Agenda is ordered Event-internal content, not independent temporal ownership. Any future requirement for independently timed internal segments requires a distinct semantic design; do not add Schedule identity to Agenda parts as a shortcut.

## 7. Semantic boundaries still binding

```text
Activity != Event
Event != Schedule
Event != Recurrence
Event != Occurrence
Event != Session
Event != Actual
Event != Outcome
Event != Participation
Event != Availability / Capacity Claim
Event identity != provider identity
Agenda part != Activity/Event/Occurrence/Schedule/Session/Actual by default
original Event expectation != current Schedule
current Schedule != future Actual
postponed/TBD Event != Planning Tray Activity
projection != canonical truth
Undo != history rewind
```

EVT-012 through EVT-015 remain explicit future-owner obligations. Their unchecked state is intentional and must not be converted into fake B03 completion.

## 8. Exact B04 starting target

B04 is **Temporal Constraints + Movement Policy**. Its pre-scope/execution plan is already frozen; implementation has not started.

Core non-collapse:

```text
Schedule != Temporal Constraint
constraint != placement
movement policy != solver result
proposal != accepted effect
planned/intended != happened
```

B04 must not prematurely implement B05 organization, B06 recurrence, B08 Session, B10 Actual or B12 solver semantics.

Every B04 slice must obey the pre-B04 DB/API same-change governance closure; no slice may close with known documentation, schema, OpenAPI or generated-client drift.

## 9. Detailed semantic authority

The full initial functionality/logic map remains binding at:

`docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

The live map records implementation/proof progress and does not replace the semantic freeze.

## 10. Next gate

```text
APPROVE B04
```

No B04 implementation and no CI run are implied by this handoff.