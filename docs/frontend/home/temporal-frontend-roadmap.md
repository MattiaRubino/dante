# DANTE — Temporal Frontend Production-Depth Roadmap

**Status:** ACTIVE AUTHORITY — C1 RE-ARCHITECTURE IN PROGRESS / C2 BLOCKED  
**Original roadmap:** 2026-08-31  
**Reconciled:** 2026-09-03  
**Workstream owner:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Frozen H0 base:** `98b486a308961022ba0d8f43bb79339518457741`  
**F0 closed:** `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`  
**Current C1 code checkpoint:** `bd9bc6db13301763393c5345685dd38a1837aaaa`  
**Current checkpoint CI:** #759 / `33744558905` — Quality PASS, Mobile PASS, Chromium 83/96 with 13 stale-contract failures, Firefox skipped, Gate FAIL  
**Scope stop:** maximum production-depth frontend capability before real backend/API/provider/solver/Occurrence/runtime integration

## 1. Authority

This roadmap governs the isolated Temporal/Timeline frontend workstream.

Current C1 product authority is:

- `temporal-create-c1-rearchitecture-2026-09-03.md`;
- `temporal-create-c1-manual-findings-2026-09-03.md`;
- `temporal-live-status.md`;
- `temporal-create-handoff.md`.

The pre-refactor C1 full-green candidates remain historical evidence only.

## 2. Frozen foundations

### H0 — CLOSED/FROZEN

Whole Home macro structure and breakpoints.

### T1 — CLOSED/FROZEN

Timeline continuous viewport, semantic anchoring, Now, custom drag/focus, time edit, Undo and frozen Firefox interactions.

### F0 — CLOSED/FROZEN

Typed temporal application foundation, deterministic local adapter, idempotency/revision/Undo/Clock/placement semantics.

These are dependencies of C1, not targets to redesign while fixing Create UX.

## 3. C1 — Manual Temporal Create

### Current gate

```text
C1 MANUAL FAIL RECORDED
RE-ARCHITECTURE ACTIVE
NOT FROZEN / CLOSED
```

The old C1 reached full automated green but failed the final human product test. The roadmap therefore keeps C1 open until the new intent-driven Create is both automated-green and manually accepted.

### C1 permanent boundaries

- manual input only;
- Activity/Event semantic truth;
- no Activity recurrence;
- Event custom recurrence maps all four CP6 families;
- no browser canonical Occurrence generation;
- no fake backend/provider/notification execution;
- Context != appearance;
- Schedule != Session != Actual;
- user placement choice != execution/session structure.

### C1 re-architecture objective

```text
user intent
→ sensible default
→ only relevant controls
→ conditional disclosure
→ Advanced depth on demand
→ DANTE semantic/application rigor underneath
```

### C1-R1 — Type-driven base Create

Status: IMPLEMENTED CHECKPOINT / TEST MIGRATION PENDING.

- title first;
- extensible type grid/registry;
- only actionable Activity/Event types shown;
- normal fields immediately visible;
- no dead owner tiles.

Primary checkpoint: `0e211643...` and descendants.

### C1-R2 — Coherent Base + Advanced disclosure

Status: IMPLEMENTED CHECKPOINT / TEST MIGRATION PENDING.

- retire user-visible Quick/Expanded/Full mental model;
- one Create editor;
- `Opzioni avanzate` for deeper relevant capabilities;
- conditional execution fields.

Primary checkpoint: `586105ca...` and descendants.

### C1-R3 — Activity placement truth

Status: IMPLEMENTED LOGIC / BLOCKING E2E REQUIRED.

- Orario;
- Tutto il giorno;
- Da collocare;
- execution/session structure cannot silently change placement.

Required proof:

`Orario + Divisibile → remains placed`.

### C1-R4 — Event quick recurrence

Status: IMPLEMENTED / E2E MIGRATION REQUIRED.

Quick choices:

- never;
- daily;
- weekly;
- monthly;
- yearly;
- custom.

