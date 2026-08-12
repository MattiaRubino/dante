# Resource v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Current revision:** 2026-08-12 — Cluster-4 integration and Cross-Cluster v4 hardening  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Data / Subjects cluster

## Canonical definition

> **Resource is the contextual planning/execution role through which a native referent, service, pool, supply, or other eligible capability-bearing thing is considered able to satisfy an execution requirement by providing usable availability, capacity, access, capability, or consumable supply. Resource does not create independent identity: the provider retains whatever native identity, value, pool, supply, service, or other semantics it independently has.**

Resource answers the bounded operational question:

> **What could provide what this execution context needs?**

Resource therefore represents **canonical semantic role / planning-and-execution capability**, not an independently persistent universal entity/root.

Typical shapes:

```text
Asset A17
Sony A7 IV
        ↓ Resource role
Photo shoot
```

```text
Person Anna
        ↓ Resource role in scheduling context
Consultation
```

```text
Room 3
        ↓ Resource role
Workshop
```

The same underlying provider may exist outside any Resource role and may play other roles simultaneously. A supply or pool does not need individual domain identity merely because it can satisfy a Requirement.

---

# 1. Why Resource semantics exist

LifeOS scheduling and execution already require a way to reason about whether something can satisfy an operational need.

Examples include:

- a Person whose time/capability is required;
- a camera, car, laptop, tool, or other Asset needed for an Activity;
- a room or place whose capacity constrains an Event;
- a service capable of satisfying a requirement;
- a pool of interchangeable capacity;
- a consumable supply required by execution;
- specialist capacity that may be allocated or reserved.

Without Resource semantics LifeOS would be pushed toward weak alternatives:

1. make Asset the universal execution-supply concept;
2. make Person the implicit universal schedulable object;
3. hard-code a separate planning system for rooms/equipment/services;
4. treat every useful thing as a generic entity called Resource;
5. collapse requirement, selection, reservation, availability and consumption into one field.

The required semantic is therefore real even though an independent Resource identity is not.

---

# 2. Resource is a role, not a native identity

A camera does not become a second object merely because it is required by an Activity.

```text
Asset A17
Sony A7 IV
```

may play Resource role in:

```text
Activity: wildlife photo shoot
```

Rejected shape:

```text
Resource R55
    ↓ wraps
Asset A17
```

The wrapper would introduce duplicate identity, lifecycle and reconciliation without adding domain truth.

Canonical rule:

> **Resource-role assignment references or evaluates the provider's independently justified semantics; it does not manufacture parallel Resource identity.**

For a Person or Asset, those semantics include native identity. For a fungible supply, they may instead be Quantity/stock/supply semantics. For a pool or service, the future domain may or may not justify persistent identity independently of Resource role.

A physical implementation may later require typed references, candidate sets, capacity providers or allocation records. Those mechanisms do not justify a universal `resources` root/table by themselves.

---

# 3. Resource versus Requirement

This is a critical boundary for LifeOS planning.

```text
Activity
Photo shoot

Requirement
camera suitable for wildlife photography
```

does not yet identify which camera will be used.

Possible candidates:

```text
Asset A17 — Sony A7 IV
Asset A18 — Sony A1
Rental service option
```

Each may be eligible to play Resource role for this requirement.

Therefore:

```text
Resource Requirement
!= concrete selected Resource
```

A requirement may describe:

- capability;
- minimum quantity;
- compatibility;
- location;
- time-window availability;
- skill/qualification;
- capacity;
- quality;
- policy;
- another bounded eligibility criterion.

Exact Requirement semantics belong to Relationships / Reasoning and planning-model review.

Canonical guardrail:

> **Do not force a concrete resource identity merely because an intention has an operational need.**

---

# 4. Resource versus candidate, allocation, reservation and actual use

Resource planning contains several separable semantic moments:

```text
Requirement
what is needed
        ↓
Candidate set
what could satisfy it
        ↓
Allocation / selection
what is chosen
        ↓
Reservation / Capacity Claim
what capacity is held/committed
        ↓
Actual use / consumption
what was actually used
```

These may coincide in simple personal use, but they are not universally identical.

Example:

```text
Requirement
one suitable camera

Candidate
A17 or A18

Allocation
A17 chosen

Reservation
A17 held 17:00–20:00

Actual
A18 used after A17 failed
```

LifeOS must be able to preserve the change rather than rewriting history to pretend A18 was always selected.

Therefore:

```text
Resource != Requirement
Resource != candidate set
Resource != Allocation
Resource != Reservation / Capacity Claim
Resource != Actual use / consumption
```

---

# 5. Resource versus Asset

Asset v0 represents individually tracked non-human physical-object identity under the current scoped baseline.

Resource represents an operational role.

```text
Asset A17
Sony A7 IV
```

may exist when:

- stored;
- retired;
- lent;
- sold but retained historically;
- currently irrelevant to scheduling.

When considered for a photo shoot, the same Asset may play Resource role.

Therefore:

```text
Asset != Resource
Asset may play Resource role
```

Asset identity does not depend on current Resource eligibility or availability.

The terminology-neutral Asset re-review completed during Cluster-4 integration retained this boundary: a universal ManagedObject root was rejected and the current physical-object identity need survived.

---

# 6. Resource versus Person

Person is native persistent human identity.

Resource is an operational role that a Person may play in a planning/scheduling context.

```text
Person Anna
```

may have:

```text
Availability
Mon–Fri 09:00–18:00

Capacity
one consultation at a time
```

and therefore be schedulable as a Resource in that context.

However, when a more precise relation is known, LifeOS should prefer it.

Example:

```text
Activity
Perform inspection

expected performer = Anna
```

is semantically stronger than merely:

```text
resource = Anna
```

Therefore:

```text
Person != Resource
Resource != Performer
Resource != Participant
Resource != Responsibility
```

Canonical rule:

> **A Person may be resource-capable without being reduced to a Resource identity, and Resource role must not erase more precise human roles.**

This distinction is important both semantically and product-wise: ordinary LifeOS UI should not describe people generically as resources when a natural role such as performer, attendee, caregiver, coach or responsible person is clearer.

---

# 7. Resource versus Actor

Actor is contextual agency.

Resource is operational eligibility/capability to satisfy an execution need.

A machine can be Resource without agency.

A software agent can be Actor without being a scheduling Resource.

A Person may play both.

Therefore:

```text
Resource != Actor
```

Agency does not establish resource availability/capacity, and resource eligibility does not establish agency.

---

# 8. Resource versus Subject

Subject answers:

> who/what is this descriptive record about?

Resource answers:

> what could satisfy this execution need?

Example:

```text
Asset A17

Observation
subject = A17
shutter count = 32,411

Photo shoot
A17 plays Resource role
```

These are independent contextual roles.

Therefore:

```text
Subject != Resource
```

---

# 9. Resource and Availability / Capacity

Availability & Capacity v0 already established:

```text
Scheduling Capacity
= time-dependent ability of a schedulable resource to accept compatible commitments
```

Resource v0 now clarifies the referent/provider model behind that language.

A **schedulable Resource** is the subset of resource-role cases for which time-dependent capacity/availability matters.

Conceptually:

```text
native referent / service / pool / supply semantics
        ↓ Resource role
eligible to satisfy execution need
        ↓ when scheduling matters
Availability + Capacity
        ↓
Reservation / Capacity Claim
```

Canonical rules:

- not every Resource use requires calendar availability;
- not every eligible provider needs a persisted capacity profile;
- Availability/Capacity does not create Resource identity;
- Capacity is contextual and may have multiple dimensions;
- current free capacity is derived from rules, claims and compatibility rather than an intrinsic Resource status;
- Schedule placement does not imply capacity consumption.

---

# 10. Place / Room as Resource

A room or place may have native Place/Location semantics independent of scheduling.

Example:

```text
Room 3
capacity = 20 people
```

For a workshop it may play Resource role.

Therefore LifeOS should not conclude:

```text
Room = Resource entity
```

merely because rooms are bookable.

Exact Place/Location semantics remain deferred.

---

# 11. Service as Resource

Some execution needs may be satisfied by a service rather than a specific Person or Asset.

Example:

```text
Requirement
transport to airport

Candidates
own car
friend's car
rental car
ride-hailing service
```

The service may play Resource role as an operational option while retaining whatever future service/provider semantics are independently justified.

Resource v0 does not introduce a universal Service entity.

---

# 12. Skills and capabilities are not automatically Resources

Example:

```text
Requirement
Japanese B2+
```

`Japanese B2+` is a capability criterion, not an independently acting Resource identity.

Candidates may include Persons satisfying that capability.

Likewise:

```text
4K video capability
```

may constrain eligible equipment without itself becoming a Resource object.

Therefore:

```text
capability / qualification / skill
!= Resource identity
```

Exact capability/requirement representation remains deferred.

---

# 13. Pools and interchangeable capacity

Some workflows need resource supply without caring initially about a specific member.

Examples:

```text
3 equivalent meeting rooms
```

```text
10 identical rental bikes
```

```text
2 support agents from eligible pool
```

Do not force early member selection merely to satisfy one `resource_id` field.

A future logical model may represent, if justified:

- pool identity;
- eligibility set;
- quantity/capacity;
- late binding to a concrete member;
- substitution.

Resource v0 fixes only the semantic requirement that eligibility/capacity can exist before concrete allocation.

It does not pre-approve a universal Pool entity or require a pool identity where a quantity/candidate-set representation is sufficient.

---

# 14. Consumables and supplies

An execution context may require consumable supply.

Example:

```text
Recipe
requires 2 eggs
```

or:

```text
Maintenance
requires 500 ml oil
```

Resource semantics may be useful operationally because a supply can satisfy an execution requirement.

But this does not imply:

```text
each egg = Resource entity
```

or:

```text
500 ml oil = identity-bearing Resource
```

or:

```text
all inventory = Asset
```

The future inventory/supply model must preserve quantity, stock, movement and actual consumption semantics if those workflows become concrete.

Canonical rule:

> **Resource role may apply to consumable supply without manufacturing per-unit or per-quantity identity.**

---

# 15. Money and budget are not Resource by default

Natural language often calls money a resource.

LifeOS should not therefore make:

```text
Money = Resource
Budget = Resource
```

Budget is more naturally a financial constraint/capacity in its own domain.

Resource v0 is intentionally bounded to planning/execution supply/capability where the role improves allocation, scheduling or execution semantics.

If future financial planning reveals a stronger common abstraction, it must be validated explicitly rather than inherited from vocabulary.

---

# 16. Resource versus ownership, access and Authority

Being able to use something does not prove ownership.

```text
Resource = rented camera
```

may be usable without being owned.

Likewise ownership does not guarantee current access or authority to allocate:

```text
shared car
owner = A
current holder = B
booking authority = household policy
```

Therefore:

```text
Resource role != owner
Resource role != holder
Resource role != steward
Resource role != Authority
Resource role != Visibility
```

Exact access, ownership, custody, stewardship and Authority relations remain deferred to Relationships / Reasoning.

---

# 17. Resource compatibility is contextual

One object may be eligible for one requirement and ineligible for another.

```text
Camera A17
```

may satisfy:

```text
portrait shoot
```

but not:

```text
underwater shoot without housing
```

Similarly a Person may be available in time but lack the required qualification.

Therefore:

> **Resource eligibility is contextual; native identity or provider existence alone does not establish suitability.**

This implies that future planners must consider requirement/resource compatibility rather than treating availability as sufficient.

---

# 18. Resource substitution and late binding

Planning often changes which Resource is used without changing the underlying Activity/Event.

```text
Activity
Drive to airport

planned car = A17
car unavailable
replacement = rental service
```

The Activity identity remains stable if the intended action remains materially the same.

A replacement Resource should not silently rewrite earlier allocation/reservation history.

Canonical direction:

- candidate/resource substitution can preserve the execution subject;
- material allocation/reservation history should remain reconstructable;
- actual used Resource may differ from planned Resource;
- requirement satisfaction can remain unresolved until late binding where valid.

---

# 19. Resource and actual execution

Planned resource allocation is not proof of actual use.

```text
planned
Camera A17

actual
Camera A18
```

LifeOS must not rewrite planned data to match actual execution.

