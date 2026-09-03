# DANTE — Temporal Create C1 Re-architecture Authority

**Status:** ACTIVE — C1 MANUAL FAIL RECORDED / RE-ARCHITECTURE IN PROGRESS  
**Date:** 2026-09-03  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Current implementation checkpoint at time of this record:** `bd9bc6db13301763393c5345685dd38a1837aaaa`  
**Current checkpoint CI:** Frontend CI `33744558905` / #759 — Quality PASS, Mobile PASS, Chromium 83/96 PASS with 13 stale-C1-contract failures, Firefox skipped, Gate FAIL  
**C1:** NOT FROZEN / NOT CLOSED  
**C2:** BLOCKED

## 1. Why this document exists

The previous C1 implementation reached automated full green, but the user's final manual product review on 2026-09-03 correctly rejected the Create experience as not yet high-level, fast or coherent enough.

Therefore the old automated candidates remain useful historical evidence, but they are not the current product target:

- `2b910092ecd70de74338427924666a965938ba9f` — pre-refactor code/test candidate, Frontend CI #676 FULL GREEN;
- `27dd5093d21b0a49c8413068aacca139fb2366a4` — pre-refactor documentation descendant, Frontend CI #680 FULL GREEN.

Those commits proved the old contract. The manual review proved that the old contract itself needed product-level re-architecture.

This document is now the authority for the C1 re-architecture until a later explicitly CI-green candidate supersedes it.

## 2. Permanent semantic boundaries that do NOT change

The re-architecture is a UX/application-authoring correction, not a license to rewrite the closed DANTE model.

Permanent rules:

```text
Activity != Event
Activity != Routine
Schedule != Occurrence != Session != Actual
planned/intended != happened
recurrence specification != generated Occurrence
Context/group membership != appearance override
provider intent != provider execution
frontend projection id != canonical backend id
ViewModel != application model != DTO != DB row
manual Create != DANTE/AI/NL/voice input
```

Activity recurrence remains forbidden. Persistent repeated Activity intent belongs to:

```text
Routine → Routine Recurrence → Occurrences
```

Repeated Event intent belongs to Event recurrence.

CP6 recurrence families remain exactly:

- `calendar_wall_clock`;
- `elapsed_interval`;
- `quota_per_period`;
- `cyclic_positional`.

The browser authors recurrence specifications only. It does not generate canonical Occurrences.

## 3. Product diagnosis from the manual fail

The failed C1 exposed too much of DANTE's internal semantic depth directly as interface structure.

The rejected direction was effectively:

```text
domain/application capabilities
→ expose many sections
→ disable/defer what is not owned
→ ask the user to understand the model
```

The replacement product rule is:

```text
USER INTENT
→ SENSIBLE DEFAULT
→ ONLY RELEVANT CONTROLS
→ CONDITIONAL PROGRESSIVE DISCLOSURE
→ ADVANCED DEPTH ON DEMAND
→ DEEP DANTE SEMANTICS UNDERNEATH
```

The user must never need to understand an ontology just to create a normal Activity or Event.

## 4. Manual findings that are now binding requirements

### 4.1 Create header

Rejected: a `+` beside the close `×`. It visually reads as another add action.

Required:

```text
BOZZA
Aggiungi                                              ×
```

No expansion icon beside `×`.

### 4.2 Title and type order

Required order:

1. Title;
2. extensible type chooser;
3. fields for the selected type;
4. Context and relevant common fields;
5. Advanced options on demand.

Do not lead with “Cosa vuoi aggiungere?” as a redundant extra step.

### 4.3 Extensible type registry

The type chooser must be structurally extensible (grid/registry/capability-driven), not a collection of scattered `if kind === ...` branches that become impossible to grow.

Only genuinely actionable types may be shown.

At the current C1 checkpoint:

- Activity: actionable;
- Event: actionable;
- Reminder/Alarm: NOT yet exposed until its semantic/runtime boundary is truthful;
- Routine: NOT exposed while its owning vertical is not genuinely actionable from Create.

No disabled/dead tile saying “requires owning vertical”.

### 4.4 No wizard tax

Choosing a type must immediately reveal a usable common case. The user must not perform a chain of clicks just to see normal fields.

Activity default:

```text
Collocazione
[ Orario ✓ ] [ Tutto il giorno ] [ Da collocare ]

Data | Ora | Durata
Context
```

Event default:

```text
Quando
[ Orario ✓ ] [ Tutto il giorno ]

Data | Inizio | Fine
Context
Luogo
Ripeti: Mai
```

Changing a semantic choice replaces only dependent fields.

Examples:

