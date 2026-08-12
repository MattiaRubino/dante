# Asset v0

**Status:** Current accepted baseline — explicitly reopenable  
**Accepted:** 2026-08-12  
**Current revision:** 2026-08-12 — Resource v0 boundary resolved; terminology-neutral Asset revisit remains mandatory  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **An Asset is a persistent native representation of an individually tracked non-human physical object whose distinct identity and management history materially matter within LifeOS. Asset identity is independent of ownership, possession, location, current operational state, Subject role, Resource role, current Account context, and external/provider identifiers.**

This is the **current scoped baseline**, not a claim that every managed/tracked thing in LifeOS is an Asset and not a claim that the word `Asset` must be the eventual product/UI label.

A mandatory terminology-neutral re-review is registered before final Cluster-4 closure to test whether a stronger cross-domain abstraction exists.

---

# 1. Why Asset exists

LifeOS needs a reusable identity/lifecycle concept for durable physical objects where the **specific instance** matters over time.

Examples:

```text
Sony A7 IV body — serial X
car — VIN Y
laptop — serial Z
bicycle — frame number Q
musical instrument — specific instrument
power tool — specific unit
appliance — specific installed unit
```

These objects can accumulate materially persistent history:

- acquisition;
- configuration/specification;
- maintenance and repair;
- warranty/service events;
- location changes;
- custody/possession changes;
- observations such as odometer, shutter count, battery health, condition;
- documents and attachments;
- temporary Resource use;
- transfer/sale/retirement/loss;
- external-system representations and reconciliations.

Without a bounded Asset identity, LifeOS would be pushed toward either:

1. duplicating the same identity/lifecycle semantics in Vehicle, Camera, Laptop, Tool, Appliance, etc.; or
2. flattening every physical thing into generic Observation/JSON/Subject/Resource structures.

Asset exists only where one persistent object identity genuinely adds semantic value.

---

# 2. Asset is native identity, not a contextual role

An Asset exists independently of whether anything currently observes, uses, owns, schedules, or manages it.

```text
Asset A17
Sony A7 IV
```

may later play:

```text
Subject role
Resource role
owned-by relationship
held-by relationship
maintenance-responsibility relationship
location relationship
```

Those relations do not define Asset identity.

Canonical rule:

> **Asset identity belongs to the tracked object itself; contextual roles and relationships do not manufacture or replace that identity.**

---

# 3. Asset versus Subject

Subject answers:

> Who or what is this descriptive record primarily about?

Asset answers:

> Which individually tracked durable physical object is this?

Example:

```text
Asset A17
Sony A7 IV
        ↑ Subject role
Observation
shutter count = 32,411
```

Therefore:

```text
Asset != Subject
Asset may play Subject role
Subject role does not create Asset identity
```

Not every Subject is an Asset. People, environments, events, groups and other future referents may play Subject role without being Assets.

---

# 4. Asset versus Person

Person is native human identity.

Asset is currently scoped to non-human physical objects.

```text
Person != Asset
```

The old `Asset/Soggetto` discovery language that grouped people with managed objects is superseded by the accepted Person and Subject boundaries.

A Person may own, use, hold, maintain, observe, schedule, or be responsible for an Asset, but those relationships do not turn Person into Asset.

---

# 5. Asset versus Resource

Resource v0 is now accepted as a **contextual planning/execution role/capability**, not an entity/root.

Asset concerns persistent physical-object identity and management history.

The same object may play Resource role:

```text
Asset A17
camera

Photo-shoot Activity
Resource Requirement
camera suitable for wildlife photography

Asset A17
candidate / selected provider
Resource role
```

but an Asset may exist while not currently usable, schedulable or relevant to an execution need.

Conversely, a Person, Place, service, pool or consumable supply may play Resource role without being an Asset.

Therefore:

```text
Asset != Resource
Asset may play Resource role
Resource role does not redefine Asset identity
```

This boundary is **RESOLVED at the current conceptual baseline** by `concepts/resource.md` and `checkpoints/resource-v0-validation.md`.

The mandatory terminology-neutral Asset revisit remains active: Resource v0 must continue to compose if Asset is later narrowed, renamed, generalized or rejected.

---

# 6. Asset versus ownership, possession, custody and stewardship

Asset does not mean `thing I own`.

Examples:

```text
company laptop
Asset = laptop
owner = company
holder = Mattia
```

```text
rented camera
Asset = camera
owner = rental company
holder = Mattia
```

