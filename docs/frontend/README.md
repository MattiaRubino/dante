# DANTE — Frontend Product Contract

**Status:** current product/UX authority for the materialized frontend.

This directory contains durable product-facing frontend contracts carried from approved exploratory work into the production-shaped React workspace. Current implementation truth remains the checked-out production code/tests; prototype branches are frozen design/history sources, not runtime dependencies.

## Read order

1. `docs/frontend/access.md` — current materialized Access Web baseline and remaining full-stack boundary
2. `docs/frontend/home/production-depth-handoff.md` — current Home phase, working strategy and new-chat bootstrap
3. `docs/frontend/home/current-checkpoint.md`
4. `docs/frontend/home/contract.md`
5. `docs/frontend/ui-registry.md`
6. `docs/frontend/design-tokens.md`
7. `docs/frontend/terminology.md`
8. `docs/frontend/localization.md`
9. `docs/frontend/production-readiness/component-architecture.md`
10. `docs/frontend/production-readiness/backend-integration-contract.md`
11. `docs/frontend/production-readiness/quality-gates.md`

Engineering/runtime authority remains the materialized frontend workspace, repository architecture, CI and local-development documentation. Product contracts do not replace those engineering authorities.

## Access

`docs/frontend/access.md` is the current durable contract for the completed pre-backend Access Web materialization. The approved cross-platform design source remains frozen on `prototype/access-system`; it is historical design evidence and must not override newer production code/current documentation.

The completed frontend work deliberately does **not** claim real Auth backend behavior. Real account/session/provider/recovery integration belongs to a later full-stack Access/Auth vertical created from current protected `main`.

## Home React migration rule

The accepted Home prototype is an executable UX/reference specification, **not** code to transliterate line-by-line into React.

Implementation must:

- preserve the accepted visual and behavioral contract before introducing redesigns;
- use the React/TypeScript architecture already materialized in the repository;
- componentize by ownership boundary rather than arbitrary pieces of the old monolith;
- separate view models from backend DTOs/domain/persistence shapes;
- preserve semantic IDs, localization keys and machine-readable Home-stage contracts;
- keep semantic World/group/event colors distinct from generic DANTE chrome.

## Deliberately not imported from exploratory branches

Exploratory branches contain extensive historical material intentionally excluded from current production documentation, including intermediate patch/archive chains, reconstruction fragments, obsolete checkpoints, abandoned experiments and regression tooling tied only to superseded prototype internals.

That history remains available on its source branch if archaeology is required, but it is not an implementation dependency.

## Frozen Home prototype evidence

Historical Home prototype authority is pinned to `prototype/frontend` commit:

`2203c96c4aa1dc10258a84bcf461aa0b923e8951`

The final user-reviewed local Home wrapper corresponding to the accepted B2 v27 state was:

```text
DANTE_Home_v43_VERIFIED_INJECTION_COLOR_FIX.html
size       87386 bytes
SHA-256    e82058e4e980208feb3f0c055dab3eec81812be1fa47e5f036e8d5d0e1fe859d
```

The wrapper itself is not copied into current production documentation; durable behavior/visual decisions and machine-readable contracts are retained instead.
