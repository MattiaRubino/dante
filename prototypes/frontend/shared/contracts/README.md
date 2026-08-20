# DANTE — Shared Frontend Contracts

Status: **PRE-PRODUCTION FOUNDATION v0**

Framework-neutral contracts keep coded prototypes, tests and the future production web client aligned. They do **not** define PostgreSQL tables, Domain entities, FastAPI payloads or production endpoints.

## Files

- `home-stage.contract.json` — state/event/ownership/invariant contract.
- `home-stage.view-model.schema.json` — stage view-model boundary schema.
- `home-responsive.matrix.json` — desktop resize/reflow regression matrix.

Synthetic examples live under `../fixtures/`.

```text
Domain / canonical model
!= backend transport DTO
!= frontend view model
!= component state
```

Adapters map boundaries. UI components do not consume persistence/ORM shapes and do not call HTTP directly.
