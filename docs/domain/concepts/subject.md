# Subject v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Current revision:** 2026-08-12 — Person / Actor / Account / Asset / Resource boundaries aligned  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **Subject is the contextual semantic role played by a native referent when a descriptive record primarily concerns that referent's state, property, condition, or asserted fact. Subject does not create independent identity: the referenced Person, Asset, Event, Device, Location, or other eligible referent retains its native identity. Being the Subject does not imply authorship, observation, recording, ownership, responsibility, authority, visibility, participation, Resource eligibility, or account identity.**

Subject answers the bounded contextual question:

> **Who or what is this descriptive record primarily about?**

Typical shapes:

```text
Person Mattia
    ↑ subject-of
Observation: body weight = 66.4 kg
```

```text
Asset Car A17
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

LifeOS needs to distinguish what a descriptive fact concerns from who created, observed, recorded, performed, confirmed, owns, governs, may use as a Resource, or may see that fact.

Examples:

```text
subject = older adult
observer = caregiver
recorder = caregiver
device = thermometer
Observation = temperature 38.2 °C
```

```text
subject = car Asset
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

The same rule applies to an Asset:

```text
Asset A17
camera

Observation O43
subject -> Asset A17
property = shutter count
value = 32,411
```

Rejected shape:

```text
Subject S9
    ↓ wraps
Person P17 / Asset A17
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

The current Asset v0 scope is itself explicitly reopenable through a terminology-neutral Cluster-4 re-review. A future Asset boundary change does not automatically change Subject semantics; it triggers a compatibility re-test instead.

---

# 4. Subject versus Person

Person is accepted as the native human-identity entity.

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

The same Person identity can play several roles simultaneously and may exist before, without, or after any LifeOS Account.

Therefore:

```text
Person != Subject
Person may play Subject role
Person identity != Account identity
```

The basic Person/Subject identity boundary is **RESOLVED** by `person.md` and `checkpoints/person-actor-account-v0-validation.md`.

---

# 5. Subject versus Actor

Actor is accepted as **contextual semantic agency**, not an entity/root.

Subject concerns aboutness and does not require agency.

Examples:

- an infant can be a Subject without acting in the workflow;
- a non-LifeOS person can be a Subject;
- an Asset can be a Subject without acting;
- a room can be a Subject;
- an animal can be a Subject;
- a software/AI system may be an Actor without being a Person or ordinary Subject.

Therefore:

```text
Subject != Actor
Actor != Person
Actor != Account
```

A Person may play both Subject and Actor roles in different relations:

```text
Person Anna
subject of Observation X
recorder / Actor of Observation Y
performer / Actor of Activity Z
```

Actor does not by itself imply Responsibility, Authority, ownership or one generic action role.

The basic Subject/Actor boundary is **RESOLVED** by `actor.md` and the Person / Actor / Account checkpoint.

---

# 6. Subject versus Account / Principal

Account is fixed conceptually as a platform/access identity distinct from Person and Actor. Principal remains a deferred security/authorization identity concept.

Subject concerns what a descriptive record is about.

Caregiver example:

```text
Person Anna
Actor role: recorder
Account Anna-A1 authenticates access

Observation
subject = Person Maria
```

Maria may have no LifeOS Account.

Canonical rules:

```text
Subject != Account
Subject != Principal
Person != Account
Actor != Account
current account holder != default subject as a kernel invariant
```

Product UI may default ordinary personal entry to `me`, but that is a contextual convenience rather than canonical identity semantics.

The Subject/Account identity boundary is **RESOLVED at conceptual level**. Exact Account/Principal/credential mechanics remain deferred to the security/logical stage.

---

# 7. Subject versus observer, recorder, source and Provenance roles

Observation distinguishes several roles that often coincide in simple personal use but diverge in real workflows.

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

Where a Person or system performs one of those roles, Actor semantics may apply, but the specific role remains more precise than a generic Actor relation.

A subject may also be a source/Actor in a self-report, but that coincidence must be represented by roles rather than assumed universally.

---

# 8. Subject versus Resource

Resource v0 is accepted as a **contextual planning/execution role/capability**, not an entity/root.

Subject answers:

> who/what is this descriptive record about?

Resource answers:

> what could satisfy this execution need?

One native referent can play both roles independently:

```text
Asset Car A17

Observation
subject = A17
odometer = 84,220 km

Trip Activity
Resource Requirement
transport with 4 seats

A17
candidate / selected Resource role
```

Likewise a Person can be Subject in one context and Resource candidate in another.

Therefore:

```text
Subject != Resource
Subject role does not imply Resource eligibility
Resource role does not imply Subject aboutness
```

The basic Subject/Resource boundary is **RESOLVED** by `concepts/resource.md` and `checkpoints/resource-v0-validation.md`.

---

# 9. Subject versus Asset

Asset v0 is accepted as the **current scoped native entity** for an individually tracked non-human physical object whose distinct identity and management history materially matter.

Subject remains a contextual role.

Example:

```text
Asset A17
Sony A7 IV
        ↑ Subject role
