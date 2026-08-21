# DANTE — Frontend Prototype Workspace

This directory documents the pre-production frontend workstream on `prototype/frontend`.

It validates product surfaces, interaction behavior, information hierarchy, naming, overlay grammar, visual language, responsive/cross-platform behavior and coded UX prototypes before production frontend implementation.

It is not the production application codebase, but from B2.5 onward durable/touched behavior is shaped with production-grade boundaries so later `apps/web` migration is implementation work rather than semantic rediscovery.

## Mandatory bootstrap

A frontend continuation must read:

1. `docs/workstreams/frontend.md`
2. `docs/frontend/ui-registry.md`
3. the current surface contract (`docs/frontend/home/contract.md` for Home)
4. `docs/frontend/terminology.md`
5. `docs/frontend/localization.md`
6. `docs/frontend/design-tokens.md`
7. `docs/frontend/production-readiness/README.md`
8. current checkpoint / QA
9. `docs/frontend/research-index.md` when semantic/UX reasoning is required

The permanent documentation invariant is defined in `docs/workstreams/frontend.md`: implementation, behavior registry, terminology, copy, visual tokens, engineering contracts and history must stay synchronized in the same bounded scope.

## Current Home state

Retained complete A2 baseline:

```text
prototypes/frontend/home/current/home.html
size     748625 bytes
SHA-256  986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob fd9788212fbbd1ee40e53271cc39cedd9275b341
```

Last formally closed Home milestone:

```text
B1 Context Rail v1
size     760281 bytes
SHA-256  a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0
```

Current B2 working visual/behavior baseline:

```text
B2 Central Stage v22 no persistent add
FULL SHA-256     18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76
PARTIAL SHA-256  f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

v22 supersedes v21 as the current B2 continuation oracle. The stage add/configuration decision is now fixed: Home has no persistent `+`, partial states show only real items, and an empty state may hand off to a dedicated management surface.

B2 remains **open** for DANTE logo/name alignment, palette/background work and final QA.

B2.5 provides the production-readiness contracts/quality gates that govern further durable work. The current Home-stage machine-readable contract version is `0.2.0`.

## Authorities

- `ui-registry.md` — current inventory and behavior/status
- `home/contract.md` — exact Home contract and non-regression
- `home/current-checkpoint.md` — current working Home oracle and QA qualification
- `terminology.md` — names, technical IDs and naming history
- `localization.md` + `prototypes/frontend/shared/locales/` — user-facing copy
- `design-tokens.md` + `prototypes/frontend/shared/theme/tokens.css` — visual tokens
- `production-readiness/` — component/data/backend-handoff/quality architecture
- `prototypes/frontend/shared/contracts/` — machine-readable framework-neutral contracts
- `prototypes/frontend/shared/fixtures/` — synthetic contract fixtures
- `change-log.md` — append-only frontend history

Current B2 checkpoint:

`docs/frontend/home/checkpoints/b2-central-stage-v22-no-persistent-add.md`

Current deterministic B2 archive:

`prototypes/frontend/home/archive/b2-central-stage-v22/`

`docs/frontend/reference/phase4/` remains evidence, not current truth when newer authorities conflict.
