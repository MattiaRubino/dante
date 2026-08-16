# Place / Location v0 — Domain Validation Methodology v3

Status: **PASS WITH HARDENING**

This checkpoint resolves the Whole-Domain `Place / Location` repair discovered after Cluster 5 closure. It is a bounded completion on Data / Subjects semantic territory, not a new Relationships / Reasoning cycle and not a full Cluster-4 reopen.

## Current-LifeOS need

Accepted V1 product requirements materially use location/travel context across meetings, activities, availability, home/work/client-site patterns, route/travel-time reasoning, imported calendar data and location-aware planning. Historical Asset/Resource/Subject reviews explicitly left Place/Location identity open until such evidence existed.

Disposition:

```text
CURRENT LIFEOS NEED
YES
```

## Candidate hypotheses

```text
H0  no canonical Place; use strings/coordinates/provider IDs
H1  scoped native Place referent; Location remains contextual vocabulary
H2  Place = Asset
H3  Place = Resource
H4  Place = Address
H5  Place = coordinates / geometry
H6  Place = provider Place ID
H7  universal Location / Property root
```

Result:

```text
H1 SURVIVES

H0 FAIL
H2 FAIL
H3 FAIL
H4 FAIL
H5 FAIL
H6 FAIL
H7 FAIL / OVERMODELED
```

## Accepted definition

> **Place is the persistent native representation of a materially reusable physical/spatial referent or bounded geographic area whose identity matters across LifeOS contexts independently from names, addresses, coordinates, provider identifiers, ownership, Resource role or any one Event/Activity/Person/Asset association.**

Core question:

> **Which persistent spatial referent is this?**

Classification:

```text
Place
= SCOPED NATIVE SPATIAL REFERENT

Location
= contextual/product spatial vocabulary
NOT a second native identity/root
```

## Canonical hardenings — PLC-01..32

```text
PLC-01  Place is a scoped native spatial referent where persistent spatial identity materially matters.
PLC-02  Location is contextual/product vocabulary, not a universal native entity/root.
PLC-03  Place != Address.
PLC-04  Place != coordinates / geometry.
PLC-05  Place != provider Place ID or geocoder record.
PLC-06  Place != Asset.
PLC-07  Place != Resource.
PLC-08  Place != Subject.
PLC-09  Place != Event / Activity / Schedule / Actual.
PLC-10  Place != Property / ownership / legal title.
PLC-11  Address/coordinates/provider IDs may support identification/reconciliation without defining canonical identity.
PLC-12  Provider identifier change does not automatically replace Place identity.
PLC-13  AI/provider matching may propose Place reconciliation but must not silently merge material ambiguity.
PLC-14  Place may play Subject role without becoming Subject identity.
PLC-15  Place may play Resource role without becoming Resource identity.
PLC-16  Event venue is a specific spatial relation/use, not Place identity.
PLC-17  Activity location/context is a specific spatial relation/use, not Place identity.
PLC-18  travel origin/destination are specific spatial roles; no universal LocationRelationship root is accepted.
PLC-19  Asset located-at does not change Asset identity.
PLC-20  Home/Work/Gym/Client-site labels are contextual spatial roles/product vocabulary, not Place identity.
PLC-21  Changing Home from Place A to Place B does not mutate A into B; history remains reconstructible.
PLC-22  expected/accepted spatial context != Actual spatial context where reality differs.
PLC-23  Actual spatial reality does not silently rewrite prior expected/accepted spatial history.
PLC-24  Place address/coordinate correction preserves history where consequential.
PLC-25  same label/name does not establish same Place; different label/address formatting does not establish different Place automatically.
PLC-26  a building may have both Place and Asset semantics only when both independently matter; no forced dual representation.
PLC-27  universal Property / ManagedObject / PlaceAsset root is rejected.
PLC-28  Place identity or Home association does not grant Authority / Visibility / Consent / Responsibility.
PLC-29  selective disclosure may expose a venue while withholding private Home/travel/location associations.
PLC-30  geofence, routing, distance and travel-time behavior are derived/integration capabilities, not Place identity primitives.
PLC-31  virtual meeting link is not Place by default; moving Asset is not Place by default.
PLC-32  no SQL/API/address-schema/provider taxonomy is accepted by this semantic review.
```

## Deep chronology

```text
T0  Imported Event contains raw location text "HQ, Via Roma 10".
    Place identity remains unresolved; source text/provenance preserved.

T1  geocoder proposes provider record G1 + coordinates.
    proposal/evidence != established canonical Place automatically.

T2  Place P1 is established for the reusable spatial referent.
    Event venue -> P1.

T3  HQ is renamed / address formatting changes.
    Place P1 remains P1.

T4  provider representation changes G1 -> G2.
    provider change != Place replacement.

T5  Event is officially moved to Place P2.
    Event identity remains; prior venue history remains.

T6  Event actually occurs at Place P3.
    Actual spatial context = P3; prior accepted venue is not rewritten.

T7  Person moves house.
    Home role P4 -> P5.
    P4/P5 remain distinct Places and historical Home relation persists.

T8  Asset A moves P5 -> P2.
    Asset identity unchanged.

T9  wrong coordinates for P2 are corrected.
    Place identity may remain when referent is the same; correction provenance retained.

T10 conflicting provider/geocoder assertions remain unresolved where necessary.
    no universal newest/provider/AI-confidence winner.

T11 shared Event exposes venue P2 while private Home P5 remains hidden.
```

