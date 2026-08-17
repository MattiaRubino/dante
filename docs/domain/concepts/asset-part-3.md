<!-- LIFEOS-CANONICAL-CONTINUATION document="asset.md" follows="asset-part-2.md" -->
> **Canonical continuation of the single logical Asset document.** Earlier Asset semantics remain preserved; this physical continuation records Place / Location integration only.

# 2026-08-16 — Place / Location integration

Place v0 resolves the historical Place/Property boundary without changing Asset identity.

```text
Asset
= individually tracked non-human physical-object identity

Place
= scoped native spatial referent
```

Canonical non-collapse:

```text
Asset != Place
Asset located-at Place != Asset identity
Place venue/site semantics != Asset physical-object semantics
```

A moving Asset may change spatial association many times while remaining the same Asset.

A building/home may have both Asset and Place semantics only when both independently matter. LifeOS must not force dual representation merely because a physical structure occupies space.

```text
building physical management
→ Asset semantics where instance/lifecycle matters

spatial venue/site identity
→ Place semantics where reusable spatial identity matters
```

No universal `Property`, `ManagedObject`, `PlaceAsset` or ownership root is introduced.

Address, coordinates and provider Place IDs belong to Place identification/reconciliation, not Asset identity.

Visibility of an Asset does not imply visibility of its current/historical Place association, and Visibility of a Place does not expose every Asset located there.

```text
ASSET v0
verdict unchanged
PASS WITH HARDENING
REOPEN 0
```

Normative reference: `../checkpoints/place-v0-validation.md`.
