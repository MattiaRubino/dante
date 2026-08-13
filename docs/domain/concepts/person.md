# Person v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Current revision:** 2026-08-12 — Resource-role boundary resolved  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **A Person is a persistent native representation of a human individual in LifeOS reality whose identity is independent of Accounts, credentials, contact/profile representations, participation, Subject roles, Actor roles, Resource roles, responsibility, authority, visibility, and current access to LifeOS.**

Person answers the identity question:

> **Which human individual is this?**

A Person is a **canonical native entity**. It is not a role and is not defined by whether the human currently uses LifeOS.

Typical examples:

```text
Person Maria
- may have no LifeOS Account
- may be Subject of Observations
- may later become a participant/performer/recorder
- may later play Resource role in scheduling
- may later obtain or lose Account access
```

```text
Person Anna
- same human before, during, and after an Account lifecycle
- may have several external contact/profile representations
```

---

# 1. Why Person exists

LifeOS must represent human identity independently of digital participation.

Ordinary scenarios include:

- a caregiver records information about an older adult who has no LifeOS Account;
- a parent manages activities concerning a child;
- an Event references an external person who never joins LifeOS;
- a contact later creates an Account;
- a person changes email/login provider;
- an Account is disabled or deleted while historical attribution must remain intelligible;
- several imported contact/profile representations may concern the same real human.

Without Person, LifeOS would be pushed toward weak alternatives:

1. equate humans with `users.id` or Account rows;
2. create synthetic Accounts for non-users;
3. make Subject/Actor/Resource roles carry identity they do not own;
4. lose historical identity when credentials or access change;
5. duplicate one human across caregiver, calendar, contact, provenance, participation and authority contexts.

Canonical rule:

> **Digital access is something a Person may obtain; it is not what makes the Person exist in the domain.**

---

# 2. Person identity is native and persistent

Person has its own native domain identity.

That identity is not derived from mutable attributes such as:

```text
name
email
phone number
username
provider subject identifier
Account ID
contact ID
```

Two people may share names. Email/phone values may change or be reassigned. External providers may expose different identifiers for the same human or similar identifiers in different scopes.

Therefore:

> **Person identity must not be a hash of current identifying attributes or a foreign-provider identifier.**

The logical identity/reconciliation mechanism is deferred, but the semantic requirement is fixed.

---

# 3. Person versus Account

Account concerns LifeOS access/membership/authentication lifecycle.

Person concerns the represented human.

```text
Person Maria
    ├─ no Account in 2026
    ├─ Account A1 in 2028
    └─ Account later disabled
```

The Person remains the same human throughout.

Canonical boundaries:

```text
Person != Account
Person identity != Account identity
Account deletion != automatic Person deletion
Account creation != Person creation when the human was already represented
```

A product policy may later restrict active Account cardinality, but such a policy does not redefine Person identity.

Exact Account/credential/auth-provider semantics belong to the identity/security logical model.

---

# 4. Person versus Subject

Subject is accepted contextual aboutness semantics.

A Person may play Subject role when a descriptive record is about that human:

```text
Person Maria
    ↑ Subject role
Observation: temperature = 38.2 °C
```

But Person identity exists independently of any such record.

Therefore:

```text
Person != Subject
Person may play Subject role
```

Being Subject does not imply that the Person created, observed, confirmed, owns, can view, or authorized the record.

---

# 5. Person versus Actor

Actor is accepted agency semantics: the contextual role/capability of a native referent or system when an action is attributed to it.

A Person may play Actor role:

```text
Person Anna
    ↓ Actor role
recorded Observation O7
```

But Person and Actor are not the same concept.

Examples:

- an infant is a Person but may not be an Actor in a given workflow;
- a deceased Person remains a Person while having no current agency;
- a software integration may be an Actor but is not a Person.

Therefore:

```text
Person != Actor
Person may play Actor role
Actor need not be Person
```

---

# 6. Person versus Resource

Resource v0 is accepted as contextual planning/execution eligibility and capacity semantics, not an entity/root.

A Person may play Resource role when that human can satisfy an execution requirement.

Example:

```text
Requirement
Japanese B2+

Candidates
Person Anna
Person Luca
```

or:

```text
Person Anna
Availability Mon-Fri 09:00-18:00
Capacity one consultation at a time
```

Person identity remains Anna regardless of whether she is currently considered a Resource.

When a more precise relationship exists, use it:

```text
expected performer = Anna
participant = Anna
responsible person = Anna
```

rather than reducing the human to a generic Resource relation.

Therefore:

```text
Person != Resource
Person may play Resource role
Resource != Performer
Resource != Participant
Resource != Responsibility
```

The Person/Resource boundary is **RESOLVED** by `concepts/resource.md` and its validation checkpoint.

---

# 7. Person versus User

`User` is useful product/implementation language but is not accepted as a separate domain primitive.

Depending on UI/technical context, `user` may mean:

- current Account holder;
- person using the application;
- authenticated principal;
- actor making a request.

Those meanings must not be collapsed in the kernel.

Canonical rule:

> **Do not build domain identity around a universal `User` concept when the semantic question is Person, Account, Actor, Principal, Participant, Subject, Resource, or another explicit role.**

---

# 8. Person versus contact/profile/source representations

A Person may be represented by several external or product records:

```text
phone contact
email contact
calendar attendee
provider profile
imported directory entry
LifeOS Account profile
```

Those representations may provide evidence that records concern the same Person, but they do not automatically become Person identity.

Canonical guardrails:

- same email does not automatically prove same Person;
- same name does not automatically prove same Person;
- provider linking does not silently rewrite historical source representation;
- uncertain identity reconciliation may remain unresolved;
- merging two Person records is a high-impact identity decision and must preserve material history/provenance.

Exact reconciliation/merge/split semantics remain deferred to the logical model + Provenance/Version/Decision work.

---

# 9. Person versus participant / performer / responsibility

A Person may play many roles around domain objects:

```text
participant
performer
requester
responsible actor
observer
recorder
confirmer
owner/governor
beneficiary
Subject
Resource
```

None defines Person identity.

Canonical rule:

> **Human identity must remain stable while contextual roles can appear, change, expire, conflict, or never exist.**

The exact role relationships belong to later Relationships / Reasoning review.

---

# 10. Person versus authority and visibility

Representing a Person does not grant rights.

```text
Person Maria exists in LifeOS
```

does not imply:

```text
Maria has an Account
Maria can see records about herself
Maria can modify those records
another actor may view all records about Maria
Maria has authority over every record where she is Subject
Maria can allocate every Resource she is eligible to use
```

Authority, visibility, consent, guardianship, delegated access and policy remain separate semantics.

This separation is especially important for caregiver, child, workplace and adversarial contexts.

---

# 11. External/non-account Person is ordinary

A Person without an Account is not an incomplete user object.

Examples:

```text
family member
friend
doctor
teacher
client
child
older adult
interview contact
vendor contact
```

LifeOS may need to reference these people in Events, Activities, Provenance, Observations, responsibilities, Resource matching or relationships without requiring product onboarding.

Canonical rule:

> **No Account is required merely for a human to participate in LifeOS reality.**

---

# 12. Account lifecycle must not erase Person history

Example:

```text
2027 Anna records Observation O10
2028 Anna changes login provider
2030 Anna closes LifeOS Account
2031 O10 history is inspected
```

Historical attribution should still be capable of resolving to Person Anna where retention/privacy rules permit.

It must not degrade automatically to an opaque `deleted user` merely because an Account row no longer participates in authentication.

This does not pre-commit retention policy. Privacy/deletion rules may require anonymization or removal in specific contexts; those are explicit policies, not consequences of conflating Person with Account.

---

# 13. Person merge, split, and mistaken identity

Identity reconciliation is high risk.

Possible scenarios:

- duplicate Person records are later recognized as one human;
- two different humans were incorrectly merged;
- imported provider data changes its own identity mapping;
- AI proposes a match with uncertain confidence.

Canonical direction:

- Person merge/split must be explicit/reconcilable rather than silent field overwrite;
- material prior identity assertions and source mappings remain historically explainable;
- AI may propose identity matches but does not silently establish Person identity;
- Account linking alone does not authorize arbitrary Person merge.

