<!-- LIFEOS-CANONICAL-CONTINUATION document="README.md" follows="README-part-13.md" -->
> **Canonical continuation of the single logical Domain Atlas README.** Earlier Atlas state remains preserved; this continuation records the Place / Location Whole-Domain repair only.

# 2026-08-16 — Place / Location integrated baseline

## Accepted semantic result

```text
Place
SCOPED NATIVE SPATIAL REFERENT
PASS WITH HARDENING

Location
CONTEXTUAL / PRODUCT SPATIAL VOCABULARY
NOT UNIVERSAL NATIVE ENTITY / ROOT
```

Key invariants:

```text
Place != Asset
Place != Person
Place != Subject
Place != Resource
Place != Address
Place != coordinates / provider Place ID
Place != Property / ownership
expected spatial context != Actual spatial context universally
```

Place may play Subject/Resource roles and may participate in specific spatial relations such as Event venue, Activity location, origin/destination, Home/work place or Asset located-at.

## Whole-Domain repair status

The post-Cluster-5 Whole-Domain audit originally identified three required bounded repairs:

```text
1. Place / Location
2. Content Artifact / Document
3. MonetaryAmount
```

Place is now semantically resolved pending remote propagation QA/closure.

Remaining required repairs:

```text
Content Artifact / Document
MonetaryAmount
```

Cluster 5 remains closed; this repair is bounded Data / Subjects territory hardening.

## No new universal roots

Rejected by this milestone:

```text
universal Location root
universal Property root
universal Place hierarchy
universal LocationRelationship
ManagedObject / PlaceAsset root
```

## Implementation status

```text
SQL              NOT STARTED / NOT IMPLIED
migrations       NOT STARTED / NOT IMPLIED
API              NOT STARTED / NOT IMPLIED
backend          NOT STARTED / NOT IMPLIED
frontend         NOT TOUCHED
prototype        NOT TOUCHED
main             NOT TOUCHED
```

Place is not repository `CLOSED` until remote propagation QA and the dedicated closure continuation succeed.

Normative reference: `checkpoints/place-v0-validation.md`.
