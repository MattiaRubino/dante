# DANTE — Temporal Workstream Live Status

**Status:** C1 MANUAL FAIL RECORDED — RE-ARCHITECTURE ACTIVE  
**Date:** 2026-09-03  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Current code checkpoint:** `bd9bc6db13301763393c5345685dd38a1837aaaa`  
**Checkpoint CI:** Frontend CI `33744558905` / #759 — Quality PASS, Mobile PASS, Chromium 83/96 with 13 stale-contract failures, Firefox skipped, Gate FAIL  
**C1:** NOT FROZEN / NOT CLOSED  
**C2:** BLOCKED

## Live authority

This file is the current operational status for Timeline / Temporal Create C1.

Read in this order:

1. `temporal-create-c1-rearchitecture-2026-09-03.md` — current product/engineering authority;
2. `temporal-create-c1-manual-findings-2026-09-03.md` — binding user findings that reopened C1;
3. `temporal-create-handoff.md` — exact restart instructions;
4. `temporal-create-c1-scope-amendment.md` — current C1 scope/stop line;
5. `temporal-create-c1-traceability.md` — requirement → implementation/test mapping;
6. `temporal-frontend-roadmap.md` — sequence and C2 gate;
7. `temporal-f0-contract.md` and `timeline-t1-frozen-contract.md` — frozen foundations.

The old `temporal-create-c1-final-validation.md`, 2026-09-02 manual acceptance and pre-refactor engineering checkpoint are historical evidence only. They must not be used as current closure authority.

## Historical pre-refactor evidence

The old Create contract had strong automated evidence:

- code/harness candidate `2b910092ecd70de74338427924666a965938ba9f`;
- Frontend CI #676 / `33660540265` — FULL GREEN;
- docs descendant `27dd5093d21b0a49c8413068aacca139fb2366a4`;
- Frontend CI #680 / `33665329466` — FULL GREEN.

The user then executed the real manual product pass and rejected the UX. Therefore these green runs are historical regression evidence, not proof that current C1 is acceptable.

## Stable foundations — do not casually reopen

- H0 Whole Home structure and breakpoints;
- T1/T1-A/T1-B Timeline interaction/navigation/continuous window;
- F0 temporal application contract at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- closed Domain and Logical model;
- accepted Physical model;
- CP6 materialized PostgreSQL / Alembic head `20260826_08`;
- `Activity != Event != Routine`;
- `Schedule != Occurrence != Session != Actual`;
- `planned/intended != happened`;
- `recurrence specification != generated Occurrence`;
- `Context/group membership != appearance override`;
- `ViewModel != application model != DTO != DB row`;
- no fake backend/provider/AI/voice success.

Database authority remains PostgreSQL 18.6, CP6 CLOSED, 68 DANTE tables, 5 views, 14 routines, 75 trigger attachments, 95 indexes, 68 FKs and 120 CHECK constraints.

Recurrence authority remains M4/M6:

- recurrence owners: Routine and Event only;
- families: `calendar_wall_clock`, `elapsed_interval`, `quota_per_period`, `cyclic_positional`;
- no Activity recurrence;
- repeated Activities go through Routine;
- backend owns canonical Occurrence generation.

## Permanent C1 input contract — manual only

Timeline Create remains a manual authoring path.

It is NOT:

- chat;
- AI command bar;
- natural-language parser;
- voice input;
- a generic DANTE interpretation surface.

`TemporalCreateFieldSeed` is deterministic manual prefill only. Future AI/DANTE/voice verticals may reuse compatible downstream application/domain/backend operations when justified, but they must not be coupled to the C1 form/session/seed contract.

## Current product direction

The previous UI exposed too much model complexity directly. The new rule is:

```text
user intent
→ sensible default
→ only relevant controls
→ conditional progressive disclosure
→ advanced depth on demand
→ deep DANTE semantics underneath
```

### Create structure

```text
BOZZA / Aggiungi / ×

Titolo
↓
Tipo registry/grid
↓
selected-type base configuration
↓
Context + relevant common fields
↓
conditional branches
↓
Opzioni avanzate
```

No `+` beside close. No user-visible Quick/Expanded/Full mental model.

### Type availability

Currently expose only genuinely creatable types:

- Activity;
- Event.

Do not expose Routine as a dead owner tile. Do not expose Reminder/Alarm until a truthful semantic/runtime boundary exists.

### Activity base

Default:

```text
[ Orario ✓ ] [ Tutto il giorno ] [ Da collocare ]
Data | Ora | Durata
Context
```

Changing placement changes only dependent controls.

Execution/session structure never silently changes placement.

### Event base

Default:

```text
[ Orario ✓ ] [ Tutto il giorno ]
Data | Inizio | Fine
Context
Luogo
Ripeti
```

