# DANTE — Temporal Create Workstream Handoff

**Status:** C1 AUTOMATED PASS — PENDING USER MANUAL ACCEPTANCE  
**Date:** 2026-09-01  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Local worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Final C1 implementation candidate:** `36aa4652731cd9a09334fd52214e66bd87544e22`  
**Frontend CI:** run `33542270688` / #416 — FULL PASS

## 1. Handoff authority

This is the operational handoff for Timeline / Temporal Create on `feature/home-timeline`.

For this branch it supersedes older generic Home operational metadata in `production-depth-handoff.md` and `current-checkpoint.md`. Those files remain historical/parallel Home references, not the live C1 handoff.

A new agent/chat must read in this order:

1. `temporal-live-status.md`;
2. `temporal-create-c1-engineering-checkpoint.md`;
3. `temporal-create-c1-manual-acceptance.md`;
4. `temporal-create-c1-scope-amendment.md`;
5. `temporal-create-q0-approval.md`;
6. `temporal-create-q0-contract.md`;
7. `temporal-frontend-roadmap.md`;
8. `temporal-f0-contract.md`;
9. `timeline-t1-frozen-contract.md`;
10. `temporal-experience-architecture.md`;
11. H0 structural contract plus current code under `apps/web/src/features/temporal-create/` and Home Timeline.

If C1 documents conflict, the scope amendment wins for product scope and this handoff/live status win for current checkpoint/gate state.

## 2. Stable foundations — do not casually reopen

- H0 Whole Home structural freeze.
- T1/T1-A/T1-B Timeline interaction baseline.
- F0 temporal application foundation at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`.
- Schedule != Occurrence != Session != Actual.
- Intention != placement != occurrence != execution.
- Proposal != accepted state.
- ViewModel != frontend application model != DTO != Domain != persistence.
- Manual/keyboard/future AI/future voice converge on semantic application commands; AI/voice do not directly mutate state.
- No fake backend/provider success.
- Child capabilities consume the frozen Home structure; they do not renegotiate it.

## 3. Current C1 state

C1 is **implemented and automated-green to complete pre-backend depth, but remains OPEN until user manual acceptance**.

Final implementation candidate:

`36aa4652731cd9a09334fd52214e66bd87544e22`

A later docs-only descendant does not change the implementation candidate unless it also changes code.

The product shape is:

```text
Quick Create
    +
Expanded Create
    +
Full Create / deep authoring
    +