Observation
shutter count = 32,411
```

The Asset exists independently of the Observation and independently of playing Subject role.

Therefore:

```text
Subject != Asset
Asset may play Subject role
Asset identity != Subject role
```

Not every Subject is an Asset. A Person, room/location, Event, group, living subject or another eligible referent may be Subject without satisfying Asset v0 invariants.

Asset v0 also does **not** absorb every managed thing. Its current physical/durable boundary remains the validated scoped baseline; later boundary changes trigger compatibility re-test rather than redefining Subject.

The basic Subject/Asset boundary is **RESOLVED at the current Asset v0 baseline**.

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

```text
subject = Asset A17
```

does not establish who owns, holds, manages, allocates as Resource, or may see that Asset.

Canonical rule:

> **Aboutness must not launder ownership, authority, visibility, responsibility, participation, possession, custody, Resource eligibility, or consent.**

Authority v0 and Visibility v0 now make this boundary canonical rather than merely deferred.

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

or:

```text
subject -> Asset A17
```

The later association must not fabricate that the subject was known at ingestion time.

Canonical rules:

- unknown Subject may remain unknown where the record can meaningfully exist without a resolved referent;
- later subject resolution preserves materially relevant Provenance/history;
- account ownership/import destination does not prove subject identity;
- source/provider identity does not prove Subject identity;
- external identifiers may support Person/Asset reconciliation but do not automatically establish it.

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

The same applies to Asset attribution:

```text
Observation O10
subject = Asset A1

later correction
subject = Asset A2
```

This may be a correction to the same observation/assertion identity rather than a new measurement, provided the underlying observational act is the same and the correction only fixes attribution.

Material history should preserve the prior attribution and correction basis through Provenance/Version semantics.

Canonical guardrail:

> **Changing Subject attribution must not silently erase material prior attribution history or pretend the corrected referent was known earlier.**

Person or Asset merge/split/reconciliation must likewise preserve material attribution history rather than silently rewriting all old Subject links.

---

# 14. Multi-subject descriptive records

Some descriptive acts legitimately concern more than one referent.

Examples may include:

- a household-level Observation;
- a relationship-level rating;
- a group-level measurement;
- an environmental reading affecting a set of resources/people/assets.

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
Person Anna
Actor role: recorder
Account Anna-A1 authenticates access
Observation about Person Maria
```

```text
Person C
Actor/manager role
records assessment about Person D
```

```text
AI/system Actor
derives Observation about Asset A17
```

The domain must preserve who/what the record concerns separately from who entered, generated, transformed, confirmed, governed, authenticated, owns/holds/allocates the Asset, or may view it.

Key rules:

> **Subject identity must not depend on Account participation.**

> **Actor attribution and Account authentication must not replace Subject identity.**

> **Asset ownership/possession or Resource role must not replace Subject identity.**

Non-LifeOS subjects are ordinary domain reality, not exceptional placeholders.

---

# 16. Privacy and selective disclosure

Subject association itself can be sensitive.

Knowing that a private Observation is about Person X or Asset A17 may disclose information even if the value is hidden.

Visibility v0 closes this boundary with the following canonical rules:

- visibility of a record does not automatically imply visibility of every related Subject detail;
- visibility of a Person/Asset does not automatically imply visibility of all records about that referent;
- visibility of both endpoints does not imply visibility of the Subject association itself;
- Authority over one context does not grant universal Visibility into all records where the same referent is Subject;
- identity linkage between records/contacts/accounts/assets/providers may itself be private;
- Resource matching does not create Visibility into private Subject records;
- derived shared projections may conceal private source/Subject detail where policy requires;
- AI must not infer disclosure permission merely because it can resolve the Subject/referent internally.

Therefore:

```text
Subject != Visibility
being Subject != right to inspect record
record visible != every Subject linkage/detail visible
```

---

# 17. AI boundary

AI may:

- propose a Subject match from imported context;
- suggest that two records concern the same native Person/Asset/referent;
- use resolved Subject identity to organize/query authorized context;
- identify likely attribution errors.

AI must not silently:

- replace unknown Subject with the current account holder;
- merge two Person/Asset/native referents merely because names/identifiers/details look similar;
- promote a probabilistic Subject/identity match into established identity without policy/authority appropriate to the context;
- disclose private facts or identity linkage merely because it knows the Subject;
- infer Resource allocation/eligibility from Subject status alone;
- create a universal Subject object as a shortcut around native domain identity.

Canonical rule:

> **AI may propose subject or native-referent resolution; it does not automatically establish identity, Authority, ownership, Resource allocation, or disclosure rights.**

