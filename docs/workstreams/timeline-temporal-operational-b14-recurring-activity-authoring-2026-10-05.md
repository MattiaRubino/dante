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