truthful external-vertical handoffs
```

All levels share one draft/application contract.

## 4. What is implemented

### Shared Create lifecycle

- title-first Quick Create;
- structured draft lifecycle;
- dirty/cancel/discard protection;
- deterministic validation;
- invalid-field focus;
- Quick -> Expanded -> Full progressive disclosure without draft duplication;
- keyboard/focus behavior;
- responsive popover/sheet/full-screen editor behavior;
- IT/EN i18n;
- accessibility regression checks;
- local F0 application runtime;
- exact retry idempotency;
- local rich-specification storage separate from Timeline projection;
- preview -> apply -> reveal/focus -> Undo lifecycle.

### Activity

The pre-backend authoring surface includes:

- context/life-area;
- timed/all-day/unscheduled form where applicable;
- expected duration;
- fixed/open/window/preferred/deadline scheduling intent;
- movement/replanning policy;
- execution/session structure;
- minimum/max session and buffer intent where applicable;
- recurrence source specification;
- confirmation/outcome/review policy seams;
- notes/tags;
- handoffs to verticals that own Project/World/etc. rather than duplicate CRUD.

Flexible scheduling intent is preserved as intent/specification; the UI does **not** fake a concrete placement that does not exist.

### Event

The pre-backend authoring surface includes:

- start/end/duration;
- all-day/date-span;
- floating/zoned timezone semantics;
- location;
- recurrence;
- availability;
- visibility;
- reminder/policy seams where represented;
- participants/resources/conference intent as truthful provider handoff only.

No invitation, resource booking or conference link is claimed to have happened locally.

### Timeline integration

- contextual double-click on empty Timeline time creates temporal defaults;
- Shift-drag on empty Timeline creates range defaults;
- cards are protected from accidental range-create capture;
- applied local Create items render as Timeline projections;
- filtering/context tone and expanded-group geometry are respected;
- created placed items can be revealed/focused;
- Undo removes F0 projection and local rich record;
- cancelling a contextual Create returns focus to the Timeline grid rather than the global `+`.

## 5. Hardening already completed — preserve it

### Architecture cycles

Create UI component-to-component type cycles were removed by extracting shared UI types. Final dependency-cruiser result: **194 modules / 459 dependencies / zero violations**.

### i18n / accessibility contract

Semantic labels such as `Durata prevista / Expected duration` are the current product contract. Recurrence controls have unambiguous accessible names.

### Contextual Shift-drag E2E

The original E2E issue was an off-screen/stale raw mouse coordinate caused by recycled Timeline geometry. The accepted test explicitly brings the day section into view and remeasures before raw pointer input.

### Mobile width

Browser sub-pixel geometry such as `390.0000028px` is tolerated only in the numeric bounding-box assertion. Real horizontal overflow remains strictly checked with `scrollWidth <= clientWidth`.

### DST

Zoned Event end/duration arithmetic uses actual Instants in the selected IANA zone. Dedicated tests cover Europe/Rome spring-forward, fall-back and multi-day arithmetic. Do not regress this to `PlainDateTime` wall-clock duration for zoned Events.

### Rich-intent idempotency

F0 fingerprints the minimal projection command; C1 separately fingerprints full rich intent. Exact retries are valid. Reusing an operation ID with changed recurrence/session/provider metadata returns `operation-id-reused` and does not mutate rich records.

### Projection layout performance

Timeline Create projection layout is single-pass O(n) with slot counters and cached group/day lookups; do not restore per-item `slice/filter/find` scans.

### Runtime initialization

`TemporalCreateEntry` lazily creates its local runtime once. Do not reintroduce `useRef(createLocalTemporalCreateRuntime())`, which evaluates a discarded runtime on every render.

### Focus-return ownership

Create stores the real return target:

- open from global Timeline `+` -> close/discard returns to `+`;
- open from Timeline double-click/Shift-drag -> clean close returns to `.timeline-grid`;
- successful placed Create transfers focus to the created projection when reveal succeeds.

### Dirty-discard modal lifecycle

The confirmation is a named `alertdialog` with contained Tab order. While active, underlying composer header/form are natively `inert`, so keyboard, pointer and accessibility exposure do not conflict with the modal contract. Continuing editing restores the control from which close was attempted when still connected.

## 6. Final automated evidence

For implementation candidate `36aa4652731cd9a09334fd52214e66bd87544e22`:

- Frontend CI run ID: `33542270688`;
- run number: `416`;
- Quality: **PASS**;
- Mobile Bundle: **PASS**;
- Chromium Web E2E: **PASS**;
- frozen Firefox Timeline interaction contract: **PASS**;
- Frontend CI Gate: **PASS**.

Quality includes:

- frontend contract drift PASS;
- active Home format PASS;
- lint PASS;
- typecheck 5/5 PASS;
- architecture PASS;
- generated-source drift PASS;
- web unit suite 25 files / 151 tests PASS, plus package suites;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

## 7. Bundle decision

Final Home route build observed on #416:

```text
233.28 kB raw
83.74 kB gzip
```

Earlier pre-expanded Create evidence was about `76.98 kB` gzip, so the complete deeper C1 surface adds roughly `6.8 kB` gzip to Home.

Decision: **keep Expanded/Full synchronous in C1**.

Do not add dynamic import/Suspense merely to recover a few gzip kilobytes. The current advanced editor participates in deterministic validation/focus/draft continuity; an async boundary would add failure/loading/focus states and architectural complexity for too little measured benefit. Revisit route splitting only if future route growth creates a material performance case.

## 8. Resume / next action

The engineering phase of C1 is automated-green. Do not continue speculative polishing.

Next action is the versioned human gate:

`docs/frontend/home/temporal-create-c1-manual-acceptance.md`

Resume procedure:

1. fresh-check branch HEAD;
2. distinguish the final implementation candidate `36aa4652...` from later docs-only descendants;
3. if a docs-only descendant has CI, require its docs/format workflow to be green as well;
4. sync the local Timeline worktree;
5. execute the manual protocol;
6. if a defect is found, reopen only the demonstrated defect plus necessary adjacent contract and rerun full gates;
7. if the user explicitly approves, document `C1 MANUAL PASS — APPROVED`, freeze C1 and only then start C2 Card -> structured Detail.

## 9. Backend/external stop line

Do not implement or fake inside C1:

- real API transport;
- PostgreSQL persistence;
- canonical server identities;
- server auth/ACL;
- provider calendar writes/sync;
- participant invitations;
- room/resource booking;
- conference creation;
- notification delivery;
- authoritative solver execution;
- multi-device reconciliation;
- AI runtime;
- voice runtime.

The frontend seams should make these later adapter/provider integrations additive instead of forcing a Create rewrite.

## 10. User gate

**C2 must not start before the complete C1 Create capability is manually tested and explicitly approved by the user.** Automated green is necessary and is now achieved; manual approval is still outstanding.
