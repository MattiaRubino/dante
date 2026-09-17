# Timeline / Temporal-Operational — B03-B Closure

- **Status:** ✅ CLOSED / PROVEN
- **Date:** 2026-09-17
- **Branch:** `feature/timeline-temporal-operational`
- **Scope:** Shared Schedule + Event Timeline
- **Alembic authority:** `20260917_28`
- **Topology:** `98|5|29|78|195|115|288|0|0|0` (unchanged structurally from `_27`; `_28` replaces governed Schedule routines)
- **Previous slice:** B03-A Event canonical core ✅ CLOSED / PROVEN
- **Next slice:** B03-C Event placement lifecycle ⬜ NEXT / NOT YET AUTHORIZED
- **CI:** not run; CI remains separately authorized

## 1. Closure invariant

B03-B proves that Event is a second explicit semantic owner of the already-established Schedule capability without creating a parallel temporal engine:

```text
Activity ─┐
          ├── shared ScheduleRef / placement MaterialState / current binding / history
Event ────┘
```

No `event_schedule` table, Event-specific Schedule current/history model, generic temporal mega-owner, or Activity-as-Event shortcut was introduced.

## 2. Implemented scope

B03-B activates:

```text
typed Schedule self-scope: Activity OR Event
atomic Event + initial Schedule creation
floating-local Event
a named-zone-local Event path with explicit DST disambiguation
all-day/date-span Event
multi-day date-span Event
Activity + Event Timeline discriminated projection
strict API / TypeScript Activity|Event union
frontend Event Timeline hydration
minimal truthful scheduled-Event Create runtime
```

The shared Schedule routines remain the canonical capability family:

```text
establish_self_schedule_placement(...)
revise_self_schedule_placement(...)
unschedule_self_schedule(...)
undo_self_schedule_unschedule_any(...)
```

`_28` generalizes their self-ownership checks through an explicit typed branch:

```text
Activity -> activity_intention.self_person_ref
Event    -> event_expectation.self_person_ref
```

## 3. Preserved stop lines

B03-B deliberately does not activate:

```text
Event reschedule/postponed/TBD/Undo product lifecycle  -> B03-C
Agenda/internal-part persistence                       -> B03-D
Event recurrence                                       -> B06
Temporal Constraints / movement policy                 -> B04
Life Area / Calendar / Tags                            -> B05
Session/execution                                      -> B08
participants / invitation responses                    -> B09
Actual / Outcome / Confirmation                        -> B10
reminders / conditional policy                         -> B11
provider conferencing / sync                           -> B13
```

Event Timeline projections are readable in B03-B, but Event revision/unschedule UI actions remain intentionally unavailable until B03-C. Activity lifecycle actions remain intact.

## 4. PostgreSQL / API proof

The targeted PostgreSQL/API gate initially executed 22 selected tests. Result:

```text
18 PASS
4 FAIL
```

All four failures reduced to one `_28` regression: the redefined `unschedule_self_schedule(...)` had lost B02 PL/pgSQL strict disambiguation, producing ambiguous `schedule_ref` references and breaking the historical downgrade round-trip contract.

The migration was corrected in:

```text
af16b700  fix(temporal): preserve B02 PL/pgSQL disambiguation in B03 shared schedule
```

The exact four previously failing proofs were rerun after the fix:

```text
4 passed in 12.10s
```

Those four cover:

- B02 all-form establish/revise/unschedule/Undo regression;
- B02 unschedule/Undo regression;
- Alembic head -> base -> head round-trip;
- preservation of the B02 PL/pgSQL hardening through `_28`.

The already-green portion of the original targeted gate covered B03 Event core, B03-B Event+Schedule/Timeline behavior, catalog/current-catalog authority, `_27`/`_28` migration guards and fresh-head migration proof.

B03-B PostgreSQL/API semantics include:

- floating-local Event;
- named-zone Event with source wall clock + resolved instants;
- single-day date-span Event;
- multi-day date-span Event;
- Event idempotent replay;
- mixed Activity/Event Timeline;
- explicit `scheduled_activity` vs `scheduled_event` identity;
- no `event_schedule` relation;
- fail-closed invalid/coarse Event create at B03-B scope;
- atomic failure behavior.

## 5. Frontend proof

Targeted Event transport/Timeline proof:

```text
3 test files passed
10 tests passed
```

Covered:

- remote Event datasource;
- Event Timeline read/parser and malformed/hybrid fail-closed behavior;
- authoritative Event Timeline hydration.

A missing dedicated B03 Create-runtime test was then added in:

```text
42eed660  test(web): prove B03 scheduled Event create runtime
```

The first run correctly exposed two closure issues:

1. the new negative test used `timeSemantics='unscheduled'`, but Event field normalization intentionally converts that prototype input to timed placement, so the test assertion itself was invalid;
2. Timeline UI mutation call sites accepted the new Activity|Event projection union while their mutation functions remained Activity-only, which would have leaked B03-C lifecycle semantics into B03-B.

Corrections:

```text
ddf60ee0  correct B03-B runtime negative proof
99ace71c  keep all-day Event lifecycle actions read-only in B03-B
3cd38fa6  narrow timed Event lifecycle actions to Activity-only in B03-B
```

Final web proof:

```text
temporal-create-b03-runtime.test.ts   2 passed
@dante/web typecheck                  PASS
```

The final runtime test proves scheduled Event creation through the canonical Event datasource, explicit Event identity in the projection, and fail-closed behavior for Event intent outside the minimal B03-B contract.

## 6. Semantic result

B03-B closes with these boundaries intact:

```text
Activity != Event
Event != Schedule
Schedule != Session != Actual
source wall-clock intent != resolved instant
date span != fabricated timed interval
projection != canonical truth
operation identity != Event identity != Schedule identity
current accepted state != latest row
Undo != history rewind
```

The detailed archived semantic freeze remains binding:

`docs/workstreams/archive/timeline-temporal-operational-map-ledger-snapshot-2026-09-15.md`

## 7. Closure decision

```text
B03-A  ✅ CLOSED / PROVEN
B03-B  ✅ CLOSED / PROVEN
B03-C  ⬜ NEXT / NOT YET AUTHORIZED
B03-D  ⬜
B03-E  ⬜
```

No B03-C/D/E implementation and no CI run are implied by this closure.