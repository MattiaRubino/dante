# DANTE — Temporal Create C1 Scope Amendment

**Status:** ACTIVE AUTHORITY — MANUAL FAIL / RE-ARCHITECTURE IN PROGRESS  
**Original amendment:** 2026-09-01  
**Reconciled:** 2026-09-03  
**Owner workstream:** `feature/home-timeline`  
**Integration target:** `feature/home-react`  
**Current code checkpoint:** `bd9bc6db13301763393c5345685dd38a1837aaaa`  
**Scope stop:** maximum useful pre-backend **manual** Create capability; no real API, PostgreSQL application persistence, provider execution, authoritative solver, recurrence evaluator/Occurrence generation, real reminder delivery, AI/NL input/runtime, voice input/runtime, or server product Auth/ACL

## 1. Scope decision

C1 remains the Timeline/manual authoring vertical, but its UI information architecture is being reworked after the 2026-09-03 manual fail.

The re-architecture does NOT reopen the closed Domain/Logical/Physical/CP6 model and does NOT widen the backend stop line.

Current authority:

- `temporal-create-c1-rearchitecture-2026-09-03.md`;
- `temporal-create-c1-manual-findings-2026-09-03.md`;
- `temporal-live-status.md`;
- `temporal-create-handoff.md`.

## 2. C1 remains manual-only

Allowed input origins:

- Timeline `+`;
- Timeline double-click on empty temporal space;
- Timeline Shift-drag/range;
- deterministic structured manual prefill.

Not C1:

- chat;
- natural-language interpretation;
- AI command bar;
- voice capture/interpretation;
- autonomous DANTE planning.

`TemporalCreateFieldSeed` remains manual deterministic prefill only.

## 3. Actionable Create types

The UI must use an extensible type registry/layout but show only types whose Create semantics are genuinely actionable.

### In current C1 scope

- Activity;
- Event.

### Deferred until truthful owner/runtime exists

- Routine direct creation from this surface;
- Reminder/Alarm direct creation;
- Project;
- Goal;
- Program;
- World;
- Template;
- Block;
- Asset.

These may exist as typed architectural handoff targets, but they must not appear as dead/disabled primary Create UI.

## 4. Activity scope

Base authoring must make the common case immediately usable.

Placement choices:

- timed/`Orario`;
- all-day/`Tutto il giorno`;
- unplaced/`Da collocare`.

Base fields must react to placement rather than remain disabled.

Activity advanced capability remains allowed for:

- exact expected duration;
- bounded window;
- deadline;
- preferred window;
- movement/replanning policy;
- indivisible/splittable execution;
- min/max session intent when splittable;
- preparation/recovery/spacing;
- fallback policy;
- confirmation/review intent;
- reminder intent as metadata only where already supported;
- Context;
- appearance override;
- notes.

Critical non-collapse:

```text
placement choice != execution/session structure
```

An Activity deliberately placed at an exact time remains placed when configured as splittable.

Activity recurrence remains OUT OF SCOPE and forbidden.

## 5. Event scope

Base authoring:

- timed Event;
- all-day/multi-day Event;
- start/end/duration;
- Context;
- location;
- common recurrence quick choices.

Quick recurrence choices:

- never;
- daily;
- weekly;
- monthly;
- yearly;
- custom.

Custom recurrence may expose all four CP6 Event recurrence families:

- calendar wall-clock;
- elapsed interval;
- quota per period;
- cyclic positional.

Advanced Event capability may include:

- floating vs named-zone time semantics;
- IANA timezone;
- availability;
- visibility intent distinct from ACL;
- purpose;
- expected outcome;
- agenda/internal parts;
- decision-required intent;
- participants;
- resources;
- pre-read;
- preparation/recovery;
- conference provider intent;
- confirmation/reminder intent;
- appearance;
- notes.

No provider execution is authorized.

## 6. Event Agenda/internal parts

C1 may author Event-internal agenda parts such as `Listening`, `Orale`, `Scritto`.

These are not automatically independent Events/Activities/Occurrences.

If a part later needs independent identity, time, state, responsibility or Actual semantics, that requires an explicit owning-domain design rather than generic nested entities.

## 7. Planning Tray scope

`Da collocare` Activity is in scope.

Desktop Planning Tray:

- anchored popover near trigger.

Mobile:

- bottom sheet.

Supported operations:

- search/filter local tray items;
- quick placement;
- carried-card drag placement;
- Escape cancel;
- direct remove with confirmation;
- Undo placement/removal;
- preserve same Activity identity across placement.

No backend inbox/backlog persistence is implied.

## 8. All-day scope

All-day uses a real per-day lane whose height participates in Timeline geometry.

It is NOT represented as:

- a global detached header strip;
- a fake 00:00–24:00 timed card.

Multi-day Event continuation is allowed across covered date lanes.

## 9. Advanced disclosure scope

The product-visible Quick/Expanded/Full model is superseded.

User-visible Create has:

- base mode;
- `Opzioni avanzate`.

Advanced sections are type/capability conditional. No dead deferred-owner panels.

## 10. Reminder/alarm stop line

The user expects a future Reminder/Alarm type, but C1 must not claim delivery without a truthful runtime.

Before exposing the type, resolve:

- canonical owner/intent;
- whether local frontend can author reminder intent independently;
- future delivery owner/provider;
- copy that distinguishes authored intent from active OS/provider notification.

Real alarm/push delivery remains outside C1.

## 11. Backend/external stop line

Not authorized in C1:

- API transport;
- PostgreSQL application writes;
- canonical server identity allocation;
- durable server idempotency;
- runtime product Auth/ACL;
- provider sync/writes;
- invitations;
- room booking;
- conference creation;
- notification/alarm delivery;
- solver/autoscheduling authority;
- recurrence evaluation/checkpoints;
- canonical Occurrence generation;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI/NL/voice input/runtime.

## 12. Gate

C1 is not eligible for closure while re-architecture code or tests are incomplete.

Required before manual retest:

1. full implementation of this scope;
2. Quality PASS;
3. Mobile PASS;
4. Chromium full E2E PASS;
5. Firefox frozen Timeline PASS;
6. Frontend CI Gate PASS;
7. documentation reconciliation to exact candidate;
8. rewritten manual acceptance.

Only explicit `C1 MANUAL PASS — APPROVED` after that new protocol can freeze/close C1.
