# Resource v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — accepted current baseline  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Data / Subjects  
**Branch:** `feature/domain-model`

## 1. Scope

- Candidate: Resource
- Candidate version: v0
- Adjacent concepts: Person, Actor, Subject, Asset, Availability, Capacity, Activity, Event, Schedule, Session, Actual, Responsibility, Participant, Performer, Requirement, Allocation, Reservation/Claim, Place/Location, service/capability, inventory/supply, Authority/Visibility
- Why this review exists: the Time cluster already depends on a concept of schedulable resource, but the domain had not decided whether Resource is native identity, entity/root, role/capability, or merely implementation vocabulary.

The review explicitly tests whether one Resource entity is needed at all.

---

# 2. Evidence reviewed

## Internal

Reviewed:

- Availability & Capacity v0;
- Activity/Event/Schedule/Session/Actual boundaries;
- Subject v0;
- Person / Actor / Account v0;
- Asset v0 and its mandatory terminology-neutral revisit;
- multi-actor readiness and responsibility/participation evidence;
- personal scheduling, equipment booking, room booking, service substitution, skills/qualification, pools, consumables and late-binding scenarios.

## External benchmark evidence

External standards/products were used as evidence only.

| Pattern | Useful lesson | Classification |
|---|---|---|
| Calendar/booking systems | rooms/equipment can be bookable while retaining room/place/device semantics | ADAPT |
| Staff booking systems | humans often remain staff/person identities while availability is scheduled | ADAPT |
| Optimization/scheduling systems | people, machines and supplies can be treated uniformly as resources inside a planning problem | ADAPT |
| Project-management resource models | `Resource` can be operationally broad, including work/material/cost categories | ADAPT WITH CAUTION |
| universal Resource superclass/entity | creates duplicate identity and encourages one generic `resource_id` relation | ANTI-PATTERN |
| requirement = selected resource | prevents late binding/substitution and loses planning history | ANTI-PATTERN |

The diversity of external meanings strengthens the conclusion that Resource is operational/contextual rather than a natural universal identity class.

---

# 3. Candidate definition

> **Resource is the contextual planning/execution role through which a native referent, service, pool, supply, or other eligible capability-bearing thing is considered able to satisfy an execution requirement by providing usable availability, capacity, access, capability, or consumable supply. Resource does not create independent identity: the underlying Person, Asset, Place, service, pool, supply, or other eligible referent retains its native semantics and identity.**

Classification: **CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY; NOT ENTITY / ROOT**.

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | Yes | resource exists before Activity? native Person/Asset does; role becomes relevant only in context | PASS | Resource role does not manufacture identity |
| CORE-02 Deep chronology | Yes | requirement → candidates → selection → reservation → substitution → actual use | PASS WITH HARDENING | preserve planning/actual distinction |
| CORE-03 Reductio | Yes | remove entity; remove semantics; merge with Person/Asset/Subject/Actor | PASS | entity rejected, semantic role survives |
| CORE-04 Redundancy | Yes | Resource vs Requirement/Allocation/Reservation/Performer | PASS WITH HARDENING | all kept distinct |
| CORE-05 Traceability | Yes | planned A17, reserved A17, actual A18 | PASS | history can reconstruct change |
| CORE-06 Orphan/independence | Yes | Asset/Person exists without Resource role; abstract requirement exists without selected Resource | PASS | role/context model confirmed |
| CORE-07 External benchmark | Yes | calendar, booking, optimization, project systems | PASS WITH HARDENING | adapt operational abstraction, not their taxonomy |
| CORE-08 Anti-pattern review | Yes | universal resources table/root, `resource_id` everywhere, anything-useful category | PASS | rejected |
| CORE-09 Correction/reconciliation | Yes | wrong allocation, substitution, candidate mismatch | PASS WITH HARDENING | changes do not rewrite earlier plan/history |
| CORE-10 Scale/performance/history | Yes | pools, many candidates, capacity, supply | PASS WITH HARDENING | no forced per-unit identity or eager expansion |
| CORE-11 Simple vs power user | Yes | ordinary user sees `camera`, `room`, `who's available?` | PASS | ontology term can remain hidden |
| CORE-12 Product value/complexity cost | Yes | common planning logic across heterogeneous providers | PASS | role delivers reuse without entity cost |
| CORE-13 Implementation pressure | Yes | heterogeneous references, eligibility, capacity, allocation | PASS WITH HARDENING | logical representation deferred; no universal FK pre-approved |

