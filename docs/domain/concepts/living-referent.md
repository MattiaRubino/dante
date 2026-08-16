# Living Referent v0

**Status:** Current accepted scoped baseline — pending repository closure QA  
**Accepted:** 2026-08-16  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **A Living Referent is the persistent native representation of an individually tracked non-human living organism/specimen whose distinct identity and materially relevant life/care history matter across LifeOS contexts independently from names, species/type labels, ownership/care relations, current Place, Subject role, provider identifiers or any one Observation/Activity.**

Canonical question:

> **Which individually tracked non-human living organism/specimen is this?**

Classification:

```text
Living Referent
= SCOPED NATIVE NON-HUMAN LIVING IDENTITY

NEW NATIVE REFERENT
YES
```

The concept is deliberately bounded. It is not a universal `LivingThing`, `BiologicalEntity`, `ManagedObject` or `Thing` root.

---

# 1. Why Living Referent exists

LifeOS already needs descriptive facts about living non-human subjects, but Subject is a contextual aboutness role and explicitly does not create identity. Asset is scoped to individually tracked non-human physical objects and deliberately excludes animals and plants by default.

The second Whole-Domain V3 safety rerun, now evaluated against the accepted LifeOS North Star and product simulations, demonstrated a concrete identity gap for individually tracked living organisms/specimens whose continuity matters over time.

Examples include:

```text
specific dog with years of weight, care and veterinary history
specific cat with changing caregiver/owner/location
specific bonsai with long-term care and condition observations
specific tree individually tracked through maintenance and health history
specific propagated specimen once it becomes independently tracked
```

Without Living Referent identity, LifeOS would be forced to either:

1. misuse Subject as an identity wrapper;
2. broaden Asset into living organisms despite its accepted physical-object boundary;
3. create ad-hoc `Pet`, `Plant`, `Animal`, `Tree`, etc. identities independently;
4. flatten persistent living identity into labels inside Observations/Activities.

All four alternatives lose semantic integrity or create unnecessary duplication.

---

# 2. Individual identity is the trigger

Physical existence or biological individuality alone is not sufficient.

Canonical rule:

> **A Living Referent is justified only when the identity of the specific organism/specimen materially matters across time or contexts.**

Examples:

```text
one companion animal with care/history
YES

one individually managed bonsai
YES

one historically tracked olive tree
POSSIBLY YES when individual identity matters

10,000 crop plants tracked only by area/count/yield
NO one referent per organism required

generic lawn/grass population
NO
```

Bulk populations, crops, biological quantities and undifferentiated stock must not create one Living Referent merely because individual organisms exist.

---

# 3. Living Referent versus Person

Person is native human identity.

Living Referent is non-human living identity.

```text
Person != Living Referent
```

Human health/care semantics continue to reference Person. Living Referent must not become a common superclass for Person merely because both are living organisms.

---

# 4. Living Referent versus Asset

Asset is the accepted scoped native identity for individually tracked non-human physical objects whose identity and management history matter.

Living Referent is a distinct scoped native identity for individually tracked non-human living organisms/specimens.

```text
Living Referent != Asset
```

A dog, cat, plant or tree does not become an Asset merely because it is owned, possessed, managed, valuable, scheduled or observed.

Conversely, a camera, car or laptop does not become a Living Referent merely because it has a lifecycle or condition history.

Shared capabilities do not collapse identity categories:

```text
persistent identity
history
location
ownership/possession
observations
responsibility
resource use
```

may apply to both while their native identities remain distinct.

---

# 5. Living Referent versus Subject

Subject is contextual aboutness.

Living Referent is native identity.

Example:

```text
Living Referent L17
Luna

Observation O9
subject -> L17
weight = 18.2 kg
```

Therefore:

```text
Living Referent != Subject
Living Referent may play Subject role
Subject role does not create Living Referent identity
```

An unresolved descriptive record may temporarily have unknown Subject. Later reconciliation to a Living Referent must preserve materially relevant attribution history.

---

# 6. Species, breed, cultivar and type are not identity

Taxonomic/product vocabulary answers what kind of organism/specimen something is; Living Referent answers which individual is being tracked.

```text
species != identity
breed != identity
cultivar != identity
variety != identity
common name/type label != identity
```

A taxonomic correction does not automatically create a new Living Referent.

Example:

```text
T0 species recorded incorrectly
T1 corrected classification

same organism
same Living Referent
```

The general kernel does not define a universal biological taxonomy ontology. Specialist veterinary, botanical, agricultural or scientific vocabularies may attach where required.

