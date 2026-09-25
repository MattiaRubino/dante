# Timeline / Temporal-Operational — B10 scope freeze

Status: **B10-A implementation candidate prepared; generated-client regeneration and user-run local automated acceptance remain pending**.

This document is the execution gate for B10-A after B09 closure. It narrows the first B10 slice without changing the canonical Domain / Logical / Physical contracts.

## 1. Canonical semantic boundaries

The following distinctions are invariants, not implementation details:

- `Schedule != Session != Actual`
- `Session != Actual != Outcome`
- `Actual != Outcome != Confirmation`
- `planned/intended != happened`
- `proposal != accepted effect`
- `projection != canonical truth`
- `current accepted state != latest row`
- `MaterialState != mutable runtime object`
- `idempotency key != Domain identity`
- `Undo != history rewind`

PostgreSQL remains the only canonical authority. API/UI/provider/AI/runtime projections may expose or propose facts, but may not become an alternative source of truth.

## 2. B10-A — Actual / realization core

B10-A is executed and accepted as **one complete vertical block**, not as A1/A2/A3 sub-blocks.

The block exposes the already-modelled `Actual` realization semantics as an explicit temporal capability without collapsing Actual into Session or Schedule and without introducing Outcome or Confirmation semantics early.

### Canonical owner

`dante.actual` is the stable scoped Actual owner. Its subject is `subject_native_ref`, not an Activity-only foreign key. The existing NativeRef eligibility contract bounds the subject family to the canonical eligible native families (currently Activity, Event and Occurrence). B10-A preserves that heterogeneous subject model and does not replace it with an `activity_id` shortcut.

### Write surface

The accepted write surface is append-only realization state:

1. create or address an Actual owner for one eligible `subject_native_ref`;
2. append one `actual_realization_state` MaterialState carrying `realization_occurred`;
3. optionally append `actual_realization_timing` (`extent_code`, `started_at`, `ended_at`) for that state;
4. optionally record one or more `actual_realization_session_basis` rows, preserving both `session_ref` and the exact `session_timing_material_state_ref` used as historical evidence;
5. change accepted/current realization by appending a new state and advancing the canonical current binding/history rather than mutating historical MaterialState payloads.

An Actual may be supported by zero or more Session/timing-state bases while Session and Actual retain separate identities. A Session ending must never create Actual implicitly.

### Read surface

Reads expose canonical current accepted realization state, not "the latest row" by accident. `dante.actual_current_realization` is the bounded current capability surface over `scoped_current_material_state` for facet `actual.realization`; historical chronology remains separate.

At minimum a caller can retrieve:

- `actual_ref` and `subject_native_ref`;
- current accepted realization `material_state_ref` and `realization_occurred`;
- current accepted realization timing when present;
- exact Session/timing-state basis references when present;
- immutable historical facts separately from the current projection through the history endpoint.

### State vocabulary

The canonical realization payload is the existing `realization_occurred` boolean plus the optional timing extent contract (`instant`, `start_only`, `interval`). B10-A does not invent a second status enum or UI persistence vocabulary.

No established Actual means unknown realization. It must not be interpreted as failed, skipped, missed, cancelled or known non-realization. The minimal Timeline surface therefore renders absence as **sconosciuto**, distinct from the explicit `realization_occurred=false` state.

### Idempotency and authorization

Command idempotency is enforced at the public consequential write boundary. Reusing an idempotency key for the same accepted command replays the same semantic result; reusing it for a different payload fails. The idempotency key is not the Actual domain identity.

`Person != Account != Actor` remains binding. API authentication resolves the self Person through the existing access/auth boundary; Actual authoring does not turn Account or UI identity into a second canonical owner.

## 3. Implemented B10-A vertical candidate

The candidate now spans the required layers:

- forward-only Alembic `20260925_70` activates guarded self-scoped Actual realization authoring/read/history over the existing CP6 Actual substrate and immutable operation receipts;
- forward-only Alembic `20260925_71` binds the capability to the exact public subject family at the PostgreSQL authority boundary, so an Activity/Event/Occurrence NativeRef cannot be accepted through the wrong family route;
- SQLAlchemy mapping, Dictionary/scope and database overlay are aligned with the new operation/capability surface;
- backend `ActualApplication` provides guarded record/current/history behavior, append-only current advancement, timing and exact Session-timing-state evidence;
- HTTP API exposes Activity, Event and Occurrence Actual POST/GET plus Actual history with stable semantic operationIds;
- OpenAPI inventory freezes those seven public operations;
- Timeline web exposes minimal explicit Actual authoring for all three eligible subject families while preserving absence as unknown;
- focused PostgreSQL/application, public API and web regression tests are committed for the user-run local gate.

The generated API client is intentionally **not edited by hand**. It must be regenerated locally through the repository-owned `pnpm api:generate` command before acceptance.

## 4. Explicitly deferred from B10-A

The following are not part of B10-A and must not be smuggled into generic payloads:

- Outcome assertion or outcome state;
- Confirmation assertion;
- partial/completed/skipped/not-completed/postponed/replaced/cancelled result vocabulary;
- finish-early result semantics;
- automatic inference that a completed Session proves an Actual;
- automatic inference that an Actual proves an Outcome;
- automatic inference that an Outcome is confirmed;
- broad measurement/quantity UX beyond the canonical Actual contract;
- solver/provider/AI authority over canonical realization facts.

These belong to later B10 work.

## 5. Execution and acceptance rule

B10-A is implemented in one pass across every required layer. There are no independently closable B10-A1/A2/A3/A4/A5 sub-blocks.

The assistant pushes coherent progress frequently. The user runs the final local automated gate after the complete B10-A candidate is ready. No GitHub Actions/CI are used for this workstream unless the user explicitly authorizes them.

The real-app/manual B10 walkthrough is **not** a B10-A closure requirement. It is deferred until the complete B10 chain is integrated.

## 6. Forward-only rule

All Alembic revisions already published on the branch are immutable. `20260925_70` and `20260925_71` are now published and therefore immutable as well. Any repair discovered by the local acceptance gate must use a new forward-only revision after `20260925_71`; never edit an older CP/M/B revision in place.

## 7. B10-A closure gate

B10-A is **not closed yet**. It closes only after the user's local gate regenerates the client and passes, proving at minimum:

- canonical append-only persistence/current-state behavior;
- heterogeneous NativeRef subject semantics and exact family enforcement;
- exact Session timing-state basis preservation when supplied;
- `Schedule != Session != Actual` and `Session END != Actual`;
- `Actual != Outcome != Confirmation` in code, API and UI;
- no Actual remains distinct from known non-realization;
- auth/self-scope and public-write idempotency;
- generated client produced by the repository generator;
- backend/API/web regression coverage;
- roadmap/map/handoff reconciled to the pending acceptance state.

After that user-run gate passes, B10-A may be marked closed and work moves to the next B10 slice. Manual real-app acceptance remains reserved for the integrated end-of-B10 walkthrough.
