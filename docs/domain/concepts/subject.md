# Subject v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **Subject is the contextual semantic role played by a native referent when a descriptive record primarily concerns that referent's state, property, condition, or asserted fact. Subject does not create independent identity: the referenced Person, Asset, Event, Device, Location, or other eligible referent retains its native identity. Being the Subject does not imply authorship, observation, recording, ownership, responsibility, authority, visibility, participation, or account identity.**

Subject answers the bounded contextual question:

> **Who or what is this descriptive record primarily about?**

Typical shapes:

```text
Person Mattia
    ↑ subject-of
Observation: body weight = 66.4 kg
```

```text
Car
    ↑ subject-of
Observation: odometer = 84,220 km
```

```text
Room
    ↑ subject-of
Observation: temperature = 21.6 °C
```

Subject is therefore a **canonical semantic role / relationship capability**, not an independently persistent domain entity and not a universal root type.

---

# 1. Why Subject semantics exist

LifeOS needs to distinguish what a descriptive fact concerns from who created, observed, recorded, performed, confirmed, owns, governs, or may see that fact.

Examples:

```text
subject = older adult
observer = caregiver
recorder = caregiver
device = thermometer
Observation = temperature 38.2 °C
```

```text
subject = car
Observation = odometer 84,220 km
```

```text
subject = dog
Observation = weight 18.2 kg
```

Without Subject semantics, LifeOS would be pushed toward weak alternatives:

1. assume every Observation is about the current account holder;
2. overload owner/creator/recorder as the thing being described;
3. make Person, Asset, Resource and Account interchangeable;
4. invent a generic universal `Subject` entity only to point back to native objects;
5. lose the ability to represent caregiver, asset, animal, location and external-participant scenarios naturally.

The required semantic is therefore real even though an independent Subject entity is not.

---

# 2. Subject is a role, not a new identity

If a Person is the subject of an Observation, the Person does not become a second object called `Subject`.

```text
Person P17
name = Anna

Observation O42
subject -> Person P17
property = temperature
value = 38.2 °C
```

Rejected shape:

```text
Subject S9
    ↓ wraps
Person P17
```

The wrapper creates duplicate identity, lifecycle and synchronization questions without adding domain truth.

Canonical rule:

> **Subject role assignment references the native identity of the referent; it does not manufacture a parallel Subject identity.**

A physical implementation may later need a typed reference mechanism, but that mechanism does not redefine the domain as one universal Subject table/root.

---

# 3. Eligible referents are contextual, not one inheritance tree

A Subject may be a Person, Asset, location-like referent, device, group, event/contextual object, or another future native concept when the descriptive record genuinely concerns it.

This does not mean every domain object must inherit from `Subject`.

```text
Person may play Subject role
Asset may play Subject role
Location may play Subject role
Device may play Subject role
Event may play Subject role when a descriptive assertion is about the Event itself
```

Canonical guardrail:

> **Eligibility to play Subject does not justify a universal Subject superclass, table, aggregate root, or ownership model.**

Exact eligible referent categories will be constrained by the containing record semantics and logical model rather than by a universal ontology root.

---

# 4. Subject versus Person

Person answers:

> Which human individual is represented?

Subject answers:

> Which native referent is this descriptive record about in this context?

A Person can be Subject without that role defining Person identity.

```text
Person Anna

Observation A
subject = Anna
weight = 62 kg

Activity B
performer = Anna

Event C
participant = Anna
```

The same Person identity can play several roles simultaneously.

Therefore:

```text
Person != Subject
Person may play Subject role
```

This is critical for the next Person / Actor boundary review.

---

# 5. Subject versus Actor

Actor concerns agency: acting, participating, holding responsibility, proposing, confirming, or exercising authority depending on later accepted semantics.

Subject does not require agency.

Examples:

- an infant can be a Subject;
- a non-LifeOS person can be a Subject;
- a car can be a Subject;
- a room can be a Subject;
- an animal can be a Subject.

Therefore:

```text
Subject != Actor
```

A Person may be both in different relations:

```text
Person Anna
subject of Observation X
actor/recorder of Observation Y
performer of Activity Z
```

No role should silently imply another.

---

# 6. Subject versus Account / Principal

Account/Principal concerns authenticated or acting identity and later authority/access semantics.

Subject concerns what a descriptive record is about.

Caregiver example:

```text
LifeOS account
Caregiver Anna

Observation
subject = Grandmother Maria
recorder = Anna
```

Maria may have no LifeOS account.

Canonical rules:

```text
Subject != Account
Subject != Principal
current account holder != default subject as a kernel invariant
```

Product UI may default ordinary personal entry to `me`, but that is a contextual convenience rather than canonical identity semantics.

---

# 7. Subject versus observer, recorder, source and Provenance roles

Observation already distinguishes several roles that often coincide in simple personal use but diverge in real workflows.

```text
subject
observer
recorder
source/provider/device
transformer
confirmer
authority
viewer
```

Example:

```text
subject = Maria
observer = Anna
recorder = Anna
device = thermometer
```

Subject does not answer who caused the record to exist.

Provenance explains materially relevant origin/evolution. Subject identifies what the assertion concerns.

Therefore:

```text
Subject != source
Subject != observer
Subject != recorder
Subject != transformer
Subject != Provenance
```

A subject may also be a source in a self-report, but that coincidence must be represented by roles rather than assumed universally.

---

# 8. Subject versus Resource

Resource semantics concern whether something can supply capacity, be reserved/consumed/used, or otherwise constrain execution/scheduling.

Subject semantics concern descriptive aboutness.

One native object can play both roles:

```text
Car

Observation
subject = Car
odometer = 84,220 km

Trip Activity
required Resource = Car
```

These are independent semantic questions.

Therefore:

```text
Subject != Resource
```

Resource review must not collapse every possible Subject into Resource or vice versa.

---

# 9. Subject versus Asset

Asset is a separate candidate whose exact boundary remains under review.

If an accepted Asset concept exists later, an Asset may play Subject role when a record describes it.

Examples:

```text
Car Asset
subject of odometer Observation
```

```text
Camera Asset
subject of shutter-count Observation
```

But Subject semantics do not prove that every non-person referent is an Asset.

A room, external organization, Event, or other contextual referent may be a Subject without satisfying future Asset invariants.

Therefore:

```text
Subject != Asset
Asset may play Subject role
```

---

# 10. Subject versus owner / beneficiary / participant / performer

Being the thing a record is about does not establish governance or benefit.

```text
subject = employee
```

does not imply:

```text
employee created record
employee owns record
employee can see record
manager can see every record about employee
employee authorized record
```

Likewise:

```text
subject = child
```

does not automatically establish guardian authority or visibility.

Canonical rule:

> **Aboutness must not launder ownership, authority, visibility, responsibility, participation, or consent.**

Those semantics remain separately modeled/reviewed.

---

# 11. Subject versus focus and context

External benchmark systems show a useful distinction between the primary subject of a record and another specific thing the observation is focused on.

LifeOS should preserve the boundary without prematurely adding a universal `Focus` primitive.

Example shape:

```text
primary Subject = patient
specific focus/context = device / body part / caregiver / event / session
```

Canonical direction:

> **Subject should not become a catch-all `related_to` relation for everything relevant to the record.**

Other relations such as focus, context, participant, performer, beneficiary, source, location, object, or evidence relation should remain separate when they answer different domain questions.

The exact generic/typed Relationship model belongs to the Relationships / Reasoning review.

---

# 12. Unknown and later-resolved Subject

LifeOS must not invent the current user as Subject merely because a record enters that user's account.

Example:

```text
imported reading
subject = unknown
```

Later reconciliation may establish:

```text
subject -> Person P17
```

The later association must not fabricate that the subject was known at ingestion time.

Canonical rules:

- unknown Subject may remain unknown where the record can meaningfully exist without a resolved referent;
- later subject resolution preserves materially relevant Provenance/history;
- account ownership/import destination does not prove subject identity;
- source/provider identity does not prove Subject identity.