---

# 7. Name and identifiers are evidence, not canonical identity

Living Referent identity is independent from:

```text
name
nickname
tag
microchip number
provider animal/plant ID
registry identifier
external-system record ID
```

These may be strong reconciliation evidence but do not silently become LifeOS canonical identity.

Canonical rules:

```text
rename != new Living Referent
identifier correction != new Living Referent automatically
provider record replacement != new Living Referent automatically
matching identifier != automatic merge when materially ambiguous
```

AI/provider reconciliation may propose an identity match but must not silently merge living referents where ambiguity is material.

---

# 8. Ownership, possession, care and stewardship are external relations

Living Referent identity does not mean `living thing I own`.

```text
Living Referent
!= Ownership
!= Possession
!= Responsibility
!= Coordination Stewardship
!= Authority
!= Visibility
```

Examples:

```text
animal owner changes
→ same Living Referent

caregiver changes
→ same Living Referent

temporary holder changes
→ same Living Referent
```

Ownership and Possession retain their accepted contextual relation semantics. Responsibility/Authority/Visibility remain independently governed.

---

# 9. Place and container continuity do not define organism continuity

Current location is not identity.

```text
move to another room
move to another home
move to veterinarian
move plant outdoors

!= new Living Referent
```

Likewise container continuity is not organism continuity.

```text
Plant P1 lives in Pot A
P1 dies
new Plant P2 placed in Pot A

P2 != P1
same container != same organism
```

Where the pot/container itself is materially tracked, it may independently be an Asset.

---

# 10. Life, death and historical continuity

Death does not erase identity/history.

```text
living
→ deceased
→ historical record consulted later
```

may remain one Living Referent identity where historical continuity matters.

Living Referent v0 does not impose a universal lifecycle enum. Species/domain-specific states remain specialist/profile semantics unless a shared kernel need is demonstrated.

Canonical rule:

> **A materially continuous organism/specimen retains identity across ordinary care, location, ownership, condition and life-state changes; death does not delete truthful history.**

---

# 11. Propagation, offspring and identity discontinuity

Biological derivation does not imply identity continuation.

Example:

```text
Plant P1
        ↓ cutting
C1
```

If C1 is not independently tracked, no separate native identity is required merely because the cutting exists.

If C1 becomes a separately tracked specimen whose own history matters:

```text
C1 -> Living Referent P2
P2 != P1
```

The same principle applies to offspring or separated organisms: distinct biological origin does not automatically require a kernel record, but once independent identity materially matters it must not be collapsed into the parent/source identity.

Detailed genealogy, pedigree, propagation science and inheritance are specialist semantics and are not introduced by v0.

---

# 12. Observation, Activity and Content Artifact boundaries

A Living Referent can participate in existing semantics without those semantics defining identity.

```text
Observation about Living Referent
!= Living Referent

Activity concerning Living Referent
!= Living Referent

Content Artifact about Living Referent
!= Living Referent
```

Examples:

```text
weight observation
feeding/care activity
vet appointment/event
vaccination document
photo
care note
```

remain owned by their respective semantic families while referencing the same native Living Referent where appropriate.

---

# 13. Resource boundary

Resource is a contextual planning/execution role/capability, not identity.

A Living Referent may play Resource role only where the workflow truthfully treats the organism/specimen as satisfying an execution need.

```text
Living Referent != Resource
Resource role does not create or redefine Living Referent identity
```

The existence of that possibility does not license treating companion animals/plants as generic resources by default.

---

# 14. Multi-actor and privacy implications

One organism/specimen should normally have one canonical Living Referent identity, not one copy per actor.

```text
Living Referent L17

owner A
caregiver B
responsible actor C
viewer D
```

Canonical guardrails:

```text
shared Living Referent != all related data shared
Visibility(referent) != Visibility(all care/health/location/history facets)
ownership != Responsibility != Authority != Visibility
care responsibility != ownership
seeing owner + referent != seeing ownership relation automatically
AI source access != disclosure permission
```

Private notes, health/care observations, exact location, ownership or identifying tag data may have independently bounded Visibility.

---

# 15. Correction, merge and split

LifeOS may later discover that:

- two imported records refer to the same living organism/specimen;
- one presumed referent actually represented two distinct organisms;
- a provider/tag/name attribution was wrong;
- an organism replacement was incorrectly treated as continuity.

Canonical rule:

> **Identity reconciliation must preserve materially relevant prior knowledge and must not fabricate that LifeOS always knew the corrected identity.**