Authority v0 and Visibility v0 mean separately that AI needs a valid governance basis to establish a material attribution change and a valid exposure basis to disclose the attribution or its private source.

---

# 18. Simple UI versus kernel semantics

Most users should rarely see the noun `Subject`.

Personal default:

```text
Weight
66.4 kg
```

may imply `me` in the UI when the context safely establishes the current Person linked to the active Account.

Caregiver/asset context may expose natural labels:

```text
Maria
Temperature
38.2 °C
```

```text
Sony A7 IV
Shutter count
32,411
```

Power-user/history surfaces may expose attribution, Account/authentication context, Asset identity details and Provenance when relevant and authorized.

Canonical rule:

> **Kernel separation of Subject from Person/Account/Actor/Asset/Resource does not require every capture form to ask users to choose those ontology roles explicitly.**

---

# 19. External benchmark synthesis

External patterns were used as evidence, not design authorities.

Useful lessons retained:

- `subject` can point to native referents rather than require one universal Subject entity;
- subject and focus/context can differ;
- aboutness is distinct from performer/source/provenance roles;
- personal UX may often make the human subject implicit while the kernel preserves separation;
- Person identity is distinct from Account/contact/source representations;
- Actor is contextual agency, not a wrapper identity;
- Asset identity remains distinct from Subject role, Resource role, ownership and provider identifiers;
- heterogeneous native things may be operational Resources without sharing one native identity type.

No external schema is adopted wholesale.

---

# 20. Adversarial reductio summary

## REMOVE Subject entity

Native Person/Asset/etc. identities remain intact and descriptive records can reference them directly.

**Result:** PASS — independent Subject entity is unnecessary.

## REMOVE Subject semantics

LifeOS can no longer reliably answer who/what an Observation is about without overloading Account/owner/recorder/source.

**Result:** FAIL.

## MERGE Subject with Person

Non-human referents and passive/non-account cases fail.

**Result:** FAIL.

## MERGE Subject with Actor

Passive subjects, objects, locations, animals and non-agent referents fail.

**Result:** FAIL.

## MERGE Subject with Resource

Aboutness and planning/execution eligibility are independent.

**Result:** FAIL.

## MERGE Subject with Asset

People and other non-Asset referents fail; Asset lifecycle and Subject aboutness are distinct.

**Result:** FAIL.

## MERGE Subject with Account/Principal

Caregiver/external-person scenarios and non-account referents fail.

**Result:** FAIL.

## MAKE UNIVERSAL SUPERCLASS

Every eligible referent must inherit from a role merely to be referenced; duplicate lifecycle/persistence abstractions appear.

**Result:** FAIL.

## Subject as contextual role over native identity

Preserves aboutness without duplicate identity and composes with accepted Person/Actor/Account/Asset/Resource/Authority/Visibility distinctions.

**Result:** PASS.

---

# 21. Core invariants

1. **Subject is a contextual semantic role, not an independent domain entity.**
2. **Subject role answers who/what a descriptive record is primarily about.**
3. **The native referent retains its own identity; no parallel Subject identity is created.**
4. **Eligible Subject referents do not require one universal inheritance root/table.**
5. **Subject != Person, although Person may play Subject role.**
6. **Subject != Actor; Actor is contextual agency rather than identity.**
7. **Person != Actor and Person != Account.**
8. **Subject != Resource; Resource is contextual planning/execution eligibility/capacity.**
9. **Subject != Asset; accepted Asset v0 may play Subject role while retaining native identity.**
10. **Subject != Account/Principal.**
11. **Subject != observer != recorder != source/provider/device != transformer != confirmer != Authority != viewer.**
12. **Being Subject does not imply ownership, possession, responsibility, participation, Resource eligibility, consent, Authority, Visibility, or benefit.**
13. **Current Account holder is not the universal default Subject at kernel level.**
14. **Unknown Subject must not be replaced with invented certainty.**
15. **Later Subject resolution/correction preserves material attribution history.**
16. **Subject must not become a universal `related_to` catch-all; focus/context/participant/source/etc. remain distinct where semantically necessary.**
17. **Subject identity/Account independence is mandatory for multi-actor and external-participant correctness.**
18. **Subject association and native identity linkage do not create disclosure permission.**
19. **AI may propose Subject/native-referent resolution but does not automatically establish identity or Authority.**
20. **Subject semantics do not imply a universal SQL `subjects` table.**
21. **A future Asset scope change triggers compatibility re-test; it does not make Subject an Asset superclass.**
22. **Visible referent != visible Subject relation or all records about it.**

---

# 22. Persistence/API implications — deliberately not physical design

Future logical modeling must support typed references from descriptive records to eligible native referents without forcing all referents into one semantic super-entity.

It should be able to represent where needed:

- native Person identity as an eligible Subject referent;
- current Asset v0 identity as an eligible Subject referent;
- other eligible native referents established by later reviews;
- one or more Subject-role references;
- unresolved/unknown Subject where valid;
- later correction/resolution with history;
- distinction among Subject, Resource, Actor-specific roles, observer, recorder, source, performer, confirmer, Authority and viewer;
- references to non-account people and non-person referents;
- Account/authentication context independently from Subject identity;
- Asset ownership/possession/provider identifiers independently from Subject identity;
- privacy/Visibility rules independently from referent identity.

Do not infer from Subject v0 that LifeOS requires:

- a universal `subjects` table;
- one `subject_id` foreign key to a generic wrapper entity;
- every domain entity inheriting from Subject;
- Subject owning Observation lifecycle;
- Subject defining permissions/ACLs;
- Subject implying Account, Asset or Resource identity;
- `persons.id = accounts.id`;
- an `actors` table;
- a `resources` table;
- every Subject becoming an Asset or Resource.

Final heterogeneous reference mechanics depend on later logical data-model pressure. The basic Person/Actor/Account/Subject/Asset/Resource/Authority/Visibility boundaries are resolved conceptually at the current baseline.

---

# 23. Adjacent Dependency Sweep

## RESOLVED NOW

### Subject vs observer / recorder / source / transformer

Resolved as distinct contextual roles. Subject concerns aboutness; Provenance/Actor roles concern origin/action.

### Subject entity vs semantic role

Resolved: semantic role survives; independent Subject entity/universal root is rejected.

### Subject vs Person

Resolved: Person is a native human entity that may play Subject role; Subject does not create or own Person identity.

### Subject vs Actor

Resolved: Actor is contextual agency over native identity; Subject is aboutness. Neither absorbs the other.

### Subject vs Account

Resolved at conceptual level: Account is platform/access identity and does not define Subject or Person identity.

### Subject vs Asset

Resolved at the current Asset v0 baseline: Asset is native physical-object identity and may play Subject role; Subject remains aboutness.

### Subject vs Resource

Resolved: Subject is descriptive aboutness; Resource is contextual planning/execution eligibility/capacity. The same native referent may play either or both roles independently.

### Subject vs Authority

Resolved: aboutness does not create governance power; Authority is separately scoped to effects/targets/basis.

### Subject vs Visibility

Resolved: aboutness does not grant exposure. Subject association itself may have Visibility distinct from both record and referent endpoints.

## SAFE DEFERRED

### Subject vs Principal / technical enforcement

**Owner:** security/logical model.  
**Why safe:** Subject creates neither security identity nor technical permission; Authority/Visibility are already separate semantic capabilities.  
**Reopening trigger:** later enforcement requires Subject itself to own security identity/rights.  
**Tests to rerun:** MA-06, MA-07, MA-08, MA-13, MA-17, XCON-02, XCON-05.

### Subject vs focus/context generic relationship semantics

**Owner:** Relationships / Reasoning.  
**Why safe:** Subject has a bounded primary-aboutness meaning and explicitly does not absorb other contextual roles.  
**Reopening trigger:** ordinary scenarios cannot distinguish primary Subject from focus/context without a more general relation that changes Subject semantics.  
**Tests to rerun:** CORE-04, CORE-05, XCON-04.

### Person / Asset identity reconciliation / merge / split

**Owner:** logical data model + Provenance/Version/Decision.  
**Why safe:** Subject references established native identity; reconciliation mechanics do not change aboutness semantics.  
**Reopening trigger:** identity reconciliation cannot preserve historical Subject attribution under accepted native-identity models.  
**Tests to rerun:** CORE-02, CORE-09, XCON-01, XCON-03.

No current dependency is a structural blocker to Subject v0.

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
- Subject = Visibility;
- Subject = generic `related_to`;
- Account/provider ID as Subject identity;
- automatic Subject establishment by AI inference.

---

# 25. Reopening triggers

Reopen Subject v0 if later evidence shows that:

1. a universal native identity concept can replace Subject-role semantics without losing aboutness distinction;
2. Person/Actor/Asset/Resource modeling cannot reference native subjects without duplicate identity;
3. ordinary descriptive records require materially different subject/focus semantics that invalidate the current primary-aboutness definition;
4. multi-subject records cannot be expressed without a new first-class identity/lifecycle concept;
5. privacy/Authority requires materially different Subject semantics rather than separate policy relationships;
6. logical persistence cannot support heterogeneous Subject references without acceptable correctness/query behavior and another semantic model is stronger;
7. AI/import reconciliation exposes a contradiction between native identity and Subject attribution history;
8. a broader native-referent abstraction materially changes the current Subject/Asset boundary;
9. Resource Requirement/Allocation modeling requires a common identity abstraction that materially changes Subject/Resource separation.

Until stronger evidence appears, Subject remains canonical **semantic role / relationship capability**, not an entity.
