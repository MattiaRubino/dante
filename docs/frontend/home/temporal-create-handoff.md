# DANTE — Temporal Create C1 Workstream Handoff

**Status:** ACTIVE RESTART AUTHORITY — C1 MANUAL FAIL / RE-ARCHITECTURE IN PROGRESS  
**Date:** 2026-09-03  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Local worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Current code checkpoint:** `bd9bc6db13301763393c5345685dd38a1837aaaa`  
**Current code checkpoint CI:** Frontend CI #759 / `33744558905` — Quality PASS, Mobile PASS, Chromium 83/96 with 13 stale-contract failures, Firefox skipped, Gate FAIL  
**C1:** NOT CLOSED  
**C2:** BLOCKED

## 1. How to restart this workstream

Do not reinterpret this as a new project or a new Create design exercise.

Read, in order:

1. `docs/frontend/home/temporal-live-status.md`;
2. `docs/frontend/home/temporal-create-c1-rearchitecture-2026-09-03.md`;
3. `docs/frontend/home/temporal-create-c1-manual-findings-2026-09-03.md`;
4. this handoff;
5. `docs/frontend/home/temporal-create-c1-scope-amendment.md`;
6. `docs/frontend/home/temporal-create-c1-traceability.md`;
7. `docs/frontend/home/temporal-frontend-roadmap.md`;
8. `docs/frontend/home/temporal-f0-contract.md`;
9. `docs/frontend/home/timeline-t1-frozen-contract.md`;
10. the current code under `apps/web/src/features/temporal-create/` and `apps/web/src/features/home/ui/timeline/`.

Then fresh-check GitHub/branch before changing code. Do not rely on this SHA if the branch has advanced.

Local sync:

```bash
cd /home/mattia/projects/dante-timeline
git pull --ff-only
git status --short --branch
git rev-parse HEAD
```

Development server:

```bash
pnpm --filter @dante/web dev
```

## 2. Why C1 is open again

The pre-refactor C1 implementation reached automated full green:

- code/harness `2b910092ecd70de74338427924666a965938ba9f` — CI #676 FULL GREEN;
- docs descendant `27dd5093d21b0a49c8413068aacca139fb2366a4` — CI #680 FULL GREEN.

The user then performed the final manual acceptance and found product-level issues that automation could not judge. The manual result is authoritative:

```text
C1 MANUAL FAIL
```

The problem was not that the domain/application semantics were weak. The problem was that too much semantic depth was exposed directly as UI structure, producing a slow, confusing, prototype-like Create experience.

Do not restore the old UI merely because it had green tests.

## 3. Stable global foundations

Do not casually reopen these while fixing Create UX.

### H0

Whole Home structural baseline and responsive breakpoints remain frozen.

Timeline work may not re-author Home macro geometry.

### T1

Frozen Timeline contract includes:

- rolling mounted temporal window;
- semantic viewport anchor;
- continuous navigation;
- Ora/Now;
- custom card focus;
- custom drag;
- first drag must work;
- no native drag ghost;
- move + Undo;
- time editor;
- no no-op mutation;
- reduced-motion contract;
- Firefox critical-interaction regression suite.

### F0

Closed application foundation at:

`7034b9b0d100709785ebe96e3816aab3e7b1d1f8`

Preserve:

- typed identities;
- operation IDs;
- Clock;
- typed placement capabilities;
- immutable drafts;
- commands/results/queries;
- deterministic local adapter;
- optimistic revision checks;
- idempotency fingerprints;
- subscriber isolation;
- Undo as a real inverse mutation, not blind state replacement;
- no fake network/storage.

Permanent distinctions:

```text
ViewModel != application projection != DTO != DB row
date-only != floating local != zoned exact != absolute instant
source/intention != placement
Schedule != Session != Actual
proposal != accepted effect
pending != success
no-op != mutation
retry != duplicate
```

## 4. Domain / DB authority that Create must obey

DANTE is a personal operating system, not a task manager with extra fields.

Core lifecycle:

