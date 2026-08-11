# Multi-Actor Evidence Synthesis Checkpoint v0

**Status:** PASS — evidence-backed multi-actor readiness baseline  
**Date:** 2026-08-11  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Scope

This checkpoint reconciles four evidence layers:

1. the accepted Intention & Execution v0 cluster;
2. the accepted Time v0 cluster;
3. the initial Multi-Actor Readiness v0 stress pass;
4. the completed multi-actor discovery simulation and consolidated external Deep Research integrated into `main`.

The purpose is not to design the complete collaboration subsystem.

The purpose is to answer:

> **Do the first two accepted Domain Atlas clusters remain structurally sound when tested against broad, independently produced multi-actor evidence, and what cross-cutting hardenings must become mandatory before later clusters are modeled?**

---

# 1. Evidence sources

## Domain baseline

- `../concepts/goal.md`
- `../concepts/plan.md`
- `../concepts/activity.md`
- `../concepts/event.md`
- `../concepts/routine.md`
- `../concepts/milestone.md`
- `../concepts/occurrence.md`
- `../concepts/schedule.md`
- `../concepts/session.md`
- `../concepts/temporal-constraint.md`
- `../concepts/recurrence.md`
- `../concepts/availability-capacity.md`
- `intention-execution-v0.md`
- `time-v0.md`
- `cross-cluster-validation-v2.md`

## Multi-actor readiness baseline

- `../multi-actor-readiness-v0.md`
- `multi-actor-readiness-v0.md`

## New discovery evidence

- `../../product/multi-actor-collaboration-discovery-simulation-2026-08.md`

The simulation covers casual social planning, household coordination, work/team use, shifts, caregiving, education, professional services, creative work, shared resources, healthcare-adjacent coordination and complex institutional stress cases.

## New external evidence

- `../../product/multi-actor-collaboration-research-2026-08.md`

The research spans CSCW/groupware, coordination theory, common ground, calendar privacy, household mental load, work/shift fairness, caregiving, healthcare, education, shared expenses, external participation, privacy-by-design, authorization feasibility, adversarial exits, high-conflict relationships, minors/guardian asymmetry, accessibility/low digital literacy and multi-party AI privacy.

---

# 2. Method

The synthesis did **not** promote research vocabulary directly into domain primitives.

Each finding was classified as one of:

- confirms an existing invariant;
- requires a cross-cutting hardening;
- requires a later concept review;
- creates a product/validation requirement only;
- contradicts the current model;
- does not justify kernel adoption.

The first two clusters were tested against these questions:

```text
Does object identity depend on one user/account?
Can shared canonical state coexist with actor-private state?
Can owner, participant, responsible actor, performer and subject differ?
Can actors participate without LifeOS accounts?
Can participation and responsibility change without replacing the object?
Can availability be coordinated without exposing private reasons?
Can proposal, agreement, authority and Actual remain distinct?
Can responsibility be claimable/delegated/substituted?
Can access end while historical attribution remains?
Does the current Time model support multiple people/resources without cloning Schedule?
Does Session remain coherent with collaborative execution?
Does any current concept require split/merge/removal?
```

Adversarial cases included:

- dinner with friends;
- recurring group activity;
- household chore rotation;
- open/claimable care task;
- work meeting;
- project review/approval;
- shift swap;
- caregiver hand-off;
- parent/guardian/child coordination;
- shared vehicle/resource;
- external technician/client appointment;
- surgical-operation coordination stress case;
- participant without LifeOS;
- private-calendar availability computation;
- high-conflict ongoing collaboration;
- emergency access revocation;
- assisted low-digital-literacy participant;
- AI mutual-time recommendation from private inputs.

---

# 3. Overall result

```text
Intention & Execution v0
PASS
no structural reopening

Time v0
PASS
no structural reopening

Multi-Actor Readiness
PASS WITH HARDENING
```

Results:

- **0 concepts removed**;
- **0 concepts merged**;
- **0 concepts split into mandatory new primitives**;
- **0 new mandatory domain primitives introduced by the evidence synthesis**;
- several cross-cutting guardrails strengthened;
- several future concept reviews raised in priority;
- three existing canonical definitions require actor-neutral wording hardening (`Goal`, `Activity`, `Routine`) without changing their semantics.

---

# 4. Strong confirmations

## 4.1 Shared canonical fact + personal overlay

The strongest multi-actor finding independently confirms the initial readiness direction.

One dinner, meeting, trip, shift or appointment should normally remain one canonical shared object while each actor maintains personal context.

This avoids per-user semantic duplication and preserves independent personal LifeOS models.

**Classification:** CONFIRMED — promote to current cross-cutting invariant.

---

## 4.2 Account is not actor/person identity

Partial adoption and external participants occur across nearly every scenario family.

Requiring every participant to become a full LifeOS account would fail ordinary social, family, client, supplier, professional and care coordination.

**Classification:** CONFIRMED — retain non-collapse rule; final Actor/Person/Account/Principal model deferred.

---

## 4.3 Participation is not Event identity

The existing Event model already separates Event state, participant response and actual attendance.

The research strongly reinforces this separation.

**Classification:** EXISTING MODEL STRONGLY CONFIRMED.

---

## 4.4 Schedule is not participant acceptance

A shared Event can have one current Schedule while participants accept, decline or remain tentative independently.

Shift swaps further demonstrate that actor assignment may change while the underlying scheduled shift occurrence does not move.

**Classification:** EXISTING MODEL STRONGLY CONFIRMED.

---

## 4.5 Schedule is not Capacity

Multi-person/resource coordination makes the existing separation more valuable.

One Event Schedule can produce independent claims on:

```text
Actor A
Actor B
Room
Vehicle
Equipment
```

A declined participant may no longer consume their capacity while the Event remains scheduled.

**Classification:** EXISTING MODEL STRONGLY CONFIRMED.

---

## 4.6 Occurrence identity is not assignment

Recurring household work, shift rotation and recurring shared activities show that performer/responsibility may change per Occurrence without requiring duplicate Routines or new occurrence identities.

**Classification:** CONFIRMED HARDENING.

---

## 4.7 Planned participation is not Actual participation

Acceptance, expected attendance and reality differ materially.

The existing LifeOS rule `planned != actual` generalizes cleanly to multi-actor participation.

**Classification:** EXISTING MODEL STRONGLY CONFIRMED.

---

## 4.8 Resource capacity belongs beside actor coordination

Rooms, vehicles, equipment, tickets and facilities repeatedly appear as dependency sources.

The current Availability/Capacity resource-oriented model remains structurally appropriate.

**Classification:** EXISTING MODEL CONFIRMED; Resource identity review remains downstream.

---

# 5. New hardenings promoted by evidence

## 5.1 Responsibility is richer than one assignee

Across household, work, care, shifts and services, responsibility can involve:

- accountability;
- expected performer;
- open/claimable work;
- approval;
- substitution;
- hand-off;
- fallback responsibility.

This does not yet prove one universal Responsibility primitive.

**Decision:** future Relationship/Responsibility review is mandatory; current Activity identity remains independent from assignee/performer.

---

## 5.2 Coordination stewardship is distinct from visible execution

External household/mental-load evidence adds a distinction not sufficiently explicit in the initial readiness pass.

Assignment can transfer execution while anticipation, reminding, monitoring and repair remain with another person.

**Decision:** preserve as a mandatory validation dimension. Do not canonize `Stewardship` as a primitive yet.

---

## 5.3 Common ground is richer than delivery

The evidence supports:

```text
sent
!= seen
!= understood
!= acknowledged
!= accepted/agreed
!= authoritative/confirmed
!= acted upon
!= Actual
```

**Decision:** preserve these semantic separations where consequence warrants them. Do not expose universal acknowledgement workflows for ordinary low-consequence life.