Exact persistence mechanics are deferred to logical-model design.

---

# 16. AI boundary

AI may:

- suggest likely species/breed/cultivar/profile classification;
- propose identity reconciliation from authorized evidence;
- summarize care/history;
- surface contradictory identifiers/classifications;
- organize authorized Observations/Activities/Documents around the referent.

AI must not silently:

- establish identity merge from probabilistic similarity;
- treat classification inference as authoritative identity truth;
- infer owner/caregiver/Authority/Visibility merely from co-occurrence;
- disclose private care/location/history because it resolved identity;
- create one Living Referent per detected organism when individual identity does not materially matter.

```text
AI classification != established classification truth
AI identity match != canonical merge
```

---

# 17. Simple UI versus kernel semantics

The product does not need to expose the generic term `Living Referent` to users.

Natural UI profiles may say:

```text
Pets
Plants
My dog
My cat
Bonsai
Trees
Garden specimens
```

Kernel precision must not force generic ontology language or complex setup into simple workflows.

A user can create `Luna` as a pet in a compact flow while the kernel preserves identity/history boundaries internally.

---

# 18. External benchmark interpretation

The targeted benchmark used during the V3 review showed a recurring pattern in mature animal/plant/clinical-adjacent systems: the individual living subject/specimen is kept distinct from classification vocabulary and from care/history records.

This benchmark is supporting evidence only. LifeOS does not inherit external domain schemas, veterinary/clinical models, botanical taxonomies or provider object structures.

---

# 19. Canonical hardenings

```text
LIV-01  Living Referent is scoped native non-human living identity.
LIV-02  Individual identity must materially matter over time.
LIV-03  Living Referent != Person.
LIV-04  Living Referent != Asset.
LIV-05  Living Referent != Subject.
LIV-06  Living Referent may play Subject role.
LIV-07  Living Referent != Resource.
LIV-08  Living Referent may play Resource role where truthful.
LIV-09  Animal / Plant / Pet are bounded kinds/profiles, not kernel roots.
LIV-10  Species/breed/cultivar != individual identity.
LIV-11  Name != identity.
LIV-12  Provider ID / tag / microchip != canonical identity.
LIV-13  Ownership != identity.
LIV-14  Possession != identity.
LIV-15  Care Responsibility != identity.
LIV-16  Current Place != identity.
LIV-17  Observation about a Living Referent != its identity.
LIV-18  Activity concerning a Living Referent != its identity.
LIV-19  Content Artifact about a Living Referent != its identity.
LIV-20  Rename does not create a new referent.
LIV-21  Descriptive/taxonomic correction does not automatically create a new referent.
LIV-22  Death does not erase identity/history.
LIV-23  New organism/specimen != continuation merely because container/owner/location is the same.
LIV-24  Propagation/cutting creates a new referent only when distinct identity becomes materially tracked.
LIV-25  Bulk/fungible biological populations do not require one referent per organism.
LIV-26  Identity reconciliation preserves material history.
LIV-27  AI identification/classification != established truth.
LIV-28  AI identity match != canonical merge.
LIV-29  Shared referent != all related information shared.
LIV-30  Visibility of referent != visibility of all care/health/ownership/location/history facets.
LIV-31  Ownership != Responsibility != Authority != Visibility.
LIV-32  Veterinary/botanical specialist ontology is not imported into the general kernel.
LIV-33  Biological genealogy/propagation science remains specialist absent demonstrated product need.
LIV-34  No SQL/API/persistence shape is accepted here.
```

---

# 20. Non-goals

Living Referent v0 does **not** define:

- universal animal/plant taxonomy;
- veterinary medical records ontology;
- clinical diagnosis/treatment semantics;
- agricultural herd/flock/crop management;
- breeding/pedigree/genetics;
- botanical propagation/genealogy engine;
- legal animal ownership law;
- wildlife population tracking;
- ecological species/population ontology;
- biological specimen-lab ontology;
- SQL tables, ORM classes, API resources or migrations.

Those require separate evidence and specialist review.

---

# 21. Canonical result

```text
LIVING REFERENT v0
SCOPED NATIVE NON-HUMAN LIVING IDENTITY

PASS WITH HARDENING

NEW NATIVE REFERENT
YES

UNIVERSAL LIVING THING ROOT
NO

ANIMAL ROOT
NO

PLANT ROOT
NO
```

Normative validation: `../checkpoints/living-referent-v0-validation.md`.
