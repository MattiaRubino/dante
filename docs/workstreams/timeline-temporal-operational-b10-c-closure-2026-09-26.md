# Timeline / Temporal-Operational — B10-C Confirmation closure evidence

Status: **CLOSED / PROVEN — 2026-09-26**

B10-C materializes contextual Confirmation as a distinct optional attestation after Outcome.

A post-closure review on 2026-09-26 found one public-contract documentation gap only: the runtime already returned `201` for creation and `200` for idempotent replay, while the generated OpenAPI artifact described the POST success only as `200`. Persistence and Confirmation semantics were not reopened. Source + regression test now document the complete HTTP response contract; generated OpenAPI/Orval artifacts must be refreshed through repository tooling before B10-D starts.

## Proven boundaries

```text
Confirmation != Outcome
Confirmation != Authority != Verification
0..N Confirmation per exact Outcome disposition MaterialState
identity = (target MS, confirmer, purpose)
stance_code is contextual, not confirmed=true
Outcome correction does not transfer old Confirmation
current accepted Confirmation state != latest row
idempotency receipt != Confirmation identity
absence of Confirmation != false
no automatic Confirmation
```

## Proven persistence frontier

Published immutable revision:

```text
20260925_79  Confirmation capability + scoped family/facet + dispatch
```

Proven database frontier:

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
```

Canonical physical family:

```text
dante.confirmation
dante.confirmation_attestation_state
dante.confirmation_attestation_current_history
dante.confirmation_attestation_operation
facet: confirmation.attestation
```

## Proven public/application behavior

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/confirmations/{confirmation_ref}/history
```

Write records the authenticated self as confirmer and does not require Outcome ownership. List is Outcome-owner scoped and returns 0..N, including historical pins. History is visible to the confirmer or the Outcome owner.

Runtime POST semantics proven by the API gate:

```text
new Confirmation       -> HTTP 201
idempotent replay      -> HTTP 200
validation/not-found/conflict/security failures
                       -> bounded ProblemDetails
```

The B10-C vertical includes:

```text
PostgreSQL capability
SQLAlchemy mappings/addressing
Dictionary + scope/current-catalog reconciliation
Confirmation runtime/application/API
OpenAPI inventory
remote web data source + Timeline Confirmation controls
focused backend/API/web tests
generated OpenAPI/Orval client artifacts
```

## User-local automated proof

Original non-PostgreSQL gate, 2026-09-26:

```text
API generation       PASS
generated check      PASS (339 files)
API client typecheck PASS
web typecheck        PASS
web tests            8/8 PASS
```

PostgreSQL slice, 2026-09-26:

```text
19 passed in 29.46s
```

That slice covered OpenAPI inventory, Dictionary scope, B10-C Confirmation application/API, B10-B Outcome regression, and both current-catalog checks.

Regression slice, 2026-09-26:

```text
19 passed in 39.76s
```

That slice covered B10-A Actual, B09 Responsibility/Participation, and B08 Session.

No CI/GitHub Actions were used. Acceptance proof was executed locally by the user.

## Generated client and post-closure hardening

Original generated B10-C artifacts were committed at:

```text
30f15adf  feat(api-client): generate B10-C Confirmation contracts
```

Post-closure source hardening:

```text
1f4c3415  fix(temporal): document B10-C confirmation HTTP outcomes
58947b45  test(temporal): freeze B10-C confirmation response contract
```

The generated OpenAPI/Orval files are intentionally **not hand-edited**. They must be regenerated through `pnpm api:generate`, checked for determinism, and committed before the B10-D gate begins.

## Deferred

B10-C deliberately does not add:

```text
B10-D reconciliation / resolution workflow
a generic Resolution ontology entity
automatic Outcome -> Confirmation
AI/provider as human confirmer or canonical authority
integrated real-app B10 walkthrough
```

The integrated manual real-app proof remains deferred to B10-E.

## Closure / continuation

```text
B10-A  CLOSED / PROVEN
B10-B  CLOSED / PROVEN
B10-C  CLOSED / PROVEN
B10-C  post-closure public-contract hardening awaiting generated refresh
B10-D  BLOCKED until that generated refresh is deterministic and committed
```