Where actual resource use matters, it belongs to execution/Actual/Session/Provenance or future typed relationship semantics rather than being inferred from reservation alone.

Canonical rule:

> **Reserved/allocated Resource != actually used Resource.**

---

# 20. Multi-actor implications

Resource v0 supports shared and independent actors without creating per-user duplicates.

Example:

```text
Asset A17
shared camera

Actor A
can allocate for project X

Actor B
can view availability but not private usage reason
```

One provider may support:

- shared canonical capacity facts;
- actor-scoped preferences;
- actor-specific access;
- separate allocation Authority;
- private source context.

Key rules:

- being Resource does not imply shared visibility;
- one Actor allocating a Resource does not automatically authorize another Actor;
- current reservation does not establish ownership;
- one Person's Resource eligibility does not imply responsibility or consent;
- external/non-LifeOS people/services may satisfy requirements without synthetic Accounts;
- actor-specific candidate ranking does not mutate shared Resource facts.

---

# 21. Privacy and selective disclosure

Availability and resource eligibility may reveal sensitive context.

Examples:

- a Person's availability;
- a device location;
- medical/care equipment usage;
- private home-room occupancy;
- why a Resource is unavailable.

Therefore LifeOS may expose:

```text
Unavailable 18:00–20:00
```

without exposing the private reason.

Canonical rules:

- Resource visibility != source-record visibility;
- free/busy projection != disclosure of underlying Event/Activity;
- candidate matching does not automatically reveal private qualifications/history;
- AI may reason over authorized context but must not use eligibility as disclosure permission.

---

# 22. AI boundary

AI may:

- infer candidate Resources from requirements;
- rank eligible candidates;
- suggest substitutions;
- detect capacity conflicts;
- propose reservations/allocations;
- explain why a candidate appears suitable where authorized.

AI must not silently:

- create Resource identity wrappers;
- convert probabilistic suitability into authoritative allocation;
- reserve shared capacity without the required authority;
- infer ownership or responsibility from Resource use;
- disclose private availability/reasons during optimization;
- rewrite planned allocation history to match actual use.

Canonical rule:

> **AI may propose resource matching and allocation; it does not inherit allocation Authority merely because it can optimize the plan.**

---

# 23. Simple UI versus kernel semantics

Most users should rarely see `Resource` as an ontology noun.

Examples:

```text
Need a camera
```

```text
Room
Conference Room 3
```

```text
Who's available?
Anna
```

```text
Equipment
Sony A7 IV
```

The UI should expose the natural domain object or action.

Advanced planning may expose:

- requirements;
- candidates;
- availability;
- allocations;
- substitutions;
- capacity conflicts.

Canonical rule:

> **Resource-role semantics may remain internal even when they materially improve planning.**

---

# 24. External benchmark synthesis

External systems were used as benchmark evidence, not design authority.

## Calendar / booking systems

Useful lessons:

- rooms/equipment can be bookable without proving that `Resource` should be their native ontology identity;
- people are often kept as staff/person objects while their availability is scheduled;
- capacity and reservation semantics are operational layers over underlying identities.

## Constraint/scheduling systems

Useful lesson:

- people, machines and other supplies can all be treated as resources in an optimization problem without requiring them to share one real-world identity type.

## Project-management systems

Useful lesson:

- some systems use `Resource` broadly for people, equipment, material and cost because it is useful for project allocation;
- that breadth is operational vocabulary, not evidence that LifeOS should make every such thing one kernel entity.

LifeOS adapts the common operational role while preserving stronger native identities and bounded provider/value/supply semantics.

---

# 25. Adversarial reductio summary

## REMOVE Resource entity

Person/Asset/Place/service/supply semantics remain intact and can be referenced directly in typed requirement/allocation semantics.

**Result:** PASS — independent Resource entity is unnecessary.

## REMOVE Resource semantics

Scheduling/allocation cannot express common eligibility/capacity across heterogeneous providers without domain-specific duplication.

**Result:** FAIL.

## Resource = Asset

People, rooms, services and supplies fail.

**Result:** FAIL.

## Resource = Person

Equipment/place/supply cases fail.

**Result:** FAIL.

