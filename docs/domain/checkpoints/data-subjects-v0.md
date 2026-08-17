# Data / Subjects Cluster v0 — Integration Checkpoint

**Status:** PASS WITH HARDENING — current validated cluster baseline  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Branch:** `feature/domain-model`

## 1. Scope

This checkpoint integrates the Data / Subjects candidate reviews as one semantic cluster. It does not treat the candidate list as a checklist of primitives that had to survive.

Reviewed outcomes:

- Quantity — accepted canonical value semantics;
- Register / RegisterEntry — kernel candidates rejected; longitudinal product/query need retained;
- Subject — accepted contextual aboutness role, no Subject entity/root;
- Person — accepted native human entity;
- Actor — accepted contextual agency role/capability, no Actor entity/root;
- Account — conceptual platform/access identity boundary accepted; detailed security model deferred;
- Asset — accepted current scoped native physical-object identity, after mandatory terminology-neutral re-review;
- Resource — accepted contextual planning/execution role/capability, no Resource entity/root.

The integration goal is to verify that these decisions reconstruct real workflows without duplicate identity, semantic wrappers, or one universal managed-object/user/resource hierarchy.

---

## 2. Integrated topology

```text
VALUE SEMANTICS
Quantity

NATIVE IDENTITIES / REFERENTS
Person
Asset — current scoped physical-object baseline
future native referents only when independently justified

CONTEXTUAL ROLES
Subject  — descriptive aboutness
Actor    — meaningful agency category expressed through specific action roles
Resource — planning/execution eligibility/capability

PLATFORM / SECURITY BOUNDARY
Account — access identity; detailed model deferred
Principal — deferred security/authorization identity

LONGITUDINAL PRODUCT CAPABILITY
native records
→ query/filter/group
→ valid aggregate/trend/comparison
→ Tracker / History / Progress / Register UI
```

No line above implies inheritance, one persistence root, one generic foreign key, or one mandatory UI noun.

---

## 3. Cluster Integration Gate

| Test | Representative pressure | Result | Finding / hardening |
|---|---|---|---|
| CL-01 Representative reconstruction | self-tracking, caregiver, camera history/use, booking, tracker | PASS | all reconstruct without new wrapper entities |
| CL-02 Deep chronology | Account lifecycle, Subject correction, Asset lifecycle, Resource substitution | PASS | native identity and plan-vs-actual history remain reconstructable |
| CL-03 Redundancy / destructive test | remove Register/Subject entity/Actor entity/Resource entity; merge Person/Asset/roles | PASS WITH HARDENING | semantic roles survive while wrapper identities remain unnecessary |
| CL-04 Top-down traceability | Goal/Plan → execution → resource need → reality/evidence | PASS | Cluster-4 semantics compose with Clusters 1–3 |
| CL-05 Bottom-up reconstruction | raw Observation/Quantity/Subject/Provenance → optional evaluation/view | PASS | no fake Activity/Actual/Register required |
| CL-06 Lateral propagation | account deletion, asset sale, resource substitution, display conversion | PASS | changes do not silently mutate unrelated identity/roles |
| CL-07 History / correction | wrong Subject, duplicate provider representation, allocation substitution | PASS WITH HARDENING | prior attribution/plan remains historically explainable |
| CL-08 Scale / product complexity | high-volume observations, stock/supply, resource pools, many contacts/assets | PASS WITH HARDENING | no eager wrapper/per-unit identity requirement |

Cluster Integration Gate verdict: **PASS WITH HARDENING**.

---

## 4. Multi-Actor Stress Gate

Representative cases:

### Caregiver measurement

```text
Person Maria
  ↑ Subject role
Observation: temperature 38.2 °C

Person Anna
  ↓ recorder role / Actor semantics

Account Anna-A1
  ↓ authentication context
```

**PASS** — Subject, Actor, Person and Account remain independent.

### Shared Asset

```text
Asset A17
shared camera

owner / holder / maintenance steward / allocation authority / viewers
= separate relationships/policies
```

**PASS WITH HARDENING** — one Asset identity does not imply universal visibility or authority.

### Shared Resource

One native Person/Asset/Place may be resource-eligible while different actors have different visibility, preference, allocation rights, or private reasons for unavailability.

**PASS WITH HARDENING** — Resource role grants no authority or disclosure rights.

### Non-account participant / actor

External people and services can remain historical Participants/Actors/Subjects without synthetic Accounts.

**PASS**.

Multi-Actor Stress Gate verdict: **PASS WITH HARDENING**.

---

## 5. Key integrated hardenings

### H1 — Actor is agency semantics, not a generic relationship