```text
UNDERSTAND
→ DISCOVER
→ ORCHESTRATE
→ DECIDE
→ PLAN & COORDINATE
→ ACT
→ OBSERVE
→ LEARN & ADAPT
```

Life is the center. Time is foundational but not the container for all life semantics.

Permanent semantic rules:

- `Activity != Event != Routine`;
- planned/intended != happened;
- effort != execution != outcome != Goal progress;
- no universal life score;
- user authority is preserved;
- AI != DANTE;
- native identity != contextual role;
- Observation != Actual;
- Evidence != Provenance;
- Authority != Visibility;
- Responsibility != Participation;
- Ownership != Possession;
- provider identity != canonical DANTE identity;
- UI terminology != ontology.

Current DB authority:

- PostgreSQL 18.6;
- Alembic head `20260826_08`;
- CP6 CLOSED/materialized;
- 68 DANTE tables + `alembic_version`;
- 5 views;
- 14 routines;
- 75 trigger attachments;
- 95 indexes;
- 68 foreign keys;
- 120 CHECK constraints.

15 LR-01 owners:

Person, Living Referent, Asset, Place, Content Artifact, Collective, Possibility, Goal, Plan, Activity, Event, Routine, Occurrence, Session, Observation.

A schema object existing does not automatically authorize a Create operation.

### Recurrence

M4 `20260825_04_cp6_recurrence.py` authorizes recurrence for Routine and Event only.

Families exactly:

- `calendar_wall_clock`;
- `elapsed_interval`;
- `quota_per_period`;
- `cyclic_positional`.

Never reintroduce Activity recurrence.

```text
Repeated Event → Event Recurrence
Repeated Activity → Routine → Routine Recurrence → Occurrences
```

M6 `20260826_06` makes backend authoritative for recurrence-generated Occurrences and their exact governing recurrence state.

C1 authors recurrence specification only.

## 5. Permanent Create input boundary

Timeline `+` is manual authoring only.

It is NOT:

- chat;
- AI command bar;
- natural-language parser;
- voice input;
- “ask DANTE”.

`TemporalCreateFieldSeed` is deterministic manual prefill for known context such as Timeline date/time/range.

Future AI/DANTE/voice input verticals remain separate. They may eventually reuse compatible downstream semantic application/domain/backend operations, but not the C1 form/session/seed contract.

## 6. Binding UX re-architecture

The new product rule is:

```text
USER INTENT
→ SENSIBLE DEFAULT
→ ONLY RELEVANT CONTROLS
→ NESTED CONDITIONAL DISCLOSURE
→ ADVANCED DEPTH ON DEMAND
→ DANTE SEMANTICS UNDER THE HOOD
```

### 6.1 Header

No `+` beside `×`.

Use a simple Create header.

### 6.2 Base hierarchy

```text
Title
↓
Type registry/grid
↓
selected-type sensible base fields
↓
Context + relevant common fields
↓
conditional sub-branches
↓
Opzioni avanzate
```

Do not create a wizard where normal creation requires many clicks.

### 6.3 Type registry

Must be extensible in architecture and layout.

Expose only genuinely actionable types.

Current C1:

- Activity: visible/actionable;
- Event: visible/actionable;
- Routine: hidden until owning vertical is actionable;
- Reminder/Alarm: hidden until truthful owner/delivery boundary is designed.

No disabled “requires owner vertical” clutter.

### 6.4 Activity

Default immediately visible:

```text
[ Orario ✓ ] [ Tutto il giorno ] [ Da collocare ]
Data | Ora | Durata
Context
```

If `Tutto il giorno`, remove irrelevant hour fields.

If `Da collocare`, remove fake date/time placement and keep expected duration + Context.

Execution settings do not decide placement.

Required regression:

```text
Orario + Divisibile → remains a placed Activity in Timeline
```

### 6.5 Event

Default immediately visible:

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

`Personalizza…` opens the full CP6 recurrence authoring.

### 6.6 Advanced

