# Timeline / Temporal-Operational — B10-A Closure Evidence

- **Status:** CLOSED / PROVEN
- **Date:** 2026-09-25
- **Branch:** `feature/timeline-temporal-operational`
- **Block:** B10-A — Actual / realization core
- **Proven Alembic head:** `20260925_74`
- **Proven topology:** `159|5|115|93|305|258|435`
- **Generated client commit:** `780c612dfbb48457784f0ef61cb2394c760f9e3d`
- **Manual real-app proof:** deliberately deferred to B10-E

## 1. Closed capability

B10-A activates explicit Actual realization over the existing CP6 Actual substrate for exactly these native subject families:

```text
Activity
Event
Occurrence
```

Canonical boundaries preserved:

```text
Session END != Actual
absence of Actual = unknown
absence of Actual != realization_occurred=false
Actual != Outcome != Confirmation
current accepted state != latest row
Session evidence != Actual identity
idempotency key != Actual identity
```

The accepted realization is append-only MaterialState truth with explicit current binding/history. Optional realized timing is bounded to `instant | start_only | interval`. Optional Session evidence preserves both the exact `session_ref` and exact `session_timing_material_state_ref`.

## 2. Persistence chain

```text
20260925_70  guarded self-scoped Actual realization authoring/read + idempotency receipt
20260925_71  exact Activity/Event/Occurrence family binding
20260925_72  forward repair for CP6 Actual/scoped-address owner creation order
20260925_73  canonical family-aware write/read signatures; retire hidden overloads
20260925_74  qualify current-history correction + canonical bounded FK name
```

Final B10-A database topology:

```text
Tables      159
Views       5
Routines    115
Triggers    93
Indexes     305
FKs         258
CHECKs      435
Enums       0
Domains     0
Sequences   0
```

Runtime does not receive raw mutation authority over the Actual realization family. Consequential writes remain behind bounded `SECURITY DEFINER` capabilities.

## 3. Vertical surface

B10-A closes the full vertical slice:

```text
PostgreSQL / Alembic / Dictionary / SQLAlchemy
→ Actual application service
→ Activity/Event/Occurrence HTTP API
→ OpenAPI
→ generated API client
→ Timeline Actual controls
→ local automated acceptance
```

The minimal Timeline surface distinguishes:

```text
no Actual                  → unknown
realization_occurred=true  → occurred
realization_occurred=false → known non-realization
```

Outcome, Confirmation, completion/result vocabulary, finish-early semantics and broader reconciliation remain outside B10-A.

## 4. Acceptance evidence

User-run local acceptance on 2026-09-25 established the final PostgreSQL/application/catalog gate:

```text
14 passed in 25.06s
POSTGRES TEST EXIT: 0
```

The passing command covered:

```text
tests/integration/temporal/test_b10_a_actual_realization.py
tests/integration/temporal/test_b10_a_actual_api.py
tests/integration/temporal/test_b08_a_session_runtime.py
tests/integration/temporal/test_b09_d_whole_block.py
tests/integration/database/test_current_catalog.py
tests/integration/database/test_database_current_catalog.py
```

Earlier in the same B10-A local gate, repository generation/check, API-client typecheck, web typecheck, focused web tests and OpenAPI inventory had already passed. The generated OpenAPI/Orval artifacts were then committed and pushed as:

```text
780c612dfbb48457784f0ef61cb2394c760f9e3d
feat(api-client): generate B10-A Actual contracts
```

No CI/GitHub Actions were used. Tests were run locally by the user.

## 5. Acceptance repairs discovered by local proof

The local gate found and closed real persistence defects rather than weakening the tests:

```text
_72  owner/scoped-address creation ordering under CP6 constraints
_73  hidden PostgreSQL overloads incompatible with exact Dictionary representation
_74  PL/pgSQL Actual current-history column ambiguity
_74  overlong receipt FK name normalized below PostgreSQL identifier limit
```

Dictionary, SQLAlchemy mappings, ACL expectations and current-catalog snapshots were reconciled to the final `_74` catalog.

## 6. Closure decision

B10-A is **CLOSED / PROVEN**.

No B10-A manual real-app walkthrough is required now. Per the workstream execution rule, the integrated real-app proof for B10 is performed only after B10-E.

Next block: **B10-B — Outcome**. Before implementation, its gate is only the proposed change/file surface for user approval.