```text
shared car
Asset = car
owners = A + B
current holder = A
maintenance steward = B
```

Canonical guardrail:

```text
Asset identity
!= owner
!= holder
!= possessor
!= custodian
!= steward
!= responsible actor
!= governor
```

Ownership, possession, custody, stewardship, responsibility and authority belong to future typed Relationship/Authority semantics.

---

# 7. Asset versus product/model/type

The physical instance and the shared product/model definition are different.

```text
Sony A7 IV
= product/model concept

my specific body, serial X
= Asset instance
```

Canonical rule:

> **Asset identity is instance identity; common model/type/catalog semantics must not replace the individual tracked object.**

A future logical model may introduce model/type/profile structures, but Asset v0 does not pre-approve their exact shape.

---

# 8. Physical thing does not automatically mean Asset

The fact that something is physical is insufficient.

```text
100 AA batteries
20 paper sheets
50 identical bottles
bulk screws
```

normally should not create one Asset identity per item when individual identity does not matter.

Canonical rule:

> **Individual identity must materially matter over time for Asset semantics to be justified.**

Fungible stock, consumables, lots, inventory quantities, components and accessories may require other structures when concrete workflows justify them.

Do not create hundreds of Asset records merely because physical instances exist.

---

# 9. Asset is not every managed thing

Asset must not become the generic root for anything users care about.

Current exclusions by default:

```text
Person
animal / living companion
plant / living specimen
Document / file / credential
FinancialAccount
financial asset/liability semantics
service/subscription
abstract right/license
Goal/Plan/Event/etc.
fungible stock quantity
```

These exclusions do not imply those domains are unsupported. They mean their semantics should be modeled on their own merits rather than absorbed into Asset for convenience.

A future review may reopen the boundary if a stronger abstraction survives testing.

---

# 10. Living things

Animals and plants may have stable identity, care history, observations and relationships, but Asset v0 does **not** classify them as Assets by default.

Reason:

- care/health/living lifecycle semantics differ materially from equipment/property management;
- calling them Asset adds no current semantic advantage;
- their potential future native identity should be evaluated from real workflows rather than inherited from generic ownership/management language.

Canonical rule:

> **Stable identity alone does not make a referent an Asset.**

Living-entity modeling is deferred until concrete workflows require it.

---

# 11. Documents, accounts and digital/service referents

A passport, bank account, file, subscription or software service may all be managed, tracked and lifecycle-bearing, but Asset v0 does not absorb them.

Examples:

```text
passport
issuer + validity + document identity + replacement history
```

```text
bank account
institution + holders + currency + transaction/balance semantics
```

```text
subscription
service + entitlement + billing + renewal/cancellation semantics
```

Those are materially different from durable physical-object identity.

The fact that another product calls something an `asset` is not enough to import that taxonomy.

---

# 12. Place / property boundary

A home/building/property may simultaneously have:

- physical-object/property-management semantics;
- place/location semantics;
- ownership/legal semantics;
- capacity/resource semantics.

Asset v0 does not force a final answer.

Possible future shapes may include:

```text
Asset + Place roles
Property specialization
Place with managed physical profile
other stronger model
```

This boundary is explicitly SAFE DEFERRED and must reopen when Place/Location/Property semantics are modeled.

---

# 13. Asset lifecycle

Asset identity survives ordinary lifecycle transitions.

Example:

```text
2026 acquired
2027 repaired
2028 loaned
2029 moved
2030 sold
2032 historical record consulted
```

The tracked object may remain the same Asset identity even when ownership, location, Resource role, active management status or condition changes.

Asset v0 does not define one universal lifecycle enum such as:

```text
ACTIVE / BROKEN / SOLD / LOST / RETIRED
```

because operational states may be profile-specific.

Canonical rule:

> **Lifecycle/state changes do not automatically create a new Asset identity.**

Material replacement/substitution/identity discontinuity requires explicit evaluation rather than field overwrite.

---

# 14. Identity and external identifiers

Asset identity is not equivalent to:

```text
serial number
VIN
MAC address
barcode
provider asset ID
manufacturer account ID
integration device ID
```

These may be high-value identity/reconciliation evidence.

They do not automatically establish sameness because:

- identifiers can be missing, reused, mistyped or provider-scoped;
- components may be replaced;
- multiple integrations may represent one object differently;
- one provider record may represent a subsystem rather than the whole physical object.

Canonical guardrail:

