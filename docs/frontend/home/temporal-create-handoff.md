# DANTE — Temporal Create Workstream Handoff

**Status:** C1 AUTOMATED PASS — PENDING USER MANUAL ACCEPTANCE  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Local worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Final C1 implementation candidate:** `81808814abb4e4998c7bde5b0c6cb8f5f903aa62`  
**Frontend CI:** run `33613239926` / #536 — FULL PASS

## 1. Handoff authority

This is the operational restart document for Timeline / Temporal Create C1.

Read in order:

1. `temporal-live-status.md`;
2. `temporal-create-c1-traceability.md`;
3. `temporal-create-c1-engineering-checkpoint.md`;
4. `temporal-create-c1-manual-acceptance.md`;
5. `temporal-create-c1-scope-amendment.md`;
6. `temporal-frontend-roadmap.md`;
7. `temporal-f0-contract.md`;
8. `timeline-t1-frozen-contract.md`;
9. `temporal-experience-architecture.md`;
10. current code under `apps/web/src/features/temporal-create/` and the Home Timeline bridge.

Older generic Home checkpoint/handoff files are not the live authority for this isolated branch.

## 2. Stable foundations

Do not casually reopen:

- H0 Whole Home structure;
- T1/T1-A/T1-B Timeline interaction and continuous navigation;
- F0 application contract at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- closed Domain / Logical / Physical semantics;
- CP6 materialized database;
- Activity/Event/Routine/Occurrence/Session owner distinctions;
- `Schedule != Session != Actual`;
- `recurrence source != generated Occurrence`;
- `proposal != accepted effect`;
- `ViewModel != application model != DTO != persistence`;
- no fake network/storage/provider/AI/voice behavior.

## 3. Current C1 architecture

```text
ENTRY
  ├─ Timeline +
  ├─ double-click
  ├─ Shift-drag range
  └─ typed semantic invocation/seed
          ↓
SHARED TEMPORAL CREATE SESSION
          ↓
Quick ↔ Expanded ↔ Full
          ↓
normalize → validate → preview
          ↓
explicit commit
          ↓
F0 application command
          ↓
local deterministic adapter NOW
backend adapter LATER
```

Quick/Expanded/Full are views of one draft and one application path.

## 4. Correct owner semantics

### Activity

Activity supports structured planning/execution intent but **does not own recurrence**.

Do not reintroduce:

```text
Activity.repeat
Activity recurrence editor
Activity recurrence capability
```

Persistent repeated Activity intent belongs to:

```text
Routine
→ Routine Recurrence
→ generated Occurrence
→ Activity/runtime semantics as defined downstream
```

Current C1 therefore shows a truthful Routine owning-vertical handoff.

### Event

Event owns recurrence directly and exposes all four CP6 M4 recurrence families:

- calendar wall-clock;
- elapsed interval;
- quota per period;
- cyclic positional.

Full Event authoring includes the current deeper semantic fields for recurrence, purpose, expected outcome, agenda, decision intent, participants, resources, pre-read, conference intent and buffers.

Provider actions remain intent only.

## 5. Current recurrence depth

Preserve these implemented semantics:

### Calendar

- daily;
- weekly + weekday set;
- monthly civil-date anchor;
- monthly ordinal weekday;
- yearly civil-date anchor;
- positive interval;
- open / until-date / count termination.

### Elapsed

- positive elapsed interval;
- backend later owns authoritative evaluator anchoring/checkpoint execution.

### Quota

- quota count;
- day/week/month/year;
- positive period span;
- floating-local / named-zone / absolute-UTC frame;
- week start only for weekly periods;
- IANA zone only for named-zone frame.

### Cyclic

- cycle length;
- day/week unit;
- multiple active positions;
- UI positions are human-friendly 1-based;
- CP6 technical position indexing remains a persistence concern.

No browser-side Occurrence generation is allowed.

## 6. Future-input / DANTE seam

`application/temporal-create-seed.ts` defines a source-neutral structured seed.

`TemporalCreateInvocation` already carries that seed into `TemporalCreateEntry` and therefore into the same session used by manual UI.

Future DANTE architecture must remain:

```text
DANTE interpretation
→ structured seed / unresolved intent
→ same Create normalize/validate/preview path
→ user/governed commit
→ same F0/backend port
```

Never implement DANTE by scripting the form.

No AI runtime exists in C1.

## 7. External owner handoff seam

`application/temporal-create-handoff.ts` is now the typed Create-side contract for external-owned objects.

Targets:

