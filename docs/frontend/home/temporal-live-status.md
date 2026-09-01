# DANTE — Temporal Workstream Live Status

**Status:** ACTIVE / C1 CREATE SYSTEM OPEN — NOT USER-ACCEPTED
**Date:** 2026-09-01
**Repository:** `MattiaRubino/dante`
**Branch:** `feature/home-timeline`
**Worktree:** `/home/mattia/projects/dante-timeline`
**Integration target:** `feature/home-react`

## Live authority

This file is the live checkpoint for the isolated Timeline/Create workstream.

For this branch it supersedes stale operational metadata in the generic Home `current-checkpoint.md` and `production-depth-handoff.md`, which still describe the parallel `feature/home-react` P1/P2 workstream.

Read next:

- `temporal-create-handoff.md`;
- `temporal-create-c1-scope-amendment.md`;
- `temporal-create-q0-approval.md`;
- `temporal-create-q0-contract.md`;
- `temporal-frontend-roadmap.md`.

## Stable closed foundations

- H0 Whole Home structural baseline: frozen.
- T1/T1-A Timeline hardening: closed.
- T1-B continuous temporal navigation/scrubber: closed.
- F0 temporal application foundation: closed on `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`.
- Q0 original Create contract: user-approved as architectural/product baseline, later amended for broader C1 scope.

## Current Create implementation checkpoint

The pre-documentation-sync implementation branch reached `abb1ec90c6791252168857b600c5c866ecdc8b59` after adding explicit raw-i18n-key regression guards.

Useful implemented foundation includes:

- compact Quick Create UI;
- Activity/Event;
- timed/all-day/unscheduled;
- date/time/duration/timezone/context/details;
- F0-backed local create runtime;
- deterministic validation;
- candidate Timeline preview;
- local applied projection;
- reveal/focus;
- Undo;
- contextual Timeline invocation;
- responsive/mobile behavior;
- i18n and accessibility/test coverage.

## Manual review finding — scope not complete

The user manually reviewed the working composer on 2026-09-01.

After restarting the Vite dev server, stale raw i18n keys disappeared and the compact UI rendered correctly. The manual review then exposed the more important product issue:

> the current UI is a valid Quick Create layer, but it is not yet the complete DANTE Create system promised by the later user mandate.

Therefore C1 is explicitly **OPEN**. The compact composer must not be presented again as the completed vertical.

The expanded authority is `temporal-create-c1-scope-amendment.md`.

## Current CI truth

The earlier full Create checkpoint `9c70b91d0d1f303b1fbf876b0dec37450669bcaf` had a fully green Frontend CI run including Quality, Mobile, Chromium and frozen Firefox Timeline contract.

After the manual stale-dev-server i18n incident, two regression protections were added. On implementation checkpoint `abb1ec90c6791252168857b600c5c866ecdc8b59`, Frontend CI #342 reported:

- Quality: PASS;
- Mobile Bundle: PASS;
- Web E2E: FAIL;
- Frontend CI Gate: FAIL as a consequence.

That checkpoint is therefore **not a green closure point**. The Web E2E failure must be triaged/fixed while the broader Create work continues.

Documentation-sync commits after `abb1ec90...` are docs-only and intentionally move branch HEAD; they do not change this implementation/CI truth.

## Current product target

C1 now means one complete progressive Create capability:

```text
Quick Create
+
Expanded Create
+
Full Create editor/deep authoring
+
truthful handoff/integration seams
```

All surfaces share one draft/application contract.

### Activity

Creation-time authoring must reach the maximum useful pre-backend depth for authoritative DANTE semantics, including relevant organization links, scheduling intent/constraints, duration/session structure, movement/replanning policy, recurrence source specification and reminder/confirmation intent.

### Event

Creation-time authoring must reach the maximum useful pre-backend depth for Event semantics, including start/end/all-day/timezone, location, recurrence, availability/visibility/reminders where authoritative, plus truthful external seams for participants/resources/conferencing.

### Other entity types

Do not flatten Goal/Project/Program/Routine/etc. into Activity/Event. Provide scalable handoff/global-create architecture when appropriate.

## Explicit stop line

Still outside this workstream until the later backend/external vertical:

- real API;
- PostgreSQL persistence;
- canonical server IDs;
- auth/ACL enforcement;
- provider sync;
- external invitations/conferencing execution;
- notification delivery;
- authoritative solver runtime;
- multi-device reconciliation;
- AI runtime;
- voice runtime.

## Next work

1. keep the useful existing Quick Create foundation;
2. triage/fix the current Web E2E regression;
3. redesign the Create interaction as progressive Quick → Expanded → Full rather than a giant popup;
4. expand the Create draft/application model only for demonstrated authoritative fields;
5. implement Activity and Event deep authoring to the amended scope;
6. add truthful external-vertical handoffs;
7. run full Quality/Mobile/Chromium/Firefox gates on one final implementation commit;
8. perform one substantive user manual review of the complete Create system;
9. only then mark C1 CLOSED.

## Delivery rule

Internal engineering slices may proceed continuously. Do not stop the user for micro-approval after each field or component. The next user acceptance gate is the coherent complete C1 Create system unless a genuinely unresolved product decision requires earlier input.