> **External identifiers help reconcile Asset identity; they do not silently become canonical Asset identity.**

AI/integration matching may propose identity links but must not silently merge Assets where ambiguity is material.

---

# 15. Correction, merge and split

LifeOS may later discover that:

- two imported representations are the same Asset;
- one presumed Asset actually represented two distinct objects;
- the wrong serial/model/identity attribution was attached;
- a replaced physical object was incorrectly treated as continuation of the old one.

Material correction must preserve history through future Provenance/Version/Decision semantics.

Canonical rule:

> **Identity reconciliation must not fabricate that LifeOS always knew the corrected Asset identity.**

Exact merge/split persistence is deferred to logical data modeling.

---

# 16. Asset and Observation

Observations may describe an Asset without replacing its lifecycle/history.

Examples:

```text
odometer = 84,220 km
battery health = 87%
shutter count = 32,411
condition = scratched
firmware version = 4.00
```

Observation captures contextual measured/asserted facts.

Asset retains native object identity.

```text
Asset != Observation
Observation about Asset != Asset state source-of-truth automatically
```

Where richer specialist semantics exist — e.g. a repair work order or financial transaction — do not flatten them into Observation merely to attach them to Asset.

---

# 17. Asset and history/provenance

Asset history may combine native events/records, Observations, documents and derived projections.

Do not introduce a universal `AssetHistoryEntry` merely to build a timeline.

Preferred direction:

```text
native records
        ↓
relations to Asset
        ↓
query / timeline / projection
```

not:

```text
native record
        ↓ duplicate
AssetHistoryEntry
```

Provider/import/repair/correction lineage follows Provenance semantics where material.

---

# 18. Multi-actor implications

One Asset should normally represent one tracked real-world object, not one copy per user.

```text
Asset A17
car

owner A + B
holder A
maintenance steward B
driver C
viewer D
```

These actor-scoped relations/states do not create multiple Asset identities.

Canonical guardrails:

- shared Asset != all related data shared;
- ownership != Authority != Visibility;
- current holder != owner;
- maintenance responsibility != ownership;
- one actor's private notes/Observations do not automatically become shared Asset state;
- Account membership does not define Asset identity;
- historical relationships may survive current-access changes where policy permits.

---

# 19. Privacy and selective disclosure

Asset identity and related metadata may themselves be sensitive.

Examples:

- exact location of a valuable object;
- serial/VIN;
- ownership;
- home-security devices;
- repair/condition history;
- purchase price;
- private documents.

Therefore:

> **Visibility of an Asset does not automatically imply visibility of every Observation, document, location, owner, serial identifier or provenance fragment related to it.**

Exact Authority/Visibility semantics remain deferred.

---

# 20. AI boundary

AI may:

- suggest that two provider/device records refer to the same Asset;
- classify a physical object into a product profile;
- summarize maintenance/history;
- suggest likely maintenance based on authorized records;
- surface inconsistent identifiers or duplicate candidates;
- propose an Asset as a Resource candidate where an execution requirement is compatible.

AI must not silently:

- merge distinct Assets because identifiers look similar;
- treat ownership as proven from possession/import context;
- disclose private location/ownership/history to another actor;
- turn every physical referent into Asset automatically;
- invent lifecycle transitions from absence of data;
- convert candidate suitability into authoritative allocation/reservation.

---

# 21. Simple UI versus kernel semantics

Users need not see a generic `Asset` noun everywhere.

UI can present natural profiles:

```text
My car
Sony A7 IV
MacBook Pro
Bike
Home appliances
Gear
```

The kernel may reuse Asset identity while product/UI language remains domain-specific.

Conversely, a product section called `Assets`, `Gear`, `Things`, `Inventory` or similar would not automatically broaden the kernel definition.

---

# 22. External benchmark synthesis

Mature systems were treated as evidence, not authority.

Useful recurring lessons include:

- maintenance/CMMS systems preserve identity, lifecycle, location and work history for individually managed equipment;
- inventory/IT-asset systems distinguish individually tagged Assets from accessories/components/consumables tracked differently;
- smart-home systems often separate physical Device identity from functional Entity/state representations and Area/location;
- model/catalog identity is distinct from individual object identity;
- source/provider identifiers may not be sufficient to merge representations safely.

LifeOS adapts those lessons while deliberately rejecting their domain-specific taxonomies as universal truth.

A **terminology-neutral benchmark re-review** remains mandatory before final Cluster-4 closure because `Asset` may otherwise inherit assumptions from asset-management products merely through naming.

