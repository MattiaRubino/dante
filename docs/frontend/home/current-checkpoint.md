# DANTE — Home Current Pre-Frontend Checkpoint

**Branch:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT**  
**Current working B2 baseline:** **B2 Central Stage v21 responsive**  
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

## Current B2 working baseline — v21

The current B2 continuation oracle is the user-reviewed responsive v21 state.

### Full

```text
DANTE_Home_B2_full_responsive_guarded_preview_v21.html
size       762160 bytes
SHA-256    b653b5455903d0978cae88ff76fb74c285d0104334871cdb9f406f6d945c4cde
```

### Partial

```text
DANTE_Home_B2_partial_responsive_guarded_preview_v21.html
size       762090 bytes
SHA-256    390f12cf6c327be27342dcc038d398fd2751c3e2a9cbab3fbf2d981092405763
```

Durable checkpoint:

`docs/frontend/home/checkpoints/b2-central-stage-v21-responsive.md`

Deterministic archive:

`prototypes/frontend/home/archive/b2-central-stage-v21/`

## B2 v21 functional/visual direction

- stage projections: `Mondi` / `Segnali`;
- stable technical IDs: `home.stage.continuity` / `home.stage.signals`;
- Mondi retains the sphere-carousel visual lineage;
- desktop Continuity target = five visible sphere positions;
- partial state renders unused existing sphere positions as ghost `+` slots;
- Segnali uses the same previous/next, selection and drag/swipe grammar;
- Segnali desktop maximum = three complete visible items;
- Signal track is centered within the stage;
- mode switch preserves stage shell/selector/lateral-navigation anchors;
- AI expanded/collapsed reflow remains Home-shell behavior;
- resize hardening follows real physical stage geometry and adapts Continuity spacing in the narrow critical state.

## Current QA evidence

```text
B2 v21 user visual/resize review       ACCEPTED WORKING BASELINE
full duplicate DOM IDs                 0
partial duplicate DOM IDs              0
full inline JS syntax failures         0
partial inline JS syntax failures      0
critical 901px + AI collapsed overflow corrected
B2.5 contract drift guard              PASS
B2.5 responsive target cases           24
fresh automated 24-case browser PASS   NOT CLAIMED
```

The complete browser-matrix rerun is not represented as PASS in this checkpoint. User review accepted the v21 responsive behavior, while the B2.5 matrix remains the formal target for final automated verification.

## Open before B2 closure

1. decide whether/how a `+` / add affordance should exist for full Mondi, Segnali and future stage projections;
2. align visible logo/product naming to DANTE;
3. review overall Home palette;
4. review background/atmosphere;
5. run final applicable Home/B2 QA after those changes.

## Non-regression / intentionally unchanged

The v21 checkpoint does not authorize changes to:

- timeline semantics;
- calendar/day ribbon semantics;
- context-rail B1 meaning;
- backend/domain/logical/physical semantics;
- production framework/runtime selection;
- real backend endpoints or persistence contracts.

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
