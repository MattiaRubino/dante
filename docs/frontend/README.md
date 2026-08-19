# DANTE — Frontend Prototype Workspace

This directory documents the pre-production frontend workstream on `prototype/frontend`.

It validates product surfaces, interaction behavior, information hierarchy, naming, overlay grammar, visual language, responsive/cross-platform behavior and coded UX prototypes before production frontend implementation.

It is not the production application codebase.

## Mandatory bootstrap

A frontend continuation must read:

1. `docs/workstreams/frontend.md`
2. `docs/frontend/ui-registry.md`
3. the current surface contract (`docs/frontend/home/contract.md` for Home)
4. `docs/frontend/terminology.md`
5. `docs/frontend/localization.md`
6. `docs/frontend/design-tokens.md`
7. current checkpoint / QA
8. `docs/frontend/research-index.md` when semantic/UX reasoning is required

The permanent documentation invariant is defined in `docs/workstreams/frontend.md`: implementation, behavior registry, terminology, copy, visual tokens and history must stay synchronized in the same bounded scope.

## Current Home state

Retained complete A2 baseline:

```text
prototypes/frontend/home/current/home.html
size     748625 bytes
SHA-256  986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob fd9788212fbbd1ee40e53271cc39cedd9275b341
```

Current accepted build:

```text
B1 Context Rail v1
size     760281 bytes
SHA-256  a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0
```

The accepted B1 result is reconstructed deterministically by `prototypes/frontend/home/work/build.py` from the retained complete baseline plus the accepted B1 override. This keeps the complete baseline, the editable/modular work source and the exact accepted result independently traceable.

## Authorities

- `ui-registry.md` — current inventory and behavior/status
- `home/contract.md` — exact Home contract and non-regression
- `terminology.md` — names, technical IDs and naming history
- `localization.md` + `prototypes/frontend/shared/locales/` — user-facing copy
- `design-tokens.md` + `prototypes/frontend/shared/theme/tokens.css` — visual tokens
- `change-log.md` — append-only frontend history

`docs/frontend/reference/phase4/` remains evidence, not current truth when newer authorities conflict.