Whether a specific record type requires a resolved Subject is a containing-concept invariant, not one universal rule.

---

# 13. Correction of Subject attribution

A record may have been attributed to the wrong referent.

Example:

```text
Observation O9
subject = Person A
```

Later:

```text
correction
subject = Person B
```

This may be a correction to the same observation/assertion identity rather than a new measurement, provided the underlying observational act is the same and the correction only fixes attribution.

Material history should preserve the prior attribution and correction basis through Provenance/Version semantics.

Canonical guardrail:

> **Changing Subject attribution must not silently erase material prior attribution history or pretend the corrected referent was known earlier.**

---

# 14. Multi-subject descriptive records

Some descriptive acts legitimately concern more than one referent.

Examples may include:

- a household-level Observation;
- a relationship-level rating;
- a group-level measurement;
- an environmental reading affecting a set of resources/people.

Do not solve this by creating a fake composite Subject merely to preserve one-field cardinality.

Canonical direction:

- permit containing concepts to define one or multiple Subject-role references when semantically justified;
- distinguish a true group/collective native referent from several independent subjects;
- do not infer that all members share identical state merely because a group is the Subject;
- cardinality belongs to the containing record semantics and logical model.

This remains a logical-model pressure point rather than a reason for a universal Subject entity.

---

# 15. Multi-actor implications

Subject role is foundational to multi-actor correctness because it prevents `user_id` coincidence from becoming domain meaning.

Canonical examples:

```text
caregiver account A
records Observation about Person B
```

```text
manager C
records assessment about Person D
```

```text
AI/system derives Observation about Asset E
```

The domain must preserve who/what the record concerns separately from who entered, generated, transformed, confirmed, governed, or may view it.

Key rule:

> **Subject identity must not depend on account participation.**

Non-LifeOS subjects are ordinary domain reality, not exceptional placeholders.

---

# 16. Privacy and selective disclosure

Subject association itself can be sensitive.

Knowing that a private Observation is about Person X may disclose information even if the value is hidden.

Therefore:

- visibility of a record does not automatically imply visibility of every related Subject detail;
- visibility of a Subject does not automatically imply visibility of all records about that Subject;
- authority over one context does not grant universal visibility into all records where the same referent is Subject;
- derived shared projections may conceal private source/subject detail where policy requires;
- AI must not infer disclosure permission merely because it can resolve the Subject internally.

Exact Visibility/Authority policy remains future work.

---

# 17. AI boundary

AI may:

- propose a Subject match from imported context;
- suggest that two records concern the same native referent;
- use resolved Subject identity to organize/query authorized context;
- identify likely attribution errors.

AI must not silently:

- replace unknown Subject with the current account holder;
- merge two native referents merely because names/details look similar;
- promote a probabilistic Subject match into established identity without policy/authority appropriate to the context;
- disclose private facts merely because it knows the Subject;
- create a universal Subject object as a shortcut around native domain identity.

Canonical rule:

> **AI may propose subject resolution; it does not automatically establish identity, authority, or disclosure rights.**

---

# 18. Simple UI versus kernel semantics

Most users should rarely see the noun `Subject`.

Personal default:

```text
Weight
66.4 kg
```

may imply `me` in the UI when the context safely establishes it.

Caregiver/asset context may expose natural labels:

```text
Maria
Temperature
38.2 °C
```

```text
My car
Odometer
84,220 km
```

Power-user/history surfaces may expose attribution and provenance when relevant.

Canonical rule:

> **Kernel separation of Subject from account/actor does not require every capture form to ask users to choose a Subject explicitly.**

---

# 19. External benchmark synthesis

External patterns were used as evidence, not design authorities.

## FHIR Observation subject/focus pattern

Useful lessons:

- `subject` points to native referents rather than requiring one universal Subject entity;
- subject and focus/context can differ;
- aboutness is distinct from performer/source/provenance roles.

LifeOS adapts the role/reference lesson but does not inherit FHIR resource taxonomy or healthcare-specific cardinalities.