- Activity `Tutto il giorno` removes irrelevant hour controls;
- Activity `Da collocare` removes date/time placement and keeps expected duration + Context;
- Event `Tutto il giorno` uses date-span controls rather than start/end clock time;
- selecting an advanced execution mode reveals only execution fields that become relevant.

### 4.5 Advanced mode

The old user-visible Quick → Expanded → Full mental model is retired.

The user-facing model is:

```text
normal Create
+
Opzioni avanzate
```

Implementation may retain internal presentation states where useful, but the product must feel like one coherent editor.

Advanced mode contains only relevant capabilities for the selected type.

It must not show dead/deferred owner blocks.

### 4.6 Activity placement is authoritative

Execution/session configuration must never silently rewrite the user's placement choice.

Required invariant:

```text
Orario + Divisibile → remains placed at the authored time
Tutto il giorno + execution details → remains all-day
Da collocare → remains unplaced until user places it
```

Session semantics describe execution structure; they do not decide whether an Activity belongs in the Planning Tray.

### 4.7 Planning Tray v2

Desktop:

- anchored to its Timeline trigger;
- appears under/near the trigger;
- not a detached right-side workspace.

Mobile:

- bounded bottom sheet.

Card action:

- direct `×`/remove action;
- confirmation before destructive removal;
- do not use `...` when there is no meaningful menu.

Drag interaction:

```text
grab actual tray card
→ tray recedes/hides
→ carried card follows pointer
→ Timeline becomes foreground destination
→ snapped target slot appears
→ drop applies placement to SAME Activity identity
```

`Esc` cancels with zero mutation.

Undo after placement returns the same Activity to the tray.

### 4.8 All-day v2

Rejected: a floating/static strip in the global Timeline header.

Rejected: a fake timed card spanning 00:00–24:00.

Required: a real per-day all-day lane in each Timeline day's geometry.

```text
DAY LABEL / ALL-DAY LANE
[ all-day card / continuation ]
-------------------------------
minute zero begins here
00:00
01:00
...
```

All-day lane height must consume real vertical space so that:

- minute mapping starts below it;
- Now line stays mathematically correct;
- scroll anchors remain correct;
- zoom remains correct;
- drag/drop minute resolution remains correct;
- multi-day all-day Event can continue across covered days without pretending continuous 24-hour clock occupation.

### 4.9 Event recurrence quick path

Common recurrence must be fast:

- Mai;
- Ogni giorno;
- Ogni settimana;
- Ogni mese;
- Ogni anno;
- Personalizza…

`Personalizza…` reveals the existing CP6-deep recurrence grammar.

The common case `Evento che si ripete ogni giorno` must not require entering the deep recurrence editor.

### 4.10 Event internal structure / Agenda

An Event may need internal agenda parts, e.g.:

```text
Lezione inglese
- Listening
- Orale
- Scritto
```

C1 should author these as Event-internal agenda items/parts unless a part needs independent identity, independent time, independent state or independent Actual semantics.

Do not invent a universal generic sub-entity.

Timeline already has a native `subitems` presentation path; integration must remain semantically explicit rather than blindly mapping every text line to a new Domain object.

### 4.11 Reminder / alarm

The user reasonably expects `Promemoria` / alarm-like authoring eventually.

Do not expose a fake product promise.

Until a truthful owner/application boundary is established, C1 must not claim:

- an OS alarm will ring;
- a push notification will be delivered;
- a provider notification has been scheduled.

A future pre-backend UI may author reminder intent only if copy clearly states that delivery/runtime is not active.

## 5. Reference-product conclusions

The re-architecture was compared against mature patterns from Google Calendar, Notion Calendar, Todoist, Sunsama, Akiflow and Motion.

DANTE intentionally combines lessons rather than copying one product:

```text
Google Calendar → temporal immediacy / all-day / quick recurrence
Notion Calendar → type-aware disclosure
Todoist → unplaced work has a home
Sunsama → task-to-calendar timeboxing / work sessions
Akiflow → fast default + depth when requested
Motion → task/event distinction + execution structure
DANTE → stricter semantic truth underneath all of the above
```

## 6. Implementation checkpoints already on branch

Starting from the old docs descendant `27dd5093...`, the active re-architecture chain includes:

