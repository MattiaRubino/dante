# DANTE — Temporal Workstream Live Status

**Status:** C1 AUTOMATED PASS — PENDING USER MANUAL ACCEPTANCE  
**Date:** 2026-09-01  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Final C1 implementation candidate:** `36aa4652731cd9a09334fd52214e66bd87544e22`  
**Frontend CI:** run `33542270688` / #416 — FULL PASS

## Live authority

This file is the live operational status for the isolated Timeline / Temporal Create workstream.

For `feature/home-timeline` it supersedes stale operational metadata in generic Home checkpoint/handoff files that belong to the parallel/integration Home line.

A continuation must read, in order:

1. `docs/frontend/home/temporal-create-handoff.md`;
2. `docs/frontend/home/temporal-create-c1-engineering-checkpoint.md`;
3. `docs/frontend/home/temporal-create-c1-manual-acceptance.md`;
4. `docs/frontend/home/temporal-create-c1-scope-amendment.md`;
5. `docs/frontend/home/temporal-create-q0-approval.md`;
6. `docs/frontend/home/temporal-create-q0-contract.md`;
7. `docs/frontend/home/temporal-frontend-roadmap.md`;
8. `docs/frontend/home/temporal-f0-contract.md`;
9. `docs/frontend/home/timeline-t1-frozen-contract.md`;
10. `docs/frontend/home/temporal-experience-architecture.md`.

When older C1 documents conflict about scope, the **C1 scope amendment wins**. The live status/handoff win for current checkpoint and gate state.

## Stable closed foundations

Do not reopen casually:

- H0 Whole Home structural baseline;
- T1/T1-A Timeline hardening;
- T1-B continuous temporal navigation / relative scrubber;
- F0 temporal application foundation at `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- Schedule / Occurrence / Session / Actual / Proposal distinctions;
- frontend application model != DTO != Domain != persistence;
- ports/adapters boundary;
- no fake backend/provider/AI/voice success.

## C1 product shape

C1 is the complete pre-backend Create capability:

```text
Quick Create
+
Expanded Create
+
Full Create / deep authoring
+
truthful external-vertical handoffs
```

All levels share one structured draft/application path.

## Implemented C1 surface

The final automated candidate includes:

- Activity and Event as distinct semantics;
- title-first Quick Create;
- timed, all-day and unscheduled forms as semantically applicable;
- date/start/end/duration;
- floating-local and named-zone/zoned time semantics;
- context/life-area assignment from Timeline groups;
- notes/tags;
- Quick -> Expanded -> Full progressive authoring without draft duplication;
- Activity fixed/open/window/preferred/deadline intent;
- movement/replanning policy;
- expected duration, session structure, minimum/max session controls and buffers where supported;
- recurrence source specification;
- confirmation/outcome/review policy seams;
- Event location, availability and visibility;
- participant/resource/conference intent as truthful provider handoff only;
- explicit handoff for Project/World/other external-owned creation instead of duplicated CRUD;
- deterministic validation and invalid-control focus;
- F0-backed command execution;
- local rich specification kept separate from minimal Timeline projection;
- exact retry idempotency at both projection and rich-intent levels;
- candidate preview, applied Timeline projection, reveal/focus and Undo;
- contextual double-click and Shift-drag range Create;
- responsive/mobile Full editor;
- IT/EN i18n;
- accessibility and modal focus lifecycle protections.

## Hardening that must not regress

1. **Architecture:** Create UI cycles removed; shared UI types are outside component-to-component cycles.
2. **i18n/a11y:** semantic labels such as `Durata prevista / Expected duration`; recurrence controls have unambiguous accessible names.
3. **Shift-drag test truth:** contextual E2E scrolls the intended recycled Timeline day into view and remeasures current geometry before raw mouse input.
4. **Mobile geometry:** sub-pixel browser width noise is tolerated, while real horizontal overflow remains strictly forbidden.
5. **DST correctness:** zoned Event end/duration arithmetic uses real Instants in the IANA zone; Europe/Rome spring-forward/fall-back and multi-day cases are covered.
6. **Rich idempotency:** same operation ID with changed rich metadata is rejected side-effect-free; exact retry remains idempotent.
7. **Projection performance:** Create projection collision/layout preparation is O(n) with slot counters and cached group/day lookups rather than repeated O(n²) scans.
8. **Runtime allocation:** the local Create runtime is lazily initialized once rather than constructing and discarding a workspace on each React render.
9. **Contextual focus return:** direct `+` close returns to `+`; Timeline double-click/Shift-drag close returns to the Timeline grid.
10. **Discard modal lifecycle:** dirty-close confirmation is a named `alertdialog`; Tab is contained inside its actions; the underlying header/form are inert; continuing editing restores the exact previous connected control.

## Final automated evidence

Implementation candidate:

`36aa4652731cd9a09334fd52214e66bd87544e22`

Frontend CI:

- run ID: `33542270688`;
- run number: `416`;
- Quality: **PASS**;
- Mobile Bundle: **PASS**;
- Web E2E Chromium: **PASS**;
- frozen Timeline interaction contract Firefox: **PASS**;
- Frontend CI Gate: **PASS**.

Quality evidence includes:

- lint PASS;
- typecheck 5/5 PASS;
- architecture PASS: 194 modules / 459 dependencies / zero violations;
- generated-source drift PASS;
- unit tests PASS: 25 web test files / 151 tests, plus package suites;
- production build PASS;
- diff check PASS;
- repository mutation check PASS.

Production Home route at the final candidate is approximately:

- `233.28 kB` raw;
- `83.74 kB` gzip.

The earlier pre-expanded Create Home route observed during this workstream was approximately `76.98 kB` gzip. The deeper C1 surface therefore adds roughly `6.8 kB` gzip to the route.

### Bundle decision

**Do not add dynamic import/Suspense for Expanded/Full in C1.**

The measured potential saving is too small to justify adding an asynchronous boundary to a form whose advanced validation must preserve deterministic focus and draft continuity. The synchronous implementation is intentionally retained unless future route growth produces material evidence that a split is worthwhile.

This is a measured product-quality decision, not an omitted optimization.

## Current gate

Automated closure is complete. The only remaining C1 gate is the human acceptance protocol in:

`docs/frontend/home/temporal-create-c1-manual-acceptance.md`

C1 is **not yet FROZEN/CLOSED**.

Required next action:

1. sync the local Timeline worktree to the final docs descendant;
2. run the manual protocol;
3. report precise defect(s) if any, or explicitly approve C1;
4. only after explicit user PASS mark C1 frozen and move to C2 Card -> structured Detail.

## Stop line

Still outside C1:

- real API transport;
- PostgreSQL persistence;
- canonical server IDs;
- auth/ACL enforcement;
- external provider writes/sync/invitations/conferencing;
- notification delivery;
- authoritative solver runtime;
- multi-device reconciliation;
- AI runtime;
- voice runtime.

## Delivery rule

Do not start C2 merely because CI is green. C1 advances only after the complete Create capability is manually tested and explicitly approved by the user.
