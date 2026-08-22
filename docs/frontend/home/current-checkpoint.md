# DANTE — Home Current Pre-Frontend Checkpoint

**Branch:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT**  
**Current working B2 baseline:** **B2 Home Branding v23 over B2 Central Stage v22**  
**Last formally closed Home milestone:** **B1 Context Rail v1**  
**Nature:** standalone HTML/CSS/JavaScript coded UX prototype with production-shaped contracts; not production application code.

## Retained baseline lineage

A2 retained complete baseline:

```text
prototypes/frontend/home/current/home.html
size       748625 bytes
SHA-256    986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
Git blob   fd9788212fbbd1ee40e53271cc39cedd9275b341
```

Last formally closed milestone remains B1 Context Rail v1:

```text
size       760281 bytes
SHA-256    a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0
```

## Structural/behavioral base — B2 v22

The v23 branding pass does not change v22 behavior.

```text
FULL v22
size       761337 bytes
SHA-256    18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76

PARTIAL v22
size       760579 bytes
SHA-256    f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

v22 authority:
- `docs/frontend/home/checkpoints/b2-central-stage-v22-no-persistent-add.md`
- `prototypes/frontend/home/archive/b2-central-stage-v22/`

Retained v22 rules include:
- `Mondi` / `Segnali`;
- no persistent `+`;
- partial Mondi renders only real items;
- Home stage is read/navigate/open, not configuration CRUD;
- management/creation lives in dedicated management surfaces;
- contract version remains `0.2.0`.

## Current visual layer — B2 branding v23

Durable checkpoint:

`docs/frontend/home/checkpoints/b2-branding-v23.md`

Deterministic archive:

`prototypes/frontend/home/archive/b2-branding-v23/`

Shared FULL/PARTIAL layer:

```text
brand-v22-to-v23.js
size       4101 bytes
SHA-256    a7a6a08dc2eb174cafe63c6e8b60d90244bfbfa6b98ef57e644ed7bb2a8132df
```

Accepted visual identity:
- topbar = official DANTE symbol in approved charcoal/orange + official wordmark geometry rendered white for the dark surface;
- no extra white panel/container;
- AI card identity = official DANTE symbol only;
- no visible `LifeOS` or `DANTE` text beside the AI symbol;
- the dark-surface wordmark treatment is a frontend derivative, not a new brand master.

Brand source is pinned to integrated main commit `db02da603f3779d8c7fcb1d7601f6f66f8a23241`.

## QA evidence

```text
B2 v23 FULL user visual review          PASS
v22 behavioral semantics                PRESERVED
FULL/PARTIAL branding implementation    SAME SHARED LAYER
B2.5/v0.2 contract semantics            UNCHANGED
responsive target cases                 24
fresh automated 24-case browser PASS    NOT CLAIMED
fresh PARTIAL browser visual PASS       NOT CLAIMED
```

## Open before B2 closure

1. review Home background / atmosphere;
2. review overall Home palette / color system;
3. review remaining shell details such as `Crea` placement only in an explicit later scope;
4. run final applicable responsive / visual / accessibility QA.

Historical `LifeOS` strings may still exist in untouched prototype-only or deprecated controls. v23 closes the **approved identity-anchor replacement**, not a global blind text rename.

## Non-regression

v23 does not authorize changes to timeline semantics, calendar/day ribbon semantics, context-rail B1 meaning, Mondi/Segnali behavior, Create semantics, backend/domain/logical/physical semantics, production framework/runtime selection, or real backend endpoints/persistence contracts.

## Current authorities

Read before Home work:
- `docs/workstreams/frontend.md`
- `docs/frontend/README.md`
- `docs/frontend/ui-registry.md`
- `docs/frontend/home/contract.md`
- `docs/frontend/terminology.md`
- `docs/frontend/localization.md`
- `docs/frontend/design-tokens.md`
- `docs/frontend/production-readiness/README.md`
- this checkpoint
- `docs/frontend/research-index.md` when semantic research is needed.
