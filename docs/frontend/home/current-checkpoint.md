# DANTE — Home Current Pre-Frontend Checkpoint

**Branch:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT**  
**Current working B2 baseline:** **B2 Home Infrastructure Color v27 over B2 Home Edge Attachment v26 over B2 Home Shell + Timeline Quick Add v25 over B2 Home Visual Skin v24 over B2 Home Branding v23 over B2 Central Stage v22**  
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

Later identity/skin/shell/edge/color checkpoints do not reopen the v22 Home-stage behavior contract.

```text
FULL v22
size       761337 bytes
SHA-256    18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76

PARTIAL v22
size       760579 bytes
SHA-256    f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

Authority:
- `docs/frontend/home/checkpoints/b2-central-stage-v22-no-persistent-add.md`;
- `prototypes/frontend/home/archive/b2-central-stage-v22/`.

Retained rules:
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

Retained visual direction:
- charcoal surfaces with restrained DANTE orange emphasis;
- accepted cosmos/neural Home atmosphere;
- stage remains translucent enough for the background to read;
- only obsolete `#netCanvas` is hidden;
- `#fxCanvas` and `.magnet-line` remain untouched so Mondi effects/animation are preserved.

## Shell/timeline layer — B2 v25

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

Accepted shell/timeline rules:
- true sticky application bar at the top of the viewport;
- shell-level edge-to-edge treatment with 24 px app-bar internal inset;
- Search follows DANTE on the left;
- Home/Mondi/Oggi stays centered;
- `Crea` is first in the right utility group;
- existing Search/Create nodes are reused, not duplicated;
- timeline temporal header is `add / month / now / week / actions`;
- the timeline `+` is a real contextual control and its current bridge to global `Crea` remains prototype-only.

## Edge-attachment layer — B2 v26

Authority:
- `docs/frontend/home/checkpoints/b2-edge-attachment-v26.md`;
- `prototypes/frontend/home/archive/b2-edge-attachment-v26/`.

Deterministic v25 -> v26 transform:

```text
edge-v25-to-v26.js
size       2827 bytes
SHA-256    55b1ef7bdf3215a61e9d8aa4215ed6f93f81d98ee458d4ec7a852a37d99d6812
```

Accepted visual edge contract:

```text
EXPANDED AI
left edge = 0
left corner radius = 0
right geometry = preserved

COLLAPSED AI RAIL
left = 0
border-radius = 0 18px 18px 0

TIMELINE
host margin-left = 0
right margin = preserved
Shadow DOM .today left radii = 0
right-side rounding = preserved
```

Exact implementation targets:
- `.ai-card.ai-chat-pro`;
- `.home-ai-rail`;
- `lifeos-today`;
- `lifeos-today.shadowRoot .today`.

User-reviewed local evidence:

```text
DANTE_Home_v38_VERIFIED_OPEN_COLLAPSED_TIMELINE.html
size       83055 bytes
SHA-256    07fab6068427a972f5201454e780d2b7a66db0e10ef9e0f5e80be7be7c5d9f22
```

## Current infrastructure-color layer — B2 v27

Authority:
- `docs/frontend/home/checkpoints/b2-infrastructure-color-v27.md`;
- `prototypes/frontend/home/archive/b2-infrastructure-color-v27/`.

Deterministic v26 -> v27 transform:

```text
chrome-v26-to-v27.js
size       5332 bytes
SHA-256    73aa897923aae6523d52d770c4dc1453d61118387198f96b7a01445edcd3b0e1
```

Accepted color contract:

```text
primary / active / selected interaction = DANTE orange
inactive generic controls               = neutral blue-grey / charcoal
semantic content identity               = preserve category/world color
```

Accepted generic Today chrome normalized away from legacy purple:
- `Ora`;
- selected/current week day;
- current-time line/marker;
- Cattura add/send controls and `Registrato` status dots;
- `Da risolvere` icon/count chrome and `Conferma` action.

Semantic colors remain authoritative for Mondi/worlds, timeline groups, event/category identity and real state semantics.

User-reviewed local evidence:

```text
DANTE_Home_v43_VERIFIED_INJECTION_COLOR_FIX.html
size       87386 bytes
SHA-256    e82058e4e980208feb3f0c055dab3eec81812be1fa47e5f036e8d5d0e1fe859d
```

v27 is color-only by contract. It does **not** alter v26 edge geometry, central-stage layout, Mondi/Segnali behavior, orientation, timeline layout/behavior, quick-add meaning, backend contracts or persistence.

## Token / production qualification

v24-v27 approve the **working prototype appearance, shell placement, edge geometry and generic infrastructure-color direction**, not final production token naming or framework implementation.

The shared semantic-token authority remains `docs/frontend/design-tokens.md`. Promotion/migration from preview values into production/shared semantic tokens remains a later bounded implementation step.

`Crea`, Search, timeline quick-add and other current popovers remain prototype interactions unless separately promoted by a production contract.

## QA evidence

```text
B2 v27 final user visual review                   PASS
v27 transform JavaScript syntax                   PASS (node --check)
v27 transform mock-structure execution            PASS
v26 edge geometry                                 PRESERVED
v25 shell/timeline semantics                      PRESERVED
v24 palette/background                            PRESERVED
v23 DANTE identity                                PRESERVED
v22 behavioral semantics                          PRESERVED
semantic World/group/event colors                 PRESERVED BY CONTRACT
Mondi/stage/orientation geometry mutations        NONE
fresh full reconstructed-Home browser matrix      NOT CLAIMED
fresh full accessibility rerun                    NOT CLAIMED
fresh PARTIAL browser visual PASS                 NOT CLAIMED
```

## Open before B2 closure

1. define final production semantics for timeline quick-add, especially contextual date/time prefill and destination;
2. reconcile legacy Review and the historical launcher only through an explicit bounded scope;
3. decide/perform production semantic-token migration when implementation reaches the shared theme layer;
4. finish remaining small shell/detail refinements;
5. run final applicable responsive / visual / accessibility QA.

Historical `LifeOS` strings may still exist in untouched prototype-only/deprecated controls. v23-v27 do not authorize a blind global rename.

## Non-regression

v27 does not authorize changes to Mondi/Segnali semantics/data, central-stage no-persistent-add semantics, calendar/date-navigation meaning, Context Rail Capture/Resolution meaning, event drag/zoom/grouping/time-edit behavior, backend/domain/logical/physical semantics, production framework/runtime selection, or real backend endpoints/persistence contracts.

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