## Resource = Subject

Aboutness and execution supply are independent.

**Result:** FAIL.

## Resource = Actor

Agency and operational eligibility are independent.

**Result:** FAIL.

## Resource = anything useful

The concept becomes semantically empty and absorbs money, information, Evidence, capabilities and arbitrary relations.

**Result:** FAIL.

## Resource as contextual planning/execution role

Preserves common allocation/capacity semantics without duplicate identity.

**Result:** PASS.

---

# 26. Core invariants

1. **Resource is a contextual semantic planning/execution role/capability, not an independent universal entity/root.**
2. **Resource does not manufacture identity; the provider retains whatever native identity, value, pool, supply, service, or other semantics it independently has.**
3. **Resource != Person, although Person may play Resource role.**
4. **Resource != Asset, although Asset may play Resource role.**
5. **Resource != Subject and Resource != Actor.**
6. **Resource != Requirement.**
7. **Resource != candidate set.**
8. **Resource != Allocation/selection.**
9. **Resource != Reservation/Capacity Claim.**
10. **Reserved/allocated Resource != proof of actual use/consumption.**
11. **Resource != Responsibility, Performer, Participant or Stewardship.**
12. **Resource role does not imply ownership, access, Authority or Visibility.**
13. **Availability does not by itself establish requirement compatibility.**
14. **Eligibility is contextual to the requirement.**
15. **A schedulable Resource is a Resource-role case whose time-dependent Capacity/Availability matters; not every Resource needs calendar semantics.**
16. **Consumable supply may satisfy Resource semantics without per-unit or per-quantity identity.**
17. **Money/Budget are not Resource by default.**
18. **Requirements may remain abstract before concrete allocation.**
19. **Resource substitution must not rewrite material planning/history.**
20. **AI optimization does not grant allocation Authority.**
21. **No universal `resources` table/root or one generic `resource_id` relation is pre-approved.**

---

# 27. Persistence/API implications — deliberately not physical design

Future logical modeling must support resource-role semantics without forcing all eligible things into one wrapper entity.

It should be able to express where justified:

- requirements separate from concrete candidates;
- candidate eligibility/compatibility;
- references to native Person/Asset/future Place/service identities where those identities exist;
- pool or quantity-based supply where needed without forced identity;
- allocation/selection history;
- Availability/Capacity for schedulable Resources;
- Capacity Reservations/Claims;
- substitutions;
- planned versus actual resource use;
- actor-scoped visibility/Authority;
- external-provider resource mappings without replacing native identity.

Do not infer from Resource v0 that LifeOS requires:

- `resources` universal table;
- `resource_id` on every schedulable object;
- Resource superclass inheritance;
- every Person or Asset always being Resource;
- a universal capacity unit;
- one generic requirement/allocation/reservation table before logical-model pressure;
- stock items becoming Assets/Resources individually;
- supplies/pools receiving synthetic identity solely for Resource role;
- money becoming Resource.

---

# 28. Adjacent Dependency Sweep

## RESOLVED NOW

### Resource vs Asset

**Resolution:** Asset is native identity under its current scoped baseline; Asset may play Resource role. The terminology-neutral Asset review completed during Cluster-4 integration retained this separation.

### Resource vs Person

**Resolution:** Person is native human identity; Person may play Resource role. More precise performer/responsibility semantics remain separate.

### Resource vs Subject

**Resolution:** Subject = aboutness; Resource = execution-supply eligibility.

### Resource vs Actor

**Resolution:** Actor = agency; Resource = execution-supply eligibility/capacity.

### Resource vs Availability / Capacity

**Resolution:** Availability/Capacity applies to schedulable Resource-role cases; Resource identity is not created by those capabilities.

## SAFE DEFERRED

### Resource Requirement

**Owner:** Relationships / Reasoning + planning semantics.  
**Why safe:** current Resource role only needs to distinguish provider from need; exact requirement object/relationship need not be fixed now.  
**Reopening trigger:** planner cannot represent abstract needs/late binding without changing Resource semantics.  
**Tests to rerun:** CORE-03, CORE-04, CORE-05, CORE-13, XCON-04.

### Allocation / Reservation / Claim

