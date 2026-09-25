# Timeline / Temporal-Operational — B10 scope freeze

Status: **B10-A scope frozen; implementation not yet accepted**.

This document is the implementation gate for the first open block after B09. It narrows B10 without changing the canonical Domain / Logical / Physical contracts.

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

B10-A exposes the already-modelled `Actual` realization semantics as an explicit temporal capability. It does **not** collapse Actual into Session or Schedule and it does **not** introduce Outcome or Confirmation semantics early.

### Canonical owner

`dante.actual` is the stable scoped Actual owner. Its subject is `subject_native_ref`, not an Activity-only foreign key. The existing NativeRef eligibility contract bounds the subject family to the canonical eligible native families (currently Activity, Event and Occurrence). B10-A must preserve that heterogeneous subject model and must not replace it with an `activity_id` shortcut.

### Write surface

The minimum accepted write surface is append-only realization state:

1. create or address an Actual owner for one eligible `subject_native_ref`;
2. append one `actual_realization_state` MaterialState carrying `realization_occurred`;
3. optionally append `actual_realization_timing` (`extent_code`, `started_at`, `ended_at`) for that state;
4. optionally record one or more `actual_realization_session_basis` rows. A basis is not merely a Session id: it preserves both `session_ref` and the exact `session_timing_material_state_ref` used as historical evidence;
5. change accepted/current realization by appending a new state and advancing the canonical current binding/history rather than mutating historical MaterialState payloads.

The capability must preserve the database rule that an Actual may be supported by zero or more Session/timing-state bases, while Session and Actual retain separate identities.

### Read surface

Reads must expose canonical current accepted realization state, not "the latest row" by accident. `dante.actual_current_realization` is the bounded current capability surface over `scoped_current_material_state` for facet `actual.realization`; historical chronology remains separate.

At minimum a caller must be able to retrieve:

- `actual_ref` and `subject_native_ref`;
- current accepted realization `material_state_ref` and `realization_occurred`;
- current accepted realization timing when present;
- exact Session/timing-state basis references when present;
- immutable historical facts separately from the current projection when history is exposed.

### State vocabulary

The canonical realization payload is the existing `realization_occurred` boolean plus the optional timing extent contract (`instant`, `start_only`, `interval`). B10-A must not invent a second status enum or UI persistence vocabulary.

### Idempotency

Command idempotency is required at the public write boundary. Reusing an idempotency key for the same accepted command must replay the same semantic result; reusing it for a different payload must fail. The idempotency key is not the Actual domain identity.

### Authorization and actor semantics

`Person != Account != Actor` remains binding. Where canonical MaterialState/current-binding functions require actor/audit references, API authentication identity must be resolved through the existing access/auth boundary rather than written as a Person or Account shortcut.

## 3. Explicitly deferred from B10-A

The following are **not** part of B10-A and must not be smuggled into generic payloads:

- Outcome assertion or outcome state;
- Confirmation assertion;
- automatic inference that a completed Session proves an Actual;
- automatic inference that an Actual proves an Outcome;
- automatic inference that an Outcome is confirmed;
- broad measurement/quantity UX beyond what the canonical Actual contract already requires;
- solver/provider/AI authority over canonical realization facts.

These belong to later B10 slices after Actual is proven independently.

## 4. Implementation order

B10 proceeds in this order:

1. **B10-A1 — contract/catalog probe**: verify the published PostgreSQL Actual tables, current views, functions/triggers, SQLAlchemy mappings, Dictionary/scope and DB docs agree with Domain/Logical/Physical semantics. Repair only by forward migration if a published database contract is insufficient.
2. **B10-A2 — backend application service**: add explicit Actual commands/queries using canonical PostgreSQL semantics and actor/idempotency boundaries.
3. **B10-A3 — API/OpenAPI**: expose the smallest public Actual contract; regenerate the API client through the repository generator only.
4. **B10-A4 — web**: add the smallest truthful realization interaction/read surface; no Outcome/Confirmation conflation.
5. **B10-A5 — acceptance**: backend PostgreSQL integration tests, API/client/web tests and a real-app proof. Only then mark B10-A closed in roadmap/map/handoff.

## 5. Forward-only rule

All Alembic revisions already published on the branch are immutable. If B10-A1 finds a persistence gap, create a new revision after the current head. Never edit an older CP/M/B revision in place.

## 6. Closure gate

B10-A is not closed merely because an endpoint exists. Closure requires evidence that:

- persistence and current-state semantics are canonical and append-only;
- heterogeneous NativeRef subject semantics are preserved;
- Session basis preserves the exact timing-state evidence, not only Session identity;
- `Schedule != Session != Actual` is preserved in code and API;
- `Actual != Outcome != Confirmation` is preserved in code, API and UI;
- auth Actor resolution and idempotency behave correctly;
- generated client is regenerated, never hand-edited;
- local tests pass on the user's worktree;
- the real app demonstrates the accepted behavior;
- roadmap, map and handoff are updated from evidence, not intention.
