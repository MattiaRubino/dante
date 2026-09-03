# DANTE — Temporal Create C1 Manual Acceptance

**Status:** BLOCKED / SUPERSEDED — DO NOT EXECUTE THE 2026-09-02 PRE-REFACTOR PROTOCOL  
**Date reconciled:** 2026-09-03  
**Branch:** `feature/home-timeline`  
**C1:** MANUAL FAIL RECORDED / RE-ARCHITECTURE ACTIVE

## Why this protocol is blocked

The old C1 manual acceptance was written for a UI based on visible Quick → Expanded → Full progression, the old Planning Tray and the old global all-day strip.

The user executed the manual product review and found material issues. The result is authoritative:

```text
C1 MANUAL FAIL
```

The current Create re-architecture intentionally removes/replaces major assumptions from the old protocol:

- no `+` beside the close `×`;
- no user-facing Quick/Expanded/Full mental model;
- title-first + extensible type registry/grid;
- Activity/Event sensible defaults immediately visible;
- conditional fields instead of dead/disabled sections;
- one `Opzioni avanzate` path;
- quick Event recurrence;
- anchored Planning Tray;
- carried-card planning drag;
- direct remove action;
- per-day all-day lane rather than global header strip;
- no visible unavailable-owner clutter.

Running the old protocol now would produce false failures for intentionally removed UI and false PASS confidence for behaviors whose UX contract has changed.

## Current authority

Read:

1. `temporal-live-status.md`;
2. `temporal-create-c1-rearchitecture-2026-09-03.md`;
3. `temporal-create-c1-manual-findings-2026-09-03.md`;
4. `temporal-create-handoff.md`.

## When a new manual acceptance may be written

Only after a post-refactor code candidate passes ALL automated frontend gates:

- Quality;
- Mobile Bundle;
- Chromium full Web E2E;
- Firefox frozen Timeline interaction contract;
- Frontend CI Gate.

The new protocol should be much more user-oriented than the old one. It should validate the questions automation cannot answer:

1. Is it immediately obvious what I am creating?
2. Can I create a normal Activity/Event quickly without wizard friction?
3. Do I see only controls relevant to my current choice?
4. When I choose `Tutto il giorno`, do irrelevant time controls disappear naturally?
5. Does `Da collocare` have an understandable home and drag interaction?
6. Does all-day look like a real calendar-grade per-day lane/card, not a header hack or 24-hour timed block?
7. Can I make common Event recurrence such as daily in one obvious action?
8. Can I access CP6-deep recurrence only when I actually need custom recurrence?
9. Does `Divisibile` reveal session controls without silently unscheduling an Activity?
10. Are Event Agenda/internal parts understandable?
11. Does Advanced feel like depth on demand rather than a DB form?
12. Are Context and appearance still clearly different?
13. Does mobile remain usable?
14. Does normal frozen Timeline interaction still feel unchanged?

## Planned targeted manual scenarios

### Activity normal path

```text
Title
→ Activity
→ default Orario
→ Data/Ora/Durata/Context already visible
→ Add
→ native Timeline card
→ Undo
```

### Activity all-day

```text
Activity
→ Tutto il giorno
→ clock fields disappear
→ create
→ real per-day all-day lane/card
```

### Activity unplaced

```text
Activity
→ Da collocare
→ Duration + Context
→ create
→ anchored Planning Tray
→ quick place / Undo
→ carried-card drag / Escape / drop / Undo
```

### Placement/execution non-collapse

```text
Activity
→ Orario
→ Advanced
→ Divisibile
→ multi-session details
→ Add
```

Expected: it remains placed at the authored time.

### Event normal + recurrence

```text
Title
→ Event
→ default timed fields already visible
→ Ripeti: Ogni giorno
→ Add
```

Then a separate custom recurrence inspection proving `Personalizza…` retains all four CP6 families without generating Occurrences in browser.

### Event Agenda

Once implemented, create an Event with internal parts such as:

- Listening;
- Orale;
- Scritto.

Verify they read as Event-internal agenda/parts, not fake independent Events unless explicitly promoted later.

### Mobile

390×844 equivalent:

- base Create;
- Advanced;
- Planning Tray bottom sheet;
- Event recurrence;
- no horizontal overflow.

### Frozen Timeline smoke

- focus existing card;
- drag/move;
- time edit;
- Undo;
- Ora/Now;
- expansion/group controls.

## Current gate

At the current code checkpoint `bd9bc6db13301763393c5345685dd38a1837aaaa`, CI #759 is NOT full green, so user retest is blocked.

Do not ask the user to execute manual acceptance yet.

## Final approval token

Only after a new full-green candidate and a newly written protocol may the user close C1 with:

```text
C1 MANUAL PASS — APPROVED
```

Until then:

```text
C1 RE-ARCHITECTURE ACTIVE
NOT FROZEN / CLOSED
C2 BLOCKED
```
