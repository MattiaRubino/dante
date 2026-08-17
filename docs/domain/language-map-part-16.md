<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-15.md" -->
> **Canonical continuation of the single logical Language Map.** Earlier terminology remains preserved; this continuation records Place / Location v0 terminology only.

# 2026-08-16 — Place / Location terminology

## Place

Use capitalized **Place** for the accepted scoped native spatial referent whose persistent identity matters across LifeOS contexts.

```text
Place
= native spatial referent
```

Examples may include a reusable home, office, room, venue, airport, hotel, client site or bounded geographic place.

## Location

Use **location** as contextual/product spatial language unless a specific spatial relation is known.

Do not create a universal `Location` entity/root.

Prefer specific meanings such as:

```text
Event venue
Activity location/context
travel origin
destination
Asset located-at
Home place
Work place
```

## Address / coordinates / provider IDs

```text
Address != Place
coordinates / geometry != Place
provider Place ID != LifeOS Place identity
```

These may locate/reconcile/describe a Place.

## Home / Work / Gym labels

Treat as contextual roles/product vocabulary, not native Place identity. A Person may change Home from Place A to Place B while both Places retain independent history.

## Property

Do not use `Property` as a universal kernel root from this review. Legal title/rights remain outside the current kernel.

## Virtual location

A meeting link/virtual room is not Place by default. Use integration/product semantics appropriate to the actual capability.

## Rejected kernel vocabulary

```text
Location entity/root
LocationRelationship root
Property root
PlaceAsset root
ManagedObject root
provider Place ID as canonical identity
```

Normative reference: `checkpoints/place-v0-validation.md`.