## Adversarial reductio

```text
Place = string/address                   FAIL
Place = coordinates                     FAIL
Place = provider record                 FAIL
Place = Asset                           FAIL
Place = Resource                        FAIL
Place = Subject                         FAIL
universal Location entity/root          FAIL
universal Property root                 FAIL
scoped persistent Place referent        SURVIVES
specific spatial relations              SURVIVE
```

## CORE gate

```text
CORE-01 Workflow inversion             PASS
CORE-02 Deep chronology                PASS WITH HARDENING
CORE-03 Adversarial reductio           PASS WITH HARDENING
CORE-04 Redundancy / merge-split       PASS WITH HARDENING
CORE-05 Traceability                   PASS
CORE-06 Independence                   PASS WITH HARDENING
CORE-07 External benchmark             PASS
CORE-08 Anti-pattern                   PASS WITH HARDENING
CORE-09 Correction / epistemic safety  PASS WITH HARDENING
CORE-10 Scale / history                PASS WITH HARDENING
CORE-11 Simple / power user            PASS
CORE-12 Product value / complexity     PASS
CORE-13 Implementation pressure        PASS WITH HARDENING

CORE GATE
PASS WITH HARDENING
```

## Multi-Actor gate

```text
MA-01 Identity/account independence       PASS
MA-02 Shared fact / actor overlay         PASS WITH HARDENING
MA-03 Responsibility                     PASS
MA-04 Coordination Stewardship            PASS
MA-05 Common ground                       PASS WITH HARDENING
MA-06 Authority                           PASS
MA-07 Selective disclosure               PASS WITH HARDENING
MA-08 Inference privacy                  PASS WITH HARDENING
MA-09 Partial adoption                   PASS
MA-10 Representation/on-behalf-of        PASS
MA-11 Lifecycle/revocation               PASS WITH HARDENING
MA-12 Conflict/adversarial               PASS WITH HARDENING
MA-13 Unequal power                      PASS WITH HARDENING
MA-14 Resource/capacity                  PASS WITH HARDENING
MA-15 Burden distribution                PASS
MA-16 Progressive disclosure             PASS
MA-17 AI / automation                    PASS WITH HARDENING
MA-18 Specialist systems                PASS
MA-19 Primitive redundancy              PASS WITH HARDENING
MA-20 Actor-scoped attribution          PASS WITH HARDENING

MULTI-ACTOR GATE
PASS WITH HARDENING
```

## Cross-concept gate

```text
XCON-01 Identity                         PASS WITH HARDENING
XCON-02 Authority                        PASS
XCON-03 current/history/material state   PASS WITH HARDENING
XCON-04 Relationships / Reasoning        PASS WITH HARDENING
XCON-05 Multi-Actor                      PASS WITH HARDENING
XCON-06 Language                         PASS WITH UPDATE

XCON GATE
PASS WITH HARDENING
```

## External benchmark classification

Targeted evidence was used only as benchmark evidence:

```text
iCalendar LOCATION/GEO
→ BORROW distinction between textual location and coordinates
→ REJECT as sufficient persistent LifeOS Place identity

Google Place IDs
→ BORROW provider reconciliation identifiers
→ REJECT provider ID as LifeOS canonical identity

FHIR Location
→ ADAPT separation of location identity from address/position
→ REJECT healthcare-specific taxonomy/resource model
```

External products/standards are evidence, never ontology authority.

## Final dependency disposition

```text
Legal Property / title
→ NOT REQUIRED BY CURRENT LIFEOS KERNEL

universal Location root
→ REJECTED / OVERMODELED

universal Place hierarchy/tree
→ REJECTED / OVERMODELED

Address / coordinate exact data shape
→ STAGE-DEFERRED logical representation

provider IDs / geocoding
→ integration/reconciliation stage

routing / distance / travel-time engine
→ derived/integration capability

geofence trigger
→ Place/geometry + Conditional Policy

virtual meeting link
→ NOT Place by default

moving vehicle
→ Asset + changing spatial association; NOT Place by default

building physical management
→ composable Asset + Place where both independently matter

SQL/API
→ STAGE-DEFERRED
```

```text
SEMANTIC SAFE DEFERRED  0
SEMANTIC UNCLASSIFIED   0
SEMANTIC UNRESOLVED     0
REOPEN                  0
```

## Read-only semantic verdict

```text
PLACE / LOCATION v0

PASS WITH HARDENING

Place
SCOPED NATIVE SPATIAL REFERENT

Location
CONTEXTUAL / PRODUCT SPATIAL VOCABULARY
NOT UNIVERSAL NATIVE ENTITY / ROOT

Address
LOCATOR / VALUE SEMANTICS
NOT Place identity

Geo position / geometry
SPATIAL VALUE / REFERENCE SEMANTICS
NOT Place identity

Provider Place ID
EXTERNAL IDENTITY / RECONCILIATION EVIDENCE
NOT LifeOS canonical identity

NEW NATIVE REFERENT
YES — Place

NEW UNIVERSAL LOCATION RELATION
NO
```

This checkpoint is not `CLOSED` until the exact propagation scope passes remote post-write QA and the closure continuation is written.
