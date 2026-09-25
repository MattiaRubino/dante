# Timeline / Temporal-Operational — B10 scope freeze

Status: **B10-A CLOSED / PROVEN; B10-B Outcome is the current cursor and requires a change/file gate before implementation**.

This document freezes the accepted B10-A semantics and the execution discipline for the remaining B10 blocks without changing the canonical Domain / Logical / Physical contracts.

## 1. Canonical semantic boundaries

The following distinctions are invariants, not implementation details:

- `Schedule != Session != Actual`
- `Session != Actual != Outcome`
- `Actual != Outcome != Confirmation`
- `Expected outcome != Outcome`
- `planned/intended != happened`
- `proposal != accepted effect`
- `projection != canonical truth`
- `current accepted state != latest row`
- `MaterialState != mutable runtime object`
- `idempotency key != Domain identity`
- `Undo != history rewind`

PostgreSQL remains the only canonical authority. API/UI/provider/AI/runtime projections may expose or propose facts, but may not become an alternative source of truth.

## 2. B10-A — Actual / realization core — CLOSED / PROVEN

B10-A was executed and accepted as **one complete vertical block**, not as A1/A2/A3 sub-blocks.

The block exposes the already-modelled `Actual` realization semantics as an explicit temporal capability without collapsing Actual into Session or Schedule and without introducing Outcome or Confirmation semantics early.

### Canonical owner

`dante.actual` is the stable scoped Actual owner. Its subject is `subject_native_ref`, not an Activity-only foreign key. The eligible public subject families are exactly Activity, Event and Occurrence.

### Write surface

The accepted write surface is append-only realization state:

1. create or address an Actual owner for one eligible `subject_native_ref`;
2. append one `actual_realization_state` MaterialState carrying `realization_occurred`;
3. optionally append `actual_realization_timing` (`extent_code`, `started_at`, `ended_at`) for that state;
4. optionally record one or more `actual_realization_session_basis` rows, preserving both `session_ref` and the exact `session_timing_material_state_ref` used as historical evidence;
5. change accepted/current realization by appending a new state and advancing the canonical current binding/history rather than mutating historical MaterialState payloads.

An Actual may be supported by zero or more Session/timing-state bases while Session and Actual retain separate identities. A Session ending never creates Actual implicitly.

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

No established Actual means unknown realization. It is not interpreted as failed, skipped, missed, cancelled or known non-realization. The Timeline surface renders absence as **sconosciuto**, distinct from explicit `realization_occurred=false`.

### Idempotency and authorization

Command idempotency is enforced at the public consequential write boundary. Reusing an idempotency key for the same accepted command replays the same semantic result; reusing it for a different payload fails. The idempotency key is not the Actual domain identity.

`Person != Account != Actor` remains binding. API authentication resolves the self Person through the existing access/auth boundary; Actual authoring does not turn Account or UI identity into a second canonical owner.

## 3. Accepted B10-A vertical implementation

Final forward-only migration chain:

```text
20260925_70  guarded self-scoped Actual realization authoring/read/history + immutable operation receipt
20260925_71  exact Activity/Event/Occurrence subject-family binding
20260925_72  repair CP6 Actual/scoped-address owner creation order
20260925_73  canonical family-aware write/read signatures; remove hidden overloads
20260925_74  qualify current-history correction + canonical bounded receipt FK name
```

Final proven database frontier:

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

Accepted vertical surface:

- SQLAlchemy mapping, Dictionary/scope and database overlay aligned to `_74`;
- backend `ActualApplication` guarded record/current/history behavior;
- HTTP API for Activity, Event and Occurrence Actual POST/GET plus Actual history;
- OpenAPI inventory for the seven public operations;
- generated OpenAPI/Orval client committed at `780c612dfbb48457784f0ef61cb2394c760f9e3d`;
- Timeline minimal Actual authoring for all three eligible subject families;
- focused PostgreSQL/application, public API, web and catalog regressions.

## 4. B10-A acceptance evidence

The user-run local acceptance culminated on 2026-09-25 with:

```text
14 passed in 25.06s
POSTGRES TEST EXIT: 0
```

The passing PostgreSQL/application/catalog command included:

```text
tests/integration/temporal/test_b10_a_actual_realization.py
tests/integration/temporal/test_b10_a_actual_api.py
tests/integration/temporal/test_b08_a_session_runtime.py
tests/integration/temporal/test_b09_d_whole_block.py
tests/integration/database/test_current_catalog.py
tests/integration/database/test_database_current_catalog.py
```

Earlier in the same local gate, repository generation/check, API-client typecheck, web typecheck, focused web tests and OpenAPI inventory had already passed. No CI/GitHub Actions were used.

Closure evidence: `timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

## 5. Acceptance repairs closed during B10-A

The local gate exposed real defects that were repaired forward-only rather than hidden by weakening tests:

- `_72`: CP6 owner/scoped-address creation order;
- `_73`: hidden function overloads incompatible with exact Dictionary/live representation;
- `_74`: PL/pgSQL output-column ambiguity in Actual current-history correction;
- `_74`: overlong receipt FK name reconciled to a stable PostgreSQL-safe identifier.

## 6. Explicitly deferred from B10-A

The following remain outside B10-A:

- Outcome assertion or outcome state;
- Confirmation assertion;
- partial/completed/skipped/not-completed/postponed/replaced/cancelled result vocabulary;
- finish-early result semantics;
- automatic inference that a completed Session proves an Actual;
- automatic inference that an Actual proves an Outcome;
- automatic inference that an Outcome is confirmed;
- broad measurement/quantity UX beyond the canonical Actual contract;
- solver/provider/AI authority over canonical realization facts.

## 7. Remaining B10 execution rule

B10-B, B10-C and B10-D are each implemented as one complete major block. The user runs one local automated gate only after that entire block is ready.

The integrated real-app/manual B10 walkthrough is **not** required for B10-A/B/C/D. It is performed once at B10-E after the whole B10 chain is integrated.

No GitHub Actions/CI are used unless the user explicitly authorizes them.

## 8. Forward-only rule

All published Alembic revisions are immutable. `20260925_70` through `20260925_74` are published candidate history and must not be edited in place. Any future repair uses a new forward-only revision after `_74`.

## 9. B10-B — Outcome cursor

B10-B has not started. Before implementation, the assistant presents only the proposed modification/file surface and the user approves or changes that gate.

Binding boundaries entering B10-B:

- `Actual != Outcome`;
- `Expected outcome != Outcome`;
- `Outcome != Confirmation`;
- `Session END != Outcome`;
- absence of Outcome is not implicit success or failure.

Any completed/partial/skipped/not-completed/postponed/replaced/cancelled vocabulary and finish-early behavior must be mapped only after verifying the repository's current Product/Domain/Logical/Physical Outcome authority. Do not invent a generic flat status enum from UI wording alone.

B10-C owns Confirmation. B10-D owns the reconciliation workflow. Do not invent a generic `Resolution` ontology entity unless repository authority explicitly requires it.

## 10. Current gate

**Current action:** approve the B10-B Outcome change/file gate. After approval, implement B10-B as one complete block, then hand the user one local automated test command. Manual real-app validation remains reserved for B10-E.