The old user-visible Quick/Expanded/Full model is retired.

Current user-facing model:

```text
Create base
+
Opzioni avanzate
```

Advanced must show only relevant capabilities.

Conditional example:

```text
Esecuzione = Indivisibile
→ hide multi-session controls

Esecuzione = Divisibile
→ reveal min session / max sessions / spacing / related execution options
```

## 7. Planning Tray v2 contract

The tray is the home for Activity that exists but has no accepted exact placement.

Desktop:

- anchored popover under/near the trigger.

Mobile:

- bottom sheet.

Card removal:

- direct `×`/trash;
- explicit confirmation;
- no pointless `...` menu.

Drag:

```text
grab actual card
→ tray visually recedes
→ carried card follows pointer
→ Timeline enters foreground planning mode
→ snapped target slot shown
→ drop applies placement to same Activity
```

No duplicate Activity.

`Esc` cancels without mutation.

Undo after placement returns same Activity to tray.

## 8. All-day v2 contract

The old global header strip is rejected.

Correct behavior is a real per-day lane:

```text
DAY
all-day lane / card bars
-----------------------
minute zero
00:00
01:00
...
```

All-day does not mean a fake 24-hour timed busy block.

The lane consumes real vertical geometry so Time mapper/Now/zoom/drag/anchors remain mathematically correct.

Multi-day Event must continue across covered days.

## 9. Event Agenda / internal parts

Need authoring for internal Event structure such as:

```text
Lezione inglese
- Listening
- Orale
- Scritto
```

Treat these as Event-internal agenda parts unless independent identity/time/state/Actual semantics are needed.

Do not invent a generic universal sub-entity.

`TimelineEvent` already has a `subitems` presentation contract. Connect Agenda to it only with explicit semantics.

## 10. Reminder / alarm decision

The user asked for alarm/reminder creation.

Do not add a cosmetic tile that lies.

Before exposing Reminder, determine:

- canonical owner/intent mapping;
- whether local C1 can author reminder intent without claiming delivery;
- what future backend/provider owns notification delivery;
- copy that distinguishes `intent configured` from `alarm active on device`.

Real delivery remains outside C1.

## 11. Re-architecture commits already landed

- `0e21164355b39d76d27b2192cb5d510e77e765f8` — type-driven base flow;
- `0d863a3765c88ded440bae45ab6a1d1e6d1257c2` — preserve exact advanced Activity duration;
- `586105ca46cd8f3b5f7fbeb663892032c9eb37f0` — conditional execution fields;
- `757a5d198353544cac4568f7804e2c39e1d86ea5` — quick Event recurrence;
- `788deee039324631575e52f871ad476a0e9165a9` — anchored Planning Tray;
- `a0cf00ef5507ff6eab4b00d5b97749e7d8d19aa2` — carried-card drag;
- `8413f2f0a2c7c6a2b82b6c06216039977cef437b` — direct remove action;
- `2ec74d25f57e8b749273e0baf10e3f3d2eaa57f7` — explicit placement + split execution test groundwork;
- `833e59a8df8063bdcfb359c8b70250619cc74e7a` — per-day all-day geometry model;
- `87aa3925fe6e275d230781e8f32a95953149a4bb` — prepare per-day lane;
- `bd9bc6db13301763393c5345685dd38a1837aaaa` — integrate lane geometry into Timeline viewport.

Fresh-check the branch before acting; documentation descendants may exist above this code checkpoint.

## 12. Exact unfinished code at `bd9bc6d...`

### All-day

Files:

- `apps/web/src/features/home/ui/timeline/model/timeline-all-day-layout.ts`;
- `apps/web/src/features/home/ui/timeline/timeline-all-day-runtime.ts`;
- `apps/web/src/features/home/ui/timeline/timeline-all-day-layer.tsx`;
- `apps/web/src/features/home/ui/timeline/timeline-all-day-layer.css`;
- `apps/web/src/features/home/ui/timeline/timeline-surface.tsx`;
- `apps/web/src/features/home/ui/timeline/timeline-day-stream.tsx`.