**Owner:** Relationships / Reasoning + scheduling logical model.  
**Why safe:** Resource role is independent of how a candidate is selected/held.  
**Reopening trigger:** allocation/reservation requires native Resource identity or conflicts with Availability/Capacity.  
**Tests to rerun:** CORE-02, CORE-04, MA-14, XCON-03, XCON-04.

### Consumable supply / inventory

**Owner:** future concrete inventory/supply workflow review.  
**Why safe:** Resource role can describe supply eligibility without approving stock ontology or identity.  
**Reopening trigger:** ordinary execution needs require quantity/movement/consumption semantics that cannot compose cleanly.  
**Tests to rerun:** CORE-03, CORE-04, CORE-10, CORE-12, CORE-13.

### Place / Location

**Owner:** future Place/Location review.  
**Why safe:** a Place may play Resource role without final Place ontology.  
**Reopening trigger:** room/location booking requires identity/capacity semantics inconsistent with current role model.  
**Tests to rerun:** CORE-04, MA-14, XCON-01, XCON-04.

### Service / capability / skill

**Owner:** Relationships / Reasoning / specialist planning.  
**Why safe:** Resource v0 distinguishes provider from capability criterion.  
**Reopening trigger:** capability/service workflows require a distinct native identity or common semantic not expressible under current model.  
**Tests to rerun:** CORE-03, CORE-04, CORE-06, CORE-12, XCON-01.

### Ownership / access / Authority / Visibility

**Owner:** Relationships / Reasoning.  
**Why safe:** Resource v0 explicitly grants none of these semantics.  
**Reopening trigger:** resource allocation rights cannot be represented without changing Resource identity/role.  
**Tests to rerun:** MA-06, MA-07, MA-13, MA-17, XCON-02.

No current dependency is a structural blocker.

---

# 29. Rejected alternatives

Rejected:

- universal Resource entity/root;
- Resource wrapper around Person/Asset/Place/service;
- Resource = Asset;
- Resource = Person;
- Resource = Subject;
- Resource = Actor;
- Resource = Requirement;
- Resource = Allocation;
- Resource = Reservation;
- Resource = Responsibility/Performer;
- Resource = anything useful;
- Money/Budget as Resource by default;
- early concrete resource selection for every requirement;
- automatic actual-use inference from planned allocation/reservation;
- universal `resource_id` implementation shortcut;
- synthetic identity for every supply/pool merely because it plays Resource role.

---

# 30. Cluster-4 integration hardening

Data / Subjects integration and Cross-Cluster Validation v4 confirmed Resource v0 with two explicit hardenings:

1. **Provider semantics are broader than native identity.** A Person/Asset/Place may bring native identity; a supply may bring Quantity/stock semantics; a pool/service may have its own future semantics only if independently justified. Resource role never creates identity.
2. **Planning stages remain reconstructable.** Requirement, candidate, allocation, reservation/claim, and actual use/consumption must remain distinguishable even when a simple workflow collapses them operationally.

Cluster-level result: **PASS WITH HARDENING; 0 structural reopenings**.

See:

- `checkpoints/data-subjects-v0.md`;
- `checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`;
- `checkpoints/cross-cluster-validation-v4.md`.

---

# 31. Reopening triggers

Reopen Resource v0 if later evidence shows that:

1. a native Resource identity with distinct lifecycle is required and cannot be represented by provider semantics plus Resource role;
2. Resource Requirement/Allocation/Reservation semantics cannot remain distinct without contradiction;
3. Availability/Capacity cannot attach coherently to heterogeneous providers without a stronger shared abstraction;
4. people/equipment/place/service/supply workflows require materially different meanings that make one Resource role misleading;
5. consumable/inventory workflows reveal that the current supply treatment loses history or quantity truth;
6. a stronger managed/capability-bearing referent abstraction emerges and survives the same reductio tests;
7. logical persistence pressure shows heterogeneous references are unacceptable and a different semantic model solves the problem more cleanly;
8. Authority/privacy constraints require Resource itself to own rights rather than separate policy relationships.

Until stronger evidence appears, Resource remains canonical **semantic planning/execution role/capability**, not an entity.