---

# 23. Adversarial reductio summary

## REMOVE Asset entirely

Durable individually tracked objects require duplicated identity/lifecycle semantics across Vehicle/Camera/Laptop/Tool/etc. or get flattened into generic structures.

**Result:** FAIL under current evidence.

## Asset = Subject

Subject is contextual aboutness and includes non-Asset referents.

**Result:** FAIL.

## Asset = Resource

Identity/history and operational eligibility/capacity semantics differ.

**Result:** FAIL.

## Asset = owned thing

Leased, borrowed, company-owned and shared objects fail.

**Result:** FAIL.

## Asset = every physical item

Fungible stock and consumables explode into meaningless identity rows.

**Result:** FAIL.

## Asset = every managed thing

Person, living things, documents, accounts, services, places and abstract rights become one semantic dumping ground.

**Result:** FAIL.

## Asset = financial asset

Financial semantics differ materially.

**Result:** FAIL.

## Asset = durable individually tracked non-human physical object

Identity/lifecycle reuse survives tested scenarios without absorbing unrelated domains.

**Result:** PASS WITH HARDENING — current baseline only.

---

# 24. Core invariants

1. **Asset is a native identity-bearing concept, not a contextual role.**
2. **Asset currently represents an individually tracked non-human physical object whose distinct identity/history materially matter.**
3. **Physical thing != Asset automatically.**
4. **Managed thing != Asset automatically.**
5. **Person != Asset.**
6. **Asset != Subject; Asset may play Subject role.**
7. **Asset != Resource; Asset may play Resource role.**
8. **Resource role does not redefine Asset identity or imply current allocation/reservation.**
9. **Asset identity != owner/holder/custodian/steward/responsible actor.**
10. **Asset identity != product/model/type definition.**
11. **External/provider identifiers are reconciliation evidence, not canonical identity by default.**
12. **Ownership/location/status changes do not automatically change Asset identity.**
13. **Fungible stock does not require one Asset per physical unit.**
14. **Living things, Documents, FinancialAccounts, services and financial assets are not absorbed by default.**
15. **Asset history should compose from native records rather than a universal history-entry wrapper.**
16. **Shared Asset identity does not imply shared visibility of every related record.**
17. **AI may propose Asset reconciliation/resource candidacy but does not silently establish identity/ownership/Authority/allocation.**
18. **Asset does not imply a final SQL table hierarchy, product taxonomy or visible UI label.**
19. **The current physical/durable scope must be retested terminology-neutrally before final Cluster-4 closure.**

---

# 25. Persistence/API implications — deliberately not physical design

The future logical model must be able to support where justified:

- stable Asset identity;
- type/model/profile references without making them identity;
- external identifiers with source/provenance;
- lifecycle/history relations;
- Subject-role references from Observations;
- Resource-role participation under Resource v0;
- ownership/possession/custody/stewardship relationships without storing them as identity fields;
- location/property relationships;
- merge/split/reconciliation history;
- specialist extensions without arbitrary universal JSON.

Do not infer from Asset v0 that LifeOS requires:

- one universal `assets` table containing all managed things;
- one table per Asset subtype;
- every physical item as Asset;
- one Asset row per consumable unit;
- Asset inheritance for Person/living entities/Documents/Accounts;
- one universal Asset status enum;
- `owner_id` as Asset identity;
- provider ID/serial as primary domain identity;
- a universal `asset_history_entries` table;
- Asset = Resource implementation inheritance;
- a Resource wrapper or `resource_id` merely to make an Asset schedulable.

Final persistence depends on the terminology-neutral Asset re-review, Relationships/Authority modeling and logical data-model pressure.

---

# 26. Adjacent Dependency Sweep

## RESOLVED NOW

### Asset vs Subject

Resolved at current baseline: Asset is native identity; Subject is contextual aboutness. Asset may play Subject role.

### Asset vs Person

Resolved: Person is a native human identity and is not Asset.

### Asset vs Resource

Resolved at current conceptual baseline: Asset is native physical-object identity; Resource is a contextual planning/execution role. Asset may play Resource role without duplicate identity.

**Mandatory re-test:** terminology-neutral Asset revisit + Cluster-4 integration. If Asset scope changes, rerun CORE-03, CORE-04, MA-14, XCON-01 and XCON-04 against Resource v0.

### Asset vs fungible inventory