Core Gate verdict: **PASS WITH HARDENING**.

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| MA-01 Identity/account independence | Yes | non-account Person/service/resource | PASS | Resource role independent of Account |
| MA-02 Shared canonical fact / actor overlay | Yes | shared camera/room with personal preferences | PASS | one native identity, actor-scoped overlays allowed |
| MA-03 Responsibility/assignment/claim | Yes | required Person vs responsible actor vs performer | PASS WITH HARDENING | Resource does not absorb Responsibility |
| MA-04 Stewardship/mental load | Yes | allocator/maintainer/user differ | PASS | no stewardship inference |
| MA-05 Common ground/state separation | Yes | actors disagree on suitability/availability | PASS | shared identity does not force one opinion |
| MA-06 Authority/canonical change | Yes | allocation rights differ | PASS WITH HARDENING | Resource role grants no Authority |
| MA-07 Selective disclosure | Yes | private availability/reason/location | PASS WITH HARDENING | free/busy projection may hide source |
| MA-08 Inference privacy | Yes | AI candidate ranking from private data | PASS WITH HARDENING | suitability inference != disclosure permission |
| MA-09 Partial adoption/external participant | Yes | external contractor/service | PASS | no synthetic Account needed |
| MA-10 Assisted participation/provenance | Yes | caregiver/assistant allocates for another | PASS | actor and Resource remain distinct |
| MA-11 Relationship lifecycle/revocation | Yes | shared resource access revoked | PASS | current access != native identity/history |
| MA-12 Conflict/adversarial relationship | Yes | disputed booking/ownership/access | PASS | relations can conflict without duplicate Resource identity |
| MA-13 Unequal power | Yes | employer equipment / caregiver schedule | PASS WITH HARDENING | access/Authority separately modeled |
| MA-14 Multi-resource/capacity | Yes | pool + concurrent capacity | PASS WITH HARDENING | core reason Resource semantics exist; pool mechanics deferred |
| MA-15 Coordination burden | Yes | allocator/maintainer/performer differ | PASS | burden not inferred from resource role |
| MA-16 Formality/progressive disclosure | Yes | personal simple use vs formal booking | PASS | kernel semantics can stay hidden |
| MA-17 AI authority/multi-party context | Yes | AI proposes allocation | PASS WITH HARDENING | optimizer does not gain Authority |
| MA-18 Specialist-system boundary | Yes | rooms/equipment/workforce adapters | PASS | map without importing external taxonomy |
| MA-19 Multi-actor primitive redundancy | Yes | universal Resource entity | PASS | rejected |
| MA-20 Actor-scoped reality attribution | Yes | planned/actual use differ by actor/context | PASS | separate roles/history preserved |

Multi-Actor Gate verdict: **PASS WITH HARDENING**.

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---|---|---|
| XCON-01 Identity compatibility | Yes | PASS | Resource role does not replace Person/Asset/native identity |
| XCON-02 Ownership/authority compatibility | Yes | PASS | no ownership/Authority implied |
| XCON-03 Planned/current/actual/history compatibility | Yes | PASS WITH HARDENING | allocation/reservation/actual use remain distinct |
| XCON-04 Relationship compatibility | Yes | PASS WITH HARDENING | Requirement/Allocation/Reservation/Performer remain typed future semantics |
| XCON-05 Multi-actor readiness compatibility | Yes | PASS | shared Resource and actor-scoped state compose |
| XCON-06 Language-map compatibility | Yes | PASS | Resource may remain hidden implementation/domain language |

Cross-Concept Gate verdict: **PASS WITH HARDENING**.

---

# 7. Adversarial reductio

## REMOVE Resource entity

Native Person/Asset/Place/service/supply identities remain; planning relations can reference them directly.

**Result:** PASS.

## REMOVE Resource semantics

LifeOS loses a common way to reason about heterogeneous eligibility, availability/capacity and candidate allocation.

**Result:** FAIL.

## Resource = Asset

People, rooms, services and supplies fail.

**Result:** FAIL.

## Resource = Person

Equipment/place/service/supply fail.

**Result:** FAIL.

## Resource = Subject

Aboutness and execution eligibility differ.

**Result:** FAIL.

## Resource = Actor

Agency and capacity/supply differ.

**Result:** FAIL.

## Resource = Requirement

Need and provider collapse; late binding becomes impossible.

**Result:** FAIL.

## Resource = Allocation / Reservation

Eligibility and current selection/claim collapse.

**Result:** FAIL.

## Resource = anything useful

The concept becomes semantic-free and absorbs information, money, Evidence and arbitrary context.

**Result:** FAIL.

## Resource as contextual planning/execution role

All representative workflows survive without duplicate identity.

**Result:** PASS.

---

# 8. Adjacent Dependency Sweep

