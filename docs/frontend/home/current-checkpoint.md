# DANTE — Home Current Pre-Frontend Checkpoint

**Branch:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT**  
**Current working B2 baseline:** **B2 Home Visual Skin v24 over B2 Home Branding v23 over B2 Central Stage v22**  
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

v23 branding and v24 visual skin do not change the v22 Home-stage behavior contract.

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

## Identity layer — B2 branding v23

Durable checkpoint:

`docs/frontend/home/checkpoints/b2-branding-v23.md`

Deterministic archive:

`prototypes/frontend/home/archive/b2-branding-v23/`

Accepted visual identity remains:
- topbar = official DANTE symbol in approved charcoal/orange + official wordmark geometry rendered white for the dark surface;
- no extra white panel/container;
- AI card identity = official DANTE symbol only;
- no visible `LifeOS` or `DANTE` text beside the AI symbol;
- the dark-surface wordmark treatment is a frontend derivative, not a new brand master.

Brand source is pinned to integrated main commit `db02da603f3779d8c7fcb1d7601f6f66f8a23241`.

## Current visual layer — B2 visual skin v24

Durable checkpoint:

`docs/frontend/home/checkpoints/b2-visual-skin-v24.md`

Deterministic archive:

`prototypes/frontend/home/archive/b2-visual-skin-v24/`

Shared v23 -> v24 CSS layer:

```text
skin-v23-to-v24.css
size       2949 bytes
SHA-256    a3bfd6e6a09d627055b9b92c0c90f3ac25f832086beaf3a54229d59b4548fb5c
```

Accepted background asset is archived deterministically as ordered Base64 parts plus `restore-v24-background.py`. The restore gate reproduces:

```text
dante-home-cosmos-mirrored-v1.webp
size       37482 bytes
SHA-256    8ce54b557e7e1cd436ecd6ac672491e619bc61111788b9b0551eeef257f74002
geometry   1920 x 1080
```

Accepted v24 visual direction:
- charcoal surfaces replace the previous generic navy/purple emphasis;
- DANTE orange `#EA5C12` becomes the restrained global emphasis color in the working skin;
- cosmos/neural artwork becomes the Home atmosphere behind the shell;
- the stage remains translucent enough for the background to read without changing layout;
- only the obsolete `#netCanvas` network layer is hidden;
- `#fxCanvas` and `.magnet-line` remain untouched so existing Mondi sphere effects/animation are preserved.

The final user-reviewed local wrapper was:

```text
DANTE_Home_ONE_BACKGROUND_MIRRORED_no_net_only.html
size       64678 bytes
SHA-256    2fde54ec03d4540bb7799342e7e5df2b99fa843dbebc395ae93eeb56df4b5e05
```

The broad cleanup variant that also hid `#fxCanvas` / `.magnet-line` caused a visible Mondi regression and is rejected.

## Token / Create qualification

v24 approves the **working prototype appearance**, not final production token naming. The existing shared semantic-token authority remains `docs/frontend/design-tokens.md`; promotion/migration from preview `--f-*` values into production/shared semantic tokens is still a later bounded implementation step.

The current skin visually renders the existing `Crea` control with orange fill. This does not close or change Create-vs-Capture semantics, placement, routing or backend behavior.

## QA evidence

```text
B2 v24 final user visual review             PASS
Mondi regression from broad cleanup          DETECTED / REJECTED
final cleanup                                #netCanvas ONLY
#fxCanvas / .magnet-line v24 overrides       NONE
v22 behavioral semantics                     PRESERVED
v23 DANTE identity                           PRESERVED
outer local review-wrapper JS syntax         PASS
responsive target cases                      24
fresh automated 24-case browser PASS         NOT CLAIMED
fresh full accessibility rerun                NOT CLAIMED
fresh PARTIAL browser visual PASS             NOT CLAIMED
```

## Open before B2 closure

1. review remaining shell/details only through explicit bounded scopes, including any later `Crea` placement/semantic decision;
2. decide/perform production semantic-token migration when implementation scope reaches the shared theme layer;
3. run final applicable responsive / visual / accessibility QA;
4. reconcile remaining historical/deprecated prototype-only shell items such as `Tutto LifeOS` / legacy Review only when explicitly scoped.

Historical `LifeOS` strings may still exist in untouched prototype-only or deprecated controls. v23/v24 do not authorize a blind global rename.

## Non-regression

v24 does not authorize changes to timeline semantics, calendar/day ribbon semantics, Context Rail B1 meaning, Mondi/Segnali data/interaction contract, no-persistent-add semantics, Create/Capture semantics, backend/domain/logical/physical semantics, production framework/runtime selection, or real backend endpoints/persistence contracts.

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
