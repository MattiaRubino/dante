# DANTE — Temporal Create C1 Manual Findings — 2026-09-03

**Status:** AUTHORITATIVE MANUAL FAIL FINDINGS  
**Date:** 2026-09-03  
**Branch:** `feature/home-timeline`  
**Result:** `C1 MANUAL FAIL` — re-architecture required before any new acceptance pass

## Purpose

This record captures the product defects found by the user after the old C1 automated green candidate. These findings are not optional polish requests; they define the re-architecture acceptance target.

## Findings

1. **Header expansion control was misleading.** A `+` beside close `×` looked like another create action. Remove it.
2. **Progressive disclosure felt like different products.** Quick/Expanded/Full changed too much structure. User-facing model must become one coherent Create plus `Opzioni avanzate`.
3. **Title/type hierarchy was wrong.** Title first, then an extensible type chooser. Context appears after type and normal fields appear immediately.
4. **No wizard tax.** Selecting Activity/Event must expose the common usable configuration immediately. Changing `Tutto il giorno`/`Da collocare` changes only dependent controls.
5. **All-day presentation was wrong.** Global header strip looked detached. Required: real per-day all-day lane/card geometry above minute zero, not a 24-hour timed card.
6. **Planning Tray placement was wrong.** Desktop tray must be anchored near its trigger, not a far-right detached drawer.
7. **Planning drag felt like a clone/ghost.** User must feel the actual tray card being grabbed and carried into the Timeline; tray recedes, Timeline foregrounds, target slot appears, drop places the same Activity.
8. **Tray `...` was pointless when it only meant delete.** Use direct remove `×`/trash with confirmation.
9. **Execution/session semantics affected placement incorrectly.** An Activity deliberately placed at an hour must remain placed even when configured as splittable/multi-session.
10. **Dead/deferred owner UI is unacceptable.** Do not show blocks such as `Routine — Richiede il verticale proprietario` in normal Create. Hide unavailable types/capabilities until genuinely actionable.
11. **Reminder/alarm use case is missing.** Do not fake it; design a truthful owner/runtime boundary before exposing a tile or claiming delivery.
12. **Daily recurring Event must be fast.** Common recurrence choices should be available directly; deep CP6 custom recurrence remains behind `Personalizza…`.
13. **Event internal parts are needed.** Example `Lezione inglese → Listening / Orale / Scritto`. Use Event Agenda/internal parts unless independent identity/time/state is actually required.
14. **The main Create must be intent-driven.** Show the right controls for the selected type and nested choice; irrelevant controls should not remain visible/disabled.
15. **Advanced depth remains valuable.** Do not delete DANTE's semantic richness. Put it behind a well-organized Advanced path containing only capabilities relevant to the selected type.

## Agreed replacement IA

```text
Titolo
↓
Tipo (extensible registry/grid)
↓
selected-type sensible default fields
↓
Context + relevant common fields
↓
conditional nested choices
↓
Opzioni avanzate
```

Activity base:

```text
[ Orario ✓ ] [ Tutto il giorno ] [ Da collocare ]
Data | Ora | Durata
Context
```

Event base:

```text
[ Orario ✓ ] [ Tutto il giorno ]
Data | Inizio | Fine
Context | Luogo
Ripeti: Mai / Ogni giorno / Ogni settimana / Ogni mese / Ogni anno / Personalizza…
```

## Acceptance consequence

All older manual-acceptance instructions based on the pre-refactor Quick/Expanded/Full UI are superseded.

Do not mark C1 closed until:

1. this re-architecture is implemented;
2. full automated frontend CI is green;
3. a new manual acceptance protocol is written for the new IA;
4. the user explicitly approves it with `C1 MANUAL PASS — APPROVED`.
