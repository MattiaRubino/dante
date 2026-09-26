# Timeline / Temporal-Operational — B10 scope freeze

Status: **B10-A/B10-B/B10-C CLOSED / PROVEN; B10-D not started**.

This document freezes the accepted B10-A semantics and the implementation candidate for B10-B without changing the canonical Domain / Logical / Physical boundaries.

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

B10-A was executed and accepted as one complete vertical block. `dante.actual` is the stable scoped owner for Activity, Event or Occurrence reality. Realization corrections append immutable MaterialStates and advance explicit current/history bindings. Session remains evidence only and never manufactures Actual.

Final proven B10-A frontier:

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

The user-run acceptance on 2026-09-25 completed with `14 passed` and `POSTGRES TEST EXIT: 0`, after generation/check, client typecheck, web typecheck, focused web tests and OpenAPI inventory had also passed. No CI/GitHub Actions were used.

Closure evidence: `timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

## 3. B10-B — Outcome implementation candidate

B10-B materializes Outcome as a distinct contextual result owner downstream of one canonical Actual.

### Identity and context

`dante.outcome` is keyed by a stable `outcome_ref` and belongs to exactly one `(actual_ref, vocabulary_code)` pair. The `vocabulary_code` identifies the domain-specific result vocabulary. It is not a universal Outcome enum.

A single Actual may therefore have multiple Outcome owners when separate contextual vocabularies are genuinely required, while ordinary corrections within one vocabulary retain the same Outcome identity.

### Result state

The accepted material facet is `outcome.result`.

Each immutable `outcome_result_state` carries:

- `material_state_ref`;
- `outcome_ref`;
- contextual `result_code`;
- optional bounded `note`.

B10-B does not define a global completed/partial/skipped taxonomy. A code such as `decision.reached` or `completed` is meaningful only under the explicitly supplied vocabulary/domain contract.

### Currentness and history

Current accepted Outcome state is selected explicitly through `scoped_current_material_state` and `outcome_result_current_history`; it is never inferred from row recency. Corrections append a new MaterialState, close the previous current-history interval and advance the current binding.

The canonical history capability currently returns chronology oldest-to-newest by `current_from_at`.

### Absence

No Outcome for an `(Actual, vocabulary)` means no result has been established for that context. Absence is not success, failure, skipped, incomplete or confirmed.

An Outcome cannot be established without an owned canonical Actual. Session end and Actual occurrence do not automatically create Outcome.

### Idempotency and scope

`outcome_result_operation` protects consequential writes. Same operation id plus same intent replays the accepted result; reuse for another intent is rejected. Expected-current MaterialState provides optimistic correction conflict detection.

Authorization remains self-scoped through the owned Actual. Raw Outcome mutation is not a second runtime authority.

## 4. B10-B candidate persistence

Candidate forward-only migration:

```text
20260925_75  contextual Outcome owner/result/current-history/operation capability
```

Candidate database frontier, awaiting the user's local proof:

```text
Alembic  20260925_75
Topology 163|5|119|93|316|268|443
```

Last proven database frontier remains B10-A `_74` until the B10-B local gate passes.

The `_75` candidate adds:

- `dante.outcome`;
- `dante.outcome_result_state`;
- `dante.outcome_result_current_history`;
- `dante.outcome_result_operation`;
- scoped family `outcome`;
- material facet `outcome.result`;
- guarded `_outcome_actual_owned`, `record_self_actual_outcome`, `get_self_actual_outcome` and `list_self_outcome_history` capabilities;
- SQLAlchemy mapping, Dictionary/scope and catalog representation.

## 5. B10-B candidate application/API surface

Backend `OutcomeApplication` exposes:

- record/correct one contextual Outcome by `(actual_ref, vocabulary_code)`;
- retrieve current accepted Outcome;
- retrieve immutable current-history chronology;
- idempotent replay, operation-reuse rejection and expected-current conflict handling.

Public HTTP candidate:

```text
POST /api/v1/temporal/actuals/{actual_ref}/outcomes/{vocabulary_code}
GET  /api/v1/temporal/actuals/{actual_ref}/outcomes/{vocabulary_code}
GET  /api/v1/temporal/outcomes/{outcome_ref}/history
```

Operation IDs:

```text
temporal_record_actual_outcome
temporal_get_actual_outcome
temporal_list_outcome_history
```

The write body carries `operation_id`, optional `expected_material_state_ref`, `result_code` and optional `note`; the vocabulary is part of the resource path and is not duplicated in the payload.

## 6. B10-B candidate Timeline surface

The Timeline keeps Actual and Outcome distinct. The Outcome control is rendered downstream of the existing Actual control for Activity, Event and Occurrence subjects.

The user explicitly selects a contextual vocabulary, loads the current Outcome for that `(Actual, vocabulary)`, and may register or correct `result_code` plus an optional note. The surface never creates an Outcome when Actual is absent and never treats an ended Session or `realization_occurred=true` as a result.

## 7. B10-B proof surface awaiting local execution

Focused candidate proof now includes:

```text
apps/backend/tests/integration/temporal/test_b10_b_outcome.py
apps/backend/tests/integration/temporal/test_b10_b_outcome_api.py
apps/web/src/features/temporal/outcome-controls.test.tsx
apps/backend/tests/test_temporal_openapi_inventory.py
apps/backend/tests/integration/database/test_database_current_catalog.py
```

The local gate must also retain B10-A/B09/B08 regressions. The user runs the tests locally; the assistant does not run CI or GitHub Actions.

Generated OpenAPI/Orval artifacts are intentionally regenerated locally only after this candidate source contract is stable, then committed before B10-B is marked closed.

## 8. Explicitly deferred from B10-B

B10-B does not introduce:

- Confirmation;
- automatic confirmation from Outcome;
- automatic Outcome from Actual or Session;
- a global Outcome status enum;
- B10-D reconciliation/resolution workflow;
- solver/provider/AI authority over canonical result facts;
- the integrated manual/real-app B10 walkthrough.

## 9. Remaining B10 execution rule

B10-C and B10-D are each implemented as one complete major block. The user runs one local automated gate only after the whole block is ready.

The integrated real-app/manual B10 walkthrough is performed once at B10-E after the whole B10 chain is integrated.

No GitHub Actions/CI are used unless the user explicitly authorizes them.

## 10. Forward-only rule

Published Alembic revisions remain immutable. `20260925_70` through `20260925_75` form the current candidate history. Any repair discovered by the local B10-B gate uses a new forward-only revision after `_75`.

## 11. Current action

**Current action:** B10-C local proof is green and closure docs are reconciled. Commit the generated client only when the user asks. Do not perform the manual real-app proof yet. Do not start B10-D until the user approves that gate.