Current geometry is integrated:

`applyTimelineAllDayGeometry(baseRenderedDays, state.allDayItems, state.filters)` offsets each day's time mapper and height.

But visual completion is still needed:

- `TimelineAllDayLane` exists;
- it is not yet mounted in every rendered day;
- CSS still contains transitional strip selectors;
- old header-layer wrapper remains in `timeline-all-day-layer.tsx` and should be removed after lane mounting.

Preferred implementation: mount one lane per rendered `TimelineDay`, or use a clean per-day portal layer if that yields a smaller safer diff. Do not return to the global header strip.

### E2E

CI #759 showed 13 failing C1 tests because they assert the old UI vocabulary/structure.

Failures include:

- `temporal-create-appearance.spec.ts` waits for old `Dettagli e pianificazione`;
- `temporal-create-manual-hardening.spec.ts` expects old header `+/-` depth control;
- four Planning Tray tests use old `Aperta, senza collocazione` radio;
- base Create test expects `surface=quick`, actual new product surface is `base`;
- advanced Activity test uses old Expanded/Full controls;
- Event deep and recurrence tests use old `Tipo` `<select>`;
- all-day test uses old Type select and old strip contract;
- validation test uses old depth button;
- mobile test uses old Expanded/Full progression.

Do NOT revert new IA to satisfy these tests.

Rewrite them to the new product contract.

## 13. CI state

On `bd9bc6...`:

Frontend CI run `33744558905` / #759:

- Quality PASS;
- Mobile Bundle PASS;
- Chromium 83/96 PASS, 13 C1 failures;
- Firefox frozen skipped;
- Gate FAIL.

The Home bundle in this run was approximately:

- `293.22 kB` raw;
- `95.81 kB` gzip.

Do not optimize by adding async complexity solely to reduce gzip without measured need.

## 14. Exact next sequence

1. finish per-day all-day visual lane;
2. remove old transitional strip/header implementation;
3. update all-day structural/unit tests;
4. rewrite C1 E2E for type grid/base+Advanced/new placement controls;
5. Planning Tray anchored/drag/remove/Undo/Escape tests;
6. `Orario + Divisibile` regression;
7. quick recurrence tests + custom CP6 round-trip;
8. Event Agenda/internal-parts implementation and tests;
9. Reminder semantic review; implement only if truthful;
10. run full CI;
11. require Quality + Mobile + Chromium + Firefox frozen + Gate PASS;
12. reconcile docs to that exact code candidate;
13. write a new concise manual acceptance for the new UX;
14. user manual pass;
15. only then freeze C1 and unblock C2.

## 15. Test discipline

- Never weaken an assertion merely because UI changed; replace it with an assertion for the new intended contract.
- No sleeps/timeouts as product fixes.
- No fake PASS.
- No test deletion without demonstrating the protected behavior is obsolete and replacing coverage where needed.
- Do not treat Quality-only green as C1 green.
- Firefox frozen Timeline must run and pass before closure candidate.
- One coherent manual acceptance after automated green; do not make the user repeatedly micro-test every patch.

## 16. Backend/external stop line

Still outside this frontend vertical:

- API transport;
- PostgreSQL writes;
- canonical backend IDs;
- durable server idempotency;
- product runtime Auth/ACL;
- provider sync/writes;
- invitations;
- room booking;
- conference creation;
- real notification/alarm delivery;
- authoritative scheduling solver;
- recurrence evaluation/checkpoints;
- canonical Occurrence generation;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI/NL/voice runtime.

## 17. Current gate

```text
C1 MANUAL FAIL RECORDED
C1 RE-ARCHITECTURE ACTIVE
CURRENT CODE CHECKPOINT PARTIALLY GREEN
USER RETEST BLOCKED
C1 NOT FROZEN / CLOSED
C2 BLOCKED
```

Do not close C1 until a NEW post-refactor manual pass explicitly says:

`C1 MANUAL PASS — APPROVED`