Quick recurrence:

- Mai;
- Ogni giorno;
- Ogni settimana;
- Ogni mese;
- Ogni anno;
- Personalizza…

`Personalizza…` reveals the existing CP6-deep Event recurrence authoring.

### Advanced

Advanced shows only relevant capabilities. No dead/deferred owner blocks.

For Activity, multi-session controls appear only when execution is `Divisibile`.

## Planning Tray v2

Required/current direction:

- desktop popover anchored under/near trigger;
- mobile bottom sheet;
- direct `×` remove with confirmation;
- carried-card drag rather than detached clone feeling;
- tray recedes during drag;
- Timeline foregrounds;
- snapped target slot appears;
- drop mutates placement of the SAME Activity;
- Escape cancels with zero mutation;
- Undo placement returns same Activity to tray.

## All-day v2

The old global header strip is rejected.

Correct model:

- per-day all-day lane;
- real lane height in day geometry;
- minute zero begins below lane;
- all-day card/bar lives in lane;
- multi-day continuation across covered days;
- never fake 00:00–24:00 timed occupation.

Current code already has per-day geometry/mapper support, but the visual lane still needs final mounting/CSS cleanup.

## Current re-architecture commit chain

From the pre-refactor docs baseline:

- `0e21164355b39d76d27b2192cb5d510e77e765f8` — type-driven base flow;
- `0d863a3765c88ded440bae45ab6a1d1e6d1257c2` — exact advanced Activity duration;
- `586105ca46cd8f3b5f7fbeb663892032c9eb37f0` — conditional execution options;
- `757a5d198353544cac4568f7804e2c39e1d86ea5` — quick Event recurrence;
- `788deee039324631575e52f871ad476a0e9165a9` — anchored Planning Tray;
- `a0cf00ef5507ff6eab4b00d5b97749e7d8d19aa2` — carried-card planning drag;
- `8413f2f0a2c7c6a2b82b6c06216039977cef437b` — direct remove action;
- `2ec74d25f57e8b749273e0baf10e3f3d2eaa57f7` — Orario + split-execution regression groundwork;
- `833e59a8df8063bdcfb359c8b70250619cc74e7a` — per-day all-day geometry model;
- `87aa3925fe6e275d230781e8f32a95953149a4bb` — per-day all-day lane preparation;
- `bd9bc6db13301763393c5345685dd38a1837aaaa` — all-day geometry integrated into Timeline runtime.

## CI truth at current code checkpoint

Frontend CI #759 / run `33744558905`:

- Quality PASS;
- Mobile Bundle PASS;
- Chromium: 83/96 PASS, 13 failures;
- Firefox frozen skipped after Chromium failure;
- Gate FAIL.

The 13 Chromium failures are principally stale pre-refactor C1 test assumptions: old `Dettagli e pianificazione`, old `+/-` depth, old `Aperta, senza collocazione`, old `quick` surface name, old Type select, and old Full progression.

Do not weaken/delete those tests. Rewrite them to protect the new IA.

All normal Timeline control/hardening/interaction tests that ran after the C1 failures passed in Chromium.

## Exact next work

1. mount `TimelineAllDayLane` per rendered Timeline day;
2. finish lane/card CSS;
3. remove transitional old header-layer code;
4. rewrite C1 E2E for base + Advanced/type-grid/new placement vocabulary;
5. harden Planning Tray v2 E2E;
6. explicit `Orario + Divisibile → remains placed` E2E;
7. quick Event recurrence + CP6 custom round-trip E2E;
8. implement Event Agenda/internal parts;
9. decide Reminder/Alarm only after semantic owner review;
10. full Quality + Mobile + Chromium + Firefox frozen + Gate;
11. reconcile docs to new green candidate;
12. one new coherent user manual acceptance.

## Backend/external stop line

Outside C1:

- real API transport;
- PostgreSQL application writes;
- canonical server IDs;
- durable server idempotency;
- product Auth/ACL enforcement;
- provider writes/sync/invitations/room booking/conference creation;
- real notification/alarm delivery;
- authoritative solver;
- recurrence evaluator/checkpoints;
- canonical Occurrence generation;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI/NL/voice runtime/input.

## Closure gate

Current state:

```text
C1 MANUAL FAIL RECORDED
C1 RE-ARCHITECTURE ACTIVE
AUTOMATED PARTIAL PASS AT CURRENT CHECKPOINT
USER RETEST NOT YET AUTHORIZED
NOT FROZEN / CLOSED
C2 BLOCKED
```

Only after a new full-green candidate and a rewritten manual acceptance may the user approve with:

`C1 MANUAL PASS — APPROVED`

Only then may C1 transition to FROZEN / CLOSED and C2 begin.
