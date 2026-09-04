# DANTE — Temporal Create C1 Scope Amendment

**Status:** ACTIVE AUTHORITY  
**Reconciled:** 2026-09-04  
**Owner workstream:** `feature/home-timeline`  
**Integration target:** `feature/home-react`  
**Current code checkpoint:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**Scope stop:** maximum useful pre-backend manual Create capability; no real API persistence, provider execution, authoritative solver, canonical recurrence evaluator/Occurrence generation, real notification delivery, AI/NL/voice runtime or server product Auth/ACL

## 1. C1 scope

C1 is the manual Timeline Create authoring surface and its truthful local application/projection integration.

Allowed entry origins:

- Timeline `+`;
- Timeline double-click on empty timed space;
- Timeline Shift-drag/range;
- deterministic structured manual prefill.

Not C1:

- chat/NL interpretation;
- AI command bar;
- voice capture/interpretation;
- autonomous DANTE planning;
- real provider/backend execution.

## 2. Actionable types

Current UI exposes only:

- Activity;
- Event.

Routine remains an owning semantic vertical rather than a dead primary tile. Reminder/Alarm and other owners remain deferred until their authoring/runtime boundary is truthful.

## 3. Activity scope

Placement choices:

- `Orario`;
- `Tutto il giorno`;
- `Da collocare`.

Placement remains authoritative when execution/session settings change.

Advanced Activity may author relevant scheduling/execution/confirmation/notes metadata without claiming Session or Actual execution.

### Activity repeat — clarified 2026-09-04

Direct canonical Activity-owned recurrence remains forbidden.

However, C1 **may expose user-facing Repeat on Activity** when the authored rule is explicitly marked Routine-backed:

```text
user chooses Activity + Repeat
→ Activity remains Activity
→ recurrence owner = Routine
→ future Routine recurrence evaluator owns canonical Occurrences
```

This is not an `Activity.repeat` domain feature.

Quota patterns such as N times/week map to CP6 `quota_per_period` under Routine ownership.

## 4. Event scope

Base Event authoring includes timed/all-day semantics, Context, location and common Repeat.

Event recurrence is Event-owned. Custom recurrence can author all four CP6 families:

- `calendar_wall_clock`;
- `elapsed_interval`;
- `quota_per_period`;
- `cyclic_positional`.

Advanced Event may author availability, visibility intent, purpose/outcome, Agenda/internal parts, participants/resources, pre-read, buffers, conference intent, confirmation metadata, appearance and notes.

Provider execution is not authorized.

## 5. Create presentation scope

### Simple/base desktop

- opens floating by default;
- stable initial position;
- compact;
- draggable;
- Home/Timeline remains interactive;
- no modal dim/freeze;
- outside/backdrop click is not the close contract;
- dirty draft close requires explicit discard confirmation.

### Advanced desktop

- larger floating surface;
- same draft;
- bounded to viewport;
- internally scrollable as needed;
- actions/back/close remain reachable;
- does not freeze Timeline.

Mobile remains viewport-bounded/full-screen appropriate.

A simple-only left pin/dock is a possible future product decision and is outside the currently implemented contract.

## 6. Planning Tray scope

Unplaced Activity is supported through:

- anchored desktop popover;
- mobile bottom sheet;
- direct remove + confirmation;
- one-card carried drag;
- same identity placement;
- Escape cancellation;
- Undo placement/removal.

No backend inbox persistence is implied.

## 7. All-day scope

All-day uses a real per-day lane. Its height participates in Timeline geometry. Multi-day continuation is supported.

Forbidden representations:

- global detached all-day header strip;
- fake 00:00–24:00 timed occupation.

## 8. Event Agenda scope

Ordered Event-internal agenda parts are in C1 and may map to native Timeline subitems.

They do not automatically become independent Activities, Events, Occurrences, Sessions or Actuals.

## 9. Recurrence materialization stop line

C1 authors recurrence **specification**, not future canonical instances.

The current local Create bridge may materialize the first/master placed projection for immediate UI feedback. It must not synthesize a fake durable recurring series.

Future vertical ownership:

```text
Routine/Event recurrence rule
→ backend evaluator/checkpoint
→ canonical Occurrences
→ temporal range/window query
→ Timeline read-model
```

## 10. Backend/external stop line

Outside C1:

- real API transport;
- PostgreSQL application writes;
- canonical server identity allocation;
- durable server idempotency/reconciliation;
- runtime Auth/ACL;
- provider writes/sync/invitations/room booking/conferencing;
- real notification/alarm delivery;
- authoritative scheduling solver;
- recurrence evaluator/checkpoints/canonical Occurrences;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI/NL/voice runtime.

## 11. Closure

C1 remains open until full automated green is followed by explicit final user manual approval.

Current code candidate `1e7b7752...` is automated green on Frontend CI #937 / `33905239085`, but manual UX refinement remains active.
