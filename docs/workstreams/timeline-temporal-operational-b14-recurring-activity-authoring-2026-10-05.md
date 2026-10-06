# B14 — Recurring Activity authoring + inherited Reminder

- **Status:** APPROVED PRODUCT/DOMAIN BOUNDARY — IMPLEMENTATION OPEN
- **Date:** 2026-10-05
- **Branch:** `feature/timeline-temporal-operational`
- **Parent:** B14 + B07 Product / UI Consolidation
- **Scope:** creation only; post-create series mutation remains out of scope

## Trigger

The consolidated Activity Create surface now exposes a simple calendar `Ripeti` control. Real-app use exposed two missing vertical links:

1. `Aggiungi` cannot truthfully persist the new recurring Activity intent through the current U2 Activity authoring path;
2. `Ricorda` is currently disabled when recurrence is active because B11-C only owns a Reminder for one accepted Schedule.

Neither issue may be fixed by UI-only fallbacks.

## Permanent boundaries

```text
Activity != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Routine occurrence policy != Schedule
series Reminder policy != Schedule Reminder
Reminder configuration != delivery
planned/intended != happened
```

A manual repeating Activity is authored as recurring intent owned by a Routine. The Routine remains the recurring source; generated Occurrences remain distinct identities; every accepted placement remains an independent Schedule.

## Creation contract

For the calendar-based Activity repeat slice accepted by the product UI:

```text
Activity Create intent
  -> Routine source
  -> Routine-owned Recurrence
  -> Routine occurrence placement policy
  -> Occurrence materialization
  -> one accepted Schedule per materialized Occurrence
```

The placement policy is source policy, not Schedule truth. It carries only what is needed to turn one generated calendar Occurrence into its concrete initial placement, including duration and the applicable local/named-zone frame. The Occurrence Schedule is still created as normal shared Schedule history and may later diverge through governed movement/replanning.

No hidden Activity duplicate is created merely to act as a recurrence template.

## Reminder inheritance

`Ricorda` remains a first-class Create control when a timed repeating Activity is authored.

A selected lead time is stored as a **Routine occurrence Reminder policy**. It is not attached only to the first generated Schedule.

When a future Occurrence is materialized and its initial Schedule is accepted:

```text
Routine Reminder policy
  -> configure that Occurrence Schedule's B11-C Schedule Reminder
```

Therefore every future occurrence inherits the configured lead without frontend loops or a finite pre-generation hack.

The resulting Reminder remains a normal B11-C Schedule Reminder:

- it belongs to one concrete Schedule;
- its due time is derived from that Schedule's current exact start;
- moving/replanning the Schedule continues to affect reminder due time through existing B11-C semantics;
- no notification-delivery claim is introduced.

If the series has no exact timed placement, `Ricorda` may remain unavailable because there is no truthful exact Schedule start from which B11-C can derive a due time. **Recurrence by itself is not a reason to disable Reminder.**

## Product metadata boundary

This slice must not silently discard Activity-only authoring data when switching to Routine ownership.

The first recurring-Activity vertical is therefore bounded to the product fields that have an explicit Routine/Occurrence home. Any Activity interval, planned Session, or other structure that has not yet been given truthful occurrence-template semantics must be rejected explicitly rather than dropped.

Life Area remains optional at the Activity product level. Recurring Activity authoring must not reintroduce the superseded B05 rule that every item requires a Life Area.

## UI decision

The main `Ripeti` selector is the single family selector. The expanded panel must not contain a second `giorno / settimana / mese / anno` selector.

The detailed panel shows:

```text
Ripeti ogni [N] giorno|settimana|mese|anno   # unit derived from the master selector

... family-specific controls ...

Termina
  ( ) Mai
  ( ) Data   [date]
  ( ) Dopo   [N] occorrenze
```

All three ending rows remain mounted and stable. Selecting one changes state; it does not make the other choices jump in or out of the layout.

## Implementation gate

This vertical is complete only when all of the following are true:

