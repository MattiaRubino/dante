# Timeline / Temporal-Operational — B10 scope freeze

Status: **B10-A / B10-B / B10-C CLOSED / PROVEN; B10-D not started**.

This document is the current B10 semantic and execution authority. It freezes the proven Actual → Outcome → Confirmation chain without redefining the canonical Domain / Logical / Physical model.

A post-closure B10-C OpenAPI hardening was added on 2026-09-26 so the public contract describes `201` creation, `200` idempotent replay and bounded ProblemDetails failures. Source + regression test are committed; generated OpenAPI/Orval artifacts must be refreshed only through repository generation tooling before B10-D starts.

## 1. Permanent B10 boundaries

```text
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Expected outcome != Outcome
Outcome != Observation
Outcome != lifecycle / operational state
Confirmation != Authority
Confirmation != Verification
Confirmation != Decision / Approval
Confirmation != universal truth
planned/intended != happened
proposal != accepted effect
projection != canonical truth
current accepted state != latest row
MaterialState != mutable runtime object
idempotency key != Domain identity
Undo != history rewind
```

PostgreSQL remains canonical authority. API, generated client, frontend, provider, solver and AI are projections/capabilities and may not create a second truth model.

## 2. Proven execution frontier

```text
B10-A Actual         CLOSED / PROVEN  2026-09-25
B10-B Outcome        CLOSED / PROVEN  2026-09-25
B10-C Confirmation   CLOSED / PROVEN  2026-09-26
B10-D Reconciliation NOT STARTED
B10-E Integration    NOT STARTED
```

Persistence frontier:

```text
20260925_74  B10-A Actual
20260925_75  initial B10-B Outcome capability
20260925_76  canonical Outcome disposition reconciliation
20260925_77  Outcome ScopedAddress owner-dispatch repair
20260925_78  Outcome MaterialState totality-dispatch repair
20260925_79  B10-C Confirmation capability + dispatch
```

Published revisions are immutable. Any future persistence correction uses a new forward-only migration.

Current proven database frontier:

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
```

## 3. B10-A — Actual / realization core — CLOSED / PROVEN

Actual is the stable scoped reality owner for Activity, Event or Occurrence realization.

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence of Actual
Session evidence != Actual identity
current accepted realization != latest row
Actual != Outcome != Confirmation
```

Canonical family:

```text
dante.actual
dante.actual_realization_state
dante.actual_realization_current_history
dante.actual_realization_operation
facet: actual.realization
```

Public surface:

```text
POST/GET /api/v1/temporal/activities/{activity_ref}/actual
POST/GET /api/v1/temporal/events/{event_ref}/actual
POST/GET /api/v1/temporal/occurrences/{occurrence_ref}/actual
GET      /api/v1/temporal/actuals/{actual_ref}/history
```

Proven frontier: `20260925_74` / topology `159|5|115|93|305|258|435`.