- `0e21164355b39d76d27b2192cb5d510e77e765f8` — `refactor(create): introduce type-driven base flow`;
- `0d863a3765c88ded440bae45ab6a1d1e6d1257c2` — preserve exact advanced Activity duration;
- `586105ca46cd8f3b5f7fbeb663892032c9eb37f0` — conditional execution options;
- `757a5d198353544cac4568f7804e2c39e1d86ea5` — quick Event recurrence;
- `788deee039324631575e52f871ad476a0e9165a9` — anchored Planning Tray;
- `a0cf00ef5507ff6eab4b00d5b97749e7d8d19aa2` — carried-card planning drag;
- `8413f2f0a2c7c6a2b82b6c06216039977cef437b` — direct remove action;
- `2ec74d25f57e8b749273e0baf10e3f3d2eaa57f7` — explicit placement + split-execution regression test;
- `833e59a8df8063bdcfb359c8b70250619cc74e7a` — all-day lane geometry model;
- `87aa3925fe6e275d230781e8f32a95953149a4bb` — prepare per-day all-day lane;
- `bd9bc6db13301763393c5345685dd38a1837aaaa` — integrate all-day lane geometry into Timeline viewport runtime.

## 7. Exact code state at `bd9bc6d...`

### Implemented

- header no longer exposes expansion `+` beside close;
- title-first base flow;
- extensible type registry with actionable Activity/Event only;
- Activity sensible default fields;
- Event sensible default fields;
- base + Advanced user-facing disclosure;
- quick Event recurrence;
- conditional Activity execution fields;
- placement no longer derived from session structure;
- Planning Tray desktop anchor;
- mobile Planning Tray bottom sheet contract retained;
- carried-card drag interaction;
- direct remove `×` with confirmation;
- per-day all-day lane geometry model and offset mapper integrated into rendered Timeline days.

### Intentionally incomplete at this checkpoint

1. The new `TimelineAllDayLane` visual component exists but is not yet mounted into every rendered day.
2. `timeline-all-day-layer.css` still contains transitional old strip selectors and needs lane/card CSS.
3. Transitional old header-layer implementation remains in `timeline-all-day-layer.tsx` and must be removed once per-day lane mounting is complete.
4. C1 Playwright tests still mostly assert the old Quick/Expanded/Full/type-select contract.
5. Event Agenda/subitem authoring is not yet complete.
6. Reminder/alarm owner boundary has not yet been resolved; no tile should be added just for visual completeness.
7. Final documentation/manual acceptance must be rewritten after a new automated full-green candidate exists.

## 8. Current CI truth

Frontend CI #759 / run `33744558905` on `bd9bc6d...`:

- Quality: PASS;
- Mobile Bundle: PASS;
- Chromium Web E2E: FAIL — 83 passed / 13 failed;
- Firefox frozen Timeline: skipped because Chromium failed;
- Frontend CI Gate: FAIL.

The 13 failures are predominantly stale test vocabulary/locators:

- old `Dettagli e pianificazione` button;
- old header `+/-` depth control;
- old `Aperta, senza collocazione` radio wording;
- old `data-temporal-create-surface="quick"` expectation while new product surface reports `base`;
- old `Tipo` select while type is now a tile/grid interaction;
- old Full/mobile progression.

This does NOT authorize deleting those tests. They must be rewritten to protect the new contract.

Normal Timeline controls/hardening/interactions that ran after the C1 failures passed in Chromium, providing useful evidence that the all-day geometry changes have not broadly regressed T1 so far.

## 9. Next implementation sequence

Do not start with documentation cosmetics or C2.

Recommended order:

1. finish per-day all-day lane mount;
2. finish all-day CSS and remove transitional header-layer code;
3. rewrite C1 E2E to the new IA;
4. add explicit regression for `Orario + Divisibile → stays placed`;
5. prove anchored Planning Tray / carried-card drag / direct remove / Escape / Undo;
6. prove quick Event recurrence and deep custom CP6 round-trip;
7. implement Event Agenda/parts with explicit internal semantics;
8. decide Reminder only after semantic owner review;
9. full Quality + Mobile + Chromium + Firefox frozen + Gate;
10. reconcile docs again to the new candidate;
11. run one coherent user manual acceptance;
12. only explicit `C1 MANUAL PASS — APPROVED` can freeze C1.

## 10. Backend stop line

Still outside C1:

- real API transport;
- PostgreSQL application writes;
- canonical server IDs;
- durable server idempotency;
- product Auth/ACL enforcement;
- invitation/room/conference/provider writes;
- actual notification/alarm delivery;
- authoritative solver;
- recurrence evaluator/checkpoints;
- canonical Occurrence generation;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI/NL/voice runtime.

## 11. Closure rule

Current state:

```text
C1 MANUAL FAIL RECORDED
C1 RE-ARCHITECTURE ACTIVE
CURRENT CHECKPOINT AUTOMATED PARTIAL PASS
NOT FROZEN / CLOSED
C2 BLOCKED
```

Do not use the old `C1 MANUAL PASS — APPROVED` protocol until a new full-green re-architecture candidate and a rewritten manual acceptance document exist.
