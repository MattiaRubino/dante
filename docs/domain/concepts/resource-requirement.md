# Resource Requirement v0

**Status:** ACCEPTED v0 — PASS WITH HARDENING  
**Accepted:** 2026-08-15  
**Cluster:** Relationships / Reasoning  
**Validation:** `../checkpoints/resource-requirement-allocation-v0-validation.md`

## Definition

> **Resource Requirement is the contextual semantic specification of what a bounded planning or execution context needs from Resource-capable providers, capacity, services, pools or supply without identifying the provider merely by expressing the need.**

It answers:

> **What does this bounded context need in order to be satisfiable or executable?**

A Resource Requirement may include, where materially relevant:

- capability or qualification;
- compatibility;
- quantity;
- location or spatial condition;
- temporal or capacity need;
- supply characteristics;
- other bounded eligibility requirements.

The requirement may be explicit and independently reconstructible where consequence/history requires it, or remain implicit/reconstructible in simple low-consequence flows. Acceptance of the semantics does **not** require a universal Requirement entity, root, table or user-visible object.

---

## 1. Core boundary

```text
Resource Requirement != Resource
Resource Requirement != Request
Resource Requirement != Criterion
Resource Requirement != Quantity
Resource Requirement != Temporal Constraint
Resource Requirement != Availability
Resource Requirement != Candidate Set
Resource Requirement != Resource Allocation
```

Criterion, Quantity, Temporal Constraint, Availability/Capacity and other accepted semantics may contribute to describing or evaluating a Requirement without being absorbed by it.

A `Request` may ask another Actor/system to provide, satisfy or respond about a Resource Requirement, but the semantic ask is not the need itself.

---

## 2. Requirement and provider identity

A Requirement does not manufacture provider identity.

```text
Requirement: qualified Japanese interpreter
```

may later be satisfied by a Person, service or other independently justified provider. The Person/service identity remains its own identity; `Resource` remains a contextual role/capability.

Likewise:

```text
Requirement: 500 ml oil
```

does not require per-unit Asset or Resource identity.

---

## 3. Requirement and candidate set

Candidate Set is a contextual/derived eligibility view by default.

```text
Requirement R1
→ candidates A17, A18, Service Z
```

If new information makes A18 ineligible:

```text
candidates A17, Service Z
```

that change alone does not revise Requirement identity or material state.

Canonical rule:

```text
candidate-set change
!= Requirement revision automatically
```

Candidate matching/ranking may use Criterion/Evaluation, private facts, Availability/Capacity, qualifications and other context. The derived set does not become a universal primitive or source of provider identity.

---

## 4. Material state and Version

A Requirement may change materially while preserving or replacing its identity according to the owning context.

Example:

```text
R1: camera suitable for original specification
→ material change
R2-state: original specification + 8K 60fps
```

Version / Material-State provides state-binding discipline but does not decide Requirement identity universally.

Canonical rule:

> **The owning context determines whether a change preserves Requirement identity; Version must not hide a semantically new Requirement.**

Where consequence requires it, previous Allocations remain bound to the materially relevant Requirement state they actually addressed.

---

## 5. Lifecycle and history

A Requirement may exist with:

```text
Candidate Set = none
Allocation    = none
Capacity Claim = none
Actual use    = none
```

This is valid.

Requirement withdrawal or expiry changes future applicability; it does not erase truthful historical Allocation, Capacity Claim, Actual use, Decision, Proposal/Request, Provenance or related history.

No universal cascade is defined.

---

## 6. Multi-actor semantics

A shared Requirement does not imply:

- identical candidate sets for every Actor;
- identical visibility into eligibility reasons;
- identical preferences or rankings;
- Agreement or Consent;
- Responsibility;
- Authority to allocate;
- one shared response.

Private qualifications or constraints may affect an authorized bounded candidate/result projection without granting visibility to the underlying private information.

External/accountless Persons or providers remain representable.

---

## 7. AI boundary

AI may:

- identify candidate providers;
- evaluate compatibility;
- rank candidates;
- explain a bounded match where visibility permits;
- propose a Resource Allocation.

AI matching/ranking does not itself create:

```text
Resource Allocation
Authority
Responsibility
Participation
Agreement
Consent
Actual use
```

Private eligibility data used internally does not become disclosure permission.

---

## 8. Persistence guardrail

Resource Requirement is canonical semantic capability/family, not a mandatory persistence root.

Simple flow:

```text
Activity: Photo shoot
Use: Sony A7 IV
```

may preserve sufficient Requirement semantics without materializing separate Requirement/Candidate/Allocation records when no consequential distinction would be lost.

Materialize/reconstruct richer Requirement state where needed for:

- alternatives/late binding;
- history;
- material versioning;
- multi-actor coordination;
- governance;
- privacy/explanation;
- capacity planning;
- reconciliation;
- consequential queryability.

---

## 9. Canonical invariants

```text
Requirement may exist without candidates or Allocation
Requirement need not be a standalone persisted object in simple cases
Candidate Set is contextual/derived by default
candidate-set change != Requirement revision automatically
material Requirement change != automatic carry-forward of prior Allocation
Requirement does not manufacture Resource/provider identity
Requirement != Request
Requirement != Resource
Requirement != Criterion
Requirement != Temporal Constraint
Requirement != Allocation
no universal Requirement root/table/state machine
persistence/materialization is consequence-sensitive
```

---

## 10. SAFE DEFERRED neighbors

Independently owned future work remains:

- Requirement composition (`all` / `any` / alternatives / cumulative satisfaction);
- exact candidate matching/ranking expression;
- pool and late-binding logical mechanics;
- Place / Service / Skill native semantics;
- exact logical/persistence/API representation;
- inventory/supply semantics where non-temporal stock behavior is required.

These deferrals do not weaken the accepted Resource Requirement boundary. Reopen only if those workflows cannot be represented without changing the semantics above.