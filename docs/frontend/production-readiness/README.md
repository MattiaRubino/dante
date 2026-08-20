# DANTE — Frontend Pre-Production Foundation v0

- Status: **CURRENT PRE-PRODUCTION ENGINEERING BASELINE**
- Scope: frontend contracts, production handoff shape and quality gates
- Branch: `prototype/frontend`

## Purpose

DANTE frontend work is not treated as disposable visual mock-up work. The coded prototype remains an UX/visual oracle, while its durable behavior, data boundaries, state ownership, responsive rules and validation are shaped so a future production client can implement them without rediscovering product semantics.

This foundation does **not** start `apps/web`, select exact package/runtime versions or define backend endpoints.

## Core rule

```text
prototype renderer may change
framework may change
transport implementation may change

product behavior + state contract + view-model boundary + quality invariants
must remain traceable and testable
```

## Authorities

- `component-architecture.md` — component/state/geometry ownership.
- `backend-integration-contract.md` — backend/client boundary and data semantics.
- `quality-gates.md` — validation required before a frontend change is called ready.
- `web-production-handoff.md` — exact path from pre-production contracts to `apps/web`.
- `prototypes/frontend/shared/contracts/` — machine-readable prototype contracts.
- `prototypes/frontend/shared/fixtures/` — synthetic contract fixtures.
- `tests/prototypes/frontend-preprod-contracts.py` — executable drift guard.

## Non-negotiable boundaries

```text
Domain / canonical DANTE model
!= backend persistence/ORM model
!= backend transport DTO
!= frontend view model
!= component-local/transient state
```

Adapters perform explicit mappings between boundaries. UI components do not consume PostgreSQL/ORM shapes and do not make ad-hoc HTTP calls.

## Production-shape requirements

Every durable surface/component must eventually define, where applicable:

- responsibility and owner;
- inputs/view model;
- events/intents;
- loading/ready/empty/partial/full/overflow/error/unavailable states;
- server state vs UI state vs transient interaction state;
- authorization/capability behavior;
- responsive/container behavior;
- accessibility and focus behavior;
- error/retry/stale semantics;
- persistence expectation;
- test/observability requirements.

## Toolchain boundary

The repository currently records an accepted historical client direction using React/Next.js, while the current Engineering Foundation explicitly leaves detailed frontend runtime/toolchain decisions to this workstream. This foundation does not supersede either source. Before creating `apps/web`, the production-scaffold gate must confirm the client ADR and select exact supported versions/package manager/build/test tooling from current evidence.

A framework/tool change that alters an accepted architectural decision requires explicit ADR supersession, not a convenience rewrite.

## Current application to Home

Home central stage is the first machine-readable contract target. It establishes one geometry owner (`home.stage`), framework-neutral stage states/events, a view-model schema, synthetic fixtures and a resize/reflow matrix. The current B2 visual checkpoint remains WIP and is not made responsive-complete by this foundation alone.