| Dependency / boundary | Closure class | Current resolution / why safe | Owner / future stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|
| Resource vs Asset | RESOLVED at current baseline | Asset may play Resource role; identity remains Asset | current + mandatory Asset revisit | Asset re-review yields incompatible shared abstraction | CORE-03, CORE-04, XCON-01, XCON-04 |
| Resource vs Person | RESOLVED | Person may play role; native identity unchanged | current | future workforce semantics require Resource identity to replace Person | CORE-03, MA-03, XCON-01 |
| Resource vs Subject | RESOLVED | execution supply != descriptive aboutness | current | future model collapses them without loss | CORE-04, XCON-01 |
| Resource vs Actor | RESOLVED | operational eligibility != agency | current | action/capacity cases cannot be separated | CORE-04, XCON-01 |
| Resource vs Availability/Capacity | RESOLVED | schedulable Resource-role cases bear availability/capacity | current Resource + Time cluster | Time model requires dedicated Resource entity | CORE-04, CORE-13, MA-14, XCON-04 |
| Resource Requirement | SAFE DEFERRED | need/provider separation fixed without final object shape | Relationships / Reasoning + planning model | abstract need/late binding cannot be represented | CORE-03, CORE-04, CORE-05, CORE-13, XCON-04 |
| Allocation / Reservation / Claim | SAFE DEFERRED | selection/holding is separate from eligibility | Relationships + scheduling logical model | requires identity model conflicting with Resource role | CORE-02, CORE-04, MA-14, XCON-03, XCON-04 |
| actual resource use / consumption | SAFE DEFERRED | planned allocation != actual use already fixed | Actual/Session + future typed relations/inventory | actual-use history cannot be reconstructed | CORE-02, CORE-05, XCON-03 |
| consumable supply / inventory | SAFE DEFERRED | supply can satisfy requirement without per-unit identity | future concrete workflow | quantity/movement semantics cannot compose | CORE-03, CORE-04, CORE-10, CORE-12, CORE-13 |
| Place / Location | SAFE DEFERRED | Place may play Resource role | future Place/Location | booking/location identity conflicts | CORE-04, MA-14, XCON-01, XCON-04 |
| service / capability / skill | SAFE DEFERRED | criterion/provider distinction preserved | Relationships / specialist planning | repeated workflows expose missing native concept | CORE-03, CORE-04, CORE-06, CORE-12 |
| Authority / Visibility / access | SAFE DEFERRED | Resource grants none | Relationships / Reasoning | allocation rights require Resource-owned authority | MA-06, MA-07, MA-13, MA-17, XCON-02 |

No current dependency is a structural blocker.

---

# 9. Representative scenarios

## Camera late binding

```text
Requirement: suitable camera
Candidates: A17 / A18
Allocation: A17
Reservation: A17 17:00–20:00
Actual use: A18
```

**PASS WITH HARDENING** — distinct phases/history preserved.

## Person with qualification

```text
Requirement: Japanese B2+
Candidates: Person A / Person B
```

**PASS** — skill is criterion, Persons may play Resource role; no Resource wrapper.

## Room booking

```text
Room 3
native Place/Room semantics
Resource role for Workshop
capacity 20
```

**PASS** — bookability does not require Resource identity.

## Shared camera

One Asset shared by several actors with different visibility/allocation rights.

**PASS WITH HARDENING** — Resource role grants no Authority.

## Consumable supply

```text
Maintenance requires 500 ml oil
```

**PASS WITH DEFERRED DEPENDENCY** — supply may satisfy requirement without per-unit Resource identity; inventory semantics remain future work.

## Budget

```text
Trip budget €500
```

**PASS** — financial constraint not automatically Resource.

---

# 10. Concept verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Accepted baseline

```text
RESOURCE
CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY
NOT AN ENTITY / ROOT

native referent / service / pool / supply
        ↓ contextual Resource role
may satisfy execution requirement
```

## Hardenings incorporated

1. Resource role does not create identity.
2. Resource != Person/Asset/Subject/Actor.
3. Requirement != selected Resource.
4. candidate != Allocation != Reservation != actual use.
5. schedulable Resource is only the subset where time-dependent Availability/Capacity matters.
6. more precise human roles such as Performer/Responsibility remain preferable when known.
7. consumable supply does not require per-unit identity.
8. Money/Budget are not Resource by default.
9. Resource eligibility is contextual to requirements.
10. Authority/Visibility/access are separate.
11. AI optimization does not grant allocation Authority.
12. no universal `resources` table/root or `resource_id` shortcut is pre-approved.

---

# 11. Mandatory future re-tests

1. Data / Subjects cluster integration.
2. Cluster-4 multi-actor stress.
3. mandatory terminology-neutral Asset revisit — confirm Resource composes with any Asset revision.
4. Resource Requirement / Allocation / Reservation during Relationships / Reasoning.
5. Availability/Capacity regression under Resource semantics.
6. Person/Performer/Responsibility regression.
7. Place/Location and inventory/supply if concrete workflows justify them.
8. logical data model heterogeneous references/pools/capacity.
9. Deferred Dependency Closure clusters 1–4.
10. Cross-Cluster Validation v4.

---

# 12. Documentation propagation

Before closing:

- [x] Resource concept created;
- [x] Availability & Capacity aligned;
- [x] Asset aligned;
- [x] Subject aligned;
- [x] Person aligned;
- [x] Language Map updated;
- [x] Domain README updated;
- [x] workstream handoff updated;
- [x] Resource entity/root rejected;
- [x] Requirement/Allocation/Reservation/actual-use boundaries recorded;
- [x] dependency owners/reopening triggers recorded.

Resource v0 propagation is complete. The next action is the **Data / Subjects Cluster Integration Gate + Cluster Multi-Actor Stress Gate in read-only mode**; no Cluster-4 checkpoint write is authorized by this scope.