The cluster destructive test confirms that agency is a useful cross-cutting semantic category, but ordinary records should use the most specific meaningful role when known:

```text
recorded_by
performed_by
observed_by
confirmed_by
proposed_by
transformed_by
```

Do not replace these with one semantic-free `actor_id` edge.

### H2 — Resource never manufactures identity

Resource semantics may apply to:

- native Person/Asset/future Place/service identities;
- pools or supplies that have their own independently justified semantics;
- consumable quantities where no per-unit identity exists.

Canonical hardening:

> **A Resource role preserves whatever native identity, value, pool, supply, or service semantics the provider independently has; Resource itself does not manufacture identity.**

Therefore `500 ml oil` need not acquire a domain ID merely because it satisfies a Requirement.

### H3 — Requirement, candidate, allocation, reservation and actual use stay separable

```text
Requirement
→ candidate(s)
→ allocation
→ reservation / claim
→ actual use / consumption
```

Simple flows may collapse these operationally, but the kernel must not make them one fact.

### H4 — Longitudinal views remain projections over native records

Register rejection survives cluster integration. Deleting/reconfiguring a tracker/view does not delete or rewrite native Observation/Session/future specialist records.

### H5 — role eligibility does not justify a universal root

A Person may play Subject, Actor and Resource roles without becoming a `Party`, `Subject`, `Actor` or `Resource` wrapper. An Asset may play Subject and Resource roles without inheritance from either.

---

## 6. Terminology-neutral Asset re-review

The mandatory re-review was executed before treating this cluster as consolidated.

The question used was not “how do other applications define Asset?” but:

> **How do mature systems represent things that people identify, manage, monitor, use, possess, locate, share, book, consume, or relate to — and which structures are actually persistent source semantics?**

Cross-domain benchmark families included:

- smart-home/device systems;
- personal possessions and equipment/inventory;
- product/inventory systems;
- property/place patterns;
- document/storage systems;
- financial accounts;
- living-subject/patient patterns;
- services/subscriptions.

### Result

A universal `ManagedObject` abstraction did **not** emerge as the stronger LifeOS model.

The recurring useful pattern was instead:

```text
native identity appropriate to the domain
+
typed relationships
+
contextual roles/capabilities
+
domain-specific lifecycle
+
shared query/UI where useful
```

Current Asset semantics still add independent value for individually tracked physical objects whose specific identity/history materially matter.

Therefore:

```text
broad ManagedObject root          REJECTED
current physical-object identity  RETAINED
exact internal noun `Asset`       NON-SEMANTIC / reopenable naming choice
```

The deeper future discussion may still revisit the naming or boundary if new workflows show a stronger abstraction. This checkpoint does not make the word `Asset` immutable.

---

## 7. Destructive cross-concept tests

### Person = Account

**FAIL** — external/non-account humans and access lifecycle break.

### Person = Subject / Actor / Resource

**FAIL** — identity and contextual role collapse.

### Asset = Subject / Resource

**FAIL** — identity/history differ from aboutness and execution eligibility.

### Subject / Actor / Resource as wrapper entities

**FAIL** — duplicate identity with no additional domain truth.

### Register as universal longitudinal container

**FAIL** — duplicates native records and ownership/history.

### Quantity as entity or universal number

**FAIL** — value semantics become over-broad and contextual truth is duplicated.

### Universal managed-object root

**FAIL** — Person, living things, documents, financial accounts, services, places and physical objects lose materially distinct semantics.

---

## 8. Cluster verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

```text
DATA / SUBJECTS v0
PASS WITH HARDENING

structural reopenings: 0
mandatory new primitives from integration: 0
kernel candidate removals retained: Register, RegisterEntry, Subject entity/root, Actor entity/root, Resource entity/root
```

The cluster is now a validated current baseline, but Relationships / Reasoning may reopen a boundary if its mandatory Adjacent Dependency Sweep finds stronger evidence.

---

## 9. Mandatory transition gates

Completed or separately recorded immediately after this checkpoint:

1. Deferred Dependency Closure — Clusters 1–4;
2. Cross-Cluster Validation v4 — Clusters 1–4.

Only after those pass may the workstream begin Relationships / Reasoning.

---

## 10. Documentation propagation

- [x] Quantity decision retained;
- [x] Register rejection retained;
- [x] Subject/Person/Actor/Account boundaries retained;
- [x] Asset terminology-neutral re-review completed and recorded;
- [x] Resource decision retained;
- [x] Actor hardening recorded;
- [x] Resource identity hardening recorded;
- [x] deferred-dependency closure prepared;
- [x] Cross-Cluster v4 prepared;
- [x] Language Map / Domain README / workstream aligned in the same approved write scope.