Closure evidence: `timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

## 4. B10-B — Outcome disposition — CLOSED / PROVEN

The temporary `_75` vocabulary/result representation is superseded. **Do not reintroduce** `vocabulary_code`, `result_code`, `outcome.result`, Outcome identity per vocabulary, or `/outcomes/{vocabulary_code}` routes.

Canonical model:

```text
one stable Outcome per Actual
Outcome identity != disposition MaterialState
Outcome disposition is contextual, not a universal enum
Outcome disposition is pinned to one exact Actual realization MaterialState
Actual correction does not reinterpret an older Outcome disposition
current accepted Outcome state != latest row
idempotency receipt != Outcome identity
absence of Outcome != success / failure / skipped
Outcome != Confirmation
```

Canonical physical family:

```text
dante.outcome
dante.outcome_disposition_state
dante.outcome_disposition_current_history
dante.outcome_disposition_operation
facet: outcome.disposition
```

Each disposition state carries:

```text
outcome_ref
actual_realization_material_state_ref
material_state_ref
disposition_code
```

Public surface:

```text
POST /api/v1/temporal/actuals/{actual_ref}/outcome
GET  /api/v1/temporal/actuals/{actual_ref}/outcome
GET  /api/v1/temporal/outcomes/{outcome_ref}/history
```

Write contract:

```text
operation_id
actual_realization_material_state_ref
expected_material_state_ref
disposition_code
```

Proven frontier: `20260925_78` / topology `163|5|119|93|317|268|440`.

Generated B10-B client: `58757fbb`.

Closure evidence: `timeline-temporal-operational-b10-b-closure-2026-09-25.md`.

## 5. B10-C — Confirmation — CLOSED / PROVEN

Confirmation is an optional contextual attestation by one confirmer toward one exact Outcome disposition MaterialState for one purpose.

```text
Confirmation != Outcome
Confirmation != Authority != Verification
absence of Confirmation != false / rejected / untrusted
0..N Confirmation per exact Outcome disposition MaterialState
identity = (target Outcome MS, confirmer Person, purpose)
stance_code is contextual, not confirmed=true
Outcome correction does not transfer old Confirmation
contrasting Confirmations from different actors remain representable
current accepted Confirmation state != latest row
idempotency receipt != Confirmation identity
no automatic Confirmation from Outcome / Actual / Session / click
```

Canonical physical family:

```text
dante.confirmation
dante.confirmation_attestation_state
dante.confirmation_attestation_current_history
dante.confirmation_attestation_operation
facet: confirmation.attestation
```

Public surface:

```text
POST /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/outcomes/{outcome_ref}/confirmations
GET  /api/v1/temporal/confirmations/{confirmation_ref}/history
```

Write body:

```text
operation_id
outcome_disposition_material_state_ref
expected_material_state_ref
purpose_code
stance_code
```

The authenticated self is the confirmer. Writing a Confirmation does not mutate the Outcome and does not itself establish Authority or universal truth.

List access remains Outcome-owner scoped. Confirmation history is available to the confirmer or the Outcome owner under the bounded B10-C capability.

Proven frontier: `20260925_79` / topology `167|5|123|93|329|279|446`.

Original generated B10-C client: `30f15adf` (339 files). After the 2026-09-26 response-contract hardening, generated artifacts must be refreshed through `pnpm api:generate`; never hand-edit generated sources.

Closure evidence: `timeline-temporal-operational-b10-c-closure-2026-09-26.md`.

## 6. B10-C post-closure public-contract hardening

Runtime behavior already proven by the B10-C API gate is:

```text
new Confirmation       -> HTTP 201
idempotent replay      -> HTTP 200
malformed/auth/security/not-found/conflict/validation/unexpected
                      -> bounded ProblemDetails responses
```

The original generated OpenAPI artifact described the POST success only as `200`. Source has now been hardened so OpenAPI explicitly carries creation/replay/failure response truth, with a dedicated regression test.

This hardening changes no Confirmation persistence semantics and requires no migration after `_79`.

Until generated OpenAPI/Orval artifacts are refreshed and committed, do not start B10-D.

## 7. B10-D boundary — not started

B10-D owns reconciliation / resolution workflow after Actual, Outcome and Confirmation are all distinct canonical layers.

It must not silently introduce:

```text
Confirmation = Decision / Authority
latest row = accepted resolution
conflicting Confirmation deletion
Outcome rewrite as reconciliation
Actual rewrite as reconciliation
generic Resolution ontology entity without accepted Domain evidence
provider / AI authority over canonical truth
```

B10-D scope must be prepared against current Domain / Logical / Physical authority before implementation.

## 8. B10-E boundary

The single integrated real-app/manual B10 walkthrough remains deferred to B10-E after B10-D is complete.

No separate B10-C manual proof is required now.

## 9. Collaboration and generation discipline

```text
user runs local tests
do not use GitHub Actions / CI
published migrations are immutable
fix persistence forward-only
generated API client comes only from repository generator
never hand-edit packages/api-client/src/generated/*
PostgreSQL remains canonical truth
```

## 10. Exact continuation

```text
1. pull the current branch;
2. regenerate OpenAPI/Orval from source through repository tooling;
3. run generated determinism + focused B10-C OpenAPI contract check;
4. commit/push generated artifacts only if deterministic;
5. reconcile the post-closure hardening checkpoint;
6. then prepare the B10-D modification gate.
```
