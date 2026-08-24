# DANTE — Frontend Product Contract

**Status:** current product/UX authority for the materialized frontend on `main`.

This directory contains the minimum product-facing frontend contract carried forward from the exploratory `prototype/frontend` branch into the production-shaped React workspace already integrated on `main`.

## Read order

1. `docs/frontend/home/current-checkpoint.md`
2. `docs/frontend/home/contract.md`
3. `docs/frontend/ui-registry.md`
4. `docs/frontend/design-tokens.md`
5. `docs/frontend/terminology.md`
6. `docs/frontend/localization.md`
7. `docs/frontend/production-readiness/component-architecture.md`
8. `docs/frontend/production-readiness/backend-integration-contract.md`
9. `docs/frontend/production-readiness/quality-gates.md`

Engineering/runtime authority remains the existing materialized frontend on `main`, including the applicable repository architecture, workspace, CI and local-development documentation. These product contracts do not replace those engineering authorities.

## React migration rule

The accepted Home prototype is an executable UX/reference specification, **not** code to transliterate line-by-line into React.

Implementation must:

- preserve the accepted visual and behavioral contract before introducing redesigns;
- use the React/TypeScript architecture already materialized on `main`;
- componentize by ownership boundary rather than by arbitrary pieces of the old monolith;
- separate view models from backend DTOs/domain/persistence shapes;
- preserve semantic IDs, localization keys and machine-readable Home-stage contracts;
- keep semantic World/group/event colors distinct from generic DANTE chrome.

## Deliberately not imported into main

The exploratory branch contains extensive historical material that is intentionally **not** part of the clean mainline handoff:

- `prototypes/frontend/home/work/**`;
- intermediate v16–v27 patch/archive chains;
- base64/background reconstruction fragments;
- obsolete prototype README/checkpoint history;
- abandoned visual experiments and wrappers;
- regression tooling tied only to superseded prototype internals.

That history remains available on `prototype/frontend` if archaeology is ever required, but it is not an implementation dependency.

## Frozen prototype evidence

Historical prototype authority is pinned to `prototype/frontend` commit:

`2203c96c4aa1dc10258a84bcf461aa0b923e8951`

The final user-reviewed local Home wrapper corresponding to the accepted B2 v27 state was:

```text
DANTE_Home_v43_VERIFIED_INJECTION_COLOR_FIX.html
size       87386 bytes
SHA-256    e82058e4e980208feb3f0c055dab3eec81812be1fa47e5f036e8d5d0e1fe859d
```

The wrapper itself is not copied into `main`; the durable behavior/visual decisions and machine-readable contracts are.