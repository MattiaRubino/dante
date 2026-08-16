# Place v0

Status: **PASS WITH HARDENING**

Place is the **scoped native spatial referent** used when recognizing the same physical/spatial place across LifeOS contexts materially matters over time.

> **Place is the persistent native representation of a materially reusable physical/spatial referent or bounded geographic area whose identity matters independently from names, addresses, coordinates, provider identifiers, ownership, Resource role or any one Event/Activity/Person/Asset association.**

Core question:

> **Which persistent spatial referent is this?**

Examples may include a home, office, room, venue, airport, hotel, client site, park or another bounded geographic/spatial referent where reuse/history/reconciliation matter.

## Canonical classification

```text
Place
= SCOPED NATIVE SPATIAL REFERENT

NEW NATIVE REFERENT
YES

Location
= contextual/product spatial vocabulary
NOT a second universal native root
```

## Identity boundaries

```text
Place != Address
Place != coordinates / geometry
Place != provider Place ID
Place != Asset
Place != Resource
Place != Subject
Place != Event
Place != Activity
Place != Schedule
Place != Actual
Place != Property / ownership
```

Address, coordinates/geometry and provider IDs may identify, locate, describe or reconcile a Place but do not individually define LifeOS canonical identity.

A Place may play Subject or Resource role where truthful without those roles manufacturing Place identity.

## Spatial relations are specific

Do not introduce a universal `LocationRelationship` merely because several concepts can have spatial context.

Prefer the most specific truthful semantics, for example:

```text
Event venue
Activity location/context
travel origin
travel destination
Asset located-at
Person home place
Person work place
Resource venue/site
```

Specific spatial relation semantics may have different history/privacy/actuality rules. `Location` is useful product/domain vocabulary, not a universal relation root.

## Home / Work / Gym style labels

`Home`, `Work`, `Gym`, `Client site` and similar labels are contextual roles or product vocabulary, not Place identity.

```text
2026 Home -> Place A
2028 move
Home -> Place B
```

Place A remains Place A; the historical Home association is not rewritten.

## Planned versus actual spatial context

Expected/accepted location and actual location must remain distinguishable where consequential.

```text
Event expected venue -> Place A
Actual occurrence    -> Place B
```

The later Actual does not rewrite the earlier accepted venue history.

## Place versus Asset / Property

A building may have both spatial-place semantics and physical-object management semantics when both materially matter.

```text
Place
= spatial/venue identity

Asset
= individually tracked physical-object identity
```

Do not force every home/building into both identities and do not introduce universal `Property`, `ManagedObject`, `PlaceAsset` or ownership roots from this review.

Legal title/property-right semantics remain outside the current LifeOS kernel.

## External identifiers and reconciliation

Provider Place IDs, geocoders, postal addresses and coordinates are external/value evidence for identification/reconciliation.

```text
provider representation != LifeOS Place identity
```

Provider identifiers may change. AI/integration matching may propose that several representations refer to one Place but must not silently merge materially ambiguous Places.

## History and correction

```text
current address != historical address
current spatial role != historical spatial role
correction != silent overwrite
provider change != Place replacement automatically
```

A correction to coordinates/address may preserve Place identity when the spatial referent is unchanged. A move to a genuinely different place creates/uses a different Place rather than mutating the old one into the new referent.

## Multi-actor / privacy

Place identity and spatial associations may be sensitive independently.

```text
Visibility(Event venue)
!= Visibility(private Home association)
!= Visibility(private travel origin/route)
```

Authority over an Event/Resource does not grant universal access to a Person's private Places. AI/system ability to reason over an authorized Place does not create disclosure permission.

## Resource boundary

A room/place may play Resource role where capacity/availability matter.

```text
Place != Resource
Place may play Resource role
```

Resource eligibility/allocation does not define Place identity.

## Trigger / travel boundary

Geofence, distance, travel-time and route behavior are derived/integration capabilities over Place/geometry and accepted Conditional Policy/Time semantics. They are not new Place identity primitives.

## Non-goals

Place v0 does not establish:

- legal property/title semantics;
- universal geographic hierarchy/tree;
- GIS topology ontology;
- universal address schema;
- provider-specific place taxonomy;
- routing engine;
- geocoder;
- map-provider source of truth;
- SQL/API/persistence representation.

## Canonical result

```text
PLACE / LOCATION v0

Place
SCOPED NATIVE SPATIAL REFERENT
PASS WITH HARDENING

Location
CONTEXTUAL / PRODUCT SPATIAL VOCABULARY
NOT UNIVERSAL NATIVE ENTITY / ROOT
```

Normative validation: `../checkpoints/place-v0-validation.md`.
