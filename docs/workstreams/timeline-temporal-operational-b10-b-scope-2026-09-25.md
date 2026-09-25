# Timeline / Temporal-Operational — B10-B Outcome scope

Status: **APPROVED / IN PROGRESS — 2026-09-25**

B10-B is executed as one complete vertical block. The user runs one local automated gate only after the entire B10-B implementation is ready. No GitHub Actions/CI are used. The integrated manual real-app proof remains deferred until B10-E.

## Canonical entry frontier

```text
B10-A Actual / realization core  CLOSED / PROVEN
Alembic                         20260925_74
Topology                        159|5|115|93|305|258|435
Generated client                780c612dfbb48457784f0ef61cb2394c760f9e3d
```

## Binding semantic boundaries

B10-B must preserve:

```text
Actual != Outcome
Expected outcome != Outcome
Outcome != Confirmation
Outcome != Observation
Outcome != lifecycle / operational state
Session END != Outcome
absence of Outcome != success/failure
current accepted state != latest row
idempotency key != Domain identity
```

Outcome is a contextual result/disposition established for a specific Actual realization. It is optional: an Actual may exist without an Outcome. B10-B must not manufacture an Outcome simply because an Activity/Event/Occurrence elapsed, a Session ended, or an Actual exists.

The canonical Domain contract explicitly rejects one universal Outcome enum. Vocabulary such as completed, partial, skipped, passed, failed, approved, rejected, postponed, replaced or changes-requested is contextual and may not be flattened into a single global lifecycle/status field.

## Approved change/file surface

B10-B may modify the following areas only as required to close Outcome end-to-end:

1. PostgreSQL persistence and forward-only Alembic revisions after `20260925_74`.
2. SQLAlchemy persistence mappings and mapping registration.
3. Database Dictionary/scope plus Timeline/Temporal-Operational database overlay and database README/current frontier.
4. Temporal backend application capability and public API/OpenAPI.
5. Generated API client through the repository generator only; generated files are never hand-edited.
6. Minimal Timeline Outcome read/author/correct surface under the existing temporal detail ownership.
7. Focused PostgreSQL/application/API/web/catalog regression tests.
8. Roadmap/map/handoff/closure evidence after the user-run local acceptance gate.

## Persistence direction to verify/implement

The implementation must derive from the accepted Domain/Logical/Physical authority. At the B10-B entry point there is no materialized Outcome persistence family equivalent to the proven Actual family, so a new bounded persistence capability is expected.

The persistence design must:

- anchor Outcome to a specific canonical `Actual`, not directly reinterpret Schedule/Session as result truth;
- preserve stable Outcome identity separately from corrections/materialized accepted state;
- support append-only correction/current-history semantics rather than in-place history rewrite;
- keep result vocabulary contextual/typed rather than introduce a universal Outcome status enum;
- preserve self-scope/auth and consequential-write idempotency patterns already proven in B08-B10-A;
- keep Confirmation/authority/provenance semantics outside B10-B.

## Explicitly deferred

B10-B does not implement:

- Confirmation or epistemic acceptance policy;
- B10-D reconciliation/resolution workflow;
- a generic `Resolution` ontology entity;
- automatic Session -> Actual inference;
- automatic Actual -> Outcome inference;
- automatic Outcome -> Confirmation inference;
- AI/provider authority over canonical result truth;
- the integrated manual real-app walkthrough, which remains B10-E.

## Acceptance rule

Implementation is not marked CLOSED merely because files are committed. Once the full B10-B candidate is ready, the assistant provides one unified local command. The user executes generation/check/typecheck/web/backend/PostgreSQL acceptance locally. Only a green user-run gate moves B10-B to CLOSED / PROVEN.