## Health/personal-data stores

Useful lesson:

- a personal product may often make the human subject implicit in ordinary UX;
- source/device identity remains distinct from what the measurement concerns.

LifeOS cannot make `current account = Subject` a universal invariant because caregiver, asset, external-participant and multi-actor scenarios are first-class.

## Person/contact/account systems

Useful lesson for the adjacent Person/Actor review:

- real-world person identity can be distinct from account/contact/source representations;
- a referent should retain native identity across contextual roles.

No external schema is adopted wholesale.

---

# 20. Adversarial reductio summary

## REMOVE Subject entity

Native Person/Asset/etc. identities remain intact and descriptive records can reference them directly.

**Result:** PASS — independent Subject entity is unnecessary.

## REMOVE Subject semantics

LifeOS can no longer reliably answer who/what an Observation is about without overloading account/owner/recorder/source.

**Result:** FAIL.

## MERGE Subject with Person

Non-human referents and passive/non-account cases fail.

**Result:** FAIL.

## MERGE Subject with Actor

Passive subjects, objects, locations, animals and non-agent referents fail.

**Result:** FAIL.

## MERGE Subject with Resource

Aboutness and schedulable/usable capacity are independent.

**Result:** FAIL.

## MERGE Subject with Asset

People and other non-Asset referents fail; future Asset semantics become overloaded.

**Result:** FAIL.

## MERGE Subject with Account/Principal

Caregiver/external-person scenarios and non-account referents fail.

**Result:** FAIL.

## MAKE UNIVERSAL SUPERCLASS

Every eligible referent must inherit from a role merely to be referenced; duplicate lifecycle/persistence abstractions appear.

**Result:** FAIL.

## Subject as contextual role over native identity

Preserves aboutness without duplicate identity and composes with Person/Asset/Resource/Actor distinctions.

**Result:** PASS.

---

# 21. Core invariants

1. **Subject is a contextual semantic role, not an independent domain entity.**
2. **Subject role answers who/what a descriptive record is primarily about.**
3. **The native referent retains its own identity; no parallel Subject identity is created.**
4. **Eligible Subject referents do not require one universal inheritance root/table.**
5. **Subject != Person, although Person may play Subject role.**
6. **Subject != Actor, although one Person may play both roles in different relations.**
7. **Subject != Resource and Subject != Asset.**
8. **Subject != Account/Principal.**
9. **Subject != observer != recorder != source/provider/device != transformer != confirmer != authority != viewer.**
10. **Being Subject does not imply ownership, responsibility, participation, consent, authority, visibility, or benefit.**
11. **Current account holder is not the universal default Subject at kernel level.**
12. **Unknown Subject must not be replaced with invented certainty.**
13. **Later Subject resolution/correction preserves material attribution history.**
14. **Subject must not become a universal `related_to` catch-all; focus/context/participant/source/etc. remain distinct where semantically necessary.**
15. **Subject identity/account independence is mandatory for multi-actor and external-participant correctness.**
16. **Subject association does not create disclosure permission.**
17. **AI may propose Subject resolution but does not automatically establish identity or authority.**
18. **Subject semantics do not imply a universal SQL `subjects` table.**

---

# 22. Persistence/API implications — deliberately not physical design

Future logical modeling must support typed references from descriptive records to eligible native referents without forcing all referents into one semantic super-entity.

It should be able to represent where needed:

- one or more Subject-role references;
- unresolved/unknown Subject where valid;
- later correction/resolution with history;
- distinction among Subject, observer, recorder, source, performer, confirmer, authority and viewer;
- references to non-account people and non-person referents;
- privacy/visibility rules independent of subject identity.

Do not infer from Subject v0 that LifeOS requires:

- a universal `subjects` table;
- one `subject_id` foreign key to a generic wrapper entity;
- every domain entity inheriting from Subject;
- Subject owning Observation lifecycle;
- Subject defining permissions/ACLs;
- Subject implying account identity.

