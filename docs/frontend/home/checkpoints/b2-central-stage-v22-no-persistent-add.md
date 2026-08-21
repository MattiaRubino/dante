# DANTE — Home B2 Central Stage v22 No Persistent Add

**Status:** USER-REVIEWED / APPROVED WORKING BASELINE / B2 OPEN  
**Date:** 2026-08-21  
**Branch:** `prototype/frontend`  
**PRE-SCOPE:** `da3ec90c3b7d282fe7b030e232a3be5db3f3ef44`

## Purpose

Preserve the B2 central-stage state after removing persistent/add-slot affordances from Home and formalizing the stage as a read/navigate/open projection rather than a configuration surface.

This checkpoint supersedes v21 as the current B2 working visual/behavior baseline. B1 Context Rail v1 remains the last formally closed Home milestone.

## Product decision — Home stage is not the management surface

Current rule:

```text
HOME STAGE
READ / NAVIGATE / OPEN

NO persistent +
NO ghost add slots
NO placeholder World/Signal items
NO configuration CRUD inside Home
```

State behavior:

```text
PARTIAL
show only real items

FULL / OVERFLOW
normal carousel/projection behavior

EMPTY
a contextual CTA may be shown so the surface is not a dead end
the CTA opens the dedicated management/creation surface
it does not create directly inside Home
```

Management belongs outside the Home stage:

- Mondi creation/edit/order/archive/removal belong to the dedicated Mondi management surface;
- Segnali selection/configuration/order/removal belong to the dedicated Signals management surface;
- future stage projections follow the same rule unless a later explicit product decision proves a different interaction is needed.

## Stage invariants carried forward

- visible projections are `Mondi` and `Segnali`;
- technical IDs remain `home.stage.continuity` and `home.stage.signals`;
- Mondi preserves the sphere-carousel visual lineage;
- Continuity desktop target remains five visible items where enough real items exist;
- Segnali renders at most three complete visible items in the current desktop composition;
- mode switching does not redefine stage outer geometry, selector anchor or lateral navigation anchors;
- AI expanded/collapsed reflow remains Home-shell behavior;
- v21 responsive hardening remains inherited by v22.

## Exact saved preview identities

### Full state

```text
source preview
DANTE_Home_B2_full_no_add_preview_v22.html

size
761337 bytes

SHA-256
18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76
```

### Partial state

```text
source preview
DANTE_Home_B2_partial_no_add_preview_v22.html

size
760579 bytes

SHA-256
f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

The archive under `prototypes/frontend/home/archive/b2-central-stage-v22/` stores deterministic gzip+Base64 unified diffs from v21 to these v22 outputs.

## Machine-readable contract evolution

The Home-stage pre-production contract advances from `0.1.0` to `0.2.0` because the interaction semantics changed:

- `ADD_REQUEST` is removed;
- `OPEN_MANAGEMENT` represents the empty-state handoff to a dedicated management surface;
- partial state contains only real items;
- empty projections use `activeIndex: null`;
- persistent add affordances are explicitly forbidden in the Home stage;
- direct create mutation from Home stage is forbidden by contract.

The schema, responsive matrix, fixtures and stdlib drift guard move together under the same version.

## QA qualification

Established for this working checkpoint:

- user reviewed v22 and approved continuation;
- full and partial static checks reported zero duplicate DOM IDs;
- full and partial inline-JavaScript syntax checks reported zero failures;
- the previous ghost/add mechanism is absent from the v22 preview lineage;
- the v0.2.0 machine-readable contract drift guard passes locally.

Contract guard:

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

Not claimed:

- a fresh automated browser PASS for every 24 responsive matrix combination;
- production React/Next implementation;
- backend API/integration PASS;
- B2 closure.

## Still open before B2 closure

1. align visible product lockup/logo to DANTE;
2. review overall Home palette/skin;
3. review Home background/atmosphere;
4. run applicable final B2/Home responsive/visual/accessibility QA after those visual decisions land.

No backend endpoint, persistence entity, Domain change or production-framework selection is created by this checkpoint.