Exact mechanics remain deferred.

---

# 14. Multi-actor implications

Person is necessary for a multi-actor-ready kernel because shared reality frequently includes humans who are not Account holders.

Core patterns:

```text
Person B is Subject
Person A acts as recorder
Account A authenticates access
```

or:

```text
Person C participates in Event
but has no LifeOS Account
```

or:

```text
Person D
candidate Resource for shared responsibility
no Account required merely to be represented
```

The model must not create duplicate per-user Person identities for the same shared human merely because several Account holders refer to them.

At the same time, identity resolution itself can be privacy-sensitive and must not reveal private cross-context linkage without authority.

---

# 15. Privacy and identity linkage

Knowing that two records concern the same Person can itself be sensitive.

Therefore:

- Person identity does not imply universal cross-context visibility;
- an actor may be able to reference a Person in one context without seeing all data attached elsewhere;
- contact/profile merging must not become an inference-privacy bypass;
- Resource matching based on private capability/availability does not grant disclosure permission;
- AI/context building must respect visibility before exploiting identity linkage;
- current access and historical attribution remain different concerns.

Exact policy belongs to Visibility/Authority/privacy review.

---

# 16. AI boundary

AI may:

- suggest likely duplicate Person representations;
- propose that an imported contact maps to an existing Person;
- use established Person identity to organize authorized context;
- flag suspicious identity conflicts;
- propose a Person as a Resource candidate when an authorized requirement/capability match exists.

AI must not silently:

- create a Person merge solely from probabilistic similarity;
- equate Account/credential/provider IDs with the human;
- disclose private cross-context identity linkage;
- reinterpret historical attribution after a later match without provenance;
- treat Resource candidacy as Responsibility, consent or allocation Authority.

Canonical rule:

> **AI can propose identity reconciliation and resource matching; it does not automatically establish human identity, responsibility, consent, allocation, or authority.**

---

# 17. Simple UI versus kernel semantics

Most personal flows should not expose identity architecture.

UI may show:

```text
Maria
Anna
Dr. Rossi
```

rather than `Person P17`.

Ordinary self-use may implicitly resolve `me` to the current Person linked to the active Account, while the kernel preserves the distinction.

Planning UI may ask `Who's available?` or show natural role labels rather than `Resource Person`.

Power-user/admin/history surfaces may expose source/contact/account linkage only when useful and authorized.

---

# 18. External benchmark synthesis

External patterns are evidence only.

Useful lessons observed across mature identity/contact/health systems include:

- a real human can be represented independently from a service account;
- provider/credential identifiers may be scoped and mutable rather than global human identity;
- multiple source/profile/contact representations may concern one human;
- identity linking requires reconciliation rather than blind equality on one attribute.

Resource/booking systems additionally reinforce that people can participate in scheduling/allocation while retaining Person/staff identity rather than requiring a universal Resource identity.

LifeOS adapts those lessons without importing external user/account/resource taxonomies wholesale.

---

# 19. Adversarial reductio summary

## REMOVE Person

Caregiver, external-participant, Account-change and historical-attribution scenarios are forced into Account/contact/role identity.

**Result:** FAIL.

## MERGE Person with Account

Non-account humans and account lifecycle break identity continuity.

**Result:** FAIL.

## MERGE Person with Subject

Human identity would exist only when something is about that human; non-human subjects still require another structure.

**Result:** FAIL.

## MERGE Person with Actor

Passive humans and non-human/software actors break the model.

**Result:** FAIL.

## MERGE Person with Resource

Human identity would depend on operational eligibility; non-human Resources still require other identities.

**Result:** FAIL.

## MAKE User the universal root

Product/auth vocabulary would absorb domain identity, agency and access semantics.

**Result:** FAIL.

## Person as native human identity

Preserves one human across digital access, contextual roles and history.

**Result:** PASS.

---

# 20. Core invariants