1. optional-Life-Area recurring Activity creation succeeds atomically;
2. recurrence and source replay/idempotency are preserved;
3. the occurrence placement policy is canonical and does not collapse Recurrence into Schedule;
4. current and future materialized Occurrences receive independent accepted Schedules;
5. a configured series Reminder is inherited by every such Occurrence Schedule through B11-C;
6. recurrence without Reminder remains valid;
7. Create closes only after the recurring source transaction has been accepted;
8. no Activity-only metadata is silently discarded;
9. OpenAPI and generated client are regenerated from source, never hand-edited;
10. focused PostgreSQL/API/web gates pass locally before this candidate is marked proven.

## 2026-10-06 — unassigned Routine readback correction

Migration `20261006_109` repairs the Routine listing capability after `_108` made
Life Area optional. An unassigned Routine returns assignment revision `0` (not
a nullable revision) so source creation can read its own accepted current state.

This is a B14 implementation repair only; the recurring-Activity vertical remains
open until every requirement in the implementation gate is proven.

## 2026-10-06 — approved complete occurrence inheritance (implementation open)

The user approved the expanded Create contract after a real-app Create rejected
recurrence combined with Activity intervals and planned Sessions. The prior
bounded implementation guard is **not** the desired final product behavior.
It remains necessary until the following contract is implemented; removing it
alone would silently lose authoring intent.

Each materialized Occurrence must start from a complete, versioned copy of the
Create template: the Activity's temporal intervals and named planned Sessions,
Sub-Activities/blocks when configured, capture/session settings, Reminder lead,
outcome-review settings, and placement protection. A generated Occurrence has
its own stable identity and independent accepted Schedule(s), planned Session
rows and subsequent Session/Actual/outcome state. Execution or editing of one
Occurrence must not mutate another or rewrite the source template.

The template is source policy, not a pre-created collection of future
Activities or Schedules. Materialization must apply it to every newly generated
Occurrence (including later checkpoints), with deterministic idempotency and
explicit zone/DST handling for multiple local intervals. No finite client-side
loop, duplicated generic Activity detached from its Occurrence, or ignored
field is an acceptable substitute. A Reminder is configured on the appropriate
concrete Occurrence Schedule once, rather than multiplied merely because an
Occurrence has several planned rows. Post-create editing of one, future and
whole series remains a separate scope and must not be claimed by Create.

The Create lock labelled "Blocca spostamenti" currently maps to B04 Movement
Policy `blocked + direct`, which prohibits only automatic movement. Manual
Timeline drag and time-editor revision remain possible. This is **not** the
approved meaning of that control. A real placement lock must persist a
distinct manual-movement prohibition, reject manual placement revisions at
the canonical server/database boundary as well as automatic movement, expose
its state to the Timeline, and provide explicit unlock before either path
can move the card. Do not reinterpret the existing B04 automation policy as
a global manual lock: its documented contract deliberately permits manual
edits when automation is blocked.

Acceptance is open until recurrence plus each supported structure/policy
combination survives Create, readback, later checkpoint and independent
per-Occurrence execution, and until a locked card cannot be moved by pointer,
keyboard, time editor or direct Schedule revision. The user runs the local
gates; no CI or unreported PASS claim.

## 2026-10-06 — placement lock candidate (not proven)

Commit `9d2b6130` introduced forward migration `_110` and an explicit Activity Schedule user placement lock. Create applies it alongside B04 automatic movement protection to the root, Activity intervals, planned Session rows and child Schedules. A database history guard rejects revisions/unschedule while locked, including non-UI callers; Timeline readback, drag/keyboard/time-editor guards and an explicit detail-panel toggle are candidate code. Commit `84161fa5` makes lock-only Timeline updates reconcile without a placement revision. This candidate has **not** received the user's PostgreSQL/OpenAPI/web gate or real-app acceptance. Existing B04 `blocked + direct` states were not backfilled as user locks because that policy intentionally allows manual edits; existing cards can be locked explicitly in their detail panel.

Complete recurring Activity template inheritance remains **open**. The `_110` lock infrastructure must not be described as solving recurring intervals, planned Sessions, outcome review, Reminder propagation or per-Occurrence independence. Generated API client and Database Dictionary reconciliation are pending the user's local gate.