- project;
- goal;
- routine;
- program;
- world;
- template;
- reminder;
- block;
- asset.

All are explicitly `deferred` today.

`prepareTemporalCreateHandoff()` preserves a normalized immutable draft snapshot. It deliberately has no route/href/CRUD/provider effect. When an owning vertical becomes available, it must integrate at this contract rather than duplicating its CRUD inside Timeline Create.

## 8. Application-boundary hardening

### Rich idempotency

F0 protects the minimal projection command. C1 additionally fingerprints rich Create specification by operation ID.

- exact replay remains idempotent;
- same ID + changed rich specification rejects `operation-id-reused`;
- rejection is side-effect free.

### Prepare/execute snapshot ownership

At final implementation candidate `81808814...`, `runtime.prepare()` re-normalizes and freezes its own copy of the specification before validation and command creation.

Do not remove this. It prevents mutable callers/importers/future DANTE adapters from changing rich intent after preparation and producing a command/specification TOCTOU mismatch.

## 9. Timeline integration hardening

The contextual Create E2E must not use a retained `.timeline-day-section.first()` across Timeline virtualization.

The Timeline recycles day-section DOM nodes. The final test:

- finds a currently visible day;
- chooses by stable `data-timeline-date`;
- verifies visible geometry;
- performs double-click/Shift-drag using current viewport coordinates;
- reacquires after the first create/close boundary.

This fixed a real test-locator/virtualization defect without weakening gesture coverage.

T1 drag/focus behavior remains frozen.

## 10. UI / accessibility state

Preserve:

- title-first Quick Create;
- semantic grouping rather than a settings wall;
- exact duration authoring in deeper Activity surfaces;
- separate Event grammar;
- shared section heading/check-grid visual grammar;
- no obsolete one-off `.is-subsection` / `.checkline` CSS debt;
- unambiguous accessible control names;
- named dirty-discard `alertdialog`;
- contained Tab loop;
- exact connected-control focus restoration;
- native `inert` background while confirmation is active;
- mobile Full editor / no horizontal overflow;
- no raw i18n keys.

## 11. CP6 truth to preserve

Current database system of record:

- PostgreSQL 18.6;
- Alembic `20260826_08`;
- CP6 CLOSED;
- 68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs.

Critical migration boundaries:

- M3 `20260825_03` — Schedule / Actual / Session;
- M4 `20260825_04` — recurrence families exactly for Routine and Event;
- M6 `20260826_06` — Occurrence generation and governing recurrence-state binding;
- M7 `20260826_07` — runtime ACL activation;
- `20260826_08` — final forward-only CP6 QA hardening, not an “M8” semantic stage.

Schema existence never authorizes a generic frontend CRUD operation.

## 12. Automated evidence

Final implementation candidate:

`81808814abb4e4998c7bde5b0c6cb8f5f903aa62`

CI `33613239926` / #536:

- Quality PASS;
- Mobile Bundle PASS;
- Chromium full Web E2E PASS;
- Firefox frozen Timeline interaction contract PASS;
- Frontend CI Gate PASS.

Exact current Quality evidence:

- 5/5 typecheck tasks;
- architecture: 199 modules / 477 dependencies / zero violations;
- web unit: 28 files / 168 tests;
- generated-source drift PASS;
- production build PASS;
- diff/mutation checks PASS.

Home route:

`252.22 kB raw / 86.38 kB gzip`.

## 13. Current stop and next transition

C1 is **not** closed yet.

Current state:

```text
IMPLEMENTATION COMPLETE
AUTOMATED PASS
DOCUMENTATION / TRACEABILITY ALIGNED
USER MANUAL ACCEPTANCE PENDING
```

Once the docs-only descendant is CI-green:

1. user syncs `feature/home-timeline` locally;
2. user executes the single manual acceptance protocol;
3. defect -> reopen only demonstrated defect + necessary adjacent contract;
4. explicit `C1 MANUAL PASS — APPROVED` -> freeze C1;
5. then and only then start C2 Card → structured Detail.

## 14. Permanent stop line

Do not implement in C1:

- API or PostgreSQL writes;
- server canonical IDs/idempotency;
- Auth/ACL product enforcement;
- provider sync/write/invitations/room booking/conference creation;
- notifications;
- solver;
- recurrence evaluator/checkpoints;
- Occurrence generation;
- Session/Actual runtime;
- multi-device reconciliation;
- AI/voice runtime.

Those later capabilities must attach through the seams now present rather than force a Create rewrite.