1. **Person is a native persistent human-identity entity.**
2. **Person identity is independent of Account, credentials, provider identifiers, contacts and profiles.**
3. **Person != Subject; a Person may play Subject role.**
4. **Person != Actor; a Person may play Actor role.**
5. **Person != Resource; a Person may play Resource role.**
6. **Resource role does not replace Performer/Participant/Responsibility semantics.**
7. **Person != Account/Principal/User.**
8. **No Account is required for a Person to exist in LifeOS reality.**
9. **Account creation/deletion does not automatically create/delete the represented Person.**
10. **Contextual participation/responsibility/resource role/authority/visibility does not define Person identity.**
11. **External identifiers are reconciliation evidence, not canonical Person identity by default.**
12. **Person merge/split/correction must preserve materially relevant identity history.**
13. **AI identity matching is proposal/inference until established by appropriate policy/authority.**
14. **Person identity linkage itself is subject to privacy/visibility policy.**

---

# 21. Persistence/API implications — deliberately not physical design

Future logical modeling must support:

- stable Person identity;
- zero or more Account/access representations over time where policy permits;
- external/contact/profile identity mappings with Provenance;
- native references from Subject/Actor/Participant/Resource/etc. roles;
- identity reconciliation/correction history;
- privacy/visibility controls over cross-context identity linkage.

Do not infer from Person v0 that LifeOS requires:

- one universal polymorphic `party` table;
- `persons.id = accounts.id`;
- synthetic Accounts for external people;
- automatic Person merge by email/name/phone;
- one visible Person object in every UI;
- a Resource wrapper/entity around schedulable people;
- final Account/credential schema now.

---

# 22. Deliberately deferred questions

- exact Account/auth-provider/credential lifecycle;
- Principal/security identity model;
- Person merge/split/reconciliation mechanics;
- contact/address book/profile representations;
- Organization/native non-human actor identity;
- Participation/Responsibility/Authority/Visibility relationships;
- Resource Requirement/Allocation/Reservation mechanics;
- consent/guardian/legal-representative semantics;
- deletion/anonymization/retention policy;
- shared Person deduplication/privacy rules;
- logical/physical typed-reference model.

These are dependencies, not reasons to collapse Person into Account, Actor or Resource.

---

# 23. Reopening triggers

Reopen Person v0 if later evidence shows that:

1. a smaller accepted identity concept can represent non-account humans and Account lifecycle without semantic loss;
2. Person identity cannot compose with Subject/Actor/Resource roles without duplicate truth;
3. privacy requirements make shared native Person identity structurally invalid rather than merely access-controlled;
4. logical persistence pressure proves native Person identity unworkable without an alternative that preserves all invariants;
5. identity reconciliation requires materially different domain semantics rather than additional relationship/history mechanics;
6. Resource/Responsibility/Participation modeling requires human identity to be represented differently rather than by contextual roles over Person.

Until then, Person remains the current accepted native human-identity concept.

---

# 2026-08-13 — Representation / on-behalf-of downstream closure

Representation v0 closes the generic Person-versus-representative boundary while preserving Person as native human identity.

Canonical separation:

```text
Person
= persistent human identity

Actor
= actual contextual semantic agent

Representation / on-behalf-of
= actual Actor acts for a distinct represented party in a bounded action/context

Principal
= technical security identity
```

Therefore:

```text
Person != Representative role
represented Person != actual Actor automatically
represented Person != Principal
represented Person requires no Account
Representation != Subject/beneficiary
```

The existence of a parent, caregiver, guardian, assistant, manager or household relationship does not by itself prove that the Person is being represented for every action or that the representative expresses the Person's personal will.

The older `consent/guardian/legal-representative semantics` deferral is now split:

- generic Representation/on-behalf-of semantic relation: **RESOLVED**;
- legal capacity, guardianship, power-of-attorney and specialist representation validity: **SAFE DEFERRED** to specialist/legal/product policy;
- Principal/AuthN/AuthZ mechanics and physical typed-reference model: **SAFE DEFERRED** to security/logical design.

No Person invariant is reopened. **Person remains the canonical native human-identity entity, REOPEN = 0.**

Normative downstream references:

- `representation.md`;
- `../checkpoints/representation-delegation-principal-v0-validation.md`.
