# Timeline / Temporal-Operational — B10 scope freeze

Status: **B10-A approved for implementation; block not yet proven**.

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

The block must expose the already-modelled `Actual` realization semantics as an explicit temporal capability without collapsing Actual into Session or Schedule and without introducing Outcome or Confirmation semantics early.

### Canonical owner

`dante.actual` is the stable scoped Actual owner. Its subject is `subject_native_ref`, not an Activity-only foreign key. The existing NativeRef eligibility contract bounds the subject family to the canonical eligible native families (currently Activity, Event and Occurrence). B10-A must preserve that heterogeneous subject model and must not replace it with an `activity_id` shortcut.

### Write surface

The accepted write surface is append-only realization state:

1. create or address an Actual owner for one eligible `subject_native_ref`;
2. append one `actual_realization_state` MaterialState carrying `realization_occurred`;
3. optionally append `actual_realization_timing` (`extent_code`, `started_at`, `ended_at`) for that state;
4. optionally record one or more `actual_realization_session_basis` rows, preserving both `session_ref` and the exact `session_timing_material_state_ref` used as historical evidence;
5. change accepted/current realization by appending a new state and advancing the canonical current binding/history rather than mutating historical MaterialState payloads.

An Actual may be supported by zero or more Session/timing-state bases while Session and Actual retain separate identities. A Session ending must never create Actual implicitly.

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

No established Actual means unknown realization. It must not be interpreted as failed, skipped, missed, cancelled or known non-realization.

### Idempotency and authorization

Command idempotency is required at the public consequential write boundary. Reusing an idempotency key for the same accepted command must replay the same semantic result; reusing it for a different payload must fail. The idempotency key is not the Actual domain identity.

`Person != Account != Actor` remains binding. Where canonical MaterialState/current-binding functions require actor/audit references, API authentication identity must be resolved through the existing access/auth boundary rather than written as a Person or Account shortcut.

## 3. Approved B10-A modification surface

B10-A may change the following areas as needed to deliver the complete vertical capability:

- PostgreSQL/Alembic only if the already-published Actual substrate is insufficient; any repair is forward-only after the current head;
- SQLAlchemy Actual mappings, Dictionary/scope and DB overlay documentation when persistence alignment requires it;
- temporal backend application/domain-adapter code;
- HTTP API and OpenAPI contract;
- generated API client through the repository generator only, never by hand;
- Timeline web read/authoring surface for Actual;
- focused backend PostgreSQL/API tests, generated-contract tests, web tests and required regressions;
- workstream roadmap/map/handoff documentation from actual implementation evidence.

No migration is created merely because a new B block has started. Existing persistence is reused when sufficient.

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

These belong to later B10 blocks.

## 5. Execution and acceptance rule

B10-A is implemented in one pass across every required layer. There are no independently closable B10-A1/A2/A3/A4/A5 sub-blocks.

The assistant pushes coherent progress frequently. The user runs the final local automated gate after the complete B10-A candidate is ready. No GitHub Actions/CI are used for this workstream unless the user explicitly authorizes them.

The real-app/manual B10 walkthrough is **not** a B10-A closure requirement. It is deferred until the end of B10-E, after the complete B10 chain is integrated.

## 6. Forward-only rule

All Alembic revisions already published on the branch are immutable. If the persistence review finds a gap, create a new revision after the current head. Never edit an older CP/M/B revision in place.

## 7. B10-A closure gate

B10-A closes only after the complete candidate exists and the user's local automated gate passes, proving at minimum:

- canonical append-only persistence/current-state behavior;
- heterogeneous NativeRef subject semantics;
- exact Session timing-state basis preservation when supplied;
- `Schedule != Session != Actual` and `Session END != Actual`;
- `Actual != Outcome != Confirmation` in code, API and UI;
- no Actual remains distinct from known non-realization;
- auth Actor resolution and public-write idempotency;
- generated client produced by the repository generator;
- backend/API/web regression coverage;
- roadmap/map/handoff reconciled from evidence.

After this gate passes, B10-A is marked closed and work moves to B10-B. The manual real-app acceptance remains reserved for end-of-B10-E.