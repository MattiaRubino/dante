# DANTE — Home Current Pre-Frontend Checkpoint

**Branch:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT**  
**Current working B2 baseline:** **B2 Home Shell + Timeline Quick Add v25 over B2 Home Visual Skin v24 over B2 Home Branding v23 over B2 Central Stage v22**  
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

The immutable A2 oracle above is not overwritten by later B2 checkpoints.

## Structural/behavioral base — B2 v22

Later identity/skin/shell checkpoints do not reopen the v22 Home-stage behavior contract.

```text
FULL v22
size       761337 bytes
SHA-256    18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76

PARTIAL v22
size       760579 bytes
SHA-256    f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

v22 authority:
- `docs/frontend/home/checkpoints/b2-central-stage-v22-no-persistent-add.md`;
- `prototypes/frontend/home/archive/b2-central-stage-v22/`.

Retained v22 rules include:
- `Mondi` / `Segnali`;
- no persistent `+` in the Home central stage;
- no ghost add slots or placeholder World/Signal items;
- Home stage is read/navigate/open, not configuration CRUD;
- management/creation lives in dedicated management surfaces;
- contract version remains `0.2.0`.

The v25 timeline quick-add is a temporal-surface affordance and does **not** relax the v22 central-stage rule.

## Identity layer — B2 branding v23

Authority:

- `docs/frontend/home/checkpoints/b2-branding-v23.md`;
- `prototypes/frontend/home/archive/b2-branding-v23/`.

Accepted identity remains:
- topbar = official DANTE symbol in approved charcoal/orange + official wordmark geometry rendered white for the dark surface;
- no extra white panel/container;
- AI card identity = official DANTE symbol only;
- no visible `LifeOS` or `DANTE` text beside the AI symbol;
- dark-surface wordmark treatment is a frontend derivative, not a new brand master.

Brand source remains pinned to integrated main commit `db02da603f3779d8c7fcb1d7601f6f66f8a23241`.

## Visual layer — B2 visual skin v24

Authority:

- `docs/frontend/home/checkpoints/b2-visual-skin-v24.md`;
- `prototypes/frontend/home/archive/b2-visual-skin-v24/`.

Shared v23 -> v24 CSS layer:

```text
skin-v23-to-v24.css
size       2949 bytes
SHA-256    a3bfd6e6a09d627055b9b92c0c90f3ac25f832086beaf3a54229d59b4548fb5c
```

Accepted background reconstruction:

```text
dante-home-cosmos-mirrored-v1.webp
size       37482 bytes
SHA-256    8ce54b557e7e1cd436ecd6ac672491e619bc61111788b9b0551eeef257f74002
geometry   1920 x 1080
```

Retained v24 visual direction:
- charcoal surfaces with restrained DANTE orange emphasis;
- accepted cosmos/neural Home atmosphere;
- stage remains translucent enough for the background to read;
- only obsolete `#netCanvas` is hidden;
- `#fxCanvas` and `.magnet-line` remain untouched so Mondi effects/animation are preserved.

Rejected regression remains rejected: hiding `#fxCanvas` / `.magnet-line` together with `#netCanvas` visibly degraded Mondi.

## Current shell/timeline layer — B2 v25

Authority:

- `docs/frontend/home/checkpoints/b2-shell-timeline-v25.md`;
- `prototypes/frontend/home/archive/b2-shell-timeline-v25/`.

Deterministic v24 -> v25 transform:

```text
shell-v24-to-v25.js
size       8391 bytes
SHA-256    6e9d3e25270f8d73482aa6a2f48f709e1ffc2324007dde2fa6d40cdea90d1d69
```

Accepted app-bar arrangement:

```text
LEFT                         CENTER                    RIGHT
DANTE + Cerca                Home / Mondi / Oggi       Crea / Review / launcher / account
```

Accepted shell rules:
- true sticky application bar at the top of the viewport;
- edge-to-edge shell treatment with **24 px internal horizontal inset**;
- Search follows DANTE on the left;
- Home/Mondi/Oggi stays centered;
- `Crea` is the first control of the right utility group, before legacy Review;
- existing Search/Create nodes are reused, not duplicated;
- the reviewed outer Home-shell side-frame cleanup is retained.

Accepted timeline-header arrangement:

```text
add / month / now / week / actions
```

The real timeline `+` sits before month/year in the same grid, so month and `Ora` move right as one aligned temporal-header composition. Its current click bridge reuses the existing global `Crea` popover and remains prototype-only; final date/time prefill, destination, command and persistence semantics are still open.

User-reviewed local evidence:

```text
DANTE_Home_v24_v13_PLUS_REFINED_MONTH_RIGHT.html
size       80922 bytes
SHA-256    0b9491525a99643837dc42e4150113db50d00bf7ff73549ea4fd3f9994adcdf9
```

## Token / production qualification

v24/v25 approve the **working prototype appearance and shell placement**, not final production token naming or framework implementation.

The shared semantic-token authority remains `docs/frontend/design-tokens.md`. Promotion/migration from preview values into production/shared semantic tokens remains a later bounded implementation step.

`Crea`, Search, timeline quick-add and other current popovers remain prototype interactions unless separately promoted by a production contract.

## QA evidence

```text
B2 v25 final user visual review              PASS
v25 transform JavaScript syntax              PASS (node --check)
v25 transform mock-structure execution       PASS
reviewed v13 wrapper inline-JS syntax        PASS
v24 Mondi regression fix                     PRESERVED
v22 behavioral semantics                     PRESERVED
v23 DANTE identity                           PRESERVED
responsive target cases                      24
fresh automated 24-case browser PASS         NOT CLAIMED
fresh full accessibility rerun               NOT CLAIMED
fresh PARTIAL browser visual PASS             NOT CLAIMED
```

## Open before B2 closure

1. define final production semantics for timeline quick-add, especially contextual date/time prefill and destination;
2. reconcile legacy Review and the historical launcher only through an explicit bounded scope;
3. decide/perform production semantic-token migration when implementation reaches the shared theme layer;
4. finish remaining small shell/detail refinements;
5. run final applicable responsive / visual / accessibility QA.

Historical `LifeOS` strings may still exist in untouched prototype-only/deprecated controls. v23-v25 do not authorize a blind global rename.

## Non-regression

v25 does not authorize changes to Mondi/Segnali semantics/data, central-stage no-persistent-add semantics, calendar/date-navigation meaning, Context Rail Capture/Resolution meaning, event drag/zoom/grouping/time-edit behavior, backend/domain/logical/physical semantics, production framework/runtime selection, or real backend endpoints/persistence contracts.

## Current authorities

Read before Home work:
- `docs/workstreams/frontend.md`;
- `docs/frontend/README.md`;
- `docs/frontend/ui-registry.md`;
- `docs/frontend/home/contract.md`;
- `docs/frontend/terminology.md`;
- `docs/frontend/localization.md`;
- `docs/frontend/design-tokens.md`;
- `docs/frontend/production-readiness/README.md`;
- this checkpoint;
- `docs/frontend/research-index.md` when semantic research is needed.
