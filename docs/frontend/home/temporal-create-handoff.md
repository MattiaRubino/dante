# DANTE — Temporal Create Workstream Handoff

**Status:** ACTIVE / C1 COMPLETE-CANDIDATE HARDENING — NOT USER-ACCEPTED  
**Date:** 2026-09-01  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Local worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Implementation checkpoint:** `4ca8de311e10fb03a4d5fd47903ebe4396271d95`

## 1. Handoff authority

This is the operational handoff for Timeline / Temporal Create on `feature/home-timeline`.

For this branch it supersedes the older generic Home operational metadata in `production-depth-handoff.md` and `current-checkpoint.md`. Those remain useful historical/parallel Home documents for `feature/home-react`, but are not the live handoff for this workstream.

A new agent/chat must read in this order:

1. `temporal-live-status.md`;
2. `temporal-create-c1-engineering-checkpoint.md`;
3. `temporal-create-c1-scope-amendment.md`;
4. `temporal-create-q0-approval.md`;
5. `temporal-create-q0-contract.md`;
6. `temporal-frontend-roadmap.md`;
7. `temporal-f0-contract.md`;
8. `timeline-t1-frozen-contract.md`;
9. `temporal-experience-architecture.md`;
10. H0 structural contract plus current code under `apps/web/src/features/temporal-create/` and Home Timeline.

If C1 documents conflict, the **scope amendment and this live handoff take precedence over the older compact-Create interpretation**.

## 2. Stable foundations — do not casually reopen

- H0 Whole Home structural freeze.
- T1/T1-A/T1-B Timeline interaction baseline.
- F0 temporal application foundation on `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`.
- Schedule != Occurrence != Session != Actual.
- Intention != placement != occurrence != execution.
- Proposal != accepted state.
- ViewModel != frontend application model != DTO != Domain != persistence.
- Manual/keyboard/future AI/future voice must converge on semantic application commands; AI/voice do not directly mutate state.
- No fake backend/provider success.
- Child capabilities consume the frozen Home structure; they do not renegotiate it.

## 3. Current C1 state

C1 is **implemented to complete-candidate depth but still OPEN / NOT USER-ACCEPTED**.

The current implementation checkpoint is:

`4ca8de311e10fb03a4d5fd47903ebe4396271d95`

Do not confuse a later docs-only branch HEAD with a new implementation checkpoint.

The active product shape is:

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
- immutable/structured draft lifecycle;
- dirty/cancel/discard protection;
- deterministic validation;
- invalid-field focus;
- Quick -> Expanded -> Full progressive disclosure;
- keyboard/focus behavior;
- responsive popover/sheet/full-screen editor behavior;
- IT/EN i18n;
- accessibility regression checks;
- local F0 application runtime;
- exact retry idempotency;
- local rich-specification storage separate from Timeline projection;
- preview -> apply -> reveal/focus -> Undo lifecycle.

### Activity

The pre-backend authoring surface includes the authoritative subset currently justified by DANTE semantics:

- context/life-area;
- timed/all-day/unscheduled form where applicable;
- expected duration;
- fixed/open/window/preferred/deadline scheduling intent;
- movement/replanning policy;
- execution/session structure;
- minimum session;
- recurrence source specification;
- confirmation/outcome policy seams;
- notes/tags;
- handoffs to verticals that own Project/World/etc. rather than duplicate CRUD.

Flexible scheduling intent is preserved as intent/specification; the UI does **not** fake a concrete placement that does not yet exist.

### Event

The pre-backend authoring surface includes:

- start/end/duration;
- all-day/date-span;
- floating/zoned timezone semantics;
- location;
- recurrence;
- availability;
- visibility;
- reminders/policy where currently represented;
- participants/resources/conference intent as truthful provider handoff only.

No invitation, resource booking or conference link is claimed to have happened locally.

### Timeline integration

- contextual double-click on empty Timeline time creates temporal defaults;
- Shift-drag on empty Timeline creates range defaults;
- cards remain protected from accidental range-create gesture capture;
- applied local Create items render as Timeline projections;
- filtering/context tone and expanded-group geometry are respected;
- created items can be revealed/focused;
- Undo removes both F0 projection and local rich record.