Resolved conceptually: individual identity must materially matter. Bulk/consumable stock is not forced into Asset-per-unit semantics.

### Asset vs ownership

Resolved at identity level only: ownership does not define Asset identity. Exact ownership relation is deferred.

## SAFE DEFERRED

### Asset scope vs terminology-neutral managed-referent model

**Owner:** Data / Subjects cluster integration + clusters 1–4 deferred-dependency closure.  
**Why safe:** current durable-physical scope passes present scenarios, but benchmark evidence may be biased by asset-management terminology.  
**Mandatory action:** perform a cross-product comparison of how mature personal, inventory, smart-home, property, document, finance, pet/plant, device and service-management products represent managed/tracked referents **without starting from their names**.  
**Reopening trigger:** a broader or different identity abstraction explains the workflows with fewer exceptions and without semantic loss.  
**Tests to rerun:** CORE-03, CORE-04, CORE-06, CORE-07, CORE-08, CORE-12, CORE-13, MA-18, MA-19, XCON-01, XCON-04, CL-03, CL-04, CL-05, CL-06.

### Asset vs Place / Location / Property

**Owner:** future Place/Location/Property review or dependency closure if required earlier.  
**Why safe:** ordinary movable-object Asset semantics do not require a final property/place ontology.  
**Reopening trigger:** property/home workflows cannot preserve identity without treating place and physical asset as one concept.  
**Tests to rerun:** CORE-04, XCON-01, XCON-04.

### Asset vs living entities

**Owner:** future concrete pet/plant/living-entity workflow review.  
**Why safe:** current Asset semantics do not need them and Person/Subject already prove stable identity can exist outside Asset.  
**Reopening trigger:** recurring LifeOS workflows require a shared native identity abstraction across durable objects and living subjects.  
**Tests to rerun:** CORE-03, CORE-04, CORE-06, XCON-01.

### Asset vs Document / Artifact / FinancialAccount / service

**Owner:** future specialist reviews / dependency closure if concrete workflow becomes blocking.  
**Why safe:** each has materially different semantics and need not be forced into Asset.  
**Reopening trigger:** repeated cross-domain behavior shows one stronger shared native identity/lifecycle abstraction.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, XCON-01.

### Asset model/type/profile semantics

**Owner:** logical data model / specialist profiles.  
**Why safe:** instance identity is accepted without fixing catalog/model persistence.  
**Reopening trigger:** model/type semantics become necessary to preserve Asset identity/history correctly.  
**Tests to rerun:** CORE-04, CORE-10, CORE-13.

### Asset merge/split/reconciliation

**Owner:** logical model + Provenance/Version/Decision.  
**Why safe:** identity invariants are fixed; physical reconciliation mechanics remain open.  
**Reopening trigger:** imports/integrations cannot preserve identity/history under current semantics.  
**Tests to rerun:** CORE-02, CORE-09, XCON-01, XCON-03.

No current dependency is a structural blocker, but the terminology-neutral scope review is **mandatory before final Cluster-4 closure**.

---

# 27. Rejected alternatives

Rejected under current evidence:

- universal managed-object root;
- Asset = Subject;
- Asset = Resource;
- Asset = Person;
- Asset = owned thing;
- Asset = any valuable thing;
- Asset = every physical item;
- Asset = financial asset;
- Asset = document/account/service catch-all;
- provider ID/serial as automatic canonical identity;
- universal Asset status enum;
- universal Asset-history wrapper.

---

# 28. Reopening triggers

Reopen Asset v0 if later evidence shows that:

1. terminology-neutral cross-product review finds a stronger shared abstraction for managed/tracked referents;
2. Resource/Requirement/Allocation modeling exposes a contradiction with the current Asset boundary or a stronger shared identity model;
3. Place/Property, living-entity, Document, FinancialAccount or service workflows repeatedly require the same identity/lifecycle semantics and the current exclusions become artificial;
4. ordinary personal use cannot distinguish when a physical object deserves Asset identity without exposing arbitrary system rules;
5. integration identity/reconciliation cannot be represented safely without a different native referent model;
6. physical/logical persistence pressure requires one stronger cross-domain identity abstraction rather than profile-specific storage;
7. multi-actor ownership/custody/visibility semantics contradict the current identity independence;
8. cluster regression shows that the current `physical + durable + individually tracked` boundary is terminology-driven rather than semantically necessary.

Until that mandatory re-review or stronger evidence changes it, Asset v0 remains the current accepted baseline.