---

## 5.4 Access lifecycle and historical attribution differ

Joining/leaving is insufficient.

Required future semantic capability includes:

- scoped sharing;
- reduced sharing;
- temporary access;
- future revocation;
- emergency revocation where appropriate;
- preservation of historical attribution;
- continuation of real-world obligations independent from access.

**Decision:** promote to cross-cutting guardrail; exact authorization/access model deferred.

---

## 5.5 Privacy includes derived inference

Hiding raw fields does not prevent leakage through explanation, recommendation, availability, notification or AI tool calls.

**Decision:** future privacy/access and AI Context Builder reviews must distinguish raw visibility from inferential disclosure.

---

## 5.6 Creator does not inherit social authority

Creating a shared object must not automatically make the creator authoritative over every participant or every fact.

**Decision:** promote to authority guardrail.

---

## 5.7 Coordination burden must be evaluated per actor

CSCW evidence shows that organizer convenience can become participant bureaucracy.

**Decision:** add coordination-burden distribution to product/domain validation. This is a validation requirement, not necessarily a persisted domain concept.

---

## 5.8 Participation capability is a spectrum

Useful future flows must tolerate full users, occasional users, bounded responders, assisted users and represented non-interacting subjects.

**Decision:** product/identity requirement; no mandatory channel implementation selected.

---

# 6. Findings deliberately NOT promoted to primitives

The evidence does **not** justify creating the following now:

```text
Actor table
Person table
Organization hierarchy
Team hierarchy
Household aggregate
Universal Group entity
Universal Participant entity/state machine
Universal Responsibility workflow
Stewardship entity
ACL/RBAC/ReBAC system
Zanzibar/OpenFGA dependency
Chat/message system
Universal approval engine
Universal fairness score
Universal audit log visible to collaborators
AI multi-agent orchestration
```

Each may later be justified, but none is required merely because research discusses it.

---

# 7. Concept-by-concept compatibility

## Goal — PASS WITH WORDING HARDENING

Problem in current wording:

```text
the user intentionally wants...
```

This is correct for personal V1 but too narrow as a canonical identity definition.

Required hardening:

- define the desired outcome independent from one mandatory user owner;
- keep governance/stakeholder/subject/contributor relationships separate;
- do not require multiple copies of one genuinely shared Goal.

No semantic split required.

---

## Plan — PASS

Plan already represents coordinated pursuit/organization rather than one user's execution identity.

Hardening:

- coordinator, contributors and responsible actors remain relationships;
- shared Plan governance remains deferred.

No structural change.

---

## Activity — PASS WITH WORDING HARDENING

Problem in current canonical wording:

```text
the user intends to perform
```

This incorrectly implies intention-holder = performer.

Required hardening:

- Activity represents actionable intended work;
- requester/responsible actor/assignee/performer/subject remain separable;
- assignment changes do not change Activity identity;
- open/claimable responsibility must remain possible later.

No split required.

---

## Event — PASS

Already naturally multi-actor.

Strong confirmations:

- organizer != participant;
- participant response != Event state;
- response != Actual attendance;
- Event shared facts may coexist with personal overlays;
- Schedule may remain shared while actor capacity impact differs.

No structural change.

---

## Routine — PASS WITH WORDING HARDENING

Problem in current canonical wording:

```text
behavior the user intends to repeat
```

Required hardening:

- repeating policy is independent from one mandatory performer;
- performer/responsibility can rotate by Occurrence;
- observed repeated behavior remains distinct from intended Routine.

No split required.

---

## Milestone — PASS

Milestone identity remains contextual checkpoint identity.

Approver/stakeholder/governor relations can vary independently.

No structural change.

---

## Occurrence — PASS

Assignment/performer changes do not alter expected-instance identity.

No structural change.

---

## Schedule — PASS

Shared canonical Schedule is compatible with actor-specific participation and capacity claims.

Important hardening:

```text
accepted Schedule != every participant accepted
```

No structural change.

---

## Session — PASS WITH DOWNSTREAM WATCH

Collaborative execution is representable as one logically continuous Session plus actor-specific execution participation where appropriate.

Independent simultaneous attempts may remain separate Sessions.

Exact actor-specific Actual/participation persistence must be resolved downstream.

No new Time primitive required.

---

## Temporal Constraint — PASS

Constraint scope and authority are separable.

Multi-actor scheduling may contain constraints on people, resources, joint timing or dependencies, but no new temporal ontology is required.

---

## Recurrence — PASS

Responsibility rotation is not recurrence identity.

Recurrence may help express repeated assignment policy later, but must not become a generic actor-allocation engine.

---

## Availability & Capacity — PASS

Already resource-oriented and therefore naturally compatible with multiple people and physical resources.

Private-source-to-safe-projection semantics becomes a stronger future privacy requirement.

---

# 8. Safety/adversarial validation

## Relationship exit

Passes conceptually only if future access is separable from historical attribution.

This is a future authority/visibility requirement, not a Time/Intention failure.

## High-conflict ongoing collaboration

Current shared-object + actor-scoped-state direction remains valid.

Future communication/audit features must avoid turning structure into a new conflict/surveillance surface.

## Guardian/minor

The evidence confirms that Actor/Subject/Authority/Visibility cannot be collapsed.

Exact legal authority is domain/jurisdiction-specific and deferred.

## Assisted user

The model must later preserve helper/source/subject distinctions through Provenance.

No first-two-cluster change required.

## AI privacy

Current AI boundary remains valid: AI access/knowledge does not create authority or disclosure permission.

Future Context Builder/tool schemas need dedicated privacy tests.

---

# 9. Terminology outcome

The synthesis exposed a documentation risk: domain, product, UI and implementation vocabulary can drift even when semantics are correct.

A new canonical quick-reference layer is therefore established:

- `../language-map.md`

It records:

- canonical terms;
- product profiles/aliases;
- UI exposure;
- frequently confused concepts;
- provisional/deferred terminology;
- terminology change policy;
- domain ↔ product ↔ UI mapping.

The old product glossary remains historical/product evidence where Domain Atlas decisions supersede it.

---

# 10. Current normative result

The evidence synthesis promotes `../multi-actor-readiness-v1.md` as the current multi-actor guardrail.

`multi-actor-readiness-v0.md` remains historical evidence of the earlier pre-research hardening rather than being silently overwritten.

This preserves the project rule:

> **new evidence may harden a decision, but history should remain reconstructible.**

---

# 11. Required downstream gates

From this checkpoint forward, every later concept review must include applicable multi-actor tests covering:

- shared vs actor-scoped truth;
- account-independent actors/subjects;
- responsibility/performer separation;
- authority/source distinction;
- availability without private-reason disclosure;
- proposal/acknowledgement/agreement/Actual distinctions;
- access/revocation lifecycle;
- partial/assisted participation;
- coordination burden per actor;
- inference privacy where AI is involved.

Particular downstream watchpoints:

```text
Actual / Outcome
Provenance / Confirmation / Evidence
Subject / Person / Actor
Resource
Relationship / Dependency
Responsibility / Hand-off
Authority / Visibility
Version / Decision
AI Proposal / Context Builder
```

---

# 12. Final checkpoint result

```text
MULTI-ACTOR EVIDENCE SYNTHESIS v0
PASS

Structural reopenings: 0
Concept removals:      0
Concept merges:        0
Mandatory new types:   0
Canonical wordings to harden: Goal, Activity, Routine
Cross-cutting guardrails strengthened: YES
New validation dimensions: YES
Full collaboration implementation selected: NO
```

The first two clusters remain valid current baselines.

The project can proceed to later Domain Atlas work after the approved terminology/documentation hardening, with multi-actor compatibility now treated as a permanent validation dimension.