## 5. Important hardening already completed

Do **not** redo these as if still open; preserve them and only reopen if a regression proves a defect.

### Architecture cycles

Create UI component-to-component type cycles were removed by extracting shared UI types. Architecture check returned zero dependency violations.

### i18n / accessibility contract

The current label contract uses semantic names such as `Durata prevista / Expected duration`; recurrence controls have non-ambiguous accessible names. Tests were aligned to the current product language rather than regressing the UI to stale labels.

### Contextual Shift-drag E2E

The earlier E2E failure was traced to raw mouse coordinates measured on an off-screen recycled Timeline day. The correct test brings the day into view and re-measures current geometry before raw pointer input. Do not revert to stale bounding boxes.

### Mobile width

A `390.0000028px` browser floating-point width was not a real overflow. Width assertion now allows sub-pixel tolerance while the independent `scrollWidth <= clientWidth` invariant remains strict.

### DST

A real temporal bug was found: treating zoned Event start/end as `PlainDateTime` could turn Europe/Rome 01:30 -> 03:30 on spring-forward day into 120 minutes and then move the zoned end to 04:30. The field helpers now accept floating vs zoned mode and timezone ID; zoned duration/end use real Instants. Dedicated tests cover spring-forward, fall-back and multi-day arithmetic.

### Rich-intent idempotency

F0 fingerprints the minimal temporal projection command, but C1 stores richer recurrence/session/provider metadata above F0. C1 therefore adds its own canonical fingerprint by `operationId`. Exact prepared retries reuse the original execution. The same operation ID with changed rich intent returns `operation-id-reused` without mutating rich records.

### Projection layout performance

The Create projection bridge no longer computes preceding slot collisions with `slice().filter()` for every projection or repeated `groups.find/findIndex`. Layout preparation uses one pass with slot counters plus cached group/day lookups, preserving current visual offsets while avoiding O(n²) growth.

## 6. Current CI truth

For implementation checkpoint `4ca8de311e10fb03a4d5fd47903ebe4396271d95`:

- Frontend CI run ID: `33539539640`;
- run number: `410`.

Verified at documentation time:

- Quality: **PASS**;
- Mobile Bundle: **PASS**;
- Web E2E: still **in progress**;
- final Frontend CI Gate: not yet claimable.

Quality PASS includes contract drift, active Home format check, lint, typecheck, architecture, generated-source drift, unit tests, production build, diff check and repository mutation check.

The previous implementation workflow reached successful Chromium and successful frozen Firefox Timeline steps after gesture/mobile fixes, but the workflow was superseded/cancelled by later hardening pushes. It is corroborating evidence, not the closure gate for the current implementation checkpoint.

## 7. How to resume safely

1. Fresh-check `feature/home-timeline` HEAD before any write.
2. Identify whether HEAD is a docs-only descendant of `4ca8de31...` or contains newer code.
3. Check CI run `33539539640` and the latest workflow created by docs sync. Never assume a pending/cancelled run is green.
4. If CI is red, inspect the first real failing step/log and fix the defect; do not weaken H0/T1/C1 semantics to satisfy a test.
5. Keep `4ca8de31...` as the current implementation checkpoint unless a later code commit supersedes it.
6. Finish the remaining bundle/critical-path audit. The current Home chunk increase from the deeper Create work is acceptable only after review; lazy-load Expanded/Full only if the split is clean and measurably useful. Do not add Suspense/code-split complexity merely for a benchmark number.
7. Re-run/confirm the complete Quality + Mobile + Chromium + Firefox + final gate on the actual final descendant.
8. Perform a final static audit of semantic truth, focus cleanup, timers/RAF/listeners, responsive behavior and repeated-use performance.
9. Give the user an exact manual verification script for the coherent complete Create system.
10. Wait for explicit user PASS.
11. Only after that mark C1 frozen/closed and start C2 Card -> Detail.

## 8. Backend/external stop line

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

The frontend seams should make these later adapter/provider integrations additive rather than force a Create rewrite.

## 9. User gate

Internal hardening may continue continuously. **C2 must not start before the complete C1 Create capability is manually tested and explicitly approved by the user.** Automated green is necessary, not sufficient.
