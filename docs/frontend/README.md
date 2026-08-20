# DANTE — Frontend Prototype Workspace

This directory documents the pre-production frontend workstream on `prototype/frontend` and bounded child surface scopes such as `prototype/access-system`.

It validates product surfaces, interaction behavior, information hierarchy, naming, overlay grammar, visual language, responsive/cross-platform behavior, security-relevant client behavior and coded UX prototypes before production frontend implementation.

It is not the production application codebase.

## Mandatory bootstrap

A frontend continuation must read:

1. `docs/workstreams/frontend.md`
2. `docs/frontend/ui-registry.md`
3. the current surface contract
4. `docs/frontend/terminology.md`
5. `docs/frontend/localization.md`
6. `docs/frontend/design-tokens.md`
7. current checkpoint / QA
8. `docs/frontend/research-index.md` when semantic/UX/security reasoning is required

For Access Mobile also read `docs/frontend/access/mobile-ui-registry.md` and the PRG-0 documents.

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

The accepted B1 result is reconstructed deterministically by `prototypes/frontend/home/work/build.py` from the retained complete baseline plus the accepted B1 override. This keeps the complete baseline, editable/modular work source and exact accepted result independently traceable.

## Current Access state

Access is developed on `prototype/access-system` and does not change the accepted Home implementation.

### Desktop / web oracle

```text
A3.4 — Access System
size     93897 bytes
SHA-256  b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6
status   APPROVED DESKTOP REVIEW ORACLE / PRE-IMPLEMENTATION
```

### Mobile oracle

```text
M1.2 + PRG-0 — Mobile Access
size     107010 bytes
SHA-256  2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676
status   PRODUCTION-READY SPECIFICATION / PRG-0 PASS / PRE-IMPLEMENTATION
```

Read:

- `docs/frontend/access/contract.md`
- `docs/frontend/access/state-model.md`
- `docs/frontend/access/current-checkpoint.md`
- `docs/frontend/access/benchmark-2026-08-20.md`
- `docs/frontend/access/mobile-ui-registry.md`
- `docs/frontend/access/mobile-technical-contract.md`
- `docs/frontend/access/mobile-research-matrix.md`
- `docs/frontend/access/mobile-production-readiness.md`
- `docs/frontend/access/mobile-qa.md`
- `prototypes/frontend/access/README.md`

The exact selected standalone artifacts are preserved through hash-verified archives because the review connector has a payload-size limit. This is storage/transport only; restored artifacts are complete standalone review oracles.

`production-ready specification` does **not** mean production executable software. Native provider SDKs, secure storage, real links, backend AuthN, device accessibility and security verification remain implementation/release gates.

## Authorities

- `ui-registry.md` — global current inventory and behavior/status
- `home/contract.md` — exact Home contract and non-regression
- `access/contract.md` — cross-platform Access contract
- `access/mobile-ui-registry.md` — mobile-specific representation/behavior registry
- `terminology.md` — names, technical IDs and naming history
- `localization.md` + `prototypes/frontend/shared/locales/` — user-facing copy
- `design-tokens.md` + `prototypes/frontend/shared/theme/tokens.css` — visual tokens
- `change-log.md` — append-only frontend history

`docs/frontend/reference/phase4/` remains evidence, not current truth when newer authorities conflict.
