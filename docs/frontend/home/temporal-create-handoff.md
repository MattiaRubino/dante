# DANTE — Temporal Create Workstream Handoff

**Status:** ACTIVE / C1 OPEN — FULL PRE-BACKEND CREATE SYSTEM IN PROGRESS
**Date:** 2026-09-01
**Repository:** `MattiaRubino/dante`
**Branch:** `feature/home-timeline`
**Local worktree:** `/home/mattia/projects/dante-timeline`
**Integration target:** `feature/home-react`

## 1. This is the handoff authority for Timeline/Create

For `feature/home-timeline`, this file supersedes the older generic Home handoff metadata in:

- `docs/frontend/home/production-depth-handoff.md`;
- `docs/frontend/home/current-checkpoint.md`.

Those files remain useful historical/parallel Home documents for `feature/home-react`, but they are **not the live operational handoff for Timeline/Create**.

A new agent/chat continuing this workstream must read, in order:

1. `docs/frontend/home/temporal-live-status.md`;
2. `docs/frontend/home/temporal-create-c1-scope-amendment.md`;
3. `docs/frontend/home/temporal-create-q0-approval.md`;
4. `docs/frontend/home/temporal-create-q0-contract.md`;
5. `docs/frontend/home/temporal-frontend-roadmap.md`;
6. `docs/frontend/home/temporal-f0-contract.md`;
7. `docs/frontend/home/timeline-t1-frozen-contract.md`;
8. `docs/frontend/home/temporal-experience-architecture.md`;
9. H0 structural contract and current code under `apps/web/src/features/temporal-create/` and Home Timeline.

When documents conflict about C1 scope, the **C1 scope amendment wins**.

## 2. Stable accepted foundations

Do not reopen casually:

- H0 Whole Home structural freeze;
- T1/T1-A/T1-B Timeline interaction baseline;
- F0 temporal application foundation, closed on `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- permanent temporal semantic distinctions from Product/Domain/Logical/Physical/DB;
- UI/application/DTO/persistence separation;
- ports/adapters boundary;
- no fake backend success;
- no AI/voice direct mutation path.

## 3. Current C1 state

C1 is **OPEN / NOT USER-ACCEPTED**.

A substantial Quick Create implementation already exists and provides useful foundation:

- Activity/Event distinction;
- title;
- timed/all-day/unscheduled forms;
- date/time/duration;
- floating/zoned time support;
- context;
- notes/details;
- immutable draft lifecycle;
- deterministic validation;
- F0 command execution through a local runtime;
- idempotency/double-submit guard;
- Timeline candidate preview;
- applied local projection;
- reveal/focus;
- Undo;
- contextual Timeline double-click invocation;
- responsive sheet/popover behavior;
- keyboard/focus/accessibility work;
- i18n IT/EN;
- Chromium/Firefox/Mobile/Quality CI coverage.

This is **not the closure point**.

Manual review demonstrated that the product surface still represented only the compact Quick Create layer and did not yet satisfy the later user mandate for the maximum useful pre-backend DANTE Create system.

## 4. Scope correction now authoritative

The user explicitly requires Create to reach maximum useful pre-backend depth before it can close.

Therefore the active target is:

```text
Quick Create
    +
Expanded Create
    +
Full Create editor / deep authoring surface
    +
truthful external-vertical handoffs
```

all sharing one structured draft/application path.

See `temporal-create-c1-scope-amendment.md` for the complete expanded grammar.

## 5. What must now be implemented

### Activity creation depth

Progressively support the authoritative subset of:

- organization/context links;
- fixed, open, windowed, preferred and deadline-constrained scheduling intent;
- expected duration/effort;
- minimum session / split policy where applicable;
- priority/planning pressure where authoritative;
- movement/lock/replanning policy;
- initial recurrence specification where the source owns recurrence;
- reminder/confirmation policy seams;
- notes/tags/template/external references where a real contract exists.

### Event creation depth

Progressively support the authoritative subset of:

- start/end/duration;
- all-day;
- floating/zoned timezone semantics;
- location;
- recurrence;
- availability/visibility where supported;
- reminder policy;
- participants/resources/conference as truthful external integration seams only.

### Other object types

Do not force Goal/Project/Program/Routine/etc. into Activity/Event.

Provide a scalable `Altro tipo…` / global Create handoff architecture when appropriate, without implementing duplicate CRUD for their owning verticals.

## 6. UI direction

Do not expand the existing popup into a giant settings form.

Required direction:

```text
LEVEL 1 — Quick Create
fast, title-dominant, low friction

LEVEL 2 — Expanded Create
semantic sections for scheduling/organization/recurrence/policy

LEVEL 3 — Full Create
side sheet or dedicated deep editor when complexity warrants it
```

The exact visual solution may evolve, but it must remain premium, calm, keyboard/touch accessible and clearly more than an administrative form.

## 7. Backend / external stop line

Do not implement or fake:

- real API transport;
- PostgreSQL persistence;
- server auth/ACL;
- provider calendar writes/sync;
- participant invitations;
- conferencing creation;
- notification delivery;
- authoritative solver execution;
- multi-device reconciliation;
- AI runtime;
- voice runtime.

Complete the frontend/application seams so those later integrations replace adapters rather than rewrite Create.

## 8. CI / QA rule

C1 is not ready merely because one implementation checkpoint is green.

Before final user acceptance:

- all active source/i18n tests must be green;
- Chromium full Web E2E green;
- frozen Timeline Firefox contract green;
- Mobile Bundle green;
- Quality lint/typecheck/architecture/unit/build/drift green;
- no raw i18n keys visible;
- repeated open/create/undo/reopen lifecycle stable;
- responsive/mobile/full-width behavior manually reviewed;
- visual hierarchy and density manually reviewed;
- complete Create grammar exercised, not only Quick Create.

## 9. Operational rules

- Work continuously across internal slices; do not stop for micro-approvals.
- Ask early only for a genuinely unresolved product decision not answerable from existing authority.
- Fresh-check branch HEAD before writes because parallel work may move branches.
- No merge/rebase/force/main mutation without explicit authorization.
- Do not touch Mondi/World Focus ownership except through deliberate shared change-control.
- Do not weaken frozen Timeline/H0 contracts to make Create easier.
- Keep documentation live as scope/status changes; do not leave stale handoff metadata behind again.