Final reference mechanics depend on the Person/Actor/Asset/Resource and Relationships reviews plus logical data-model pressure.

---

# 23. Adjacent Dependency Sweep

## RESOLVED NOW

### Subject vs observer / recorder / source / transformer

Resolved as distinct contextual roles. Subject concerns aboutness; Provenance/actor roles concern origin/action.

Re-test if the future relationship model proposes one generic role that would erase these distinctions.

### Subject entity vs semantic role

Resolved: semantic role survives; independent Subject entity/universal root is rejected.

### Subject vs current Account

Resolved at the basic boundary: current account holder does not define Subject identity.

## SAFE DEFERRED

### Subject vs Person / Actor

**Owner:** immediate Person / Actor boundary review.  
**Why safe:** Subject can already reference native referent identity without deciding final Person/Actor implementation.  
**Reopening trigger:** Person/Actor review concludes that one accepted identity abstraction cannot express passive/non-account subjects or acting-role separation.  
**Tests to rerun:** CORE-04, CORE-06, MA-01, MA-09, MA-10, XCON-01, XCON-05.

### Subject vs Asset

**Owner:** Asset candidate review in this cluster.  
**Why safe:** Subject only requires native referent identity; Asset eligibility does not determine Subject semantics.  
**Reopening trigger:** Asset review proposes a universal managed-object identity that would subsume or conflict with Subject-role semantics.  
**Tests to rerun:** CORE-04, CORE-06, XCON-01, XCON-04.

### Subject vs Resource

**Owner:** Resource candidate review in this cluster.  
**Why safe:** aboutness and resource/capacity roles are already independently meaningful.  
**Reopening trigger:** Resource review claims every eligible Subject must be Resource or introduces conflicting generic identity.  
**Tests to rerun:** CORE-04, MA-14, XCON-01.

### Subject vs Account / Principal / Authority / Visibility

**Owner:** Person/Actor review for Account boundary, then Relationships / Reasoning for Principal/Authority/Visibility.  
**Why safe:** Subject v0 explicitly creates no account, authority or visibility semantics.  
**Reopening trigger:** later authority/access design requires Subject itself to own rights or identity.  
**Tests to rerun:** MA-01, MA-06, MA-07, MA-08, MA-13, MA-17, XCON-02, XCON-05.

### Subject vs focus/context generic relationship semantics

**Owner:** Relationships / Reasoning.  
**Why safe:** Subject has a bounded primary-aboutness meaning and explicitly does not absorb other contextual roles.  
**Reopening trigger:** ordinary scenarios cannot distinguish primary Subject from focus/context without introducing a more general accepted relation that changes Subject semantics.  
**Tests to rerun:** CORE-04, CORE-05, XCON-04.

No current dependency is a structural blocker to accepting Subject as a semantic role.

---

# 24. Rejected alternatives

Rejected:

- universal Subject entity/root;
- `Subject` wrapper around every Person/Asset/etc.;
- Subject = current user/account;
- Subject = Person;
- Subject = Actor;
- Subject = Asset;
- Subject = Resource;
- Subject = owner/governor;
- Subject = generic `related_to`;
- account/provider ID as Subject identity;
- automatic Subject establishment by AI inference.

---

# 25. Reopening triggers

Reopen Subject v0 if later evidence shows that:

1. a universal native identity concept can replace Subject-role semantics without losing aboutness distinction;
2. Person/Actor/Asset/Resource modeling cannot reference native subjects without duplicate identity;
3. ordinary descriptive records require materially different subject/focus semantics that invalidate the current primary-aboutness definition;
4. multi-subject records cannot be expressed without a new first-class identity/lifecycle concept;
5. privacy/authority requires materially different Subject semantics rather than separate policy relationships;
6. logical persistence cannot support heterogeneous Subject references without unacceptable correctness or query cost and a different semantic model solves that problem more cleanly;
7. AI/import reconciliation exposes a contradiction between native identity and Subject attribution history.

Until stronger evidence appears, Subject remains canonical **semantic role / relationship capability**, not an entity.