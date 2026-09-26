# Timeline / Temporal-Operational — B10-C Confirmation scope

Status: **APPROVED / CLOSED / PROVEN 2026-09-26** — closure evidence: `timeline-temporal-operational-b10-c-closure-2026-09-26.md`.

Post-closure note: the 2026-09-26 review found an OpenAPI response-description gap only. Confirmation semantics/persistence remain proven at `_79`; source + regression test now document `201` creation, `200` idempotent replay and bounded ProblemDetails failures. Generated OpenAPI/Orval artifacts must be refreshed through repository tooling before B10-D starts.

B10-C was executed as one complete vertical block after proven B10-B. The user ran the local automated gate; no GitHub Actions/CI were used. No real-app proof is required before B10-E.

## Canonical entry frontier

```text
B10-B Outcome  CLOSED / PROVEN
Alembic        20260925_78
Topology       163|5|119|93|317|268|440
Generated      335 files at 58757fbb
```

## Binding semantic boundaries

```text
Confirmation != Outcome != Actual
Confirmation != Authority
Confirmation != Verification
Confirmation != universal truth
absence of Confirmation != false / rejected / untrusted
material target change does not transfer Confirmation
0..N Confirmation per Outcome disposition MaterialState
contrasting Confirmations from different actors remain representable
current accepted Confirmation state != latest row
idempotency receipt != Confirmation identity
no confirmed=true universal flag
no automatic Confirmation from Outcome / Session / click
```

A Confirmation is an optional contextual attestation by one confirmer toward one exact Outcome disposition MaterialState for one purpose. Stance is a contextual code, not a boolean.

Identity:

```text
one Confirmation owner per
  (outcome_disposition_material_state_ref, confirmer_person_ref, purpose_code)
```

Outcome correction creates a new Outcome MaterialState. Existing Confirmation owners stay pinned to the old state. A later Confirmation on the new state is a new owner.

## Persistence

Forward-only revision:

```text
20260925_79  Confirmation owner / attestation / current-history / operation
             + scoped family confirmation
             + facet confirmation.attestation
             + ScopedAddress owner dispatch
             + MaterialState totality dispatch
```

Proven topology:

```text
167|5|123|93|329|279|446
```

Physical family:

```text
dante.confirmation
dante.confirmation_attestation_state
dante.confirmation_attestation_current_history
dante.confirmation_attestation_operation
facet: confirmation.attestation
```

Write does not require Outcome ownership; confirmer is always authenticated self. List requires Outcome ownership and returns 0..N current Confirmations, including those still pinned to historical Outcome states. History is visible to the confirmer or the Outcome owner.

## Public surface

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/confirmations/{confirmation_ref}/history
```

```text
temporal_record_outcome_confirmation
temporal_list_outcome_confirmations
temporal_list_confirmation_history
```

Write body: `operation_id`, `outcome_disposition_material_state_ref`, optional `expected_material_state_ref`, `purpose_code`, `stance_code`.

POST runtime contract:

```text
new accepted Confirmation  -> 201
idempotent replay          -> 200
bounded failures           -> ProblemDetails
```

## Timeline

Confirmation controls sit beside Outcome. Visible states:

```text
Outcome absent
Outcome present + no Confirmation
explicit Confirmation
```

Absence is not rendered as false. Outcome save / Session / click do not create Confirmation.

## Explicitly deferred

```text
B10-D reconciliation / resolution workflow
generic Resolution ontology entity
automatic Confirmation
AI/provider as human confirmer or canonical authority
real-app proof before B10-E
```

## Local proof

The user-run B10-C gate passed on 2026-09-26. Closure evidence records:

```text
API generation        PASS
generated check       PASS (339 files)
API client typecheck  PASS
web typecheck         PASS
web tests             8/8 PASS
PostgreSQL slice      19 passed
regression slice      19 passed
```

The subsequent OpenAPI hardening adds no persistence semantics and does not reopen `_79`. It requires only regeneration/determinism plus the focused OpenAPI contract test before B10-D begins.
