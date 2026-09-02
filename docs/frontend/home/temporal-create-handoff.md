# DANTE — Temporal Create Workstream Handoff

**Status:** C1 IMPLEMENTATION FULL GREEN — USER MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Local worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Final C1 implementation candidate:** `7028633921d1b438bd04961a718457afd82ccc13`  
**Frontend CI:** run `33635389124` / #632 — FULL PASS

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

## 3. C1 permanent product boundary — manual authoring only

The Timeline `+` is DANTE's highest-depth **manual authoring** path before backend integration.

It is explicitly not:

- a chat;
- an AI command bar;
- a natural-language parser;
- a voice surface;
- a generic “intent interpreter” UI.

Current C1 entry topology:

```text
Timeline +
Timeline double-click
Timeline Shift-drag/range
        ↓
manual structured prefill
        ↓
SHARED TEMPORAL CREATE SESSION
        ↓
Quick ↔ Expanded ↔ Full
        ↓
normalize → validate → candidate preview
        ↓
explicit user commit
        ↓
F0 application command
        ↓
local deterministic adapter NOW
backend adapter LATER
```

Quick/Expanded/Full are views of one draft and one application path.

`TemporalCreateFieldSeed` is a deterministic **manual-prefill** seam for values already known by the manual Timeline interaction. It is not an AI/NL/voice contract.

A future DANTE/AI vertical remains a separate product surface. It may later reuse compatible downstream application/domain/backend commands when that vertical's own contract justifies the reuse; it is not required to enter through the C1 form, session or seed.

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
→ backend Occurrence generation later
```

Current C1 therefore shows a truthful Routine owning-vertical handoff.

Flexible/open/window/deadline/preferred Activity intent may be authored without fabricating an accepted exact Schedule.

### Event

Event owns recurrence directly and exposes all four CP6 M4 recurrence families:

- calendar wall-clock;
- elapsed interval;
- quota per period;
- cyclic positional.

Full Event authoring includes recurrence, purpose, expected outcome, agenda, decision intent, participants, resources, pre-read, conference intent and buffers.

Provider actions remain intent only.

## 5. Current recurrence depth

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
- UI positions are human-friendly 1-based.

No browser-side Occurrence generation is allowed.

## 6. Context and appearance semantics

Do not collapse Context and appearance.

```text
Context/groupId
→ organization
→ grouping
→ filtering
→ inherited visual tone by default

appearanceTone override
→ presentation only
→ does not mutate Context/groupId
→ does not change filter membership
```

The manual Create appearance control exposes stable color vocabulary independent from Context names:

- Viola / Purple;
- Ciano / Cyan;
- Verde / Green;
- Ambra / Amber;
- Rosa / Pink;
- Rosso / Red.

The E2E contract proves that a Focus item with a red presentation override remains a Focus item for grouping/filtering.

## 7. External owner handoff seam

`application/temporal-create-handoff.ts` is the typed Create-side contract for objects owned by other verticals.

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

At the final implementation candidate `7028633921d1b438bd04961a718457afd82ccc13`, `runtime.prepare()` re-normalizes and freezes its own copy of the specification before validation and command creation.

Do not remove this. It prevents mutable callers from changing rich intent after preparation and producing a command/specification TOCTOU mismatch.

## 9. Timeline integration hardening

The contextual Create E2E must not assume that a mounted `.timeline-day-section` is already intersecting the browser viewport after `/home` loads, and it must not retain a stale virtualized day node across Create open/close.

The final hardened test:

- scrolls the Timeline grid into the browser viewport;
- intersects day-section geometry with both the Timeline grid viewport and browser viewport;
- requires a useful visible interaction band rather than accepting zero-height/edge-only visibility;
- anchors the chosen section by stable `data-timeline-date`;
- performs double-click using the section-local visible band;
- reacquires current geometry before Shift-drag;
- performs Shift-drag with current browser coordinates;
- uses no arbitrary sleeps/retries and weakens no gesture assertion.

This closes the demonstrated virtualization/viewport locator defect while preserving real contextual-create coverage. The resulting contract passed Chromium and the frozen Timeline Firefox suite at CI #632.

T1 drag/focus behavior remains frozen.

The appearance E2E also follows a stable native card identity across filter remounts rather than relying on an imperative DOM marker that disappears when React remounts the card.

## 10. UI / accessibility state

Preserve:

- title-first Quick Create;
- semantic grouping rather than a settings wall;
- exact duration authoring in deeper Activity surfaces;
- separate Event grammar;
- shared section heading/check-grid visual grammar;
- Full Event section headings using the same `:is(h3, h4)` grammar rather than one-off styles;
- unambiguous accessible control names;
- named dirty-discard `alertdialog`;
- contained Tab loop;
- exact connected-control focus restoration;
- native `inert` background while confirmation is active;
- mobile Full editor / no horizontal overflow;
- no raw i18n keys;
- no AI/NL/voice affordance inside manual Create.

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

`7028633921d1b438bd04961a718457afd82ccc13`

CI `33635389124` / #632:

- Quality PASS;
- Mobile Bundle PASS;
- Chromium full Web E2E PASS;
- Firefox frozen Timeline interaction contract PASS;
- Frontend CI Gate PASS.

Exact Quality evidence:

- frontend contract drift / active Home format PASS;
- lint PASS;
- typecheck 5/5;
- architecture: **214 modules / 522 dependencies / zero violations**;
- generated-source drift PASS;
- web unit: **34 files / 183 tests**;
- production build PASS;
- diff/mutation checks PASS.

Home route:

`268.40 kB raw / 90.13 kB gzip`.

## 13. Current stop and next transition

C1 is **not** closed yet.

Current state:

```text
IMPLEMENTATION COMPLETE
AUTOMATED FULL PASS
DOCUMENTATION RECONCILIATION COMPLETE
FINAL DOCUMENTATION DESCENDANT MUST BE CI-GREEN
USER MANUAL ACCEPTANCE PENDING
NOT FROZEN / CLOSED
```

Once the final documentation descendant is itself CI-green:

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
- AI/NL runtime or input;
- voice runtime or input.

Those later capabilities must attach through their own verticals and compatible downstream seams rather than force a manual Create rewrite.
