# DANTE — Home Current Pre-Frontend Checkpoint

**Branch:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT**  
**Current working B2 baseline:** **B2 Central Stage v22 no persistent add**  
**Last formally closed Home milestone:** **B1 Context Rail v1**  
**Nature:** standalone HTML/CSS/JavaScript coded UX prototype with production-shaped contracts; not production application code.

## Retained complete baseline

A2 complete baseline is deliberately preserved:

```text
path
prototypes/frontend/home/current/home.html

size
748625 bytes

SHA-256
986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df

Git blob
fd9788212fbbd1ee40e53271cc39cedd9275b341
```

## Last formally closed Home milestone — B1

B1 Context Rail v1 remains the last completely closed Home milestone and is reconstructed from the retained A2 baseline plus the accepted B1 override through `prototypes/frontend/home/work/build.py`.

```text
size
760281 bytes

SHA-256
a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0

result
DETERMINISTIC BUILD MATCH
```

B1 accepted:

- one integrated context rail beside timeline;
- Capture = user -> DANTE low-friction unclassified capture;
- Resolution = DANTE -> user unresolved matters requiring meaningful user input;
- real button/segmented controls rather than text pretending to be actions;
- both functions visible together;
- rail stretches down with the timeline column;
- existing timeline expansion still yields/removes the rail.

## Current B2 working baseline — v22

The current B2 continuation oracle is the user-reviewed v22 state with no persistent add affordance.

### Full

```text
DANTE_Home_B2_full_no_add_preview_v22.html
size       761337 bytes
SHA-256    18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76
```

### Partial

```text
DANTE_Home_B2_partial_no_add_preview_v22.html
size       760579 bytes
SHA-256    f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

Durable checkpoint:

`docs/frontend/home/checkpoints/b2-central-stage-v22-no-persistent-add.md`

Deterministic archive:

`prototypes/frontend/home/archive/b2-central-stage-v22/`

## B2 v22 functional/visual direction

- stage projections: `Mondi` / `Segnali`;
- stable technical IDs: `home.stage.continuity` / `home.stage.signals`;
- Mondi retains the sphere-carousel visual lineage;
- desktop Continuity target = five visible real items where enough items exist;
- partial state renders only actual Mondi; no ghost `+` slots and no placeholder entities;
- Segnali uses the same previous/next, selection and drag/swipe grammar;
- Segnali desktop maximum = three complete visible items;
- Signal track is centered within the stage;
- mode switch preserves stage shell/selector/lateral-navigation anchors;
- AI expanded/collapsed reflow remains Home-shell behavior;
- v21 responsive hardening is preserved;
- Home stage is read/navigate/open rather than a configuration CRUD surface;
- no persistent `+` is shown for Mondi or Segnali;
- true empty state may provide a contextual management CTA;
- Mondi/Segnali creation and configuration live in dedicated management surfaces.

## Current machine-readable contract

```text
contractVersion                         0.2.0
persistentAddAffordance                 false
configurationInHome                     false
partialRendersOnlyRealItems             true
emptyStateMayOfferManagementEntry       true
directCreateMutationFromStage           false
ADD_REQUEST                              removed
OPEN_MANAGEMENT                          active intent
```

An empty fixture uses `activeIndex: null`; the UI does not manufacture a selected index when no real item exists.

## Current QA evidence

```text
B2 v22 user review                      ACCEPTED WORKING BASELINE
full duplicate DOM IDs                  0
partial duplicate DOM IDs               0
full inline JS syntax failures          0
partial inline JS syntax failures       0
ghost/add mechanism in v22 preview      absent
B2.5/v0.2 contract drift guard          PASS
B2.5 responsive target cases            24
fresh automated 24-case browser PASS    NOT CLAIMED
```

Current contract guard:

```text
frontend pre-production contracts: PASS
contractVersion=0.2.0
responsiveCases=24
signalsMaxVisible=3
continuityTargetVisible=5
persistentAdd=false
partialRealItemsOnly=true
emptyManagementEntry=true
```

The complete browser-matrix rerun is not represented as PASS in this checkpoint. User review accepted the v22 behavior, while the B2.5 matrix remains the formal target for final automated verification.

## Open before B2 closure

1. align visible logo/product naming to DANTE;
2. review overall Home palette;
3. review background/atmosphere;
4. run final applicable Home/B2 responsive/visual/accessibility QA after those changes.

## Non-regression / intentionally unchanged

The v22 checkpoint does not authorize changes to timeline semantics, calendar/day ribbon semantics, context-rail B1 meaning, backend/domain/logical/physical semantics, production framework/runtime selection, or real backend endpoints/persistence contracts.

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