Custom retains full CP6 deep grammar.

Checkpoint: `757a5d19...`.

### C1-R5 — Planning Tray v2

Status: IMPLEMENTED CHECKPOINT / E2E MIGRATION REQUIRED.

- anchored desktop popover;
- mobile bottom sheet;
- carried-card drag;
- direct remove;
- same identity placement;
- Escape/Undo correctness.

Checkpoints:

- `788deee0...`;
- `a0cf00ef...`;
- `8413f2f0...`.

### C1-R6 — All-day lane v2

Status: IN PROGRESS.

Geometry foundation:

- per-day lane height;
- offset time mapper;
- rendered-day height/offset recalculation.

Current checkpoint: `bd9bc6db...`.

Remaining:

- mount `TimelineAllDayLane` visually per day;
- final lane/card CSS;
- remove transitional old header strip implementation;
- blocking viewport/Now/drag/zoom/all-day E2E.

### C1-R7 — Event Agenda/internal parts

Status: NOT YET COMPLETE.

Need structured Event-internal agenda authoring without inventing generic nested domain entities.

Example:

```text
Lezione inglese
- Listening
- Orale
- Scritto
```

Use native Timeline subitem presentation only with explicit semantic mapping.

### C1-R8 — Reminder/Alarm feasibility

Status: SEMANTIC REVIEW REQUIRED.

Do not expose until the frontend can author truthful reminder intent without claiming notification/device delivery.

Real alarm/push delivery is outside C1.

### C1-R9 — Automated contract migration

Status: BLOCKING.

CI #759 has 13 C1 failures because old tests assert removed controls/vocabulary.

Rewrite coverage for:

- base/Advanced;
- type grid;
- new placement controls;
- conditional fields;
- Planning Tray v2;
- all-day lane v2;
- quick recurrence;
- Orario + Divisibile;
- Agenda;
- mobile.

Never revert product IA simply to satisfy stale tests.

### C1-R10 — New full green

Required:

- Quality PASS;
- Mobile PASS;
- Chromium full PASS;
- Firefox frozen PASS;
- Frontend CI Gate PASS.

### C1-R11 — New manual acceptance

Only after C1-R10.

Manual test should judge:

- obviousness;
- speed;
- relevance of visible fields;
- quality of disclosure;
- all-day feel;
- Planning Tray drag feel;
- recurrence usability;
- Agenda usability;
- mobile;
- frozen Timeline regression feel.

Explicit token required:

`C1 MANUAL PASS — APPROVED`

Only then:

```text
C1 TEMPORAL CREATE → FROZEN / CLOSED
```

## 4. C2 — Card → Structured Detail

**BLOCKED until C1 is explicitly closed.**

Do not start C2 opportunistically while C1 remains red or manually unaccepted.

Once unblocked, C2 must consume the frozen C1/F0/T1 contracts rather than reinterpret them.

## 5. Later temporal roadmap

After C1/C2, future verticals may include richer detail/edit, Routine-specific authoring, Reminder/notification runtime, backend temporal adapter, provider integration, recurrence materialization, Session/Actual runtime and DANTE intelligence inputs.

Each must preserve owner and temporal non-collapse rules.

## 6. Backend stop line for current frontend roadmap

Not part of C1 implementation:

- real API transport;
- PostgreSQL writes;
- canonical server identity allocation;
- server durable idempotency;
- runtime Auth/ACL;
- provider writes/sync/invitations/booking/conferencing;
- real notification delivery;
- authoritative scheduling solver;
- recurrence evaluator/checkpoints;
- canonical Occurrence generation;
- Session/Actual runtime;
- multi-device reconciliation;
- AI/NL/voice runtime.

## 7. Current next action

Resume C1-R6 first: finish all-day per-day visual lane on the already integrated geometry. Then migrate the stale C1 tests and continue through Agenda/full CI. Do not ask the user to retest before a new full-green candidate exists.
